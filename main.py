from fastapi import FastAPI, HTTPException, Depends, status
from dependencies import tasks_db, get_next_id
import uvicorn
from schemas import STaskUpdate, Task

app = FastAPI()


@app.post("/tasks", status_code=status.HTTP_200_OK)
def create_task(task: Task, next_id: str = Depends(get_next_id)) -> dict:
    new_task = {
        "id": next_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
    }
    tasks_db[next_id] = new_task
    return new_task


@app.get("/tasks")
def get_tasks():
    return list(tasks_db.values())


@app.get("/tasks/{id}")
def get_task(id: int):
    task = tasks_db.get(id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    task = tasks_db.pop(id, None)
    if task is not None:
        return {"message": f"task №{id} has been deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@app.patch("/tasks/{id}", status_code=status.HTTP_200_OK)
def update_task(id: int, task: STaskUpdate):
    if id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    updated_task = task.model_dump(exclude_unset=True)
    tasks_db[id].update(updated_task)
    return tasks_db[id]


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
