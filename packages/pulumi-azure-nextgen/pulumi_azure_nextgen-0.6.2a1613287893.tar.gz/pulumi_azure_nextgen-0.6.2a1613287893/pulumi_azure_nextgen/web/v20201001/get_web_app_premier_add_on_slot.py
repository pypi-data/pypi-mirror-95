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
    'GetWebAppPremierAddOnSlotResult',
    'AwaitableGetWebAppPremierAddOnSlotResult',
    'get_web_app_premier_add_on_slot',
]

@pulumi.output_type
class GetWebAppPremierAddOnSlotResult:
    """
    Premier add-on.
    """
    def __init__(__self__, id=None, kind=None, location=None, marketplace_offer=None, marketplace_publisher=None, name=None, product=None, sku=None, system_data=None, tags=None, type=None, vendor=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if marketplace_offer and not isinstance(marketplace_offer, str):
            raise TypeError("Expected argument 'marketplace_offer' to be a str")
        pulumi.set(__self__, "marketplace_offer", marketplace_offer)
        if marketplace_publisher and not isinstance(marketplace_publisher, str):
            raise TypeError("Expected argument 'marketplace_publisher' to be a str")
        pulumi.set(__self__, "marketplace_publisher", marketplace_publisher)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if product and not isinstance(product, str):
            raise TypeError("Expected argument 'product' to be a str")
        pulumi.set(__self__, "product", product)
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        pulumi.set(__self__, "sku", sku)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vendor and not isinstance(vendor, str):
            raise TypeError("Expected argument 'vendor' to be a str")
        pulumi.set(__self__, "vendor", vendor)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="marketplaceOffer")
    def marketplace_offer(self) -> Optional[str]:
        """
        Premier add on Marketplace offer.
        """
        return pulumi.get(self, "marketplace_offer")

    @property
    @pulumi.getter(name="marketplacePublisher")
    def marketplace_publisher(self) -> Optional[str]:
        """
        Premier add on Marketplace publisher.
        """
        return pulumi.get(self, "marketplace_publisher")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def product(self) -> Optional[str]:
        """
        Premier add on Product.
        """
        return pulumi.get(self, "product")

    @property
    @pulumi.getter
    def sku(self) -> Optional[str]:
        """
        Premier add on SKU.
        """
        return pulumi.get(self, "sku")

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
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def vendor(self) -> Optional[str]:
        """
        Premier add on Vendor.
        """
        return pulumi.get(self, "vendor")


class AwaitableGetWebAppPremierAddOnSlotResult(GetWebAppPremierAddOnSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWebAppPremierAddOnSlotResult(
            id=self.id,
            kind=self.kind,
            location=self.location,
            marketplace_offer=self.marketplace_offer,
            marketplace_publisher=self.marketplace_publisher,
            name=self.name,
            product=self.product,
            sku=self.sku,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            vendor=self.vendor)


def get_web_app_premier_add_on_slot(name: Optional[str] = None,
                                    premier_add_on_name: Optional[str] = None,
                                    resource_group_name: Optional[str] = None,
                                    slot: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWebAppPremierAddOnSlotResult:
    """
    Use this data source to access information about an existing resource.

    :param str name: Name of the app.
    :param str premier_add_on_name: Add-on name.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get the named add-on for the production slot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['premierAddOnName'] = premier_add_on_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:web/v20201001:getWebAppPremierAddOnSlot', __args__, opts=opts, typ=GetWebAppPremierAddOnSlotResult).value

    return AwaitableGetWebAppPremierAddOnSlotResult(
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        marketplace_offer=__ret__.marketplace_offer,
        marketplace_publisher=__ret__.marketplace_publisher,
        name=__ret__.name,
        product=__ret__.product,
        sku=__ret__.sku,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        vendor=__ret__.vendor)
