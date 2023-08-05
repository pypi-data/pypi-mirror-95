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

__all__ = ['Api']


class Api(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_id: Optional[pulumi.Input[str]] = None,
                 api_revision: Optional[pulumi.Input[str]] = None,
                 api_revision_description: Optional[pulumi.Input[str]] = None,
                 api_type: Optional[pulumi.Input[Union[str, 'ApiType']]] = None,
                 api_version: Optional[pulumi.Input[str]] = None,
                 api_version_description: Optional[pulumi.Input[str]] = None,
                 api_version_set: Optional[pulumi.Input[pulumi.InputType['ApiVersionSetContractDetailsArgs']]] = None,
                 api_version_set_id: Optional[pulumi.Input[str]] = None,
                 authentication_settings: Optional[pulumi.Input[pulumi.InputType['AuthenticationSettingsContractArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 format: Optional[pulumi.Input[Union[str, 'ContentFormat']]] = None,
                 is_current: Optional[pulumi.Input[bool]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 protocols: Optional[pulumi.Input[Sequence[pulumi.Input['Protocol']]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 service_url: Optional[pulumi.Input[str]] = None,
                 soap_api_type: Optional[pulumi.Input[Union[str, 'SoapApiType']]] = None,
                 source_api_id: Optional[pulumi.Input[str]] = None,
                 subscription_key_parameter_names: Optional[pulumi.Input[pulumi.InputType['SubscriptionKeyParameterNamesContractArgs']]] = None,
                 subscription_required: Optional[pulumi.Input[bool]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 wsdl_selector: Optional[pulumi.Input[pulumi.InputType['ApiCreateOrUpdatePropertiesWsdlSelectorArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Api details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_id: API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
        :param pulumi.Input[str] api_revision: Describes the Revision of the Api. If no value is provided, default revision 1 is created
        :param pulumi.Input[str] api_revision_description: Description of the Api Revision.
        :param pulumi.Input[Union[str, 'ApiType']] api_type: Type of API.
        :param pulumi.Input[str] api_version: Indicates the Version identifier of the API if the API is versioned
        :param pulumi.Input[str] api_version_description: Description of the Api Version.
        :param pulumi.Input[pulumi.InputType['ApiVersionSetContractDetailsArgs']] api_version_set: Version set details
        :param pulumi.Input[str] api_version_set_id: A resource identifier for the related ApiVersionSet.
        :param pulumi.Input[pulumi.InputType['AuthenticationSettingsContractArgs']] authentication_settings: Collection of authentication settings included into this API.
        :param pulumi.Input[str] description: Description of the API. May include HTML formatting tags.
        :param pulumi.Input[str] display_name: API name. Must be 1 to 300 characters long.
        :param pulumi.Input[Union[str, 'ContentFormat']] format: Format of the Content in which the API is getting imported.
        :param pulumi.Input[bool] is_current: Indicates if API revision is current api revision.
        :param pulumi.Input[str] path: Relative URL uniquely identifying this API and all of its resource paths within the API Management service instance. It is appended to the API endpoint base URL specified during the service instance creation to form a public URL for this API.
        :param pulumi.Input[Sequence[pulumi.Input['Protocol']]] protocols: Describes on which protocols the operations in this API can be invoked.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[str] service_url: Absolute URL of the backend service implementing this API. Cannot be more than 2000 characters long.
        :param pulumi.Input[Union[str, 'SoapApiType']] soap_api_type: Type of Api to create. 
                * `http` creates a SOAP to REST API 
                * `soap` creates a SOAP pass-through API .
        :param pulumi.Input[str] source_api_id: API identifier of the source API.
        :param pulumi.Input[pulumi.InputType['SubscriptionKeyParameterNamesContractArgs']] subscription_key_parameter_names: Protocols over which API is made available.
        :param pulumi.Input[bool] subscription_required: Specifies whether an API or Product subscription is required for accessing the API.
        :param pulumi.Input[str] value: Content value when Importing an API.
        :param pulumi.Input[pulumi.InputType['ApiCreateOrUpdatePropertiesWsdlSelectorArgs']] wsdl_selector: Criteria to limit import of WSDL to a subset of the document.
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

            if api_id is None and not opts.urn:
                raise TypeError("Missing required property 'api_id'")
            __props__['api_id'] = api_id
            __props__['api_revision'] = api_revision
            __props__['api_revision_description'] = api_revision_description
            __props__['api_type'] = api_type
            __props__['api_version'] = api_version
            __props__['api_version_description'] = api_version_description
            __props__['api_version_set'] = api_version_set
            __props__['api_version_set_id'] = api_version_set_id
            __props__['authentication_settings'] = authentication_settings
            __props__['description'] = description
            __props__['display_name'] = display_name
            __props__['format'] = format
            __props__['is_current'] = is_current
            if path is None and not opts.urn:
                raise TypeError("Missing required property 'path'")
            __props__['path'] = path
            __props__['protocols'] = protocols
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__['service_name'] = service_name
            __props__['service_url'] = service_url
            __props__['soap_api_type'] = soap_api_type
            __props__['source_api_id'] = source_api_id
            __props__['subscription_key_parameter_names'] = subscription_key_parameter_names
            __props__['subscription_required'] = subscription_required
            __props__['value'] = value
            __props__['wsdl_selector'] = wsdl_selector
            __props__['is_online'] = None
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:apimanagement:Api"), pulumi.Alias(type_="azure-nextgen:apimanagement/latest:Api"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20160707:Api"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20161010:Api"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20170301:Api"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20180101:Api"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20180601preview:Api"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20190101:Api"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20191201preview:Api"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20200601preview:Api")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Api, __self__).__init__(
            'azure-nextgen:apimanagement/v20191201:Api',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Api':
        """
        Get an existing Api resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Api(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiRevision")
    def api_revision(self) -> pulumi.Output[Optional[str]]:
        """
        Describes the Revision of the Api. If no value is provided, default revision 1 is created
        """
        return pulumi.get(self, "api_revision")

    @property
    @pulumi.getter(name="apiRevisionDescription")
    def api_revision_description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the Api Revision.
        """
        return pulumi.get(self, "api_revision_description")

    @property
    @pulumi.getter(name="apiType")
    def api_type(self) -> pulumi.Output[Optional[str]]:
        """
        Type of API.
        """
        return pulumi.get(self, "api_type")

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates the Version identifier of the API if the API is versioned
        """
        return pulumi.get(self, "api_version")

    @property
    @pulumi.getter(name="apiVersionDescription")
    def api_version_description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the Api Version.
        """
        return pulumi.get(self, "api_version_description")

    @property
    @pulumi.getter(name="apiVersionSet")
    def api_version_set(self) -> pulumi.Output[Optional['outputs.ApiVersionSetContractDetailsResponse']]:
        """
        Version set details
        """
        return pulumi.get(self, "api_version_set")

    @property
    @pulumi.getter(name="apiVersionSetId")
    def api_version_set_id(self) -> pulumi.Output[Optional[str]]:
        """
        A resource identifier for the related ApiVersionSet.
        """
        return pulumi.get(self, "api_version_set_id")

    @property
    @pulumi.getter(name="authenticationSettings")
    def authentication_settings(self) -> pulumi.Output[Optional['outputs.AuthenticationSettingsContractResponse']]:
        """
        Collection of authentication settings included into this API.
        """
        return pulumi.get(self, "authentication_settings")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the API. May include HTML formatting tags.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        API name. Must be 1 to 300 characters long.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="isCurrent")
    def is_current(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates if API revision is current api revision.
        """
        return pulumi.get(self, "is_current")

    @property
    @pulumi.getter(name="isOnline")
    def is_online(self) -> pulumi.Output[bool]:
        """
        Indicates if API revision is accessible via the gateway.
        """
        return pulumi.get(self, "is_online")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def path(self) -> pulumi.Output[str]:
        """
        Relative URL uniquely identifying this API and all of its resource paths within the API Management service instance. It is appended to the API endpoint base URL specified during the service instance creation to form a public URL for this API.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def protocols(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Describes on which protocols the operations in this API can be invoked.
        """
        return pulumi.get(self, "protocols")

    @property
    @pulumi.getter(name="serviceUrl")
    def service_url(self) -> pulumi.Output[Optional[str]]:
        """
        Absolute URL of the backend service implementing this API. Cannot be more than 2000 characters long.
        """
        return pulumi.get(self, "service_url")

    @property
    @pulumi.getter(name="sourceApiId")
    def source_api_id(self) -> pulumi.Output[Optional[str]]:
        """
        API identifier of the source API.
        """
        return pulumi.get(self, "source_api_id")

    @property
    @pulumi.getter(name="subscriptionKeyParameterNames")
    def subscription_key_parameter_names(self) -> pulumi.Output[Optional['outputs.SubscriptionKeyParameterNamesContractResponse']]:
        """
        Protocols over which API is made available.
        """
        return pulumi.get(self, "subscription_key_parameter_names")

    @property
    @pulumi.getter(name="subscriptionRequired")
    def subscription_required(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether an API or Product subscription is required for accessing the API.
        """
        return pulumi.get(self, "subscription_required")

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

