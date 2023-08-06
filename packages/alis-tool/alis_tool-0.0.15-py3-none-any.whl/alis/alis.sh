#!/bin/bash

set -e

###################
####>> TOOLS <<####
###################

function arr_contains_el() {
  local ARGS=("$@")
  local arg
  for ((arg = 1; arg < "${#ARGS[@]}"; arg++)); do
    if [[ "${ARGS[$arg]}" == "${ARGS[0]}" ]]; then
      return 0 # emit no error
    fi
  done

  return 1 # emit error
}

function checkpoint_variables() {
  IFS=' ' read -r -a INITIAL_VARIABLES <<<"$(compgen -v | tr "\n" " ")"
}

function collect_variables() {
  IFS=' ' read -r -a FINALE_VARIABLES <<<"$(compgen -v | tr "\n" " ")"

  local VARIABLE
  local var
  for var in "${FINALE_VARIABLES[@]}"; do
    if ! arr_contains_el "$var" "${INITIAL_VARIABLES[@]}" && [[ "$var" != INITIAL_VARIABLES ]]; then
      VARIABLE="
        $VARIABLE
        $(declare -p | pcregrep -M " $var=((\(.*\))|(\"((\n|.)*?)\"))")
      "
    fi
  done

  echo "$VARIABLE"
}

function device_list() {
  local DEVICES
  DEVICES=$(lsblk | grep disk | awk -v FS=' ' '{print "/dev/"$1}' | tr "\n" " ")
  echo "$DEVICES"
}

function save_function() {
  local FN_NAME="$1"
  local NEW_FN_NAME="$2"
  local ORIG_FUNC
  ORIG_FUNC=$(declare -f "$FN_NAME")
  local NEW_NAME_FUNC="$NEW_FN_NAME${ORIG_FUNC#$FN_NAME}"
  eval "$NEW_NAME_FUNC"
}

function last_partition_name() {
  local DEVICE="$1"
  fdisk "$DEVICE" -l | awk 'END {print $1}'
}

function last_partition_end_mb() {
  local DEVICE="$1"
  parted "$DEVICE" unit MB print | awk '{if($1 ~ /[0-9]/) a=$3} {if(a == "") a="0%"} END {print a}'
}

function last_partition_end_number_parted() {
  local DEVICE="$1"
  parted "$DEVICE" print | awk '{if($1 ~ /[0-9]/) a=$1} {if(a == "") a="1"} END {print a}'
}

function add_mb() {
  echo "$1 $2" | awk -F'MB' '{print $1+$2 "MB"}'
}

function chroot_if_needed() {
  if [ "$(ls -A /mnt)" ]; then
    cp "$0" /mnt
    ARGUMENTS=$(printf '%q ' "$@")
    arch-chroot /mnt bash -c "/alis.sh $ARGUMENTS"
    rm /mnt/alis.sh

    return 0
  fi

  return 1
}

function user_chroot() {
  local RUNNING_USER="$1"

  if [[ "$USER" != "$RUNNING_USER" ]]; then
    echo "$RUNNING_USER ALL=(ALL) NOPASSWD: ALL" >/etc/sudoers.d/10_"$RUNNING_USER"
    chmod +x /etc/sudoers.d/10_"$RUNNING_USER"
    su "$RUNNING_USER" -c "$0 ${*:2}"
    rm -fr /etc/sudoers.d/10_"$RUNNING_USER"

    return 0
  fi

  return 1
}

function working_device() {
  local UUID
  local PARTITION
  local DEVICE
  UUID=$(< /etc/fstab awk -v FS='=| ' '{if($2 != "") a=$2}END{print a}')
  PARTITION=$(lsblk -no NAME,UUID | grep "$UUID" |awk '{print $1}' | grep -o -e '[0-9a-zA-Z]*')
  DEVICE=$(lsblk | grep disk | awk -v FS=' ' '{print $1}' | awk '{if("$PARTITION" ~ /$1.*/) a=$1} END {print a}')

  echo "$DEVICE"
}


###################
####<< TOOLS >>####
###################

function install_official_packages() {
  pacman -Sy --noconfirm "$@"
}

function install_yay_if_not_exist() {
  if ! pacman -Q | grep yay -q; then
    cd ~
    git clone https://aur.archlinux.org/yay-git.git
    cd yay-git
    makepkg -si --noconfirm
    cd ..
    rm -rf yay-git
  fi
}

function install_aur_packages() {
  install_yay_if_not_exist
  yay -Sy --noconfirm "$@"
}

function uninstall_aur_packages() {
  install_yay_if_not_exist
  yay -Rs --noconfirm "$@"
}

function refactor_mirror_list() {
  install_official_packages pacman-contrib

  echo "Sort /etc/pacman.d/mirrorlist by speed!"
  cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.backup
  rankmirrors -n 10 /etc/pacman.d/mirrorlist.backup > /etc/pacman.d/mirrorlist
}

function alis_defaults() {
  local DEVICE="$1"
  local ROOT_PASSWORD="$2"
  local SEC_LOCALE="$3"
  local SWAP_SIZE="$4"

  alis_create_partition "$DEVICE"
  alis_pacstrap
  alis_config_minimum "$ROOT_PASSWORD" "" "$SEC_LOCALE" "$SWAP_SIZE"
}

function alis_create_partition() {
  local DEVICE="$1"
  local ALONGSIDE="$2"

  : "${ALONGSIDE:=False}"

  function arch_linux_wipe_partition() {
    local DEVICE="$1"

    sgdisk --zap-all "$DEVICE"
    wipefs -a "$DEVICE"

    if [ -d /sys/firmware/efi ]; then
      parted "$DEVICE" mklabel gpt
    else
      parted "$DEVICE" mklabel msdos
    fi
  }

  function arch_linux_create_next_partition() {
    local DEVICE="$1"
    local SIZE="$2"
    : "${SIZE:=100%}"
    local LAST_MB
    local NEXT_SIZE

    LAST_MB=$(last_partition_end_mb "$DEVICE")
    if [[ "$LAST_MB" == 0% ]] || [[ "$SIZE" == 100% ]]; then
      NEXT_SIZE="$SIZE"
    else
      NEXT_SIZE=$(add_mb "$LAST_MB" "$SIZE")
    fi

    parted "$DEVICE" mkpart primary "$LAST_MB" "$NEXT_SIZE" >&2

    last_partition_name "$DEVICE"
  }

  function arch_linux_format_partition() {
    local PARTITION="$1"
    local LABEL="$2"
    if [[ "$LABEL" == "" ]]; then
      mkfs.ext4 "$PARTITION"
    else
      mkfs.ext4 -L "$LABEL" "$PARTITION"
    fi
  }

  function arch_linux_mount_partition() {
    local PARTITION="$1"
    local MOUNT_POINT="$2"
    local MOUNT_OPTIONS="$3"
    : "${MOUNT_OPTIONS:=defaults,noatime}"

    mkdir -p /mnt"$MOUNT_POINT"
    mount -o "$MOUNT_OPTIONS" "$PARTITION" /mnt"$MOUNT_POINT"
  }

  function arch_linux_create_boot_partition() {
    local DEVICE="$1"
    local PARTITION_NAME
    local PARTITION_NUMBER
    PARTITION_NAME=$(arch_linux_create_next_partition "$DEVICE" 512MB)
    PARTITION_NUMBER=$(last_partition_end_number_parted "$DEVICE")

    parted "$DEVICE" set "$PARTITION_NUMBER" boot on >&2
    if [ -d /sys/firmware/efi ]; then
      parted "$DEVICE" set "$PARTITION_NUMBER" esp on >&2
    fi

    echo "$PARTITION_NAME"
  }

  function arch_linux_format_boot_partition() {
    local PARTITION_BOOT="$1"
    if [ -d /sys/firmware/efi ]; then
      mkfs.fat -n "boot" -F32 "$PARTITION_BOOT"
    else
      arch_linux_format_partition "$PARTITION_BOOT" "boot"
    fi
  }

  if [[ "$ALONGSIDE" == False ]]; then
      arch_linux_wipe_partition "$DEVICE"
  fi

  arch_linux_wipe_partition "$DEVICE"
  PARTITION_BOOT=$(arch_linux_create_boot_partition "$DEVICE")
  PARTITION_ROOT=$(arch_linux_create_next_partition "$DEVICE")
  arch_linux_format_boot_partition "$PARTITION_BOOT"
  arch_linux_format_partition "$PARTITION_ROOT"
  arch_linux_mount_partition "$PARTITION_ROOT"
  arch_linux_mount_partition "$PARTITION_BOOT" /boot/efi
}

function alis_pacstrap() {
  refactor_mirror_list

  pacstrap /mnt base base-devel linux linux-headers linux-firmware

  genfstab -U /mnt >>/mnt/etc/fstab
}

function alis_install_package() {
  ARGUMENTS=$(printf '%q ' "$@")
  if eval chroot_if_needed alis_install_package "$ARGUMENTS"; then
    return 0
  fi

  local PRE_CONFIG="$1"
  local RUNNING_USER="$2"
  local PACKAGES="${*:3}"
  IFS=' ' read -r -a PACKAGES <<<"$PACKAGES"
  : "${PRE_CONFIG:=False}"
  : "${RUNNING_USER:=$SUDO_USER}"

  if [[ "$RUNNING_USER" == "" ]]; then
    if [[ "$USER" == root ]]; then
      echo Please provide user or logged as one and run with sudo!
    else
      echo Run this script with sudo or as root!
    fi
    exit 1
  fi

  if ! pacman -Q | grep git -q; then
    install_official_packages git
  fi

  if [[ "$PRE_CONFIG" == True ]]; then
    local ALL_PACKAGES
    ALL_PACKAGES=()
    ALL_CONFIG=()

    function collect_configs() {
      for PKG in "$@"; do
        if printf '%s\n' "${ALL_PACKAGES[@]}" | grep -x -q "$PKG"; then
          continue
        fi

        case "$PKG" in
        yay)
          ALL_PACKAGES+=( git )
          ;;
        gnome)
          ALL_PACKAGES+=(gnome gnome-extra matcha-gtk-theme xcursor-breeze papirus-maia-icon-theme-git ttf-dejavu noto-fonts ttf-liberation gnome-shell-extensions gnome-shell-extension-topicons-plus chrome-gnome-shell evolution-ews evolution-on)
          ALL_CONFIG+=(gnome_terminal_transparency_user gnome_bluetooth_user gnome_system)
          ;;
        docker)
          ALL_PACKAGES+=(docker docker-compose)
          ALL_CONFIG+=("docker_system $RUNNING_USER")
          ;;
        virtualbox)
          ALL_PACKAGES+=(virtualbox virtualbox-host-modules-arch virtualbox-guest-iso)
          ALL_CONFIG+=(virtualbox_system)
          ;;
        teamviewer)
          ALL_PACKAGES+=(teamviewer)
          ALL_CONFIG+=(teamviewer_system)
          ;;
        imwheel)
          ALL_PACKAGES+=(imwheel)
          ALL_CONFIG+=(imwheel_user)
          ;;
        intellij)
          ALL_PACKAGES+=(intellij-idea-ultimate-edition jdk11-openjdk)
          ALL_CONFIG+=(intellij_system)
          ;;
        util-packages)
          collect_configs nano zip unzip wget bash-completion openssh seahorse networkmanager-fortisslvpn
          ;;
        dev-packages)
          collect_configs maven npm vagrant packer git python python-pip docker virtualbox
          ;;
        tools-packages)
          collect_configs google-chrome variety slack-desktop intellij teamviewer
          ;;
        all-packages)
          collect_configs util-packages dev-packages tools-packages imwheel gnome
          ;;
        *)
          ALL_PACKAGES+=( "$PKG" )
          ;;
        esac
      done
    }

    collect_configs "${PACKAGES[@]}"

    user_chroot "$RUNNING_USER" install_aur_packages "${ALL_PACKAGES[@]}"
    for CONF in "${ALL_CONFIG[@]}"; do
      local CONF_ARR
      read -ra CONF_ARR <<<"$CONF"
      if [[ "${CONF_ARR[0]}" == *_user ]]; then
        user_chroot "$RUNNING_USER" pre_conf_packages "$CONF"
      else
        pre_conf_packages "$CONF"
      fi
    done
  else
    user_chroot "$RUNNING_USER" install_aur_packages "${PACKAGES[@]}"
  fi

}

function pre_conf_packages() {

  function gnome_system() {
    systemctl enable gdm.service
    if ! systemctl is-active --quiet gdm; then
      systemctl start gdm.service
    fi

    ln -s /etc/fonts/conf.avail/70-no-bitmaps.conf /etc/fonts/conf.d
    ln -s /etc/fonts/conf.avail/10-sub-pixel-rgb.conf /etc/fonts/conf.d
    ln -s /etc/fonts/conf.avail/11-lcdfilter-default.conf /etc/fonts/conf.d

    mkdir -p /etc/dconf/profile
    cat <<'EOT' >/etc/dconf/profile/user
user-db:user
system-db:site
EOT

    mkdir -p /etc/dconf/db/site.d
    cat <<'EOT' >/etc/dconf/db/site.d/00_site_settings
[org/gnome/GWeather]
temperature-unit='centigrade'

[org/gnome/Weather]
automatic-location=true

[org/gnome/calendar]
active-view='month'

[org/gnome/control-center]
last-panel='keyboard'

[org/gnome/desktop/interface]
cursor-theme='Breeze'
document-font-name='Sans 11'
enable-animations=true
font-name='Noto Sans 11'
gtk-im-module='gtk-im-context-simple'
gtk-theme='Matcha-azul'
icon-theme='Papirus-Dark-Maia'
monospace-font-name='Liberation Mono 11'

[org/gnome/desktop/peripherals/keyboard]
numlock-state=true

[org/gnome/desktop/wm/keybindings]
show-desktop=['<Super>d']
switch-applications=@as []
switch-applications-backward=@as []
switch-to-workspace-left=@as []
switch-to-workspace-right=@as []
switch-windows=['<Alt>Tab']
switch-windows-backward=['<Shift><Alt>Tab']

[org/gnome/desktop/wm/preferences]
button-layout='appmenu:minimize,maximize,close'

[org/gnome/gedit/preferences/editor]
scheme='solarized-dark'
use-default-font=true
wrap-last-split-mode='word'

[org/gnome/nautilus/icon-view]
default-zoom-level='small'

[org/gnome/settings-daemon/plugins/media-keys]
custom-keybindings=['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/']
home=['<Super>e']
www=['<Super>g']

[org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0]
binding='<Primary><Alt>t'
command='gnome-terminal'
name='terminal'

[org/gnome/shell]
disable-user-extensions=false
disabled-extensions=@as []
enabled-extensions=['TopIcons@phocean.net']

[org/gnome/shell/extensions/user-theme]
name='Matcha-dark-sea'

[org/gnome/shell/extensions/topicons]
icon-brightness=2.7755575615628914e-17
icon-contrast=2.7755575615628914e-17
icon-opacity=230
icon-saturation=0.40000000000000002
icon-size=16
tray-order=2
tray-pos='right'

[org/gnome/shell/weather]
automatic-location=true

[org/gnome/shell/world-clocks]
locations=@av []

[org/gnome/system/location]
enabled=true

[org/gnome/terminal/legacy/profiles:]
default='c07cafa6-2725-4bc3-bc30-fda45a6eae8f'
list=['b1dcc9dd-5262-4d8d-a863-c897e6d979b9', 'c07cafa6-2725-4bc3-bc30-fda45a6eae8f']

[org/gnome/terminal/legacy/profiles:/:c07cafa6-2725-4bc3-bc30-fda45a6eae8f]
audible-bell=false
background-color='#2E3440'
background-transparency-percent=9
bold-color='#D8DEE9'
bold-color-same-as-fg=true
cursor-background-color='rgb(216,222,233)'
cursor-colors-set=true
cursor-foreground-color='rgb(59,66,82)'
default-size-columns=100
default-size-rows=27
foreground-color='#D8DEE9'
highlight-background-color='rgb(136,192,208)'
highlight-colors-set=true
highlight-foreground-color='rgb(46,52,64)'
nord-gnome-terminal-version='0.1.0'
palette=['#3B4252', '#BF616A', '#A3BE8C', '#EBCB8B', '#81A1C1', '#B48EAD', '#88C0D0', '#E5E9F0', '#4C566A', '#BF616A', '#A3BE8C', '#EBCB8B', '#81A1C1', '#B48EAD', '#8FBCBB', '#ECEFF4']
scrollbar-policy='never'
use-system-font=true
use-theme-background=false
use-theme-colors=false
use-theme-transparency=false
use-transparent-background=true
visible-name='Nord'

[org/gnome/evolution/calendar]
allow-direct-summary-edit=false
confirm-purge=true
date-navigator-pane-position=175
date-navigator-pane-position-sub=175
hpane-position=3
month-hpane-position=6
prefer-new-item=''
primary-calendar='system-calendar'
primary-memos='system-memo-list'
primary-tasks='system-task-list'
recur-events-italic=false
tag-vpane-position=0.0019305019305019266
time-divisions=30
use-24hour-format=true
week-start-day-name='monday'
work-day-friday=true
work-day-monday=true
work-day-saturday=false
work-day-sunday=false
work-day-thursday=true
work-day-tuesday=true
work-day-wednesday=true

[org/gnome/evolution/mail]
browser-close-on-reply-policy='ask'
forward-style-name='attached'
hpaned-size=1618159
hpaned-size-sub=1594771
image-loading-policy='never'
junk-check-custom-header=true
junk-check-incoming=true
junk-empty-on-exit-days=0
junk-lookup-addressbook=false
layout=1
paned-size=1210424
paned-size-sub=1632933
prompt-on-mark-all-read=true
reply-style-name='quoted'
search-gravatar-for-photo=false
show-to-do-bar=false
show-to-do-bar-sub=false
to-do-bar-width=1150000
to-do-bar-width-sub=1282913
trash-empty-on-exit-days=0

[org/gnome/evolution/plugin/evolution-on]
hidden-on-startup=true
hide-on-close=true
hide-on-minimize=true

[org/gnome/evolution/shell]
attachment-view=0
buttons-visible=true
default-component-id='mail'
folder-bar-width=256
menubar-visible=true
sidebar-visible=true
statusbar-visible=false
toolbar-visible=false

EOT

    sed -i 's/#WaylandEnable=/WaylandEnable=/' /etc/gdm/custom.conf

    if systemctl is-active --quiet dbus; then
      dconf update
    fi
  }

  function gnome_terminal_transparency_user() {
    uninstall_aur_packages gnome-terminal
    install_aur_packages gnome-terminal-transparency
  }

  function gnome_bluetooth_user() {
    yes | yay -S gnome-bluetooth-pantheon
  }

  function docker_system() {
    systemctl enable docker
    systemctl start docker.service
    usermod -aG docker "$1"
  }

  function virtualbox_system() {
    vboxreload
  }

  function teamviewer_system() {
    systemctl enable teamviewerd.service
    systemctl start teamviewerd.service
  }

  function imwheel_user() {
    cat <<'EOT' >~/.imwheelrc
"^.*$"
    None, Up, Button4, 3.5
    None, Down, Button5, 3.5
EOT

    mkdir -p ~/.config/autostart
    cat <<'EOT' >~/.config/autostart/imwheel.desktop
[Desktop Entry]
Comment[en_US]=
Comment=
Exec=/usr/bin/imwheel -b 45
GenericName[en_US]=
GenericName=
Icon=system-run
MimeType=
Name[en_US]=imwheel
Name=imwheel
Path=
StartupNotify=true
Terminal=false
TerminalOptions=
Type=Application
X-DBUS-ServiceName=
X-DBUS-StartupType=
X-KDE-SubstituteUID=false
X-KDE-Username=
EOT

    /usr/bin/imwheel -b 45 &
  }
  
  function intellij_system() {
    archlinux-java set java-11-openjdk
  }

  ARGUMENTS=$(printf '%q ' "${*:2}")
  eval "$1" "$ARGUMENTS"
}

function alis_config_minimum() {
  ARGUMENTS=$(printf '%q ' "$@")
  if eval chroot_if_needed alis_config_minimum "$ARGUMENTS"; then
    return 0
  fi

  local ROOT_PASSWORD="$1"
  local ARCH_NAME="$2"
  local SEC_LOCALE="$3"
  local SWAP_SIZE="$4"
  local TIMEZONE="$5"
  local DEVICE
  DEVICE=$(working_device)
  local DEFAULT_SWAP_SIZE
  DEFAULT_SWAP_SIZE=$(grep MemTotal /proc/meminfo | awk '{$2/=1024; $2=int($2); print $2}')

  : "${ROOT_PASSWORD:=admin}"
  : "${ARCH_NAME:=archlinux}"
  : "${SEC_LOCALE:=en_US}"
  : "${SWAP_SIZE:=$DEFAULT_SWAP_SIZE}"

  refactor_mirror_list

  {
    echo "[multilib]"
    echo "Include = /etc/pacman.d/mirrorlist"
  } >>/etc/pacman.conf
  sed -i 's/#Color/Color/' /etc/pacman.conf
  sed -i 's/#TotalDownload/TotalDownload/' /etc/pacman.conf

  sed -i "s/# %wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/" /etc/sudoers

  cat <<EOT >>/etc/bash.bashrc
alias ll='ls -alF'
alias grep='grep --colour=auto'
alias egrep='egrep --colour=auto'
alias fgrep='fgrep --colour=auto'
PS1='\[\033[01;32m\][\u@\h\[\033[01;37m\] \W\[\033[01;32m\]]\$\[\033[00m\] '
EOT

  if [[ "$DEVICE" != "" ]] && ! lsblk "$DEVICE" --discard | grep -q 0B; then
    systemctl enable fstrim.timer
  fi

  echo "$ARCH_NAME" >/etc/hostname

  sed -i "s/#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/" /etc/locale.gen
  sed -i "s/#$SEC_LOCALE.UTF-8 UTF-8/$SEC_LOCALE.UTF-8 UTF-8/" /etc/locale.gen

  locale-gen

  {
    echo "LANG=en_US.UTF-8"
    echo "LC_ADDRESS=$SEC_LOCALE.UTF-8"
    echo "LC_IDENTIFICATION=$SEC_LOCALE.UTF-8"
    echo "LC_MEASUREMENT=$SEC_LOCALE.UTF-8"
    echo "LC_MONETARY=$SEC_LOCALE.UTF-8"
    echo "LC_NAME=$SEC_LOCALE.UTF-8"
    echo "LC_NUMERIC=$SEC_LOCALE.UTF-8"
    echo "LC_PAPER=$SEC_LOCALE.UTF-8"
    echo "LC_TELEPHONE=$SEC_LOCALE.UTF-8"
    echo "LC_TIME=$SEC_LOCALE.UTF-8"
  }>>/etc/locale.conf
  echo -e "KEYMAP=us" >/etc/vconsole.conf

  local SWAPFILE=/swapfile
  dd if=/dev/zero of="$SWAPFILE" bs=1M count="$SWAP_SIZE" status=progress
  chmod 600 "$SWAPFILE"
  mkswap "$SWAPFILE"
  swapon "$SWAPFILE"
  {
    echo "# swap"
    echo "$SWAPFILE none swap defaults 0 0"
    echo ""
  } >>/etc/fstab

  mkdir -p /etc/sysctl.d
  echo 'vm.swappiness=10' >/etc/sysctl.d/99-swappiness.conf

  install_official_packages networkmanager
  systemctl enable NetworkManager.service
  systemctl start NetworkManager.service

  printf "%s\n%s\n" "$ROOT_PASSWORD" "$ROOT_PASSWORD" | passwd

  if test -z "$TIMEZONE"; then
    install_official_packages python python-pip
    pip install -U tzupdate

    TIMEZONE=$(tzupdate -p)
  fi

  ln -s -f /usr/share/zoneinfo/"$TIMEZONE" /etc/localtime
  hwclock --systohc

  local BOOT_MOUNT
  BOOT_MOUNT=$(findmnt -s | awk '{if($0 ~ /boot/) print $1}')

  install_official_packages grub os-prober
  sed -i 's/GRUB_DEFAULT=0/GRUB_DEFAULT=saved/' /etc/default/grub
  sed -i "s/#GRUB_SAVEDEFAULT=\"true\"/GRUB_SAVEDEFAULT=\"true\"/" /etc/default/grub
  if [ -d /sys/firmware/efi ]; then
    install_official_packages efibootmgr
    grub-install --target=x86_64-efi --bootloader-id=grub --efi-directory="$BOOT_MOUNT" --recheck
  else
    grub-install --target=i386-pc --recheck "$DEVICE"
  fi

  grub-mkconfig -o "/boot/grub/grub.cfg"
  if lspci | grep -q -i virtualbox; then
    echo -n "\EFI\grub\grubx64.efi" >"$BOOT_MOUNT/startup.nsh"
  fi

  local SWAP
  SWAP=$(findmnt -s | awk '{if($0 ~ /swap/) print $2}')
  if [[ "$SWAP" != '' ]] && pacman -Q | grep grub -q; then
    eval "local $(< /etc/default/grub grep GRUB_CMDLINE_LINUX_DEFAULT)"
    if [[ "$SWAP" == UUID=* ]]; then
      GRUB_CMDLINE_LINUX_DEFAULT="$GRUB_CMDLINE_LINUX_DEFAULT resume=${SWAP#UUID=}"
    else
      local SWAP_DEVICE
      local SWAP_FILE_OFFSET
      SWAP_DEVICE=$(findmnt -no UUID -T "$SWAP")
      SWAP_FILE_OFFSET=$(filefrag -v "$SWAP" | awk '{ if($1=="0:"){print $4} }' | tr -d '.')
      GRUB_CMDLINE_LINUX_DEFAULT="$GRUB_CMDLINE_LINUX_DEFAULT resume=$SWAP_DEVICE resume_offset=$SWAP_FILE_OFFSET"
    fi
    sed -i -E "s/GRUB_CMDLINE_LINUX_DEFAULT=.*$/GRUB_CMDLINE_LINUX_DEFAULT=\"$GRUB_CMDLINE_LINUX_DEFAULT\"/g" /etc/default/grub

    grub-mkconfig -o "/boot/grub/grub.cfg"
  fi

  echo "Refresh Keys"
  pacman-key --refresh-keys
}

function alis_admin_user() {
  ARGUMENTS=$(printf '%q ' "$@")
  if eval chroot_if_needed alis_admin_user "$ARGUMENTS"; then
    return 0
  fi

  local USERNAME="$1"
  local PASSWORD="$2"
  : "${USERNAME:=admin}"
  : "${PASSWORD:=admin}"

  useradd -m -G wheel,storage,optical -s /bin/bash "$USERNAME"
  printf "%s\n%s\n" "$PASSWORD" "$PASSWORD" | passwd "$USERNAME"

  sed -i 's/PS1=/#PS1=/g' "/home/$USERNAME/.bashrc"
}

ARGUMENTS=$(printf '%q ' "$@")
eval "$ARGUMENTS"
