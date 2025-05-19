from enum import Enum


class State(str, Enum):
    """role enum

    Args:
        str (name): name of the status
        Enum (name): status identifier
    """

    TODO = "To Do"
    PROGRESS = "In progress"
    REVIEW = "In review"
    BLOCKED = "Blocked"
    FINISH = "Finished"