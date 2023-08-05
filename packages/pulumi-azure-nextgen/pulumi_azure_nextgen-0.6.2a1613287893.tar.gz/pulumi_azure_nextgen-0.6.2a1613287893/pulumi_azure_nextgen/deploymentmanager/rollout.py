# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['Rollout']


class Rollout(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifact_source_id: Optional[pulumi.Input[str]] = None,
                 build_version: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rollout_name: Optional[pulumi.Input[str]] = None,
                 step_groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StepGroupArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_service_topology_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Defines the PUT rollout request body.
        API Version: 2019-11-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] artifact_source_id: The reference to the artifact source resource Id where the payload is located.
        :param pulumi.Input[str] build_version: The version of the build being deployed.
        :param pulumi.Input[pulumi.InputType['IdentityArgs']] identity: Identity for the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] rollout_name: The rollout name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StepGroupArgs']]]] step_groups: The list of step groups that define the orchestration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] target_service_topology_id: The resource Id of the service topology from which service units are being referenced in step groups to be deployed.
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

            __props__['artifact_source_id'] = artifact_source_id
            if build_version is None and not opts.urn:
                raise TypeError("Missing required property 'build_version'")
            __props__['build_version'] = build_version
            if identity is None and not opts.urn:
                raise TypeError("Missing required property 'identity'")
            __props__['identity'] = identity
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if rollout_name is None and not opts.urn:
                raise TypeError("Missing required property 'rollout_name'")
            __props__['rollout_name'] = rollout_name
            if step_groups is None and not opts.urn:
                raise TypeError("Missing required property 'step_groups'")
            __props__['step_groups'] = step_groups
            __props__['tags'] = tags
            if target_service_topology_id is None and not opts.urn:
                raise TypeError("Missing required property 'target_service_topology_id'")
            __props__['target_service_topology_id'] = target_service_topology_id
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:deploymentmanager/v20180901preview:Rollout"), pulumi.Alias(type_="azure-nextgen:deploymentmanager/v20191101preview:Rollout")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Rollout, __self__).__init__(
            'azure-nextgen:deploymentmanager:Rollout',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Rollout':
        """
        Get an existing Rollout resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Rollout(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="artifactSourceId")
    def artifact_source_id(self) -> pulumi.Output[Optional[str]]:
        """
        The reference to the artifact source resource Id where the payload is located.
        """
        return pulumi.get(self, "artifact_source_id")

    @property
    @pulumi.getter(name="buildVersion")
    def build_version(self) -> pulumi.Output[str]:
        """
        The version of the build being deployed.
        """
        return pulumi.get(self, "build_version")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output['outputs.IdentityResponse']:
        """
        Identity for the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="stepGroups")
    def step_groups(self) -> pulumi.Output[Sequence['outputs.StepGroupResponse']]:
        """
        The list of step groups that define the orchestration.
        """
        return pulumi.get(self, "step_groups")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetServiceTopologyId")
    def target_service_topology_id(self) -> pulumi.Output[str]:
        """
        The resource Id of the service topology from which service units are being referenced in step groups to be deployed.
        """
        return pulumi.get(self, "target_service_topology_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

