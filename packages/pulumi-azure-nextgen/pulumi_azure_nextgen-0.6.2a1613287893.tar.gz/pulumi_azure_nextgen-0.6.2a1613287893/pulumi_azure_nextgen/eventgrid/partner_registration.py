# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from ._enums import *

__all__ = ['PartnerRegistration']


class PartnerRegistration(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorized_azure_subscription_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 customer_service_uri: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 logo_uri: Optional[pulumi.Input[str]] = None,
                 long_description: Optional[pulumi.Input[str]] = None,
                 partner_customer_service_extension: Optional[pulumi.Input[str]] = None,
                 partner_customer_service_number: Optional[pulumi.Input[str]] = None,
                 partner_name: Optional[pulumi.Input[str]] = None,
                 partner_registration_name: Optional[pulumi.Input[str]] = None,
                 partner_resource_type_description: Optional[pulumi.Input[str]] = None,
                 partner_resource_type_display_name: Optional[pulumi.Input[str]] = None,
                 partner_resource_type_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 setup_uri: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 visibility_state: Optional[pulumi.Input[Union[str, 'PartnerRegistrationVisibilityState']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Information about a partner registration.
        API Version: 2020-04-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] authorized_azure_subscription_ids: List of Azure subscription Ids that are authorized to create a partner namespace
               associated with this partner registration. This is an optional property. Creating
               partner namespaces is always permitted under the same Azure subscription as the one used
               for creating the partner registration.
        :param pulumi.Input[str] customer_service_uri: The extension of the customer service URI of the publisher.
        :param pulumi.Input[str] location: Location of the resource.
        :param pulumi.Input[str] logo_uri: URI of the logo.
        :param pulumi.Input[str] long_description: Long description for the custom scenarios and integration to be displayed in the portal if needed.
               Length of this description should not exceed 2048 characters.
        :param pulumi.Input[str] partner_customer_service_extension: The extension of the customer service number of the publisher. Only digits are allowed and number of digits should not exceed 10.
        :param pulumi.Input[str] partner_customer_service_number: The customer service number of the publisher. The expected phone format should start with a '+' sign 
               followed by the country code. The remaining digits are then followed. Only digits and spaces are allowed and its
               length cannot exceed 16 digits including country code. Examples of valid phone numbers are: +1 515 123 4567 and
               +966 7 5115 2471. Examples of invalid phone numbers are: +1 (515) 123-4567, 1 515 123 4567 and +966 121 5115 24 7 551 1234 43
        :param pulumi.Input[str] partner_name: Official name of the partner name. For example: "Contoso".
        :param pulumi.Input[str] partner_registration_name: Name of the partner registration.
        :param pulumi.Input[str] partner_resource_type_description: Short description of the partner resource type. The length of this description should not exceed 256 characters.
        :param pulumi.Input[str] partner_resource_type_display_name: Display name of the partner resource type.
        :param pulumi.Input[str] partner_resource_type_name: Name of the partner resource type.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription.
        :param pulumi.Input[str] setup_uri: URI of the partner website that can be used by Azure customers to setup Event Grid
               integration on an event source.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags of the resource.
        :param pulumi.Input[Union[str, 'PartnerRegistrationVisibilityState']] visibility_state: Visibility state of the partner registration.
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

            __props__['authorized_azure_subscription_ids'] = authorized_azure_subscription_ids
            __props__['customer_service_uri'] = customer_service_uri
            __props__['location'] = location
            __props__['logo_uri'] = logo_uri
            __props__['long_description'] = long_description
            __props__['partner_customer_service_extension'] = partner_customer_service_extension
            __props__['partner_customer_service_number'] = partner_customer_service_number
            __props__['partner_name'] = partner_name
            if partner_registration_name is None and not opts.urn:
                raise TypeError("Missing required property 'partner_registration_name'")
            __props__['partner_registration_name'] = partner_registration_name
            __props__['partner_resource_type_description'] = partner_resource_type_description
            __props__['partner_resource_type_display_name'] = partner_resource_type_display_name
            __props__['partner_resource_type_name'] = partner_resource_type_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['setup_uri'] = setup_uri
            __props__['tags'] = tags
            __props__['visibility_state'] = visibility_state
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:eventgrid/v20200401preview:PartnerRegistration"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20201015preview:PartnerRegistration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PartnerRegistration, __self__).__init__(
            'azure-nextgen:eventgrid:PartnerRegistration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PartnerRegistration':
        """
        Get an existing PartnerRegistration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return PartnerRegistration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authorizedAzureSubscriptionIds")
    def authorized_azure_subscription_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of Azure subscription Ids that are authorized to create a partner namespace
        associated with this partner registration. This is an optional property. Creating
        partner namespaces is always permitted under the same Azure subscription as the one used
        for creating the partner registration.
        """
        return pulumi.get(self, "authorized_azure_subscription_ids")

    @property
    @pulumi.getter(name="customerServiceUri")
    def customer_service_uri(self) -> pulumi.Output[Optional[str]]:
        """
        The extension of the customer service URI of the publisher.
        """
        return pulumi.get(self, "customer_service_uri")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="logoUri")
    def logo_uri(self) -> pulumi.Output[Optional[str]]:
        """
        URI of the logo.
        """
        return pulumi.get(self, "logo_uri")

    @property
    @pulumi.getter(name="longDescription")
    def long_description(self) -> pulumi.Output[Optional[str]]:
        """
        Long description for the custom scenarios and integration to be displayed in the portal if needed.
        Length of this description should not exceed 2048 characters.
        """
        return pulumi.get(self, "long_description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="partnerCustomerServiceExtension")
    def partner_customer_service_extension(self) -> pulumi.Output[Optional[str]]:
        """
        The extension of the customer service number of the publisher. Only digits are allowed and number of digits should not exceed 10.
        """
        return pulumi.get(self, "partner_customer_service_extension")

    @property
    @pulumi.getter(name="partnerCustomerServiceNumber")
    def partner_customer_service_number(self) -> pulumi.Output[Optional[str]]:
        """
        The customer service number of the publisher. The expected phone format should start with a '+' sign 
        followed by the country code. The remaining digits are then followed. Only digits and spaces are allowed and its
        length cannot exceed 16 digits including country code. Examples of valid phone numbers are: +1 515 123 4567 and
        +966 7 5115 2471. Examples of invalid phone numbers are: +1 (515) 123-4567, 1 515 123 4567 and +966 121 5115 24 7 551 1234 43
        """
        return pulumi.get(self, "partner_customer_service_number")

    @property
    @pulumi.getter(name="partnerName")
    def partner_name(self) -> pulumi.Output[Optional[str]]:
        """
        Official name of the partner name. For example: "Contoso".
        """
        return pulumi.get(self, "partner_name")

    @property
    @pulumi.getter(name="partnerResourceTypeDescription")
    def partner_resource_type_description(self) -> pulumi.Output[Optional[str]]:
        """
        Short description of the partner resource type. The length of this description should not exceed 256 characters.
        """
        return pulumi.get(self, "partner_resource_type_description")

    @property
    @pulumi.getter(name="partnerResourceTypeDisplayName")
    def partner_resource_type_display_name(self) -> pulumi.Output[Optional[str]]:
        """
        Display name of the partner resource type.
        """
        return pulumi.get(self, "partner_resource_type_display_name")

    @property
    @pulumi.getter(name="partnerResourceTypeName")
    def partner_resource_type_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the partner resource type.
        """
        return pulumi.get(self, "partner_resource_type_name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the partner registration.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="setupUri")
    def setup_uri(self) -> pulumi.Output[Optional[str]]:
        """
        URI of the partner website that can be used by Azure customers to setup Event Grid
        integration on an event source.
        """
        return pulumi.get(self, "setup_uri")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="visibilityState")
    def visibility_state(self) -> pulumi.Output[Optional[str]]:
        """
        Visibility state of the partner registration.
        """
        return pulumi.get(self, "visibility_state")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

