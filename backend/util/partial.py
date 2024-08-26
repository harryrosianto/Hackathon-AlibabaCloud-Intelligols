from typing import Any, get_type_hints
from pydantic import BaseModel, create_model

def optional(*fields):
    def dec(cls):
        new_fields = {}
        for name, field in cls.model_fields.items():
            if name in fields:
                new_fields[name] = (Any | None, None)
            else:
                new_fields[name] = (field.annotation, ...)

        return create_model(
            f"Optional{cls.__name__}",
            __base__=cls,
            **new_fields
        )

    if fields and isinstance(fields[0], type) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.model_fields.keys()
        return dec(cls)
    return dec