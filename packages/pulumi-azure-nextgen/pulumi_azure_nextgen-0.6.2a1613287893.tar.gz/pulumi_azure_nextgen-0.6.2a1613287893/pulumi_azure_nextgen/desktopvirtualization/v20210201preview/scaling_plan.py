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

__all__ = ['ScalingPlan']


class ScalingPlan(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 exclusion_tag: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 host_pool_references: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScalingHostPoolReferenceArgs']]]]] = None,
                 host_pool_type: Optional[pulumi.Input[Union[str, 'HostPoolType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 scaling_plan_name: Optional[pulumi.Input[str]] = None,
                 schedules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScalingScheduleArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 time_zone: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents a scaling plan definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of scaling plan.
        :param pulumi.Input[str] exclusion_tag: Exclusion tag for scaling plan.
        :param pulumi.Input[str] friendly_name: User friendly name of scaling plan.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScalingHostPoolReferenceArgs']]]] host_pool_references: List of ScalingHostPoolReference definitions.
        :param pulumi.Input[Union[str, 'HostPoolType']] host_pool_type: HostPool type for scaling plan.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] scaling_plan_name: The name of the scaling plan.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScalingScheduleArgs']]]] schedules: List of ScalingSchedule definitions.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] time_zone: Timezone of the scaling plan.
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

            __props__['description'] = description
            __props__['exclusion_tag'] = exclusion_tag
            __props__['friendly_name'] = friendly_name
            __props__['host_pool_references'] = host_pool_references
            __props__['host_pool_type'] = host_pool_type
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if scaling_plan_name is None and not opts.urn:
                raise TypeError("Missing required property 'scaling_plan_name'")
            __props__['scaling_plan_name'] = scaling_plan_name
            __props__['schedules'] = schedules
            __props__['tags'] = tags
            __props__['time_zone'] = time_zone
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:desktopvirtualization:ScalingPlan"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20201110preview:ScalingPlan"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20210114preview:ScalingPlan")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ScalingPlan, __self__).__init__(
            'azure-nextgen:desktopvirtualization/v20210201preview:ScalingPlan',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ScalingPlan':
        """
        Get an existing ScalingPlan resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ScalingPlan(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of scaling plan.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="exclusionTag")
    def exclusion_tag(self) -> pulumi.Output[Optional[str]]:
        """
        Exclusion tag for scaling plan.
        """
        return pulumi.get(self, "exclusion_tag")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> pulumi.Output[Optional[str]]:
        """
        User friendly name of scaling plan.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="hostPoolReferences")
    def host_pool_references(self) -> pulumi.Output[Optional[Sequence['outputs.ScalingHostPoolReferenceResponse']]]:
        """
        List of ScalingHostPoolReference definitions.
        """
        return pulumi.get(self, "host_pool_references")

    @property
    @pulumi.getter(name="hostPoolType")
    def host_pool_type(self) -> pulumi.Output[Optional[str]]:
        """
        HostPool type for scaling plan.
        """
        return pulumi.get(self, "host_pool_type")

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
    @pulumi.getter
    def schedules(self) -> pulumi.Output[Optional[Sequence['outputs.ScalingScheduleResponse']]]:
        """
        List of ScalingSchedule definitions.
        """
        return pulumi.get(self, "schedules")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> pulumi.Output[Optional[str]]:
        """
        Timezone of the scaling plan.
        """
        return pulumi.get(self, "time_zone")

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

