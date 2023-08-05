# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .consumer_group import *
from .event_hub import *
from .event_hub_authorization_rule import *
from .get_consumer_group import *
from .get_event_hub import *
from .get_event_hub_authorization_rule import *
from .get_namespace import *
from .get_namespace_authorization_rule import *
from .list_event_hub_keys import *
from .list_namespace_keys import *
from .namespace import *
from .namespace_authorization_rule import *
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
            if typ == "azure-nextgen:eventhub/v20150801:ConsumerGroup":
                return ConsumerGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:eventhub/v20150801:EventHub":
                return EventHub(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:eventhub/v20150801:EventHubAuthorizationRule":
                return EventHubAuthorizationRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:eventhub/v20150801:Namespace":
                return Namespace(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:eventhub/v20150801:NamespaceAuthorizationRule":
                return NamespaceAuthorizationRule(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "eventhub/v20150801", _module_instance)

_register_module()
