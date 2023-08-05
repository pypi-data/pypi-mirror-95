# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'ListSaasResourceAccessTokenResult',
    'AwaitableListSaasResourceAccessTokenResult',
    'list_saas_resource_access_token',
]

@pulumi.output_type
class ListSaasResourceAccessTokenResult:
    """
    the ISV access token result response.
    """
    def __init__(__self__, publisher_offer_base_uri=None, token=None):
        if publisher_offer_base_uri and not isinstance(publisher_offer_base_uri, str):
            raise TypeError("Expected argument 'publisher_offer_base_uri' to be a str")
        pulumi.set(__self__, "publisher_offer_base_uri", publisher_offer_base_uri)
        if token and not isinstance(token, str):
            raise TypeError("Expected argument 'token' to be a str")
        pulumi.set(__self__, "token", token)

    @property
    @pulumi.getter(name="publisherOfferBaseUri")
    def publisher_offer_base_uri(self) -> Optional[str]:
        """
        The Publisher Offer Base Uri
        """
        return pulumi.get(self, "publisher_offer_base_uri")

    @property
    @pulumi.getter
    def token(self) -> Optional[str]:
        """
        The generated token
        """
        return pulumi.get(self, "token")


class AwaitableListSaasResourceAccessTokenResult(ListSaasResourceAccessTokenResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListSaasResourceAccessTokenResult(
            publisher_offer_base_uri=self.publisher_offer_base_uri,
            token=self.token)


def list_saas_resource_access_token(resource_id: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListSaasResourceAccessTokenResult:
    """
    Use this data source to access information about an existing resource.

    :param str resource_id: The Saas resource ID. This is a GUID-formatted string (e.g. 00000000-0000-0000-0000-000000000000)
    """
    __args__ = dict()
    __args__['resourceId'] = resource_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:saas:listSaasResourceAccessToken', __args__, opts=opts, typ=ListSaasResourceAccessTokenResult).value

    return AwaitableListSaasResourceAccessTokenResult(
        publisher_offer_base_uri=__ret__.publisher_offer_base_uri,
        token=__ret__.token)
