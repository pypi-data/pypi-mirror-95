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

__all__ = ['Task']


class Task(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 project_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union[pulumi.InputType['ConnectToSourcePostgreSqlSyncTaskPropertiesArgs'], pulumi.InputType['ConnectToSourceSqlServerSyncTaskPropertiesArgs'], pulumi.InputType['ConnectToSourceSqlServerTaskPropertiesArgs'], pulumi.InputType['ConnectToTargetAzureDbForMySqlTaskPropertiesArgs'], pulumi.InputType['ConnectToTargetAzureDbForPostgreSqlSyncTaskPropertiesArgs'], pulumi.InputType['ConnectToTargetSqlDbTaskPropertiesArgs'], pulumi.InputType['ConnectToTargetSqlMISyncTaskPropertiesArgs'], pulumi.InputType['ConnectToTargetSqlMITaskPropertiesArgs'], pulumi.InputType['ConnectToTargetSqlSqlDbSyncTaskPropertiesArgs'], pulumi.InputType['GetTdeCertificatesSqlTaskPropertiesArgs'], pulumi.InputType['GetUserTablesSqlSyncTaskPropertiesArgs'], pulumi.InputType['GetUserTablesSqlTaskPropertiesArgs'], pulumi.InputType['MigrateMySqlAzureDbForMySqlSyncTaskPropertiesArgs'], pulumi.InputType['MigratePostgreSqlAzureDbForPostgreSqlSyncTaskPropertiesArgs'], pulumi.InputType['MigrateSqlServerSqlDbSyncTaskPropertiesArgs'], pulumi.InputType['MigrateSqlServerSqlDbTaskPropertiesArgs'], pulumi.InputType['MigrateSqlServerSqlMISyncTaskPropertiesArgs'], pulumi.InputType['MigrateSqlServerSqlMITaskPropertiesArgs'], pulumi.InputType['ValidateMigrationInputSqlServerSqlDbSyncTaskPropertiesArgs'], pulumi.InputType['ValidateMigrationInputSqlServerSqlMISyncTaskPropertiesArgs'], pulumi.InputType['ValidateMigrationInputSqlServerSqlMITaskPropertiesArgs']]]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 task_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A task resource
        API Version: 2018-04-19.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: HTTP strong entity tag value. This is ignored if submitted.
        :param pulumi.Input[str] group_name: Name of the resource group
        :param pulumi.Input[str] project_name: Name of the project
        :param pulumi.Input[Union[pulumi.InputType['ConnectToSourcePostgreSqlSyncTaskPropertiesArgs'], pulumi.InputType['ConnectToSourceSqlServerSyncTaskPropertiesArgs'], pulumi.InputType['ConnectToSourceSqlServerTaskPropertiesArgs'], pulumi.InputType['ConnectToTargetAzureDbForMySqlTaskPropertiesArgs'], pulumi.InputType['ConnectToTargetAzureDbForPostgreSqlSyncTaskPropertiesArgs'], pulumi.InputType['ConnectToTargetSqlDbTaskPropertiesArgs'], pulumi.InputType['ConnectToTargetSqlMISyncTaskPropertiesArgs'], pulumi.InputType['ConnectToTargetSqlMITaskPropertiesArgs'], pulumi.InputType['ConnectToTargetSqlSqlDbSyncTaskPropertiesArgs'], pulumi.InputType['GetTdeCertificatesSqlTaskPropertiesArgs'], pulumi.InputType['GetUserTablesSqlSyncTaskPropertiesArgs'], pulumi.InputType['GetUserTablesSqlTaskPropertiesArgs'], pulumi.InputType['MigrateMySqlAzureDbForMySqlSyncTaskPropertiesArgs'], pulumi.InputType['MigratePostgreSqlAzureDbForPostgreSqlSyncTaskPropertiesArgs'], pulumi.InputType['MigrateSqlServerSqlDbSyncTaskPropertiesArgs'], pulumi.InputType['MigrateSqlServerSqlDbTaskPropertiesArgs'], pulumi.InputType['MigrateSqlServerSqlMISyncTaskPropertiesArgs'], pulumi.InputType['MigrateSqlServerSqlMITaskPropertiesArgs'], pulumi.InputType['ValidateMigrationInputSqlServerSqlDbSyncTaskPropertiesArgs'], pulumi.InputType['ValidateMigrationInputSqlServerSqlMISyncTaskPropertiesArgs'], pulumi.InputType['ValidateMigrationInputSqlServerSqlMITaskPropertiesArgs']]] properties: Custom task properties
        :param pulumi.Input[str] service_name: Name of the service
        :param pulumi.Input[str] task_name: Name of the Task
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

            __props__['etag'] = etag
            if group_name is None and not opts.urn:
                raise TypeError("Missing required property 'group_name'")
            __props__['group_name'] = group_name
            if project_name is None and not opts.urn:
                raise TypeError("Missing required property 'project_name'")
            __props__['project_name'] = project_name
            __props__['properties'] = properties
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__['service_name'] = service_name
            if task_name is None and not opts.urn:
                raise TypeError("Missing required property 'task_name'")
            __props__['task_name'] = task_name
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:datamigration/latest:Task"), pulumi.Alias(type_="azure-nextgen:datamigration/v20171115preview:Task"), pulumi.Alias(type_="azure-nextgen:datamigration/v20180315preview:Task"), pulumi.Alias(type_="azure-nextgen:datamigration/v20180331preview:Task"), pulumi.Alias(type_="azure-nextgen:datamigration/v20180419:Task"), pulumi.Alias(type_="azure-nextgen:datamigration/v20180715preview:Task")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Task, __self__).__init__(
            'azure-nextgen:datamigration:Task',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Task':
        """
        Get an existing Task resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Task(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        HTTP strong entity tag value. This is ignored if submitted.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Any]:
        """
        Custom task properties
        """
        return pulumi.get(self, "properties")

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

