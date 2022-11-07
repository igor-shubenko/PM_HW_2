from fastapi import FastAPI
import uvicorn
from typing import Union
from pydantic import BaseModel
from file_workers import JsonFileWorker


app = FastAPI()

file_object = JsonFileWorker('data.jsonl')

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None
#
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


@app.get('/{ind}')
def get_record(ind: Union[str, int]):
    if ind == 'all':
        return file_object.data
    return f"Need idea for unique identificator: {ind}"

@app.post('/')
def create_record(data):
    pass

@app.put('/{ind}')
def update_record(dara):
    pass

@app.delete('/{ind}')
def delete_record(ind: Union[str, int]):
    if ind == 'all':
        file_object.data = []
    return f"Need idea for unique identificator: {ind}"


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8765, reload=True)

