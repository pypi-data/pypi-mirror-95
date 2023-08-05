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
    'GetUserSettingsResult',
    'AwaitableGetUserSettingsResult',
    'get_user_settings',
]

@pulumi.output_type
class GetUserSettingsResult:
    """
    Response to get user settings
    """
    def __init__(__self__, properties=None):
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.UserPropertiesResponse':
        """
        The cloud shell user settings properties.
        """
        return pulumi.get(self, "properties")


class AwaitableGetUserSettingsResult(GetUserSettingsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserSettingsResult(
            properties=self.properties)


def get_user_settings(user_settings_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserSettingsResult:
    """
    Use this data source to access information about an existing resource.

    :param str user_settings_name: The name of the user settings
    """
    __args__ = dict()
    __args__['userSettingsName'] = user_settings_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:portal/latest:getUserSettings', __args__, opts=opts, typ=GetUserSettingsResult).value

    return AwaitableGetUserSettingsResult(
        properties=__ret__.properties)
