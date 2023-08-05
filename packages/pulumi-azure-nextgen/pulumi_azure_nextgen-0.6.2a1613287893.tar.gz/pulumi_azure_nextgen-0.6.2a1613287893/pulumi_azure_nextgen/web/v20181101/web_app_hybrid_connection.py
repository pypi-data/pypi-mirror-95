# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['WebAppHybridConnection']


class WebAppHybridConnection(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hostname: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 relay_arm_uri: Optional[pulumi.Input[str]] = None,
                 relay_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 send_key_name: Optional[pulumi.Input[str]] = None,
                 send_key_value: Optional[pulumi.Input[str]] = None,
                 service_bus_namespace: Optional[pulumi.Input[str]] = None,
                 service_bus_suffix: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Hybrid Connection contract. This is used to configure a Hybrid Connection.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] hostname: The hostname of the endpoint.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: The name of the web app.
        :param pulumi.Input[str] namespace_name: The namespace for this hybrid connection.
        :param pulumi.Input[int] port: The port of the endpoint.
        :param pulumi.Input[str] relay_arm_uri: The ARM URI to the Service Bus relay.
        :param pulumi.Input[str] relay_name: The name of the Service Bus relay.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] send_key_name: The name of the Service Bus key which has Send permissions. This is used to authenticate to Service Bus.
        :param pulumi.Input[str] send_key_value: The value of the Service Bus key. This is used to authenticate to Service Bus. In ARM this key will not be returned
               normally, use the POST /listKeys API instead.
        :param pulumi.Input[str] service_bus_namespace: The name of the Service Bus namespace.
        :param pulumi.Input[str] service_bus_suffix: The suffix for the service bus endpoint. By default this is .servicebus.windows.net
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

            __props__['hostname'] = hostname
            __props__['kind'] = kind
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__['namespace_name'] = namespace_name
            __props__['port'] = port
            __props__['relay_arm_uri'] = relay_arm_uri
            if relay_name is None and not opts.urn:
                raise TypeError("Missing required property 'relay_name'")
            __props__['relay_name'] = relay_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['send_key_name'] = send_key_name
            __props__['send_key_value'] = send_key_value
            __props__['service_bus_namespace'] = service_bus_namespace
            __props__['service_bus_suffix'] = service_bus_suffix
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web:WebAppHybridConnection"), pulumi.Alias(type_="azure-nextgen:web/latest:WebAppHybridConnection"), pulumi.Alias(type_="azure-nextgen:web/v20160801:WebAppHybridConnection"), pulumi.Alias(type_="azure-nextgen:web/v20180201:WebAppHybridConnection"), pulumi.Alias(type_="azure-nextgen:web/v20190801:WebAppHybridConnection"), pulumi.Alias(type_="azure-nextgen:web/v20200601:WebAppHybridConnection"), pulumi.Alias(type_="azure-nextgen:web/v20200901:WebAppHybridConnection"), pulumi.Alias(type_="azure-nextgen:web/v20201001:WebAppHybridConnection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppHybridConnection, __self__).__init__(
            'azure-nextgen:web/v20181101:WebAppHybridConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppHybridConnection':
        """
        Get an existing WebAppHybridConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WebAppHybridConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def hostname(self) -> pulumi.Output[Optional[str]]:
        """
        The hostname of the endpoint.
        """
        return pulumi.get(self, "hostname")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[int]]:
        """
        The port of the endpoint.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="relayArmUri")
    def relay_arm_uri(self) -> pulumi.Output[Optional[str]]:
        """
        The ARM URI to the Service Bus relay.
        """
        return pulumi.get(self, "relay_arm_uri")

    @property
    @pulumi.getter(name="relayName")
    def relay_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the Service Bus relay.
        """
        return pulumi.get(self, "relay_name")

    @property
    @pulumi.getter(name="sendKeyName")
    def send_key_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the Service Bus key which has Send permissions. This is used to authenticate to Service Bus.
        """
        return pulumi.get(self, "send_key_name")

    @property
    @pulumi.getter(name="sendKeyValue")
    def send_key_value(self) -> pulumi.Output[Optional[str]]:
        """
        The value of the Service Bus key. This is used to authenticate to Service Bus. In ARM this key will not be returned
        normally, use the POST /listKeys API instead.
        """
        return pulumi.get(self, "send_key_value")

    @property
    @pulumi.getter(name="serviceBusNamespace")
    def service_bus_namespace(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the Service Bus namespace.
        """
        return pulumi.get(self, "service_bus_namespace")

    @property
    @pulumi.getter(name="serviceBusSuffix")
    def service_bus_suffix(self) -> pulumi.Output[Optional[str]]:
        """
        The suffix for the service bus endpoint. By default this is .servicebus.windows.net
        """
        return pulumi.get(self, "service_bus_suffix")

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

