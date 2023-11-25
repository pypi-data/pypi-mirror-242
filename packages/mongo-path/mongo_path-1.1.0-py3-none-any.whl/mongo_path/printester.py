from pydantic import BaseModel

from mongo_path.meta import MongoMeta


class B(BaseModel):
    c: str

class A(BaseModel, metaclass=MongoMeta):
    d: int
    b: B

print(A.b.c)
print(A(d=2,b=B(c='c')))
