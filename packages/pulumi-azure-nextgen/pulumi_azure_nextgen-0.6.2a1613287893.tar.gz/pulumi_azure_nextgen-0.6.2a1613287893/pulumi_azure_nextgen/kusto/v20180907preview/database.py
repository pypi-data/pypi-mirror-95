# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = ['Database']


class Database(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 hot_cache_period_in_days: Optional[pulumi.Input[int]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 soft_delete_period_in_days: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Class representing a Kusto database.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_name: The name of the Kusto cluster.
        :param pulumi.Input[str] database_name: The name of the database in the Kusto cluster.
        :param pulumi.Input[int] hot_cache_period_in_days: The number of days of data that should be kept in cache for fast queries.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_group_name: The name of the resource group containing the Kusto cluster.
        :param pulumi.Input[int] soft_delete_period_in_days: The number of days data should be kept before it stops being accessible to queries.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
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

            if cluster_name is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_name'")
            __props__['cluster_name'] = cluster_name
            if database_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_name'")
            __props__['database_name'] = database_name
            __props__['hot_cache_period_in_days'] = hot_cache_period_in_days
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if soft_delete_period_in_days is None and not opts.urn:
                raise TypeError("Missing required property 'soft_delete_period_in_days'")
            __props__['soft_delete_period_in_days'] = soft_delete_period_in_days
            __props__['tags'] = tags
            __props__['etag'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['statistics'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:kusto:Database"), pulumi.Alias(type_="azure-nextgen:kusto/latest:Database"), pulumi.Alias(type_="azure-nextgen:kusto/v20170907privatepreview:Database"), pulumi.Alias(type_="azure-nextgen:kusto/v20190121:Database"), pulumi.Alias(type_="azure-nextgen:kusto/v20190515:Database"), pulumi.Alias(type_="azure-nextgen:kusto/v20190907:Database"), pulumi.Alias(type_="azure-nextgen:kusto/v20191109:Database"), pulumi.Alias(type_="azure-nextgen:kusto/v20200215:Database"), pulumi.Alias(type_="azure-nextgen:kusto/v20200614:Database"), pulumi.Alias(type_="azure-nextgen:kusto/v20200918:Database")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Database, __self__).__init__(
            'azure-nextgen:kusto/v20180907preview:Database',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Database':
        """
        Get an existing Database resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Database(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        An ETag of the resource created.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="hotCachePeriodInDays")
    def hot_cache_period_in_days(self) -> pulumi.Output[Optional[int]]:
        """
        The number of days of data that should be kept in cache for fast queries.
        """
        return pulumi.get(self, "hot_cache_period_in_days")

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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioned state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="softDeletePeriodInDays")
    def soft_delete_period_in_days(self) -> pulumi.Output[int]:
        """
        The number of days data should be kept before it stops being accessible to queries.
        """
        return pulumi.get(self, "soft_delete_period_in_days")

    @property
    @pulumi.getter
    def statistics(self) -> pulumi.Output['outputs.DatabaseStatisticsResponse']:
        """
        The statistics of the database.
        """
        return pulumi.get(self, "statistics")

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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

