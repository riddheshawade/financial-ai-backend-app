# 📊 Finance AI Backend

## 📌 Overview
This project is a FastAPI-based Financial Document Management System with AI-powered semantic search (RAG).

It allows organizations to upload, manage, and search financial documents like invoices, reports, and contracts using intelligent retrieval.

---

## 🚀 Features

### 🔐 Authentication & Security
- JWT-based Authentication
- Secure Login & Registration

### 👥 Role-Based Access Control (RBAC)
- Admin → Full Access  
- Analyst → Upload & Edit Documents  
- Auditor → Review Documents  
- Client → View Documents  

---

### 📄 Document Management
- Upload PDF documents  
- Extract text using PyPDF2  
- Store documents in database  
- Retrieve all documents  
- Get document by ID  
- Delete documents  

---

### 🤖 AI Semantic Search (RAG)
- Text extraction from PDFs  
- Chunking of document content  
- Embedding generation  
- Semantic search over documents  

---

## 🛠️ Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT (python-jose)
- PyPDF2
- Uvicorn

---

## ▶️ How to Run

### 1️⃣ Install dependencies
pip install -r requirements.txt

### 2️⃣ Run server
uvicorn app:app --reload

### 3️⃣ Open Swagger UI
http://127.0.0.1:8000/docs

---

## 🔄 API Workflow

1. Register a user → /auth/register  
2. Login → /auth/login  
3. Copy JWT token  
4. Click Authorize in Swagger  
5. Upload document → /documents/upload  
6. Search documents → /rag/search  

---

## 📌 Example Use Case

Search Query:
What is the financial risk in this document?

Returns:
- Relevant document chunks  
- Context-based answers  

---

## 👨‍💻 Author

Riddhesh Awade
