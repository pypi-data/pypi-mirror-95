# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['MigrationConfig']


class MigrationConfig(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config_name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 post_migration_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 target_namespace: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Single item in List or Get Migration Config operation
        API Version: 2017-04-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] config_name: The configuration name. Should always be "$default".
        :param pulumi.Input[str] namespace_name: The namespace name
        :param pulumi.Input[str] post_migration_name: Name to access Standard Namespace after migration
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[str] target_namespace: Existing premium Namespace ARM Id name which has no entities, will be used for migration
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

            if config_name is None and not opts.urn:
                raise TypeError("Missing required property 'config_name'")
            __props__['config_name'] = config_name
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__['namespace_name'] = namespace_name
            if post_migration_name is None and not opts.urn:
                raise TypeError("Missing required property 'post_migration_name'")
            __props__['post_migration_name'] = post_migration_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if target_namespace is None and not opts.urn:
                raise TypeError("Missing required property 'target_namespace'")
            __props__['target_namespace'] = target_namespace
            __props__['migration_state'] = None
            __props__['name'] = None
            __props__['pending_replication_operations_count'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:servicebus/latest:MigrationConfig"), pulumi.Alias(type_="azure-nextgen:servicebus/v20170401:MigrationConfig"), pulumi.Alias(type_="azure-nextgen:servicebus/v20180101preview:MigrationConfig")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MigrationConfig, __self__).__init__(
            'azure-nextgen:servicebus:MigrationConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MigrationConfig':
        """
        Get an existing MigrationConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return MigrationConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="migrationState")
    def migration_state(self) -> pulumi.Output[str]:
        """
        State in which Standard to Premium Migration is, possible values : Unknown, Reverting, Completing, Initiating, Syncing, Active
        """
        return pulumi.get(self, "migration_state")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pendingReplicationOperationsCount")
    def pending_replication_operations_count(self) -> pulumi.Output[float]:
        """
        Number of entities pending to be replicated.
        """
        return pulumi.get(self, "pending_replication_operations_count")

    @property
    @pulumi.getter(name="postMigrationName")
    def post_migration_name(self) -> pulumi.Output[str]:
        """
        Name to access Standard Namespace after migration
        """
        return pulumi.get(self, "post_migration_name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of Migration Configuration 
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="targetNamespace")
    def target_namespace(self) -> pulumi.Output[str]:
        """
        Existing premium Namespace ARM Id name which has no entities, will be used for migration
        """
        return pulumi.get(self, "target_namespace")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

