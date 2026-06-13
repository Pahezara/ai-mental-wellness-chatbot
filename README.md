\# 🧠 AI-Powered Bilingual Mental Wellness Chatbot



A bilingual AI mental wellness platform supporting Sinhala and English users through emotion recognition, risk assessment, and a fine-tuned Qwen2.5 language model.



\---



\## 📖 Overview



The Mental Wellness Chatbot is an AI-powered support system designed to provide empathetic conversations for users experiencing emotional distress. The system combines machine learning, natural language processing, translation services, and a fine-tuned large language model to deliver safe and context-aware responses.



\---



\## ✨ Key Features



\- \*\*Bilingual Conversations\*\* – Sinhala and English support.

\- \*\*Automatic Language Detection\*\* – Detects user language automatically.

\- \*\*Emotion Recognition\*\* – Identifies emotional states using NLP models.

\- \*\*Risk Assessment\*\* – Detects potential crisis situations.

\- \*\*AI Response Generation\*\* – Powered by a fine-tuned Qwen2.5 model.

\- \*\*Google Translation Integration\*\* – Accurate Sinhala ↔ English translation.

\- \*\*Session Management\*\* – Maintains conversation history.

\- \*\*Privacy-Aware Design\*\* – Optional user text storage.



\---



\## 🏗️ System Architecture



User

↓

React Frontend

↓

FastAPI Backend

↓

Translation Layer

↓

Emotion Detection

↓

Risk Assessment

↓

Fine-Tuned Qwen2.5 (Ollama)

↓

Response Generation



\---



\## 💻 Technology Stack



\### Frontend



\- React

\- TypeScript

\- Vite



\### Backend



\- FastAPI

\- Python

\- SQLAlchemy

\- SQLite



\### Artificial Intelligence



\- Qwen2.5-7B-Instruct

\- QLoRA Fine-Tuning

\- Ollama

\- Hugging Face Transformers



\### Translation



\- Google Cloud Translation API



\---



\## 🚀 Installation



\### Backend



```bash

cd backend

pip install -r requirements.txt

python main.py

