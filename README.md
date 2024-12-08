# Fedora41_setup
Mémo pour le setup complet de Fedora 41
  
   

## **1 - Installation**

* a - Désactiver `Secure Boot` dans le Bios (F2)

* b - Désactiver la caméra et le lecteur de carte dans le bios

* c - Graver l'iso `Fedora-Everything-netinst`

* d - Utiliser `systemd-boot` plutot que Grub : passer l'argument suivant dans le kernel de 
l'iso  d'installation (en pressant Espace au boot) juste avant QUIET
  
```
inst.sdboot
```




## **2 - Allégement du système**

* a - Supprimer les logiciels inutiles avec Gnome-software
    

* b - Supprimer les logiciels suivants avec le terminal :
  
```
sudo dnf remove speech-dispatcher
sudo dnf remove gnome-remote-desktop
sudo dnf vim*
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
sudo dnf remove firewalld
sudo dnf remove rygel
sudo dnf remove totem
sudo dnf remove avahi-tools
sudo dnf remove virtualbox-guest-additions
sudo dnf remove gnome-boxes
```

    
* c - Supprimer et masquer les services inutiles :
  
```
sudo systemctl mask NetworkManager-wait-online.service
sudo systemctl mask auditd.service
sudo systemctl mask ModemManager.service
sudo systemctl mask avahi-daemon.service
sudo systemctl mask plymouth-quit-wait.service
sudo systemctl mask switcheroo-control.service
sudo systemctl mask sys-kernel-tracing.mount
sudo systemctl mask sys-kernel-debug.mount
sudo systemctl mask httpd.service
sudo systemctl mask mdmonitor.service
sudo systemctl mask mdmonitor.service
sudo systemctl mask raid-check.timer
sudo systemctl mask sssd-kcm.service
sudo systemctl mask pcscd
sudo systemctl mask raid-check.timer
sudo systemctl mask fwupd
sudo systemctl mask avahi-daemon.socket
sudo systemctl mask sssd-kcm.socket
sudo systemctl mask pcscd.socket
sudo systemctl mask sssd.service
```
  
et désactiver le Bluetooth pour l'activer à la volée (voir script dans la rubrique UI Gnome) + cups :
  
```
sudo systemctl disable bluetooth.service
sudo systemctl disable cups
```
  
Enfin, reboot puis controle de l'état des services avec :
```
systemd-analyze blame | grep -v '\.device$'
```

et :
```
systemctl list-unit-files --type=service --state=enabled
```


* d - Alléger les journaux système et les mettre en RAM :
```
sudo gnome-text-editor /usr/lib/systemd/journald.conf
```
puis remplacer le contenu du fichier par celui du fichier `journald.conf.txt` & relancer le service :
```
sudo systemctl restart systemd-journald
```
  
* e - Supprimer les `coredump` en éditant systemd :
  
``` 
sudo gnome-text-editor /usr/lib/systemd/coredump.conf
```
Editer le fichier comme suit :
```
[Coredump]
Storage=none
ProcessSizeMax=0
```

* e - Supprimer le lancement au boot de gnome-software : dans dconf-editor, désactiver les deux options `update` dans org/gnome/software


* f - Supprimer le `watchdog` et blacklister les pilotes inutiles `Nouveau` & `ELAN:Fingerprint` : éditer le fichier suivant :
  
olution pour Fedora 41 : Utiliser /etc/sysctl.d/

    Créer un fichier de configuration spécifique : Créez un fichier dans le répertoire /etc/sysctl.d/ pour ajouter votre modification. Ce répertoire est destiné aux fichiers de configuration sysctl personnalisés, et les fichiers qu'il contient sont chargés automatiquement au démarrage.

    Voici la procédure :

        Ouvrez un terminal et créez un fichier, par exemple 99-custom.conf, dans /etc/sysctl.d/ :

sudo gnome-text-editor /etc/sysctl.d/99-custom.conf

Ou, si vous préférez un éditeur en ligne de commande, utilisez nano :

    sudo nano /etc/sysctl.d/99-custom.conf

Ajouter la ligne pour désactiver le watchdog :

Dans le fichier ouvert, ajoutez la ligne suivante pour désactiver le nmi_watchdog :

kernel.nmi_watchdog=0

Sauvegarder et fermer :

    Dans gnome-text-editor, cliquez sur "Enregistrer" et fermez.
    Si vous utilisez nano, appuyez sur CTRL+O pour sauvegarder et CTRL+X pour quitter.

Appliquer les changements immédiatement : Après avoir créé ce fichier, vous pouvez appliquer les modifications sans redémarrer en exécutant :

    sudo sysctl --system

    Cela rechargera toutes les configurations sysctl et appliquera vos changements.

    Vérification des fichiers de configuration sysctl

    Vérifier que la modification a été appliquée :

    Pour vérifier que votre configuration a bien été appliquée, vous pouvez utiliser la commande suivante pour vérifier l'état de nmi_watchdog :

sudo sysctl kernel.nmi_watchdog

Si la configuration est correctement appliquée, la sortie devrait être :

kernel.nmi_watchdog = 0


Puis créer un fichier `blacklist` ```sudo gnome-text-editor /etc/modprobe.d/blacklist.conf``` et l'éditer :
  ```
blacklist iTCO_vendor_support
blacklist wdat_wdt
blacklist intel_pmc_bxt
blacklist nouveau
blacklist ELAN:Fingerprint
```


  


## **3 - Optimisation du système**


* a - Désactiver `SElinux` :
  
```
sudo gnome-text-editor /etc/selinux/config
```
et saisir ```SELINUX=disabled```
  
Vérifier la désactivation après reboot avec la commande ```sestatus```

Enfin supprimer les labels SElinux avec :
 
```
sudo find / -print0 | xargs -r0 setfattr -x security.selinux 2>/dev/null
```
  

* b - Passer `xwayland` en autoclose : sur dconf-editor, modifier la clé suivante.
  
```
org.gnome.mutter experimental-features
```


* c - Optimiser le kernel :
  
```
sudo gnome-text-editor /etc/kernel/cmdline
```

Puis saisir :
```
mitigations=off selinux=0 cgroup_disable=rdma nmi_watchdog=0
```
puis reinstaller le noyau avec la commande suivante :
  
```
sudo kernel-install add $(uname -r) /lib/modules/$(uname -r)/vmlinuz
```

```
sudo dracut
```
  
Au reboot, contrôler le fichier de boot de `systemd-boot` avec la commande :
```
cat /proc/cmdline
```

* d - Réduire le temps d'affichage du menu systemd-boot à 0 seconde ou une seconde, au choix:

```
sudo bootctl set-timeout 0
```

* e - Editer le mount des partitions BTRFS `/` et `/home` avec la commande :

```
sudo gnome-text-editor /etc/fstab
```
puis saisir les flags suivants :

```
noatime,commit=120,discard=async,space_cache=v2
```
Contrôler avec `cat /etc/fstab` après un reboot.

   
* f - Mettre les fichiers temporaires en RAM :
  
```
sudo gnome-text-editor /etc/fstab
```
puis saisir :
  
```
tmpfs /tmp tmpfs defaults,noatime,mode=1777,nosuid,size=4196M 0 0
```
Contrôler avec `cat /etc/fstab` après un reboot.  

* g - Activer et régler le pare-feu :
  
```
sudo systemctl enable ufw
sudo systemctl start ufw
sudo ufw logging off
sudo ufw default deny incoming
sudo ufw default allow outgoing
```
  
pour nicotine :
```
sudo ufw allow in 2234/tcp
```

pour Fragments :
```
sudo ufw allow in 51413/tcp
sudo ufw allow in 51413/udp
```

pour le serveur FTP du SSD de la TV Android :
```
sudo ufw allow 2121/tcp
sudo ufw allow 1024:1048/tcp
sudo ufw enable
sudo ufw status
```


* h - Modifier le `swappiness` :
  
```
echo vm.swappiness=5 | sudo tee -a /etc/sysctl.d/99-sysctl.conf
echo vm.vfs_cache_pressure=50 | sudo tee -a /etc/sysctl.d/99-sysctl.conf
sudo sysctl -p /etc/sysctl.d/99-sysctl.conf
```

  
* i - Accélérer `DNF` : A MODIFIER POUR DNF5
  
  ```
  echo 'max_parallel_downloads=20' | sudo tee -a /etc/dnf/dnf.conf

  ```
  
* j - Passer à 1 le nombre de `ttys` au boot  :
  
```
sudo gnome-text-editor /usr/lib/systemd/logind.conf
```
puis décommenter et editer `NautoVTS=1`

* k - Vérifier que le système utilise bien les DNS du routeur Xiaomi (192.168.31.1) :

```
nmcli dev show |grep DNS
```



## **4 - Remplacement et installation de logiciels et codecs**

* a - Ajouter les sources `RPMFusion` :
  
RPMFusion Free
```
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E%fedora).noarch.rpm 
```

RMPFusion Non free
```
sudo dnf install https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```
    
* c - Ajouter les codecs `FFMPEG`, multimedia, `AV1`, & le `pilote Intel` d'accélération matérielle :

```
sudo dnf swap ffmpeg-free ffmpeg --allowerasing
sudo dnf install intel-media-driver
sudo dnf update @multimedia --setopt="install_weak_deps=False" --exclude=PackageKit-gstreamer-plugin
```

  
* e - Installer les logiciels Flatpak suivants : nota : utiliser prioritairement les flatpaks Fedora OU Flathub car les runtimes ne sont pas partagés entre les 2.

```
flatpak install flathub com.mattjakeman.ExtensionManager -y
flatpak install flathub io.github.giantpinkrobots.flatsweep -y
flatpak install flathub io.missioncenter.MissionCenter flatpak run io.missioncenter.MissionCenter-y
flatpak install flathub org.jdownloader.JDownloader -y
flatpak install flathub org.onlyoffice.desktopeditors -y
flatpak install flathub de.haeckerfelix.Fragments -y
flatpak install flathub org.gnome.Papers -y
flatpak install flathub page.codeberg.libre_menu_editor.LibreMenuEditor -y
flatpak install flathub com.mattjakeman.ExtensionManager -y
flatpak install flathub io.github.celluloid_player.Celluloid -y
flatpak install flathub org.gnome.Epiphany -y
flatpak install flathub org.nicotine_plus.Nicotine -y
```

    
* f - Installer les logiciels suivants avec dnf :

```
sudo dnf install dconf-editor -y
sudo dnf install gnome-tweaks -y
sudo dnf install powertop -y
sudo dnf install zstd -y
sudo dnf install ffmpegthumbnailer.x86_64 -y
sudo dnf install profile-cleaner -y
sudo dnf install btrfs-assistant -y
sudo dnf install seahorse -y
sudo dnf install ufw -y
```

* h - Installer [Dropbox](https://www.dropbox.com/fr/install-linux)





## **5 - Réglages de l'UI Gnome Shell**

* a - Régler le système avec Paramètres (penser à désactiver les animations dans Accessibilité??) puis Ajustements (Changer les polices d'écriture pour `Noto Sans` en 11 ?)

* b - Régler Nautilus & créer un marque-page pour `Dropbox` & pour l'accès `ftp` au disque SSD sur la TV Android :
  
```
192.168.31.68:2121
```

* c - Modifier le mot de passe au démarrage avec le logiciel Mots de Passe, puis laisser les champs vides. Penser à reconnecter le compte Google dans Gnome.

* d - Changer le [wallpaper](https://github.com/CubeJ/LinuxWallpaper)

* e - Régler HiDPI sur 175, cacher les dossiers Modèles, Bureau, ainsi que le wallaper et l'image user, augmenter la taille des icones dossiers.

* f - Installer diverses extensions (2 temporaires, 10 permanentes) :
  
1 - [Alphabetical Grid](https://extensions.gnome.org/extension/4269/alphabetical-app-grid/) puis la supprimer : l'ordre alphabetique persistera.

2 - [Privacy Quick Settings](https://extensions.gnome.org/extension/4491/privacy-settings-menu/) puis la supprimer une fois les réglages réalisés.

3 - [Appindicator](https://extensions.gnome.org/extension/615/appindicator-support/)

4 - [AutoActivities](https://extensions.gnome.org/extension/5500/auto-activities/)
  
5 - [Battery Time](https://extensions.gnome.org/extension/5425/battery-time/)
    
6 - [Caffeine](https://extensions.gnome.org/extension/517/caffeine/)
  
7 - [Clipboard History](https://extensions.gnome.org/extension/4839/clipboard-history/)
  
8 - [Frequency Boost Switch](https://extensions.gnome.org/extension/4792/frequency-boost-switch/)
    
9 - [Hot Edge](https://extensions.gnome.org/extension/4222/hot-edge/)
    
10 - [Grand Theft Focus](https://extensions.gnome.org/extension/5410/grand-theft-focus/)
    
11 - [Hide Activities Button](https://extensions.gnome.org/extension/744/hide-activities-button/)

12 - [Auto Screen Brightness](https://extensions.gnome.org/extension/7311/auto-screen-brightness/) & supprimer la luminosité automatique dans Settings de Gnome

13 - User Themes

et désactiver l'extension native `Background logo`

* g - Installer [Nautilus-admin](https://download.copr.fedorainfracloud.org/results/tomaszgasior/mushrooms/fedora-41-x86_64/07341996-nautilus-admin/nautilus-admin-1.1.9-5.fc41.noarch.rpm) puis lancer la commande ```nautilus -q``` pour relancer Fichiers

* h - Raccourcis à éditer dans Gnome : mettre `ptyxis` à la place de la touche Exposant, et la commande ```flatpak run io.missioncenter.MissionCenter``` pour la combinaison `ctrl-alt-supp`.

* i - Régler Gnome-text-editor et Ptyxis; améliorer l'autocomplétion du terminal en créant le fichier`.inputrc` et le placer dans `~/` :
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

  
* j - Améliorer  Celluloid :
- inscrire `vo=gpu-next` dans Paramètres --> Divers --> Options supplémentaires
- installer les deux scripts lua suivants pour la musique :
[Visualizer](https://www.dropbox.com/scl/fi/bbwlvfhtjnu8sgr4yoai9/visualizer.lua?rlkey=gr3bmjnrlexj7onqrxzjqxafl&dl=0)
[Delete File avec traduction française](https://www.dropbox.com/scl/fi/c2cacmw2a815husriuvc1/delete_file.lua?rlkey=6b9d352xtvybu685ujx5mpv7v&dl=0)
- activer l'option `focus` et `toujours afficher les boutons de titre`
  

* k - Modifier Jdownloader`: réglages de base, thème Dark Moon puis icones Flat, puis désactiver les éléments suivants : tooltip, help, Update Button Flashing, banner, Premium Alert, Donate, speed meter visible.


* l - Télécharger le script de `transfert des vidéos` intitulé `.transfert_videos` pour déplacer automatiquement les vidéos vers Vidéos en supprimant le sous-dossier d'origine : en faire un raccourci avec l'éditeur de menu MenuLibre (Menu principal n'y parvient pas) et lui mettre l'icone `/usr/share/icons/Adwaita/scalable/devices/drive-multidisk.svg`


* m - Télécharger le script de `bascule Bluetooth` `.bluetooth_toggle` pour activer/désactiver le service bluetooth à la volée : en faire un raccourci avec l'éditeur de menu e MenuLibre (Menu principal n'y parvient pas) et mettre l'icone `/usr/share/icons/Adwaita/scalable/devices/phone.svg`.

* n - Accélérer les animations :  saisir ```GNOME_SHELL_SLOWDOWN_FACTOR=0.5``` dans le fichier ```sudo gnome-text-editor /etc/environment```

* o - Mettre le thème [Adwaita-Darker](https://github.com/varunbpatil/Adwaita-darker)

* p - Curseurs [Bibata Ice](https://objects.githubusercontent.com/github-production-release-asset-2e65be/108837747/0348a382-abba-45ca-9bea-e4ebd0865801?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20241208%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241208T153811Z&X-Amz-Expires=300&X-Amz-Signature=02308e1abe01f1bee052debfb0141a8ce43a03c40817ddc14f3607d0de73ff81&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DBibata-Modern-Ice.tar.xz&response-content-type=application%2Foctet-stream) à copier-coller dans le dossier /home/ogu/.local/share/icons (dossier `icons` à créer), puis ferme rla session et activer avec Tweaks.
Nota : vérifier si une release plus récente est disponible pour Bibata Ice NO RIGHT

* q - Faire le tri dans `~/.local/share/`, `/home/ogu/.config/`, `/usr/share/` et `/etc/`



   
## **6 - Réglages du navigateur Firefox**

* a - Réglages internes de Firefox (penser à activer CTRL-TAB pour faire défiler dans l'ordre d'utilisation)

* b - Changer le thème pour [Materia Dark](https://addons.mozilla.org/fr/firefox/addon/materia-dark-theme/)

* c - Dans about:config :
`nglayout.initialpaint.delay` = 1
`browser.sessionstore.interval` à `600000` pour réduire l'intervalle de sauvegarde des sessions
`extensions.pocket.enabled` = false et supprimer Pocket de la barre d'outil si besoin
`devtools.f12_enabled` = false
`accessibility.force_disabled` = 1 pour supprimer l'accessibilité
`extensions.screenshots.disabled` = true pour désactiver le screenshot


  
* c - Extensions
  
[Enhancer for Youtube](https://chromewebstore.google.com/detail/enhancer-for-youtube/ponfpcnoihfmfllpaingbgckeeldkhle?hl=fr) qui intègre leurs fonctions. Le configurer d'un coup en rentrant le code du fichier `youtube_enhancer_conf`

[uBlock Origin](https://addons.mozilla.org/fr/firefox/addon/ublock-origin/)
  
[New Tab Suspender](https://addons.mozilla.org/en-US/firefox/addon/new-tab-suspender/)

[Raindrop](https://raindrop.io/r/extension/firefox) et supprimer `Pocket` de Firefox avec `extensions.pocket.enabled` dans `about:config` puis supprimer le raccourci dans la barre.
  
[Clear Browsing Data](https://addons.mozilla.org/fr/firefox/addon/clear-browsing-data/)
  
[Undo Close Tab Button](https://addons.mozilla.org/firefox/addon/undoclosetabbutton) et mettre ALT-Z comme raccourci à partir du menu général de sextensions (roue dentée)

[LocalCDN](https://addons.mozilla.org/fr/firefox/addon/localcdn-fork-of-decentraleyes/)


* l - Activer ``openh264`` dans les plugins firefox.






## **7 - Maintenance de la distribution**

```
sudo dnf autoremove
sudo dnf -y upgrade --refresh
flatpak update
```

Unmask temporaire de fwupd puis 
sudo fwupdmgr get-devices 
sudo fwupdmgr refresh --force 
sudo fwupdmgr get-updates 
sudo fwupdmgr update
???


















Boot time : avant optimisation :
Startup finished in 2.213s (firmware) + 500ms (loader) + 1.806s (kernel) + 3.901s (initrd) + 28.363s (userspace) = 36.786s


Boot time après désactivation des services inutiles :
Startup finished in 2.314s (firmware) + 505ms (loader) + 1.865s (kernel) + 4.035s (initrd) + 3.633s (userspace) = 12.354s 

Boot time après blacklist, selinux-disabled, mitigations=off, fstab etc...
Startup finished in 2.306s (firmware) + 503ms (loader) + 1.771s (kernel) + 3.958s (initrd) + 3.336s (userspace) = 11.876s 





   A TESTER :
    
* n - Créer un toggle `Powertop` qui va lancer powertop en `auto-tune` pour économiser encore plus de batterie, et baisser la luminosité sur 5% : rentrer cette commande pour le toggle activé :
```
pkexec powertop --auto-tune && gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness " <int32 5>"()
```
  
Et cette commande pour le toggle désactivé :
```
gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness " <int32 2O>"()
```
Enfin rentrer le nom de l'icone : `thunderbolt-symbolic` 

* o - Créer un toggle "No Touchscreen" et le rendre permanent au boot :
    
```
echo 'i2c-ELAN9008:00' | pkexec tee /sys/bus/i2c/drivers/i2c_hid_acpi/unbind > /dev/null
```
```
echo 'i2c-ELAN9008:00' | pkexec tee /sys/bus/i2c/drivers/i2c_hid_acpi/bind > /dev/null                         
```



* l - EXPERIMENTAL : créer un initramfs plus petit et plus rapide en désactivant des modules inutiles : manipulation à faire à chaque màj du kernel : d'abord désactiver vconsole :

  ```
  cp /usr/bin/true /usr/lib/systemd/systemd-vconsole-setup

  ```
     puis créer un fichier de configuration `dracut` (ou dracut --regenerate-all), ou télécharger directement le fichier dracut.conf.

  ```
  sudo gnome-text-editor /etc/dracut.conf.d/dracut.conf
  ```
  
     et copier-coller ces options de configuration :

  ```
  # Configuration du fichier dracut.conf pour obtenir un initrd le plus léger possible

  omit_dracutmodules+=" multipath nss-softokn memstrack usrmount mdraid dmraid debug selinux fcoe fcoe-uefi terminfo 
  watchdog crypt-gpg crypt-loop cdrom pollcdrom pcsc ecryptfs rescue watchdog-module network cifs nfs nbd brltty 
  busybox rdma i18n isci wacom "
  omit_drivers+=" nvidia amd nouveau "
  filesystems+=" ext4 btrfs fat "
  # Ne pas exécuter fsck
  nofscks="yes"
  # Niveau de journalisation
  stdlog="0"
  # Compression de l'initramfs
  compress="zstd"
  compress_options="-4"
  # Mode silencieux
  quiet="yes"
  # Autres options
  force="yes"
  hostonly="yes"
  ```
  
     Vérifier l'output après sudo dracut : `sudo lsinitrd -m`




* e - Supprimer les flatpaks KDE :
  
  ```
  flatpak remove org.kde.KStyle.Adwaita org.kde.PlatformTheme.QGnomePlatform     
  org.kde.WaylandDecoration.QAdwaitaDecorations QGnomePlatform-decoration  
  org.kde.WaylandDecoration.QGnomePlatform-decoration   org.kde.Platform 
  ```

