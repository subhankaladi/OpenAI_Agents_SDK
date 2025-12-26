from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int

# Galat input
u = User(id="abc", name="Ali", age="20")




class User:
    def __init__(self, id: int, name: str, age: int):
        self.id = id
        self.name = name
        self.age = age

# Galat input
u = User(id="abc", name="Ali", age="20")
print(u.id, u.age)
