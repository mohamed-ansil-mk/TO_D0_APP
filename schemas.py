from pydantic import BaseModel

class TodoBase(BaseModel):
    title:str
    description:str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    title:str | None = None
    description:str | None = None
    completed:bool | None = None

class Todoresponse(TodoBase):
    id:int
    completed:bool

    class config:
        orm_mode = True