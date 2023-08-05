# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .appliance import *
from .appliance_definition import *
from .application import *
from .application_definition import *
from .get_appliance import *
from .get_appliance_definition import *
from .get_application import *
from .get_application_definition import *
from .get_jit_request import *
from .jit_request import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    latest,
    v20160901preview,
    v20170901,
    v20180601,
    v20190701,
    v20200821preview,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:solutions:Appliance":
                return Appliance(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:solutions:ApplianceDefinition":
                return ApplianceDefinition(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:solutions:Application":
                return Application(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:solutions:ApplicationDefinition":
                return ApplicationDefinition(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:solutions:JitRequest":
                return JitRequest(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "solutions", _module_instance)

_register_module()
