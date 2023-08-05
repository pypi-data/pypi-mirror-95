# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['HierarchySetting']


class HierarchySetting(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 default_management_group: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 require_authorization_for_group_creation: Optional[pulumi.Input[bool]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Settings defined at the Management Group scope.
        API Version: 2020-05-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default_management_group: Settings that sets the default Management Group under which new subscriptions get added in this tenant. For example, /providers/Microsoft.Management/managementGroups/defaultGroup
        :param pulumi.Input[str] group_id: Management Group ID.
        :param pulumi.Input[bool] require_authorization_for_group_creation: Indicates whether RBAC access is required upon group creation under the root Management Group. If set to true, user will require Microsoft.Management/managementGroups/write action on the root Management Group scope in order to create new Groups directly under the root. This will prevent new users from creating new Management Groups, unless they are given access.
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

            __props__['default_management_group'] = default_management_group
            if group_id is None and not opts.urn:
                raise TypeError("Missing required property 'group_id'")
            __props__['group_id'] = group_id
            __props__['require_authorization_for_group_creation'] = require_authorization_for_group_creation
            __props__['name'] = None
            __props__['tenant_id'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:management/latest:HierarchySetting"), pulumi.Alias(type_="azure-nextgen:management/v20200201:HierarchySetting"), pulumi.Alias(type_="azure-nextgen:management/v20200501:HierarchySetting")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(HierarchySetting, __self__).__init__(
            'azure-nextgen:management:HierarchySetting',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'HierarchySetting':
        """
        Get an existing HierarchySetting resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return HierarchySetting(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="defaultManagementGroup")
    def default_management_group(self) -> pulumi.Output[Optional[str]]:
        """
        Settings that sets the default Management Group under which new subscriptions get added in this tenant. For example, /providers/Microsoft.Management/managementGroups/defaultGroup
        """
        return pulumi.get(self, "default_management_group")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the object. In this case, default.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="requireAuthorizationForGroupCreation")
    def require_authorization_for_group_creation(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether RBAC access is required upon group creation under the root Management Group. If set to true, user will require Microsoft.Management/managementGroups/write action on the root Management Group scope in order to create new Groups directly under the root. This will prevent new users from creating new Management Groups, unless they are given access.
        """
        return pulumi.get(self, "require_authorization_for_group_creation")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[Optional[str]]:
        """
        The AAD Tenant ID associated with the hierarchy settings. For example, 00000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.  For example, Microsoft.Management/managementGroups/settings.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

