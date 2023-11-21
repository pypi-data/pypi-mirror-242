# -*- coding: utf-8 -*-
# pylint: disable=C0114

import json
from typing import Any, Dict, List

from delpinos.core.encoders.raw_encoder import RawEncoder

from delpinos.crud.domain.entities import BaseEntity


class BaseEncoder(RawEncoder):
    def encode(self, obj: Any, **_) -> str:
        if isinstance(obj, str):
            return obj
        if isinstance(obj, BaseEntity):
            return obj.model_dump_json(by_alias=True)
        if isinstance(obj, (dict, list, set)):
            obj = self.decode(obj)
        return json.dumps(obj, default=str)

    def decode(self, obj: Any, **_) -> Dict[str, Any] | List[Any]:
        if isinstance(obj, BaseEntity):
            return obj.model_dump(by_alias=True)
        if isinstance(obj, dict):
            new_value = {}
            for key, value in obj.items():
                new_value[key] = self.decode(value)
            return new_value
        if isinstance(obj, (list, set)):
            return list(map(self.decode, obj))
        return obj
