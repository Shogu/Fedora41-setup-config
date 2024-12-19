#!/usr/bin/env python3
import os
import sys

def hide_invisible(files):
    for file in files:
        # Vérifier si le fichier existe
        if os.path.exists(file):
            dirname, filename = os.path.split(file)
            new_name = os.path.join(dirname, '.' + filename)
            os.rename(file, new_name)
        else:
            print(f"Erreur : le fichier ou dossier '{file}' n'existe pas.")

def main():
    # Récupérer les fichiers/dossiers sélectionnés
    files = sys.argv[1:]

    if not files:
        print("Aucun fichier ou dossier sélectionné.")
        return

    hide_invisible(files)

if __name__ == "__main__":
    main()

