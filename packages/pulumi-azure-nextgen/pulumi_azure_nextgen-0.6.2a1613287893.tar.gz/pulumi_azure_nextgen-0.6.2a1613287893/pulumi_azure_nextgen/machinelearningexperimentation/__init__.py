# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .account import *
from .get_account import *
from .get_project import *
from .get_workspace import *
from .project import *
from .workspace import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    v20170501preview,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:machinelearningexperimentation:Account":
                return Account(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:machinelearningexperimentation:Project":
                return Project(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:machinelearningexperimentation:Workspace":
                return Workspace(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "machinelearningexperimentation", _module_instance)

_register_module()
