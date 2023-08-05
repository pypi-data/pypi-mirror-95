# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = ['OuContainer']


class OuContainer(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 domain_service_name: Optional[pulumi.Input[str]] = None,
                 ou_container_name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 spn: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Resource for OuContainer.
        API Version: 2020-01-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The account name
        :param pulumi.Input[str] domain_service_name: The name of the domain service.
        :param pulumi.Input[str] ou_container_name: The name of the OuContainer.
        :param pulumi.Input[str] password: The account password
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[str] spn: The account spn
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

            __props__['account_name'] = account_name
            if domain_service_name is None and not opts.urn:
                raise TypeError("Missing required property 'domain_service_name'")
            __props__['domain_service_name'] = domain_service_name
            if ou_container_name is None and not opts.urn:
                raise TypeError("Missing required property 'ou_container_name'")
            __props__['ou_container_name'] = ou_container_name
            __props__['password'] = password
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['spn'] = spn
            __props__['accounts'] = None
            __props__['container_id'] = None
            __props__['deployment_id'] = None
            __props__['distinguished_name'] = None
            __props__['domain_name'] = None
            __props__['etag'] = None
            __props__['location'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['service_status'] = None
            __props__['tags'] = None
            __props__['tenant_id'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:aad/latest:OuContainer"), pulumi.Alias(type_="azure-nextgen:aad/v20170601:OuContainer"), pulumi.Alias(type_="azure-nextgen:aad/v20200101:OuContainer")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(OuContainer, __self__).__init__(
            'azure-nextgen:aad:OuContainer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'OuContainer':
        """
        Get an existing OuContainer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return OuContainer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def accounts(self) -> pulumi.Output[Optional[Sequence['outputs.ContainerAccountResponse']]]:
        """
        The list of container accounts
        """
        return pulumi.get(self, "accounts")

    @property
    @pulumi.getter(name="containerId")
    def container_id(self) -> pulumi.Output[str]:
        """
        The OuContainer name
        """
        return pulumi.get(self, "container_id")

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> pulumi.Output[str]:
        """
        The Deployment id
        """
        return pulumi.get(self, "deployment_id")

    @property
    @pulumi.getter(name="distinguishedName")
    def distinguished_name(self) -> pulumi.Output[str]:
        """
        Distinguished Name of OuContainer instance
        """
        return pulumi.get(self, "distinguished_name")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        The domain name of Domain Services.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Resource etag
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The current deployment or provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serviceStatus")
    def service_status(self) -> pulumi.Output[str]:
        """
        Status of OuContainer instance
        """
        return pulumi.get(self, "service_status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[str]:
        """
        Azure Active Directory tenant id
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

