from sqlalchemy.orm import Session

from models.example_table import ExampleTable


async def example_service(id: str, db: Session):
    example_record = ExampleTable(id=id)
    db.add(example_record)
    db.commit()
    db.refresh(example_record)
    return example_record