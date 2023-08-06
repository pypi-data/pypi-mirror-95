"""GraphQL directives for the auth app."""

from ariadne import SchemaDirectiveVisitor
from graphql import default_field_resolver
from graphql.type.definition import GraphQLNonNull

from turbulette.exceptions import SchemaError
from turbulette.utils import is_query

from .decorators import access_token_required, fresh_token_required, scope_required


class AccessTokenRequiredDirective(SchemaDirectiveVisitor):
    """Require a valid access token."""

    name = "access_token_required"

    def visit_field_definition(
        self, field, object_type
    ):  # pylint: disable=unused-argument
        original_resolver = field.resolve or default_field_resolver

        @access_token_required
        async def resolve_login_required(obj, info, **kwargs):
            return await original_resolver(obj, info, **kwargs)

        field.resolve = resolve_login_required
        return field


class FreshTokenRequiredDirective(SchemaDirectiveVisitor):
    """Require a valid fresh token."""

    name = "fresh_token_required"

    def visit_field_definition(
        self, field, object_type
    ):  # pylint: disable=unused-argument
        original_resolver = field.resolve or default_field_resolver

        @fresh_token_required
        async def resolve_fresh_token_required(obj, info, **kwargs):
            return await original_resolver(obj, info, **kwargs)

        field.resolve = resolve_fresh_token_required
        return field


class PolicyDirective(SchemaDirectiveVisitor):
    """Tell Turbulette to evaluate the policy schema for this field."""

    name = "policy"

    def visit_field_definition(
        self, field, object_type
    ):  # pylint: disable=unused-argument
        original_resolver = field.resolve or default_field_resolver

        if isinstance(field.type, GraphQLNonNull):
            raise SchemaError("Fields with @policy directive cannot be non-null")

        @scope_required
        async def resolve_scope(obj, info, **kwargs):
            if is_query(info):
                return await original_resolver(obj, info, **kwargs)
            return original_resolver(obj, info, **kwargs)

        field.resolve = resolve_scope
        return field
