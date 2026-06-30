from marshmallow import Schema, fields


class PermissionSchema(Schema):
    id: fields.Int = fields.Int()
    name: fields.Str = fields.Str()


class RoleSchema(Schema):
    id: fields.Int = fields.Int()
    name: fields.Str = fields.Str()

    # Nested permissions list
    permissions: fields.Nested = fields.Nested(PermissionSchema, many=True)


class UserSchema(Schema):
    id: fields.Int = fields.Int()
    email: fields.Email = fields.Email()
    name: fields.Str = fields.Str(allow_none=True)
    surname: fields.Str = fields.Str(allow_none=True)
    role: fields.Nested = fields.Nested(RoleSchema)


class MeasureSchema(Schema):
    id: fields.Int = fields.Int()
    items_per_m2: fields.Decimal = fields.Decimal(as_string=True)
    weight: fields.Decimal = fields.Decimal(as_string=True)
    area: fields.Decimal = fields.Decimal(as_string=True)

    pet: fields.Int = fields.Int()
    pead: fields.Int = fields.Int()
    pebd: fields.Int = fields.Int()
    pvc: fields.Int = fields.Int()
    pp: fields.Int = fields.Int()
    ps: fields.Int = fields.Int()
    pa: fields.Int = fields.Int()
    other: fields.Int = fields.Int()

    ihr_plata: fields.Decimal = fields.Decimal(as_string=True)
    ibirp: fields.Decimal = fields.Decimal(as_string=True)

    # Nested user info
    collaborator: fields.Nested = fields.Nested(UserSchema)


class SpotSchema(Schema):
    id: fields.Int = fields.Int()
    title: fields.Str = fields.Str()
    latitude: fields.Decimal = fields.Decimal(as_string=True)
    longitude: fields.Decimal = fields.Decimal(as_string=True)

    # Nested measures list
    measures: fields.Nested = fields.Nested(MeasureSchema, many=True)


# Schema instances

permission_schema = PermissionSchema()
permissions_schema = PermissionSchema(many=True)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

measure_schema = MeasureSchema()
measures_schema = MeasureSchema(many=True)

spot_schema = SpotSchema()
spots_schema = SpotSchema(many=True)
