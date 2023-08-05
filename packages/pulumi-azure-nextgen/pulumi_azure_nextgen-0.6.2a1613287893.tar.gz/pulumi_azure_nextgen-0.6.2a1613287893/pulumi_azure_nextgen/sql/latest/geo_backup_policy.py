# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['GeoBackupPolicy']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:sql:GeoBackupPolicy'.""", DeprecationWarning)


class GeoBackupPolicy(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:sql:GeoBackupPolicy'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 geo_backup_policy_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input['GeoBackupPolicyState']] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A database geo backup policy.
        Latest API Version: 2014-04-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database_name: The name of the database.
        :param pulumi.Input[str] geo_backup_policy_name: The name of the geo backup policy.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input['GeoBackupPolicyState'] state: The state of the geo backup policy.
        """
        pulumi.log.warn("GeoBackupPolicy is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:sql:GeoBackupPolicy'.")
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

            if database_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_name'")
            __props__['database_name'] = database_name
            if geo_backup_policy_name is None and not opts.urn:
                raise TypeError("Missing required property 'geo_backup_policy_name'")
            __props__['geo_backup_policy_name'] = geo_backup_policy_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__['server_name'] = server_name
            if state is None and not opts.urn:
                raise TypeError("Missing required property 'state'")
            __props__['state'] = state
            __props__['kind'] = None
            __props__['location'] = None
            __props__['name'] = None
            __props__['storage_type'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql:GeoBackupPolicy"), pulumi.Alias(type_="azure-nextgen:sql/v20140401:GeoBackupPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(GeoBackupPolicy, __self__).__init__(
            'azure-nextgen:sql/latest:GeoBackupPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'GeoBackupPolicy':
        """
        Get an existing GeoBackupPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return GeoBackupPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Kind of geo backup policy.  This is metadata used for the Azure portal experience.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Backup policy location.
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
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the geo backup policy.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="storageType")
    def storage_type(self) -> pulumi.Output[str]:
        """
        The storage type of the geo backup policy.
        """
        return pulumi.get(self, "storage_type")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

