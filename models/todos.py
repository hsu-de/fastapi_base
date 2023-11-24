from pydantic import BaseModel

class Todo(BaseModel):
    name: str
    description: str | None =None
    complete: bool =False

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "name": "todo title",
                    "description": "todo description",
                    "complete": False
                }
            ]
        }