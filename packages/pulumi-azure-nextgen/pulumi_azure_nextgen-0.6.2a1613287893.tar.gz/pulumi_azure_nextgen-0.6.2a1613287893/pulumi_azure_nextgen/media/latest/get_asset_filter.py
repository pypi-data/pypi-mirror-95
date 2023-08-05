# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = [
    'GetAssetFilterResult',
    'AwaitableGetAssetFilterResult',
    'get_asset_filter',
]

@pulumi.output_type
class GetAssetFilterResult:
    """
    An Asset Filter.
    """
    def __init__(__self__, first_quality=None, id=None, name=None, presentation_time_range=None, system_data=None, tracks=None, type=None):
        if first_quality and not isinstance(first_quality, dict):
            raise TypeError("Expected argument 'first_quality' to be a dict")
        pulumi.set(__self__, "first_quality", first_quality)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if presentation_time_range and not isinstance(presentation_time_range, dict):
            raise TypeError("Expected argument 'presentation_time_range' to be a dict")
        pulumi.set(__self__, "presentation_time_range", presentation_time_range)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tracks and not isinstance(tracks, list):
            raise TypeError("Expected argument 'tracks' to be a list")
        pulumi.set(__self__, "tracks", tracks)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="firstQuality")
    def first_quality(self) -> Optional['outputs.FirstQualityResponse']:
        """
        The first quality.
        """
        return pulumi.get(self, "first_quality")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="presentationTimeRange")
    def presentation_time_range(self) -> Optional['outputs.PresentationTimeRangeResponse']:
        """
        The presentation time range.
        """
        return pulumi.get(self, "presentation_time_range")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tracks(self) -> Optional[Sequence['outputs.FilterTrackSelectionResponse']]:
        """
        The tracks selection conditions.
        """
        return pulumi.get(self, "tracks")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetAssetFilterResult(GetAssetFilterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAssetFilterResult(
            first_quality=self.first_quality,
            id=self.id,
            name=self.name,
            presentation_time_range=self.presentation_time_range,
            system_data=self.system_data,
            tracks=self.tracks,
            type=self.type)


def get_asset_filter(account_name: Optional[str] = None,
                     asset_name: Optional[str] = None,
                     filter_name: Optional[str] = None,
                     resource_group_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAssetFilterResult:
    """
    Use this data source to access information about an existing resource.

    :param str account_name: The Media Services account name.
    :param str asset_name: The Asset name.
    :param str filter_name: The Asset Filter name
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['assetName'] = asset_name
    __args__['filterName'] = filter_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:media/latest:getAssetFilter', __args__, opts=opts, typ=GetAssetFilterResult).value

    return AwaitableGetAssetFilterResult(
        first_quality=__ret__.first_quality,
        id=__ret__.id,
        name=__ret__.name,
        presentation_time_range=__ret__.presentation_time_range,
        system_data=__ret__.system_data,
        tracks=__ret__.tracks,
        type=__ret__.type)
