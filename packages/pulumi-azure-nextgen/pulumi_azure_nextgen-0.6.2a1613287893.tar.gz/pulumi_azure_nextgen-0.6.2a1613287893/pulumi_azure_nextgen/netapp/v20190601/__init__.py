# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .account import *
from .get_account import *
from .get_pool import *
from .get_snapshot import *
from .get_volume import *
from .pool import *
from .snapshot import *
from .volume import *
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
            if typ == "azure-nextgen:netapp/v20190601:Account":
                return Account(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:netapp/v20190601:Pool":
                return Pool(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:netapp/v20190601:Snapshot":
                return Snapshot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:netapp/v20190601:Volume":
                return Volume(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "netapp/v20190601", _module_instance)

_register_module()
