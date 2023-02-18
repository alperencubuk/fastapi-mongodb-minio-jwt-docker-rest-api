from enum import Enum


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"

    @classmethod
    def values(cls) -> list:
        return [role.value for role in UserRole]
