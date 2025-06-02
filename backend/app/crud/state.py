from sqlmodel import Session
from app.enums.state import State

# LOOP-124
def get_states():
    return [State.BLOCKED, State.FINISH, State.PROGRESS, State.REVIEW, State.TODO]
