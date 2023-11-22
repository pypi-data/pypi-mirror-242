
import gradio as gr
from gradio_gptchatbot import GPTChatbot


example = [
    ("How do I create a Gradio app?",
    "You can create a Gradio app by...")
]

with gr.Blocks() as demo:
    with gr.Row():
        GPTChatbot(label="Blank", placeholder_title="GradioGPT", placeholder_image="https://i.ibb.co/H2kSY2R/Gradio-component-1.png"),  # blank component
        GPTChatbot(value=example, label="Populated", layout="panel"),  # populated component


demo.launch()
