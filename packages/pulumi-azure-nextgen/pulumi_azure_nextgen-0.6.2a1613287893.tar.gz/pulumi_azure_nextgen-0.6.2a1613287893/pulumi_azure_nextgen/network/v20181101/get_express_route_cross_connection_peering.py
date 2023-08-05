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
    'GetExpressRouteCrossConnectionPeeringResult',
    'AwaitableGetExpressRouteCrossConnectionPeeringResult',
    'get_express_route_cross_connection_peering',
]

@pulumi.output_type
class GetExpressRouteCrossConnectionPeeringResult:
    """
    Peering in an ExpressRoute Cross Connection resource.
    """
    def __init__(__self__, azure_asn=None, etag=None, gateway_manager_etag=None, id=None, ipv6_peering_config=None, last_modified_by=None, microsoft_peering_config=None, name=None, peer_asn=None, peering_type=None, primary_azure_port=None, primary_peer_address_prefix=None, provisioning_state=None, secondary_azure_port=None, secondary_peer_address_prefix=None, shared_key=None, state=None, vlan_id=None):
        if azure_asn and not isinstance(azure_asn, int):
            raise TypeError("Expected argument 'azure_asn' to be a int")
        pulumi.set(__self__, "azure_asn", azure_asn)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if gateway_manager_etag and not isinstance(gateway_manager_etag, str):
            raise TypeError("Expected argument 'gateway_manager_etag' to be a str")
        pulumi.set(__self__, "gateway_manager_etag", gateway_manager_etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ipv6_peering_config and not isinstance(ipv6_peering_config, dict):
            raise TypeError("Expected argument 'ipv6_peering_config' to be a dict")
        pulumi.set(__self__, "ipv6_peering_config", ipv6_peering_config)
        if last_modified_by and not isinstance(last_modified_by, str):
            raise TypeError("Expected argument 'last_modified_by' to be a str")
        pulumi.set(__self__, "last_modified_by", last_modified_by)
        if microsoft_peering_config and not isinstance(microsoft_peering_config, dict):
            raise TypeError("Expected argument 'microsoft_peering_config' to be a dict")
        pulumi.set(__self__, "microsoft_peering_config", microsoft_peering_config)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if peer_asn and not isinstance(peer_asn, float):
            raise TypeError("Expected argument 'peer_asn' to be a float")
        pulumi.set(__self__, "peer_asn", peer_asn)
        if peering_type and not isinstance(peering_type, str):
            raise TypeError("Expected argument 'peering_type' to be a str")
        pulumi.set(__self__, "peering_type", peering_type)
        if primary_azure_port and not isinstance(primary_azure_port, str):
            raise TypeError("Expected argument 'primary_azure_port' to be a str")
        pulumi.set(__self__, "primary_azure_port", primary_azure_port)
        if primary_peer_address_prefix and not isinstance(primary_peer_address_prefix, str):
            raise TypeError("Expected argument 'primary_peer_address_prefix' to be a str")
        pulumi.set(__self__, "primary_peer_address_prefix", primary_peer_address_prefix)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if secondary_azure_port and not isinstance(secondary_azure_port, str):
            raise TypeError("Expected argument 'secondary_azure_port' to be a str")
        pulumi.set(__self__, "secondary_azure_port", secondary_azure_port)
        if secondary_peer_address_prefix and not isinstance(secondary_peer_address_prefix, str):
            raise TypeError("Expected argument 'secondary_peer_address_prefix' to be a str")
        pulumi.set(__self__, "secondary_peer_address_prefix", secondary_peer_address_prefix)
        if shared_key and not isinstance(shared_key, str):
            raise TypeError("Expected argument 'shared_key' to be a str")
        pulumi.set(__self__, "shared_key", shared_key)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if vlan_id and not isinstance(vlan_id, int):
            raise TypeError("Expected argument 'vlan_id' to be a int")
        pulumi.set(__self__, "vlan_id", vlan_id)

    @property
    @pulumi.getter(name="azureASN")
    def azure_asn(self) -> int:
        """
        The Azure ASN.
        """
        return pulumi.get(self, "azure_asn")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="gatewayManagerEtag")
    def gateway_manager_etag(self) -> Optional[str]:
        """
        The GatewayManager Etag.
        """
        return pulumi.get(self, "gateway_manager_etag")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipv6PeeringConfig")
    def ipv6_peering_config(self) -> Optional['outputs.Ipv6ExpressRouteCircuitPeeringConfigResponse']:
        """
        The IPv6 peering configuration.
        """
        return pulumi.get(self, "ipv6_peering_config")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        Gets whether the provider or the customer last modified the peering.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="microsoftPeeringConfig")
    def microsoft_peering_config(self) -> Optional['outputs.ExpressRouteCircuitPeeringConfigResponse']:
        """
        The Microsoft peering configuration.
        """
        return pulumi.get(self, "microsoft_peering_config")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="peerASN")
    def peer_asn(self) -> Optional[float]:
        """
        The peer ASN.
        """
        return pulumi.get(self, "peer_asn")

    @property
    @pulumi.getter(name="peeringType")
    def peering_type(self) -> Optional[str]:
        """
        The peering type.
        """
        return pulumi.get(self, "peering_type")

    @property
    @pulumi.getter(name="primaryAzurePort")
    def primary_azure_port(self) -> str:
        """
        The primary port.
        """
        return pulumi.get(self, "primary_azure_port")

    @property
    @pulumi.getter(name="primaryPeerAddressPrefix")
    def primary_peer_address_prefix(self) -> Optional[str]:
        """
        The primary address prefix.
        """
        return pulumi.get(self, "primary_peer_address_prefix")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Gets the provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="secondaryAzurePort")
    def secondary_azure_port(self) -> str:
        """
        The secondary port.
        """
        return pulumi.get(self, "secondary_azure_port")

    @property
    @pulumi.getter(name="secondaryPeerAddressPrefix")
    def secondary_peer_address_prefix(self) -> Optional[str]:
        """
        The secondary address prefix.
        """
        return pulumi.get(self, "secondary_peer_address_prefix")

    @property
    @pulumi.getter(name="sharedKey")
    def shared_key(self) -> Optional[str]:
        """
        The shared key.
        """
        return pulumi.get(self, "shared_key")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The peering state.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="vlanId")
    def vlan_id(self) -> Optional[int]:
        """
        The VLAN ID.
        """
        return pulumi.get(self, "vlan_id")


class AwaitableGetExpressRouteCrossConnectionPeeringResult(GetExpressRouteCrossConnectionPeeringResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetExpressRouteCrossConnectionPeeringResult(
            azure_asn=self.azure_asn,
            etag=self.etag,
            gateway_manager_etag=self.gateway_manager_etag,
            id=self.id,
            ipv6_peering_config=self.ipv6_peering_config,
            last_modified_by=self.last_modified_by,
            microsoft_peering_config=self.microsoft_peering_config,
            name=self.name,
            peer_asn=self.peer_asn,
            peering_type=self.peering_type,
            primary_azure_port=self.primary_azure_port,
            primary_peer_address_prefix=self.primary_peer_address_prefix,
            provisioning_state=self.provisioning_state,
            secondary_azure_port=self.secondary_azure_port,
            secondary_peer_address_prefix=self.secondary_peer_address_prefix,
            shared_key=self.shared_key,
            state=self.state,
            vlan_id=self.vlan_id)


def get_express_route_cross_connection_peering(cross_connection_name: Optional[str] = None,
                                               peering_name: Optional[str] = None,
                                               resource_group_name: Optional[str] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetExpressRouteCrossConnectionPeeringResult:
    """
    Use this data source to access information about an existing resource.

    :param str cross_connection_name: The name of the ExpressRouteCrossConnection.
    :param str peering_name: The name of the peering.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['crossConnectionName'] = cross_connection_name
    __args__['peeringName'] = peering_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:network/v20181101:getExpressRouteCrossConnectionPeering', __args__, opts=opts, typ=GetExpressRouteCrossConnectionPeeringResult).value

    return AwaitableGetExpressRouteCrossConnectionPeeringResult(
        azure_asn=__ret__.azure_asn,
        etag=__ret__.etag,
        gateway_manager_etag=__ret__.gateway_manager_etag,
        id=__ret__.id,
        ipv6_peering_config=__ret__.ipv6_peering_config,
        last_modified_by=__ret__.last_modified_by,
        microsoft_peering_config=__ret__.microsoft_peering_config,
        name=__ret__.name,
        peer_asn=__ret__.peer_asn,
        peering_type=__ret__.peering_type,
        primary_azure_port=__ret__.primary_azure_port,
        primary_peer_address_prefix=__ret__.primary_peer_address_prefix,
        provisioning_state=__ret__.provisioning_state,
        secondary_azure_port=__ret__.secondary_azure_port,
        secondary_peer_address_prefix=__ret__.secondary_peer_address_prefix,
        shared_key=__ret__.shared_key,
        state=__ret__.state,
        vlan_id=__ret__.vlan_id)
