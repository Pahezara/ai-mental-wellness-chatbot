# Mental Health Chatbot (Sinhala + English) - Backend

## Setup (Windows)
1) Create venv and activate
2) Install torch using PyTorch official command (CUDA build)
3) Install requirements:
   pip install -r requirements.txt
4) Run:
   python main.py

## Endpoints
- GET  /healthz
- POST /chat
- GET  /analytics/emotions/{user_id}?days=14