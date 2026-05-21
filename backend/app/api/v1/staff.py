from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.user import User, Role
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate, Role as RoleSchema, RoleCreate
from app.core.dependencies import get_current_active_user, require_role

router = APIRouter()

# --- ROLES ---
@router.get("/roles", response_model=List[RoleSchema])
async def get_roles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role))
    return result.scalars().all()

@router.post("/roles", response_model=RoleSchema)
async def create_role(role_in: RoleCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role).filter(Role.name == role_in.name))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Role already exists")
    
    role = Role(
        name=role_in.name,
        description=role_in.description,
        allowed_tabs=role_in.allowed_tabs
    )
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role

# --- USERS / STAFF ---
@router.get("/users", response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).options(selectinload(User.role)))
    return result.scalars().all()

@router.post("/users", response_model=UserSchema)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Check if role exists
    if user_in.role_id:
        role_result = await db.execute(select(Role).filter(Role.id == user_in.role_id))
        if not role_result.scalars().first():
            raise HTTPException(status_code=400, detail="Role does not exist")

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        role_id=user_in.role_id
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Load role relationship to return in response
    result = await db.execute(select(User).options(selectinload(User.role)).filter(User.id == user.id))
    return result.scalars().first()

@router.put("/roles/{role_id}", response_model=RoleSchema)
async def update_role(role_id: int, role_in: RoleCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role).filter(Role.id == role_id))
    role = result.scalars().first()
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    
    # Check name collision if renaming
    if role.name != role_in.name:
        collision_res = await db.execute(select(Role).filter(Role.name == role_in.name))
        if collision_res.scalars().first():
            raise HTTPException(status_code=400, detail="Роль с таким системным именем уже существует")
            
    role.name = role_in.name
    role.description = role_in.description
    role.allowed_tabs = role_in.allowed_tabs
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role

@router.delete("/roles/{role_id}")
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role).filter(Role.id == role_id))
    role = result.scalars().first()
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    
    # Check if users are assigned to this role
    users_res = await db.execute(select(User).filter(User.role_id == role_id))
    if users_res.scalars().first():
        raise HTTPException(status_code=400, detail="Невозможно удалить роль, так как к ней привязаны сотрудники")
        
    await db.delete(role)
    await db.commit()
    return {"msg": "Роль успешно удалена"}

@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
        
    # Check email collision
    if user.email != user_in.email:
        collision_res = await db.execute(select(User).filter(User.email == user_in.email))
        if collision_res.scalars().first():
            raise HTTPException(status_code=400, detail="Сотрудник с такой почтой уже существует")
            
    user.email = user_in.email
    user.full_name = user_in.full_name
    user.is_active = user_in.is_active
    user.role_id = user_in.role_id
    
    if user_in.password:
        user.hashed_password = get_password_hash(user_in.password)
        
    db.add(user)
    await db.commit()
    
    result = await db.execute(select(User).options(selectinload(User.role)).filter(User.id == user.id))
    return result.scalars().first()

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
        
    await db.delete(user)
    await db.commit()
    return {"msg": "Сотрудник успешно удален"}
