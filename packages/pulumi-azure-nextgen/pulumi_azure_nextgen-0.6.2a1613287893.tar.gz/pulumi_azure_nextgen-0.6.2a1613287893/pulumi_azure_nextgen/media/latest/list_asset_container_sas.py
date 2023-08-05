# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = [
    'ListAssetContainerSasResult',
    'AwaitableListAssetContainerSasResult',
    'list_asset_container_sas',
]

@pulumi.output_type
class ListAssetContainerSasResult:
    """
    The Asset Storage container SAS URLs.
    """
    def __init__(__self__, asset_container_sas_urls=None):
        if asset_container_sas_urls and not isinstance(asset_container_sas_urls, list):
            raise TypeError("Expected argument 'asset_container_sas_urls' to be a list")
        pulumi.set(__self__, "asset_container_sas_urls", asset_container_sas_urls)

    @property
    @pulumi.getter(name="assetContainerSasUrls")
    def asset_container_sas_urls(self) -> Optional[Sequence[str]]:
        """
        The list of Asset container SAS URLs.
        """
        return pulumi.get(self, "asset_container_sas_urls")


class AwaitableListAssetContainerSasResult(ListAssetContainerSasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListAssetContainerSasResult(
            asset_container_sas_urls=self.asset_container_sas_urls)


def list_asset_container_sas(account_name: Optional[str] = None,
                             asset_name: Optional[str] = None,
                             expiry_time: Optional[str] = None,
                             permissions: Optional[Union[str, 'AssetContainerPermission']] = None,
                             resource_group_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListAssetContainerSasResult:
    """
    Use this data source to access information about an existing resource.

    :param str account_name: The Media Services account name.
    :param str asset_name: The Asset name.
    :param str expiry_time: The SAS URL expiration time.  This must be less than 24 hours from the current time.
    :param Union[str, 'AssetContainerPermission'] permissions: The permissions to set on the SAS URL.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['assetName'] = asset_name
    __args__['expiryTime'] = expiry_time
    __args__['permissions'] = permissions
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:media/latest:listAssetContainerSas', __args__, opts=opts, typ=ListAssetContainerSasResult).value

    return AwaitableListAssetContainerSasResult(
        asset_container_sas_urls=__ret__.asset_container_sas_urls)
