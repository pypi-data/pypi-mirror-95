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

__all__ = ['Output']


class Output(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 datasource: Optional[pulumi.Input[Union[pulumi.InputType['AzureDataLakeStoreOutputDataSourceArgs'], pulumi.InputType['AzureSqlDatabaseOutputDataSourceArgs'], pulumi.InputType['AzureTableOutputDataSourceArgs'], pulumi.InputType['BlobOutputDataSourceArgs'], pulumi.InputType['DocumentDbOutputDataSourceArgs'], pulumi.InputType['EventHubOutputDataSourceArgs'], pulumi.InputType['PowerBIOutputDataSourceArgs'], pulumi.InputType['ServiceBusQueueOutputDataSourceArgs'], pulumi.InputType['ServiceBusTopicOutputDataSourceArgs']]]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 output_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 serialization: Optional[pulumi.Input[Union[pulumi.InputType['AvroSerializationArgs'], pulumi.InputType['CsvSerializationArgs'], pulumi.InputType['JsonSerializationArgs']]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        An output object, containing all information associated with the named output. All outputs are contained under a streaming job.
        API Version: 2016-03-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[pulumi.InputType['AzureDataLakeStoreOutputDataSourceArgs'], pulumi.InputType['AzureSqlDatabaseOutputDataSourceArgs'], pulumi.InputType['AzureTableOutputDataSourceArgs'], pulumi.InputType['BlobOutputDataSourceArgs'], pulumi.InputType['DocumentDbOutputDataSourceArgs'], pulumi.InputType['EventHubOutputDataSourceArgs'], pulumi.InputType['PowerBIOutputDataSourceArgs'], pulumi.InputType['ServiceBusQueueOutputDataSourceArgs'], pulumi.InputType['ServiceBusTopicOutputDataSourceArgs']]] datasource: Describes the data source that output will be written to. Required on PUT (CreateOrReplace) requests.
        :param pulumi.Input[str] job_name: The name of the streaming job.
        :param pulumi.Input[str] name: Resource name
        :param pulumi.Input[str] output_name: The name of the output.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[Union[pulumi.InputType['AvroSerializationArgs'], pulumi.InputType['CsvSerializationArgs'], pulumi.InputType['JsonSerializationArgs']]] serialization: Describes how data from an input is serialized or how data is serialized when written to an output. Required on PUT (CreateOrReplace) requests.
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

            __props__['datasource'] = datasource
            if job_name is None and not opts.urn:
                raise TypeError("Missing required property 'job_name'")
            __props__['job_name'] = job_name
            __props__['name'] = name
            if output_name is None and not opts.urn:
                raise TypeError("Missing required property 'output_name'")
            __props__['output_name'] = output_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['serialization'] = serialization
            __props__['diagnostics'] = None
            __props__['etag'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:streamanalytics/latest:Output"), pulumi.Alias(type_="azure-nextgen:streamanalytics/v20160301:Output"), pulumi.Alias(type_="azure-nextgen:streamanalytics/v20170401preview:Output")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Output, __self__).__init__(
            'azure-nextgen:streamanalytics:Output',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Output':
        """
        Get an existing Output resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Output(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def datasource(self) -> pulumi.Output[Optional[Any]]:
        """
        Describes the data source that output will be written to. Required on PUT (CreateOrReplace) requests.
        """
        return pulumi.get(self, "datasource")

    @property
    @pulumi.getter
    def diagnostics(self) -> pulumi.Output['outputs.DiagnosticsResponse']:
        """
        Describes conditions applicable to the Input, Output, or the job overall, that warrant customer attention.
        """
        return pulumi.get(self, "diagnostics")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The current entity tag for the output. This is an opaque string. You can use it to detect whether the resource has changed between requests. You can also use it in the If-Match or If-None-Match headers for write operations for optimistic concurrency.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def serialization(self) -> pulumi.Output[Optional[Any]]:
        """
        Describes how data from an input is serialized or how data is serialized when written to an output. Required on PUT (CreateOrReplace) requests.
        """
        return pulumi.get(self, "serialization")

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

