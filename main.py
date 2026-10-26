from fastapi import FastAPI,Depends,HTTPException
from schemas import TodoCreate,TodoSchema
from sqlalchemy.orm import Session
from database import SessionLocal,engine,Base
from models import Todo

Base.metadata.create_all(bind=engine)
app=FastAPI()

#Dependency for DB session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST - Create TODO tasks
@app.post("/todos",response_model=TodoSchema)
def create(todo:TodoCreate,db:Session=Depends(get_db)):
    db_todo=Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

#GET - ALL TODOs
@app.get("/todos",response_model=list[TodoSchema])
def read_todos(db:Session=Depends(get_db)):
    return db.query(Todo).all()

#GET - getting the single TODO
@app.get("/todos/{todo_id}",response_model=TodoSchema)
def read_todo(todo_id:int,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo Not Found")
    return todo

#PUT - UPDATE THE todos
@app.put("/todos/{todo_id}",response_model=TodoSchema)
def update_todo(todo_id:int, updated:TodoCreate,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo Not Found")
    for key,value in updated.dict().items():
        setattr(todo,key,value)
    db.commit()
    db.refresh(todo)
    return todo
      
#DELETE - delete the todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
         raise HTTPException(status_code=404,detail="Todo Not Found")
    db.delete(todo)
    db.commit()
    return {"message":"TODO deleted Successfully"}

@app.get("/")
def root():
    return {"message": "Todo API is running"}