from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="To-Do-List API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new task
@app.post("/tools/", response_model=schemas.Todoresponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# Get all tasks
@app.get("/tools/", response_model=list[schemas.Todoresponse])
def read_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


# Get a task by ID
@app.get("/tools/{todo_id}", response_model=schemas.Todoresponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return todo

# Update a task by ID
@app.put("/tools/{todo_id}", response_model=schemas.Todoresponse)
def update_todo(todo_id: int, update_data: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

# Delete a task by ID
@app.delete("/tools/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "To-do deleted successfully"}

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html directly
@app.get("/")
def read_root():
    file_path = os.path.join("static", "index.html")
    return FileResponse(file_path)
