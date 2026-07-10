from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

tasks_db = []
cur_counter = 1

class Task(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    completed: bool = False

@app.post("/tasks")
def create_task(task: Task) -> dict:
    global cur_counter
    cur_id = cur_counter
    cur_counter += 1
    new_task = {"id": cur_id, "title": task.title, "description": task.description, "completed":task.completed}
    tasks_db.append(new_task)
    return new_task

@app.get("/tasks")
def get_tasks():
    return tasks_db

@app.get("/tasks/{id}")
def get_task(id:int):
    for i in range(len(tasks_db)):
        if tasks_db[i]["id"] == id:
            return tasks_db[i]
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}")
def delete_task(id:int):
    for i in range(len(tasks_db)):
        if tasks_db[i]["id"] == id:
            tasks_db.pop(i)
            return f'"message": task №{id} has been deleted'
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{id}")
def update_task(id: int, task: Task):
    for index, el in enumerate(tasks_db):
        if el["id"] == id:
            tasks_db[index] = {"id": id, "title": task.title, "description": task.description, "completed":task.completed}
            return f'task №{id} has been updated'
    raise HTTPException(status_code=404, detail="Task not found")