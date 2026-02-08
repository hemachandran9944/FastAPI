from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from schemas import Todo as TodoSchema

# Table create 
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.post("/todos", response_model=TodoSchema)
def create_todo(todo: TodoSchema, db: Session = Depends(get_db)):
    db_todo = models.Todo(**todo.dict(exclude={"id"}))
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos", response_model=list[TodoSchema])
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

@app.get("/todos/{todo_id}", response_model=TodoSchema)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()