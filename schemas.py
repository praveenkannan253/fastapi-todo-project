from pydantic import BaseModel,ConfigDict

class TodoBase(BaseModel):
    title:str
    description:str|None = None
    completed:bool=False

class TodoCreate(TodoBase):
    pass

class TodoSchema(TodoBase):
    id:int
    model_config = ConfigDict(from_attributes=True)