r"""
Copyright &copy; 2023 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CifsServiceDelete", "CifsServiceDeleteSchema"]
__pdoc__ = {
    "CifsServiceDeleteSchema.resource": False,
    "CifsServiceDeleteSchema.opts": False,
    "CifsServiceDelete": False,
}


class CifsServiceDeleteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsServiceDelete object"""

    ad_domain = marshmallow_fields.Nested("netapp_ontap.models.ad_domain_delete.AdDomainDeleteSchema", unknown=EXCLUDE, data_key="ad_domain", allow_none=True)
    r""" The ad_domain field of the cifs_service_delete. """

    @property
    def resource(self):
        return CifsServiceDelete

    gettable_fields = [
        "ad_domain",
    ]
    """ad_domain,"""

    patchable_fields = [
        "ad_domain",
    ]
    """ad_domain,"""

    postable_fields = [
        "ad_domain",
    ]
    """ad_domain,"""


class CifsServiceDelete(Resource):

    _schema = CifsServiceDeleteSchema
