from fastapi import FastAPI, Body
import uvicorn
from file_workers import DataWorker
from typing import Union

app = FastAPI()

file_object = DataWorker('data.jsonl')

@app.get('/get/{ind}')
def get_record(ind: str):
    return file_object.get_record(ind)

@app.post('/add/')
def create_record(data: Union[dict, None]=Body()):
    return file_object.create_record(data)

@app.put('/change/{ind}')
def update_record(ind, data: Union[dict, None]=Body()):
    return file_object.update_record(ind, data)

@app.delete('/delete/{ind}')
def delete_record(ind: str):
    return file_object.delete_record(ind)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8765, reload=True, workers=1)

