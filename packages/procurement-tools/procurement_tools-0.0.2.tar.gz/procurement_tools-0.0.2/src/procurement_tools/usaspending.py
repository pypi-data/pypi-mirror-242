from hashlib import md5
import uuid


def convertUEItoHash(uei: str, level: str = "P") -> str:
    """Convert a UEI into a Hash for USASpending.gov"""
    uei_string = ("uei-" + uei).upper()
    m = md5(bytes(uei_string.encode()))
    return f"{str(uuid.UUID(m.hexdigest()))}-{level}"
