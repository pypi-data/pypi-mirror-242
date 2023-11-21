# Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import List, Optional, Type, get_args

from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo

from erniebot.utils.logging import logger

INVALID_FIELD_NAME = "__invalid_field_name__"


def is_optional_type(type: Type):
    args = get_args(type)
    if len(args) == 0:
        return False

    return len([arg for arg in args if arg is None.__class__]) > 0


def get_typing_list_type(type):
    """get typing.List[T] element type

    Args:
        type (typing.List): Generics type
    """
    # 1. checking list type
    if getattr(type, "_name", None) != "List":
        return None

    arg_type = get_args(type)[0]
    return json_type(arg_type)


def json_type(type: Optional[Type[object]] = None):
    if type is None:
        return "object"

    mapping = {
        int: "integer",
        str: "string",
        list: "array",
        List: "array",
        float: "number",
        ToolParameterView: "object",
    }

    if inspect.isclass(type) and issubclass(type, ToolParameterView):
        return "object"

    if getattr(type, "_name", None) == "List":
        return "array"

    if type not in mapping:
        args = [arg for arg in get_args(type) if arg is not None.__class__]
        if len(args) > 1 or len(args) == 0:
            raise ValueError(
                "only support simple type: FieldType=int/str/float/ToolParameterView, "
                "so the target type should be one of: FieldType, List[FieldType], "
                f"Optional[FieldType], but receive {type}"
            )
        type = args[0]

    if type in mapping:
        return mapping[type]

    if inspect.isclass(type) and issubclass(type, ToolParameterView):
        return "object"

    return str(type)


def python_type_from_json_type(json_type_dict: dict) -> Type[object]:
    simple_types = {"integer": int, "string": str, "number": float, "object": ToolParameterView}
    if json_type_dict["type"] in simple_types:
        return simple_types[json_type_dict["type"]]

    assert (
        json_type_dict["type"] == "array"
    ), f"only support simple_types<{','.join(simple_types)}> and array type"
    assert "type" in json_type_dict["items"], "<items> field must be defined when 'type'=array"

    json_type_value = json_type_dict["items"]["type"]
    if json_type_value == "string":
        return List[str]
    if json_type_value == "integer":
        return List[int]
    if json_type_value == "number":
        return List[float]
    if json_type_value == "object":
        return List[ToolParameterView]

    raise ValueError(f"unsupported data type: {json_type_value}")


def scrub_dict(d: dict, remove_empty_dict: bool = False) -> Optional[dict]:
    """remove empty Value node,

        function_call_schema: require

    Args:
        d (dict): the instance of dictionary
        remove_empty_dict (bool): whether remove empty dict

    Returns:
        dict: the dictionary data after slimming down
    """
    if type(d) is dict:
        result = {}
        for k, v in d.items():
            v = scrub_dict(v, remove_empty_dict)
            if v is not None:
                result[k] = v

        if len(result) == 0:
            if not remove_empty_dict:
                return {}
            return None

        return result
    elif isinstance(d, list):
        return [scrub_dict(item, remove_empty_dict) for item in d]  # type: ignore
    else:
        return d


class OpenAPIProperty(BaseModel):
    type: str
    description: Optional[str] = None
    required: Optional[List[str]] = None
    items: dict = Field(default_factory=dict)
    properties: dict = Field(default_factory=dict)


def get_field_openapi_property(field_info: FieldInfo) -> OpenAPIProperty:
    """convert pydantic FieldInfo instance to OpenAPIProperty value

    Args:
        field_info (FieldInfo): the field instance

    Returns:
        OpenAPIProperty: the converted OpenAPI Property
    """
    typing_list_type = get_typing_list_type(field_info.annotation)
    if typing_list_type is not None:
        field_type = "array"
    elif is_optional_type(field_info.annotation):
        field_type = json_type(get_args(field_info.annotation)[0])
    else:
        field_type = json_type(field_info.annotation)

    property = {
        "type": field_type,
        "description": field_info.description,
    }

    if property["type"] == "array":
        if typing_list_type == "object":
            list_type: Type[ToolParameterView] = get_args(field_info.annotation)[0]
            property["items"] = list_type.to_openapi_dict()
        else:
            property["items"] = {"type": typing_list_type}
    elif property["type"] == "object":
        if is_optional_type(field_info.annotation):
            field_type_class: Type[ToolParameterView] = get_args(field_info.annotation)[0]
        else:
            field_type_class = field_info.annotation

        openapi_dict = field_type_class.to_openapi_dict()
        property.update(openapi_dict)

    property["description"] = property.get("description", "")
    return OpenAPIProperty(**property)


class ToolParameterView(BaseModel):
    @classmethod
    def from_openapi_dict(cls, name, schema: dict) -> Type[ToolParameterView]:
        """parse openapi component schemas to ParameterView
        Args:
            response_or_returns (dict): the content of status code

        Returns:
            _type_: _description_
        """

        # TODO(wj-Mcat): to load Optional field
        fields = {}
        for field_name, field_dict in schema.get("properties", {}).items():
            field_type = python_type_from_json_type(field_dict)

            if field_type is List[ToolParameterView]:
                SubParameterView: Type[ToolParameterView] = ToolParameterView.from_openapi_dict(
                    field_name, field_dict["items"]
                )
                field_type = List[SubParameterView]  # type: ignore

            # TODO(wj-Mcat): remove supporting for `summary` field
            if "summary" in field_dict:
                description = field_dict["summary"]
                logger.info("`summary` field will be deprecated, please use `description`")

                if "description" in field_dict:
                    logger.info("`description` field will be used instead of `summary`")
                    description = field_dict["description"]
            else:
                description = field_dict.get("description", None)

            description = description or ""

            field = FieldInfo(annotation=field_type, description=description)

            # TODO(wj-Mcat): to handle list field required & not-required
            # if get_typing_list_type(field_type) is not None:
            #     field.default_factory = list

            fields[field_name] = (field_type, field)

        return create_model("OpenAPIParameterView", __base__=ToolParameterView, **fields)

    @classmethod
    def to_openapi_dict(cls) -> dict:
        """convert ParametersView to openapi spec dict

        Returns:
            dict: schema of openapi
        """

        required_names, properties = [], {}
        for field_name, field_info in cls.model_fields.items():
            if field_info.is_required() and not is_optional_type(field_info.annotation):
                required_names.append(field_name)

            properties[field_name] = dict(get_field_openapi_property(field_info))

        result = {
            "type": "object",
            "properties": properties,
        }
        if len(required_names) > 0:
            result["required"] = required_names
        result = scrub_dict(result, remove_empty_dict=True)  # type: ignore
        return result or {}

    @classmethod
    def function_call_schema(cls) -> dict:
        """get function_call schame

        Returns:
            dict: the schema of function_call
        """
        return cls.to_openapi_dict()


@dataclass
class RemoteToolView:
    uri: str
    method: str
    name: str
    description: str
    parameters: Optional[Type[ToolParameterView]] = None
    parameters_description: Optional[str] = None
    returns: Optional[Type[ToolParameterView]] = None
    returns_description: Optional[str] = None

    returns_ref_uri: Optional[str] = None
    parameters_ref_uri: Optional[str] = None

    def to_openapi_dict(self):
        result = {
            "operationId": self.name,
            "description": self.description,
        }
        if self.returns is not None:
            response = {
                "200": {
                    "description": self.returns_description,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/" + (self.returns_ref_uri or "")}
                        }
                    },
                }
            }
            result["responses"] = response

        if self.parameters is not None:
            parameters = {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/" + (self.parameters_ref_uri or "")}
                    }
                },
            }
            result["requestBody"] = parameters
        return {self.method: result}

    @staticmethod
    def from_openapi_dict(
        uri: str, method: str, path_info: dict, parameters_views: dict[str, Type[ToolParameterView]]
    ) -> RemoteToolView:
        """construct RemoteToolView from openapi spec-dict info

        Args:
            uri (str): the url path of remote tool
            method (str): http method: one of [get, post, put, delete]
            path_info (dict): the spec info of remote tool
            parameters_views (dict[str, ParametersView]):
                the dict of parameters views which are the schema of input/output of tool

        Returns:
            RemoteToolView: the instance of remote tool view
        """
        parameters_ref_uri, returns_ref_uri = None, None
        parameters, parameters_description = None, None
        if "requestBody" in path_info:
            request_ref = path_info["requestBody"]["content"]["application/json"]["schema"]["$ref"]
            parameters_ref_uri = request_ref.split("/")[-1]
            assert parameters_ref_uri in parameters_views
            parameters = parameters_views[parameters_ref_uri]
            parameters_description = path_info["requestBody"].get("description", None)

        returns, returns_description = None, None
        if "responses" in path_info:
            response_ref = list(path_info["responses"].values())[0]["content"]["application/json"]["schema"][
                "$ref"
            ]
            returns_ref_uri = response_ref.split("/")[-1]
            assert returns_ref_uri in parameters_views
            returns = parameters_views[returns_ref_uri]
            returns_description = list(path_info["responses"].values())[0].get("description", None)

        return RemoteToolView(
            name=path_info["operationId"],
            parameters=parameters,
            parameters_description=parameters_description,
            returns=returns,
            returns_description=returns_description,
            description=path_info.get("description", path_info.get("summary", None)),
            method=method,
            uri=uri,
            # save ref id info
            returns_ref_uri=returns_ref_uri,
            parameters_ref_uri=parameters_ref_uri,
        )

    def function_call_schema(self):
        inputs = {
            "name": self.name,
            "description": self.description,
            # TODO(wj-Mcat): read examples from openapi.yaml
            # "examples": [example.to_dict() for example in self.examples],
        }
        if self.parameters is not None:
            inputs["parameters"] = self.parameters.function_call_schema()  # type: ignore
        else:
            inputs["parameters"] = {"type": "object", "properties": {}}

        if self.returns is not None:
            inputs["responses"] = self.returns.function_call_schema()  # type: ignore
        return scrub_dict(inputs) or {}


@dataclass
class Endpoint:
    url: str


@dataclass
class EndpointInfo:
    title: str
    description: str
    version: str
