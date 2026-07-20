# 🤖 Multi-Agent AI Customer Support Assistant

An enterprise-grade **Multi-Agent Customer Support Assistant** built with **Python, FastAPI, Next.js, and Google Gemini**. Instead of relying on a single chatbot, the system uses a **custom Machine Learning intent router** to dispatch customer queries to specialized AI agents. Responses are grounded using **Retrieval-Augmented Generation (RAG)** with a FAISS vector database, ensuring accurate answers based on company documentation while minimizing AI hallucinations.

---

## 📖 Overview

This project demonstrates how modern AI systems can be combined with traditional Machine Learning techniques to build an intelligent customer support platform.

The workflow consists of:

1. User submits a query through the web interface.
2. A custom **TF-IDF + Logistic Regression** model predicts the user's intent.
3. The query is routed to a specialized AI agent.
4. The agent retrieves relevant company documents from a **FAISS vector database**.
5. Google Gemini generates a response using only the retrieved context.
6. The complete conversation is stored in MongoDB Atlas.

---

## ✨ Features

- 🚀 Multi-Agent Architecture
- 🧠 Custom ML Intent Router (TF-IDF + Logistic Regression)
- 📚 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic Search using FAISS
- 🤖 Google Gemini Integration
- 💬 Persistent Chat History with MongoDB Atlas
- ⚡ FastAPI Backend
- 🎨 Next.js + React Frontend
- ☁️ Cloud Deployment Ready (Render + Vercel)

---

## 🏗️ Architecture

```
                     User
                      │
                      ▼
             Next.js Frontend
                      │
                      ▼
               FastAPI Backend
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
 Intent Classification        Conversation Memory
(TF-IDF + Logistic Reg.)      (MongoDB Atlas)
        │
        ▼
  Specialized Agent
        │
        ▼
   FAISS Vector Search
        │
        ▼
 Company Knowledge Base
        │
        ▼
   Google Gemini LLM
        │
        ▼
      Response
```

---

# 📂 Project Structure

```
customer-support-ai/
│
├── backend/
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── router.py
│   │   ├── billing_agent.py
│   │   ├── technical_agent.py
│   │   ├── product_agent.py
│   │   ├── complaint_agent.py
│   │   └── faq_agent.py
│   │
│   ├── database/
│   │   └── mongodb.py
│   │
│   ├── ml/
│   │   ├── train_router.py
│   │   └── artifacts/
│   │       └── router_model.pkl
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   └── retriever.py
│   │
│   ├── vectorstore/
│   │
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│
├── knowledge_base/
│   ├── faq.pdf
│   ├── refund_policy.pdf
│   ├── shipping_policy.pdf
│   ├── warranty.pdf
│   └── user_manual.pdf
│
└── README.md
```

---

# 🗄️ Datasets

## Intent Classification Dataset

**Source**

- Banking77 Dataset
- https://huggingface.co/datasets/banking77

### Usage

The Banking77 dataset contains more than **10,000 customer support queries** across multiple intent categories.

For this project:

- Intent classes were mapped into five business domains.
- Additional e-commerce customer support queries were added.
- Dataset balancing was performed before training.

---

## Knowledge Base

The RAG system uses a collection of company documents.

Included documents:

- FAQ
- Shipping Policy
- Refund Policy
- Warranty Policy
- Product User Manual

These PDFs are:

- Split into semantic chunks
- Embedded using Google's embedding model
- Stored inside a FAISS vector database

---

# 🛠️ Tech Stack

## Frontend

- React.js
- Next.js
- Tailwind CSS

## Backend

- Python
- FastAPI
- Uvicorn

## AI & Machine Learning

- Google Gemini
- LangChain
- Scikit-learn
- TF-IDF Vectorizer
- Logistic Regression

## Vector Database

- FAISS

## Database

- MongoDB Atlas

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/JohnPrice11/Customer-Support-AI

cd customer-support-ai
```

---

## Backend Setup

```bash
python -m venv .venv
```

### Activate Environment

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# 🔑 Environment Variables

Create a `.env` file inside the backend directory.

```env
GOOGLE_API_KEY=your_google_gemini_api_key

MONGODB_URI=your_mongodb_connection_string
```

---

# 🧠 Train the Intent Router

```bash
python backend/ml/train_router.py
```

Expected output

```
Training Complete!
Accuracy: ~95%
```

---

# 📚 Build the FAISS Vector Database

```bash
python backend/rag/ingest.py
```

Expected output

```
FAISS Vector Database successfully generated.
```

---

# 🚀 Run the Application

## Start Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Backend

```
http://127.0.0.1:8000
```

---

## Start Frontend

```bash
cd frontend

npm run dev
```

Frontend

```
http://localhost:3000
```

---

# 🔄 Workflow

```
User Query
     │
     ▼
Intent Router
     │
     ▼
Choose Appropriate Agent
     │
     ▼
Retrieve Relevant Documents
     │
     ▼
Generate Gemini Response
     │
     ▼
Store Conversation
     │
     ▼
Return Response
```

## ⭐ If you found this project useful, consider giving it a star!
