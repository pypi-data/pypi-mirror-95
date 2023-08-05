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
    'GetAssetEncryptionKeyResult',
    'AwaitableGetAssetEncryptionKeyResult',
    'get_asset_encryption_key',
]

@pulumi.output_type
class GetAssetEncryptionKeyResult:
    """
    Data needed to decrypt asset files encrypted with legacy storage encryption.
    """
    def __init__(__self__, asset_file_encryption_metadata=None, key=None):
        if asset_file_encryption_metadata and not isinstance(asset_file_encryption_metadata, list):
            raise TypeError("Expected argument 'asset_file_encryption_metadata' to be a list")
        pulumi.set(__self__, "asset_file_encryption_metadata", asset_file_encryption_metadata)
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, "key", key)

    @property
    @pulumi.getter(name="assetFileEncryptionMetadata")
    def asset_file_encryption_metadata(self) -> Optional[Sequence['outputs.AssetFileEncryptionMetadataResponseResult']]:
        """
        Asset File encryption metadata.
        """
        return pulumi.get(self, "asset_file_encryption_metadata")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The Asset File storage encryption key.
        """
        return pulumi.get(self, "key")


class AwaitableGetAssetEncryptionKeyResult(GetAssetEncryptionKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAssetEncryptionKeyResult(
            asset_file_encryption_metadata=self.asset_file_encryption_metadata,
            key=self.key)


def get_asset_encryption_key(account_name: Optional[str] = None,
                             asset_name: Optional[str] = None,
                             resource_group_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAssetEncryptionKeyResult:
    """
    Use this data source to access information about an existing resource.

    :param str account_name: The Media Services account name.
    :param str asset_name: The Asset name.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['assetName'] = asset_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:media/v20200501:getAssetEncryptionKey', __args__, opts=opts, typ=GetAssetEncryptionKeyResult).value

    return AwaitableGetAssetEncryptionKeyResult(
        asset_file_encryption_metadata=__ret__.asset_file_encryption_metadata,
        key=__ret__.key)
