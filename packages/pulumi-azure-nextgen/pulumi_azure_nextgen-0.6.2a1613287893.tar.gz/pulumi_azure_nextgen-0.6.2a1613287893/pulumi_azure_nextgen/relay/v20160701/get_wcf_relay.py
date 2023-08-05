# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetWCFRelayResult',
    'AwaitableGetWCFRelayResult',
    'get_wcf_relay',
]

@pulumi.output_type
class GetWCFRelayResult:
    """
    Description of WcfRelays Resource.
    """
    def __init__(__self__, created_at=None, id=None, is_dynamic=None, listener_count=None, name=None, relay_type=None, requires_client_authorization=None, requires_transport_security=None, type=None, updated_at=None, user_metadata=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_dynamic and not isinstance(is_dynamic, bool):
            raise TypeError("Expected argument 'is_dynamic' to be a bool")
        pulumi.set(__self__, "is_dynamic", is_dynamic)
        if listener_count and not isinstance(listener_count, int):
            raise TypeError("Expected argument 'listener_count' to be a int")
        pulumi.set(__self__, "listener_count", listener_count)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if relay_type and not isinstance(relay_type, str):
            raise TypeError("Expected argument 'relay_type' to be a str")
        pulumi.set(__self__, "relay_type", relay_type)
        if requires_client_authorization and not isinstance(requires_client_authorization, bool):
            raise TypeError("Expected argument 'requires_client_authorization' to be a bool")
        pulumi.set(__self__, "requires_client_authorization", requires_client_authorization)
        if requires_transport_security and not isinstance(requires_transport_security, bool):
            raise TypeError("Expected argument 'requires_transport_security' to be a bool")
        pulumi.set(__self__, "requires_transport_security", requires_transport_security)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)
        if user_metadata and not isinstance(user_metadata, str):
            raise TypeError("Expected argument 'user_metadata' to be a str")
        pulumi.set(__self__, "user_metadata", user_metadata)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        The time the WCFRelay was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isDynamic")
    def is_dynamic(self) -> bool:
        """
        true if the relay is dynamic; otherwise, false.
        """
        return pulumi.get(self, "is_dynamic")

    @property
    @pulumi.getter(name="listenerCount")
    def listener_count(self) -> int:
        """
        The number of listeners for this relay. min : 1 and max:25 supported
        """
        return pulumi.get(self, "listener_count")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="relayType")
    def relay_type(self) -> Optional[str]:
        """
        WCFRelay Type.
        """
        return pulumi.get(self, "relay_type")

    @property
    @pulumi.getter(name="requiresClientAuthorization")
    def requires_client_authorization(self) -> Optional[bool]:
        """
        true if client authorization is needed for this relay; otherwise, false.
        """
        return pulumi.get(self, "requires_client_authorization")

    @property
    @pulumi.getter(name="requiresTransportSecurity")
    def requires_transport_security(self) -> Optional[bool]:
        """
        true if transport security is needed for this relay; otherwise, false.
        """
        return pulumi.get(self, "requires_transport_security")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        The time the namespace was updated.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="userMetadata")
    def user_metadata(self) -> Optional[str]:
        """
        usermetadata is a placeholder to store user-defined string data for the HybridConnection endpoint.e.g. it can be used to store  descriptive data, such as list of teams and their contact information also user-defined configuration settings can be stored.
        """
        return pulumi.get(self, "user_metadata")


class AwaitableGetWCFRelayResult(GetWCFRelayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWCFRelayResult(
            created_at=self.created_at,
            id=self.id,
            is_dynamic=self.is_dynamic,
            listener_count=self.listener_count,
            name=self.name,
            relay_type=self.relay_type,
            requires_client_authorization=self.requires_client_authorization,
            requires_transport_security=self.requires_transport_security,
            type=self.type,
            updated_at=self.updated_at,
            user_metadata=self.user_metadata)


def get_wcf_relay(namespace_name: Optional[str] = None,
                  relay_name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWCFRelayResult:
    """
    Use this data source to access information about an existing resource.

    :param str namespace_name: The Namespace Name
    :param str relay_name: The relay name
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['namespaceName'] = namespace_name
    __args__['relayName'] = relay_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:relay/v20160701:getWCFRelay', __args__, opts=opts, typ=GetWCFRelayResult).value

    return AwaitableGetWCFRelayResult(
        created_at=__ret__.created_at,
        id=__ret__.id,
        is_dynamic=__ret__.is_dynamic,
        listener_count=__ret__.listener_count,
        name=__ret__.name,
        relay_type=__ret__.relay_type,
        requires_client_authorization=__ret__.requires_client_authorization,
        requires_transport_security=__ret__.requires_transport_security,
        type=__ret__.type,
        updated_at=__ret__.updated_at,
        user_metadata=__ret__.user_metadata)
