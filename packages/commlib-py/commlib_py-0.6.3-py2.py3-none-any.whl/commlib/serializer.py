# Copyright (C) 2020  Panayiotou, Konstantinos <klpanagi@gmail.com>
# Author: Panayiotou, Konstantinos <klpanagi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import abc
import enum
from typing import Any

DEFAULT_JSON_SERIALIZER = 'ujson'


if DEFAULT_JSON_SERIALIZER == 'json':
    import json as json
elif DEFAULT_JSON_SERIALIZER == 'orjson':
    import orjson as json
elif DEFAULT_JSON_SERIALIZER == 'ujson':
    import ujson as json


class SerializationTypes(enum.IntEnum):
    JSON = 0


class ContentType:
    """Content Types."""
    json: str = 'application/json'
    raw_bytes: str = 'application/octet-stream'
    text: str = 'plain/text'


class Serializer(abc.ABC):
    """Serializer Abstract Class."""
    CONTENT_TYPE: str = 'None'
    CONTENT_ENCODING: str = 'None'

    @staticmethod
    def serialize(data: Any) -> str:
        """serialize.

        Args:
            data (dict): Serialize a dict
        """
        raise NotImplementedError()

    @staticmethod
    def deserialize(data: str) -> Any:
        """deserialize.

        Args:
            data (str): -
        """
        raise NotImplementedError()


class JSONSerializer(Serializer):
    """Thin wrapper to implement json serializer.

    Static class.
    """
    CONTENT_TYPE: str = 'application/json'
    CONTENT_ENCODING: str = 'utf8'

    @staticmethod
    def serialize(data: Any) -> str:
        """serialize.

        Args:
            data (dict): Serialize to json string
        """
        return json.dumps(data)

    @staticmethod
    def deserialize(data: str) -> Any:
        """deserialize.

        Args:
            data (str): json str to dict
        """
        return json.loads(data)
