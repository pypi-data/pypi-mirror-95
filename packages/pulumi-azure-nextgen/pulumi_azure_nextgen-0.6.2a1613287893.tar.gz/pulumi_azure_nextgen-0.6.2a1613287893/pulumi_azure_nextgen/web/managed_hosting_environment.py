# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['ManagedHostingEnvironment']


class ManagedHostingEnvironment(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_multi_sizes: Optional[pulumi.Input[str]] = None,
                 allowed_worker_sizes: Optional[pulumi.Input[str]] = None,
                 api_management_account_id: Optional[pulumi.Input[str]] = None,
                 cluster_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NameValuePairArgs']]]]] = None,
                 database_edition: Optional[pulumi.Input[str]] = None,
                 database_service_objective: Optional[pulumi.Input[str]] = None,
                 dns_suffix: Optional[pulumi.Input[str]] = None,
                 environment_capacities: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StampCapacityArgs']]]]] = None,
                 environment_is_healthy: Optional[pulumi.Input[bool]] = None,
                 environment_status: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 internal_load_balancing_mode: Optional[pulumi.Input['InternalLoadBalancingMode']] = None,
                 ipssl_address_count: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 last_action: Optional[pulumi.Input[str]] = None,
                 last_action_result: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maximum_number_of_machines: Optional[pulumi.Input[int]] = None,
                 multi_role_count: Optional[pulumi.Input[int]] = None,
                 multi_size: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_access_control_list: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkAccessControlEntryArgs']]]]] = None,
                 provisioning_state: Optional[pulumi.Input['ProvisioningState']] = None,
                 resource_group: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input['HostingEnvironmentStatus']] = None,
                 subscription_id: Optional[pulumi.Input[str]] = None,
                 suspended: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 upgrade_domains: Optional[pulumi.Input[int]] = None,
                 vip_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualIPMappingArgs']]]]] = None,
                 virtual_network: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkProfileArgs']]] = None,
                 vnet_name: Optional[pulumi.Input[str]] = None,
                 vnet_resource_group_name: Optional[pulumi.Input[str]] = None,
                 vnet_subnet_name: Optional[pulumi.Input[str]] = None,
                 worker_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WorkerPoolArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Description of an hostingEnvironment (App Service Environment)
        API Version: 2015-08-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allowed_multi_sizes: List of comma separated strings describing which VM sizes are allowed for front-ends
        :param pulumi.Input[str] allowed_worker_sizes: List of comma separated strings describing which VM sizes are allowed for workers
        :param pulumi.Input[str] api_management_account_id: Api Management Account associated with this Hosting Environment
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NameValuePairArgs']]]] cluster_settings: Custom settings for changing the behavior of the hosting environment
        :param pulumi.Input[str] database_edition: Edition of the metadata database for the hostingEnvironment (App Service Environment) e.g. "Standard"
        :param pulumi.Input[str] database_service_objective: Service objective of the metadata database for the hostingEnvironment (App Service Environment) e.g. "S0"
        :param pulumi.Input[str] dns_suffix: DNS suffix of the hostingEnvironment (App Service Environment)
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StampCapacityArgs']]]] environment_capacities: Current total, used, and available worker capacities
        :param pulumi.Input[bool] environment_is_healthy: True/false indicating whether the hostingEnvironment (App Service Environment) is healthy
        :param pulumi.Input[str] environment_status: Detailed message about with results of the last check of the hostingEnvironment (App Service Environment)
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input['InternalLoadBalancingMode'] internal_load_balancing_mode: Specifies which endpoints to serve internally in the hostingEnvironment's (App Service Environment) VNET
        :param pulumi.Input[int] ipssl_address_count: Number of IP SSL addresses reserved for this hostingEnvironment (App Service Environment)
        :param pulumi.Input[str] kind: Kind of resource
        :param pulumi.Input[str] last_action: Last deployment action on this hostingEnvironment (App Service Environment)
        :param pulumi.Input[str] last_action_result: Result of the last deployment action on this hostingEnvironment (App Service Environment)
        :param pulumi.Input[str] location: Resource Location
        :param pulumi.Input[int] maximum_number_of_machines: Maximum number of VMs in this hostingEnvironment (App Service Environment)
        :param pulumi.Input[int] multi_role_count: Number of front-end instances
        :param pulumi.Input[str] multi_size: Front-end VM size, e.g. "Medium", "Large"
        :param pulumi.Input[str] name: Resource Name
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkAccessControlEntryArgs']]]] network_access_control_list: Access control list for controlling traffic to the hostingEnvironment (App Service Environment)
        :param pulumi.Input['ProvisioningState'] provisioning_state: Provisioning state of the hostingEnvironment (App Service Environment)
        :param pulumi.Input[str] resource_group: Resource group of the hostingEnvironment (App Service Environment)
        :param pulumi.Input[str] resource_group_name: Name of resource group
        :param pulumi.Input['HostingEnvironmentStatus'] status: Current status of the hostingEnvironment (App Service Environment)
        :param pulumi.Input[str] subscription_id: Subscription of the hostingEnvironment (App Service Environment)
        :param pulumi.Input[bool] suspended: True/false indicating whether the hostingEnvironment is suspended. The environment can be suspended e.g. when the management endpoint is no longer available
                           (most likely because NSG blocked the incoming traffic)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Resource type
        :param pulumi.Input[int] upgrade_domains: Number of upgrade domains of this hostingEnvironment (App Service Environment)
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualIPMappingArgs']]]] vip_mappings: Description of IP SSL mapping for this hostingEnvironment (App Service Environment)
        :param pulumi.Input[pulumi.InputType['VirtualNetworkProfileArgs']] virtual_network: Description of the hostingEnvironment's (App Service Environment) virtual network
        :param pulumi.Input[str] vnet_name: Name of the hostingEnvironment's (App Service Environment) virtual network
        :param pulumi.Input[str] vnet_resource_group_name: Resource group of the hostingEnvironment's (App Service Environment) virtual network
        :param pulumi.Input[str] vnet_subnet_name: Subnet of the hostingEnvironment's (App Service Environment) virtual network
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WorkerPoolArgs']]]] worker_pools: Description of worker pools with worker size ids, VM sizes, and number of workers in each pool
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

            __props__['allowed_multi_sizes'] = allowed_multi_sizes
            __props__['allowed_worker_sizes'] = allowed_worker_sizes
            __props__['api_management_account_id'] = api_management_account_id
            __props__['cluster_settings'] = cluster_settings
            __props__['database_edition'] = database_edition
            __props__['database_service_objective'] = database_service_objective
            __props__['dns_suffix'] = dns_suffix
            __props__['environment_capacities'] = environment_capacities
            __props__['environment_is_healthy'] = environment_is_healthy
            __props__['environment_status'] = environment_status
            __props__['id'] = id
            __props__['internal_load_balancing_mode'] = internal_load_balancing_mode
            __props__['ipssl_address_count'] = ipssl_address_count
            __props__['kind'] = kind
            __props__['last_action'] = last_action
            __props__['last_action_result'] = last_action_result
            __props__['location'] = location
            __props__['maximum_number_of_machines'] = maximum_number_of_machines
            __props__['multi_role_count'] = multi_role_count
            __props__['multi_size'] = multi_size
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            __props__['network_access_control_list'] = network_access_control_list
            __props__['provisioning_state'] = provisioning_state
            __props__['resource_group'] = resource_group
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if status is None and not opts.urn:
                raise TypeError("Missing required property 'status'")
            __props__['status'] = status
            __props__['subscription_id'] = subscription_id
            __props__['suspended'] = suspended
            __props__['tags'] = tags
            __props__['type'] = type
            __props__['upgrade_domains'] = upgrade_domains
            __props__['vip_mappings'] = vip_mappings
            __props__['virtual_network'] = virtual_network
            __props__['vnet_name'] = vnet_name
            __props__['vnet_resource_group_name'] = vnet_resource_group_name
            __props__['vnet_subnet_name'] = vnet_subnet_name
            __props__['worker_pools'] = worker_pools
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web/latest:ManagedHostingEnvironment"), pulumi.Alias(type_="azure-nextgen:web/v20150801:ManagedHostingEnvironment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedHostingEnvironment, __self__).__init__(
            'azure-nextgen:web:ManagedHostingEnvironment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagedHostingEnvironment':
        """
        Get an existing ManagedHostingEnvironment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ManagedHostingEnvironment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowedMultiSizes")
    def allowed_multi_sizes(self) -> pulumi.Output[Optional[str]]:
        """
        List of comma separated strings describing which VM sizes are allowed for front-ends
        """
        return pulumi.get(self, "allowed_multi_sizes")

    @property
    @pulumi.getter(name="allowedWorkerSizes")
    def allowed_worker_sizes(self) -> pulumi.Output[Optional[str]]:
        """
        List of comma separated strings describing which VM sizes are allowed for workers
        """
        return pulumi.get(self, "allowed_worker_sizes")

    @property
    @pulumi.getter(name="apiManagementAccountId")
    def api_management_account_id(self) -> pulumi.Output[Optional[str]]:
        """
        Api Management Account associated with this Hosting Environment
        """
        return pulumi.get(self, "api_management_account_id")

    @property
    @pulumi.getter(name="clusterSettings")
    def cluster_settings(self) -> pulumi.Output[Optional[Sequence['outputs.NameValuePairResponse']]]:
        """
        Custom settings for changing the behavior of the hosting environment
        """
        return pulumi.get(self, "cluster_settings")

    @property
    @pulumi.getter(name="databaseEdition")
    def database_edition(self) -> pulumi.Output[Optional[str]]:
        """
        Edition of the metadata database for the hostingEnvironment (App Service Environment) e.g. "Standard"
        """
        return pulumi.get(self, "database_edition")

    @property
    @pulumi.getter(name="databaseServiceObjective")
    def database_service_objective(self) -> pulumi.Output[Optional[str]]:
        """
        Service objective of the metadata database for the hostingEnvironment (App Service Environment) e.g. "S0"
        """
        return pulumi.get(self, "database_service_objective")

    @property
    @pulumi.getter(name="dnsSuffix")
    def dns_suffix(self) -> pulumi.Output[Optional[str]]:
        """
        DNS suffix of the hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "dns_suffix")

    @property
    @pulumi.getter(name="environmentCapacities")
    def environment_capacities(self) -> pulumi.Output[Optional[Sequence['outputs.StampCapacityResponse']]]:
        """
        Current total, used, and available worker capacities
        """
        return pulumi.get(self, "environment_capacities")

    @property
    @pulumi.getter(name="environmentIsHealthy")
    def environment_is_healthy(self) -> pulumi.Output[Optional[bool]]:
        """
        True/false indicating whether the hostingEnvironment (App Service Environment) is healthy
        """
        return pulumi.get(self, "environment_is_healthy")

    @property
    @pulumi.getter(name="environmentStatus")
    def environment_status(self) -> pulumi.Output[Optional[str]]:
        """
        Detailed message about with results of the last check of the hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "environment_status")

    @property
    @pulumi.getter(name="internalLoadBalancingMode")
    def internal_load_balancing_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies which endpoints to serve internally in the hostingEnvironment's (App Service Environment) VNET
        """
        return pulumi.get(self, "internal_load_balancing_mode")

    @property
    @pulumi.getter(name="ipsslAddressCount")
    def ipssl_address_count(self) -> pulumi.Output[Optional[int]]:
        """
        Number of IP SSL addresses reserved for this hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "ipssl_address_count")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastAction")
    def last_action(self) -> pulumi.Output[Optional[str]]:
        """
        Last deployment action on this hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "last_action")

    @property
    @pulumi.getter(name="lastActionResult")
    def last_action_result(self) -> pulumi.Output[Optional[str]]:
        """
        Result of the last deployment action on this hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "last_action_result")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maximumNumberOfMachines")
    def maximum_number_of_machines(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum number of VMs in this hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "maximum_number_of_machines")

    @property
    @pulumi.getter(name="multiRoleCount")
    def multi_role_count(self) -> pulumi.Output[Optional[int]]:
        """
        Number of front-end instances
        """
        return pulumi.get(self, "multi_role_count")

    @property
    @pulumi.getter(name="multiSize")
    def multi_size(self) -> pulumi.Output[Optional[str]]:
        """
        Front-end VM size, e.g. "Medium", "Large"
        """
        return pulumi.get(self, "multi_size")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkAccessControlList")
    def network_access_control_list(self) -> pulumi.Output[Optional[Sequence['outputs.NetworkAccessControlEntryResponse']]]:
        """
        Access control list for controlling traffic to the hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "network_access_control_list")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Provisioning state of the hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> pulumi.Output[Optional[str]]:
        """
        Resource group of the hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "resource_group")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Current status of the hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> pulumi.Output[Optional[str]]:
        """
        Subscription of the hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "subscription_id")

    @property
    @pulumi.getter
    def suspended(self) -> pulumi.Output[Optional[bool]]:
        """
        True/false indicating whether the hostingEnvironment is suspended. The environment can be suspended e.g. when the management endpoint is no longer available
                    (most likely because NSG blocked the incoming traffic)
        """
        return pulumi.get(self, "suspended")

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

    @property
    @pulumi.getter(name="upgradeDomains")
    def upgrade_domains(self) -> pulumi.Output[Optional[int]]:
        """
        Number of upgrade domains of this hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "upgrade_domains")

    @property
    @pulumi.getter(name="vipMappings")
    def vip_mappings(self) -> pulumi.Output[Optional[Sequence['outputs.VirtualIPMappingResponse']]]:
        """
        Description of IP SSL mapping for this hostingEnvironment (App Service Environment)
        """
        return pulumi.get(self, "vip_mappings")

    @property
    @pulumi.getter(name="virtualNetwork")
    def virtual_network(self) -> pulumi.Output[Optional['outputs.VirtualNetworkProfileResponse']]:
        """
        Description of the hostingEnvironment's (App Service Environment) virtual network
        """
        return pulumi.get(self, "virtual_network")

    @property
    @pulumi.getter(name="vnetName")
    def vnet_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the hostingEnvironment's (App Service Environment) virtual network
        """
        return pulumi.get(self, "vnet_name")

    @property
    @pulumi.getter(name="vnetResourceGroupName")
    def vnet_resource_group_name(self) -> pulumi.Output[Optional[str]]:
        """
        Resource group of the hostingEnvironment's (App Service Environment) virtual network
        """
        return pulumi.get(self, "vnet_resource_group_name")

    @property
    @pulumi.getter(name="vnetSubnetName")
    def vnet_subnet_name(self) -> pulumi.Output[Optional[str]]:
        """
        Subnet of the hostingEnvironment's (App Service Environment) virtual network
        """
        return pulumi.get(self, "vnet_subnet_name")

    @property
    @pulumi.getter(name="workerPools")
    def worker_pools(self) -> pulumi.Output[Optional[Sequence['outputs.WorkerPoolResponse']]]:
        """
        Description of worker pools with worker size ids, VM sizes, and number of workers in each pool
        """
        return pulumi.get(self, "worker_pools")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

