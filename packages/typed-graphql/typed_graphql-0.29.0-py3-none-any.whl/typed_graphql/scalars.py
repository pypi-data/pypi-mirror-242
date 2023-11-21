from graphql.type import scalars, GraphQLScalarType


def newtype_to_scalar(t) -> GraphQLScalarType:
    if t.__supertype__ is int:
        return GraphQLScalarType(
            name=t.__name__,
            # description=
            serialize=scalars.serialize_int,
            parse_value=scalars.coerce_int,
            parse_literal=scalars.parse_int_literal,
        )
    elif t.__supertype__ is str:
        return GraphQLScalarType(
            name=t.__name__,
            serialize=scalars.serialize_string,
            parse_value=scalars.coerce_string,
            parse_literal=scalars.parse_string_literal,
        )
    elif t.__supertype__ is bool:
        return GraphQLScalarType(
            name=t.__name__,
            serialize=scalars.serialize_boolean,
            parse_value=scalars.coerce_boolean,
            parse_literal=scalars.parse_boolean_literal,
        )
    elif t.__supertype__ is float:
        return GraphQLScalarType(
            name=t.__name__,
            serialize=scalars.serialize_float,
            parse_value=scalars.coerce_float,
            parse_literal=scalars.parse_float_literal,
        )
    else:
        raise Exception(f"Unknown scalar type: {t.__supertype__}")
