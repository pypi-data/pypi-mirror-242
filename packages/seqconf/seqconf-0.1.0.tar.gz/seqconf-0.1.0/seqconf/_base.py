from __future__ import annotations

import os
import io
import csv
import yaml
import json
import toml
import requests
import pydantic
from urllib import parse
from requests import HTTPError
from pydantic import (
    Field, Extra, root_validator)
from typing import Literal, Union, get_origin
from abc import ABC, abstractmethod
from pathlib import Path


def extract(
    data: dict,
    template: dict,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False
):
    class HelpClass(pydantic.BaseModel):
        data: dict | list
    
    help_instance = HelpClass(data=data)
    template = {'data': template}
    return help_instance.model_dump(
            include = dict(template),
            by_alias = by_alias,
            exclude_unset = exclude_unset,
            exclude_defaults = exclude_defaults,
            exclude_none = exclude_none,
            warnings = True
    )['data']

def combine_data(
    primary_data: dict | list,
    secondary_data: dict | list
) -> dict | list:
    if not secondary_data:
        return primary_data
    if not primary_data:
        return secondary_data
    type_a = type(primary_data)
    type_b = type(secondary_data)
    if type_a != type_b:
        raise TypeError(
            f"types '{type_a}' and ''{type_b} are not compatible")
    if isinstance(primary_data, list):
        return primary_data + secondary_data
    elif isinstance(primary_data, dict):
        return primary_data | secondary_data
    raise TypeError(f"type '{type_a}' can not be merged")


def _transform(input):
    if isinstance(input, dict):
        for key, value in input.items():
            if key == '__env__':
                return os.getenv(value)
            if key == '__input__':
                return InputData(**value).read()
    return input


class BaseModel(pydantic.BaseModel):
    """The Base Model is an extension for config parsing. The pydantic 
    validator _convert_env will be executed before an object is initialized. 
    The _transform function will search for dunder fields like:
    __env__
    In that case you can read content from a different localization.
    E.g. in the following example the name attribute is set to test
    
    .. code-block:: python
        {"name": "test"}
    
    If the attribute should be set to a specific environment variable, this is 
    how it is set

    .. code-block:: python
        {"name": {"__env__": "name"}}
    """

    type: str = None

    _convert_env = pydantic.validator(
        '*', pre=True, allow_reuse=True)(_transform)

    @root_validator(pre=True)
    def type_validator(cls, values):
        """in order to have the ability to differentiate between the different 
        models and have a much more generic way to do this, this function will 
        validate a given configuration and selection of models. In case that 
        the inheriting class has the Literal set for the type field or in the 
        given configuration no type field is set, the validation should be 
        handled by the native pydantic validator.
        If a type field is set within the configuration and the type field is 
        not a Literal, we will validate the type field against the given class 
        name

        :param values: configuration (dict)
        :type values: dict
        :raises ValidationError: if the given type name is not equal to the 
            class name
        :return: returns the unchanged configuration
        :rtype: dict
        """
        if isinstance(values, dict):
            if value_type := values.get('type'):
                if annotation := cls.model_fields['type'].annotation:
                    if get_origin(annotation) is Literal:
                        return values
                if value_type != cls.__name__:
                    raise ValueError(f"type name {value_type} != {cls.__name__}")
        return values

    class Config:
        extra = Extra.forbid

    def get_fields(self, exclude=set()):
        return self.model_dump(
            exclude = ({"type"} | exclude),
            exclude_none = True,
            exclude_unset = True
        )


class BaseTask(BaseModel, ABC):
    """The base task which inherits from the BaseModel and expects the execute 
    method"""

    name: str = None
    needs: str | list[str] = None

    @abstractmethod
    def execute(self, input: any = None) -> any:
        return input

class BaseStream(BaseTask, ABC):

    @abstractmethod
    def execute(self, input: any = None) -> list[io.IOBase]:
        ...

class FileStream(BaseStream):

    name: Path
    buffering: int = -1
    encoding: str = None
    errors: str = None
    newline: str = None

    def open(self, mode: str):
        return self.name.open(
            mode,
            buffering = self.buffering,
            encoding = self.encoding,
            errors = self.errors,
            newline = self.newline
        )

class FileStreamWriter(FileStream):

    mkdir: bool = False

    def execute(self) -> list[io.IOBase]:
        parent = self.name.absolute().parent
        if not parent.exists() and self.mkdir:
            parent.mkdir(parents=True)
        return [self.open('w+')]

class FileStreamReader(FileStream):

    def execute(self) -> list[io.IOBase]:
        return [self.open('r')]

class GitlabStream(BaseStream):

    name: str
    base_url: str
    project_id: int
    token: str
    ref: str = "main"
    proxies: dict = None
    exist: bool = True

    def get_head(self):
        response = self.request('head')
        response.raise_for_status()
        return response.json()
    
    def does_exist(self):
        if self.exist:
            return self.exist

        try:
            self.get_head()
            return True
        except HTTPError as ex:
            return False

    def get_url(self):
        project_url = f"{self.base_url}/api/v4/projects/{self.project_id}/"
        encoded_file_path = parse.quote(self.name, safe="")
        return f"{project_url}repository/files/{encoded_file_path}"

    def request(
        self,
        method: str,
        sub_url: str = None,
        **kwargs
    ):
        headers = kwargs.setdefault('headers', {})
        headers['Authorization'] = f"Bearer {self.token}"

        params = kwargs.setdefault('params', {})
        params['ref'] = self.ref

        kwargs.setdefault('proxies', self.proxies)

        return requests.request(
            method,
            self.get_url() + (sub_url or ""),
            **kwargs
        )


class GitlabStreamReader(GitlabStream):

    def open(self) -> io.BytesIO:
        response = self.request('get', '/raw')
        response.raise_for_status()
        return io.BytesIO(response.content)

    def execute(self, input: any = None) -> list[io.IOBase]:
        return [self.open()]


class GitlabStreamWriter(GitlabStream):
    """Write a Stream into an Gitlab File"""

    # see https://docs.gitlab.com/ee/api/repository_files.html
    author_name: str = None
    author_email: str = None
    encoding: str = None
    execute_filemode: bool = None
    last_commit_id: str = None
    start_branch: str = None
    commit_message: str = None

    _stream: io.StringIO = None

    def write(self, input: any = None):
        fields = set(
            field for field in self.__class__.__annotations__.keys()
            if not field.startswith("_"))
        data = self.model_dump(include=fields, exclude_unset=True)
        data['content'] = input
        data['branch'] = self.ref

        if not self.commit_message:
            data['commit_message'] = "Gitlab Stream Writer"

        http_method = "put" if self.does_exist() else "post"
        response = self.request(http_method, json = data)
        response.raise_for_status()
        return input

    def __enter__(self):
        self._stream = io.StringIO()
        return self._stream

    def __exit__(self, type, value, traceback):
        self.write(self._stream.getvalue())

    def execute(self, input: any = None):
        return [self]


class BaseFile(BaseTask, ABC):
    """Basic implementation to define files"""

    directory: Path = Field(
        None,
        title = "directory",
        description = "define the directory"
    )

    def get_files(self) -> list[Path]:
        return

    def read_data(self) -> any:
        return

    def get_paths(self) -> list[Path]:
        if not self.directory:
            return self.get_files()
        return [self.directory / path for path in self.get_files()]

    def execute(self, input: any = None) -> any:
        return super().execute(self.get_paths())


class SingleFile(BaseFile):
    """Implementation to define a single file"""

    name: Path = Field(
        title = "file name",
        description = "define the file name"
    )

    def get_files(self) -> list[Path]:
        return [self.name]


class MultipleFiles(BaseFile):
    """Implementation to define multiple files"""

    names: list[Path] = Field(
        title = "file names",
        description = "define a list of file names"
    )

    def get_files(self) -> list[Path]:
        return self.names


class MultipleRegexFiles(BaseFile):
    """Implementation to define multiple file by regular expression
    TODO: Not implemented yet"""

    expression: str = Field(
        title = "expression",
        description = "define a regular expression to find the files",
    )

    def get_files(self) -> list[Path]:
        raise NotImplementedError()


class ParameterizedFile(SingleFile):
    """Implementation to define multiple file by passed parameter expression"""

    name: Path

    def get_paramezerized_file(self, *args, **kwargs) -> Path:
        formatted_path = str(self.name.absolute()).format(*args, **kwargs)
        return Path(formatted_path)


class BaseReader(BaseTask):
    """Basic implementation to read data from a file"""

    buffering: int = -1
    encoding: str = None
    newline: str = None

    @abstractmethod
    def read(self, stream_io: io.IOBase):
        ...

    def execute(self, stream_io: io.IOBase) -> any:
        data = self.read(stream_io)
        return super().execute(data)

    def get_fields(self, exclude=set()):
        return super().get_fields(
            {"buffering", "encoding", "newline"} | exclude)


class JsonReader(BaseReader):
    """Implementation to read data from a json file"""

    type: Literal["json"]

    def read(self, stream_io: io.IOBase):
        data = None
        with stream_io as stream:
            data = json.load(stream)
        return data


class YamlReader(BaseReader):
    """Implementation to read data from a yaml file"""
    
    type: Literal["yaml"]

    def read(self, stream_io: io.IOBase):
        data = None
        with stream_io as stream:
            data = yaml.load(stream, yaml.loader.SafeLoader)
        return data


class TextReader(BaseReader):
    """Implementation to read data from a text file"""

    type: Literal["text"]

    def read(self, stream_io: io.IOBase):
        data = None
        with stream_io as stream:
            data = stream.read()
        return str(data, encoding=self.encoding)


class CsvReader(TextReader):
    """Implementation to read data from a csv file."""

    type: Literal["csv"]
    fieldnames: list[str] = None
    dialect: str = None
    delimiter: str = ","
    quotechar: str = '"'
    escapechar: str = None
    doublequote: bool = None
    skipinitialspace: bool = None
    lineterminator: str = None
    strict: bool = None

    def read(self, stream_io: io.IOBase):
        content = super().read(stream_io)
        options = self.get_fields()
        reader = csv.DictReader(
            content.split(self.newline),
            **options
        )
        return [row for row in reader]


class TomlReader(BaseReader):
    """Implementation to read data from a toml file"""

    type: Literal["toml"]

    def read(self, stream_io: io.IOBase):
        data = None
        with stream_io as stream:
            data = toml.load(stream)
        return data

class BaseStreamWriter(BaseTask, ABC):

    def write(self, data, stream_io: io.IOBase):
        with stream_io as stream:
            stream.write(data)

    def execute(self, data, stream_io: io.IOBase) -> any:
        return self.write(data, stream_io)

class BaseFileWriter(BaseFile, ABC):
    """Basic implementation to write data from a file"""

    buffering: int = -1
    encoding: str = None
    newline: str = None

    mkdir: bool = False

    def open(self, path: Path):
        parent = path.absolute().parent
        if not parent.exists() and self.mkdir:
            parent.mkdir(parents=True)

        return path.open(
            mode = "w+",
            buffering = self.buffering,
            encoding = self.encoding,
            newline = self.newline
        )

    def execute(self, input: any = None) -> any:
        return


class JsonWriter(BaseStreamWriter):
    """Implementation to write data to a json file"""

    type: Literal["json"]
    skipkeys: bool = False
    indent: int | None = 4

    def write(self, data, stream_io: io.IOBase):
        with stream_io as stream:
            json.dump(data, stream, skipkeys=self.skipkeys, indent=self.indent)


class YamlWriter(BaseStreamWriter):
    """Implementation to write data to a yaml file"""

    type: Literal["yaml"]

    def write(self, data, stream_io: io.IOBase):
        with stream_io as stream:
            yaml.dump(data, stream)


class TextWriter(BaseStreamWriter):
    """Implementation to write data to a text file"""

    type: Literal["text"]

    def write(self, data, stream_io: io.IOBase):
        with stream_io as stream:
            stream.write(data)


class CsvWriter(BaseStreamWriter):
    """Implementation to write data to a csv file
    TODO: read not implemented yet"""

    type: Literal["csv"]

    def write(self, data, stream_io: io.IOBase):
        with stream_io as stream:
            raise NotImplementedError()


class TomlWriter(BaseStreamWriter):
    """Implementation to write data to a toml file"""

    type: Literal["toml"]

    def write(self, data, stream_io: io.IOBase):
        with stream_io as stream:
            toml.dump(data, stream)


class RawData(BaseTask):

    raw_data: Union[dict, list]

    def execute(self, input: any = None) -> any:
        data = combine_data(input, self.raw_data)
        return data

class InputData(BaseTask):
    """Defines input data. This can be raw data and or data read from a single 
    or multiple files"""

    stream: Union[
        FileStreamReader,
        GitlabStreamReader
    ]

    reader: Union[
        JsonReader,
        YamlReader,
        TomlReader,
        CsvReader
    ]

    def read(self):
        data = None
        stream_ios = self.stream.execute()
        for stream_io in stream_ios:
            read_data = self.reader.read(stream_io)
            data = combine_data(data, read_data)
        return data

    def execute(self, input: any = None) -> any:
        data = combine_data(input, self.read())
        return data


class DataExtractor(BaseTask):
    """Defines a template data"""

    template: InputData | RawData

    by_alias: bool = Field(default=False)
    exclude_none: bool = Field(default=False)
    exclude_unset: bool = Field(default=False)
    exclude_defaults: bool = Field(default=False)

    def model_extract(self, model: BaseModel):
        return model.model_dump(
            include = self.template.execute(),
            by_alias = self.by_alias,
            exclude_unset = self.exclude_unset,
            exclude_defaults = self.exclude_defaults,
            exclude_none = self.exclude_none
        )

    def extract(self, data: dict):
        return extract(
            data,
            self.template.execute(),
            self.by_alias,
            self.exclude_unset,
            self.exclude_defaults,
            self.exclude_none,
        )

    def execute(self, input: any = None) -> any:
        data = self.extract(input)
        return super().execute(data)


class OutputData(BaseTask):

    stream: FileStreamWriter | GitlabStreamWriter

    writer: Union[
        JsonWriter,
        YamlWriter,
        TomlWriter
    ]

    def execute(self, input: any = None) -> any:
        for stream_io in self.stream.execute():
            self.writer.execute(input, stream_io)
        return super().execute(input)
