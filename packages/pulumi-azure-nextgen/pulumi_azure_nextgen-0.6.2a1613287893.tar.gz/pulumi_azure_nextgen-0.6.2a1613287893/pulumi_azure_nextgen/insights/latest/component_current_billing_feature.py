# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['ComponentCurrentBillingFeature']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:insights:ComponentCurrentBillingFeature'.""", DeprecationWarning)


class ComponentCurrentBillingFeature(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:insights:ComponentCurrentBillingFeature'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 current_billing_features: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_volume_cap: Optional[pulumi.Input[pulumi.InputType['ApplicationInsightsComponentDataVolumeCapArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        An Application Insights component billing features
        Latest API Version: 2015-05-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] current_billing_features: Current enabled pricing plan. When the component is in the Enterprise plan, this will list both 'Basic' and 'Application Insights Enterprise'.
        :param pulumi.Input[pulumi.InputType['ApplicationInsightsComponentDataVolumeCapArgs']] data_volume_cap: An Application Insights component daily data volume cap
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name_: The name of the Application Insights component resource.
        """
        pulumi.log.warn("ComponentCurrentBillingFeature is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:insights:ComponentCurrentBillingFeature'.")
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

            __props__['current_billing_features'] = current_billing_features
            __props__['data_volume_cap'] = data_volume_cap
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__['resource_name'] = resource_name_
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:insights:ComponentCurrentBillingFeature"), pulumi.Alias(type_="azure-nextgen:insights/v20150501:ComponentCurrentBillingFeature")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ComponentCurrentBillingFeature, __self__).__init__(
            'azure-nextgen:insights/latest:ComponentCurrentBillingFeature',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ComponentCurrentBillingFeature':
        """
        Get an existing ComponentCurrentBillingFeature resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ComponentCurrentBillingFeature(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="currentBillingFeatures")
    def current_billing_features(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Current enabled pricing plan. When the component is in the Enterprise plan, this will list both 'Basic' and 'Application Insights Enterprise'.
        """
        return pulumi.get(self, "current_billing_features")

    @property
    @pulumi.getter(name="dataVolumeCap")
    def data_volume_cap(self) -> pulumi.Output[Optional['outputs.ApplicationInsightsComponentDataVolumeCapResponse']]:
        """
        An Application Insights component daily data volume cap
        """
        return pulumi.get(self, "data_volume_cap")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

