

# 🧳 Travel Bot – Rasa Chatbot

This is a travel assistant chatbot built with **Rasa**. It helps users plan trips by collecting travel details, offering weather information, and responding to FAQs.

---

## 📁 Project Structure

Travel_bot/
├── actions/ # Custom action files (Python)
├── data/ # NLU, stories, rules
├── models/ # Trained model files
├── config.yml # Pipeline and policies
├── domain.yml # Intents, entities, responses, slots
├── endpoints.yml # Action server configuration
├── credentials.yml # Rasa channels
├── requirements.txt # Python dependencies
├── Dockerfile # For deployment
└── README.md # This file

yaml
Copy
Edit

---

## ⚙️ Local Setup

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Train the model
bash
Copy
Edit
rasa train
4. Run the Rasa server
bash
Copy
Edit
rasa run --enable-api --cors "*" --port 5001
5. Run the action server
bash
Copy
Edit
rasa run actions
