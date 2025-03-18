from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from validations import get_current_user
import crud.material
import config.db
import schemas.materials
import models.material

material = APIRouter()

models.material.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@material.get("/material/", response_model=List[schemas.materials.Material], tags=["Materials"])
async def read_materials(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.material.get_materials(db=db, skip=skip, limit=limit)

@material.post("/material/", response_model=schemas.materials.Material, tags=["Materials"])
async def create_material(material_data: schemas.materials.MaterialCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.material.create_material(db=db, material=material_data)

@material.put("/material/{id}", response_model=schemas.materials.Material, tags=["Materials"])
async def update_material(id: int, material_data: schemas.materials.MaterialUpdate, db: Session = Depends(get_db,), current_user: dict = Depends(get_current_user)):
    db_material = crud.material.update_material(db=db, material_id=id, material=material_data)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

@material.delete("/material/{id}", response_model=schemas.materials.Material, tags=["Materials"])
async def delete_material(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_material = crud.material.delete_material(db=db, material_id=id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material
