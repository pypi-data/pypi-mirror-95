# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['BandwidthSchedule']


class BandwidthSchedule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 days: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]]] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rate_in_mbps: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 start: Optional[pulumi.Input[str]] = None,
                 stop: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The bandwidth schedule details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]] days: The days of the week when this schedule is applicable.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] name: The bandwidth schedule name which needs to be added/updated.
        :param pulumi.Input[int] rate_in_mbps: The bandwidth rate in Mbps.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[str] start: The start time of the schedule in UTC.
        :param pulumi.Input[str] stop: The stop time of the schedule in UTC.
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

            if days is None and not opts.urn:
                raise TypeError("Missing required property 'days'")
            __props__['days'] = days
            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__['device_name'] = device_name
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if rate_in_mbps is None and not opts.urn:
                raise TypeError("Missing required property 'rate_in_mbps'")
            __props__['rate_in_mbps'] = rate_in_mbps
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if start is None and not opts.urn:
                raise TypeError("Missing required property 'start'")
            __props__['start'] = start
            if stop is None and not opts.urn:
                raise TypeError("Missing required property 'stop'")
            __props__['stop'] = stop
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:databoxedge:BandwidthSchedule"), pulumi.Alias(type_="azure-nextgen:databoxedge/latest:BandwidthSchedule"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20190701:BandwidthSchedule"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20190801:BandwidthSchedule"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200501preview:BandwidthSchedule"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200901:BandwidthSchedule"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200901preview:BandwidthSchedule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(BandwidthSchedule, __self__).__init__(
            'azure-nextgen:databoxedge/v20190301:BandwidthSchedule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BandwidthSchedule':
        """
        Get an existing BandwidthSchedule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return BandwidthSchedule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def days(self) -> pulumi.Output[Sequence[str]]:
        """
        The days of the week when this schedule is applicable.
        """
        return pulumi.get(self, "days")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="rateInMbps")
    def rate_in_mbps(self) -> pulumi.Output[int]:
        """
        The bandwidth rate in Mbps.
        """
        return pulumi.get(self, "rate_in_mbps")

    @property
    @pulumi.getter
    def start(self) -> pulumi.Output[str]:
        """
        The start time of the schedule in UTC.
        """
        return pulumi.get(self, "start")

    @property
    @pulumi.getter
    def stop(self) -> pulumi.Output[str]:
        """
        The stop time of the schedule in UTC.
        """
        return pulumi.get(self, "stop")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

