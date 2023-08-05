from typing import Optional, Any, Dict
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

class Book(BaseModel):
    title: str = Field(...)
    price: float = Field(...)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "book": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "English is fun",
                "price": 100
            }
        }


class BookUpdate(BaseModel):
    title: Optional[str]
    price: Optional[float]

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        json_schema_extra = {
            "book": {
                "title": "English is fun",
                "price": 100
            }
        }
