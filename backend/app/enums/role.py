from enum import Enum

class Role(str, Enum):
    """role enum

    Args:
        str (name): name of the role
        Enum (name): role identifier
    """
    PRODUCTOWNER = "Product-Owner"
    PROJECTMEMBER = "Project-Member"
    USER = "User"