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
    'GetCustomImageResult',
    'AwaitableGetCustomImageResult',
    'get_custom_image',
]

@pulumi.output_type
class GetCustomImageResult:
    """
    A custom image.
    """
    def __init__(__self__, author=None, creation_date=None, custom_image_plan=None, data_disk_storage_info=None, description=None, id=None, is_plan_authorized=None, location=None, managed_image_id=None, managed_snapshot_id=None, name=None, provisioning_state=None, tags=None, type=None, unique_identifier=None, vhd=None, vm=None):
        if author and not isinstance(author, str):
            raise TypeError("Expected argument 'author' to be a str")
        pulumi.set(__self__, "author", author)
        if creation_date and not isinstance(creation_date, str):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, "creation_date", creation_date)
        if custom_image_plan and not isinstance(custom_image_plan, dict):
            raise TypeError("Expected argument 'custom_image_plan' to be a dict")
        pulumi.set(__self__, "custom_image_plan", custom_image_plan)
        if data_disk_storage_info and not isinstance(data_disk_storage_info, list):
            raise TypeError("Expected argument 'data_disk_storage_info' to be a list")
        pulumi.set(__self__, "data_disk_storage_info", data_disk_storage_info)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_plan_authorized and not isinstance(is_plan_authorized, bool):
            raise TypeError("Expected argument 'is_plan_authorized' to be a bool")
        pulumi.set(__self__, "is_plan_authorized", is_plan_authorized)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_image_id and not isinstance(managed_image_id, str):
            raise TypeError("Expected argument 'managed_image_id' to be a str")
        pulumi.set(__self__, "managed_image_id", managed_image_id)
        if managed_snapshot_id and not isinstance(managed_snapshot_id, str):
            raise TypeError("Expected argument 'managed_snapshot_id' to be a str")
        pulumi.set(__self__, "managed_snapshot_id", managed_snapshot_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if unique_identifier and not isinstance(unique_identifier, str):
            raise TypeError("Expected argument 'unique_identifier' to be a str")
        pulumi.set(__self__, "unique_identifier", unique_identifier)
        if vhd and not isinstance(vhd, dict):
            raise TypeError("Expected argument 'vhd' to be a dict")
        pulumi.set(__self__, "vhd", vhd)
        if vm and not isinstance(vm, dict):
            raise TypeError("Expected argument 'vm' to be a dict")
        pulumi.set(__self__, "vm", vm)

    @property
    @pulumi.getter
    def author(self) -> Optional[str]:
        """
        The author of the custom image.
        """
        return pulumi.get(self, "author")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> str:
        """
        The creation date of the custom image.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="customImagePlan")
    def custom_image_plan(self) -> Optional['outputs.CustomImagePropertiesFromPlanResponse']:
        """
        Storage information about the plan related to this custom image
        """
        return pulumi.get(self, "custom_image_plan")

    @property
    @pulumi.getter(name="dataDiskStorageInfo")
    def data_disk_storage_info(self) -> Optional[Sequence['outputs.DataDiskStorageTypeInfoResponse']]:
        """
        Storage information about the data disks present in the custom image
        """
        return pulumi.get(self, "data_disk_storage_info")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the custom image.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The identifier of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isPlanAuthorized")
    def is_plan_authorized(self) -> Optional[bool]:
        """
        Whether or not the custom images underlying offer/plan has been enabled for programmatic deployment
        """
        return pulumi.get(self, "is_plan_authorized")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedImageId")
    def managed_image_id(self) -> Optional[str]:
        """
        The Managed Image Id backing the custom image.
        """
        return pulumi.get(self, "managed_image_id")

    @property
    @pulumi.getter(name="managedSnapshotId")
    def managed_snapshot_id(self) -> Optional[str]:
        """
        The Managed Snapshot Id backing the custom image.
        """
        return pulumi.get(self, "managed_snapshot_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning status of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="uniqueIdentifier")
    def unique_identifier(self) -> str:
        """
        The unique immutable identifier of a resource (Guid).
        """
        return pulumi.get(self, "unique_identifier")

    @property
    @pulumi.getter
    def vhd(self) -> Optional['outputs.CustomImagePropertiesCustomResponse']:
        """
        The VHD from which the image is to be created.
        """
        return pulumi.get(self, "vhd")

    @property
    @pulumi.getter
    def vm(self) -> Optional['outputs.CustomImagePropertiesFromVmResponse']:
        """
        The virtual machine from which the image is to be created.
        """
        return pulumi.get(self, "vm")


class AwaitableGetCustomImageResult(GetCustomImageResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCustomImageResult(
            author=self.author,
            creation_date=self.creation_date,
            custom_image_plan=self.custom_image_plan,
            data_disk_storage_info=self.data_disk_storage_info,
            description=self.description,
            id=self.id,
            is_plan_authorized=self.is_plan_authorized,
            location=self.location,
            managed_image_id=self.managed_image_id,
            managed_snapshot_id=self.managed_snapshot_id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            tags=self.tags,
            type=self.type,
            unique_identifier=self.unique_identifier,
            vhd=self.vhd,
            vm=self.vm)


def get_custom_image(expand: Optional[str] = None,
                     lab_name: Optional[str] = None,
                     name: Optional[str] = None,
                     resource_group_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCustomImageResult:
    """
    Use this data source to access information about an existing resource.

    :param str expand: Specify the $expand query. Example: 'properties($select=vm)'
    :param str lab_name: The name of the lab.
    :param str name: The name of the custom image.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['labName'] = lab_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:devtestlab/latest:getCustomImage', __args__, opts=opts, typ=GetCustomImageResult).value

    return AwaitableGetCustomImageResult(
        author=__ret__.author,
        creation_date=__ret__.creation_date,
        custom_image_plan=__ret__.custom_image_plan,
        data_disk_storage_info=__ret__.data_disk_storage_info,
        description=__ret__.description,
        id=__ret__.id,
        is_plan_authorized=__ret__.is_plan_authorized,
        location=__ret__.location,
        managed_image_id=__ret__.managed_image_id,
        managed_snapshot_id=__ret__.managed_snapshot_id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        tags=__ret__.tags,
        type=__ret__.type,
        unique_identifier=__ret__.unique_identifier,
        vhd=__ret__.vhd,
        vm=__ret__.vm)
