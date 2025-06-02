from enum import Enum

class Priority(str, Enum):
    """role enum

    Args:
        str (name): name of the priority
        Enum (name): priority identifier
    """
    VHIGH = "Very high"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    VLOW = "Very low"