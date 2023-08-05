# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'GetGuestDiagnosticsSettingsAssociationResult',
    'AwaitableGetGuestDiagnosticsSettingsAssociationResult',
    'get_guest_diagnostics_settings_association',
]

@pulumi.output_type
class GetGuestDiagnosticsSettingsAssociationResult:
    """
    Virtual machine guest diagnostic settings resource.
    """
    def __init__(__self__, guest_diagnostic_settings_name=None, id=None, location=None, name=None, tags=None, type=None):
        if guest_diagnostic_settings_name and not isinstance(guest_diagnostic_settings_name, str):
            raise TypeError("Expected argument 'guest_diagnostic_settings_name' to be a str")
        pulumi.set(__self__, "guest_diagnostic_settings_name", guest_diagnostic_settings_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="guestDiagnosticSettingsName")
    def guest_diagnostic_settings_name(self) -> str:
        """
        The guest diagnostic settings name.
        """
        return pulumi.get(self, "guest_diagnostic_settings_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetGuestDiagnosticsSettingsAssociationResult(GetGuestDiagnosticsSettingsAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGuestDiagnosticsSettingsAssociationResult(
            guest_diagnostic_settings_name=self.guest_diagnostic_settings_name,
            id=self.id,
            location=self.location,
            name=self.name,
            tags=self.tags,
            type=self.type)


def get_guest_diagnostics_settings_association(association_name: Optional[str] = None,
                                               resource_uri: Optional[str] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGuestDiagnosticsSettingsAssociationResult:
    """
    Use this data source to access information about an existing resource.

    :param str association_name: The name of the diagnostic settings association.
    :param str resource_uri: The fully qualified ID of the resource, including the resource name and resource type.
    """
    __args__ = dict()
    __args__['associationName'] = association_name
    __args__['resourceUri'] = resource_uri
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:insights:getGuestDiagnosticsSettingsAssociation', __args__, opts=opts, typ=GetGuestDiagnosticsSettingsAssociationResult).value

    return AwaitableGetGuestDiagnosticsSettingsAssociationResult(
        guest_diagnostic_settings_name=__ret__.guest_diagnostic_settings_name,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        tags=__ret__.tags,
        type=__ret__.type)
