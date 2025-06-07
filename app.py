import gradio as gr
import requests

# Replace with your deployed Rasa backend URL
#RASA_BACKEND = "https://travelbot-production-3749.up.railway.app/webhooks/rest/webhook"

RASA_BACKEND = "http://localhost:5005/webhooks/rest/webhook"

def chat_with_rasa(message, chat_history):
    status = "Sending message..."
    try:
        # Prepare the payload
        payload = {
            "sender": "user",
            "message": message
        }

        # Send message to Rasa
        response = requests.post(RASA_BACKEND, json=payload)
        response.raise_for_status()  # raise error for non-200 responses
        responses = response.json()

        # Extract bot replies
        bot_messages = [r.get("text") for r in responses if "text" in r]

        # Update chat history
        for bot_msg in bot_messages:
            chat_history.append((message, bot_msg))
            message = ""  # clear input

        status = "Bot replied ✅" if bot_messages else "No response from bot 🤖"

    except requests.exceptions.RequestException as e:
        status = f"❌ Error: {e}"

    return chat_history, "", status


with gr.Blocks() as demo:
    gr.Markdown("### 🤖 Travel Assistant Chatbot")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(show_label=False, placeholder="Type your message here...")
    status = gr.Label()
    state = gr.State([])

    msg.submit(chat_with_rasa, inputs=[msg, state], outputs=[chatbot, msg, status])

demo.launch(share=True)  # share=True to get public link
