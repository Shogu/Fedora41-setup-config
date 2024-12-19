#!/bin/bash
source ~/.bashrc

# Dossiers de source et de destination
SOURCE_DIR=~/Téléchargements
DEST_DIR=~/Vidéos

# Extensions de fichiers vidéo
VIDEO_EXTENSIONS=("*.mp4" "*.mkv" "*.avi" "*.mov" "*.flv" "*.wmv" "*.mpeg" "*.mpg" "*.webm")

# Fonction pour déplacer un fichier et supprimer son dossier s'il est vide
move_and_cleanup() {
    local file="$1"
    local dest="$2"
    local dir

    echo "Fichier trouvé: $file"
    read -p "Voulez-vous déplacer ce fichier vers $dest ? (o/n) " choice
    if [[ $choice == [oO] ]]; then
        # Créer le répertoire de destination s'il n'existe pas
        mkdir -p "$dest"
        # Déplacer le fichier vidéo
        mv "$file" "$dest"
        echo "Fichier déplacé vers $dest"
        # Supprimer le sous-dossier vide s'il n'y a plus de fichiers dedans
        dir=$(dirname "$file")
        while [ "$dir" != "$SOURCE_DIR" ]; do
            if [ -z "$(ls -A "$dir")" ]; then
                rmdir "$dir"
                echo "Sous-dossier supprimé: $dir"
                dir=$(dirname "$dir")
            else
                break
            fi
        done
    else
        echo "Fichier ignoré."
    fi
}

export -f move_and_cleanup
export DEST_DIR
export SOURCE_DIR

# Trouver et traiter les fichiers vidéo
for ext in "${VIDEO_EXTENSIONS[@]}"; do
    find "$SOURCE_DIR" -type f -name "$ext" -exec bash -c 'move_and_cleanup "$0" "$DEST_DIR"' {} \;
done

echo "Traitement terminé."

# Fermer automatiquement la fenêtre du terminal (solution portable)
if [[ $SHLVL -eq 1 ]]; then
    exit
fi


