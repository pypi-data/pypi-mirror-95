# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['IotSensor']


class IotSensor(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 iot_sensor_name: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 ti_automatic_updates: Optional[pulumi.Input[bool]] = None,
                 zone: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        IoT sensor model
        API Version: 2020-08-06-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] iot_sensor_name: Name of the IoT sensor
        :param pulumi.Input[str] scope: Scope of the query (IoT Hub, /providers/Microsoft.Devices/iotHubs/myHub)
        :param pulumi.Input[bool] ti_automatic_updates: TI Automatic mode status of the IoT sensor
        :param pulumi.Input[str] zone: Zone of the IoT sensor
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

            if iot_sensor_name is None and not opts.urn:
                raise TypeError("Missing required property 'iot_sensor_name'")
            __props__['iot_sensor_name'] = iot_sensor_name
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__['scope'] = scope
            __props__['ti_automatic_updates'] = ti_automatic_updates
            __props__['zone'] = zone
            __props__['connectivity_time'] = None
            __props__['creation_time'] = None
            __props__['dynamic_learning'] = None
            __props__['learning_mode'] = None
            __props__['name'] = None
            __props__['sensor_status'] = None
            __props__['sensor_version'] = None
            __props__['ti_status'] = None
            __props__['ti_version'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:security/v20200806preview:IotSensor")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(IotSensor, __self__).__init__(
            'azure-nextgen:security:IotSensor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'IotSensor':
        """
        Get an existing IotSensor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return IotSensor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectivityTime")
    def connectivity_time(self) -> pulumi.Output[str]:
        """
        Last connectivity time of the IoT sensor
        """
        return pulumi.get(self, "connectivity_time")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        Creation time of the IoT sensor
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="dynamicLearning")
    def dynamic_learning(self) -> pulumi.Output[bool]:
        """
        Dynamic mode status of the IoT sensor
        """
        return pulumi.get(self, "dynamic_learning")

    @property
    @pulumi.getter(name="learningMode")
    def learning_mode(self) -> pulumi.Output[bool]:
        """
        Learning mode status of the IoT sensor
        """
        return pulumi.get(self, "learning_mode")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sensorStatus")
    def sensor_status(self) -> pulumi.Output[str]:
        """
        Status of the IoT sensor
        """
        return pulumi.get(self, "sensor_status")

    @property
    @pulumi.getter(name="sensorVersion")
    def sensor_version(self) -> pulumi.Output[str]:
        """
        Version of the IoT sensor
        """
        return pulumi.get(self, "sensor_version")

    @property
    @pulumi.getter(name="tiAutomaticUpdates")
    def ti_automatic_updates(self) -> pulumi.Output[Optional[bool]]:
        """
        TI Automatic mode status of the IoT sensor
        """
        return pulumi.get(self, "ti_automatic_updates")

    @property
    @pulumi.getter(name="tiStatus")
    def ti_status(self) -> pulumi.Output[str]:
        """
        TI Status of the IoT sensor
        """
        return pulumi.get(self, "ti_status")

    @property
    @pulumi.getter(name="tiVersion")
    def ti_version(self) -> pulumi.Output[str]:
        """
        TI Version of the IoT sensor
        """
        return pulumi.get(self, "ti_version")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def zone(self) -> pulumi.Output[Optional[str]]:
        """
        Zone of the IoT sensor
        """
        return pulumi.get(self, "zone")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

