# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['ApplicationPackage']


class ApplicationPackage(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        An application package which represents a particular version of an application.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the Batch account.
        :param pulumi.Input[str] application_id: The ID of the application.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the Batch account.
        :param pulumi.Input[str] version: The version of the application.
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

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__['account_name'] = account_name
            if application_id is None and not opts.urn:
                raise TypeError("Missing required property 'application_id'")
            __props__['application_id'] = application_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if version is None and not opts.urn:
                raise TypeError("Missing required property 'version'")
            __props__['version'] = version
            __props__['format'] = None
            __props__['last_activation_time'] = None
            __props__['state'] = None
            __props__['storage_url'] = None
            __props__['storage_url_expiry'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:batch:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/latest:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20151201:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20170501:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20170901:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20181201:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20190401:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20190801:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20200301:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20200501:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20200901:ApplicationPackage"), pulumi.Alias(type_="azure-nextgen:batch/v20210101:ApplicationPackage")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ApplicationPackage, __self__).__init__(
            'azure-nextgen:batch/v20170101:ApplicationPackage',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApplicationPackage':
        """
        Get an existing ApplicationPackage resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ApplicationPackage(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def format(self) -> pulumi.Output[str]:
        """
        The format of the application package, if the package is active.
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter(name="lastActivationTime")
    def last_activation_time(self) -> pulumi.Output[str]:
        """
        The time at which the package was last activated, if the package is active.
        """
        return pulumi.get(self, "last_activation_time")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the application package.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="storageUrl")
    def storage_url(self) -> pulumi.Output[str]:
        """
        The storage URL at which the application package is stored.
        """
        return pulumi.get(self, "storage_url")

    @property
    @pulumi.getter(name="storageUrlExpiry")
    def storage_url_expiry(self) -> pulumi.Output[str]:
        """
        The UTC time at which the storage URL will expire.
        """
        return pulumi.get(self, "storage_url_expiry")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        The version of the application package. 
        """
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

