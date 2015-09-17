from marshmallow import Schema, fields


class EveApiKeySerializer(Schema):
    id = fields.Integer()

    key_id = fields.Integer()
    vcode = fields.String()

    status = fields.String()
    access_mask = fields.Integer()
    key_type = fields.String()

    expires = fields.DateTime()
    deleted = fields.Boolean()
