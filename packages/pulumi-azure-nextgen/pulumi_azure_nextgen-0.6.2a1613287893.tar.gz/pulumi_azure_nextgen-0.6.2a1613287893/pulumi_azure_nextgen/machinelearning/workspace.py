# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['Workspace']


class Workspace(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_vault_identifier_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 owner_email: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_storage_account_id: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        An object that represents a machine learning workspace.
        API Version: 2016-04-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_vault_identifier_id: The key vault identifier used for encrypted workspaces.
        :param pulumi.Input[str] location: The location of the resource. This cannot be changed after the resource is created.
        :param pulumi.Input[str] owner_email: The email id of the owner for this workspace.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the machine learning workspace belongs.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags of the resource.
        :param pulumi.Input[str] user_storage_account_id: The fully qualified arm id of the storage account associated with this workspace.
        :param pulumi.Input[str] workspace_name: The name of the machine learning workspace.
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

            __props__['key_vault_identifier_id'] = key_vault_identifier_id
            __props__['location'] = location
            if owner_email is None and not opts.urn:
                raise TypeError("Missing required property 'owner_email'")
            __props__['owner_email'] = owner_email
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            if user_storage_account_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_storage_account_id'")
            __props__['user_storage_account_id'] = user_storage_account_id
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__['workspace_name'] = workspace_name
            __props__['creation_time'] = None
            __props__['name'] = None
            __props__['studio_endpoint'] = None
            __props__['type'] = None
            __props__['workspace_id'] = None
            __props__['workspace_state'] = None
            __props__['workspace_type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:machinelearning/latest:Workspace"), pulumi.Alias(type_="azure-nextgen:machinelearning/v20160401:Workspace"), pulumi.Alias(type_="azure-nextgen:machinelearning/v20191001:Workspace")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Workspace, __self__).__init__(
            'azure-nextgen:machinelearning:Workspace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Workspace':
        """
        Get an existing Workspace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Workspace(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        The creation time for this workspace resource.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="keyVaultIdentifierId")
    def key_vault_identifier_id(self) -> pulumi.Output[Optional[str]]:
        """
        The key vault identifier used for encrypted workspaces.
        """
        return pulumi.get(self, "key_vault_identifier_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ownerEmail")
    def owner_email(self) -> pulumi.Output[str]:
        """
        The email id of the owner for this workspace.
        """
        return pulumi.get(self, "owner_email")

    @property
    @pulumi.getter(name="studioEndpoint")
    def studio_endpoint(self) -> pulumi.Output[str]:
        """
        The regional endpoint for the machine learning studio service which hosts this workspace.
        """
        return pulumi.get(self, "studio_endpoint")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userStorageAccountId")
    def user_storage_account_id(self) -> pulumi.Output[str]:
        """
        The fully qualified arm id of the storage account associated with this workspace.
        """
        return pulumi.get(self, "user_storage_account_id")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Output[str]:
        """
        The immutable id associated with this workspace.
        """
        return pulumi.get(self, "workspace_id")

    @property
    @pulumi.getter(name="workspaceState")
    def workspace_state(self) -> pulumi.Output[str]:
        """
        The current state of workspace resource.
        """
        return pulumi.get(self, "workspace_state")

    @property
    @pulumi.getter(name="workspaceType")
    def workspace_type(self) -> pulumi.Output[str]:
        """
        The type of this workspace.
        """
        return pulumi.get(self, "workspace_type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

