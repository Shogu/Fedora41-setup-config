#!/usr/bin/env python3

import sys
import os
import subprocess
import webbrowser

def main():
    # Définir le chemin de base autorisé
    allowed_base_path = os.path.expanduser("~/Dropbox")

    if len(sys.argv) < 2:
        print("Aucun fichier sélectionné.")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        # Obtenir le chemin absolu
        file_path = os.path.abspath(file_path)

        # Vérifiez si le fichier existe
        if not os.path.exists(file_path):
            print(f"Le fichier {file_path} n'existe pas.")
            continue

        # Vérifier si le fichier est dans le dossier autorisé
        if not file_path.startswith(allowed_base_path):
            print(f"Le fichier {file_path} n'est pas dans le dossier autorisé ({allowed_base_path}).")
            continue

        print(f"Fichier trouvé : {file_path}")

        # Extraire le répertoire contenant le fichier
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)

        print(f"Répertoire du fichier : {file_dir}")
        print(f"Nom du fichier : {file_name}")

        # Utiliser Maestral CLI pour vérifier s'il existe déjà un lien partagé
        try:
            # Se déplacer dans le répertoire du fichier
            os.chdir(file_dir)
            print(f"Répertoire de travail changé vers : {file_dir}")

            # Vérifier s'il existe déjà un lien partagé
            result = subprocess.run(
                ["maestral", "sharelink", "list", file_name],
                capture_output=True,
                text=True
            )

            if result.returncode == 0 and result.stdout.strip():
                # Si un lien existe déjà, ouvrir ce lien
                dropbox_url = result.stdout.strip().splitlines()[0]  # Récupérer le premier lien
                print(f"Lien existant trouvé : {dropbox_url}")
                webbrowser.open(dropbox_url)
            else:
                # Si aucun lien n'existe, créer un nouveau lien
                print("Aucun lien existant, création d'un nouveau lien...")
                create_result = subprocess.run(
                    ["maestral", "sharelink", "create", file_name],
                    capture_output=True,
                    text=True
                )

                if create_result.returncode == 0:
                    dropbox_url = create_result.stdout.strip()
                    print(f"Nouveau lien généré : {dropbox_url}")
                    webbrowser.open(dropbox_url)
                else:
                    print(f"Erreur lors de la génération du lien : {create_result.stderr}")

        except FileNotFoundError:
            print("Maestral CLI n'est pas installé ou configuré.")
            sys.exit(1)

if __name__ == "__main__":
    main()

