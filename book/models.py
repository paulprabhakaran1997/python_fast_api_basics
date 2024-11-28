from pydantic import BaseModel

class Book(BaseModel):
    name : str
    price : float = 0
    is_offer : bool = None