# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'ListWorkspaceKeysResult',
    'AwaitableListWorkspaceKeysResult',
    'list_workspace_keys',
]

@pulumi.output_type
class ListWorkspaceKeysResult:
    """
    The shared keys for a workspace.
    """
    def __init__(__self__, primary_shared_key=None, secondary_shared_key=None):
        if primary_shared_key and not isinstance(primary_shared_key, str):
            raise TypeError("Expected argument 'primary_shared_key' to be a str")
        pulumi.set(__self__, "primary_shared_key", primary_shared_key)
        if secondary_shared_key and not isinstance(secondary_shared_key, str):
            raise TypeError("Expected argument 'secondary_shared_key' to be a str")
        pulumi.set(__self__, "secondary_shared_key", secondary_shared_key)

    @property
    @pulumi.getter(name="primarySharedKey")
    def primary_shared_key(self) -> Optional[str]:
        """
        The primary shared key of a workspace.
        """
        return pulumi.get(self, "primary_shared_key")

    @property
    @pulumi.getter(name="secondarySharedKey")
    def secondary_shared_key(self) -> Optional[str]:
        """
        The secondary shared key of a workspace.
        """
        return pulumi.get(self, "secondary_shared_key")


class AwaitableListWorkspaceKeysResult(ListWorkspaceKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListWorkspaceKeysResult(
            primary_shared_key=self.primary_shared_key,
            secondary_shared_key=self.secondary_shared_key)


def list_workspace_keys(resource_group_name: Optional[str] = None,
                        workspace_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListWorkspaceKeysResult:
    """
    Use this data source to access information about an existing resource.

    :param str resource_group_name: The Resource Group name.
    :param str workspace_name: The Log Analytics Workspace name.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:operationalinsights/latest:listWorkspaceKeys', __args__, opts=opts, typ=ListWorkspaceKeysResult).value

    return AwaitableListWorkspaceKeysResult(
        primary_shared_key=__ret__.primary_shared_key,
        secondary_shared_key=__ret__.secondary_shared_key)
