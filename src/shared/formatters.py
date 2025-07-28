from pydantic import BaseModel as PydanticBaseModel


class BoolConverter(PydanticBaseModel):
    value: str | int | bool

    def as_bool(self) -> bool:
        truthy_values = {"y", "yes", "true", "1"}
        falsy_values = {"n", "no", "false", "0"}

        val_str = str(self.value).strip().lower()
        if val_str in truthy_values:
            return True
        elif val_str in falsy_values:
            return False
        else:
            raise ValueError(f"Cannot convert '{self.value}' to boolean")
