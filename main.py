from fastapi import FastAPI, HTTPException
import uvicorn
from schemas import Task

app = FastAPI()

tasks_db = {}
cur_counter = 1


@app.post("/tasks")
def create_task(task: Task) -> dict:
    global cur_counter
    cur_id = cur_counter
    cur_counter += 1
    new_task = {
        "id": cur_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
    }
    tasks_db[cur_id] = new_task
    return new_task


@app.get("/tasks")
def get_tasks():
    return list(tasks_db.values())


@app.get("/tasks/{id}")
def get_task(id: int):
    task = tasks_db.get(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{id}")
def delete_task(id: int):
    task = tasks_db.pop(id, None)
    if task is not None:
        return {"message": f"task №{id} has been deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{id}")
def update_task(id: int, task: Task):
    if id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = {
        "id": id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
    }
    tasks_db[id] = updated_task
    return updated_task


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
