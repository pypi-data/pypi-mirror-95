# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetExposureControlFeatureValueResult',
    'AwaitableGetExposureControlFeatureValueResult',
    'get_exposure_control_feature_value',
]

@pulumi.output_type
class GetExposureControlFeatureValueResult:
    """
    The exposure control response.
    """
    def __init__(__self__, feature_name=None, value=None):
        if feature_name and not isinstance(feature_name, str):
            raise TypeError("Expected argument 'feature_name' to be a str")
        pulumi.set(__self__, "feature_name", feature_name)
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="featureName")
    def feature_name(self) -> str:
        """
        The feature name.
        """
        return pulumi.get(self, "feature_name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The feature value.
        """
        return pulumi.get(self, "value")


class AwaitableGetExposureControlFeatureValueResult(GetExposureControlFeatureValueResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetExposureControlFeatureValueResult(
            feature_name=self.feature_name,
            value=self.value)


def get_exposure_control_feature_value(feature_name: Optional[str] = None,
                                       feature_type: Optional[str] = None,
                                       location_id: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetExposureControlFeatureValueResult:
    """
    Use this data source to access information about an existing resource.

    :param str feature_name: The feature name.
    :param str feature_type: The feature type.
    :param str location_id: The location identifier.
    """
    __args__ = dict()
    __args__['featureName'] = feature_name
    __args__['featureType'] = feature_type
    __args__['locationId'] = location_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:datafactory/latest:getExposureControlFeatureValue', __args__, opts=opts, typ=GetExposureControlFeatureValueResult).value

    return AwaitableGetExposureControlFeatureValueResult(
        feature_name=__ret__.feature_name,
        value=__ret__.value)
