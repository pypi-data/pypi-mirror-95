# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = [
    'GetInterfaceEndpointResult',
    'AwaitableGetInterfaceEndpointResult',
    'get_interface_endpoint',
]

@pulumi.output_type
class GetInterfaceEndpointResult:
    """
    Interface endpoint resource.
    """
    def __init__(__self__, endpoint_service=None, etag=None, fqdn=None, id=None, location=None, name=None, network_interfaces=None, owner=None, provisioning_state=None, subnet=None, tags=None, type=None):
        if endpoint_service and not isinstance(endpoint_service, dict):
            raise TypeError("Expected argument 'endpoint_service' to be a dict")
        pulumi.set(__self__, "endpoint_service", endpoint_service)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        pulumi.set(__self__, "fqdn", fqdn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError("Expected argument 'network_interfaces' to be a list")
        pulumi.set(__self__, "network_interfaces", network_interfaces)
        if owner and not isinstance(owner, str):
            raise TypeError("Expected argument 'owner' to be a str")
        pulumi.set(__self__, "owner", owner)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if subnet and not isinstance(subnet, dict):
            raise TypeError("Expected argument 'subnet' to be a dict")
        pulumi.set(__self__, "subnet", subnet)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="endpointService")
    def endpoint_service(self) -> Optional['outputs.EndpointServiceResponse']:
        """
        A reference to the service being brought into the virtual network.
        """
        return pulumi.get(self, "endpoint_service")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Gets a unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[str]:
        """
        A first-party service's FQDN that is mapped to the private IP allocated via this interface endpoint.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Sequence['outputs.NetworkInterfaceResponse']:
        """
        Gets an array of references to the network interfaces created for this interface endpoint.
        """
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter
    def owner(self) -> str:
        """
        A read-only property that identifies who created this interface endpoint.
        """
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the interface endpoint. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def subnet(self) -> Optional['outputs.SubnetResponse']:
        """
        The ID of the subnet from which the private IP will be allocated.
        """
        return pulumi.get(self, "subnet")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetInterfaceEndpointResult(GetInterfaceEndpointResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInterfaceEndpointResult(
            endpoint_service=self.endpoint_service,
            etag=self.etag,
            fqdn=self.fqdn,
            id=self.id,
            location=self.location,
            name=self.name,
            network_interfaces=self.network_interfaces,
            owner=self.owner,
            provisioning_state=self.provisioning_state,
            subnet=self.subnet,
            tags=self.tags,
            type=self.type)


def get_interface_endpoint(expand: Optional[str] = None,
                           interface_endpoint_name: Optional[str] = None,
                           resource_group_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInterfaceEndpointResult:
    """
    Use this data source to access information about an existing resource.

    :param str expand: Expands referenced resources.
    :param str interface_endpoint_name: The name of the interface endpoint.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['interfaceEndpointName'] = interface_endpoint_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:network/v20181201:getInterfaceEndpoint', __args__, opts=opts, typ=GetInterfaceEndpointResult).value

    return AwaitableGetInterfaceEndpointResult(
        endpoint_service=__ret__.endpoint_service,
        etag=__ret__.etag,
        fqdn=__ret__.fqdn,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        network_interfaces=__ret__.network_interfaces,
        owner=__ret__.owner,
        provisioning_state=__ret__.provisioning_state,
        subnet=__ret__.subnet,
        tags=__ret__.tags,
        type=__ret__.type)
