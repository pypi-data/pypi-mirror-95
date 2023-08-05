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

__all__ = ['SqlVirtualMachineGroup']


class SqlVirtualMachineGroup(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sql_image_offer: Optional[pulumi.Input[str]] = None,
                 sql_image_sku: Optional[pulumi.Input[Union[str, 'SqlVmGroupImageSku']]] = None,
                 sql_virtual_machine_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 wsfc_domain_profile: Optional[pulumi.Input[pulumi.InputType['WsfcDomainProfileArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A SQL virtual machine group.
        API Version: 2017-03-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] sql_image_offer: SQL image offer. Examples may include SQL2016-WS2016, SQL2017-WS2016.
        :param pulumi.Input[Union[str, 'SqlVmGroupImageSku']] sql_image_sku: SQL image sku.
        :param pulumi.Input[str] sql_virtual_machine_group_name: Name of the SQL virtual machine group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[pulumi.InputType['WsfcDomainProfileArgs']] wsfc_domain_profile: Cluster Active Directory domain profile.
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

            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['sql_image_offer'] = sql_image_offer
            __props__['sql_image_sku'] = sql_image_sku
            if sql_virtual_machine_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'sql_virtual_machine_group_name'")
            __props__['sql_virtual_machine_group_name'] = sql_virtual_machine_group_name
            __props__['tags'] = tags
            __props__['wsfc_domain_profile'] = wsfc_domain_profile
            __props__['cluster_configuration'] = None
            __props__['cluster_manager_type'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['scale_type'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sqlvirtualmachine/v20170301preview:SqlVirtualMachineGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SqlVirtualMachineGroup, __self__).__init__(
            'azure-nextgen:sqlvirtualmachine:SqlVirtualMachineGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SqlVirtualMachineGroup':
        """
        Get an existing SqlVirtualMachineGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return SqlVirtualMachineGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterConfiguration")
    def cluster_configuration(self) -> pulumi.Output[str]:
        """
        Cluster type.
        """
        return pulumi.get(self, "cluster_configuration")

    @property
    @pulumi.getter(name="clusterManagerType")
    def cluster_manager_type(self) -> pulumi.Output[str]:
        """
        Type of cluster manager: Windows Server Failover Cluster (WSFC), implied by the scale type of the group and the OS type.
        """
        return pulumi.get(self, "cluster_manager_type")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state to track the async operation status.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="scaleType")
    def scale_type(self) -> pulumi.Output[str]:
        """
        Scale type.
        """
        return pulumi.get(self, "scale_type")

    @property
    @pulumi.getter(name="sqlImageOffer")
    def sql_image_offer(self) -> pulumi.Output[Optional[str]]:
        """
        SQL image offer. Examples may include SQL2016-WS2016, SQL2017-WS2016.
        """
        return pulumi.get(self, "sql_image_offer")

    @property
    @pulumi.getter(name="sqlImageSku")
    def sql_image_sku(self) -> pulumi.Output[Optional[str]]:
        """
        SQL image sku.
        """
        return pulumi.get(self, "sql_image_sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="wsfcDomainProfile")
    def wsfc_domain_profile(self) -> pulumi.Output[Optional['outputs.WsfcDomainProfileResponse']]:
        """
        Cluster Active Directory domain profile.
        """
        return pulumi.get(self, "wsfc_domain_profile")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

