from fastapi import FastAPI, UploadFile, File, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
import models

from auth import create_token, verify_token
from pdf_utils import read_pdf
from rag import chunk_text, add_chunks, search

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance AI Backend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= AUTH =================

@app.post("/auth/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()
    return {"msg": "Registered"}

@app.post("/auth/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid")

    token = create_token({"sub": username, "role": user.role})
    return {"access_token": token}

# ================= RBAC =================

@app.post("/roles/create")
def create_role(role: str):
    return {"msg": f"{role} created"}

@app.post("/users/assign-role")
def assign_role(username: str, role: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    user.role = role
    db.commit()
    return {"msg": "Role assigned"}

@app.get("/users/{username}/roles")
def get_role(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    return {"role": user.role}

@app.get("/users/{username}/permissions")
def permissions(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    perms = {
        "Admin": ["upload", "delete", "view"],
        "Analyst": ["upload", "view"],
        "Auditor": ["view"],
        "Client": ["view"]
    }

    return {"role": user.role, "permissions": perms.get(user.role)}

# ================= DOCUMENT =================

@app.post("/documents/upload")
def upload(
    file: UploadFile = File(...),
    company_name: str = Form(...),
    document_type: str = Form(...),
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    if user["role"] not in ["Admin", "Analyst"]:
        raise HTTPException(403, "Permission denied")

    text = read_pdf(file.file)

    chunks = chunk_text(text)
    add_chunks(chunks)

    doc = models.Document(
        title=file.filename,
        company_name=company_name,
        document_type=document_type,
        uploaded_by=user["sub"],
        content=text
    )

    db.add(doc)
    db.commit()

    return {"msg": "Document stored and indexed"}

@app.get("/documents")
def get_docs(db: Session = Depends(get_db)):
    return db.query(models.Document).all()

@app.get("/documents/{id}")
def get_doc(id: int, db: Session = Depends(get_db)):
    return db.query(models.Document).filter(models.Document.id == id).first()

@app.delete("/documents/{id}")
def delete_doc(id: int, db: Session = Depends(get_db), user=Depends(verify_token)):
    if user["role"] != "Admin":
        raise HTTPException(403, "Only admin")

    doc = db.query(models.Document).filter(models.Document.id == id).first()
    db.delete(doc)
    db.commit()

    return {"msg": "Deleted"}

@app.get("/documents/search")
def search_docs(company_name: str = "", db: Session = Depends(get_db)):
    return db.query(models.Document).filter(models.Document.company_name.contains(company_name)).all()

# ================= RAG =================

@app.post("/rag/index-document")
def index_doc(text: str):
    add_chunks(chunk_text(text))
    return {"msg": "Indexed"}

@app.post("/rag/search")
def rag_search(query: str):
    return {"results": search(query)}

@app.delete("/rag/remove-document/{id}")
def remove_doc(id: int):
    return {"msg": "Removed (simulation)"}

@app.get("/rag/context/{id}")
def context(id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == id).first()
    return {"context": doc.content[:500] if doc else "Not found"}