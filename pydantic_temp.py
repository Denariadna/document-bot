from dataclasses import dataclass

from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int


class User2(BaseModel):
    name: str
    age: int
    user: User


@dataclass
class UserDTO:
    name: str
    age: int


if __name__ == '__main__':
    a = User(name='Arina', age='19')
    x = User2(name='Daniil', age='18', user=a)
