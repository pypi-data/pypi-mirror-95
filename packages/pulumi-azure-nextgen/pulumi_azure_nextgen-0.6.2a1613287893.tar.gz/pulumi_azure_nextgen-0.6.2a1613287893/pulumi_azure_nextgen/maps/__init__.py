# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .account import *
from .creator import *
from .get_account import *
from .get_creator import *
from .get_private_atlase import *
from .list_account_keys import *
from .private_atlase import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    latest,
    v20170101preview,
    v20180501,
    v20200201preview,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:maps:Account":
                return Account(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:maps:Creator":
                return Creator(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:maps:PrivateAtlase":
                return PrivateAtlase(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "maps", _module_instance)

_register_module()
