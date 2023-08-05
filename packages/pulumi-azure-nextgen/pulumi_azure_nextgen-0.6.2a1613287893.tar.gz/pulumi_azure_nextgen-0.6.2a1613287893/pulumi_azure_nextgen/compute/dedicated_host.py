# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['DedicatedHost']


class DedicatedHost(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_replace_on_failure: Optional[pulumi.Input[bool]] = None,
                 host_group_name: Optional[pulumi.Input[str]] = None,
                 host_name: Optional[pulumi.Input[str]] = None,
                 license_type: Optional[pulumi.Input['DedicatedHostLicenseTypes']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 platform_fault_domain: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Specifies information about the Dedicated host.
        API Version: 2020-12-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_replace_on_failure: Specifies whether the dedicated host should be replaced automatically in case of a failure. The value is defaulted to 'true' when not provided.
        :param pulumi.Input[str] host_group_name: The name of the dedicated host group.
        :param pulumi.Input[str] host_name: The name of the dedicated host .
        :param pulumi.Input['DedicatedHostLicenseTypes'] license_type: Specifies the software license type that will be applied to the VMs deployed on the dedicated host. <br><br> Possible values are: <br><br> **None** <br><br> **Windows_Server_Hybrid** <br><br> **Windows_Server_Perpetual** <br><br> Default: **None**
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[int] platform_fault_domain: Fault domain of the dedicated host within a dedicated host group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: SKU of the dedicated host for Hardware Generation and VM family. Only name is required to be set. List Microsoft.Compute SKUs for a list of possible values.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
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

            __props__['auto_replace_on_failure'] = auto_replace_on_failure
            if host_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'host_group_name'")
            __props__['host_group_name'] = host_group_name
            if host_name is None and not opts.urn:
                raise TypeError("Missing required property 'host_name'")
            __props__['host_name'] = host_name
            __props__['license_type'] = license_type
            __props__['location'] = location
            __props__['platform_fault_domain'] = platform_fault_domain
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if sku is None and not opts.urn:
                raise TypeError("Missing required property 'sku'")
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['host_id'] = None
            __props__['instance_view'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['provisioning_time'] = None
            __props__['type'] = None
            __props__['virtual_machines'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:compute/latest:DedicatedHost"), pulumi.Alias(type_="azure-nextgen:compute/v20190301:DedicatedHost"), pulumi.Alias(type_="azure-nextgen:compute/v20190701:DedicatedHost"), pulumi.Alias(type_="azure-nextgen:compute/v20191201:DedicatedHost"), pulumi.Alias(type_="azure-nextgen:compute/v20200601:DedicatedHost"), pulumi.Alias(type_="azure-nextgen:compute/v20201201:DedicatedHost")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DedicatedHost, __self__).__init__(
            'azure-nextgen:compute:DedicatedHost',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DedicatedHost':
        """
        Get an existing DedicatedHost resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return DedicatedHost(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoReplaceOnFailure")
    def auto_replace_on_failure(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether the dedicated host should be replaced automatically in case of a failure. The value is defaulted to 'true' when not provided.
        """
        return pulumi.get(self, "auto_replace_on_failure")

    @property
    @pulumi.getter(name="hostId")
    def host_id(self) -> pulumi.Output[str]:
        """
        A unique id generated and assigned to the dedicated host by the platform. <br><br> Does not change throughout the lifetime of the host.
        """
        return pulumi.get(self, "host_id")

    @property
    @pulumi.getter(name="instanceView")
    def instance_view(self) -> pulumi.Output['outputs.DedicatedHostInstanceViewResponse']:
        """
        The dedicated host instance view.
        """
        return pulumi.get(self, "instance_view")

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the software license type that will be applied to the VMs deployed on the dedicated host. <br><br> Possible values are: <br><br> **None** <br><br> **Windows_Server_Hybrid** <br><br> **Windows_Server_Perpetual** <br><br> Default: **None**
        """
        return pulumi.get(self, "license_type")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="platformFaultDomain")
    def platform_fault_domain(self) -> pulumi.Output[Optional[int]]:
        """
        Fault domain of the dedicated host within a dedicated host group.
        """
        return pulumi.get(self, "platform_fault_domain")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="provisioningTime")
    def provisioning_time(self) -> pulumi.Output[str]:
        """
        The date when the host was first provisioned.
        """
        return pulumi.get(self, "provisioning_time")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.SkuResponse']:
        """
        SKU of the dedicated host for Hardware Generation and VM family. Only name is required to be set. List Microsoft.Compute SKUs for a list of possible values.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualMachines")
    def virtual_machines(self) -> pulumi.Output[Sequence['outputs.SubResourceReadOnlyResponse']]:
        """
        A list of references to all virtual machines in the Dedicated Host.
        """
        return pulumi.get(self, "virtual_machines")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

