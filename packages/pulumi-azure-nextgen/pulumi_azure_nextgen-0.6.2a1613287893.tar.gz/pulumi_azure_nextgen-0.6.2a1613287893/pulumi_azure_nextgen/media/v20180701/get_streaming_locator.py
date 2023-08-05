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
    'GetStreamingLocatorResult',
    'AwaitableGetStreamingLocatorResult',
    'get_streaming_locator',
]

@pulumi.output_type
class GetStreamingLocatorResult:
    """
    A Streaming Locator resource
    """
    def __init__(__self__, alternative_media_id=None, asset_name=None, content_keys=None, created=None, default_content_key_policy_name=None, end_time=None, filters=None, id=None, name=None, start_time=None, streaming_locator_id=None, streaming_policy_name=None, type=None):
        if alternative_media_id and not isinstance(alternative_media_id, str):
            raise TypeError("Expected argument 'alternative_media_id' to be a str")
        pulumi.set(__self__, "alternative_media_id", alternative_media_id)
        if asset_name and not isinstance(asset_name, str):
            raise TypeError("Expected argument 'asset_name' to be a str")
        pulumi.set(__self__, "asset_name", asset_name)
        if content_keys and not isinstance(content_keys, list):
            raise TypeError("Expected argument 'content_keys' to be a list")
        pulumi.set(__self__, "content_keys", content_keys)
        if created and not isinstance(created, str):
            raise TypeError("Expected argument 'created' to be a str")
        pulumi.set(__self__, "created", created)
        if default_content_key_policy_name and not isinstance(default_content_key_policy_name, str):
            raise TypeError("Expected argument 'default_content_key_policy_name' to be a str")
        pulumi.set(__self__, "default_content_key_policy_name", default_content_key_policy_name)
        if end_time and not isinstance(end_time, str):
            raise TypeError("Expected argument 'end_time' to be a str")
        pulumi.set(__self__, "end_time", end_time)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
        if streaming_locator_id and not isinstance(streaming_locator_id, str):
            raise TypeError("Expected argument 'streaming_locator_id' to be a str")
        pulumi.set(__self__, "streaming_locator_id", streaming_locator_id)
        if streaming_policy_name and not isinstance(streaming_policy_name, str):
            raise TypeError("Expected argument 'streaming_policy_name' to be a str")
        pulumi.set(__self__, "streaming_policy_name", streaming_policy_name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="alternativeMediaId")
    def alternative_media_id(self) -> Optional[str]:
        """
        Alternative Media ID of this Streaming Locator
        """
        return pulumi.get(self, "alternative_media_id")

    @property
    @pulumi.getter(name="assetName")
    def asset_name(self) -> str:
        """
        Asset Name
        """
        return pulumi.get(self, "asset_name")

    @property
    @pulumi.getter(name="contentKeys")
    def content_keys(self) -> Optional[Sequence['outputs.StreamingLocatorContentKeyResponse']]:
        """
        The ContentKeys used by this Streaming Locator.
        """
        return pulumi.get(self, "content_keys")

    @property
    @pulumi.getter
    def created(self) -> str:
        """
        The creation time of the Streaming Locator.
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter(name="defaultContentKeyPolicyName")
    def default_content_key_policy_name(self) -> Optional[str]:
        """
        Name of the default ContentKeyPolicy used by this Streaming Locator.
        """
        return pulumi.get(self, "default_content_key_policy_name")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[str]:
        """
        The end time of the Streaming Locator.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence[str]]:
        """
        A list of asset or account filters which apply to this streaming locator
        """
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[str]:
        """
        The start time of the Streaming Locator.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter(name="streamingLocatorId")
    def streaming_locator_id(self) -> Optional[str]:
        """
        The StreamingLocatorId of the Streaming Locator.
        """
        return pulumi.get(self, "streaming_locator_id")

    @property
    @pulumi.getter(name="streamingPolicyName")
    def streaming_policy_name(self) -> str:
        """
        Name of the Streaming Policy used by this Streaming Locator. Either specify the name of Streaming Policy you created or use one of the predefined Streaming Policies. The predefined Streaming Policies available are: 'Predefined_DownloadOnly', 'Predefined_ClearStreamingOnly', 'Predefined_DownloadAndClearStreaming', 'Predefined_ClearKey', 'Predefined_MultiDrmCencStreaming' and 'Predefined_MultiDrmStreaming'
        """
        return pulumi.get(self, "streaming_policy_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetStreamingLocatorResult(GetStreamingLocatorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStreamingLocatorResult(
            alternative_media_id=self.alternative_media_id,
            asset_name=self.asset_name,
            content_keys=self.content_keys,
            created=self.created,
            default_content_key_policy_name=self.default_content_key_policy_name,
            end_time=self.end_time,
            filters=self.filters,
            id=self.id,
            name=self.name,
            start_time=self.start_time,
            streaming_locator_id=self.streaming_locator_id,
            streaming_policy_name=self.streaming_policy_name,
            type=self.type)


def get_streaming_locator(account_name: Optional[str] = None,
                          resource_group_name: Optional[str] = None,
                          streaming_locator_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStreamingLocatorResult:
    """
    Use this data source to access information about an existing resource.

    :param str account_name: The Media Services account name.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    :param str streaming_locator_name: The Streaming Locator name.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['streamingLocatorName'] = streaming_locator_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:media/v20180701:getStreamingLocator', __args__, opts=opts, typ=GetStreamingLocatorResult).value

    return AwaitableGetStreamingLocatorResult(
        alternative_media_id=__ret__.alternative_media_id,
        asset_name=__ret__.asset_name,
        content_keys=__ret__.content_keys,
        created=__ret__.created,
        default_content_key_policy_name=__ret__.default_content_key_policy_name,
        end_time=__ret__.end_time,
        filters=__ret__.filters,
        id=__ret__.id,
        name=__ret__.name,
        start_time=__ret__.start_time,
        streaming_locator_id=__ret__.streaming_locator_id,
        streaming_policy_name=__ret__.streaming_policy_name,
        type=__ret__.type)
