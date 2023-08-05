# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from ._enums import *

__all__ = ['Registration']


class Registration(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[Union[str, 'Location']]] = None,
                 registration_name: Optional[pulumi.Input[str]] = None,
                 registration_token: Optional[pulumi.Input[str]] = None,
                 resource_group: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Registration information.
        API Version: 2017-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'Location']] location: Location of the resource.
        :param pulumi.Input[str] registration_name: Name of the Azure Stack registration.
        :param pulumi.Input[str] registration_token: The token identifying registered Azure Stack
        :param pulumi.Input[str] resource_group: Name of the resource group.
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
            if registration_name is None and not opts.urn:
                raise TypeError("Missing required property 'registration_name'")
            __props__['registration_name'] = registration_name
            if registration_token is None and not opts.urn:
                raise TypeError("Missing required property 'registration_token'")
            __props__['registration_token'] = registration_token
            if resource_group is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group'")
            __props__['resource_group'] = resource_group
            __props__['billing_model'] = None
            __props__['cloud_id'] = None
            __props__['etag'] = None
            __props__['name'] = None
            __props__['object_id'] = None
            __props__['tags'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:azurestack/latest:Registration"), pulumi.Alias(type_="azure-nextgen:azurestack/v20170601:Registration"), pulumi.Alias(type_="azure-nextgen:azurestack/v20200601preview:Registration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Registration, __self__).__init__(
            'azure-nextgen:azurestack:Registration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Registration':
        """
        Get an existing Registration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Registration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="billingModel")
    def billing_model(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the billing mode for the Azure Stack registration.
        """
        return pulumi.get(self, "billing_model")

    @property
    @pulumi.getter(name="cloudId")
    def cloud_id(self) -> pulumi.Output[Optional[str]]:
        """
        The identifier of the registered Azure Stack.
        """
        return pulumi.get(self, "cloud_id")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        The entity tag used for optimistic concurrency when modifying the resource.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> pulumi.Output[Optional[str]]:
        """
        The object identifier associated with the Azure Stack connecting to Azure.
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Custom tags for the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of Resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

