# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .connector import *
from .connector_mapping import *
from .get_connector import *
from .get_connector_mapping import *
from .get_hub import *
from .get_image_upload_url_for_data import *
from .get_image_upload_url_for_entity_type import *
from .get_kpi import *
from .get_link import *
from .get_profile import *
from .get_relationship import *
from .get_relationship_link import *
from .get_role_assignment import *
from .get_view import *
from .hub import *
from .kpi import *
from .link import *
from .profile import *
from .relationship import *
from .relationship_link import *
from .role_assignment import *
from .view import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from ... import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:customerinsights/v20170101:Connector":
                return Connector(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:customerinsights/v20170101:ConnectorMapping":
                return ConnectorMapping(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:customerinsights/v20170101:Hub":
                return Hub(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:customerinsights/v20170101:Kpi":
                return Kpi(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:customerinsights/v20170101:Link":
                return Link(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:customerinsights/v20170101:Profile":
                return Profile(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:customerinsights/v20170101:Relationship":
                return Relationship(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:customerinsights/v20170101:RelationshipLink":
                return RelationshipLink(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:customerinsights/v20170101:RoleAssignment":
                return RoleAssignment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:customerinsights/v20170101:View":
                return View(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "customerinsights/v20170101", _module_instance)

_register_module()
