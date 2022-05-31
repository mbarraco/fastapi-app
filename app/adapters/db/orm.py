from typing import Any, Dict, Optional

from sqlalchemy.ext.declarative import as_declarative, declared_attr

class_registry: Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: Any
    __name__: str
    table_name: Optional[str] = None

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.table_name if cls.table_name else cls.__name__.lower() + "s"

    def to_dict(self):
        return dict(
            (col, getattr(self, col)) for col in self.__table__.columns.keys()
        )
