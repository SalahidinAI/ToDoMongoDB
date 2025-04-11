from pydantic import ValidationError
from todo_app.db.models import User
from todo_app.db.schema import UserGet, UserCreate, UserUpdate
from fastapi import APIRouter, HTTPException
from typing import List

user_router = APIRouter(prefix='/user', tags=['Users'])


@user_router.post('/', response_model=dict)
async def user_create(user: UserCreate):
    user_db = User(**user.model_dump())
    await user_db.insert()
    return {'message': 'Saved'}


@user_router.get('/', response_model=List[UserGet])
async def user_list():
    users = await User.all().to_list()
    return [UserGet(id=str(user.id), **user.model_dump(exclude={'id'})) for user in users]


@user_router.get('/{user_id}/', response_model=UserGet)
async def user_detail(user_id: str):
    try:
        user_db = await User.get(user_id)
        if not user_db:
            raise HTTPException(status_code=404, detail='User not found')
        return UserGet(id=str(user_db.id), **user_db.model_dump(exclude={'id'}))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f'Wrong id {str(e)}')


@user_router.put('/{user_id}/', response_model=dict)
async def user_update(user_id: str, user_form: UserUpdate):
    try:
        user_db = await User.get(user_id)
        if user_db is None:
            raise HTTPException(status_code=404, detail='User not found')

        user_data = user_form.model_dump(exclude_unset=True)
        await user_db.update({'$set': user_data})
        return {'message': 'Upgraded'}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f'Wrong id {str(e)}')


@user_router.delete('/{user_id}/', response_model=dict)
async def user_delete(user_id: str):
    try:
        user_db = await User.get(user_id)
        if not user_db:
            raise HTTPException(status_code=404, detail='User not found')

        await user_db.delete()
        return {'message': 'Deleted'}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f'Wrong id {str(e)}')
