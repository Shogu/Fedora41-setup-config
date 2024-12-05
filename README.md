# Fedora41_setup
Mémo pour le setup complet de Fedora 41


# Fedora_config pour ASUS ZENBOK S13 FLIP OLED


Tips &amp; tricks de configuration de Fedora 39

  
Sommaire :

1. [Installation](https://github.com/Shogu/Configuration-Fedora-ASUS-Zenbook-13/blob/main/README.md#1---installation)

2. [Réglages de base](https://github.com/Shogu/Configuration-Fedora-ASUS-Zenbook-13/blob/main/README.md#2---réglages-de-base)

3. [Remplacement et installation de logiciels et codecs](https://github.com/Shogu/Configuration-Fedora-ASUS-Zenbook-13/blob/main/README.md#3---remplacement-et-installation-de-logiciels-et-codecs)

4. [Réglages des navigateurs Opera & Firefox](https://github.com/Shogu/Configuration-Fedora-ASUS-Zenbook-13/blob/main/README.md#4---réglages-des-navigateurs-opera--firefox)

5. [Réglages de l'UI Gnome Shell](https://github.com/Shogu/Configuration-Fedora-ASUS-Zenbook-13/blob/main/README.md#5---réglages-de-lui-gnome-shell)
   
6. [Allégement du système](https://github.com/Shogu/Configuration-Fedora-ASUS-Zenbook-13/blob/main/README.md#6---allégement-du-système)

7. [Optimisation du système](https://github.com/Shogu/Configuration-Fedora-ASUS-Zenbook-13/blob/main/README.md#7---optimisation-du-système)

8. [Maintenance de la distribution](https://github.com/Shogu/Configuration-Fedora-ASUS-Zenbook-13?tab=readme-ov-file#7---optimisation-du-système)

   
   

## **1 - Installation**

* a - Désactiver `Secure Boot` dans le Bios (F2)

* b - Désactiver la caméra dans le bios

* c - Graver l'iso `Fedora-Everything-netinst`

* d - Utiliser `systemd-boot` plutot que Grub : passer l'argument suivant dans le kernel de 
      l'iso  d'installation (en pressant Espace au boot) juste avant QUIET
  
  ```
  inst.sdboot
  ```






## **2 - Réglages de base**

* a - Télécharger le fichier `README.MD` et l'ouvrir avec `Marker` pour faciliter la suite des 
      instructions : penser à régler l'UI de Marker avec les options `cobalt`, `screen_light` 
      et `mode sombre` :
  
  ```
  flatpak install flathub com.github.fabiocolacio.marker
  ```

* b - Régler le système avec Paramètres (penser à désactiver les animations dans Accessibilité) puis Ajustements :
  
  ```
  sudo dnf install gnome-tweaks
  ```

* c - Régler Nautilus & créer un marque-page pour `Dropbox` & pour l'accès `ftp` au disque SSD sur la TV Android :
  
  ```
  192.168.31.68:2121
  ```

* d - Supprimer le mot de passe au démarrage avec le logiciel puis penser à reconnecter le compte Google dans Gnome :

  ```
  rm -v ~/.local/share/keyrings/*.keyring && reboot
  ```
  
* e - Installer le plugin dnf `snapper` avant d'utiliser dnf et s'assurer que le plugin installe bien la dépendance snapper :
  
  ```
  sudo dnf install  dnf-plugins-core dnf-plugin-snapper
  ```
  
     puis l'activer avec :
  
  ```
  snapper create-config / 
  ```

     Compléter avec l'installation du logiciel de sauvegarde BTRFS-Assistant :

  ```
  sudo dnf install btrfs-assistant
  ```





## **3 - Remplacement et installation de logiciels et codecs**

* a - Ajouter les sources `RPMFusion` :
  
     RPMFusion Free
  ```
  sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E%fedora).noarch.rpm 
  ```

     RMPFusion Non free
  ```
  sudo dnf install https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
  ```
    

* c - Ajouter les codecs `FFMPEG` & `AV1` :

  ```
  sudo dnf swap ffmpeg-free ffmpeg --allowerasing && dnf install gstreamer1-plugins-bad-free-extras
  ```
TEST ogu@fedora-ogu:~$ sudo dnf swap ffmpeg-free ffmpeg --allowerasing 
Mise à jour et chargement des dépôts :
Dépôts chargés.
Paquet                                                     Architecture       Version                                                    Dépôt                             Taille
Suppression de :
 ffmpeg-free                                               x86_64             7.0.2-7.fc41                                               fedora                           2.5 MiB
Suppression des paquets dépendants :
 libavcodec-free                                           x86_64             7.0.2-7.fc41                                               fedora                           9.5 MiB
 libavdevice-free                                          x86_64             7.0.2-7.fc41                                               fedora                         215.2 KiB
 libavfilter-free                                          x86_64             7.0.2-7.fc41                                               fedora                           4.1 MiB
 libavformat-free                                          x86_64             7.0.2-7.fc41                                               fedora                           2.6 MiB
 libavutil-free                                            x86_64             7.0.2-7.fc41                                               fedora                         950.7 KiB
 libpostproc-free                                          x86_64             7.0.2-7.fc41                                               fedora                          89.7 KiB
 libswresample-free                                        x86_64             7.0.2-7.fc41                                               fedora                         147.4 KiB
 libswscale-free                                           x86_64             7.0.2-7.fc41                                               fedora                         587.3 KiB
Installation de :
 ffmpeg                                                    x86_64             7.0.2-4.fc41                                               rpmfusion-free                   2.5 MiB
Installation des dépendances :
 ffmpeg-libs                                               x86_64             7.0.2-4.fc41                                               rpmfusion-free                  21.0 MiB
 libavdevice                                               x86_64             7.0.2-4.fc41                                               rpmfusion-free                 162.1 KiB
 x264-libs                                                 x86_64             0.164-15.20231001git31e19f92.fc41                          rpmfusion-free                   2.8 MiB
 x265-libs                                                 x86_64             3.6-3.fc41                                                 rpmfusion-free                  16.4 MiB
Installation des dépendances faibles :
 vmaf-models   

* d - Ajouter le `pilote Intel` d'accélération matérielle :

  ```
  sudo dnf install intel-media-driver
  ```

  
* e - Installer les logiciels Flatpak suivants : nota : utiliser prioritairement les flatpaks 
      Fedora OU Flathub car les runtimes ne sont pas partagés entre les 2.

  ```
  flatpak install flathub com.mattjakeman.ExtensionManager io.github.giantpinkrobots.flatsweep net.nokyan.Resources 
  com.github.fabiocolacio.marker org.jdownloader.JDownloader  org.onlyoffice.desktopeditors de.haeckerfelix.Fragments -y
  ```

    
* f - Installer les logiciels suivants avec dnf :

  ```
  sudo dnf install htop dconf-editor bleachbit ufw gnome-tweaks nicotine+ powertop loupe zstd gnome-network-displays ffmpegthumbnailer.x86_64 file-roller profile-cleaner celluloid -y
  ```

  
* g - Installer [Opera en rpm](https://www.opera.com/download/get/?partner=www&opsys=Linux&package=RPM)

* h - Installer [Dropbox](https://www.dropbox.com/fr/install-linux)





   
## **4 - Réglages des navigateurs Opera & Firefox**

* a -Passer Opera en navigateur par défaut dans Gnome : !! à adapter à la version rpm!

  ```
  xdg-settings set default-web-browser com.opera.Opera.desktop
  ```

* b - Passer Opera en français : éditer le raccourci avec l'application :
  
  ```
  flatpak install flathub page.codeberg.libre_menu_editor.LibreMenuEditor
  ```
  puis éditer le chemin du raccourci avec  `Opera @@u --lang=fr %U @@`
  

* c - Editer le raccourci Opera :
      -pour ouvrir un onglet fermé avec `ctrl-q`
      -`ctrl-s` pour `Sélectionner l'onglet actif précédent`
      -`ctrl-<` pour `Ouvrir ChatGPT dans la barre latérale`

* d - Passer Opera sur `wayland` APRES avoir fait un snap (possible problème de flou) avec le flag `chrome://flags/#ozone-platform-hint` puis activer l'autoclose de xwayland (voir plus bas).
  
* e - Créer les `tuiles` dans la page d'accueil

* f - Extensions Opera :

   1 - [LocalCDN](https://chromewebstore.google.com/detail/localcdn/njdfdhgcmkocbgbhcioffdbicglldapd)

   2 - [Bypass Paywalls](https://github.com/bpc-clone/bpc_updates/releases/tag/latest) (via le 
   fichier crx en mode développeur)

   3 - [I don't care about cookies](https://addons.opera.com/extensions/download/i-dont-care-about-cookies/)
  
   4 - [Raindrop](https://raindrop.io/r/extension/chrome)
  
   5 - [uBlock Origin](https://addons.opera.com/fr/extensions/details/ublock/) Penser à désactiver le bloqueur de pub natif d'Opera qui est bien moins performant, puis régler l'extension avec les filtres. Envisager le mode [MEDIUM](https://github.com/gorhill/uBlock/wiki/Blocking-mode:-medium-mode) même s'il complique souvent la navigation : chercher un ensemble de règles comme [celui-ci](https://raw.githubusercontent.com/Yuki2718/adblock2/main/medium_mode/dynamic-rules.txt) et les copier dans `Mon filtrage dynamique`, `règles temporaires` : enregistrer puis `appliquer` pour en faire des règles permanentes.
ATTENTION cela désactive ChatGPT dans la sidebar! 
  
   6 - [Cleaner Pro](https://addons.opera.com/fr/extensions/details/cleaner-pro-clear-cache-history/)
  
   7 - [Disable HTML5](https://chromewebstore.google.com/detail/disable-html5-autoplay-re/cafckninonjkogajnihihlnnimmkndgf) et activer le preloading dans les options.
  
   8 - [h264ify](https://addons.opera.com/fr/extensions/details/h264ify/)

   9 - [Simple Notepad](https://chromewebstore.google.com/detail/simple-notepad/ghnkdbkeniegahdcjeeikjoaapakeomf)
  
    ou remplacer Disable HTML5 & h264ify par 10 - [Enhancer for Youtube](https://chromewebstore.google.com/detail/enhancer-for-youtube/ponfpcnoihfmfllpaingbgckeeldkhle?hl=fr) qui intègre leurs fonctions. Le configurer d'un coup en rentrant le code du fichier `youtube_enhancer_conf`
  

* g - Codecs vidéos [libffmpeg](https://onedrive.live.com/?authkey=%21AC7ddalBsUiWsUE&id=75D48EF8D3750510%21234&cid=75D48EF8D3750510) pour Opera : à 
      coller en root dans le dossier suivant si les vidéos en ligne ne marchent pas :

```
à éditer pour la version rpm!
```
   
* h - Désactiver les options inutiles et `Faire defiler les onglets dans l'ordre d'utilisation`
  
* i - Dans `about:flags`, modifier les options suivantes :
  
  1 - Sidebar : `opera://flags/#sidebar-site-panel`

  2 - Pinboard : `chrome://flags/#pinboard`
  
  3 - Emoji tab : `chrome://flags/#tab-art`
  
  4 - UI refresh 2023 : `chrome://flags/#chrome-webui-refresh-2023`
  
  5 - Devtools : `chrome://flags/#devtools-tab-target`
  
  6 - Sync banner : `chrome://flags/#startpage-sync-banner`
  
  7 - Check d'extension : `chrome://flags/#safety-check-extension`
  
  8 - Wallet : `chrome://flags/#wallet-selector` & `chrome://flags/#native-crypto-wallet`
  
  9 - Autofill : `opera://flags/#show-autofill-type-predictions`
  
  10 - Caption : `chrome://flags/#enable-live-caption-multilang` & `chrome://flags/#enable- 
  accessibility-live-caption`
  
  11 - Profile Badging : `chrome://flags/#enable-enterprise-profile-badging`
  
  12 - Support tool : `chrome://flags/#support-tool`
  
  13 - Reading mode Screen2x : `chrome://flags/#read-anything-with-screen2x`
  
  14 - GPU Rasterization : `chrome://flags/#enable-gpu-rasterization` & `chrome://flags/#ui-enable-shared-image-cache-for-gpu` & `chrome://flags/#canvas-oop-rasterization`
  
  15 - Memory Saver : `opera://flags/#memory-saver` & `chrome://flags/#memory-saver-multi-state-mode` puis activer les options.
  
  16 - Split Screen : `opera://flags/#split-screen`
  
  17 - Disable accessibility : `chrome://flags/#enable-auto-disable-accessibility`
  
  18 - Scrollbar old school : `chrome://flags/#component-based-scrollbar`
  
  19 - Drag des groupes & onglets : `chrome://flags/#drag-multiple-tabs`
  
  20 - Scroll dans la barre d'onglets : `chrome://flags/#scrollable-tab-strip`
  
  21 - Dark thème pour les sites : `opera://flags/#enable-force-dark-from-settings`
  
  22 - Activer le protocole QUIC : `opera://flags/#enable-quic`
  
  23 - Parallel Downloading : `opera://flags/#enable-parallel-downloading`

  24 - Oop video decoding : `opera://flags/#use-out-of-process-video-decoding`

  25 - Update au lancement : `chrome://flags/#sync-poll-immediately-on-every-startup` à désactiver (vérifier si la 
       synchronisation se fait quand même)

  26 - Tab Cycler (à désactiver) : `opera://flags/#component-based-tab-cycler`


* j - Créer dans la barre latérale d'Opera les sites internet suivants APRES s'être connecté à 
      Google :
  
     [Google Translate](translate.google.com)
  
     [Gmail](https://mail.google.com/mail/u/0/?pli=1#inbox)
  
     [Keep](keep.google.com)
  
     [Raindrop](https://app.raindrop.io/my/0)
  
     [Play Livres pour le mode tablette](https://play.google.com/store/books?hl=fr)


* k - Extensions pour Firefox :

     [uBlock Origin](https://addons.mozilla.org/fr/firefox/addon/ublock-origin/)
  
     [Autotab Discard](https://addons.mozilla.org/fr/firefox/addon/auto-tab-discard/)

     [Raindrop](https://raindrop.io/r/extension/firefox) et supprimer `Pocket` de Firefox avec `extensions.pocket.enabled` dans `about:config` puis supprimer le raccourci dans la barre.
  
     [Keep Notes](https://addons.mozilla.org/fr/firefox/addon/google-keep-notes/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search)

     [I Dont' Care About Cookies](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiH4djZpPWGAxVnVaQEHVC4Ah4QFnoECBwQAQ&url=https%3A%2F%2Faddons.mozilla.org%2Ffr%2Ffirefox%2Faddon%2Fi-dont-care-about-cookies%2F&usg=AOvVaw1V3SeotV2aYuif7_jcLW43&opi=89978449)
  
     [Clear Browsing Data](https://addons.mozilla.org/fr/firefox/addon/clear-browsing-data/)
  
     [Undo Close Tab Button](https://addons.mozilla.org/firefox/addon/undoclosetabbutton)

     [LocalCDN](https://addons.mozilla.org/fr/firefox/addon/localcdn-fork-of-decentraleyes/)


* l - Activer ``openh264`` dans les plugins firefox.

* m - Réduire l'intervalle de sauvegarde des sessions Firefox en la passant à `600000` avec 
      `about:config`:

```
browser.sessionstore.interval
```





## **5 - Réglages de l'UI Gnome Shell**

* a - Changer le [wallpaper](https://github.com/CubeJ/LinuxWallpaper)

* b - Régler HiDPI sur 200, cacher les dossiers Modèles, Bureau, ainsi que le wallaper et l'image user, augmenter la 
      taille des icones dossiers.

* c - Installer diverses extensions :
  
    1 - [Appindicator](https://extensions.gnome.org/extension/615/appindicator-support/)

    2 - [Tiling Shell](https://extensions.gnome.org/extension/7065/tiling-shell/) puis la désactiver (voir script d'activation plus bas)

    3 - [Alphabetical Grid](https://extensions.gnome.org/extension/4269/alphabetical-app-grid/) puis la supprimer : l'ordre alphabetique persistera.

    4 - [Mute/unmute](https://extensions.gnome.org/extension/5088/muteunmute/)

    5 - [Screen Rotate](https://extensions.gnome.org/extension/5389/screen-rotate/)) puis la désactiver (voir script d'activation plus bas)
  
    6 - [AutoActivities](https://extensions.gnome.org/extension/5500/auto-activities/)
  
    7 - [Battery Time](https://extensions.gnome.org/extension/5425/battery-time/)
    
    8 - [Caffeine](https://extensions.gnome.org/extension/517/caffeine/)
  
    9 - [Clipboard History](https://extensions.gnome.org/extension/4839/clipboard-history/)
  
    10 - [Frequency Boost Switch](https://extensions.gnome.org/extension/4792/frequency-boost-switch/)
  
    11 - [Quick Settings Extension](https://extensions.gnome.org/extension/5446/quick-settings-tweaker/)
  
    12 - [Hot Edge](https://extensions.gnome.org/extension/4222/hot-edge/)
  
    13 - [Impatience](https://extensions.gnome.org/extension/277/impatience/)
  
    14 - [NoAnnoyance](https://extensions.gnome.org/extension/6109/noannoyance-fork/)

    15 - [Custom Command Toggle](https://extensions.gnome.org/extension/7012/custom-command-toggle/)
  
    16 - [Power Profile Indicator](https://extensions.gnome.org/extension/6679/power-profile-indicator/)
  
    17 - [Privacy Quick Settings](https://extensions.gnome.org/extension/4491/privacy-settings-menu/) puis la 
         supprimer une fois les réglages réalisés.


* d - Installer [Nautilus-admin](https://download.copr.fedorainfracloud.org/results/tomaszgasior/mushrooms/fedora-38-x86_64/06214967-nautilus-admin/) puis lancer la commande ```nautilus -q``` pour relancer Fichiers

* e - Raccourcis à éditer dans Gnome : mettre ```x-terminal-emulator``` à la place de la touche Exposant, et la 
      commande ```flatpak run net.nokyan.Resources``` pour la combinaison ```ctrl-alt-supp```.

* f - Passer Gnome-text-editor en `theme LIGHT`, puis  régler gnome-terminal (police, raccourci copier-coller, 
      curseur, et surtout `palette prédéfinie=Gnome Clair` & `Désactiver la barre de défilement`.


* g - Supprimer le décompte de 60 secondes lors de l'extinction du PC et désactiver dans Settings l'extinction par le 
      bouton Power :
  
```
gsettings set org.gnome.SessionManager logout-prompt false
```
  
* h - Changer les polices d'écriture pour `Noto Sans` en 11 ?
  
* i - Améliorer  Celluloid :
    - inscrire `hwdec=auto-safe` dans Paramètres --> Divers --> Options supplémentaires
    - installer les deux scripts lua suivants pour la musique :
      [Visualizer](https://www.dropbox.com/scl/fi/bbwlvfhtjnu8sgr4yoai9/visualizer.lua?rlkey=gr3bmjnrlexj7onqrxzjqxafl&dl=0)
      [Delete File avec traduction française](https://www.dropbox.com/scl/fi/c2cacmw2a815husriuvc1/delete_file.lua?rlkey=6b9d352xtvybu685ujx5mpv7v&dl=0)
      - activer l'option `focus` et `toujours afficher les boutons de titre`
  
* j - Améliorer l'autocomplétion du terminal en téléchargeant le fichier`.inputrc` et le palcer dans `~/`, puis 
      changer les polices au profit de `Noto Sans 12` ou `Monospace 11`
  

* k - Modifier le thème de `Jdownloader` avec ce dépôt [Github](https://calendar.google.com/calendar/u/0/r?pli=1) : 
      (attention, les polices et sont trop grosses et rendent la lecture trop difficile, ou alors avec les icons 
      `flat` et le thème `Black Star` puis supprimer les bannières, menus & colonnes inutiles.


* l - Télécharger le script de `transfert des vidéos` intitulé `.transfert_videos` pour déplacer automatiquement les 
      vidéos vers Vidéos en supprimant le sous-dossier d'origine : en faire un raccourci avec l'éditeur de menu et 
      lui mettre l'icone `/usr/share/icons/Adwaita/scalable/devices/drive-multidisk.svg`


  
* m - Télécharger le script de `bascule Bluetooth` `.bluetooth_toggle` pour activer/désactiver le service bluetooth à 
      la volée : en faire un raccourci avec l'éditeur de menu et mettre l'icone 
      `/usr/share/icons/Adwaita/scalable/devices/phone.svg`.





               ******** Rajouter des toggles au menu de Gnome-Shell ********
  
![](https://i.postimg.cc/FR3wnnV6/Capture-d-cran-du-2024-06-24-19-25-39.png) 
![](https://i.postimg.cc/L5SGdBy8/Capture-d-cran-du-2024-06-24-19-26-15.png) 



  
* n - Télécharger le script `.activer_tiling.sh` pour activer/désactiver l'extension de `Tiling`, puis rendre le script exécutable et créer  le toggle avec Custom 
      Command Toggle :
  ![Toggle Tiling](https://i.ibb.co/CMsJQpK/Capture-d-cran-du-2024-06-19-14-32-27.png)


* o - Créer le `Mode Tablette` (à compléter avec les logiciels Wike, Librum, et un raccourci Google Play Livres) : créer un toggle Gnome-shell qui lance le script 
      `.tablette.sh` qui va activer l'extension  Screen-rotate (qu'il faut régler en rajoutant l'option Manual) et le clavier virtuel, ou les désactiver s'ils 
      sont en fonction, et lui attribuer le raccourci `pda-symbolic`.
     
    
* p - Créer un toggle `Powertop` qui va lancer powertop en `auto-tune` pour économiser encore plus de batterie, et baisser la luminosité sur 5% : rentrer cette 
      commande pour le toggle activé :
  
  ```
  pkexec powertop --auto-tune && gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness " <int32 5>"()
  ```
  
     Et cette commande pour le toggle désactivé :
      
  ```
  gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path /org/gnome/SettingsDaemon/Power --method 
  org.freedesktop.DBus.Properties.Set org.gnome.SettingsDaemon.Power.Screen Brightness " 
  <int32 2O>"()
  ```
     Enfin rentrer le nom de l'icone : `thunderbolt-symbolic` 

 
* q - Créer un toggle `luminosité` pour passer à 70 ou 20% :  attribuer l'icone `view-reveal-symbolic` puis passer les arguments suivants :
  
  ```
  gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path 
  /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set 
  org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 70>"()

  gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path 
  /org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set 
  org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 20>"()
  ```

  * l - Créer un toggle "No Touchscreen" :
    
    ```
    echo 'i2c-ELAN9008:00' | pkexec tee /sys/bus/i2c/drivers/i2c_hid_acpi/unbind > /dev/null
    ```
    ```
    echo 'i2c-ELAN9008:00' | pkexec tee /sys/bus/i2c/drivers/i2c_hid_acpi/bind > /dev/null                         
    ```


## **6 - Allégement du système**

* a - Supprimer les logiciels inutiles avec Gnome-software
    
   

* d - Supprimer les logiciels suivants avec le terminal :
  
  ```
  sudo dnf autoremove speech-dispatcher mdadm lvm2 mdadm lvm2 sssd firewalld ibus-libzhuyin 
  ibus-libpinyin ibus-typing-booster ibus-m17n ibus-hangul ibus-anthy yelp abrt brltty 
  podman openvpn gnome-weather rygel totem virtualbox* avahi-tools -y
  ```

  
* e - Supprimer les flatpaks KDE :
  
  ```
  flatpak remove org.kde.KStyle.Adwaita org.kde.PlatformTheme.QGnomePlatform     
  org.kde.WaylandDecoration.QAdwaitaDecorations QGnomePlatform-decoration  
  org.kde.WaylandDecoration.QGnomePlatform-decoration   org.kde.Platform 
  ```

  
* f - Supprimer et masquer les services inutiles :
  
  ```
  sudo systemctl mask NetworkManager-wait-online.service auditd.service ModemManager.service avahi-daemon.service plymouth-quit-wait.service switcheroo-control.service sys-kernel-tracing.mount sys-kernel-debug.mount httpd.service   mdmonitor.service mdmonitor.service raid-check.timer sssd-kcm.service pcscd raid-check.timer fwupd avahi-daemon.socket sssd-kcm.socket pcscd.socket

  ```
  
     et désactiver le Bluetooth pour l' activer à la volée (voir script dans la rubrique UI Gnome) + cups :
  
  ```
  sudo systemctl disable bluetooth.service cups
  ```
  

     Enfin, reboot puis controle de l'état des services avec :
  
  ```
  systemd-analyze blame | grep -v '\.device$'
  ```

     et :

```
systemctl list-unit-files --type=service --state=enabled
```
  

  ```
  

* h - Alléger les journaux système et les mettre en RAM :
  
  ```
  sudo gnome-text-editor /etc/systemd/journald.conf
  ```
  
     puis remplacer le contenu du fichier par celui du fichier `journald.conf.txt` & relancer le service :
  
  ```
  sudo systemctl restart systemd-journald
  ```
  
* j - Supprimer les `coredump` en éditant systemd :
  
  ``` 
  sudo gnome-text-editor /etc/systemd/coredump.conf.d/
  ```
     Editer le fichier comme suit :
  
  ```
  [Coredump]
  Storage=none
  ProcessSizeMax=0
  ```
     et supprimer le service dans le noyau ```kernel```  avec la commande :

  ```
  sudo ln -sf /dev/null /usr/lib/sysctl.d/50-coredump.conf
   
  ```
     puis

  ```
  sudo gnome-text-editor /etc/sysctl.d/50-coredump.conf
  ```
     et y inscrire :

  ```
  kernel.core_pattern=|/bin/false
  ```
  
     Enfin configurer `ulimit` pour désactiver les core dumps au niveau utilisateur :
  
  ```
  sudo gnome-text-editor /etc/security/limits.conf
  ```
     puis coller : `* hard core 0`

* k - Supprimer le `watchdog` et blacklister les pilotes inutiles `Nouveau` & `ELAN:Fingerprint` : éditer le fichier 
      suivant :
  
  ```
  sudo gnome-text-editor /etc/sysctl.conf
  ```
     et ajouter :
  
  ```
  kernel.nmi_watchdog=0
  ```
     Puis créer un fichier `blacklist` ```sudo gnome-text-editor /etc/modprobe.d/blacklist.conf``` et l'éditer :
  
  ```
  blacklist iTCO_vendor_support
  blacklist wdat_wdt
  blacklist intel_pmc_bxt
  blacklist nouveau
  blacklist ELAN:Fingerprint
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


  
* m - Faire le tri dans `~/.local/share/`, `/home/ogu/.config/`, `/usr/share/` et `/etc/`




## **7 - Optimisation du système**


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
  
  ```sudo systemctl enable ufw```
  ```sudo ufw logging off```
  ```sudo systemctl start ufw```
  ```sudo ufw default deny incoming```
  ```sudo ufw default allow outgoing```
  
     pour nicotine :
  ```sudo ufw allow in 2232/tcp```

     pour Fragments :
  ```sudo ufw allow in 51413/tcp```
  ```sudo ufw allow in 51413/udp```

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

  
* i - Accélérer `DNF` :
  
  ```
  echo 'max_parallel_downloads=20' | sudo tee -a /etc/dnf/dnf.conf

  ```
  
* j - Diviser le nombre de `ttys` au boot par deux :
  
  ```
  sudo gnome-text-editor /etc/systemd/logind.conf
  ```
     puis editer `NautoVTS=3`

* k - Vérifier que le système utilise bien les DNS du routeur Xiaomi (192.168.31.1) :

  ```
  nmcli dev show |grep DNS
  ```






## **8 - Maintenance de la distribution**


 * a -  Télécharger le script complet de mise à jour & nettoyage `.update_fedora.sh` dans `~/`
        NOTA : pensez à lancer Bleachbit en gui une première fois pour sélectionner les options.
   






Boot time : avant optimisation :

ogu@fedora-ogu:~$ systemd-analyze
Startup finished in 2.213s (firmware) + 500ms (loader) + 1.806s (kernel) + 3.901s (initrd) + 28.363s (userspace) = 36.786s
graphical.target reached after 28.330s in userspace.

Boot time après désactivation des services inutiles :
