# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['Certificate']


class Certificate(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_id: Optional[pulumi.Input[str]] = None,
                 data: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Certificate details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_id: Identifier of the certificate entity. Must be unique in the current API Management service instance.
        :param pulumi.Input[str] data: Base 64 encoded certificate using the application/x-pkcs12 representation.
        :param pulumi.Input[str] password: Password for the Certificate
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

            if certificate_id is None and not opts.urn:
                raise TypeError("Missing required property 'certificate_id'")
            __props__['certificate_id'] = certificate_id
            if data is None and not opts.urn:
                raise TypeError("Missing required property 'data'")
            __props__['data'] = data
            if password is None and not opts.urn:
                raise TypeError("Missing required property 'password'")
            __props__['password'] = password
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__['service_name'] = service_name
            __props__['expiration_date'] = None
            __props__['name'] = None
            __props__['subject'] = None
            __props__['thumbprint'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:apimanagement:Certificate"), pulumi.Alias(type_="azure-nextgen:apimanagement/latest:Certificate"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20160707:Certificate"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20161010:Certificate"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20170301:Certificate"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20180101:Certificate"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20180601preview:Certificate"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20190101:Certificate"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20191201preview:Certificate"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20200601preview:Certificate")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Certificate, __self__).__init__(
            'azure-nextgen:apimanagement/v20191201:Certificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Certificate':
        """
        Get an existing Certificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Certificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> pulumi.Output[str]:
        """
        Expiration date of the certificate. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO 8601 standard.
        """
        return pulumi.get(self, "expiration_date")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def subject(self) -> pulumi.Output[str]:
        """
        Subject attribute of the certificate.
        """
        return pulumi.get(self, "subject")

    @property
    @pulumi.getter
    def thumbprint(self) -> pulumi.Output[str]:
        """
        Thumbprint of the certificate.
        """
        return pulumi.get(self, "thumbprint")

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

