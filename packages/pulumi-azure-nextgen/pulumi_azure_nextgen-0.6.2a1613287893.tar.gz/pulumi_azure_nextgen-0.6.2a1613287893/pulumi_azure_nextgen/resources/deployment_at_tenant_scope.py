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

__all__ = ['DeploymentAtTenantScope']


class DeploymentAtTenantScope(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 deployment_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['DeploymentPropertiesArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Deployment information.
        API Version: 2020-10-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] deployment_name: The name of the deployment.
        :param pulumi.Input[str] location: The location to store the deployment data.
        :param pulumi.Input[pulumi.InputType['DeploymentPropertiesArgs']] properties: The deployment properties.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Deployment tags
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

            if deployment_name is None and not opts.urn:
                raise TypeError("Missing required property 'deployment_name'")
            __props__['deployment_name'] = deployment_name
            __props__['location'] = location
            if properties is None and not opts.urn:
                raise TypeError("Missing required property 'properties'")
            __props__['properties'] = properties
            __props__['tags'] = tags
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:resources/latest:DeploymentAtTenantScope"), pulumi.Alias(type_="azure-nextgen:resources/v20190701:DeploymentAtTenantScope"), pulumi.Alias(type_="azure-nextgen:resources/v20190801:DeploymentAtTenantScope"), pulumi.Alias(type_="azure-nextgen:resources/v20191001:DeploymentAtTenantScope"), pulumi.Alias(type_="azure-nextgen:resources/v20200601:DeploymentAtTenantScope"), pulumi.Alias(type_="azure-nextgen:resources/v20200801:DeploymentAtTenantScope"), pulumi.Alias(type_="azure-nextgen:resources/v20201001:DeploymentAtTenantScope")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DeploymentAtTenantScope, __self__).__init__(
            'azure-nextgen:resources:DeploymentAtTenantScope',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DeploymentAtTenantScope':
        """
        Get an existing DeploymentAtTenantScope resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return DeploymentAtTenantScope(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        the location of the deployment.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the deployment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.DeploymentPropertiesExtendedResponse']:
        """
        Deployment properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Deployment tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the deployment.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

