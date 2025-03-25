from enum import Enum

class Type(str, Enum):
    USERSTORY = "User Story"
    BUG = "Bug"
    SUBTASK = "Subtask"
    EPIC = "Epic"