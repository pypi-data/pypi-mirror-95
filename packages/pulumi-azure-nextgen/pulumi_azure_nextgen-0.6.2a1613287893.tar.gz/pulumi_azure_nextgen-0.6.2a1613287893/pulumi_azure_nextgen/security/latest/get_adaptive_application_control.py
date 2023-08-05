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
    'GetAdaptiveApplicationControlResult',
    'AwaitableGetAdaptiveApplicationControlResult',
    'get_adaptive_application_control',
]

@pulumi.output_type
class GetAdaptiveApplicationControlResult:
    def __init__(__self__, configuration_status=None, enforcement_mode=None, id=None, issues=None, location=None, name=None, path_recommendations=None, protection_mode=None, recommendation_status=None, source_system=None, type=None, vm_recommendations=None):
        if configuration_status and not isinstance(configuration_status, str):
            raise TypeError("Expected argument 'configuration_status' to be a str")
        pulumi.set(__self__, "configuration_status", configuration_status)
        if enforcement_mode and not isinstance(enforcement_mode, str):
            raise TypeError("Expected argument 'enforcement_mode' to be a str")
        pulumi.set(__self__, "enforcement_mode", enforcement_mode)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if issues and not isinstance(issues, list):
            raise TypeError("Expected argument 'issues' to be a list")
        pulumi.set(__self__, "issues", issues)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if path_recommendations and not isinstance(path_recommendations, list):
            raise TypeError("Expected argument 'path_recommendations' to be a list")
        pulumi.set(__self__, "path_recommendations", path_recommendations)
        if protection_mode and not isinstance(protection_mode, dict):
            raise TypeError("Expected argument 'protection_mode' to be a dict")
        pulumi.set(__self__, "protection_mode", protection_mode)
        if recommendation_status and not isinstance(recommendation_status, str):
            raise TypeError("Expected argument 'recommendation_status' to be a str")
        pulumi.set(__self__, "recommendation_status", recommendation_status)
        if source_system and not isinstance(source_system, str):
            raise TypeError("Expected argument 'source_system' to be a str")
        pulumi.set(__self__, "source_system", source_system)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vm_recommendations and not isinstance(vm_recommendations, list):
            raise TypeError("Expected argument 'vm_recommendations' to be a list")
        pulumi.set(__self__, "vm_recommendations", vm_recommendations)

    @property
    @pulumi.getter(name="configurationStatus")
    def configuration_status(self) -> str:
        """
        The configuration status of the machines group or machine or rule
        """
        return pulumi.get(self, "configuration_status")

    @property
    @pulumi.getter(name="enforcementMode")
    def enforcement_mode(self) -> Optional[str]:
        """
        The application control policy enforcement/protection mode of the machine group
        """
        return pulumi.get(self, "enforcement_mode")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def issues(self) -> Sequence['outputs.AdaptiveApplicationControlIssueSummaryResponse']:
        return pulumi.get(self, "issues")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Location where the resource is stored
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pathRecommendations")
    def path_recommendations(self) -> Optional[Sequence['outputs.PathRecommendationResponse']]:
        return pulumi.get(self, "path_recommendations")

    @property
    @pulumi.getter(name="protectionMode")
    def protection_mode(self) -> Optional['outputs.ProtectionModeResponse']:
        """
        The protection mode of the collection/file types. Exe/Msi/Script are used for Windows, Executable is used for Linux.
        """
        return pulumi.get(self, "protection_mode")

    @property
    @pulumi.getter(name="recommendationStatus")
    def recommendation_status(self) -> str:
        """
        The initial recommendation status of the machine group or machine
        """
        return pulumi.get(self, "recommendation_status")

    @property
    @pulumi.getter(name="sourceSystem")
    def source_system(self) -> str:
        """
        The source type of the machine group
        """
        return pulumi.get(self, "source_system")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vmRecommendations")
    def vm_recommendations(self) -> Optional[Sequence['outputs.VmRecommendationResponse']]:
        return pulumi.get(self, "vm_recommendations")


class AwaitableGetAdaptiveApplicationControlResult(GetAdaptiveApplicationControlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAdaptiveApplicationControlResult(
            configuration_status=self.configuration_status,
            enforcement_mode=self.enforcement_mode,
            id=self.id,
            issues=self.issues,
            location=self.location,
            name=self.name,
            path_recommendations=self.path_recommendations,
            protection_mode=self.protection_mode,
            recommendation_status=self.recommendation_status,
            source_system=self.source_system,
            type=self.type,
            vm_recommendations=self.vm_recommendations)


def get_adaptive_application_control(asc_location: Optional[str] = None,
                                     group_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAdaptiveApplicationControlResult:
    """
    Use this data source to access information about an existing resource.

    :param str asc_location: The location where ASC stores the data of the subscription. can be retrieved from Get locations
    :param str group_name: Name of an application control machine group
    """
    __args__ = dict()
    __args__['ascLocation'] = asc_location
    __args__['groupName'] = group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:security/latest:getAdaptiveApplicationControl', __args__, opts=opts, typ=GetAdaptiveApplicationControlResult).value

    return AwaitableGetAdaptiveApplicationControlResult(
        configuration_status=__ret__.configuration_status,
        enforcement_mode=__ret__.enforcement_mode,
        id=__ret__.id,
        issues=__ret__.issues,
        location=__ret__.location,
        name=__ret__.name,
        path_recommendations=__ret__.path_recommendations,
        protection_mode=__ret__.protection_mode,
        recommendation_status=__ret__.recommendation_status,
        source_system=__ret__.source_system,
        type=__ret__.type,
        vm_recommendations=__ret__.vm_recommendations)
