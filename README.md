# AI-Powered Bilingual Mental Wellness Chatbot

## Overview

This project is an AI-powered mental wellness chatbot designed to provide supportive conversations in both Sinhala and English. The system combines emotion recognition, risk assessment, machine translation, and a fine-tuned Large Language Model (LLM) to deliver context-aware and empathetic responses while maintaining user safety.

The solution was developed as a final-year academic project and demonstrates the integration of Artificial Intelligence, Natural Language Processing, Machine Learning, and Full-Stack Software Engineering.

---

## Key Features

* Sinhala and English conversational support
* Automatic language detection
* Google Translate integration for Sinhala ↔ English translation
* Emotion recognition using transformer-based NLP models
* Risk assessment for crisis-related conversations
* Fine-tuned Qwen2.5-based local LLM using Ollama
* FastAPI backend architecture
* React + TypeScript frontend
* Session management and conversation tracking
* Privacy-aware design with optional text storage
* Mental wellness focused response generation

---

## Technology Stack

### Frontend

* React
* TypeScript
* Vite
* CSS

### Backend

* FastAPI
* Python
* SQLAlchemy
* SQLite

### Artificial Intelligence

* Qwen2.5-7B-Instruct
* QLoRA Fine-Tuning
* Ollama
* Hugging Face Transformers
* GoEmotions Emotion Classification

### Translation

* Google Cloud Translation API

---

## System Architecture

User → React Frontend → FastAPI Backend → Translation Layer → Emotion Detection → Risk Assessment → Fine-Tuned Qwen2.5 Model (Ollama) → Response Generation → Frontend

---

## Project Structure

```text
backend/
frontend/
training/
docs/
README.md
```

---

## Running the Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## Fine-Tuned Model

Base Model:

```text
Qwen2.5-7B-Instruct
```

Fine-Tuning Method:

```text
QLoRA
```

Deployment:

```text
Ollama
```

The final GGUF model is stored separately due to GitHub file size limitations.

---

## Safety Notice

This application is intended to provide emotional support and wellness-oriented conversation. It is not a substitute for professional mental health services, medical advice, diagnosis, or treatment.

For high-risk situations, users should seek immediate assistance from qualified professionals and emergency services.

---

## Author

Lakindu Pehesara

BSc (Hons) Data Science

Plymouth University

United Kingdom

---

## Academic Purpose

This repository was developed as part of a final-year undergraduate research and development project focused on AI-assisted mental wellness support systems.
