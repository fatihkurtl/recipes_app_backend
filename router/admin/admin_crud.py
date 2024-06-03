from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.members import Members
from schemas.members_schema import MemberBase


def get_all_members(db: Session, skip: int = 0, limit: int = 10):
    try:
        members = db.query(Members).offset(skip).limit(limit).all()
        if not members:
            raise HTTPException(status_code=404, detail="No members found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return [MemberBase.from_orm(member) for member in members]