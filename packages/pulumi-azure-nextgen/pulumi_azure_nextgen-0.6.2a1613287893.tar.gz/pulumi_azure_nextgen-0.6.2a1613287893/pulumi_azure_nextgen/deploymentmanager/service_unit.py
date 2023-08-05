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

__all__ = ['ServiceUnit']


class ServiceUnit(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifacts: Optional[pulumi.Input[pulumi.InputType['ServiceUnitArtifactsArgs']]] = None,
                 deployment_mode: Optional[pulumi.Input['DeploymentMode']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 service_topology_name: Optional[pulumi.Input[str]] = None,
                 service_unit_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_resource_group: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents the response of a service unit resource.
        API Version: 2019-11-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ServiceUnitArtifactsArgs']] artifacts: The artifacts for the service unit.
        :param pulumi.Input['DeploymentMode'] deployment_mode: Describes the type of ARM deployment to be performed on the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] service_name: The name of the service resource.
        :param pulumi.Input[str] service_topology_name: The name of the service topology .
        :param pulumi.Input[str] service_unit_name: The name of the service unit resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] target_resource_group: The Azure Resource Group to which the resources in the service unit belong to or should be deployed to.
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

            __props__['artifacts'] = artifacts
            if deployment_mode is None and not opts.urn:
                raise TypeError("Missing required property 'deployment_mode'")
            __props__['deployment_mode'] = deployment_mode
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__['service_name'] = service_name
            if service_topology_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_topology_name'")
            __props__['service_topology_name'] = service_topology_name
            if service_unit_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_unit_name'")
            __props__['service_unit_name'] = service_unit_name
            __props__['tags'] = tags
            if target_resource_group is None and not opts.urn:
                raise TypeError("Missing required property 'target_resource_group'")
            __props__['target_resource_group'] = target_resource_group
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:deploymentmanager/v20180901preview:ServiceUnit"), pulumi.Alias(type_="azure-nextgen:deploymentmanager/v20191101preview:ServiceUnit")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ServiceUnit, __self__).__init__(
            'azure-nextgen:deploymentmanager:ServiceUnit',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ServiceUnit':
        """
        Get an existing ServiceUnit resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ServiceUnit(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def artifacts(self) -> pulumi.Output[Optional['outputs.ServiceUnitArtifactsResponse']]:
        """
        The artifacts for the service unit.
        """
        return pulumi.get(self, "artifacts")

    @property
    @pulumi.getter(name="deploymentMode")
    def deployment_mode(self) -> pulumi.Output[str]:
        """
        Describes the type of ARM deployment to be performed on the resource.
        """
        return pulumi.get(self, "deployment_mode")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetResourceGroup")
    def target_resource_group(self) -> pulumi.Output[str]:
        """
        The Azure Resource Group to which the resources in the service unit belong to or should be deployed to.
        """
        return pulumi.get(self, "target_resource_group")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

