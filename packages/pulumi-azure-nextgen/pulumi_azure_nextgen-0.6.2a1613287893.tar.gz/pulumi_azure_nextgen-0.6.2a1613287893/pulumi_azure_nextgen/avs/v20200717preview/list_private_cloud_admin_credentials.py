# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'ListPrivateCloudAdminCredentialsResult',
    'AwaitableListPrivateCloudAdminCredentialsResult',
    'list_private_cloud_admin_credentials',
]

@pulumi.output_type
class ListPrivateCloudAdminCredentialsResult:
    """
    Administrative credentials for accessing vCenter and NSX-T
    """
    def __init__(__self__, nsxt_password=None, nsxt_username=None, vcenter_password=None, vcenter_username=None):
        if nsxt_password and not isinstance(nsxt_password, str):
            raise TypeError("Expected argument 'nsxt_password' to be a str")
        pulumi.set(__self__, "nsxt_password", nsxt_password)
        if nsxt_username and not isinstance(nsxt_username, str):
            raise TypeError("Expected argument 'nsxt_username' to be a str")
        pulumi.set(__self__, "nsxt_username", nsxt_username)
        if vcenter_password and not isinstance(vcenter_password, str):
            raise TypeError("Expected argument 'vcenter_password' to be a str")
        pulumi.set(__self__, "vcenter_password", vcenter_password)
        if vcenter_username and not isinstance(vcenter_username, str):
            raise TypeError("Expected argument 'vcenter_username' to be a str")
        pulumi.set(__self__, "vcenter_username", vcenter_username)

    @property
    @pulumi.getter(name="nsxtPassword")
    def nsxt_password(self) -> str:
        """
        NSX-T Manager password
        """
        return pulumi.get(self, "nsxt_password")

    @property
    @pulumi.getter(name="nsxtUsername")
    def nsxt_username(self) -> str:
        """
        NSX-T Manager username
        """
        return pulumi.get(self, "nsxt_username")

    @property
    @pulumi.getter(name="vcenterPassword")
    def vcenter_password(self) -> str:
        """
        vCenter admin password
        """
        return pulumi.get(self, "vcenter_password")

    @property
    @pulumi.getter(name="vcenterUsername")
    def vcenter_username(self) -> str:
        """
        vCenter admin username
        """
        return pulumi.get(self, "vcenter_username")


class AwaitableListPrivateCloudAdminCredentialsResult(ListPrivateCloudAdminCredentialsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListPrivateCloudAdminCredentialsResult(
            nsxt_password=self.nsxt_password,
            nsxt_username=self.nsxt_username,
            vcenter_password=self.vcenter_password,
            vcenter_username=self.vcenter_username)


def list_private_cloud_admin_credentials(private_cloud_name: Optional[str] = None,
                                         resource_group_name: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListPrivateCloudAdminCredentialsResult:
    """
    Use this data source to access information about an existing resource.

    :param str private_cloud_name: Name of the private cloud
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['privateCloudName'] = private_cloud_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:avs/v20200717preview:listPrivateCloudAdminCredentials', __args__, opts=opts, typ=ListPrivateCloudAdminCredentialsResult).value

    return AwaitableListPrivateCloudAdminCredentialsResult(
        nsxt_password=__ret__.nsxt_password,
        nsxt_username=__ret__.nsxt_username,
        vcenter_password=__ret__.vcenter_password,
        vcenter_username=__ret__.vcenter_username)
