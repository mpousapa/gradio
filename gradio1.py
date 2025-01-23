import gradio as gr
import requests
import random

items = None
item_actual = None

def load_data():
    global items

    capcalera = {"Content-Type": "application/json"}
    api_url = "https://zelda.fanapis.com/api/items"

    try: 
        resposta = requests.get(url = api_url, headers=capcalera)

        if resposta.status_code == 200:
            dades_json = resposta.json()
            items = dades_json["data"]
        else:
            print("No s'han trobat resultats a la crida.")
    
    except Exception as exc:
        print(f"Error al obtenir les dades de la api: {exc}")

def obtenir_item_random():
    global items

    if items is None:
        return None
    
    index = random.randint(0, len(items))
    return items[index]

def show_question(message, history):
    global items
    global item_actual

    missatge = ""

    # Comprovem les dades que tenim i actuem en conseqüència
    if items is None:
        return "Something went wrong... The items are not loaded."
    
    # Si no és el primer missatge
    if item_actual is not None:
        missatge = "Good answer! Let's go for another one: " if item_actual["name"] == message else f"You failed... the response was '{item_actual["name"]}'. Try once again: "
    
    # Si és el primer missatge (per tant no hi ha possible resposta)
    if item_actual is None:
        missatge = "Well, let's start. You only have to answer the name of the item in Zelda games based on its description: "
    
    # Obtenim el següent item a avaluar
    item_actual = obtenir_item_random()

    missatge += item_actual["description"]
    return missatge

load_data() # Carreguem les dades

gr.ChatInterface(
    show_question,
    type="messages",
    textbox=gr.Textbox(placeholder="Let's answer some Zelda questions...", scale=7),
).launch()