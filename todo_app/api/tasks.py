from pydantic import ValidationError
from todo_app.db.models import Task
from todo_app.db.schema import TaskGet, TaskCreate, TaskUpdate, UserUpdate
from fastapi import APIRouter, HTTPException
from typing import List

task_router = APIRouter(prefix='/task', tags=['Tasks'])


@task_router.post('/', response_model=dict)
async def task_create(task: TaskCreate):
    task_db = Task(**task.model_dump())
    await task_db.insert()
    return {'message': 'Perfect ✅'}


@task_router.get('/', response_model=List[TaskGet])
async def task_list():
    tasks = await Task.all().to_list()
    return [TaskGet(id=str(task.id), **task.model_dump(exclude={'id'})) for task in tasks]


@task_router.get('/{task_id}/', response_model=TaskGet)
async def task_detail(task_id: str):
    try:
        task_db = await Task.get(task_id)
        if not task_db:
            raise HTTPException(status_code=404, detail='Task not found')
        return TaskGet(id=str(task_db.id), **task_db.model_dump(exclude=({'id'})))
    except ValidationError:
        raise HTTPException(status_code=404, detail='Wrong data')


@task_router.put('/{task_id}/', response_model=dict)
async def task_update(task_id: str, task_form: TaskUpdate):
    try:
        task_db = await Task.get(task_id)
        if not task_db:
            raise HTTPException(status_code=404, detail='Task not found')
        user_data = task_form.model_dump(exclude_unset=True)
        await task_db.update({'$set': user_data})
        return {'message': 'Updated'}

    except ValidationError:
        raise HTTPException(status_code=404, detail='Wrong data')


@task_router.delete('/{task_id}/', response_model=dict)
async def task_delete(task_id: str):
    try:
        task_db = await Task.get(task_id)
        if not task_db:
            raise HTTPException(status_code=404, detail='Task not found')

        await task_db.delete()
        return {'message': 'Deleted'}
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=f'Wrong data {e}')
