# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetProjectResult',
    'AwaitableGetProjectResult',
    'get_project',
]

@pulumi.output_type
class GetProjectResult:
    """
    Azure Migrate Project.
    """
    def __init__(__self__, created_timestamp=None, customer_workspace_id=None, discovery_status=None, e_tag=None, id=None, location=None, name=None, number_of_assessments=None, number_of_groups=None, number_of_machines=None, provisioning_state=None, tags=None, type=None, updated_timestamp=None):
        if created_timestamp and not isinstance(created_timestamp, str):
            raise TypeError("Expected argument 'created_timestamp' to be a str")
        pulumi.set(__self__, "created_timestamp", created_timestamp)
        if customer_workspace_id and not isinstance(customer_workspace_id, str):
            raise TypeError("Expected argument 'customer_workspace_id' to be a str")
        pulumi.set(__self__, "customer_workspace_id", customer_workspace_id)
        if discovery_status and not isinstance(discovery_status, str):
            raise TypeError("Expected argument 'discovery_status' to be a str")
        pulumi.set(__self__, "discovery_status", discovery_status)
        if e_tag and not isinstance(e_tag, str):
            raise TypeError("Expected argument 'e_tag' to be a str")
        pulumi.set(__self__, "e_tag", e_tag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if number_of_assessments and not isinstance(number_of_assessments, int):
            raise TypeError("Expected argument 'number_of_assessments' to be a int")
        pulumi.set(__self__, "number_of_assessments", number_of_assessments)
        if number_of_groups and not isinstance(number_of_groups, int):
            raise TypeError("Expected argument 'number_of_groups' to be a int")
        pulumi.set(__self__, "number_of_groups", number_of_groups)
        if number_of_machines and not isinstance(number_of_machines, int):
            raise TypeError("Expected argument 'number_of_machines' to be a int")
        pulumi.set(__self__, "number_of_machines", number_of_machines)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if updated_timestamp and not isinstance(updated_timestamp, str):
            raise TypeError("Expected argument 'updated_timestamp' to be a str")
        pulumi.set(__self__, "updated_timestamp", updated_timestamp)

    @property
    @pulumi.getter(name="createdTimestamp")
    def created_timestamp(self) -> str:
        """
        Time when this project was created. Date-Time represented in ISO-8601 format.
        """
        return pulumi.get(self, "created_timestamp")

    @property
    @pulumi.getter(name="customerWorkspaceId")
    def customer_workspace_id(self) -> Optional[str]:
        """
        ARM ID of the Service Map workspace created by user.
        """
        return pulumi.get(self, "customer_workspace_id")

    @property
    @pulumi.getter(name="discoveryStatus")
    def discovery_status(self) -> str:
        """
        Reports whether project is under discovery.
        """
        return pulumi.get(self, "discovery_status")

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> Optional[str]:
        """
        For optimistic concurrency control.
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Path reference to this project /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Azure location in which project is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the project.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="numberOfAssessments")
    def number_of_assessments(self) -> int:
        """
        Number of assessments created in the project.
        """
        return pulumi.get(self, "number_of_assessments")

    @property
    @pulumi.getter(name="numberOfGroups")
    def number_of_groups(self) -> int:
        """
        Number of groups created in the project.
        """
        return pulumi.get(self, "number_of_groups")

    @property
    @pulumi.getter(name="numberOfMachines")
    def number_of_machines(self) -> int:
        """
        Number of machines in the project.
        """
        return pulumi.get(self, "number_of_machines")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Provisioning state of the project.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        """
        Tags provided by Azure Tagging service.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the object = [Microsoft.Migrate/projects].
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedTimestamp")
    def updated_timestamp(self) -> str:
        """
        Time when this project was last updated. Date-Time represented in ISO-8601 format.
        """
        return pulumi.get(self, "updated_timestamp")


class AwaitableGetProjectResult(GetProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectResult(
            created_timestamp=self.created_timestamp,
            customer_workspace_id=self.customer_workspace_id,
            discovery_status=self.discovery_status,
            e_tag=self.e_tag,
            id=self.id,
            location=self.location,
            name=self.name,
            number_of_assessments=self.number_of_assessments,
            number_of_groups=self.number_of_groups,
            number_of_machines=self.number_of_machines,
            provisioning_state=self.provisioning_state,
            tags=self.tags,
            type=self.type,
            updated_timestamp=self.updated_timestamp)


def get_project(project_name: Optional[str] = None,
                resource_group_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectResult:
    """
    Use this data source to access information about an existing resource.

    :param str project_name: Name of the Azure Migrate project.
    :param str resource_group_name: Name of the Azure Resource Group that project is part of.
    """
    __args__ = dict()
    __args__['projectName'] = project_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:migrate/v20171111preview:getProject', __args__, opts=opts, typ=GetProjectResult).value

    return AwaitableGetProjectResult(
        created_timestamp=__ret__.created_timestamp,
        customer_workspace_id=__ret__.customer_workspace_id,
        discovery_status=__ret__.discovery_status,
        e_tag=__ret__.e_tag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        number_of_assessments=__ret__.number_of_assessments,
        number_of_groups=__ret__.number_of_groups,
        number_of_machines=__ret__.number_of_machines,
        provisioning_state=__ret__.provisioning_state,
        tags=__ret__.tags,
        type=__ret__.type,
        updated_timestamp=__ret__.updated_timestamp)
