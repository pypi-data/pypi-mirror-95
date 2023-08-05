# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['BatchAccount']


class BatchAccount(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 auto_storage: Optional[pulumi.Input[pulumi.InputType['AutoStorageBasePropertiesArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Contains information about an Azure Batch account.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: A name for the Batch account which must be unique within the region. Batch account names must be between 3 and 24 characters in length and must use only numbers and lowercase letters. This name is used as part of the DNS name that is used to access the Batch service in the region in which the account is created. For example: http://accountname.region.batch.azure.com/.
        :param pulumi.Input[pulumi.InputType['AutoStorageBasePropertiesArgs']] auto_storage: The properties related to auto storage account.
        :param pulumi.Input[str] location: The region in which to create the account.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the new Batch account.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The user specified tags associated with the account.
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
            __props__['auto_storage'] = auto_storage
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['account_endpoint'] = None
            __props__['active_job_and_job_schedule_quota'] = None
            __props__['core_quota'] = None
            __props__['name'] = None
            __props__['pool_quota'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:batch:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/latest:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/v20170101:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/v20170501:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/v20170901:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/v20181201:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/v20190401:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/v20190801:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/v20200301:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/v20200501:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/v20200901:BatchAccount"), pulumi.Alias(type_="azure-nextgen:batch/v20210101:BatchAccount")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(BatchAccount, __self__).__init__(
            'azure-nextgen:batch/v20151201:BatchAccount',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BatchAccount':
        """
        Get an existing BatchAccount resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return BatchAccount(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountEndpoint")
    def account_endpoint(self) -> pulumi.Output[str]:
        """
        The endpoint used by this account to interact with the Batch services.
        """
        return pulumi.get(self, "account_endpoint")

    @property
    @pulumi.getter(name="activeJobAndJobScheduleQuota")
    def active_job_and_job_schedule_quota(self) -> pulumi.Output[int]:
        """
        The active job and job schedule quota for this Batch account.
        """
        return pulumi.get(self, "active_job_and_job_schedule_quota")

    @property
    @pulumi.getter(name="autoStorage")
    def auto_storage(self) -> pulumi.Output[Optional['outputs.AutoStoragePropertiesResponse']]:
        """
        The properties and status of any auto storage account associated with the account.
        """
        return pulumi.get(self, "auto_storage")

    @property
    @pulumi.getter(name="coreQuota")
    def core_quota(self) -> pulumi.Output[int]:
        """
        The core quota for this Batch account.
        """
        return pulumi.get(self, "core_quota")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The location of the resource
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
    @pulumi.getter(name="poolQuota")
    def pool_quota(self) -> pulumi.Output[int]:
        """
        The pool quota for this Batch account.
        """
        return pulumi.get(self, "pool_quota")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        The provisioned state of the resource
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags of the resource
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

