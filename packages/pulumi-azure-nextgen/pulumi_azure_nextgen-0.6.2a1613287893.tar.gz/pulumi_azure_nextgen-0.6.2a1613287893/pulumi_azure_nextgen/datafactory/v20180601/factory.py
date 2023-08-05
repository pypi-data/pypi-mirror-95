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

__all__ = ['Factory']


class Factory(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 encryption: Optional[pulumi.Input[pulumi.InputType['EncryptionConfigurationArgs']]] = None,
                 factory_name: Optional[pulumi.Input[str]] = None,
                 global_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['GlobalParameterSpecificationArgs']]]]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['FactoryIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 repo_configuration: Optional[pulumi.Input[Union[pulumi.InputType['FactoryGitHubConfigurationArgs'], pulumi.InputType['FactoryVSTSConfigurationArgs']]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Factory resource type.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['EncryptionConfigurationArgs']] encryption: Properties to enable Customer Managed Key for the factory.
        :param pulumi.Input[str] factory_name: The factory name.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['GlobalParameterSpecificationArgs']]]] global_parameters: List of parameters for factory.
        :param pulumi.Input[pulumi.InputType['FactoryIdentityArgs']] identity: Managed service identity of the factory.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[Union[str, 'PublicNetworkAccess']] public_network_access: Whether or not public network access is allowed for the data factory.
        :param pulumi.Input[Union[pulumi.InputType['FactoryGitHubConfigurationArgs'], pulumi.InputType['FactoryVSTSConfigurationArgs']]] repo_configuration: Git repo information of the factory.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
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

            __props__['encryption'] = encryption
            if factory_name is None and not opts.urn:
                raise TypeError("Missing required property 'factory_name'")
            __props__['factory_name'] = factory_name
            __props__['global_parameters'] = global_parameters
            __props__['identity'] = identity
            __props__['location'] = location
            __props__['public_network_access'] = public_network_access
            __props__['repo_configuration'] = repo_configuration
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['create_time'] = None
            __props__['e_tag'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
            __props__['version'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:datafactory:Factory"), pulumi.Alias(type_="azure-nextgen:datafactory/latest:Factory"), pulumi.Alias(type_="azure-nextgen:datafactory/v20170901preview:Factory")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Factory, __self__).__init__(
            'azure-nextgen:datafactory/v20180601:Factory',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Factory':
        """
        Get an existing Factory resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Factory(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Time the factory was created in ISO8601 format.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> pulumi.Output[str]:
        """
        Etag identifies change in the resource.
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter
    def encryption(self) -> pulumi.Output[Optional['outputs.EncryptionConfigurationResponse']]:
        """
        Properties to enable Customer Managed Key for the factory.
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter(name="globalParameters")
    def global_parameters(self) -> pulumi.Output[Optional[Mapping[str, 'outputs.GlobalParameterSpecificationResponse']]]:
        """
        List of parameters for factory.
        """
        return pulumi.get(self, "global_parameters")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.FactoryIdentityResponse']]:
        """
        Managed service identity of the factory.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Factory provisioning state, example Succeeded.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> pulumi.Output[Optional[str]]:
        """
        Whether or not public network access is allowed for the data factory.
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter(name="repoConfiguration")
    def repo_configuration(self) -> pulumi.Output[Optional[Any]]:
        """
        Git repo information of the factory.
        """
        return pulumi.get(self, "repo_configuration")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        Version of the factory.
        """
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

