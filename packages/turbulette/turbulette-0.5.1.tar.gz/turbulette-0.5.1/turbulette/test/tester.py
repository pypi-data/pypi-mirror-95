"""Test helper to make resolver testing more convenient."""

from importlib import import_module
from typing import Any, Dict, List

from ariadne import graphql
from ariadne.types import GraphQLResult, GraphQLSchema

from turbulette import conf
from turbulette.errors import ErrorCode, error_formatter
from turbulette.extensions import PolicyExtension


class TestRequest:
    def __init__(self, headers: dict = None, jwt: str = None):
        # Need to import here to make sure that settings are initialized
        settings = getattr(import_module("turbulette.conf"), "settings")

        self.headers = {} if not headers else headers
        if jwt:
            self.headers["authorization"] = f"{settings.JWT_PREFIX} {jwt}"


class Tester:
    """Helper class to test GraphQL queries against the GraphQL schema."""

    def __init__(self, schema: GraphQLSchema):
        self.schema = schema
        self.error_field = conf.settings.ERROR_FIELD

    async def query(
        self,
        query: str,
        variables: dict = None,
        op_name: str = None,
        headers: dict = None,
        jwt: str = None,
    ) -> GraphQLResult:
        return await graphql(
            self.schema,
            data={"query": query, "variables": variables, "operationName": op_name},
            context_value={"request": TestRequest(headers, jwt)},
            debug=True,
            error_formatter=error_formatter,
            extensions=[PolicyExtension],
        )

    async def assert_query_success(
        self,
        query: str,
        op_name: str,
        variables: dict = None,
        headers: dict = None,
        jwt: str = None,
        op_errors=False,
        error_codes: List[ErrorCode] = None,
    ) -> GraphQLResult:
        """Assert True if the GraphQL query succeeds.

        With default params, the query succeeds if:

        - Request status is `200`
        - GraphQL `errors` array is **not** present
        - The name of the GraphQL operation is in the response at the top level

        Additional options can be used to assert specific results :

        Args:
            query: The GraphQL query to execute
            op_name: The name of the GraphQL operation
            variables: Operation variables.
            headers: Request headers.
            jwt: JWT (must be formatted as `prefix token`).
            op_errors: If `True`, will assert the presence of the error
                field (defined by the `ERROR_FIELD` setting) in operation response data.
            error_codes: List of error codes that must be present in the response.

        Returns:
            Ariadne's GraphQLResult object response
        """
        response = await self.query(query, variables, op_name, headers, jwt)
        self.assert_status_200(response)
        self.assert_no_errors(response)
        assert response[1]["data"][op_name]
        if error_codes:
            for val in list(response[1]["extensions"].values()):
                if isinstance(val, dict):
                    assert any(code.name in val for code in error_codes)
        if op_errors:
            assert response[1]["data"][op_name][self.error_field]
        else:
            # If no errors, will assert to None
            assert not response[1]["data"][op_name].get(self.error_field)
        return response

    async def assert_query_failed(
        self,
        query: str,
        op_name: str,
        variables: dict = None,
        headers: dict = None,
        jwt: str = None,
        errors: bool = True,
        error_codes: List[ErrorCode] = None,
        raises: ErrorCode = None,
    ) -> GraphQLResult:
        """Assert True if the GraphQL query fails.

        With default params, the query fails if:

        - Request status is `200` (we test the query execution, not the HTTP request)
        - GraphQL `errors` array **is** present
        - The name of the GraphQL operation is **not** in the operation response data

        Additional options can be used to assert specific results :

        Args:
            query: The GraphQL query to execute
            op_name: The name of the GraphQL operation
            variables: Operation variables.
            headers: Request headers.
            jwt: JWT (must be formatted as `prefix token`).
            errors: Assert that the response data contains the GraphQL `errors` array
            error_codes: List of error codes that must be present in the response.
            raises ErrorCode: Error code that must be present
                                 in `["extension"]["code"]`.

        Returns:
            Ariadne's GraphQLResult object response
        """
        response = await self.query(query, variables, op_name, headers, jwt)
        self.assert_status_200(response)
        if errors:
            self.assert_errors(response)
        if response[1]["data"]:
            assert not response[1]["data"][op_name]
        if raises:
            assert (
                raises.name
                in response[1]["errors"][0]["extensions"][
                    conf.settings.TURBULETTE_ERROR_KEY
                ]
            )
        if error_codes:
            for val in list(response[1]["extensions"].values()):
                if isinstance(val, dict):
                    assert any(code.name in val for code in error_codes)
        return response

    def assert_status_200(self, response: GraphQLResult):
        assert response[0]

    def assert_no_errors(self, response: GraphQLResult):
        assert self.error_field not in response[1]

    def assert_errors(self, response: GraphQLResult):
        assert self.error_field in response[1]

    @classmethod
    def assert_data_in_response(cls, response: dict, data: Dict[str, Any]):
        """Assert that the response contains the specified data dict.

        Args:
            response (dict): Response data to check
            data (Dict[str, Any]): Data that should be present in `response`
        """
        for key, value in data.items():
            if key in response:
                assert response[key] == value
