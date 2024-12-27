<table>
  <tr>
    <td style="vertical-align: middle;">
      <img src="https://github.com/Shogu/Fedora41-setup-config/blob/main/Images%20USER/.user-astronaut.png" alt="logo_user" width="150">
    </td>
    <td style="vertical-align: middle; padding-left: 10px;">
      <h2 style="margin: 0;">Fedora 41 setup & config</h2>
    </td>
  </tr>
</table>



🐧 Mémo pour le setup complet de **Fedora 41** sur laptop **ASUS ZENBOOK S13 FLIP OLED UP5302Z** 

***Table des matières:***

A - [Installation](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-a---installation)

B - [Allégement du système](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-b---all%C3%A9gement-du-syst%C3%A8me)

C - [Optimisation du système](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-c---optimisation-du-syst%C3%A8me)

D - [Remplacement et installation de logiciels](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-d---remplacement-et-installation-de-logiciels-et-codecs)

E - [Réglages de l'UI Gnome Shell](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-e---r%C3%A9glages-de-lui-gnome-shell)

F - [Réglages de Firefox](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-f---r%C3%A9glages-du-navigateur-firefox)

G - [Maintenance et mises à jour](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-g---maintenance-de-la-distribution)

----------------------------------------------------------------------------------------------

## 💾 **A - Installation**

* **1** - Désactiver `Secure Boot` dans le Bios (F2)

* **2** - Désactiver la caméra et le lecteur de carte dans le bios

* **3** - Graver l'iso `Fedora-Everything-netinst`

* **4** - Utiliser `systemd-boot` plutot que Grub : passer l'argument suivant dans le kernel de l'iso  d'installation (en pressant Espace au boot) juste avant QUIET
```
inst.sdboot
```
* **5** - Au démarrage, renommer le label BTRFS :
```
sudo btrfs filesystem label / fedora_41
```
Contrôler avec :
```
sudo btrfs filesystem show /
```
----------------------------------------------------------------------------------------------


## ✨ **B - Allégement du système**

* **6** - Supprimer les `logiciels inutiles` avec Gnome-software
  
* **7** - Compléter en supprimant les `logiciels inutiles` suivants avec dnf :
```
sudo dnf remove libertas-firmware
sudo dnf remove cirrus-audio-firmware
sudo dnf remove amd-gpu-firmware
sudo dnf remove amd-ucode-firmware
sudo dnf remove atheros-firmware
sudo dnf remove brcmfmac-firmware
sudo dnf remove tiwilink-firmware
sudo dnf remove nxpwireless-firmware
sudo dnf remove gnome-classic-session
sudo dnf remove mt7xxx-firmware
sudo dnf remove nvidia-gpu-firmware 
sudo dnf remove speech-dispatcher
sudo dnf remove ModemManager
sudo dnf remove gnome-remote-desktop
sudo dnf remove gnome-browser-connector
sudo dnf remove gnome-backgrounds
sudo dnf remove evince-djvu
sudo dnf gnome-user-share
sudo dnf remove vim*
sudo dnf remove ibus-libzhuyin
sudo dnf remove ibus-libpinyin
sudo dnf remove ibus-typing-booster
sudo dnf remove ibus-m17n
sudo dnf remove ibus-hangul 
sudo dnf remove ibus-anthy
sudo dnf remove yelp
sudo dnf remove abrt
sudo dnf remove brltty
sudo dnf remove podman
sudo dnf remove openvpn
sudo dnf remove gnome-weather
sudo dnf remove rygel
sudo dnf remove totem
sudo dnf remove avahi-tools
sudo dnf remove virtualbox-guest-additions
sudo dnf remove gnome-boxes
sudo dnf remove fedora-bookmarks
sudo dnf remove gnome-user-docs
sudo dnf remove hplip*
sudo dnf remove sane*
sudo dnf remove avahi
sudo dnf remove cups
```
    
* **8** - Supprimer et masquer les services `SYSTEM` & `USER` inutiles :
**SYSTEM**
```
sudo systemctl mask serial-getty@ttyS2.service
sudo systemctl mask systemd-vconsole-setup.service #attention, cela crée parfois un message d'erreur au boot!
sudo systemctl mask NetworkManager-wait-online.service
sudo systemctl mask auditd.service
sudo systemctl mask ModemManager.service
sudo systemctl mask avahi-daemon.service
sudo systemctl mask avahi-daemon.socket
sudo systemctl mask plymouth-quit-wait.service
sudo systemctl mask switcheroo-control.service
sudo systemctl mask sys-kernel-tracing.mount
sudo systemctl mask sys-kernel-debug.mount
sudo systemctl mask httpd.service
sudo systemctl mask mdmonitor.service
sudo systemctl mask raid-check.timer
sudo systemctl mask sssd-kcm.service
sudo systemctl mask pcscd
sudo systemctl mask pcscd.socket
sudo systemctl mask fwupd
sudo systemctl mask sssd-kcm.socket
sudo systemctl mask sssd.service
sudo systemctl mask iio-sensor-proxy #accéléromètre qui ne répond pas sur Fedora41 (mais marchait sur F39 en étant trop sensible...) + détecteur de luminosité auto pour le réglage de Gnome-settings qui est désactivé. Nota : l'extension gnome-shell `Screen Rotate` remplace avantageusement le capteur pour passer Fedora en mode tablette)
```
puis désactiver le Bluetooth pour l'activer à la volée (voir script dans la rubrique  Gnome) :
```
sudo systemctl disable bluetooth.service
```
Enfin, reboot puis controle de l'état des services avec :
```
systemd-analyze blame | grep -v '\.device$'
```
et :
```
systemctl list-unit-files --type=service --state=enabled
```

**USER**
```
systemctl --user mask evolution-addressbook-factory.service #contacts d'Evolution
systemctl --user mask org.gnome.SettingsDaemon.Wacom.service #Wacom
systemctl --user mask org.gnome.SettingsDaemon.Keyboard.service #paramètres du clavier
systemctl --user mask org.freedesktop.IBus.session.GNOME.service #saisie multilingue
systemctl --user mask org.gnome.SettingsDaemon.PrintNotifications.service #imprimante
systemctl --user mask org.gnome.SettingsDaemon.A11ySettings.service #accessibilité
systemctl --user mask at-spi-dbus-bus.service #accessibilité type lecteur d'écran
systemctl --user mask org.gnome.SettingsDaemon.Smartcard.service #carte à puce
```
Puis contrôler avec :
```
systemd-analyze --user blame
```
---> boot time --user avant optimisation : 3.8 secondes / userspace 293 ms

`systemd-analyze --user
Startup finished in 3.800s (userspace)
default.target reached after 293ms in userspace.`

---> boot time --user après optimisation : 3 secondes / userspace 232 ms

`systemd-analyze --user
Startup finished in 3.007s (userspace)
default.target reached after 232ms in userspace.`

* **9** - Alléger les `journaux système` et les mettre en RAM :
```
sudo gnome-text-editor /etc/systemd/journald.conf
```
puis remplacer le contenu du fichier par celui du fichier `journald.conf.txt` & relancer le service :
```
sudo systemctl restart systemd-journald
```

* **10** - Remplacer chronyd par `systemd-timesyncd` (plus rapide au boot) ([source](https://www.dsfc.net/systeme/linux/ntp-passage-de-chrony-a-systemd-timesyncd/))
```
sudo dnf remove chrony
sudo systemctl enable systemd-timesyncd
sudo gnome-text-editor /etc/systemd/timesyncd.conf
```
et saisir :
```
[Time]
NTP=0.fr.pool.ntp.org 1.fr.pool.ntp.org 2.fr.pool.ntp.org 3.fr.pool.ntp.org
FallbackNTP=3.fr.pool.ntp.org 2.fr.pool.ntp.org 2.fr.pool.ntp.org 0.fr.pool.ntp.org
```
Puis 
```
sudo systemctl start systemd-timesyncd
timedatectl set-ntp true
```
Au reboot, vérifier que le serveur de temps est bien en France et que le service est actif :
```
timedatectl status
systemctl status systemd-timesyncd
```

* **11** - Supprimer les `coredump` en éditant systemd : 
``` 
sudo gnome-text-editor /usr/lib/systemd/coredump.conf
```
Editer le fichier comme suit :
```
[Coredump]
Storage=none
ProcessSizeMax=0
```

* **12** - Supprimer le `watchdog`
```
sudo gnome-text-editor /etc/sysctl.d/99-custom.conf
```

et saisir : `kernel.nmi_watchdog=0`, puis relancer avec : ```sudo sysctl --system```

Reboot & contrôle avec :
```
sudo sysctl kernel.nmi_watchdog
```

* **13** - Blacklister les pilotes inutiles : créer un fichier `blacklist` ```sudo gnome-text-editor /etc/modprobe.d/blacklist.conf``` et l'éditer :
```
#watchdogs
blacklist iTCO_vendor_support
blacklist iTCO_wdt
blacklist wdat_wdt
blacklist intel_pmc_bxtvidia

#driver pour nvidia
blacklist nouveaudrivers

#drivers inutiles
blacklist ELAN:Fingerprint
blacklist btusb
blacklist joydev

#drivers accéléromètre et capteur luminosité
blacklist hid_sensor_accel_3d
blacklist hid_sensor_als
blacklist hid_sensor_trigger
blacklist hid_sensor_iio_common
blacklist hid_sensor_hub
blacklist industrialio
blacklist industrialio_triggered_buffer

#drivers netbios
blacklist nf_conntrack_netbios_ns
blacklist nf_conntrack_broadcast

#drivers son realtek
blacklist snd_hda_codec_realtek
blacklist snd_hda_codec_generic

#tty
blacklist serial8250
blacklist 8250_pci
```
Puis lancer `sudo dracut --force`
Au reboot, vérifier avec la commande `lsmod | grep hid_sensor`

* **14** - Autosuspendre le `capteur de luminosité et l'accéléromètre` (en complément de son maskage)
```
echo 'ACTION=="add", SUBSYSTEM=="pci", KERNEL=="0000:00:12.0", ATTR{power/control}="auto"' | sudo tee /etc/udev/rules.d/99-pci-autosuspend.rules > /dev/null
```
Puis
```
sudo udevadm control --reload-rules
```
Et contrôler avec :
```
cat /etc/udev/rules.d/99-pci-autosuspend.rules
```

* **EXPERIMENTAL** : réduire l`initramfs` en désactivant des modules inutiles (manipulation à faire à chaque màj du kernel)
Créer un fichier de configuration `dracut` :
```
sudo gnome-text-editor /etc/dracut.conf.d/dracut.conf
```
et copier-coller ces options de configuration :
```
# Configuration du fichier dracut.conf pour obtenir un initrd le plus léger possible

# Suppression des modules inutiles
omit_dracutmodules+=" multipath nss-softokn memstrack usrmount mdraid dmraid debug selinux fcoe fcoe-uefi terminfo watchdog crypt-gpg crypt-loop cdrom pollcdrom pcsc ecryptfs rescue watchdog-module network cifs nfs nbd brltty fips fips-crypto-policies busybox rdma i18n isci pcmcia wacom "

omit_modules+=" systemd-vconsole-setup "

omit_drivers+=" nvidia amd nouveau "

# Système de fichiers utilisés
filesystems+=" ext4 btrfs fat "

# Ne pas exécuter fsck
nofscks="yes"
  
# Suppression de la journalisation
stdlog="0"

# Suppression des symboles de debogage
do_strip="yes"
aggressive_strip="yes"

# Compression de l'initramfs
compress="zstd"
compress_options="-4"

# Mode silencieux
quiet="yes"
  
# Autres options
force="yes"
hostonly="yes"
hostonly_mode="strict"
```

Installer binutils pour obtenir le module `strip` :
```
sudo dnf install binutils -y
```

Recréer l'initramfs avec :
```
sudo dracut --force --verbose
```
Vérifier l'output après sudo dracut :
```
sudo lsinitrd -m
```
----------------------------------------------------------------------------------------------


## 🚀 **C - Optimisation du système**

* **15** - Désactiver `SElinux` :
```
sudo gnome-text-editor /etc/selinux/config
```
et saisir ```SELINUX=disabled```
  
Vérifier la désactivation après reboot avec la commande ```sestatus```

Enfin supprimer les labels SElinux avec :
```
sudo find / -print0 | xargs -r0 setfattr -x security.selinux 2>/dev/null
```

* **16** - Passer `xwayland` en autoclose : sur dconf-editor, modifier la clé suivante.
```
org.gnome.mutter experimental-features
```

* **17** - Optimiser le `kernel` :
```
sudo gnome-text-editor /etc/kernel/cmdline
```

Puis saisir :
```
mitigations=off selinux=0 cgroup_disable=rdma nmi_watchdog=0 loglevel=0 noresume console=tty1 8250.nr_uarts=1
```
Nota : si le boot est bavard, envisager l'argument `systemd.show_status=false`

Relancer systemd conformément au conseil dans les commentaires de fstab :
```
systemctl daemon-reload
```
Actualiser le kernel et l'initramfs avec les commandes suivantes :
```
sudo kernel-install add $(uname -r) /lib/modules/$(uname -r)/vmlinuz
```
```
sudo dracut --force
```
  
Au reboot, contrôler le fichier de boot de `systemd-boot` avec la commande :
```
cat /proc/cmdline
```

* **18** - Réduire le `temps d'affichage du menu systemd-boot` à 0 seconde  (appuyer sur MAJ pour le faire apparaitre au boot):
```
sudo bootctl set-timeout 0
```
Reboot, puis vérifier que le fichier loader.conf soit à 0 :
```
sudo cat /boot/efi/loader/loader.conf
timeout 5
#console-mode keep
```
Si non, l'éditer et passer le timeout à 0 :
```
sudo gnome-text-editor /boot/efi/loader/loader.conf
```
Puis reconstruire le kernel avec :
```
sudo kernel-install add $(uname -r) /lib/modules/$(uname -r)/vmlinuz && sudo dracut --force
```

* **19** - Editer le mount des `partitions BTRFS` **/** et **/home** avec la commande :
```
sudo gnome-text-editor /etc/fstab
```
puis saisir les flags suivants :

Pour les volumes BTRFS :
```
noatime,commit=120,discard=async,space_cache=v2
```
Pour les volumes EXT4 :
```
noatime
```
Contrôler avec `cat /etc/fstab` après un reboot.

* **20** - Mettre les `fichiers temporaires en RAM` :
```
sudo gnome-text-editor /etc/fstab
```
puis saisir :
  
```
tmpfs /tmp tmpfs defaults,noatime,mode=1777,nosuid,size=1024M 0 0
```
Contrôler avec `cat /etc/fstab` après un reboot, et `df -h /tmp`

* **21** - Régler le `pare-feu` :
  
Connaitre la zone par défaut du système (en général FedoraWorkstation) avec :
```
sudo firewall-cmd --get-default-zone
```
Puis bloquer toutes les connexions entrantes par défaut
```
sudo firewall-cmd --permanent --zone=FedoraWorkstation --set-target=DROP
```
Redémarrer firewalld :
```
sudo firewall-cmd --reload
```
Enfin, vérifier les réglages :
```
sudo firewall-cmd --zone=FedoraWorkstation --list-all
sudo firewall-cmd --get-active-zones
```

* **22** - Modifier les réglages d'accès au `swap`, le `dirty_writeback` etc (conformément aux réglages de Powertop, et partiellement de CachyOS):
```
echo vm.swappiness=5 | sudo tee -a /etc/sysctl.d/99-sysctl.conf
echo vm.vfs_cache_pressure=50 | sudo tee -a /etc/sysctl.d/99-sysctl.conf
echo vm.watermark_boost_factor=0 | sudo tee -a /etc/sysctl.d/99-sysctl.conf
echo vm.watermark_scale_factor=50 | sudo tee -a /etc/sysctl.d/99-sysctl.conf
echo vm.page-cluster=0| sudo tee -a /etc/sysctl.d/99-sysctl.conf
echo vm.dirty_bytes = 268435456 | sudo tee -a /etc/sysctl.d/99-sysctl.conf
echo "vm.dirty_writeback_centisecs=1500" | sudo tee -a /etc/sysctl.d/99-sysctl.conf
sudo sysctl -p /etc/sysctl.d/99-sysctl.conf
sudo sysctl --system
```

Reboot et vérifier avec :
```
cat /proc/sys/vm/swappiness
cat /proc/sys/vm/vfs_cache_pressure
cat /proc/sys/vm/dirty_writeback_centisecs
```
  
* **23** - Accélérer `DNF` : 
```
echo 'max_parallel_downloads=10' | sudo tee -a /etc/dnf/dnf.conf
```
  
* **24** - Passer à 1 le nombre de `ttys` au boot  :  
```
sudo gnome-text-editor /etc/systemd/logind.conf
```
puis saisir : `NautoVTS=1`

* **25** - Vérifier que le système utilise bien les DNS du `routeur Xiaomi` (192.168.31.1) :
```
nmcli dev show |grep DNS
```

* **26** - Amélioration du réseau : après plusieurs test comparatifs, améliorer le ping, la latence, et un peu le débit
  
Commencer par désactiver `ipv6` dans les Paramètres wifi de Gnome.

Puis modifier les réglages `sysctl`
```
sudo gnome-text-editor /etc/sysctl.d/99-sysctl.conf
```
Puis saisir :
```
# Optimisation TCP pour minimiser ping et latence tout en conservant un bon débit
net.ipv4.tcp_congestion_control = cubic
net.ipv4.tcp_rmem = 4096 87380 8388608
net.ipv4.tcp_wmem = 4096 87380 8388608
net.core.rmem_default = 8388608
net.core.rmem_max = 8388608
net.core.wmem_default = 8388608
net.core.wmem_max = 8388608
net.ipv4.tcp_mtu_probing = 0
net.ipv4.tcp_low_latency = 1
net.ipv4.tcp_ecn = 1
net.ipv4.tcp_slow_start_after_idle = 0
net.ipv4.tcp_rfc1337 = 1
net.core.netdev_max_backlog = 4096
```
Relancer avec :
```
sudo sysctl -p
```

**Boot time : avant optimisation : 23.7 secondes**

`Startup finished in 5.8s (firmware) + 508ms (loader) + 1.896s (kernel) + 4s (initrd) + 11.5s (userspace) = 23.7s`

**Boot time : après optimisation : 11.5 secondes**

`Startup finished in 2.315s (firmware) + 486ms (loader) + 1.742s (kernel) + 3.863s (initrd) + 3.174s (userspace) = 11.583s`

----------------------------------------------------------------------------------------------


## 📦 **D - Remplacement et installation de logiciels et codecs**

* **27** - Ajouter les sources `RPMFusion` :
  
**RPMFusion Free**
```
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E%fedora).noarch.rpm 
```

**RMPFusion Non free**
```
sudo dnf install https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```
    
* **28** - Ajouter les codecs `FFMPEG`, multimedia, `AV1`, & le `pilote Intel` d'accélération matérielle :
```
sudo dnf swap ffmpeg-free ffmpeg --allowerasing
sudo dnf install intel-media-driver
sudo dnf swap libva-intel-media-driver intel-media-driver --allowerasing
sudo dnf update @multimedia --setopt="install_weak_deps=False" --exclude=PackageKit-gstreamer-plugin
```

* **29** - Réglages de `gnome-software`

* **30** - Installer les logiciels `Flatpak` suivants : nota : utiliser prioritairement les flatpaks Fedora OU Flathub car les runtimes ne sont pas partagés entre les 2.
```
flatpak install flathub com.mattjakeman.ExtensionManager -y
flatpak install flathub io.github.flattool.Warehouse -y
NE PAS INSTALLER FLATSWEEP : il utilise la version obsolète 46 de Gnome, soit 1 Go de contenu pour pas grand chose...flatpak install flathub io.github.giantpinkrobots.flatsweep -y
flatpak install flathub net.nokyan.Resources -y
flatpak install flathub org.jdownloader.JDownloader -y
flatpak install flathub org.onlyoffice.desktopeditors -y
flatpak install flathub de.haeckerfelix.Fragments -y
flatpak install flathub org.gnome.Papers -y
flatpak install flathub page.codeberg.libre_menu_editor.LibreMenuEditor -y
flatpak install flathub io.github.celluloid_player.Celluloid -y
flatpak install flathub org.nicotine_plus.Nicotine -y
flatpak install flathub de.schmidhuberj.tubefeeder -y
flatpak install flathub org.gnome.Epiphany -y
```
Nota : penser à décocher "Exécuter en arrière plan" dans les réglages de Gnome (rubrique `applications`) pour le navigateur secondaire `Web`, sans quoi il semble se lancer au boot.

* **31** - Installer les `logiciels` suivants avec dnf :
```
sudo dnf install dconf-editor -y
sudo dnf install evince-thumbnailer -y
sudo dnf install gnome-tweaks -y
sudo dnf install powertop -y
sudo dnf install zstd -y
sudo dnf install ffmpegthumbnailer.x86_64 -y
sudo dnf install profile-cleaner -y
sudo dnf install btrfs-assistant -y
sudo dnf install seahorse -y
sudo dnf install dnfdragora -y
sudo dnf install ImageMagick -y
```

* **32** - Installer `Dropbox` avec **Maestral** :
```
sudo dnf install gcc
sudo dnf install python3-devel
sudo dnf install python3-pip  
python3 -m venv maestral-venv
mv maestral-venv .maestral-venv
source .maestral-venv/bin/activate
python3 -m pip install --upgrade 'maestral[gui]' ou python3 -m pip install --user maestral[gui]
maestral gui
sudo dnf remove gcc python3-devel python3-pip
```

* **33** - Désinstaller `gnome-software` et `packagekit` (ainsi que le cache) pour éviter leur lancement au boot, et les remplacer par `DNFdragora` :
  
```
sudo dnf remove PackageKit-gstreamer-plugin PackageKit PackageKit-command-not-found gnome-software
sudo rm -rf /var/cache/PackageKit
```

OU désactiver l'autostart : copier le fichier `/etc/xdg/autostart/gnome-software-service.desktop` vers `~/.config/autostart/`, puis désactiver l'autostart et la recherche de logiciels à partir de l'overview (qui réactive automatiquement gnome-software) en rajoutant le code suivant en fin de fichier :
```
X-GNOME-Autostart-enabled=false
```
Puis saisir dans un terminal : 
```
dconf write /org/gnome/desktop/search-providers/disabled "['org.gnome.Software.desktop']"
```
----------------------------------------------------------------------------------------------


## 🐾 **E - Réglages de l'UI Gnome Shell** 

* **34** - Régler le système avec `Paramètres` puis `Ajustements` (Changer les polices d'écriture pour `Noto Sans` en 11)

* **35** - Régler Nautilus & créer un marque-page pour `Dropbox` & pour l'accès `ftp` au disque SSD sur la TV Android :
```
192.168.31.68:2121
```

* **36** - Modifier le mot de passe au démarrage avec le logiciel `Mots de Passe`, puis laisser les champs vides. Penser à reconnecter le compte Google dans Gnome!

* **37** - Installer le [wallpaper F34](https://fedoraproject.org/w/uploads/d/de/F34_default_wallpaper_night.jpg) et le thème de curseurs [Phinger NO LEFT Light](https://github.com/phisch/phinger-cursors/releases); utiliser `dconf-editor` pour les passer en taille 32 :
```
org/gnome/desktop/interface/cursor-size
```
* **38** - Régler `HiDPI` sur 175, cacher les dossiers Modèles, Bureau, ainsi que le wallaper et l'image user, augmenter la taille des icones dossiers.
  
* **39** Renommer les `logiciels dans l'overview`, cacher ceux qui sont inutiles de faàon à n'avoir qu'une seule et unique page, en utilisant le logiciel `Menu Principal`.
En profiter pour changer avec Menu Principal l'icone de `Ptyxis`, en la remplaçant par celle de [gnome-terminal](https://upload.wikimedia.org/wikipedia/commons/d/da/GNOME_Terminal_icon_2019.svg)

* **40** - Installer diverses `extensions` :

Extensions esthétiques :

a - [Panel Corners](https://extensions.gnome.org/extension/4805/panel-corners/)

b - [Hide Activities Button](https://extensions.gnome.org/extension/744/hide-activities-button/)

c - [Remove World Clock](https://extensions.gnome.org/extension/6973/remove-world-clocks/)

Extensions apportant des fonctions de productivité :

d - [Appindicator](https://extensions.gnome.org/extension/615/appindicator-support/)

e - [Alphabetical Grid](https://extensions.gnome.org/extension/4269/alphabetical-app-grid/)

f - [Caffeine](https://extensions.gnome.org/extension/517/caffeine/)

g - [Clipboard History](https://extensions.gnome.org/extension/4839/clipboard-history/)

Extensions apportant des fonctions UI :  

h - [Battery Time Percentage Compact](https://extensions.gnome.org/extension/2929/battery-time-percentage-compact/) ou [Battery Time](https://extensions.gnome.org/extension/5425/battery-time/)

i - [Privacy Quick Settings](https://extensions.gnome.org/extension/4491/privacy-settings-menu/) puis la supprimer une fois les réglages réalisés.
 
j - [Grand Theft Focus](https://extensions.gnome.org/extension/5410/grand-theft-focus/)
    
k - [AutoActivities](https://extensions.gnome.org/extension/5500/auto-activities/)

l - [Auto Screen Brightness](https://extensions.gnome.org/extension/7311/auto-screen-brightness/) & supprimer la luminosité automatique dans Settings de Gnome

m - [Hot Edge](https://extensions.gnome.org/extension/4222/hot-edge/)
  
n - [Auto Power Profile](https://extensions.gnome.org/extension/6583/auto-power-profile/)
  
o - [Frequency Boost Switch](https://extensions.gnome.org/extension/4792/frequency-boost-switch/)
    
Extension à désactiver :

p - désactiver l'extension native `Background logo`

* **41** - Installer [Nautilus-admin](https://download.copr.fedorainfracloud.org/results/tomaszgasior/mushrooms/fedora-41-x86_64/07341996-nautilus-admin/nautilus-admin-1.1.9-5.fc41.noarch.rpm) puis lancer la commande ```nautilus -q``` pour relancer Fichiers

* **42** - Raccourcis à éditer dans Gnome : mettre `ptyxis` à la place de la touche Exposant, et la commande ```flatpak run net.nokyan.Resources``` pour la combinaison `ctrl-alt-supp`.

* **43** - Régler `Gnome-text-editor`, mais surtout `Ptyxis` en installant `fish` et 'tldr' ("too long/don't read", un manpage en français et simplifié :
```
sudo dnf install fish tldr
```
Puis mettre fish comme shell par défaut :
```
chsh -s /usr/bin/fish
```
Enfin éditer son fichier de configuration avec `gnome-text-editor ~/.config/fish/config.fish` et saisir :
```
# supprimer le message d'accueil.
set -g fish_greeting
# supprimer les codes d'erreur rouge mais maintenir les couleurs d'origine
function fish_prompt
    # Couleur verte intense pour "ogu"
    set_color green --bold
    echo -n "ogu"
    set_color normal
    echo -n "@fedora-ogu " (prompt_pwd) " > "
end
```

Pour le shell bash : améliorer l'autocomplétion du terminal en créant le fichier`.inputrc` et le placer dans `~/` :
```
# Ignore la casse lors de la complétion
set completion-ignore-case on

# Affiche toutes les options si ambiguïté
set show-all-if-ambiguous on

# Affiche toutes les options si la ligne n'a pas changé
set show-all-if-unmodified on

# Montre des infos comme les permissions (ls-like)
set visible-stats on

# Permet de parcourir les suggestions avec TAB
TAB: menu-complete
```
  
* **44** - `Celluloid` :
inscrire `vo=gpu-next` dans Paramètres --> Divers --> Options supplémentaires, activer l'option `focus` et `toujours afficher les boutons de titre`, enfin installer les deux scripts lua suivants pour la musique :
[Visualizer](https://www.dropbox.com/scl/fi/bbwlvfhtjnu8sgr4yoai9/visualizer.lua?rlkey=gr3bmjnrlexj7onqrxzjqxafl&dl=0)
[Delete File avec traduction française](https://www.dropbox.com/scl/fi/c2cacmw2a815husriuvc1/delete_file.lua?rlkey=6b9d352xtvybu685ujx5mpv7v&dl=0)

* **45** - `Jdownloader`: réglages de base, thème Black Moon puis icones Flat; font Noto Sans Regular, désactivatioin du dpi et font sur 175; puis désactiver les éléments suivants : tooltip, help, Update Button Flashing, banner, Premium Alert, Donate, speed meter visible.

* **46** - Script de `transfert des vidéos` intitulé `.transfert_videos` pour déplacer automatiquement les vidéos vers Vidéos en supprimant le sous-dossier d'origine.
Le télécharger depuis le dossier `SCRIPTS`, en faire un raccourci avec l'éditeur de menu, passer le chemin `sh /home/ogu/.transfert_videos.sh` et lui mettre l'icone `/usr/share/icons/Adwaita/scalable/devices/drive-multidisk.svg`

* **47** - Script de `bascule Bluetooth` `.bluetooth_toggle` pour activer/désactiver le service bluetooth à la volée.
Le télécharger depuis le dossier `SCRIPTS`, en faire un raccourci avec l'éditeur de menu, raccourci d'exécution `bash /home/ogu/.bluetooth_toggle.sh` & mettre l'icone `/usr/share/icons/Adwaita/scalable/devices/phone.svg`.

* **48** - Accélérer les `animations` :  saisir
```
GNOME_SHELL_SLOWDOWN_FACTOR=0.5
```
dans le fichier 
```
sudo gnome-text-editor /etc/environment
```

* **49** - `Scripts` Nautilus :
a - `Dropbox.py` pour imiter l'extension nautilus-dropbox avec Maestral (édition et lecture du fichier sur le site Dropbox & copie de l'url de partage)
b - `Hide.py` et `Unhide.py` pour masquer/rendre visibles les fichiers
A télécharger depuis le dossier `SCRIPTS` puis à coller dans le dossier `/home/ogu/.local/share/nautilus/scripts/.
Penser à les rendre exécutables!

* **50** - `LibreOffice` : régler l'UI et les paramètres, désactiver Java, rajouter `-nologo` au raccourci avec l'éditeur de menu pour supprimer le splash screen, passer à `600000000` la valeur de `Graphic Manager` + `UseOpenGL` = true + `UseSkia` = true dans la Configuration Avancée + désactiver l'enregistrement des données personnelles dans les fichiers (Menu Sécurité). 

* **51** - Faire le tri dans `~/.local/share/`, `/home/ogu/.config/`, `/usr/share/` et `/etc/`
----------------------------------------------------------------------------------------------

 
## 🌐 **F - Réglages du navigateur Firefox**

* **52** - Réglages internes de `Firefox` (penser à activer CTRL-TAB pour faire défiler dans l'ordre d'utilisation & à passer sur `Sombre` plutot qu'`auto` le paramètre `Apparence des sites web`)

* **53** - Changer le `thème` pour [Materia Dark](https://addons.mozilla.org/fr/firefox/addon/materia-dark-theme/) ou [Gnome Dark ](https://addons.mozilla.org/fr/firefox/addon/adwaita-gnome-dark/?utm_content=addons-manager-reviews-link&utm_medium=firefox-browser&utm_source=firefox-browser)

* **54** - Dans `about:config` :
  
a - `ui.key.menuAccessKey` = 0 pour désactiver la touche Alt qui ouvre les menus
  
b - `browser.sessionstore.interval` à `600000` pour réduire l'intervalle de sauvegarde des sessions

c - `extensions.pocket.enabled` = false, `browser.newtabpage.activity-stream.discoverystream.sendToPocket.enable` = false, et supprimer Pocket de la barre d'outils si besoin

d - `devtools.f12_enabled` = false

e - `accessibility.force_disabled` = 1 pour supprimer l'accessibilité

f - `extensions.screenshots.disabled` = true pour désactiver le screenshot

g - `privacy.userContext.enabled` = false pour désactiver les containers

h - `browser.tabs.crashReporting.sendReport` = false

i - `network.http.max-persistent-connections-per-server` = 10  

j - `image.mem.decode_bytes_at_a_time` = 131072

k - `browser.translations.enable` = false

l - `dom.battery.enabled` = false 

m - `extensions.htmlaboutaddons.recommendations.enabled` = false pour désactiver l'affichage des "extensions recommandées" dans le menu de Firefox

n - `sidebar.revamp` = true, puis régler la barre latérale

o - `apz.overscroll.enabled` = false pour supprimer le rebonb lors d uscroll jusqu'en fin de page

p - `browser.cache.disk.parent_directory` à créer sour forme de `chaine`, et lui passer l'argument /run/user/1000/firefox, afin de déplacer le cache en RAM. Saisir `
about:cache` pour contrôle. 

* **55** - **Extensions**
  
a - [uBlock Origin](https://addons.mozilla.org/fr/firefox/addon/ublock-origin/) : réglages à faire + import des deux listes sauvegardées
  
b - [Auto Tab Discard](https://addons.mozilla.org/fr/firefox/addon/auto-tab-discard/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=featured) : importer les réglages avec le fichier de backup et bien activer les 2 options de dégel des onglets à droite et à gauche de l'onglet courant.

c - [Raindrop](https://raindrop.io/r/extension/firefox) et supprimer `Pocket` de Firefox avec `extensions.pocket.enabled` dans `about:config` puis supprimer le raccourci dans la barre.
  
d - [Clear Browsing Data](https://addons.mozilla.org/fr/firefox/addon/clear-browsing-data/)
  
e - [Undo Close Tab Button](https://addons.mozilla.org/firefox/addon/undoclosetabbutton) et mettre ALT-Z comme raccourci à partir du menu général des extensions (roue dentée)

f - [LocalCDN](https://addons.mozilla.org/fr/firefox/addon/localcdn-fork-of-decentraleyes/), puis faire le [test](https://decentraleyes.org/test/).

g - [Side View](https://addons.mozilla.org/fr/firefox/addon/side-view/)

h - [Scroll To Top Lite](https://addons.mozilla.org/fr/firefox/addon/scroll-to-top-lite/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search)

* **56** - Activer `openh264` & `widevine` dans les plugins firefox.
  
* **57** - Désactiver les `recherches populaires` : dans la barre d'adresse, cliquer en bas sur la roue dentée correspondant à Recherches populaires et les désactiver.

* **58** - Mettre le profil de Firefox en RAM avec `profile-sync-daemon` :
* ATTENTION : suivre ces consignes avec **Firefox fermé** - utiliser le browser secondaire WEB
  
Installer psd (avec dnf `sudo dnf install profile-sync-daemon`, ou avec make en cas d'échec - voir le fichier INSTALL sur le Github), puis l'activer avec les commandes suivantes (sans quoi le service échoue à démarrer) :
```
psd
systemctl --user daemon-reload
sytemctl --user enable psd
reboot
```
Puis vérifier que psd fonctionne en contrôlant d'abord les profils Firefox :
```
cat ~/.mozilla/firefox/profiles.ini  #default=1 correspond au profil par défaut
cd ~/.mozilla/firefox/
ls ~/.mozilla/firefox/
```
Puis se rendre dans le dossier `~/.mozilla/firefox/` et copier-coller les profils dans un dossier de sauvegarde. Les supprimer un par un en relançant Firefox pour contrôle. Une fois le dossier unique par défaut établi, le renommer avec
```
firefox --ProfileManager #renommer le profil par défaut et eventuellement supprimer le profil en double  
```
Enfin régler & contrôler le bon fonctionnement de psd : passer à 2 le nombre de backups au lieu de 5 avec `BACKUP_LIMIT=2`, & circonscrire psd au seul Firefox avec `BROWSERS=(firefox)`:
```
psd -p
sudo gnome-text-editor /home/ogu/.config/psd/psd.conf *# The default is to save the most recent 5 crash recovery snapshots BACKUP_LIMIT=2 & BROWSERS=(firefox)
```
Lancer Firefox et s'assurer que le profil originel ne pèse que quelques Ko :
```
cd ~/.mozilla/firefox
du -sh ~/.mozilla/firefox/
```
Puis s'assurer que les centaines de Mo du profil sont bien en ram :
```
cd /run/user/1000
ls /run/user/1000
cd psd
ls
cd firefox
ls
du -sh /run/user/1000/psd/nom du profil/
```



## 🪛 **G - Maintenance de la distribution**
 en cours de rédaction
```
sudo dnf autoremove
sudo dnf -y upgrade --refresh
sudo dnf clean all
flatpak update
profile-cleaner f
```

Unmask temporaire de fwupd puis 
sudo fwupdmgr get-devices 
sudo fwupdmgr refresh --force 
sudo fwupdmgr get-updates 
sudo fwupdmgr update
???

flatpak uninstall --unused
flatpak run io.github.flattool.Warehouse

sudo fsck -n /boot sudo fsck -n /boot/efi

Regarder script de F39





















****************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************


💡 A TESTER :

* - Remplacement de wpa_supplicant par `iwd` pour le **wifi**
 
ATTENTION : a ureboot la connection auto ne se fait pas, voir les reglages de config de iwd
ATTENTION2 : le service démarre plus lentement que wpa_supplicant, à voir le temps de boot pour network-manager avec iwd plutot que wpa

Installer iwd :
```
sudo dnf install iwd -y
```
Lancer le service iwd et désactiver temporairement wpa_supplicant
```
sudo systemctl start iwd
sudo systemctl stop wpa_supplicant
sudo systemctl disable wpa_supplicant
```
Puis créer le fichier de configuration de NetworkManager : 
```
sudo gnome-text-editor /etc/NetworkManager/conf.d/00-iwd.conf
```
Ajouter les lignes suivantes :
```
[device]
wifi.backend=iwd

[main]
dns=systemd-resolved
```
Redémarrer NetworkManager pour appliquer la configuration :
```
sudo systemctl restart NetworkManager
```
Se reconnecter & vérifier l'état des connexions Wi-Fi avec `nmcli` :
```
nmcli device status
```
Si la connection est fonctionnelle, activer le service iwd au boot :
```
sudo systemctl enable iwd
```
Reboot, puis suppression de wpa_supplicant :
```
sudo dnf remove wpa_supplicant
```
    
* Créer un toggle `Powertop` qui va lancer powertop en `auto-tune` pour économiser encore plus de batterie, et baisser la luminosité sur 5% : rentrer cette commande pour le toggle activé :
```
pkexec powertop --auto-tune && gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness " <int32 5>"()
```
  
Et cette commande pour le toggle désactivé :
```
gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness " <int32 2O>"()
```
Enfin rentrer le nom de l'icone : `thunderbolt-symbolic` 

* Créer un toggle "No Touchscreen" et le rendre permanent au boot :
    
```
echo 'i2c-ELAN9008:00' | pkexec tee /sys/bus/i2c/drivers/i2c_hid_acpi/unbind > /dev/null
```
```
echo 'i2c-ELAN9008:00' | pkexec tee /sys/bus/i2c/drivers/i2c_hid_acpi/bind > /dev/null                         
```






  ```

