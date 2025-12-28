from fastapi import FastAPI, Depends
from schemas import Todo as TodoSchema
from sqlalchemy.orm import session
from database import SessionLocal
from models import Todo



app = FastAPI()

#Dependency for DB session 

def get_db():
    db = sessionLocal()
    try:
        yield db 
    finally:
        db.close()    

# Post - Create  TODO

@app.post("/todos", response_model=TodoSchema)
def create(todo : TodoSchema, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh()
    return db_todo

    



