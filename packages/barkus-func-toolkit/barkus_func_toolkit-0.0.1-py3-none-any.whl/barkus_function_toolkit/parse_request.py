import base64
import json
from typing import TypeVar, Type, Any, TypedDict, Dict, Callable, List, Optional
from typing_extensions import Unpack, NotRequired
from dacite import from_dict, Config
from .decorators import log

DataModel = TypeVar("DataModel")

class ParseOptions(TypedDict):
    type_hooks: NotRequired[Dict[Type, Callable[[Any], Any]]]
    cast: NotRequired[List[Type]]
    forward_references: NotRequired[Optional[Dict[str, Any]]]
    check_types: NotRequired[bool]
    strict: NotRequired[bool]
    strict_unions_match: NotRequired[bool]

def _parse_data(data, Model: Type[DataModel], **kwargs) -> DataModel:
    if Model == dict:
        return data

    return from_dict(Model, data, Config(**kwargs))


@log(0, name = "parse_request.http")
def http(request, *, Model: Type[DataModel], **kwargs: Unpack[ParseOptions]) -> DataModel:
    print(f"{request=}")
    request_body = request.get_json(silent=True)  or {}
    print(f"{request_body=}")
    data: Any = request_body
    print(f"{data=}")
    return _parse_data(data, Model, **kwargs)

@log(0, name = "parse_request.http")
def cloud_event(cloud_event, *, Model: Type[DataModel], **kwargs: Unpack[ParseOptions]) -> DataModel:
    cloud_event_data = cloud_event.data['message']['data']
    decoded_event = base64.b64decode(cloud_event_data)
    print(f"{decoded_event=}")
    event_data_string = base64.b64decode(cloud_event_data).decode('utf-8')
    print(f"{event_data_string=}")

    data = json.loads(event_data_string)
    return _parse_data(data, Model, **kwargs)
