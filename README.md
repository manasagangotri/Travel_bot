

# 🧳 Travel Bot – Rasa Chatbot

This is a travel assistant chatbot built with **Rasa**. It helps users plan trips by collecting travel details, offering weather information, and responding to FAQs.


## ⚙️ Local Setup

### 1. Create a virtual environment

python -m venv venv

source venv/bin/activate  # or venv\Scripts\activate on Windows

### 2. Install dependencies

pip install -r requirements.txt

### 3. Train the model

rasa train

### 4. Run the Rasa server

rasa run --enable-api --cors "*" --port 5001


5. Run the action server

rasa run actions
