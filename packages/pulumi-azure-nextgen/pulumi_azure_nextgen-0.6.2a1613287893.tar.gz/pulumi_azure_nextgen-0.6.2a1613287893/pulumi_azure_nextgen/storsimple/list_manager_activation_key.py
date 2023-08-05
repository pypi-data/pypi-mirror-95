# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'ListManagerActivationKeyResult',
    'AwaitableListManagerActivationKeyResult',
    'list_manager_activation_key',
]

@pulumi.output_type
class ListManagerActivationKeyResult:
    """
    The key.
    """
    def __init__(__self__, activation_key=None):
        if activation_key and not isinstance(activation_key, str):
            raise TypeError("Expected argument 'activation_key' to be a str")
        pulumi.set(__self__, "activation_key", activation_key)

    @property
    @pulumi.getter(name="activationKey")
    def activation_key(self) -> str:
        """
        The activation key for the device.
        """
        return pulumi.get(self, "activation_key")


class AwaitableListManagerActivationKeyResult(ListManagerActivationKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListManagerActivationKeyResult(
            activation_key=self.activation_key)


def list_manager_activation_key(manager_name: Optional[str] = None,
                                resource_group_name: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListManagerActivationKeyResult:
    """
    Use this data source to access information about an existing resource.

    :param str manager_name: The manager name
    :param str resource_group_name: The resource group name
    """
    __args__ = dict()
    __args__['managerName'] = manager_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:storsimple:listManagerActivationKey', __args__, opts=opts, typ=ListManagerActivationKeyResult).value

    return AwaitableListManagerActivationKeyResult(
        activation_key=__ret__.activation_key)
