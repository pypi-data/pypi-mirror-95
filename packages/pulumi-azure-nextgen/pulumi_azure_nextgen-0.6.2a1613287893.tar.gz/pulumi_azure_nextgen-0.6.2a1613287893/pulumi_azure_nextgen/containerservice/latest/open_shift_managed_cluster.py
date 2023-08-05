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

__all__ = ['OpenShiftManagedCluster']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:containerservice:OpenShiftManagedCluster'.""", DeprecationWarning)


class OpenShiftManagedCluster(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:containerservice:OpenShiftManagedCluster'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_pool_profiles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OpenShiftManagedClusterAgentPoolProfileArgs']]]]] = None,
                 auth_profile: Optional[pulumi.Input[pulumi.InputType['OpenShiftManagedClusterAuthProfileArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 master_pool_profile: Optional[pulumi.Input[pulumi.InputType['OpenShiftManagedClusterMasterPoolProfileArgs']]] = None,
                 network_profile: Optional[pulumi.Input[pulumi.InputType['NetworkProfileArgs']]] = None,
                 open_shift_version: Optional[pulumi.Input[str]] = None,
                 plan: Optional[pulumi.Input[pulumi.InputType['PurchasePlanArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 router_profiles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OpenShiftRouterProfileArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        OpenShift Managed cluster.
        Latest API Version: 2019-04-30.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OpenShiftManagedClusterAgentPoolProfileArgs']]]] agent_pool_profiles: Configuration of OpenShift cluster VMs.
        :param pulumi.Input[pulumi.InputType['OpenShiftManagedClusterAuthProfileArgs']] auth_profile: Configures OpenShift authentication.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[pulumi.InputType['OpenShiftManagedClusterMasterPoolProfileArgs']] master_pool_profile: Configuration for OpenShift master VMs.
        :param pulumi.Input[pulumi.InputType['NetworkProfileArgs']] network_profile: Configuration for OpenShift networking.
        :param pulumi.Input[str] open_shift_version: Version of OpenShift specified when creating the cluster.
        :param pulumi.Input[pulumi.InputType['PurchasePlanArgs']] plan: Define the resource plan as required by ARM for billing purposes
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] resource_name_: The name of the OpenShift managed cluster resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OpenShiftRouterProfileArgs']]]] router_profiles: Configuration for OpenShift router(s).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        pulumi.log.warn("OpenShiftManagedCluster is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:containerservice:OpenShiftManagedCluster'.")
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

            __props__['agent_pool_profiles'] = agent_pool_profiles
            __props__['auth_profile'] = auth_profile
            __props__['location'] = location
            __props__['master_pool_profile'] = master_pool_profile
            __props__['network_profile'] = network_profile
            if open_shift_version is None and not opts.urn:
                raise TypeError("Missing required property 'open_shift_version'")
            __props__['open_shift_version'] = open_shift_version
            __props__['plan'] = plan
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__['resource_name'] = resource_name_
            __props__['router_profiles'] = router_profiles
            __props__['tags'] = tags
            __props__['cluster_version'] = None
            __props__['fqdn'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['public_hostname'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:containerservice:OpenShiftManagedCluster"), pulumi.Alias(type_="azure-nextgen:containerservice/v20180930preview:OpenShiftManagedCluster"), pulumi.Alias(type_="azure-nextgen:containerservice/v20190430:OpenShiftManagedCluster"), pulumi.Alias(type_="azure-nextgen:containerservice/v20190930preview:OpenShiftManagedCluster"), pulumi.Alias(type_="azure-nextgen:containerservice/v20191027preview:OpenShiftManagedCluster")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(OpenShiftManagedCluster, __self__).__init__(
            'azure-nextgen:containerservice/latest:OpenShiftManagedCluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'OpenShiftManagedCluster':
        """
        Get an existing OpenShiftManagedCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return OpenShiftManagedCluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentPoolProfiles")
    def agent_pool_profiles(self) -> pulumi.Output[Optional[Sequence['outputs.OpenShiftManagedClusterAgentPoolProfileResponse']]]:
        """
        Configuration of OpenShift cluster VMs.
        """
        return pulumi.get(self, "agent_pool_profiles")

    @property
    @pulumi.getter(name="authProfile")
    def auth_profile(self) -> pulumi.Output[Optional['outputs.OpenShiftManagedClusterAuthProfileResponse']]:
        """
        Configures OpenShift authentication.
        """
        return pulumi.get(self, "auth_profile")

    @property
    @pulumi.getter(name="clusterVersion")
    def cluster_version(self) -> pulumi.Output[str]:
        """
        Version of OpenShift specified when creating the cluster.
        """
        return pulumi.get(self, "cluster_version")

    @property
    @pulumi.getter
    def fqdn(self) -> pulumi.Output[str]:
        """
        Service generated FQDN for OpenShift API server loadbalancer internal hostname.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="masterPoolProfile")
    def master_pool_profile(self) -> pulumi.Output[Optional['outputs.OpenShiftManagedClusterMasterPoolProfileResponse']]:
        """
        Configuration for OpenShift master VMs.
        """
        return pulumi.get(self, "master_pool_profile")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkProfile")
    def network_profile(self) -> pulumi.Output[Optional['outputs.NetworkProfileResponse']]:
        """
        Configuration for OpenShift networking.
        """
        return pulumi.get(self, "network_profile")

    @property
    @pulumi.getter(name="openShiftVersion")
    def open_shift_version(self) -> pulumi.Output[str]:
        """
        Version of OpenShift specified when creating the cluster.
        """
        return pulumi.get(self, "open_shift_version")

    @property
    @pulumi.getter
    def plan(self) -> pulumi.Output[Optional['outputs.PurchasePlanResponse']]:
        """
        Define the resource plan as required by ARM for billing purposes
        """
        return pulumi.get(self, "plan")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The current deployment or provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicHostname")
    def public_hostname(self) -> pulumi.Output[str]:
        """
        Service generated FQDN for OpenShift API server.
        """
        return pulumi.get(self, "public_hostname")

    @property
    @pulumi.getter(name="routerProfiles")
    def router_profiles(self) -> pulumi.Output[Optional[Sequence['outputs.OpenShiftRouterProfileResponse']]]:
        """
        Configuration for OpenShift router(s).
        """
        return pulumi.get(self, "router_profiles")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

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

