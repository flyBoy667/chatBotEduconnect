from whatsapp_chatbot_python import BaseStates, GreenAPIBot, Notification
from whatsapp_chatbot_python.filters import TEXT_TYPES
from whatsapp_api_client_python import API

ID_INSTANCE = "7103942142"
API_TOKEN = "b4a667fb16db46b1bcaa470b9c1119b71d04a9ea7ef44b4d87"

bot = GreenAPIBot(
    ID_INSTANCE, API_TOKEN
)

greenAPI = API.GreenAPI(
    ID_INSTANCE, API_TOKEN
)

API_BASE_URL = "http://127.0.0.1:8000/api/"
ALL_STUDENTS_ENDPOINT = "etudiants"