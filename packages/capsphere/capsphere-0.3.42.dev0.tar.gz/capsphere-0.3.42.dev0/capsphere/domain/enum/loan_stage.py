from enum import Enum


class LoanStage(Enum):
    NORMAL = "NORMAL"
    DEFAULTED = "DEFAULTED"
    EXPIRED = "EXPIRED"
