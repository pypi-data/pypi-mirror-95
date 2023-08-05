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

__all__ = ['Namespace']


class Namespace(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 critical: Optional[pulumi.Input[bool]] = None,
                 data_center: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 namespace_type: Optional[pulumi.Input['NamespaceType']] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 scale_unit: Optional[pulumi.Input[str]] = None,
                 service_bus_endpoint: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 subscription_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 updated_at: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Description of a Namespace resource.
        API Version: 2017-04-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_at: The time the namespace was created.
        :param pulumi.Input[bool] critical: Whether or not the namespace is set as Critical.
        :param pulumi.Input[str] data_center: Data center for the namespace
        :param pulumi.Input[bool] enabled: Whether or not the namespace is currently enabled.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] name: The name of the namespace.
        :param pulumi.Input[str] namespace_name: The namespace name.
        :param pulumi.Input['NamespaceType'] namespace_type: The namespace type.
        :param pulumi.Input[str] provisioning_state: Provisioning state of the Namespace.
        :param pulumi.Input[str] region: Specifies the targeted region in which the namespace should be created. It can be any of the following values: Australia East, Australia Southeast, Central US, East US, East US 2, West US, North Central US, South Central US, East Asia, Southeast Asia, Brazil South, Japan East, Japan West, North Europe, West Europe
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] scale_unit: ScaleUnit where the namespace gets created
        :param pulumi.Input[str] service_bus_endpoint: Endpoint you can use to perform NotificationHub operations.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The sku of the created namespace
        :param pulumi.Input[str] status: Status of the namespace. It can be any of these values:1 = Created/Active2 = Creating3 = Suspended4 = Deleting
        :param pulumi.Input[str] subscription_id: The Id of the Azure subscription associated with the namespace.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] updated_at: The time the namespace was updated.
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

            __props__['created_at'] = created_at
            __props__['critical'] = critical
            __props__['data_center'] = data_center
            __props__['enabled'] = enabled
            __props__['location'] = location
            __props__['name'] = name
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__['namespace_name'] = namespace_name
            __props__['namespace_type'] = namespace_type
            __props__['provisioning_state'] = provisioning_state
            __props__['region'] = region
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['scale_unit'] = scale_unit
            __props__['service_bus_endpoint'] = service_bus_endpoint
            __props__['sku'] = sku
            __props__['status'] = status
            __props__['subscription_id'] = subscription_id
            __props__['tags'] = tags
            __props__['updated_at'] = updated_at
            __props__['metric_id'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:notificationhubs/latest:Namespace"), pulumi.Alias(type_="azure-nextgen:notificationhubs/v20140901:Namespace"), pulumi.Alias(type_="azure-nextgen:notificationhubs/v20160301:Namespace"), pulumi.Alias(type_="azure-nextgen:notificationhubs/v20170401:Namespace")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Namespace, __self__).__init__(
            'azure-nextgen:notificationhubs:Namespace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Namespace':
        """
        Get an existing Namespace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Namespace(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[Optional[str]]:
        """
        The time the namespace was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def critical(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether or not the namespace is set as Critical.
        """
        return pulumi.get(self, "critical")

    @property
    @pulumi.getter(name="dataCenter")
    def data_center(self) -> pulumi.Output[Optional[str]]:
        """
        Data center for the namespace
        """
        return pulumi.get(self, "data_center")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether or not the namespace is currently enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="metricId")
    def metric_id(self) -> pulumi.Output[str]:
        """
        Identifier for Azure Insights metrics
        """
        return pulumi.get(self, "metric_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namespaceType")
    def namespace_type(self) -> pulumi.Output[Optional[str]]:
        """
        The namespace type.
        """
        return pulumi.get(self, "namespace_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Provisioning state of the Namespace.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the targeted region in which the namespace should be created. It can be any of the following values: Australia East, Australia Southeast, Central US, East US, East US 2, West US, North Central US, South Central US, East Asia, Southeast Asia, Brazil South, Japan East, Japan West, North Europe, West Europe
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="scaleUnit")
    def scale_unit(self) -> pulumi.Output[Optional[str]]:
        """
        ScaleUnit where the namespace gets created
        """
        return pulumi.get(self, "scale_unit")

    @property
    @pulumi.getter(name="serviceBusEndpoint")
    def service_bus_endpoint(self) -> pulumi.Output[Optional[str]]:
        """
        Endpoint you can use to perform NotificationHub operations.
        """
        return pulumi.get(self, "service_bus_endpoint")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The sku of the created namespace
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Status of the namespace. It can be any of these values:1 = Created/Active2 = Creating3 = Suspended4 = Deleting
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> pulumi.Output[Optional[str]]:
        """
        The Id of the Azure subscription associated with the namespace.
        """
        return pulumi.get(self, "subscription_id")

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
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[Optional[str]]:
        """
        The time the namespace was updated.
        """
        return pulumi.get(self, "updated_at")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

