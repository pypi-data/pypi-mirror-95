# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .afd_custom_domain import *
from .afd_endpoint import *
from .afd_origin import *
from .afd_origin_group import *
from .custom_domain import *
from .endpoint import *
from .get_afd_custom_domain import *
from .get_afd_endpoint import *
from .get_afd_origin import *
from .get_afd_origin_group import *
from .get_custom_domain import *
from .get_endpoint import *
from .get_origin import *
from .get_origin_group import *
from .get_policy import *
from .get_profile import *
from .get_profile_supported_optimization_types import *
from .get_route import *
from .get_rule import *
from .get_rule_set import *
from .get_secret import *
from .get_security_policy import *
from .origin import *
from .origin_group import *
from .policy import *
from .profile import *
from .route import *
from .rule import *
from .rule_set import *
from .secret import *
from .security_policy import *
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
            if typ == "azure-nextgen:cdn/latest:AFDCustomDomain":
                return AFDCustomDomain(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:AFDEndpoint":
                return AFDEndpoint(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:AFDOrigin":
                return AFDOrigin(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:AFDOriginGroup":
                return AFDOriginGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:CustomDomain":
                return CustomDomain(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:Endpoint":
                return Endpoint(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:Origin":
                return Origin(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:OriginGroup":
                return OriginGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:Policy":
                return Policy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:Profile":
                return Profile(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:Route":
                return Route(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:Rule":
                return Rule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:RuleSet":
                return RuleSet(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:Secret":
                return Secret(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:cdn/latest:SecurityPolicy":
                return SecurityPolicy(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "cdn/latest", _module_instance)

_register_module()
