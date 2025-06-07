

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


### 5. Run the action server

rasa run actions

## Result

![Screenshot 2025-06-07 125958](https://github.com/user-attachments/assets/5d951620-02fa-46be-87b3-3cc59f980eff)



![Screenshot 2025-06-07 124431](https://github.com/user-attachments/assets/75b7a116-4bda-4449-b6e7-2fa6e6ac64fa)


