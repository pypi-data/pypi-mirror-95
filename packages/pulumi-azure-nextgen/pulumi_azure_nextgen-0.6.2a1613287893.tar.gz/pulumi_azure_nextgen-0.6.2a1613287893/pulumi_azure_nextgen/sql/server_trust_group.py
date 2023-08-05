# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['ServerTrustGroup']


class ServerTrustGroup(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_members: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServerInfoArgs']]]]] = None,
                 location_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_trust_group_name: Optional[pulumi.Input[str]] = None,
                 trust_scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A server trust group.
        API Version: 2020-08-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServerInfoArgs']]]] group_members: Group members information for the server trust group.
        :param pulumi.Input[str] location_name: The name of the region where the resource is located.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_trust_group_name: The name of the server trust group.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] trust_scopes: Trust scope of the server trust group.
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

            if group_members is None and not opts.urn:
                raise TypeError("Missing required property 'group_members'")
            __props__['group_members'] = group_members
            if location_name is None and not opts.urn:
                raise TypeError("Missing required property 'location_name'")
            __props__['location_name'] = location_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if server_trust_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_trust_group_name'")
            __props__['server_trust_group_name'] = server_trust_group_name
            if trust_scopes is None and not opts.urn:
                raise TypeError("Missing required property 'trust_scopes'")
            __props__['trust_scopes'] = trust_scopes
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql/v20200202preview:ServerTrustGroup"), pulumi.Alias(type_="azure-nextgen:sql/v20200801preview:ServerTrustGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ServerTrustGroup, __self__).__init__(
            'azure-nextgen:sql:ServerTrustGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ServerTrustGroup':
        """
        Get an existing ServerTrustGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ServerTrustGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="groupMembers")
    def group_members(self) -> pulumi.Output[Sequence['outputs.ServerInfoResponse']]:
        """
        Group members information for the server trust group.
        """
        return pulumi.get(self, "group_members")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="trustScopes")
    def trust_scopes(self) -> pulumi.Output[Sequence[str]]:
        """
        Trust scope of the server trust group.
        """
        return pulumi.get(self, "trust_scopes")

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

