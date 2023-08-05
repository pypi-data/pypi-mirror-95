# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['VirtualMachine']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:devtestlab:VirtualMachine'.""", DeprecationWarning)


class VirtualMachine(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:devtestlab:VirtualMachine'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_claim: Optional[pulumi.Input[bool]] = None,
                 artifact_deployment_status: Optional[pulumi.Input[pulumi.InputType['ArtifactDeploymentStatusPropertiesArgs']]] = None,
                 artifacts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ArtifactInstallPropertiesArgs']]]]] = None,
                 compute_id: Optional[pulumi.Input[str]] = None,
                 created_by_user: Optional[pulumi.Input[str]] = None,
                 created_by_user_id: Optional[pulumi.Input[str]] = None,
                 created_date: Optional[pulumi.Input[str]] = None,
                 custom_image_id: Optional[pulumi.Input[str]] = None,
                 data_disk_parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DataDiskPropertiesArgs']]]]] = None,
                 disallow_public_ip_address: Optional[pulumi.Input[bool]] = None,
                 environment_id: Optional[pulumi.Input[str]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 fqdn: Optional[pulumi.Input[str]] = None,
                 gallery_image_reference: Optional[pulumi.Input[pulumi.InputType['GalleryImageReferenceArgs']]] = None,
                 is_authentication_with_ssh_key: Optional[pulumi.Input[bool]] = None,
                 lab_name: Optional[pulumi.Input[str]] = None,
                 lab_subnet_name: Optional[pulumi.Input[str]] = None,
                 lab_virtual_network_id: Optional[pulumi.Input[str]] = None,
                 last_known_power_state: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_interface: Optional[pulumi.Input[pulumi.InputType['NetworkInterfacePropertiesArgs']]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[str]] = None,
                 owner_object_id: Optional[pulumi.Input[str]] = None,
                 owner_user_principal_name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 plan_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule_parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScheduleCreationParameterArgs']]]]] = None,
                 size: Optional[pulumi.Input[str]] = None,
                 ssh_key: Optional[pulumi.Input[str]] = None,
                 storage_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 virtual_machine_creation_source: Optional[pulumi.Input[Union[str, 'VirtualMachineCreationSource']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A virtual machine.
        Latest API Version: 2018-09-15.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_claim: Indicates whether another user can take ownership of the virtual machine
        :param pulumi.Input[pulumi.InputType['ArtifactDeploymentStatusPropertiesArgs']] artifact_deployment_status: The artifact deployment status for the virtual machine.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ArtifactInstallPropertiesArgs']]]] artifacts: The artifacts to be installed on the virtual machine.
        :param pulumi.Input[str] compute_id: The resource identifier (Microsoft.Compute) of the virtual machine.
        :param pulumi.Input[str] created_by_user: The email address of creator of the virtual machine.
        :param pulumi.Input[str] created_by_user_id: The object identifier of the creator of the virtual machine.
        :param pulumi.Input[str] created_date: The creation date of the virtual machine.
        :param pulumi.Input[str] custom_image_id: The custom image identifier of the virtual machine.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DataDiskPropertiesArgs']]]] data_disk_parameters: New or existing data disks to attach to the virtual machine after creation
        :param pulumi.Input[bool] disallow_public_ip_address: Indicates whether the virtual machine is to be created without a public IP address.
        :param pulumi.Input[str] environment_id: The resource ID of the environment that contains this virtual machine, if any.
        :param pulumi.Input[str] expiration_date: The expiration date for VM.
        :param pulumi.Input[str] fqdn: The fully-qualified domain name of the virtual machine.
        :param pulumi.Input[pulumi.InputType['GalleryImageReferenceArgs']] gallery_image_reference: The Microsoft Azure Marketplace image reference of the virtual machine.
        :param pulumi.Input[bool] is_authentication_with_ssh_key: Indicates whether this virtual machine uses an SSH key for authentication.
        :param pulumi.Input[str] lab_name: The name of the lab.
        :param pulumi.Input[str] lab_subnet_name: The lab subnet name of the virtual machine.
        :param pulumi.Input[str] lab_virtual_network_id: The lab virtual network identifier of the virtual machine.
        :param pulumi.Input[str] last_known_power_state: Last known compute power state captured in DTL
        :param pulumi.Input[str] location: The location of the resource.
        :param pulumi.Input[str] name: The name of the virtual machine.
        :param pulumi.Input[pulumi.InputType['NetworkInterfacePropertiesArgs']] network_interface: The network interface properties.
        :param pulumi.Input[str] notes: The notes of the virtual machine.
        :param pulumi.Input[str] os_type: The OS type of the virtual machine.
        :param pulumi.Input[str] owner_object_id: The object identifier of the owner of the virtual machine.
        :param pulumi.Input[str] owner_user_principal_name: The user principal name of the virtual machine owner.
        :param pulumi.Input[str] password: The password of the virtual machine administrator.
        :param pulumi.Input[str] plan_id: The id of the plan associated with the virtual machine image
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScheduleCreationParameterArgs']]]] schedule_parameters: Virtual Machine schedules to be created
        :param pulumi.Input[str] size: The size of the virtual machine.
        :param pulumi.Input[str] ssh_key: The SSH key of the virtual machine administrator.
        :param pulumi.Input[str] storage_type: Storage type to use for virtual machine (i.e. Standard, Premium).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags of the resource.
        :param pulumi.Input[str] user_name: The user name of the virtual machine.
        :param pulumi.Input[Union[str, 'VirtualMachineCreationSource']] virtual_machine_creation_source: Tells source of creation of lab virtual machine. Output property only.
        """
        pulumi.log.warn("VirtualMachine is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:devtestlab:VirtualMachine'.")
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['allow_claim'] = allow_claim
            __props__['artifact_deployment_status'] = artifact_deployment_status
            __props__['artifacts'] = artifacts
            __props__['compute_id'] = compute_id
            __props__['created_by_user'] = created_by_user
            __props__['created_by_user_id'] = created_by_user_id
            __props__['created_date'] = created_date
            __props__['custom_image_id'] = custom_image_id
            __props__['data_disk_parameters'] = data_disk_parameters
            __props__['disallow_public_ip_address'] = disallow_public_ip_address
            __props__['environment_id'] = environment_id
            __props__['expiration_date'] = expiration_date
            __props__['fqdn'] = fqdn
            __props__['gallery_image_reference'] = gallery_image_reference
            __props__['is_authentication_with_ssh_key'] = is_authentication_with_ssh_key
            if lab_name is None and not opts.urn:
                raise TypeError("Missing required property 'lab_name'")
            __props__['lab_name'] = lab_name
            __props__['lab_subnet_name'] = lab_subnet_name
            __props__['lab_virtual_network_id'] = lab_virtual_network_id
            __props__['last_known_power_state'] = last_known_power_state
            __props__['location'] = location
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            __props__['network_interface'] = network_interface
            __props__['notes'] = notes
            __props__['os_type'] = os_type
            __props__['owner_object_id'] = owner_object_id
            __props__['owner_user_principal_name'] = owner_user_principal_name
            __props__['password'] = password
            __props__['plan_id'] = plan_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['schedule_parameters'] = schedule_parameters
            __props__['size'] = size
            __props__['ssh_key'] = ssh_key
            __props__['storage_type'] = storage_type
            __props__['tags'] = tags
            __props__['user_name'] = user_name
            __props__['virtual_machine_creation_source'] = virtual_machine_creation_source
            __props__['applicable_schedule'] = None
            __props__['compute_vm'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
            __props__['unique_identifier'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:devtestlab:VirtualMachine"), pulumi.Alias(type_="azure-nextgen:devtestlab/v20150521preview:VirtualMachine"), pulumi.Alias(type_="azure-nextgen:devtestlab/v20160515:VirtualMachine"), pulumi.Alias(type_="azure-nextgen:devtestlab/v20180915:VirtualMachine")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualMachine, __self__).__init__(
            'azure-nextgen:devtestlab/latest:VirtualMachine',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualMachine':
        """
        Get an existing VirtualMachine resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return VirtualMachine(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowClaim")
    def allow_claim(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether another user can take ownership of the virtual machine
        """
        return pulumi.get(self, "allow_claim")

    @property
    @pulumi.getter(name="applicableSchedule")
    def applicable_schedule(self) -> pulumi.Output['outputs.ApplicableScheduleResponse']:
        """
        The applicable schedule for the virtual machine.
        """
        return pulumi.get(self, "applicable_schedule")

    @property
    @pulumi.getter(name="artifactDeploymentStatus")
    def artifact_deployment_status(self) -> pulumi.Output[Optional['outputs.ArtifactDeploymentStatusPropertiesResponse']]:
        """
        The artifact deployment status for the virtual machine.
        """
        return pulumi.get(self, "artifact_deployment_status")

    @property
    @pulumi.getter
    def artifacts(self) -> pulumi.Output[Optional[Sequence['outputs.ArtifactInstallPropertiesResponse']]]:
        """
        The artifacts to be installed on the virtual machine.
        """
        return pulumi.get(self, "artifacts")

    @property
    @pulumi.getter(name="computeId")
    def compute_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource identifier (Microsoft.Compute) of the virtual machine.
        """
        return pulumi.get(self, "compute_id")

    @property
    @pulumi.getter(name="computeVm")
    def compute_vm(self) -> pulumi.Output['outputs.ComputeVmPropertiesResponse']:
        """
        The compute virtual machine properties.
        """
        return pulumi.get(self, "compute_vm")

    @property
    @pulumi.getter(name="createdByUser")
    def created_by_user(self) -> pulumi.Output[Optional[str]]:
        """
        The email address of creator of the virtual machine.
        """
        return pulumi.get(self, "created_by_user")

    @property
    @pulumi.getter(name="createdByUserId")
    def created_by_user_id(self) -> pulumi.Output[Optional[str]]:
        """
        The object identifier of the creator of the virtual machine.
        """
        return pulumi.get(self, "created_by_user_id")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> pulumi.Output[Optional[str]]:
        """
        The creation date of the virtual machine.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="customImageId")
    def custom_image_id(self) -> pulumi.Output[Optional[str]]:
        """
        The custom image identifier of the virtual machine.
        """
        return pulumi.get(self, "custom_image_id")

    @property
    @pulumi.getter(name="dataDiskParameters")
    def data_disk_parameters(self) -> pulumi.Output[Optional[Sequence['outputs.DataDiskPropertiesResponse']]]:
        """
        New or existing data disks to attach to the virtual machine after creation
        """
        return pulumi.get(self, "data_disk_parameters")

    @property
    @pulumi.getter(name="disallowPublicIpAddress")
    def disallow_public_ip_address(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether the virtual machine is to be created without a public IP address.
        """
        return pulumi.get(self, "disallow_public_ip_address")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource ID of the environment that contains this virtual machine, if any.
        """
        return pulumi.get(self, "environment_id")

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> pulumi.Output[Optional[str]]:
        """
        The expiration date for VM.
        """
        return pulumi.get(self, "expiration_date")

    @property
    @pulumi.getter
    def fqdn(self) -> pulumi.Output[Optional[str]]:
        """
        The fully-qualified domain name of the virtual machine.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter(name="galleryImageReference")
    def gallery_image_reference(self) -> pulumi.Output[Optional['outputs.GalleryImageReferenceResponse']]:
        """
        The Microsoft Azure Marketplace image reference of the virtual machine.
        """
        return pulumi.get(self, "gallery_image_reference")

    @property
    @pulumi.getter(name="isAuthenticationWithSshKey")
    def is_authentication_with_ssh_key(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether this virtual machine uses an SSH key for authentication.
        """
        return pulumi.get(self, "is_authentication_with_ssh_key")

    @property
    @pulumi.getter(name="labSubnetName")
    def lab_subnet_name(self) -> pulumi.Output[Optional[str]]:
        """
        The lab subnet name of the virtual machine.
        """
        return pulumi.get(self, "lab_subnet_name")

    @property
    @pulumi.getter(name="labVirtualNetworkId")
    def lab_virtual_network_id(self) -> pulumi.Output[Optional[str]]:
        """
        The lab virtual network identifier of the virtual machine.
        """
        return pulumi.get(self, "lab_virtual_network_id")

    @property
    @pulumi.getter(name="lastKnownPowerState")
    def last_known_power_state(self) -> pulumi.Output[Optional[str]]:
        """
        Last known compute power state captured in DTL
        """
        return pulumi.get(self, "last_known_power_state")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkInterface")
    def network_interface(self) -> pulumi.Output[Optional['outputs.NetworkInterfacePropertiesResponse']]:
        """
        The network interface properties.
        """
        return pulumi.get(self, "network_interface")

    @property
    @pulumi.getter
    def notes(self) -> pulumi.Output[Optional[str]]:
        """
        The notes of the virtual machine.
        """
        return pulumi.get(self, "notes")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Output[Optional[str]]:
        """
        The OS type of the virtual machine.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="ownerObjectId")
    def owner_object_id(self) -> pulumi.Output[Optional[str]]:
        """
        The object identifier of the owner of the virtual machine.
        """
        return pulumi.get(self, "owner_object_id")

    @property
    @pulumi.getter(name="ownerUserPrincipalName")
    def owner_user_principal_name(self) -> pulumi.Output[Optional[str]]:
        """
        The user principal name of the virtual machine owner.
        """
        return pulumi.get(self, "owner_user_principal_name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        """
        The password of the virtual machine administrator.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="planId")
    def plan_id(self) -> pulumi.Output[Optional[str]]:
        """
        The id of the plan associated with the virtual machine image
        """
        return pulumi.get(self, "plan_id")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning status of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="scheduleParameters")
    def schedule_parameters(self) -> pulumi.Output[Optional[Sequence['outputs.ScheduleCreationParameterResponse']]]:
        """
        Virtual Machine schedules to be created
        """
        return pulumi.get(self, "schedule_parameters")

    @property
    @pulumi.getter
    def size(self) -> pulumi.Output[Optional[str]]:
        """
        The size of the virtual machine.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter(name="sshKey")
    def ssh_key(self) -> pulumi.Output[Optional[str]]:
        """
        The SSH key of the virtual machine administrator.
        """
        return pulumi.get(self, "ssh_key")

    @property
    @pulumi.getter(name="storageType")
    def storage_type(self) -> pulumi.Output[Optional[str]]:
        """
        Storage type to use for virtual machine (i.e. Standard, Premium).
        """
        return pulumi.get(self, "storage_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="uniqueIdentifier")
    def unique_identifier(self) -> pulumi.Output[str]:
        """
        The unique immutable identifier of a resource (Guid).
        """
        return pulumi.get(self, "unique_identifier")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[Optional[str]]:
        """
        The user name of the virtual machine.
        """
        return pulumi.get(self, "user_name")

    @property
    @pulumi.getter(name="virtualMachineCreationSource")
    def virtual_machine_creation_source(self) -> pulumi.Output[Optional[str]]:
        """
        Tells source of creation of lab virtual machine. Output property only.
        """
        return pulumi.get(self, "virtual_machine_creation_source")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

