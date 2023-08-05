# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['SiteInstanceDeployment']


class SiteInstanceDeployment(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 active: Optional[pulumi.Input[bool]] = None,
                 author: Optional[pulumi.Input[str]] = None,
                 author_email: Optional[pulumi.Input[str]] = None,
                 deployer: Optional[pulumi.Input[str]] = None,
                 details: Optional[pulumi.Input[str]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents user credentials used for publishing activity

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] active: Active
        :param pulumi.Input[str] author: Author
        :param pulumi.Input[str] author_email: AuthorEmail
        :param pulumi.Input[str] deployer: Deployer
        :param pulumi.Input[str] details: Detail
        :param pulumi.Input[str] end_time: EndTime
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[str] instance_id: Id of web app instance
        :param pulumi.Input[str] kind: Kind of resource
        :param pulumi.Input[str] location: Resource Location
        :param pulumi.Input[str] message: Message
        :param pulumi.Input[str] name: Resource Name
        :param pulumi.Input[str] resource_group_name: Name of resource group
        :param pulumi.Input[str] start_time: StartTime
        :param pulumi.Input[int] status: Status
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Resource type
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

            __props__['active'] = active
            __props__['author'] = author
            __props__['author_email'] = author_email
            __props__['deployer'] = deployer
            __props__['details'] = details
            __props__['end_time'] = end_time
            if id is None and not opts.urn:
                raise TypeError("Missing required property 'id'")
            __props__['id'] = id
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__['instance_id'] = instance_id
            __props__['kind'] = kind
            __props__['location'] = location
            __props__['message'] = message
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['start_time'] = start_time
            __props__['status'] = status
            __props__['tags'] = tags
            __props__['type'] = type
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web:SiteInstanceDeployment"), pulumi.Alias(type_="azure-nextgen:web/latest:SiteInstanceDeployment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SiteInstanceDeployment, __self__).__init__(
            'azure-nextgen:web/v20150801:SiteInstanceDeployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SiteInstanceDeployment':
        """
        Get an existing SiteInstanceDeployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return SiteInstanceDeployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def active(self) -> pulumi.Output[Optional[bool]]:
        """
        Active
        """
        return pulumi.get(self, "active")

    @property
    @pulumi.getter
    def author(self) -> pulumi.Output[Optional[str]]:
        """
        Author
        """
        return pulumi.get(self, "author")

    @property
    @pulumi.getter(name="authorEmail")
    def author_email(self) -> pulumi.Output[Optional[str]]:
        """
        AuthorEmail
        """
        return pulumi.get(self, "author_email")

    @property
    @pulumi.getter
    def deployer(self) -> pulumi.Output[Optional[str]]:
        """
        Deployer
        """
        return pulumi.get(self, "deployer")

    @property
    @pulumi.getter
    def details(self) -> pulumi.Output[Optional[str]]:
        """
        Detail
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[Optional[str]]:
        """
        EndTime
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def message(self) -> pulumi.Output[Optional[str]]:
        """
        Message
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[Optional[str]]:
        """
        StartTime
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[int]]:
        """
        Status
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

