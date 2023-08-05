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
    'GetLiveEventResult',
    'AwaitableGetLiveEventResult',
    'get_live_event',
]

@pulumi.output_type
class GetLiveEventResult:
    """
    The live event.
    """
    def __init__(__self__, created=None, cross_site_access_policies=None, description=None, encoding=None, hostname_prefix=None, id=None, input=None, last_modified=None, location=None, name=None, preview=None, provisioning_state=None, resource_state=None, stream_options=None, system_data=None, tags=None, transcriptions=None, type=None, use_static_hostname=None):
        if created and not isinstance(created, str):
            raise TypeError("Expected argument 'created' to be a str")
        pulumi.set(__self__, "created", created)
        if cross_site_access_policies and not isinstance(cross_site_access_policies, dict):
            raise TypeError("Expected argument 'cross_site_access_policies' to be a dict")
        pulumi.set(__self__, "cross_site_access_policies", cross_site_access_policies)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if encoding and not isinstance(encoding, dict):
            raise TypeError("Expected argument 'encoding' to be a dict")
        pulumi.set(__self__, "encoding", encoding)
        if hostname_prefix and not isinstance(hostname_prefix, str):
            raise TypeError("Expected argument 'hostname_prefix' to be a str")
        pulumi.set(__self__, "hostname_prefix", hostname_prefix)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if input and not isinstance(input, dict):
            raise TypeError("Expected argument 'input' to be a dict")
        pulumi.set(__self__, "input", input)
        if last_modified and not isinstance(last_modified, str):
            raise TypeError("Expected argument 'last_modified' to be a str")
        pulumi.set(__self__, "last_modified", last_modified)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if preview and not isinstance(preview, dict):
            raise TypeError("Expected argument 'preview' to be a dict")
        pulumi.set(__self__, "preview", preview)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_state and not isinstance(resource_state, str):
            raise TypeError("Expected argument 'resource_state' to be a str")
        pulumi.set(__self__, "resource_state", resource_state)
        if stream_options and not isinstance(stream_options, list):
            raise TypeError("Expected argument 'stream_options' to be a list")
        pulumi.set(__self__, "stream_options", stream_options)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if transcriptions and not isinstance(transcriptions, list):
            raise TypeError("Expected argument 'transcriptions' to be a list")
        pulumi.set(__self__, "transcriptions", transcriptions)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if use_static_hostname and not isinstance(use_static_hostname, bool):
            raise TypeError("Expected argument 'use_static_hostname' to be a bool")
        pulumi.set(__self__, "use_static_hostname", use_static_hostname)

    @property
    @pulumi.getter
    def created(self) -> str:
        """
        The creation time for the live event
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter(name="crossSiteAccessPolicies")
    def cross_site_access_policies(self) -> Optional['outputs.CrossSiteAccessPoliciesResponse']:
        """
        Live event cross site access policies.
        """
        return pulumi.get(self, "cross_site_access_policies")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description for the live event.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def encoding(self) -> Optional['outputs.LiveEventEncodingResponse']:
        """
        Encoding settings for the live event. It configures whether a live encoder is used for the live event and settings for the live encoder if it is used.
        """
        return pulumi.get(self, "encoding")

    @property
    @pulumi.getter(name="hostnamePrefix")
    def hostname_prefix(self) -> Optional[str]:
        """
        When useStaticHostname is set to true, the hostnamePrefix specifies the first part of the hostname assigned to the live event preview and ingest endpoints. The final hostname would be a combination of this prefix, the media service account name and a short code for the Azure Media Services data center.
        """
        return pulumi.get(self, "hostname_prefix")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def input(self) -> 'outputs.LiveEventInputResponse':
        """
        Live event input settings. It defines how the live event receives input from a contribution encoder.
        """
        return pulumi.get(self, "input")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> str:
        """
        The last modified time of the live event.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def preview(self) -> Optional['outputs.LiveEventPreviewResponse']:
        """
        Live event preview settings. Preview allows live event producers to preview the live streaming content without creating any live output.
        """
        return pulumi.get(self, "preview")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the live event.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> str:
        """
        The resource state of the live event. See https://go.microsoft.com/fwlink/?linkid=2139012 for more information.
        """
        return pulumi.get(self, "resource_state")

    @property
    @pulumi.getter(name="streamOptions")
    def stream_options(self) -> Optional[Sequence[str]]:
        """
        The options to use for the LiveEvent. This value is specified at creation time and cannot be updated. The valid values for the array entry values are 'Default' and 'LowLatency'.
        """
        return pulumi.get(self, "stream_options")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def transcriptions(self) -> Optional[Sequence['outputs.LiveEventTranscriptionResponse']]:
        """
        Live transcription settings for the live event. See https://go.microsoft.com/fwlink/?linkid=2133742 for more information about the live transcription feature.
        """
        return pulumi.get(self, "transcriptions")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="useStaticHostname")
    def use_static_hostname(self) -> Optional[bool]:
        """
        Specifies whether a static hostname would be assigned to the live event preview and ingest endpoints. This value can only be updated if the live event is in Standby state
        """
        return pulumi.get(self, "use_static_hostname")


class AwaitableGetLiveEventResult(GetLiveEventResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLiveEventResult(
            created=self.created,
            cross_site_access_policies=self.cross_site_access_policies,
            description=self.description,
            encoding=self.encoding,
            hostname_prefix=self.hostname_prefix,
            id=self.id,
            input=self.input,
            last_modified=self.last_modified,
            location=self.location,
            name=self.name,
            preview=self.preview,
            provisioning_state=self.provisioning_state,
            resource_state=self.resource_state,
            stream_options=self.stream_options,
            system_data=self.system_data,
            tags=self.tags,
            transcriptions=self.transcriptions,
            type=self.type,
            use_static_hostname=self.use_static_hostname)


def get_live_event(account_name: Optional[str] = None,
                   live_event_name: Optional[str] = None,
                   resource_group_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLiveEventResult:
    """
    Use this data source to access information about an existing resource.

    :param str account_name: The Media Services account name.
    :param str live_event_name: The name of the live event, maximum length is 32.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['liveEventName'] = live_event_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:media/latest:getLiveEvent', __args__, opts=opts, typ=GetLiveEventResult).value

    return AwaitableGetLiveEventResult(
        created=__ret__.created,
        cross_site_access_policies=__ret__.cross_site_access_policies,
        description=__ret__.description,
        encoding=__ret__.encoding,
        hostname_prefix=__ret__.hostname_prefix,
        id=__ret__.id,
        input=__ret__.input,
        last_modified=__ret__.last_modified,
        location=__ret__.location,
        name=__ret__.name,
        preview=__ret__.preview,
        provisioning_state=__ret__.provisioning_state,
        resource_state=__ret__.resource_state,
        stream_options=__ret__.stream_options,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        transcriptions=__ret__.transcriptions,
        type=__ret__.type,
        use_static_hostname=__ret__.use_static_hostname)
