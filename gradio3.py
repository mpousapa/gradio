import gradio as gr
from transformers import pipeline

es = "Espanyol"
en = "Anglès"

estil_idioma = "### "

idioma_entrada = estil_idioma + es
idioma_sortida = estil_idioma + en

model_entrada_es = "Helsinki-NLP/opus-mt-es-en"
model_entrada_en = "Helsinki-NLP/opus-mt-en-es"

credencials = [("iabd", "iabd")]


def intercanvia():
    global idioma_entrada
    global idioma_sortida

    temp = idioma_entrada

    idioma_entrada = idioma_sortida
    idioma_sortida = temp

    return idioma_entrada, idioma_sortida

def tradueix(input):
    global idioma_entrada
    global model_entrada_es
    global model_entrada_en

    model_a_usar = model_entrada_es if es in idioma_entrada else model_entrada_en

    pipe = pipeline("translation", model = model_a_usar)
    frase_es = pipe(input)

    return frase_es[0]["translation_text"]

with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("# Escull l'idioma per a traduir")

    with gr.Row():
        # Mostrar
        idioma1 = gr.Markdown(idioma_entrada)
        btn_intercanvia = gr.Button("Intercanvia idiomes")
        idioma2 = gr.Markdown(idioma_sortida)
        btn_intercanvia.click(fn=intercanvia, outputs=[idioma1, idioma2])

    with gr.Row():
        input_text = gr.Textbox(label="Text a traduir")
        output_text = gr.Textbox(label="Traducció")
    
    btn_tradueix = gr.Button("Tradueix")
    btn_tradueix.click(fn=tradueix, inputs=[input_text], outputs=[output_text])

demo.launch(auth = credencials)