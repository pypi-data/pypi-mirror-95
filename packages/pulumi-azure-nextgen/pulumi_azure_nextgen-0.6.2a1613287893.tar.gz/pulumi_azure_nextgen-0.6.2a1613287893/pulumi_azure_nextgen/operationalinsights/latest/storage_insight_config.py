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

__all__ = ['StorageInsightConfig']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:operationalinsights:StorageInsightConfig'.""", DeprecationWarning)


class StorageInsightConfig(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:operationalinsights:StorageInsightConfig'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 e_tag: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_account: Optional[pulumi.Input[pulumi.InputType['StorageAccountArgs']]] = None,
                 storage_insight_name: Optional[pulumi.Input[str]] = None,
                 tables: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The top level storage insight resource container.
        Latest API Version: 2020-08-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] containers: The names of the blob containers that the workspace should read
        :param pulumi.Input[str] e_tag: The ETag of the storage insight.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[pulumi.InputType['StorageAccountArgs']] storage_account: The storage account connection details
        :param pulumi.Input[str] storage_insight_name: Name of the storageInsightsConfigs resource
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tables: The names of the Azure tables that the workspace should read
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        pulumi.log.warn("StorageInsightConfig is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:operationalinsights:StorageInsightConfig'.")
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

            __props__['containers'] = containers
            __props__['e_tag'] = e_tag
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if storage_account is None and not opts.urn:
                raise TypeError("Missing required property 'storage_account'")
            __props__['storage_account'] = storage_account
            if storage_insight_name is None and not opts.urn:
                raise TypeError("Missing required property 'storage_insight_name'")
            __props__['storage_insight_name'] = storage_insight_name
            __props__['tables'] = tables
            __props__['tags'] = tags
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__['workspace_name'] = workspace_name
            __props__['name'] = None
            __props__['status'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:operationalinsights:StorageInsightConfig"), pulumi.Alias(type_="azure-nextgen:operationalinsights/v20150320:StorageInsightConfig"), pulumi.Alias(type_="azure-nextgen:operationalinsights/v20200301preview:StorageInsightConfig"), pulumi.Alias(type_="azure-nextgen:operationalinsights/v20200801:StorageInsightConfig")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StorageInsightConfig, __self__).__init__(
            'azure-nextgen:operationalinsights/latest:StorageInsightConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StorageInsightConfig':
        """
        Get an existing StorageInsightConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return StorageInsightConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def containers(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The names of the blob containers that the workspace should read
        """
        return pulumi.get(self, "containers")

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> pulumi.Output[Optional[str]]:
        """
        The ETag of the storage insight.
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.StorageInsightStatusResponse']:
        """
        The status of the storage insight
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="storageAccount")
    def storage_account(self) -> pulumi.Output['outputs.StorageAccountResponse']:
        """
        The storage account connection details
        """
        return pulumi.get(self, "storage_account")

    @property
    @pulumi.getter
    def tables(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The names of the Azure tables that the workspace should read
        """
        return pulumi.get(self, "tables")

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

