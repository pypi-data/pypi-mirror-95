# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .get_machine import *
from .get_machine_extension import *
from .machine import *
from .machine_extension import *
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
            if typ == "azure-nextgen:hybridcompute/latest:Machine":
                return Machine(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:hybridcompute/latest:MachineExtension":
                return MachineExtension(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "hybridcompute/latest", _module_instance)

_register_module()
