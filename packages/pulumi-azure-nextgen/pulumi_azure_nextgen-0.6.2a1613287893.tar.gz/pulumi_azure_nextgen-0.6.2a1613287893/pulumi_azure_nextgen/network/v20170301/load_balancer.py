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

__all__ = ['LoadBalancer']


class LoadBalancer(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_address_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BackendAddressPoolArgs']]]]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 inbound_nat_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InboundNatPoolArgs']]]]] = None,
                 inbound_nat_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InboundNatRuleArgs']]]]] = None,
                 load_balancer_name: Optional[pulumi.Input[str]] = None,
                 load_balancing_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 outbound_nat_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OutboundNatRuleArgs']]]]] = None,
                 probes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ProbeArgs']]]]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_guid: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        LoadBalancer resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BackendAddressPoolArgs']]]] backend_address_pools: Collection of backend address pools used by a load balancer
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']]]] frontend_ip_configurations: Object representing the frontend IPs to be used for the load balancer
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InboundNatPoolArgs']]]] inbound_nat_pools: Defines an external port range for inbound NAT to a single backend port on NICs associated with a load balancer. Inbound NAT rules are created automatically for each NIC associated with the Load Balancer using an external port from this range. Defining an Inbound NAT pool on your Load Balancer is mutually exclusive with defining inbound Nat rules. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an inbound NAT pool. They have to reference individual inbound NAT rules.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InboundNatRuleArgs']]]] inbound_nat_rules: Collection of inbound NAT Rules used by a load balancer. Defining inbound NAT rules on your load balancer is mutually exclusive with defining an inbound NAT pool. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an Inbound NAT pool. They have to reference individual inbound NAT rules.
        :param pulumi.Input[str] load_balancer_name: The name of the load balancer.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]] load_balancing_rules: Object collection representing the load balancing rules Gets the provisioning 
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OutboundNatRuleArgs']]]] outbound_nat_rules: The outbound NAT rules.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ProbeArgs']]]] probes: Collection of probe objects used in the load balancer
        :param pulumi.Input[str] provisioning_state: Gets the provisioning state of the PublicIP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] resource_guid: The resource GUID property of the load balancer resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
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

            __props__['backend_address_pools'] = backend_address_pools
            __props__['etag'] = etag
            __props__['frontend_ip_configurations'] = frontend_ip_configurations
            __props__['id'] = id
            __props__['inbound_nat_pools'] = inbound_nat_pools
            __props__['inbound_nat_rules'] = inbound_nat_rules
            if load_balancer_name is None and not opts.urn:
                raise TypeError("Missing required property 'load_balancer_name'")
            __props__['load_balancer_name'] = load_balancer_name
            __props__['load_balancing_rules'] = load_balancing_rules
            __props__['location'] = location
            __props__['outbound_nat_rules'] = outbound_nat_rules
            __props__['probes'] = probes
            __props__['provisioning_state'] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['resource_guid'] = resource_guid
            __props__['tags'] = tags
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/latest:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20150501preview:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20150615:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20160330:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20160601:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20160901:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20161201:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20170601:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20170801:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20170901:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20171001:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20171101:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20180101:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20180201:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20180401:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20180601:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20180701:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20180801:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20181001:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20181101:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20181201:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20190201:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20190401:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20190601:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20190701:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20190801:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20190901:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20191101:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20191201:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20200301:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20200401:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20200501:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20200601:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20200701:LoadBalancer"), pulumi.Alias(type_="azure-nextgen:network/v20200801:LoadBalancer")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(LoadBalancer, __self__).__init__(
            'azure-nextgen:network/v20170301:LoadBalancer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'LoadBalancer':
        """
        Get an existing LoadBalancer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return LoadBalancer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backendAddressPools")
    def backend_address_pools(self) -> pulumi.Output[Optional[Sequence['outputs.BackendAddressPoolResponse']]]:
        """
        Collection of backend address pools used by a load balancer
        """
        return pulumi.get(self, "backend_address_pools")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="frontendIPConfigurations")
    def frontend_ip_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.FrontendIPConfigurationResponse']]]:
        """
        Object representing the frontend IPs to be used for the load balancer
        """
        return pulumi.get(self, "frontend_ip_configurations")

    @property
    @pulumi.getter(name="inboundNatPools")
    def inbound_nat_pools(self) -> pulumi.Output[Optional[Sequence['outputs.InboundNatPoolResponse']]]:
        """
        Defines an external port range for inbound NAT to a single backend port on NICs associated with a load balancer. Inbound NAT rules are created automatically for each NIC associated with the Load Balancer using an external port from this range. Defining an Inbound NAT pool on your Load Balancer is mutually exclusive with defining inbound Nat rules. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an inbound NAT pool. They have to reference individual inbound NAT rules.
        """
        return pulumi.get(self, "inbound_nat_pools")

    @property
    @pulumi.getter(name="inboundNatRules")
    def inbound_nat_rules(self) -> pulumi.Output[Optional[Sequence['outputs.InboundNatRuleResponse']]]:
        """
        Collection of inbound NAT Rules used by a load balancer. Defining inbound NAT rules on your load balancer is mutually exclusive with defining an inbound NAT pool. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an Inbound NAT pool. They have to reference individual inbound NAT rules.
        """
        return pulumi.get(self, "inbound_nat_rules")

    @property
    @pulumi.getter(name="loadBalancingRules")
    def load_balancing_rules(self) -> pulumi.Output[Optional[Sequence['outputs.LoadBalancingRuleResponse']]]:
        """
        Object collection representing the load balancing rules Gets the provisioning 
        """
        return pulumi.get(self, "load_balancing_rules")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outboundNatRules")
    def outbound_nat_rules(self) -> pulumi.Output[Optional[Sequence['outputs.OutboundNatRuleResponse']]]:
        """
        The outbound NAT rules.
        """
        return pulumi.get(self, "outbound_nat_rules")

    @property
    @pulumi.getter
    def probes(self) -> pulumi.Output[Optional[Sequence['outputs.ProbeResponse']]]:
        """
        Collection of probe objects used in the load balancer
        """
        return pulumi.get(self, "probes")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Gets the provisioning state of the PublicIP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> pulumi.Output[Optional[str]]:
        """
        The resource GUID property of the load balancer resource.
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

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

