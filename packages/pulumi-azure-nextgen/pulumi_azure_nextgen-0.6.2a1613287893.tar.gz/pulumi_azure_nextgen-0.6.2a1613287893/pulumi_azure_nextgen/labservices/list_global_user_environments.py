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
    'ListGlobalUserEnvironmentsResult',
    'AwaitableListGlobalUserEnvironmentsResult',
    'list_global_user_environments',
]

@pulumi.output_type
class ListGlobalUserEnvironmentsResult:
    """
    Represents the list of environments owned by a user
    """
    def __init__(__self__, environments=None):
        if environments and not isinstance(environments, list):
            raise TypeError("Expected argument 'environments' to be a list")
        pulumi.set(__self__, "environments", environments)

    @property
    @pulumi.getter
    def environments(self) -> Optional[Sequence['outputs.EnvironmentDetailsResponseResult']]:
        """
        List of all the environments
        """
        return pulumi.get(self, "environments")


class AwaitableListGlobalUserEnvironmentsResult(ListGlobalUserEnvironmentsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListGlobalUserEnvironmentsResult(
            environments=self.environments)


def list_global_user_environments(lab_id: Optional[str] = None,
                                  user_name: Optional[str] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListGlobalUserEnvironmentsResult:
    """
    Use this data source to access information about an existing resource.

    :param str lab_id: The resource Id of the lab
    :param str user_name: The name of the user.
    """
    __args__ = dict()
    __args__['labId'] = lab_id
    __args__['userName'] = user_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:labservices:listGlobalUserEnvironments', __args__, opts=opts, typ=ListGlobalUserEnvironmentsResult).value

    return AwaitableListGlobalUserEnvironmentsResult(
        environments=__ret__.environments)
