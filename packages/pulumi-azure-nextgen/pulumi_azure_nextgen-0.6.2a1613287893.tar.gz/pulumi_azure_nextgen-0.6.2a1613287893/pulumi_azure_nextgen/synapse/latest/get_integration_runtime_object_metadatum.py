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
    'GetIntegrationRuntimeObjectMetadatumResult',
    'AwaitableGetIntegrationRuntimeObjectMetadatumResult',
    'get_integration_runtime_object_metadatum',
]

@pulumi.output_type
class GetIntegrationRuntimeObjectMetadatumResult:
    """
    A list of SSIS object metadata.
    """
    def __init__(__self__, next_link=None, value=None):
        if next_link and not isinstance(next_link, str):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, "next_link", next_link)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="nextLink")
    def next_link(self) -> Optional[str]:
        """
        The link to the next page of results, if any remaining results exist.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence[Any]]:
        """
        List of SSIS object metadata.
        """
        return pulumi.get(self, "value")


class AwaitableGetIntegrationRuntimeObjectMetadatumResult(GetIntegrationRuntimeObjectMetadatumResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIntegrationRuntimeObjectMetadatumResult(
            next_link=self.next_link,
            value=self.value)


def get_integration_runtime_object_metadatum(integration_runtime_name: Optional[str] = None,
                                             metadata_path: Optional[str] = None,
                                             resource_group_name: Optional[str] = None,
                                             workspace_name: Optional[str] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIntegrationRuntimeObjectMetadatumResult:
    """
    Use this data source to access information about an existing resource.

    :param str integration_runtime_name: Integration runtime name
    :param str metadata_path: Metadata path.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['integrationRuntimeName'] = integration_runtime_name
    __args__['metadataPath'] = metadata_path
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:synapse/latest:getIntegrationRuntimeObjectMetadatum', __args__, opts=opts, typ=GetIntegrationRuntimeObjectMetadatumResult).value

    return AwaitableGetIntegrationRuntimeObjectMetadatumResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
