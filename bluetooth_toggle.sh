#!/bin/bash
source ~/.bashrc

# Vérifier l'état actuel du service Bluetooth
SERVICE_STATUS=$(systemctl is-active bluetooth)

if [ "$SERVICE_STATUS" = "active" ]; then
    # Le service Bluetooth est en cours d'exécution, donc l'arrêter
    echo "Le service Bluetooth est actuellement actif. Arrêt du service..."
    sudo systemctl stop bluetooth
    if [ $? -eq 0 ]; then
        echo "Le service Bluetooth a été arrêté avec succès."
    else
        echo "Échec de l'arrêt du service Bluetooth."
    fi
else
    # Le service Bluetooth est arrêté, donc le démarrer
    echo "Le service Bluetooth est actuellement inactif. Démarrage du service..."
    sudo systemctl start bluetooth
    if [ $? -eq 0 ]; then
        echo "Le service Bluetooth a été démarré avec succès."
    else
        echo "Échec du démarrage du service Bluetooth."
    fi
fi

