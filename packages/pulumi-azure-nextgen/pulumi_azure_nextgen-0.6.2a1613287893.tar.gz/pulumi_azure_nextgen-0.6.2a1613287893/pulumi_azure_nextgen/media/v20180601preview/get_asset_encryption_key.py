# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetAssetEncryptionKeyResult',
    'AwaitableGetAssetEncryptionKeyResult',
    'get_asset_encryption_key',
]

@pulumi.output_type
class GetAssetEncryptionKeyResult:
    """
    The Asset Storage encryption key.
    """
    def __init__(__self__, storage_encryption_key=None):
        if storage_encryption_key and not isinstance(storage_encryption_key, str):
            raise TypeError("Expected argument 'storage_encryption_key' to be a str")
        pulumi.set(__self__, "storage_encryption_key", storage_encryption_key)

    @property
    @pulumi.getter(name="storageEncryptionKey")
    def storage_encryption_key(self) -> Optional[str]:
        """
        The Asset storage encryption key.
        """
        return pulumi.get(self, "storage_encryption_key")


class AwaitableGetAssetEncryptionKeyResult(GetAssetEncryptionKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAssetEncryptionKeyResult(
            storage_encryption_key=self.storage_encryption_key)


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
    __ret__ = pulumi.runtime.invoke('azure-nextgen:media/v20180601preview:getAssetEncryptionKey', __args__, opts=opts, typ=GetAssetEncryptionKeyResult).value

    return AwaitableGetAssetEncryptionKeyResult(
        storage_encryption_key=__ret__.storage_encryption_key)
