from sqlmodel import Session
from app.enums.issueType import Type 
# LOOP-124
def get_categories():
    return [Type.BUG, Type.EPIC, Type.USERSTORY, Type.SUBTASK]
