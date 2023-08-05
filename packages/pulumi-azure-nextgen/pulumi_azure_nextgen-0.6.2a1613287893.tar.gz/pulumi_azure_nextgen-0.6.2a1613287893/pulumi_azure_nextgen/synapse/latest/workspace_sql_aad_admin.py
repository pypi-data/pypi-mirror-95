# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['WorkspaceSqlAadAdmin']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:synapse:WorkspaceSqlAadAdmin'.""", DeprecationWarning)


class WorkspaceSqlAadAdmin(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:synapse:WorkspaceSqlAadAdmin'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 administrator_type: Optional[pulumi.Input[str]] = None,
                 login: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sid: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Workspace active directory administrator
        Latest API Version: 2020-12-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] administrator_type: Workspace active directory administrator type
        :param pulumi.Input[str] login: Login of the workspace active directory administrator
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] sid: Object ID of the workspace active directory administrator
        :param pulumi.Input[str] tenant_id: Tenant ID of the workspace active directory administrator
        :param pulumi.Input[str] workspace_name: The name of the workspace
        """
        pulumi.log.warn("WorkspaceSqlAadAdmin is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:synapse:WorkspaceSqlAadAdmin'.")
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

            __props__['administrator_type'] = administrator_type
            __props__['login'] = login
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['sid'] = sid
            __props__['tenant_id'] = tenant_id
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__['workspace_name'] = workspace_name
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:synapse:WorkspaceSqlAadAdmin"), pulumi.Alias(type_="azure-nextgen:synapse/v20190601preview:WorkspaceSqlAadAdmin"), pulumi.Alias(type_="azure-nextgen:synapse/v20201201:WorkspaceSqlAadAdmin")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WorkspaceSqlAadAdmin, __self__).__init__(
            'azure-nextgen:synapse/latest:WorkspaceSqlAadAdmin',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WorkspaceSqlAadAdmin':
        """
        Get an existing WorkspaceSqlAadAdmin resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WorkspaceSqlAadAdmin(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="administratorType")
    def administrator_type(self) -> pulumi.Output[Optional[str]]:
        """
        Workspace active directory administrator type
        """
        return pulumi.get(self, "administrator_type")

    @property
    @pulumi.getter
    def login(self) -> pulumi.Output[Optional[str]]:
        """
        Login of the workspace active directory administrator
        """
        return pulumi.get(self, "login")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def sid(self) -> pulumi.Output[Optional[str]]:
        """
        Object ID of the workspace active directory administrator
        """
        return pulumi.get(self, "sid")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[Optional[str]]:
        """
        Tenant ID of the workspace active directory administrator
        """
        return pulumi.get(self, "tenant_id")

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

