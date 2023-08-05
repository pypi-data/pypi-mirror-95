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
    'GetConnectedClusterResult',
    'AwaitableGetConnectedClusterResult',
    'get_connected_cluster',
]

@pulumi.output_type
class GetConnectedClusterResult:
    """
    Represents a connected cluster.
    """
    def __init__(__self__, agent_public_key_certificate=None, agent_version=None, connectivity_status=None, distribution=None, id=None, identity=None, infrastructure=None, kubernetes_version=None, last_connectivity_time=None, location=None, managed_identity_certificate_expiration_time=None, name=None, offering=None, provisioning_state=None, system_data=None, tags=None, total_core_count=None, total_node_count=None, type=None):
        if agent_public_key_certificate and not isinstance(agent_public_key_certificate, str):
            raise TypeError("Expected argument 'agent_public_key_certificate' to be a str")
        pulumi.set(__self__, "agent_public_key_certificate", agent_public_key_certificate)
        if agent_version and not isinstance(agent_version, str):
            raise TypeError("Expected argument 'agent_version' to be a str")
        pulumi.set(__self__, "agent_version", agent_version)
        if connectivity_status and not isinstance(connectivity_status, str):
            raise TypeError("Expected argument 'connectivity_status' to be a str")
        pulumi.set(__self__, "connectivity_status", connectivity_status)
        if distribution and not isinstance(distribution, str):
            raise TypeError("Expected argument 'distribution' to be a str")
        pulumi.set(__self__, "distribution", distribution)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if infrastructure and not isinstance(infrastructure, str):
            raise TypeError("Expected argument 'infrastructure' to be a str")
        pulumi.set(__self__, "infrastructure", infrastructure)
        if kubernetes_version and not isinstance(kubernetes_version, str):
            raise TypeError("Expected argument 'kubernetes_version' to be a str")
        pulumi.set(__self__, "kubernetes_version", kubernetes_version)
        if last_connectivity_time and not isinstance(last_connectivity_time, str):
            raise TypeError("Expected argument 'last_connectivity_time' to be a str")
        pulumi.set(__self__, "last_connectivity_time", last_connectivity_time)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_identity_certificate_expiration_time and not isinstance(managed_identity_certificate_expiration_time, str):
            raise TypeError("Expected argument 'managed_identity_certificate_expiration_time' to be a str")
        pulumi.set(__self__, "managed_identity_certificate_expiration_time", managed_identity_certificate_expiration_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if offering and not isinstance(offering, str):
            raise TypeError("Expected argument 'offering' to be a str")
        pulumi.set(__self__, "offering", offering)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if total_core_count and not isinstance(total_core_count, int):
            raise TypeError("Expected argument 'total_core_count' to be a int")
        pulumi.set(__self__, "total_core_count", total_core_count)
        if total_node_count and not isinstance(total_node_count, int):
            raise TypeError("Expected argument 'total_node_count' to be a int")
        pulumi.set(__self__, "total_node_count", total_node_count)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="agentPublicKeyCertificate")
    def agent_public_key_certificate(self) -> str:
        """
        Base64 encoded public certificate used by the agent to do the initial handshake to the backend services in Azure.
        """
        return pulumi.get(self, "agent_public_key_certificate")

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> str:
        """
        Version of the agent running on the connected cluster resource
        """
        return pulumi.get(self, "agent_version")

    @property
    @pulumi.getter(name="connectivityStatus")
    def connectivity_status(self) -> str:
        """
        Represents the connectivity status of the connected cluster.
        """
        return pulumi.get(self, "connectivity_status")

    @property
    @pulumi.getter
    def distribution(self) -> Optional[str]:
        """
        The Kubernetes distribution running on this connected cluster.
        """
        return pulumi.get(self, "distribution")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> 'outputs.ConnectedClusterIdentityResponse':
        """
        The identity of the connected cluster.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def infrastructure(self) -> Optional[str]:
        """
        The infrastructure on which the Kubernetes cluster represented by this connected cluster is running on.
        """
        return pulumi.get(self, "infrastructure")

    @property
    @pulumi.getter(name="kubernetesVersion")
    def kubernetes_version(self) -> str:
        """
        The Kubernetes version of the connected cluster resource
        """
        return pulumi.get(self, "kubernetes_version")

    @property
    @pulumi.getter(name="lastConnectivityTime")
    def last_connectivity_time(self) -> str:
        """
        Time representing the last instance when heart beat was received from the cluster
        """
        return pulumi.get(self, "last_connectivity_time")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedIdentityCertificateExpirationTime")
    def managed_identity_certificate_expiration_time(self) -> str:
        """
        Expiration time of the managed identity certificate
        """
        return pulumi.get(self, "managed_identity_certificate_expiration_time")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def offering(self) -> str:
        """
        Connected cluster offering
        """
        return pulumi.get(self, "offering")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Provisioning state of the connected cluster resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="totalCoreCount")
    def total_core_count(self) -> int:
        """
        Number of CPU cores present in the connected cluster resource
        """
        return pulumi.get(self, "total_core_count")

    @property
    @pulumi.getter(name="totalNodeCount")
    def total_node_count(self) -> int:
        """
        Number of nodes present in the connected cluster resource
        """
        return pulumi.get(self, "total_node_count")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetConnectedClusterResult(GetConnectedClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectedClusterResult(
            agent_public_key_certificate=self.agent_public_key_certificate,
            agent_version=self.agent_version,
            connectivity_status=self.connectivity_status,
            distribution=self.distribution,
            id=self.id,
            identity=self.identity,
            infrastructure=self.infrastructure,
            kubernetes_version=self.kubernetes_version,
            last_connectivity_time=self.last_connectivity_time,
            location=self.location,
            managed_identity_certificate_expiration_time=self.managed_identity_certificate_expiration_time,
            name=self.name,
            offering=self.offering,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            tags=self.tags,
            total_core_count=self.total_core_count,
            total_node_count=self.total_node_count,
            type=self.type)


def get_connected_cluster(cluster_name: Optional[str] = None,
                          resource_group_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectedClusterResult:
    """
    Use this data source to access information about an existing resource.

    :param str cluster_name: The name of the Kubernetes cluster on which get is called.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:kubernetes/v20210401preview:getConnectedCluster', __args__, opts=opts, typ=GetConnectedClusterResult).value

    return AwaitableGetConnectedClusterResult(
        agent_public_key_certificate=__ret__.agent_public_key_certificate,
        agent_version=__ret__.agent_version,
        connectivity_status=__ret__.connectivity_status,
        distribution=__ret__.distribution,
        id=__ret__.id,
        identity=__ret__.identity,
        infrastructure=__ret__.infrastructure,
        kubernetes_version=__ret__.kubernetes_version,
        last_connectivity_time=__ret__.last_connectivity_time,
        location=__ret__.location,
        managed_identity_certificate_expiration_time=__ret__.managed_identity_certificate_expiration_time,
        name=__ret__.name,
        offering=__ret__.offering,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        total_core_count=__ret__.total_core_count,
        total_node_count=__ret__.total_node_count,
        type=__ret__.type)
