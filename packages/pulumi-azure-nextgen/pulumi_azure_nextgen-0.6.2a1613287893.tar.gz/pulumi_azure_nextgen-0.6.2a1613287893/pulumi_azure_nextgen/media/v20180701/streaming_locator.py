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

__all__ = ['StreamingLocator']


class StreamingLocator(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 alternative_media_id: Optional[pulumi.Input[str]] = None,
                 asset_name: Optional[pulumi.Input[str]] = None,
                 content_keys: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StreamingLocatorContentKeyArgs']]]]] = None,
                 default_content_key_policy_name: Optional[pulumi.Input[str]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 filters: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 streaming_locator_id: Optional[pulumi.Input[str]] = None,
                 streaming_locator_name: Optional[pulumi.Input[str]] = None,
                 streaming_policy_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A Streaming Locator resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The Media Services account name.
        :param pulumi.Input[str] alternative_media_id: Alternative Media ID of this Streaming Locator
        :param pulumi.Input[str] asset_name: Asset Name
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StreamingLocatorContentKeyArgs']]]] content_keys: The ContentKeys used by this Streaming Locator.
        :param pulumi.Input[str] default_content_key_policy_name: Name of the default ContentKeyPolicy used by this Streaming Locator.
        :param pulumi.Input[str] end_time: The end time of the Streaming Locator.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] filters: A list of asset or account filters which apply to this streaming locator
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the Azure subscription.
        :param pulumi.Input[str] start_time: The start time of the Streaming Locator.
        :param pulumi.Input[str] streaming_locator_id: The StreamingLocatorId of the Streaming Locator.
        :param pulumi.Input[str] streaming_locator_name: The Streaming Locator name.
        :param pulumi.Input[str] streaming_policy_name: Name of the Streaming Policy used by this Streaming Locator. Either specify the name of Streaming Policy you created or use one of the predefined Streaming Policies. The predefined Streaming Policies available are: 'Predefined_DownloadOnly', 'Predefined_ClearStreamingOnly', 'Predefined_DownloadAndClearStreaming', 'Predefined_ClearKey', 'Predefined_MultiDrmCencStreaming' and 'Predefined_MultiDrmStreaming'
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

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__['account_name'] = account_name
            __props__['alternative_media_id'] = alternative_media_id
            if asset_name is None and not opts.urn:
                raise TypeError("Missing required property 'asset_name'")
            __props__['asset_name'] = asset_name
            __props__['content_keys'] = content_keys
            __props__['default_content_key_policy_name'] = default_content_key_policy_name
            __props__['end_time'] = end_time
            __props__['filters'] = filters
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['start_time'] = start_time
            __props__['streaming_locator_id'] = streaming_locator_id
            if streaming_locator_name is None and not opts.urn:
                raise TypeError("Missing required property 'streaming_locator_name'")
            __props__['streaming_locator_name'] = streaming_locator_name
            if streaming_policy_name is None and not opts.urn:
                raise TypeError("Missing required property 'streaming_policy_name'")
            __props__['streaming_policy_name'] = streaming_policy_name
            __props__['created'] = None
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:media:StreamingLocator"), pulumi.Alias(type_="azure-nextgen:media/latest:StreamingLocator"), pulumi.Alias(type_="azure-nextgen:media/v20180330preview:StreamingLocator"), pulumi.Alias(type_="azure-nextgen:media/v20180601preview:StreamingLocator"), pulumi.Alias(type_="azure-nextgen:media/v20200501:StreamingLocator")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StreamingLocator, __self__).__init__(
            'azure-nextgen:media/v20180701:StreamingLocator',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StreamingLocator':
        """
        Get an existing StreamingLocator resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return StreamingLocator(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="alternativeMediaId")
    def alternative_media_id(self) -> pulumi.Output[Optional[str]]:
        """
        Alternative Media ID of this Streaming Locator
        """
        return pulumi.get(self, "alternative_media_id")

    @property
    @pulumi.getter(name="assetName")
    def asset_name(self) -> pulumi.Output[str]:
        """
        Asset Name
        """
        return pulumi.get(self, "asset_name")

    @property
    @pulumi.getter(name="contentKeys")
    def content_keys(self) -> pulumi.Output[Optional[Sequence['outputs.StreamingLocatorContentKeyResponse']]]:
        """
        The ContentKeys used by this Streaming Locator.
        """
        return pulumi.get(self, "content_keys")

    @property
    @pulumi.getter
    def created(self) -> pulumi.Output[str]:
        """
        The creation time of the Streaming Locator.
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter(name="defaultContentKeyPolicyName")
    def default_content_key_policy_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the default ContentKeyPolicy used by this Streaming Locator.
        """
        return pulumi.get(self, "default_content_key_policy_name")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[Optional[str]]:
        """
        The end time of the Streaming Locator.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def filters(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of asset or account filters which apply to this streaming locator
        """
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[Optional[str]]:
        """
        The start time of the Streaming Locator.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter(name="streamingLocatorId")
    def streaming_locator_id(self) -> pulumi.Output[Optional[str]]:
        """
        The StreamingLocatorId of the Streaming Locator.
        """
        return pulumi.get(self, "streaming_locator_id")

    @property
    @pulumi.getter(name="streamingPolicyName")
    def streaming_policy_name(self) -> pulumi.Output[str]:
        """
        Name of the Streaming Policy used by this Streaming Locator. Either specify the name of Streaming Policy you created or use one of the predefined Streaming Policies. The predefined Streaming Policies available are: 'Predefined_DownloadOnly', 'Predefined_ClearStreamingOnly', 'Predefined_DownloadAndClearStreaming', 'Predefined_ClearKey', 'Predefined_MultiDrmCencStreaming' and 'Predefined_MultiDrmStreaming'
        """
        return pulumi.get(self, "streaming_policy_name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

