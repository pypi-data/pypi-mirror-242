import boto3
import copy
import json
from botocore.exceptions import NoCredentialsError
from typing import Any, Callable, Dict, List, Union
from unittest.mock import MagicMock, Mock, PropertyMock

from rehearser.constants import (GUMMIES_INTERACTIONS_FILE_TYPE,
                                 INTERACTIONS_KEY, InteractionType,
                                 SupportedInteractionsType)
from rehearser.utils import (from_serializable_interactions,
                             get_json_or_file_path)


class MockGenerator:
    def __init__(
        self, interactions_src: Union[str, Dict[str, Any], List[Dict[str, Any]]]
    ):
        """
        Initialize the MockGenerator with interactions source.
        Args:
            interactions_src: The source of interactions, either a JSON string or a dictionary.
        """
        self.__method_interactions = {}
        self.__attribute_interactions = {}
        self.__interactions_src_type = None
        self.load_interactions_src(interactions_src)


    def load_interactions_src(self, interactions_src: Union[str, Dict[str, Any], List[Dict[str, Any]]]) -> Any:
        """"
        Load interactions source.
        
        Args:
            interactions_src: filename or a JSON string or a dictionary or an S3 bucket path.
        """
        if isinstance(interactions_src, str):
            if interactions_src.startswith('s3://'):
                # Load from S3
                s3 = boto3.client('s3')
                bucket_name, key = interactions_src[5:].split('/', 1)
                try:
                    s3_response_object = s3.get_object(Bucket=bucket_name, Key=key)
                    interactions_src = s3_response_object['Body'].read().decode('utf-8')
                except NoCredentialsError:
                    print("No AWS credentials found")
                    return
            else:
                # Load from local file if not a JSON string
                interactions_src, py_type = get_json_or_file_path(interactions_src)
                if py_type == str:
                    # it should be a file name
                    with open(interactions_src) as f:
                        interactions_src = json.load(f)
                        if not interactions_src:
                            raise Exception(f"Empty interactions file: {interactions_src}")

        # make sure interactions_src is a dictionary or list now

        if isinstance(interactions_src, dict):
            # extract interactions_src_type and the list form of interactions
            self.__interactions_src_type = interactions_src.get(
                GUMMIES_INTERACTIONS_FILE_TYPE,
                SupportedInteractionsType.PYTHON_INSTANCE.name,
            )
            if self.__interactions_src_type in (
                SupportedInteractionsType.PYTHON_INSTANCE.name,
                SupportedInteractionsType.PYTHON_CALLABLE.name,
            ):
                interactions_src = interactions_src[INTERACTIONS_KEY]
            else:
                raise Exception(
                    f"Unsupported interactions type: {interactions_src[GUMMIES_INTERACTIONS_FILE_TYPE]}"
                )
        elif isinstance(interactions_src, list):
            self.__interactions_src_type = SupportedInteractionsType.PYTHON_INSTANCE.name
            pass

        if not self.__interactions_src_type:
            raise Exception(
                f"Unsupported interactions type: {type(interactions_src)}"
            )

        # interactions_src is supposed to be a list now
        interactions = from_serializable_interactions(interactions_src)
        for interaction in interactions:
            if interaction["type"] in (
                InteractionType.INSTANCE_METHOD_CALL.name,
                InteractionType.METHOD_CALL.name,
            ):
                if interaction["name"] not in self.__method_interactions:
                    self.__method_interactions[interaction["name"]] = []
                self.__method_interactions[interaction["name"]].append(interaction)
            elif interaction["type"] == InteractionType.ATTRIBUTE_ACCESS.name:
                if interaction["name"] not in self.__attribute_interactions:
                    self.__attribute_interactions[interaction["name"]] = []
                self.__attribute_interactions[interaction["name"]].append(interaction)
        
        return self
        

    def create_mock(self) -> Union[MagicMock, Mock, Callable]:
        """
        Create a mock object based on the interactions.

        Returns:
            A mock object with methods and attributes set based on the interactions.
        """
        mock = MagicMock()

        if (
            self.__interactions_src_type
            == SupportedInteractionsType.PYTHON_INSTANCE.name
        ):
            # all methods share the same interactions log
            attr_side_effect = {}
            for attr_name, interactions in self.__attribute_interactions.items():
                attr_side_effect[attr_name] = []
                for attr_info in interactions:
                    attr_side_effect[attr_name].append(attr_info.get("result"))
            for attr_name in self.__attribute_interactions.keys():
                setattr(
                    type(mock),
                    attr_name,
                    PropertyMock(side_effect=attr_side_effect[attr_name]),
                )

            # all methods share the same interactions log
            for method_name, interactions in self.__method_interactions.items():
                setattr(
                    mock,
                    method_name,
                    Mock(side_effect=self.__get_side_effect(interactions)),
                )
            return mock
        elif (
            self.__interactions_src_type
            == SupportedInteractionsType.PYTHON_CALLABLE.name
        ):
            return Mock(side_effect=self.__get_side_effect(list(self.__method_interactions.values())[0]))


    def __get_side_effect(self, interactions: List[Dict[str, Any]]) -> Callable:
        """
        Get the side effect function for a mock method.

        Args:
            interactions: The list of interactions for the method.

        Returns:
            A function that can be used as the side effect for the mock method.
        """
        # make sure every mock created has its own copy of interactions
        _get_side_effect_interactions = copy.deepcopy(interactions)

        def side_effect(*args: Any, **kwargs: Any) -> Any:
            """
            The side effect function for the mock method.
            """
            if not _get_side_effect_interactions:
                raise StopIteration
            interaction = _get_side_effect_interactions.pop(0)
            if "result" in interaction:
                result = interaction["result"]
                # if result is a mock, make sure it has __enter__ and __exit__ methods just in case it is used as a context manager
                if isinstance(result, Mock):
                    result.__enter__ = Mock(return_value=result)
                    result.__exit__ = Mock(return_value=None)                
                return result
            elif "exception" in interaction:
                raise interaction["exception"]

        return side_effect
