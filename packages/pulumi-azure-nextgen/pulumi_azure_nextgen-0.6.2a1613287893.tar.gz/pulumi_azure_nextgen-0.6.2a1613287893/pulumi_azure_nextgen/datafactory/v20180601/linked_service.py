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

__all__ = ['LinkedService']


class LinkedService(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 factory_name: Optional[pulumi.Input[str]] = None,
                 linked_service_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union[pulumi.InputType['AmazonMWSLinkedServiceArgs'], pulumi.InputType['AmazonRedshiftLinkedServiceArgs'], pulumi.InputType['AmazonS3LinkedServiceArgs'], pulumi.InputType['AzureBatchLinkedServiceArgs'], pulumi.InputType['AzureBlobFSLinkedServiceArgs'], pulumi.InputType['AzureBlobStorageLinkedServiceArgs'], pulumi.InputType['AzureDataExplorerLinkedServiceArgs'], pulumi.InputType['AzureDataLakeAnalyticsLinkedServiceArgs'], pulumi.InputType['AzureDataLakeStoreLinkedServiceArgs'], pulumi.InputType['AzureDatabricksDeltaLakeLinkedServiceArgs'], pulumi.InputType['AzureDatabricksLinkedServiceArgs'], pulumi.InputType['AzureFileStorageLinkedServiceArgs'], pulumi.InputType['AzureFunctionLinkedServiceArgs'], pulumi.InputType['AzureKeyVaultLinkedServiceArgs'], pulumi.InputType['AzureMLLinkedServiceArgs'], pulumi.InputType['AzureMLServiceLinkedServiceArgs'], pulumi.InputType['AzureMariaDBLinkedServiceArgs'], pulumi.InputType['AzureMySqlLinkedServiceArgs'], pulumi.InputType['AzurePostgreSqlLinkedServiceArgs'], pulumi.InputType['AzureSearchLinkedServiceArgs'], pulumi.InputType['AzureSqlDWLinkedServiceArgs'], pulumi.InputType['AzureSqlDatabaseLinkedServiceArgs'], pulumi.InputType['AzureSqlMILinkedServiceArgs'], pulumi.InputType['AzureStorageLinkedServiceArgs'], pulumi.InputType['AzureTableStorageLinkedServiceArgs'], pulumi.InputType['CassandraLinkedServiceArgs'], pulumi.InputType['CommonDataServiceForAppsLinkedServiceArgs'], pulumi.InputType['ConcurLinkedServiceArgs'], pulumi.InputType['CosmosDbLinkedServiceArgs'], pulumi.InputType['CosmosDbMongoDbApiLinkedServiceArgs'], pulumi.InputType['CouchbaseLinkedServiceArgs'], pulumi.InputType['CustomDataSourceLinkedServiceArgs'], pulumi.InputType['Db2LinkedServiceArgs'], pulumi.InputType['DrillLinkedServiceArgs'], pulumi.InputType['DynamicsAXLinkedServiceArgs'], pulumi.InputType['DynamicsCrmLinkedServiceArgs'], pulumi.InputType['DynamicsLinkedServiceArgs'], pulumi.InputType['EloquaLinkedServiceArgs'], pulumi.InputType['FileServerLinkedServiceArgs'], pulumi.InputType['FtpServerLinkedServiceArgs'], pulumi.InputType['GoogleAdWordsLinkedServiceArgs'], pulumi.InputType['GoogleBigQueryLinkedServiceArgs'], pulumi.InputType['GoogleCloudStorageLinkedServiceArgs'], pulumi.InputType['GreenplumLinkedServiceArgs'], pulumi.InputType['HBaseLinkedServiceArgs'], pulumi.InputType['HDInsightLinkedServiceArgs'], pulumi.InputType['HDInsightOnDemandLinkedServiceArgs'], pulumi.InputType['HdfsLinkedServiceArgs'], pulumi.InputType['HiveLinkedServiceArgs'], pulumi.InputType['HttpLinkedServiceArgs'], pulumi.InputType['HubspotLinkedServiceArgs'], pulumi.InputType['ImpalaLinkedServiceArgs'], pulumi.InputType['InformixLinkedServiceArgs'], pulumi.InputType['JiraLinkedServiceArgs'], pulumi.InputType['MagentoLinkedServiceArgs'], pulumi.InputType['MariaDBLinkedServiceArgs'], pulumi.InputType['MarketoLinkedServiceArgs'], pulumi.InputType['MicrosoftAccessLinkedServiceArgs'], pulumi.InputType['MongoDbAtlasLinkedServiceArgs'], pulumi.InputType['MongoDbLinkedServiceArgs'], pulumi.InputType['MongoDbV2LinkedServiceArgs'], pulumi.InputType['MySqlLinkedServiceArgs'], pulumi.InputType['NetezzaLinkedServiceArgs'], pulumi.InputType['ODataLinkedServiceArgs'], pulumi.InputType['OdbcLinkedServiceArgs'], pulumi.InputType['Office365LinkedServiceArgs'], pulumi.InputType['OracleLinkedServiceArgs'], pulumi.InputType['OracleServiceCloudLinkedServiceArgs'], pulumi.InputType['PaypalLinkedServiceArgs'], pulumi.InputType['PhoenixLinkedServiceArgs'], pulumi.InputType['PostgreSqlLinkedServiceArgs'], pulumi.InputType['PrestoLinkedServiceArgs'], pulumi.InputType['QuickBooksLinkedServiceArgs'], pulumi.InputType['ResponsysLinkedServiceArgs'], pulumi.InputType['RestServiceLinkedServiceArgs'], pulumi.InputType['SalesforceLinkedServiceArgs'], pulumi.InputType['SalesforceMarketingCloudLinkedServiceArgs'], pulumi.InputType['SalesforceServiceCloudLinkedServiceArgs'], pulumi.InputType['SapBWLinkedServiceArgs'], pulumi.InputType['SapCloudForCustomerLinkedServiceArgs'], pulumi.InputType['SapEccLinkedServiceArgs'], pulumi.InputType['SapHanaLinkedServiceArgs'], pulumi.InputType['SapOpenHubLinkedServiceArgs'], pulumi.InputType['SapTableLinkedServiceArgs'], pulumi.InputType['ServiceNowLinkedServiceArgs'], pulumi.InputType['SftpServerLinkedServiceArgs'], pulumi.InputType['SharePointOnlineListLinkedServiceArgs'], pulumi.InputType['ShopifyLinkedServiceArgs'], pulumi.InputType['SnowflakeLinkedServiceArgs'], pulumi.InputType['SparkLinkedServiceArgs'], pulumi.InputType['SqlServerLinkedServiceArgs'], pulumi.InputType['SquareLinkedServiceArgs'], pulumi.InputType['SybaseLinkedServiceArgs'], pulumi.InputType['TeradataLinkedServiceArgs'], pulumi.InputType['VerticaLinkedServiceArgs'], pulumi.InputType['WebLinkedServiceArgs'], pulumi.InputType['XeroLinkedServiceArgs'], pulumi.InputType['ZohoLinkedServiceArgs']]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Linked service resource type.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] factory_name: The factory name.
        :param pulumi.Input[str] linked_service_name: The linked service name.
        :param pulumi.Input[Union[pulumi.InputType['AmazonMWSLinkedServiceArgs'], pulumi.InputType['AmazonRedshiftLinkedServiceArgs'], pulumi.InputType['AmazonS3LinkedServiceArgs'], pulumi.InputType['AzureBatchLinkedServiceArgs'], pulumi.InputType['AzureBlobFSLinkedServiceArgs'], pulumi.InputType['AzureBlobStorageLinkedServiceArgs'], pulumi.InputType['AzureDataExplorerLinkedServiceArgs'], pulumi.InputType['AzureDataLakeAnalyticsLinkedServiceArgs'], pulumi.InputType['AzureDataLakeStoreLinkedServiceArgs'], pulumi.InputType['AzureDatabricksDeltaLakeLinkedServiceArgs'], pulumi.InputType['AzureDatabricksLinkedServiceArgs'], pulumi.InputType['AzureFileStorageLinkedServiceArgs'], pulumi.InputType['AzureFunctionLinkedServiceArgs'], pulumi.InputType['AzureKeyVaultLinkedServiceArgs'], pulumi.InputType['AzureMLLinkedServiceArgs'], pulumi.InputType['AzureMLServiceLinkedServiceArgs'], pulumi.InputType['AzureMariaDBLinkedServiceArgs'], pulumi.InputType['AzureMySqlLinkedServiceArgs'], pulumi.InputType['AzurePostgreSqlLinkedServiceArgs'], pulumi.InputType['AzureSearchLinkedServiceArgs'], pulumi.InputType['AzureSqlDWLinkedServiceArgs'], pulumi.InputType['AzureSqlDatabaseLinkedServiceArgs'], pulumi.InputType['AzureSqlMILinkedServiceArgs'], pulumi.InputType['AzureStorageLinkedServiceArgs'], pulumi.InputType['AzureTableStorageLinkedServiceArgs'], pulumi.InputType['CassandraLinkedServiceArgs'], pulumi.InputType['CommonDataServiceForAppsLinkedServiceArgs'], pulumi.InputType['ConcurLinkedServiceArgs'], pulumi.InputType['CosmosDbLinkedServiceArgs'], pulumi.InputType['CosmosDbMongoDbApiLinkedServiceArgs'], pulumi.InputType['CouchbaseLinkedServiceArgs'], pulumi.InputType['CustomDataSourceLinkedServiceArgs'], pulumi.InputType['Db2LinkedServiceArgs'], pulumi.InputType['DrillLinkedServiceArgs'], pulumi.InputType['DynamicsAXLinkedServiceArgs'], pulumi.InputType['DynamicsCrmLinkedServiceArgs'], pulumi.InputType['DynamicsLinkedServiceArgs'], pulumi.InputType['EloquaLinkedServiceArgs'], pulumi.InputType['FileServerLinkedServiceArgs'], pulumi.InputType['FtpServerLinkedServiceArgs'], pulumi.InputType['GoogleAdWordsLinkedServiceArgs'], pulumi.InputType['GoogleBigQueryLinkedServiceArgs'], pulumi.InputType['GoogleCloudStorageLinkedServiceArgs'], pulumi.InputType['GreenplumLinkedServiceArgs'], pulumi.InputType['HBaseLinkedServiceArgs'], pulumi.InputType['HDInsightLinkedServiceArgs'], pulumi.InputType['HDInsightOnDemandLinkedServiceArgs'], pulumi.InputType['HdfsLinkedServiceArgs'], pulumi.InputType['HiveLinkedServiceArgs'], pulumi.InputType['HttpLinkedServiceArgs'], pulumi.InputType['HubspotLinkedServiceArgs'], pulumi.InputType['ImpalaLinkedServiceArgs'], pulumi.InputType['InformixLinkedServiceArgs'], pulumi.InputType['JiraLinkedServiceArgs'], pulumi.InputType['MagentoLinkedServiceArgs'], pulumi.InputType['MariaDBLinkedServiceArgs'], pulumi.InputType['MarketoLinkedServiceArgs'], pulumi.InputType['MicrosoftAccessLinkedServiceArgs'], pulumi.InputType['MongoDbAtlasLinkedServiceArgs'], pulumi.InputType['MongoDbLinkedServiceArgs'], pulumi.InputType['MongoDbV2LinkedServiceArgs'], pulumi.InputType['MySqlLinkedServiceArgs'], pulumi.InputType['NetezzaLinkedServiceArgs'], pulumi.InputType['ODataLinkedServiceArgs'], pulumi.InputType['OdbcLinkedServiceArgs'], pulumi.InputType['Office365LinkedServiceArgs'], pulumi.InputType['OracleLinkedServiceArgs'], pulumi.InputType['OracleServiceCloudLinkedServiceArgs'], pulumi.InputType['PaypalLinkedServiceArgs'], pulumi.InputType['PhoenixLinkedServiceArgs'], pulumi.InputType['PostgreSqlLinkedServiceArgs'], pulumi.InputType['PrestoLinkedServiceArgs'], pulumi.InputType['QuickBooksLinkedServiceArgs'], pulumi.InputType['ResponsysLinkedServiceArgs'], pulumi.InputType['RestServiceLinkedServiceArgs'], pulumi.InputType['SalesforceLinkedServiceArgs'], pulumi.InputType['SalesforceMarketingCloudLinkedServiceArgs'], pulumi.InputType['SalesforceServiceCloudLinkedServiceArgs'], pulumi.InputType['SapBWLinkedServiceArgs'], pulumi.InputType['SapCloudForCustomerLinkedServiceArgs'], pulumi.InputType['SapEccLinkedServiceArgs'], pulumi.InputType['SapHanaLinkedServiceArgs'], pulumi.InputType['SapOpenHubLinkedServiceArgs'], pulumi.InputType['SapTableLinkedServiceArgs'], pulumi.InputType['ServiceNowLinkedServiceArgs'], pulumi.InputType['SftpServerLinkedServiceArgs'], pulumi.InputType['SharePointOnlineListLinkedServiceArgs'], pulumi.InputType['ShopifyLinkedServiceArgs'], pulumi.InputType['SnowflakeLinkedServiceArgs'], pulumi.InputType['SparkLinkedServiceArgs'], pulumi.InputType['SqlServerLinkedServiceArgs'], pulumi.InputType['SquareLinkedServiceArgs'], pulumi.InputType['SybaseLinkedServiceArgs'], pulumi.InputType['TeradataLinkedServiceArgs'], pulumi.InputType['VerticaLinkedServiceArgs'], pulumi.InputType['WebLinkedServiceArgs'], pulumi.InputType['XeroLinkedServiceArgs'], pulumi.InputType['ZohoLinkedServiceArgs']]] properties: Properties of linked service.
        :param pulumi.Input[str] resource_group_name: The resource group name.
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

            if factory_name is None and not opts.urn:
                raise TypeError("Missing required property 'factory_name'")
            __props__['factory_name'] = factory_name
            if linked_service_name is None and not opts.urn:
                raise TypeError("Missing required property 'linked_service_name'")
            __props__['linked_service_name'] = linked_service_name
            if properties is None and not opts.urn:
                raise TypeError("Missing required property 'properties'")
            __props__['properties'] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['etag'] = None
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:datafactory:LinkedService"), pulumi.Alias(type_="azure-nextgen:datafactory/latest:LinkedService"), pulumi.Alias(type_="azure-nextgen:datafactory/v20170901preview:LinkedService")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(LinkedService, __self__).__init__(
            'azure-nextgen:datafactory/v20180601:LinkedService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'LinkedService':
        """
        Get an existing LinkedService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return LinkedService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Etag identifies change in the resource.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Any]:
        """
        Properties of linked service.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

