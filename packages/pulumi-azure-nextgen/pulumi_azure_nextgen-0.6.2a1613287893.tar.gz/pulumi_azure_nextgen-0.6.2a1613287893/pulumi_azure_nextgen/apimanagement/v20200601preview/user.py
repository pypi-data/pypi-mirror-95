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

__all__ = ['User']


class User(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_type: Optional[pulumi.Input[Union[str, 'AppType']]] = None,
                 confirmation: Optional[pulumi.Input[Union[str, 'Confirmation']]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 first_name: Optional[pulumi.Input[str]] = None,
                 identities: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserIdentityContractArgs']]]]] = None,
                 last_name: Optional[pulumi.Input[str]] = None,
                 note: Optional[pulumi.Input[str]] = None,
                 notify: Optional[pulumi.Input[bool]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[Union[str, 'UserState']]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        User details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'AppType']] app_type: Determines the type of application which send the create user request. Default is legacy portal.
        :param pulumi.Input[Union[str, 'Confirmation']] confirmation: Determines the type of confirmation e-mail that will be sent to the newly created user.
        :param pulumi.Input[str] email: Email address. Must not be empty and must be unique within the service instance.
        :param pulumi.Input[str] first_name: First name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserIdentityContractArgs']]]] identities: Collection of user identities.
        :param pulumi.Input[str] last_name: Last name.
        :param pulumi.Input[str] note: Optional note about a user set by the administrator.
        :param pulumi.Input[bool] notify: Send an Email notification to the User.
        :param pulumi.Input[str] password: User Password. If no value is provided, a default password is generated.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[Union[str, 'UserState']] state: Account state. Specifies whether the user is active or not. Blocked users are unable to sign into the developer portal or call any APIs of subscribed products. Default state is Active.
        :param pulumi.Input[str] user_id: User identifier. Must be unique in the current API Management service instance.
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

            __props__['app_type'] = app_type
            __props__['confirmation'] = confirmation
            if email is None and not opts.urn:
                raise TypeError("Missing required property 'email'")
            __props__['email'] = email
            if first_name is None and not opts.urn:
                raise TypeError("Missing required property 'first_name'")
            __props__['first_name'] = first_name
            __props__['identities'] = identities
            if last_name is None and not opts.urn:
                raise TypeError("Missing required property 'last_name'")
            __props__['last_name'] = last_name
            __props__['note'] = note
            __props__['notify'] = notify
            __props__['password'] = password
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__['service_name'] = service_name
            if state is None:
                state = 'active'
            __props__['state'] = state
            if user_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_id'")
            __props__['user_id'] = user_id
            __props__['groups'] = None
            __props__['name'] = None
            __props__['registration_date'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:apimanagement:User"), pulumi.Alias(type_="azure-nextgen:apimanagement/latest:User"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20160707:User"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20161010:User"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20170301:User"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20180101:User"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20180601preview:User"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20190101:User"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20191201:User"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20191201preview:User")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(User, __self__).__init__(
            'azure-nextgen:apimanagement/v20200601preview:User',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'User':
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return User(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def email(self) -> pulumi.Output[Optional[str]]:
        """
        Email address.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter(name="firstName")
    def first_name(self) -> pulumi.Output[Optional[str]]:
        """
        First name.
        """
        return pulumi.get(self, "first_name")

    @property
    @pulumi.getter
    def groups(self) -> pulumi.Output[Sequence['outputs.GroupContractPropertiesResponse']]:
        """
        Collection of groups user is part of.
        """
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter
    def identities(self) -> pulumi.Output[Optional[Sequence['outputs.UserIdentityContractResponse']]]:
        """
        Collection of user identities.
        """
        return pulumi.get(self, "identities")

    @property
    @pulumi.getter(name="lastName")
    def last_name(self) -> pulumi.Output[Optional[str]]:
        """
        Last name.
        """
        return pulumi.get(self, "last_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def note(self) -> pulumi.Output[Optional[str]]:
        """
        Optional note about a user set by the administrator.
        """
        return pulumi.get(self, "note")

    @property
    @pulumi.getter(name="registrationDate")
    def registration_date(self) -> pulumi.Output[Optional[str]]:
        """
        Date of user registration. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO 8601 standard.
        """
        return pulumi.get(self, "registration_date")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[Optional[str]]:
        """
        Account state. Specifies whether the user is active or not. Blocked users are unable to sign into the developer portal or call any APIs of subscribed products. Default state is Active.
        """
        return pulumi.get(self, "state")

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

