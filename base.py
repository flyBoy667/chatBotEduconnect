import requests
from whatsapp_chatbot_python import GreenAPIBot, Notification, BaseStates
from whatsapp_chatbot_python.filters import TEXT_TYPES

from conf import bot, API_BASE_URL, ALL_STUDENTS_ENDPOINT

ID = "1"  # Correction de la déclaration globale


class States(BaseStates):
    START = "start"
    MAIN_MENU = "main_menu"
    SHOW_NOTES = "show_notes"
    SHOW_ANNONCE = "show_annonce"
    PAYMENT_STATUS = "payment_status"


@bot.router.message(text_message=['Bonjour', 'bonjour'])
def start_handler(notification: Notification) -> None:
    global ID  # Déclaration pour utiliser la variable globale
    sender = notification.sender
    sender_data = notification.event['senderData']
    sender_num = sender_data['sender']

    response = requests.get(f"{API_BASE_URL}{ALL_STUDENTS_ENDPOINT}")
    if response.status_code == 200:
        students_data = response.json()
        for student in students_data:
            # Conversion du num pour le chatbot
            valid_number = '223' + student['user']['telephone'] + '@c.us'

            if valid_number == sender_num:
                ID = student['id']
                student_name = student['user']['prenom'] + " " + student['user']['nom']
                notification.answer(f"Bienvenue *{student_name}*!")
                notification.answer("Que voulez-vous faire ? : \n"
                                    "1️⃣ - Voir mes  *notes*. \n"
                                    "2️⃣ - Voir mes  *annonces*. \n"
                                    "3️⃣ - Voir mon  *status de paiement*.")
                notification.state_manager.set_state(sender, States.MAIN_MENU.value)
                break
        else:
            notification.answer(f"Vous n'etes pas enregistre!")
            print()

    else:
        notification.answer("Erreur lors de la recherche des etudiants!")
        print(f"Erreur: La requête a retourné un code d'erreur {response.status_code}")


@bot.router.message(state=States.MAIN_MENU.value, type_message=TEXT_TYPES)
def menu_handler(notification: Notification) -> None:
    sender = notification.sender
    print(ID)
    STUDENT_ENDPOINT = f"etudiants/{ID}/infos"
    selected_option = notification.message_text
    response = requests.get(f"{API_BASE_URL}{STUDENT_ENDPOINT}")

    if response.status_code == 200:
        student_data = response.json()
        print(student_data)
        if selected_option == '1':
            print('yes')
            # for module in student_data['modules']:

        elif selected_option == '2':
            notification.answer("Voici vos annonces :")
            notification.answer("Annonce 1 : Participation à un concert")
            notification.answer("Annonce 2 : Rendez-vous à la bibliothèque")
        elif selected_option == '3':
            notification.answer("Voici votre statut de paiement :")
            notification.answer("Paiement effectué")
        else:
            notification.answer("Veuillez choisir une option valide!")
    else:
        notification.answer("Erreur lors de la recherche des etudiants!")
        print(f"Erreur: La requête a retourné un code d'erreur {response.status_code}")


bot.run_forever()
