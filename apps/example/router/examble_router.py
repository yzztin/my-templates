import re
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database.mysql_client import get_db
from apps.example.service.example_service import example_service

router = APIRouter()


@router.post("/db-test")
async def db_test(id: str, db: Session = Depends(get_db)):
    return example_service(id, db)