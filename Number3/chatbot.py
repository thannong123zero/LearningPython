import gradio as gr
from ollama import chat

def deepSeek(content):
    stream = chat(
        model='deepseek-r1',
        messages=[{'role': 'user', 'content': content}],
        stream=True
    )
    
    response = ""
    for chunk in stream:
        response += chunk['message']['content']
    
    return response

def chat_logic(massage, response):
    bot_response = deepSeek(massage)
    response.append([massage, bot_response])

    return "",response

with gr.Blocks() as chatbot:
    gr.Markdown("## Chatbot")
    massage = gr.Textbox(label="Enter your message")
    response = gr.Chatbot(label="Response")

    massage.submit(chat_logic,inputs=[massage, response], outputs=[massage,response])

chatbot.launch()
