from sqlalchemy.orm import Session

from app.helper.enum import ConfigValueType
from app.model import Config


class ConfigProvider:
    @classmethod
    def create_config(cls, db: Session, commit: bool = False, **data) -> Config:
        config_dict = {
            "id": data.get("id", None),
            "value": data.get("value", "BIDV"),
            "type": data.get("type", ConfigValueType.COUNTRY.value),
            "name": data.get("name", "BIDV"),
            "deleted_at": data.get("deleted_at", None)
        }

        config: Config = Config.create(db, config_dict, commit=commit)

        return config
