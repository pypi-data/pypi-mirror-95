# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .get_remediation_at_management_group import *
from .get_remediation_at_resource import *
from .get_remediation_at_resource_group import *
from .get_remediation_at_subscription import *
from .list_remediation_deployments_at_management_group import *
from .list_remediation_deployments_at_resource import *
from .list_remediation_deployments_at_resource_group import *
from .list_remediation_deployments_at_subscription import *
from .remediation_at_management_group import *
from .remediation_at_resource import *
from .remediation_at_resource_group import *
from .remediation_at_subscription import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    latest,
    v20180701preview,
    v20190701,
    v20210101,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:policyinsights:RemediationAtManagementGroup":
                return RemediationAtManagementGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:policyinsights:RemediationAtResource":
                return RemediationAtResource(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:policyinsights:RemediationAtResourceGroup":
                return RemediationAtResourceGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:policyinsights:RemediationAtSubscription":
                return RemediationAtSubscription(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "policyinsights", _module_instance)

_register_module()
