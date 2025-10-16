from pydantic import BaseModel

class TodoBase(BaseModel):
    title:str
    description:str

class TodoCreate(TodoBase):
    completed: bool = False

class TodoUpdate(TodoBase):
    title:str | None = None
    description:str | None = None
    completed:bool | None = None

class Todoresponse(TodoBase):
    id:int
    completed:bool

    class Config:
        orm_mode = True