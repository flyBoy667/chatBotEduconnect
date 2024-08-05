from whatsapp_chatbot_python import BaseStates, GreenAPIBot, Notification
from whatsapp_chatbot_python.filters import TEXT_TYPES
from whatsapp_api_client_python import API
import requests
from PIL import Image
from io import BytesIO

ID_INSTANCE = "7103900959"
API_TOKEN = "cee70882caea421a9d81f5af79dcba69595225f92e114eb6a2"

bot = GreenAPIBot(
    ID_INSTANCE, API_TOKEN
)

greenAPI = API.GreenAPI(
    ID_INSTANCE, API_TOKEN
)

API_BASE_URL = "http://127.0.0.1:8000/api/"
ALL_STUDENTS_ENDPOINT = "etudiants"


def file_sender(sender_num, file_path, file_name, legend):
    response = greenAPI.sending.sendFileByUpload(
        sender_num,
        file_path,
        file_name,
        legend
    )

    print(response.data)


def retrieve_annonce_images(annonces):
    for annonce in annonces:
        if annonce['image']:
            # Charger l'image à partir des données binaires
            image = Image.open(BytesIO(annonce['image']))

            # Vérifier le mode de l'image
            if image.mode != 'RGB':
                # Convertir l'image en mode RGB si nécessaire
                rgb_image = image.convert('RGB')
            else:
                rgb_image = image  # L'image est déjà en mode RGB

            # Construire le nom de fichier pour sauvegarder l'image
            image_filename = f"{annonce['titre']}.jpeg"

            # Sauvegarder l'image localement en tant que JPEG
            rgb_image.save(image_filename, 'JPEG')

            print(f"Image saved as {image_filename}")
            annonce["image_path"] = image_filename
        else:
            print(f"Pas d'image pour cette annonce")
            return None
    return annonces
