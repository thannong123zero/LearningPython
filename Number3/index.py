import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()   
#---------------------------------------------------------------
# from ollama import chat
# from ollama import ChatResponse

# response: ChatResponse = chat(model='deepseek-r1', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# print(response['message']['content'])
# # or access fields directly from the response object
# print(response.message.content)
#---------------------------------------------------------------
# from ollama import chat

# stream = chat(
#     model='deepseek-r1',
#     messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
#     stream=True,
# )

# for chunk in stream:
#   print(chunk['message']['content'], end='', flush=True)