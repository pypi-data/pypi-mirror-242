import copy
import json
from typing import Callable, Optional, Type, TypeVar

from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain.schema import ChatGeneration, Generation, OutputParserException
from langchain.schema.output_parser import BaseGenerationOutputParser, BaseOutputParser
from pydantic.v1 import BaseModel, ValidationError

from .types import ParserBaseModel, CodeBlock as CodeBlock

T = TypeVar("T")


class LambdaOutputParser(BaseOutputParser[T]):
    _parse: Optional[Callable[[str], T]] = None

    def parse(self, text: str) -> T:
        if self._parse is None:
            raise NotImplementedError(
                "LambdaOutputParser.lambda_parse() is not implemented"
            )
        return self._parse(text)

    @property
    def _type(self) -> str:
        return "lambda"


class BoolOutputParser(BaseOutputParser[bool]):
    def parse(self, text: str) -> bool:
        return text.strip()[:1].lower() == "y"

    def get_format_instructions(self) -> str:
        return "\nAnswer only with 'Yes' or 'No'."

    @property
    def _type(self) -> str:
        return "bool"


M = TypeVar("M", bound=BaseModel)


class MultiToolParser(BaseGenerationOutputParser[M]):
    output_types: list[Type[M]]

    def parse_result(self, result: list[Generation], *, partial: bool = False) -> M:
        function_call = self._pre_parse_function_call(result)

        output_type_names = [t.__name__.lower() for t in self.output_types]

        if function_call["name"] not in output_type_names:
            raise OutputParserException("Invalid function call")

        parser = self._get_parser_for(function_call["name"])

        return parser.parse_result(result)

    def _pre_parse_function_call(self, result: list[Generation]) -> dict:
        generation = result[0]
        if not isinstance(generation, ChatGeneration):
            raise OutputParserException(
                "This output parser can only be used with a chat generation."
            )
        message = generation.message
        try:
            func_call = copy.deepcopy(message.additional_kwargs["function_call"])
        except KeyError:
            raise OutputParserException(
                f"The model refused to respond with a function call:\n{message.content}\n\n"
            )

        return func_call

    def _get_parser_for(self, function_name: str) -> BaseGenerationOutputParser[M]:
        output_type_iter = filter(
            lambda t: t.__name__.lower() == function_name, self.output_types
        )
        if output_type_iter is None:
            raise OutputParserException(
                f"No parser found for function: {function_name}"
            )
        output_type: Type[M] = next(output_type_iter)

        return PydanticOutputFunctionsParser(pydantic_schema=output_type)


P = TypeVar("P", bound=ParserBaseModel)


class CustomPydanticOutputParser(BaseOutputParser[P]):
    pydantic_object: Type[P]

    def parse(self, text: str) -> P:
        try:
            return self.pydantic_object.parse(text)
        except (json.JSONDecodeError, ValidationError) as e:
            raise OutputParserException(
                f"Failed to parse {self.pydantic_object.__name__} from completion {text}. Got: {e}",
                llm_output=text,
            )

    def get_format_instructions(self) -> str:
        reduced_schema = self.pydantic_object.schema()
        if "title" in reduced_schema:
            del reduced_schema["title"]
        if "type" in reduced_schema:
            del reduced_schema["type"]

        return self.pydantic_object.format_instructions().format(
            schema=json.dumps(reduced_schema),
        )

    @property
    def _type(self) -> str:
        return "pydantic"
