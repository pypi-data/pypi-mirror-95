# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['NotificationRecipientEmail']


class NotificationRecipientEmail(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 notification_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Recipient Email details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] email: Email identifier.
        :param pulumi.Input[str] notification_name: Notification Name Identifier.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
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

            if email is None and not opts.urn:
                raise TypeError("Missing required property 'email'")
            __props__['email'] = email
            if notification_name is None and not opts.urn:
                raise TypeError("Missing required property 'notification_name'")
            __props__['notification_name'] = notification_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__['service_name'] = service_name
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:apimanagement:NotificationRecipientEmail"), pulumi.Alias(type_="azure-nextgen:apimanagement/latest:NotificationRecipientEmail"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20170301:NotificationRecipientEmail"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20180101:NotificationRecipientEmail"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20180601preview:NotificationRecipientEmail"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20190101:NotificationRecipientEmail"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20191201:NotificationRecipientEmail"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20191201preview:NotificationRecipientEmail")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NotificationRecipientEmail, __self__).__init__(
            'azure-nextgen:apimanagement/v20200601preview:NotificationRecipientEmail',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NotificationRecipientEmail':
        """
        Get an existing NotificationRecipientEmail resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return NotificationRecipientEmail(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def email(self) -> pulumi.Output[Optional[str]]:
        """
        User Email subscribed to notification.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

