# 🐧 ***Fedora 41 setup & config*** 

Mémo pour le setup complet de Fedora 41 sur laptop ASUS ZENBOOK S13 FLIP OLED UP5302Z

Table des matières:

A - [Installation](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-a---installation)

B - [Allégement du système](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-b---all%C3%A9gement-du-syst%C3%A8me)

C - [Optimisation du système](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-c---optimisation-du-syst%C3%A8me)

D - [Remplacement et installation de logiciels](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-d---remplacement-et-installation-de-logiciels-et-codecs)

E - [Réglages de l'UI Gnome Shell](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-e---r%C3%A9glages-de-lui-gnome-shell)

F - [Réglages de Firefox](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-f---r%C3%A9glages-du-navigateur-firefox)

E - [Maintenance et mises à jour](https://github.com/Shogu/Fedora41-setup-config/blob/main/README.md#-g---maintenance-de-la-distribution)
   

## 💾 **A - Installation**

* **1** - Désactiver `Secure Boot` dans le Bios (F2)

* **2** - Désactiver la caméra et le lecteur de carte dans le bios

* **3** - Graver l'iso `Fedora-Everything-netinst`

* **4** - Utiliser `systemd-boot` plutot que Grub : passer l'argument suivant dans le kernel de l'iso  d'installation (en pressant Espace au boot) juste avant QUIET
```
inst.sdboot
```



## ✨ **B - Allégement du système**

* **5** - Supprimer les logiciels inutiles avec Gnome-software
  
* **6** - Supprimer les logiciels suivants avec le terminal :
```
sudo dnf remove libertas-firmware
sudo dnf remove cirrus-audio-firmware
sudo dnf remove amd-gpu-firmware
sudo dnf remove amd-ucode-firmware
sudo dnf remove atheros-firmware
sudo dnf remove brcmfmac-firmware
sudo dnf remove tiwilink-firmware
sudo dnf remove nxpwireless-firmware
sudo dnf remove mt7xxx-firmware
sudo dnf remove nvidia-gpu-firmware 
sudo dnf remove speech-dispatcher
sudo dnf remove gnome-remote-desktop
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
```
    
* **7** - Supprimer et masquer les services inutiles :
```
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
```
  
et désactiver le Bluetooth pour l'activer à la volée (voir script dans la rubrique  Gnome) + cups :
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

* **8** - Alléger les journaux système et les mettre en RAM :
```
sudo gnome-text-editor /usr/lib/systemd/journald.conf
```
puis remplacer le contenu du fichier par celui du fichier `journald.conf.txt` & relancer le service :
```
sudo systemctl restart systemd-journald
```

* **9** - Remplacer chronyd par systemd-timesyncd (plus rapide au boot) ([source](https://www.dsfc.net/systeme/linux/ntp-passage-de-chrony-a-systemd-timesyncd/))
```
sudo dnf remove chrony
sudo systemctl enable systemd-timesyncd
sudo gnome-text-editor /usr/lib/systemd/timesyncd.conf
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

* **10** - Supprimer les `coredump` en éditant systemd : 
``` 
sudo gnome-text-editor /usr/lib/systemd/coredump.conf
```
Editer le fichier comme suit :
```
[Coredump]
Storage=none
ProcessSizeMax=0
```

* **11** - Supprimer le `watchdog`
```
sudo gnome-text-editor /etc/sysctl.d/99-custom.conf
```

et saisir : `kernel.nmi_watchdog=0`, puis relancer avec : ```sudo sysctl --system```

Reboot & contrôle avec :
```
sudo sysctl kernel.nmi_watchdog
```

* **12** - Blacklister les pilotes inutiles `Nouveau` & `ELAN:Fingerprint` : créer un fichier `blacklist` ```sudo gnome-text-editor /etc/modprobe.d/blacklist.conf``` et l'éditer :
```
blacklist iTCO_vendor_support
blacklist wdat_wdt
blacklist intel_pmc_bxt
blacklist nouveau
blacklist ELAN:Fingerprint
```



## 🚀 **C - Optimisation du système**

* **13** - Désactiver `SElinux` :
```
sudo gnome-text-editor /etc/selinux/config
```
et saisir ```SELINUX=disabled```
  
Vérifier la désactivation après reboot avec la commande ```sestatus```

Enfin supprimer les labels SElinux avec :
```
sudo find / -print0 | xargs -r0 setfattr -x security.selinux 2>/dev/null
```

* **14** - Passer `xwayland` en autoclose : sur dconf-editor, modifier la clé suivante.
```
org.gnome.mutter experimental-features
```

* **15** - Optimiser le kernel :
```
sudo gnome-text-editor /etc/kernel/cmdline
```

Puis saisir :
```
mitigations=off selinux=0 cgroup_disable=rdma nmi_watchdog=0 loglevel=1
```
puis reinstaller le noyau avec la commande suivante :
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

* **16** - Réduire le temps d'affichage du menu systemd-boot à 0 seconde ou une seconde, au choix:
```
sudo bootctl set-timeout 0
```

* **17** - Editer le mount des partitions BTRFS `/` et `/home` avec la commande :
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

* **18** - Mettre les fichiers temporaires en RAM :
```
sudo gnome-text-editor /etc/fstab
```
puis saisir :
  
```
tmpfs /tmp tmpfs defaults,noatime,mode=1777,nosuid,size=4196M 0 0
```
Contrôler avec `cat /etc/fstab` après un reboot.  

* **19** - Régler le pare-feu :
  
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

* **20** - Modifier le `swappiness` :
```
echo vm.swappiness=5 | sudo tee -a /etc/sysctl.d/99-sysctl.conf
echo vm.vfs_cache_pressure=50 | sudo tee -a /etc/sysctl.d/99-sysctl.conf
sudo sysctl -p /etc/sysctl.d/99-sysctl.conf
```
  
* **21** - Accélérer `DNF` : 
```
echo 'max_parallel_downloads=10' | sudo tee -a /etc/dnf/dnf.conf
```
  
* **22** - Passer à 1 le nombre de `ttys` au boot  :  
```
sudo gnome-text-editor /usr/lib/systemd/logind.conf
```
puis décommenter et editer `NautoVTS=1`

* **23** - Vérifier que le système utilise bien les DNS du routeur Xiaomi (192.168.31.1) :
```
nmcli dev show |grep DNS
```

**Boot time : avant optimisation :
Startup finished in 5.8s (firmware) + 508ms (loader) + 1.896s (kernel) + 4s (initrd) + 11.5s (userspace) = 23.7s**

**Boot time après optimisation :
Startup finished in 2.324s (firmware) + 509ms (loader) + 1.986s (kernel) + 4.020s (initrd) + 3.234s (userspace) = 12.075s**



## 📦 **D - Remplacement et installation de logiciels et codecs**

* **24** - Ajouter les sources `RPMFusion` :
  
**RPMFusion Free**
```
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E%fedora).noarch.rpm 
```

**RMPFusion Non free**
```
sudo dnf install https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```
    
* **25** - Ajouter les codecs `FFMPEG`, multimedia, `AV1`, & le `pilote Intel` d'accélération matérielle :
```
sudo dnf swap ffmpeg-free ffmpeg --allowerasing
sudo dnf install intel-media-driver
sudo dnf update @multimedia --setopt="install_weak_deps=False" --exclude=PackageKit-gstreamer-plugin
```

* **26** - Réglages de gnome-software

* **27** - Installer les logiciels Flatpak suivants : nota : utiliser prioritairement les flatpaks Fedora OU Flathub car les runtimes ne sont pas partagés entre les 2.
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
flatpak install flathub org.gnome.Epiphany -y
flatpak install flathub org.nicotine_plus.Nicotine -y
```

* **28** - Installer les logiciels suivants avec dnf :
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
```

* **29** - Installer `Dropbox` avec Maestral :
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

* **30** - Désinstaller `gnome-software` et `packagekit` (ainsi que le cache) pour éviter leur lancement au boot :
  
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



## 🐾 **E - Réglages de l'UI Gnome Shell** 

* **31** - Régler le système avec Paramètres (penser à désactiver les animations dans Accessibilité??) puis Ajustements (Changer les polices d'écriture pour `Noto Sans` en 11 ?)

* **32** - Régler Nautilus & créer un marque-page pour `Dropbox` & pour l'accès `ftp` au disque SSD sur la TV Android :
  
```
192.168.31.68:2121
```

* **33** - Modifier le mot de passe au démarrage avec le logiciel Mots de Passe, puis laisser les champs vides. Penser à reconnecter le compte Google dans Gnome!

* **34** - Installer le [wallpaper Fedora 34](https://fedoraproject.org/w/uploads/d/de/F34_default_wallpaper_night.jpg)

* **35** - Régler HiDPI sur 175, cacher les dossiers Modèles, Bureau, ainsi que le wallaper et l'image user, augmenter la taille des icones dossiers.

* **36** - Installer diverses extensions :
  
a - [Alphabetical Grid](https://extensions.gnome.org/extension/4269/alphabetical-app-grid/)

b - [Privacy Quick Settings](https://extensions.gnome.org/extension/4491/privacy-settings-menu/) puis la supprimer une fois les réglages réalisés.

c - [Appindicator](https://extensions.gnome.org/extension/615/appindicator-support/)

d - [AutoActivities](https://extensions.gnome.org/extension/5500/auto-activities/)
  
e - [Battery Time Percentage Compact](https://extensions.gnome.org/extension/2929/battery-time-percentage-compact/) ou [Battery Time](https://extensions.gnome.org/extension/5425/battery-time/)
    
f - [Caffeine](https://extensions.gnome.org/extension/517/caffeine/)
  
g - [Clipboard History](https://extensions.gnome.org/extension/4839/clipboard-history/)
  
h - [Frequency Boost Switch](https://extensions.gnome.org/extension/4792/frequency-boost-switch/)
    
i - [Hot Edge](https://extensions.gnome.org/extension/4222/hot-edge/)
    
j - [Grand Theft Focus](https://extensions.gnome.org/extension/5410/grand-theft-focus/)
    
k - [Hide Activities Button](https://extensions.gnome.org/extension/744/hide-activities-button/)

l - [Auto Screen Brightness](https://extensions.gnome.org/extension/7311/auto-screen-brightness/) & supprimer la luminosité automatique dans Settings de Gnome

m- [Auto Power Profile](https://extensions.gnome.org/extension/6583/auto-power-profile/)

n - [Remove World Clock](https://extensions.gnome.org/extension/6973/remove-world-clocks/)

et désactiver l'extension native `Background logo`

* **37** - Installer [Nautilus-admin](https://download.copr.fedorainfracloud.org/results/tomaszgasior/mushrooms/fedora-41-x86_64/07341996-nautilus-admin/nautilus-admin-1.1.9-5.fc41.noarch.rpm) puis lancer la commande ```nautilus -q``` pour relancer Fichiers

* **38** - Raccourcis à éditer dans Gnome : mettre `ptyxis` à la place de la touche Exposant, et la commande ```flatpak run net.nokyan.Resources``` pour la combinaison `ctrl-alt-supp`.

* **39** - Régler Gnome-text-editor et Ptyxis; améliorer l'autocomplétion du terminal en créant le fichier`.inputrc` et le placer dans `~/` :
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
  
* **40** - Celluloid :
inscrire `vo=gpu-next` dans Paramètres --> Divers --> Options supplémentaires, activer l'option `focus` et `toujours afficher les boutons de titre`, enfin installer les deux scripts lua suivants pour la musique :
[Visualizer](https://www.dropbox.com/scl/fi/bbwlvfhtjnu8sgr4yoai9/visualizer.lua?rlkey=gr3bmjnrlexj7onqrxzjqxafl&dl=0)
[Delete File avec traduction française](https://www.dropbox.com/scl/fi/c2cacmw2a815husriuvc1/delete_file.lua?rlkey=6b9d352xtvybu685ujx5mpv7v&dl=0)

* **41** - `Jdownloader`: réglages de base, thème Black Moon puis icones Flat; font Noto Sans Regular, désactivatioin du dpi et font sur 175; puis désactiver les éléments suivants : tooltip, help, Update Button Flashing, banner, Premium Alert, Donate, speed meter visible.

* **42** - Script de `transfert des vidéos` intitulé `.transfert_videos` pour déplacer automatiquement les vidéos vers Vidéos en supprimant le sous-dossier d'origine : en faire un raccourci avec l'éditeur de menu, passer le chemin `sh /home/ogu/.transfert_videos.sh` et lui mettre l'icone `/usr/share/icons/Adwaita/scalable/devices/drive-multidisk.svg`

* **43** - Script de `bascule Bluetooth` `.bluetooth_toggle` pour activer/désactiver le service bluetooth à la volée : en faire un raccourci avec l'éditeur de menu, raccourci d'exécution `bash /home/ogu/.bluetooth_toggle.sh` & mettre l'icone `/usr/share/icons/Adwaita/scalable/devices/phone.svg`.

* **44** - Accélérer les animations :  saisir ```GNOME_SHELL_SLOWDOWN_FACTOR=0.5``` dans le fichier ```sudo gnome-text-editor /etc/environment```

* **45** - Changer avec Menu Principal l'icone de Ptyxis, en la remplaçant par celle de [gnome-terminal](https://upload.wikimedia.org/wikipedia/commons/d/da/GNOME_Terminal_icon_2019.svg)

* **46** - `Scripts` Nautilus : Dropbox.py, Hide.py et Unhide.py à télécharger puis à coller dans le fichier /home/ogu/.local/share/nautilus/scripts/. Penser à les rendre exécutables!

* **47** - `LibreOffice` : régler l'UI et les paramètres, désactiver Java, rajouter `-nologo` au raccourci avec l'éditeur de menu pour supprimer le splash screen, passer à `600000000` la valeur de `Graphic Manager` + `UseOpenGL` = true + `UseSkia` = true dans la Configuration Avancée + désactiver l'enregistrement des données personnelles dans les fichiers (Menu Sécurité). 

* **48** - Faire le tri dans `~/.local/share/`, `/home/ogu/.config/`, `/usr/share/` et `/etc/`


 
## 🌐 **F - Réglages du navigateur Firefox**

* **49** - Réglages internes de Firefox (penser à activer CTRL-TAB pour faire défiler dans l'ordre d'utilisation)

* **50** - Changer le thème pour [Materia Dark](https://addons.mozilla.org/fr/firefox/addon/materia-dark-theme/) ou [Gnome Dark ](https://addons.mozilla.org/fr/firefox/addon/adwaita-gnome-dark/?utm_content=addons-manager-reviews-link&utm_medium=firefox-browser&utm_source=firefox-browser)

* **51** - Dans about:config :
  
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

* **52** - Extensions
  
a - [uBlock Origin](https://addons.mozilla.org/fr/firefox/addon/ublock-origin/) : réglages à faire + import des deux listes sauvegardées
  
b - [New Tab Suspender](https://addons.mozilla.org/en-US/firefox/addon/new-tab-suspender/) ou [Tab Suspender Mini}(https://addons.mozilla.org/en-US/firefox/addon/tab-suspender-mini/), ce dernier semblant plus réactif + icone d'hibernation dans chaque onglet mais possiblement cause de lags, ou bien le classique [Auto Tab Discard](https://addons.mozilla.org/fr/firefox/addon/auto-tab-discard/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=featured), bien plus configurable : importer les réglages avec le fichier de backup et bien activer les 2 options de dégel des onglets à droite et à gauche de l'onglet courant.

c - [Raindrop](https://raindrop.io/r/extension/firefox) et supprimer `Pocket` de Firefox avec `extensions.pocket.enabled` dans `about:config` puis supprimer le raccourci dans la barre.
  
d - [Clear Browsing Data](https://addons.mozilla.org/fr/firefox/addon/clear-browsing-data/)
  
e - [Undo Close Tab Button](https://addons.mozilla.org/firefox/addon/undoclosetabbutton) et mettre ALT-Z comme raccourci à partir du menu général des extensions (roue dentée)

f - [LocalCDN](https://addons.mozilla.org/fr/firefox/addon/localcdn-fork-of-decentraleyes/), puis faire le [test](https://decentraleyes.org/test/).

g - [Side View](https://addons.mozilla.org/fr/firefox/addon/side-view/)

* **54** - Activer `openh264` & `widevine` dans les plugins firefox.



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

Regarder script de F39
























  💡 A TESTER :
    
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

* EXPERIMENTAL : créer un initramfs plus petit et plus rapide en désactivant des modules inutiles : manipulation à faire à chaque màj du kernel : d'abord désactiver vconsole :

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




* Supprimer les flatpaks KDE :
  
  ```
  flatpak remove org.kde.KStyle.Adwaita org.kde.PlatformTheme.QGnomePlatform     
  org.kde.WaylandDecoration.QAdwaitaDecorations QGnomePlatform-decoration  
  org.kde.WaylandDecoration.QGnomePlatform-decoration   org.kde.Platform 
  ```

