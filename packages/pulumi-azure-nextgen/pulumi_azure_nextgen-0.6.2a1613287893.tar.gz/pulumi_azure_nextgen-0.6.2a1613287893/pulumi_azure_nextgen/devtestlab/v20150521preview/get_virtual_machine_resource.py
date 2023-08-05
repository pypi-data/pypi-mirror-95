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
    'GetVirtualMachineResourceResult',
    'AwaitableGetVirtualMachineResourceResult',
    'get_virtual_machine_resource',
]

@pulumi.output_type
class GetVirtualMachineResourceResult:
    """
    A virtual machine.
    """
    def __init__(__self__, artifact_deployment_status=None, artifacts=None, compute_id=None, created_by_user=None, created_by_user_id=None, custom_image_id=None, disallow_public_ip_address=None, fqdn=None, gallery_image_reference=None, id=None, is_authentication_with_ssh_key=None, lab_subnet_name=None, lab_virtual_network_id=None, location=None, name=None, notes=None, os_type=None, owner_object_id=None, password=None, provisioning_state=None, size=None, ssh_key=None, tags=None, type=None, user_name=None):
        if artifact_deployment_status and not isinstance(artifact_deployment_status, dict):
            raise TypeError("Expected argument 'artifact_deployment_status' to be a dict")
        pulumi.set(__self__, "artifact_deployment_status", artifact_deployment_status)
        if artifacts and not isinstance(artifacts, list):
            raise TypeError("Expected argument 'artifacts' to be a list")
        pulumi.set(__self__, "artifacts", artifacts)
        if compute_id and not isinstance(compute_id, str):
            raise TypeError("Expected argument 'compute_id' to be a str")
        pulumi.set(__self__, "compute_id", compute_id)
        if created_by_user and not isinstance(created_by_user, str):
            raise TypeError("Expected argument 'created_by_user' to be a str")
        pulumi.set(__self__, "created_by_user", created_by_user)
        if created_by_user_id and not isinstance(created_by_user_id, str):
            raise TypeError("Expected argument 'created_by_user_id' to be a str")
        pulumi.set(__self__, "created_by_user_id", created_by_user_id)
        if custom_image_id and not isinstance(custom_image_id, str):
            raise TypeError("Expected argument 'custom_image_id' to be a str")
        pulumi.set(__self__, "custom_image_id", custom_image_id)
        if disallow_public_ip_address and not isinstance(disallow_public_ip_address, bool):
            raise TypeError("Expected argument 'disallow_public_ip_address' to be a bool")
        pulumi.set(__self__, "disallow_public_ip_address", disallow_public_ip_address)
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        pulumi.set(__self__, "fqdn", fqdn)
        if gallery_image_reference and not isinstance(gallery_image_reference, dict):
            raise TypeError("Expected argument 'gallery_image_reference' to be a dict")
        pulumi.set(__self__, "gallery_image_reference", gallery_image_reference)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_authentication_with_ssh_key and not isinstance(is_authentication_with_ssh_key, bool):
            raise TypeError("Expected argument 'is_authentication_with_ssh_key' to be a bool")
        pulumi.set(__self__, "is_authentication_with_ssh_key", is_authentication_with_ssh_key)
        if lab_subnet_name and not isinstance(lab_subnet_name, str):
            raise TypeError("Expected argument 'lab_subnet_name' to be a str")
        pulumi.set(__self__, "lab_subnet_name", lab_subnet_name)
        if lab_virtual_network_id and not isinstance(lab_virtual_network_id, str):
            raise TypeError("Expected argument 'lab_virtual_network_id' to be a str")
        pulumi.set(__self__, "lab_virtual_network_id", lab_virtual_network_id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if notes and not isinstance(notes, str):
            raise TypeError("Expected argument 'notes' to be a str")
        pulumi.set(__self__, "notes", notes)
        if os_type and not isinstance(os_type, str):
            raise TypeError("Expected argument 'os_type' to be a str")
        pulumi.set(__self__, "os_type", os_type)
        if owner_object_id and not isinstance(owner_object_id, str):
            raise TypeError("Expected argument 'owner_object_id' to be a str")
        pulumi.set(__self__, "owner_object_id", owner_object_id)
        if password and not isinstance(password, str):
            raise TypeError("Expected argument 'password' to be a str")
        pulumi.set(__self__, "password", password)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if size and not isinstance(size, str):
            raise TypeError("Expected argument 'size' to be a str")
        pulumi.set(__self__, "size", size)
        if ssh_key and not isinstance(ssh_key, str):
            raise TypeError("Expected argument 'ssh_key' to be a str")
        pulumi.set(__self__, "ssh_key", ssh_key)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_name and not isinstance(user_name, str):
            raise TypeError("Expected argument 'user_name' to be a str")
        pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="artifactDeploymentStatus")
    def artifact_deployment_status(self) -> Optional['outputs.ArtifactDeploymentStatusPropertiesResponse']:
        """
        The artifact deployment status for the virtual machine.
        """
        return pulumi.get(self, "artifact_deployment_status")

    @property
    @pulumi.getter
    def artifacts(self) -> Optional[Sequence['outputs.ArtifactInstallPropertiesResponse']]:
        """
        The artifacts to be installed on the virtual machine.
        """
        return pulumi.get(self, "artifacts")

    @property
    @pulumi.getter(name="computeId")
    def compute_id(self) -> Optional[str]:
        """
        The resource identifier (Microsoft.Compute) of the virtual machine.
        """
        return pulumi.get(self, "compute_id")

    @property
    @pulumi.getter(name="createdByUser")
    def created_by_user(self) -> Optional[str]:
        """
        The email address of creator of the virtual machine.
        """
        return pulumi.get(self, "created_by_user")

    @property
    @pulumi.getter(name="createdByUserId")
    def created_by_user_id(self) -> Optional[str]:
        """
        The object identifier of the creator of the virtual machine.
        """
        return pulumi.get(self, "created_by_user_id")

    @property
    @pulumi.getter(name="customImageId")
    def custom_image_id(self) -> Optional[str]:
        """
        The custom image identifier of the virtual machine.
        """
        return pulumi.get(self, "custom_image_id")

    @property
    @pulumi.getter(name="disallowPublicIpAddress")
    def disallow_public_ip_address(self) -> Optional[bool]:
        """
        Indicates whether the virtual machine is to be created without a public IP address.
        """
        return pulumi.get(self, "disallow_public_ip_address")

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[str]:
        """
        The fully-qualified domain name of the virtual machine.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter(name="galleryImageReference")
    def gallery_image_reference(self) -> Optional['outputs.GalleryImageReferenceResponse']:
        """
        The Microsoft Azure Marketplace image reference of the virtual machine.
        """
        return pulumi.get(self, "gallery_image_reference")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The identifier of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isAuthenticationWithSshKey")
    def is_authentication_with_ssh_key(self) -> Optional[bool]:
        """
        A value indicating whether this virtual machine uses an SSH key for authentication.
        """
        return pulumi.get(self, "is_authentication_with_ssh_key")

    @property
    @pulumi.getter(name="labSubnetName")
    def lab_subnet_name(self) -> Optional[str]:
        """
        The lab subnet name of the virtual machine.
        """
        return pulumi.get(self, "lab_subnet_name")

    @property
    @pulumi.getter(name="labVirtualNetworkId")
    def lab_virtual_network_id(self) -> Optional[str]:
        """
        The lab virtual network identifier of the virtual machine.
        """
        return pulumi.get(self, "lab_virtual_network_id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def notes(self) -> Optional[str]:
        """
        The notes of the virtual machine.
        """
        return pulumi.get(self, "notes")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[str]:
        """
        The OS type of the virtual machine.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="ownerObjectId")
    def owner_object_id(self) -> Optional[str]:
        """
        The object identifier of the owner of the virtual machine.
        """
        return pulumi.get(self, "owner_object_id")

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        The password of the virtual machine administrator.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        The provisioning status of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def size(self) -> Optional[str]:
        """
        The size of the virtual machine.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter(name="sshKey")
    def ssh_key(self) -> Optional[str]:
        """
        The SSH key of the virtual machine administrator.
        """
        return pulumi.get(self, "ssh_key")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[str]:
        """
        The user name of the virtual machine.
        """
        return pulumi.get(self, "user_name")


class AwaitableGetVirtualMachineResourceResult(GetVirtualMachineResourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualMachineResourceResult(
            artifact_deployment_status=self.artifact_deployment_status,
            artifacts=self.artifacts,
            compute_id=self.compute_id,
            created_by_user=self.created_by_user,
            created_by_user_id=self.created_by_user_id,
            custom_image_id=self.custom_image_id,
            disallow_public_ip_address=self.disallow_public_ip_address,
            fqdn=self.fqdn,
            gallery_image_reference=self.gallery_image_reference,
            id=self.id,
            is_authentication_with_ssh_key=self.is_authentication_with_ssh_key,
            lab_subnet_name=self.lab_subnet_name,
            lab_virtual_network_id=self.lab_virtual_network_id,
            location=self.location,
            name=self.name,
            notes=self.notes,
            os_type=self.os_type,
            owner_object_id=self.owner_object_id,
            password=self.password,
            provisioning_state=self.provisioning_state,
            size=self.size,
            ssh_key=self.ssh_key,
            tags=self.tags,
            type=self.type,
            user_name=self.user_name)


def get_virtual_machine_resource(lab_name: Optional[str] = None,
                                 name: Optional[str] = None,
                                 resource_group_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualMachineResourceResult:
    """
    Use this data source to access information about an existing resource.

    :param str lab_name: The name of the lab.
    :param str name: The name of the virtual Machine.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['labName'] = lab_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:devtestlab/v20150521preview:getVirtualMachineResource', __args__, opts=opts, typ=GetVirtualMachineResourceResult).value

    return AwaitableGetVirtualMachineResourceResult(
        artifact_deployment_status=__ret__.artifact_deployment_status,
        artifacts=__ret__.artifacts,
        compute_id=__ret__.compute_id,
        created_by_user=__ret__.created_by_user,
        created_by_user_id=__ret__.created_by_user_id,
        custom_image_id=__ret__.custom_image_id,
        disallow_public_ip_address=__ret__.disallow_public_ip_address,
        fqdn=__ret__.fqdn,
        gallery_image_reference=__ret__.gallery_image_reference,
        id=__ret__.id,
        is_authentication_with_ssh_key=__ret__.is_authentication_with_ssh_key,
        lab_subnet_name=__ret__.lab_subnet_name,
        lab_virtual_network_id=__ret__.lab_virtual_network_id,
        location=__ret__.location,
        name=__ret__.name,
        notes=__ret__.notes,
        os_type=__ret__.os_type,
        owner_object_id=__ret__.owner_object_id,
        password=__ret__.password,
        provisioning_state=__ret__.provisioning_state,
        size=__ret__.size,
        ssh_key=__ret__.ssh_key,
        tags=__ret__.tags,
        type=__ret__.type,
        user_name=__ret__.user_name)
