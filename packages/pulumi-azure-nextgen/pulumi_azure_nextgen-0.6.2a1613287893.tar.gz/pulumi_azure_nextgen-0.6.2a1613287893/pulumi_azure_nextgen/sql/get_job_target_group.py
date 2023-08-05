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
    'GetJobTargetGroupResult',
    'AwaitableGetJobTargetGroupResult',
    'get_job_target_group',
]

@pulumi.output_type
class GetJobTargetGroupResult:
    """
    A group of job targets.
    """
    def __init__(__self__, id=None, members=None, name=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if members and not isinstance(members, list):
            raise TypeError("Expected argument 'members' to be a list")
        pulumi.set(__self__, "members", members)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def members(self) -> Sequence['outputs.JobTargetResponse']:
        """
        Members of the target group.
        """
        return pulumi.get(self, "members")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetJobTargetGroupResult(GetJobTargetGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetJobTargetGroupResult(
            id=self.id,
            members=self.members,
            name=self.name,
            type=self.type)


def get_job_target_group(job_agent_name: Optional[str] = None,
                         resource_group_name: Optional[str] = None,
                         server_name: Optional[str] = None,
                         target_group_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetJobTargetGroupResult:
    """
    Use this data source to access information about an existing resource.

    :param str job_agent_name: The name of the job agent.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    :param str target_group_name: The name of the target group.
    """
    __args__ = dict()
    __args__['jobAgentName'] = job_agent_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['serverName'] = server_name
    __args__['targetGroupName'] = target_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:sql:getJobTargetGroup', __args__, opts=opts, typ=GetJobTargetGroupResult).value

    return AwaitableGetJobTargetGroupResult(
        id=__ret__.id,
        members=__ret__.members,
        name=__ret__.name,
        type=__ret__.type)
