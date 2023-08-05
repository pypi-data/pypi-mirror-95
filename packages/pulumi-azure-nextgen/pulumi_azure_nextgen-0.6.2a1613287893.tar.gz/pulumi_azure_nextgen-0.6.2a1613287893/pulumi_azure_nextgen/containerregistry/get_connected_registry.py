# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'GetConnectedRegistryResult',
    'AwaitableGetConnectedRegistryResult',
    'get_connected_registry',
]

@pulumi.output_type
class GetConnectedRegistryResult:
    """
    An object that represents a connected registry for a container registry.
    """
    def __init__(__self__, activation=None, client_token_ids=None, connection_state=None, id=None, last_activity_time=None, logging=None, login_server=None, mode=None, name=None, parent=None, provisioning_state=None, status_details=None, system_data=None, type=None, version=None):
        if activation and not isinstance(activation, dict):
            raise TypeError("Expected argument 'activation' to be a dict")
        pulumi.set(__self__, "activation", activation)
        if client_token_ids and not isinstance(client_token_ids, list):
            raise TypeError("Expected argument 'client_token_ids' to be a list")
        pulumi.set(__self__, "client_token_ids", client_token_ids)
        if connection_state and not isinstance(connection_state, str):
            raise TypeError("Expected argument 'connection_state' to be a str")
        pulumi.set(__self__, "connection_state", connection_state)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_activity_time and not isinstance(last_activity_time, str):
            raise TypeError("Expected argument 'last_activity_time' to be a str")
        pulumi.set(__self__, "last_activity_time", last_activity_time)
        if logging and not isinstance(logging, dict):
            raise TypeError("Expected argument 'logging' to be a dict")
        pulumi.set(__self__, "logging", logging)
        if login_server and not isinstance(login_server, dict):
            raise TypeError("Expected argument 'login_server' to be a dict")
        pulumi.set(__self__, "login_server", login_server)
        if mode and not isinstance(mode, str):
            raise TypeError("Expected argument 'mode' to be a str")
        pulumi.set(__self__, "mode", mode)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parent and not isinstance(parent, dict):
            raise TypeError("Expected argument 'parent' to be a dict")
        pulumi.set(__self__, "parent", parent)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if status_details and not isinstance(status_details, list):
            raise TypeError("Expected argument 'status_details' to be a list")
        pulumi.set(__self__, "status_details", status_details)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def activation(self) -> 'outputs.ActivationPropertiesResponse':
        """
        The activation properties of the connected registry.
        """
        return pulumi.get(self, "activation")

    @property
    @pulumi.getter(name="clientTokenIds")
    def client_token_ids(self) -> Optional[Sequence[str]]:
        """
        The list of the ACR token resource IDs used to authenticate clients to the connected registry.
        """
        return pulumi.get(self, "client_token_ids")

    @property
    @pulumi.getter(name="connectionState")
    def connection_state(self) -> str:
        """
        The current connection state of the connected registry.
        """
        return pulumi.get(self, "connection_state")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastActivityTime")
    def last_activity_time(self) -> str:
        """
        The last activity time of the connected registry.
        """
        return pulumi.get(self, "last_activity_time")

    @property
    @pulumi.getter
    def logging(self) -> Optional['outputs.LoggingPropertiesResponse']:
        """
        The logging properties of the connected registry.
        """
        return pulumi.get(self, "logging")

    @property
    @pulumi.getter(name="loginServer")
    def login_server(self) -> Optional['outputs.LoginServerPropertiesResponse']:
        """
        The login server properties of the connected registry.
        """
        return pulumi.get(self, "login_server")

    @property
    @pulumi.getter
    def mode(self) -> str:
        """
        The mode of the connected registry resource that indicates the permissions of the registry.
        """
        return pulumi.get(self, "mode")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parent(self) -> 'outputs.ParentPropertiesResponse':
        """
        The parent of the connected registry.
        """
        return pulumi.get(self, "parent")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="statusDetails")
    def status_details(self) -> Sequence['outputs.StatusDetailPropertiesResponse']:
        """
        The list of current statuses of the connected registry.
        """
        return pulumi.get(self, "status_details")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The current version of ACR runtime on the connected registry.
        """
        return pulumi.get(self, "version")


class AwaitableGetConnectedRegistryResult(GetConnectedRegistryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectedRegistryResult(
            activation=self.activation,
            client_token_ids=self.client_token_ids,
            connection_state=self.connection_state,
            id=self.id,
            last_activity_time=self.last_activity_time,
            logging=self.logging,
            login_server=self.login_server,
            mode=self.mode,
            name=self.name,
            parent=self.parent,
            provisioning_state=self.provisioning_state,
            status_details=self.status_details,
            system_data=self.system_data,
            type=self.type,
            version=self.version)


def get_connected_registry(connected_registry_name: Optional[str] = None,
                           registry_name: Optional[str] = None,
                           resource_group_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectedRegistryResult:
    """
    Use this data source to access information about an existing resource.

    :param str connected_registry_name: The name of the connected registry.
    :param str registry_name: The name of the container registry.
    :param str resource_group_name: The name of the resource group to which the container registry belongs.
    """
    __args__ = dict()
    __args__['connectedRegistryName'] = connected_registry_name
    __args__['registryName'] = registry_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:containerregistry:getConnectedRegistry', __args__, opts=opts, typ=GetConnectedRegistryResult).value

    return AwaitableGetConnectedRegistryResult(
        activation=__ret__.activation,
        client_token_ids=__ret__.client_token_ids,
        connection_state=__ret__.connection_state,
        id=__ret__.id,
        last_activity_time=__ret__.last_activity_time,
        logging=__ret__.logging,
        login_server=__ret__.login_server,
        mode=__ret__.mode,
        name=__ret__.name,
        parent=__ret__.parent,
        provisioning_state=__ret__.provisioning_state,
        status_details=__ret__.status_details,
        system_data=__ret__.system_data,
        type=__ret__.type,
        version=__ret__.version)
