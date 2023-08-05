# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._enums import *

__all__ = [
    'SaasPropertiesResponseTerm',
    'SaasResourceResponseProperties',
]

@pulumi.output_type
class SaasPropertiesResponseTerm(dict):
    """
    The current Term object.
    """
    def __init__(__self__, *,
                 end_date: Optional[str] = None,
                 start_date: Optional[str] = None,
                 term_unit: Optional[str] = None):
        """
        The current Term object.
        :param str end_date: The end date of the current term
        :param str start_date: The start date of the current term
        :param str term_unit: The unit indicating Monthly / Yearly
        """
        if end_date is not None:
            pulumi.set(__self__, "end_date", end_date)
        if start_date is not None:
            pulumi.set(__self__, "start_date", start_date)
        if term_unit is not None:
            pulumi.set(__self__, "term_unit", term_unit)

    @property
    @pulumi.getter(name="endDate")
    def end_date(self) -> Optional[str]:
        """
        The end date of the current term
        """
        return pulumi.get(self, "end_date")

    @property
    @pulumi.getter(name="startDate")
    def start_date(self) -> Optional[str]:
        """
        The start date of the current term
        """
        return pulumi.get(self, "start_date")

    @property
    @pulumi.getter(name="termUnit")
    def term_unit(self) -> Optional[str]:
        """
        The unit indicating Monthly / Yearly
        """
        return pulumi.get(self, "term_unit")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SaasResourceResponseProperties(dict):
    """
    saas properties
    """
    def __init__(__self__, *,
                 created: str,
                 auto_renew: Optional[bool] = None,
                 is_free_trial: Optional[bool] = None,
                 last_modified: Optional[str] = None,
                 offer_id: Optional[str] = None,
                 payment_channel_metadata: Optional[Mapping[str, str]] = None,
                 payment_channel_type: Optional[str] = None,
                 publisher_id: Optional[str] = None,
                 publisher_test_environment: Optional[str] = None,
                 quantity: Optional[float] = None,
                 saas_resource_name: Optional[str] = None,
                 saas_session_id: Optional[str] = None,
                 saas_subscription_id: Optional[str] = None,
                 sku_id: Optional[str] = None,
                 status: Optional[str] = None,
                 term: Optional['outputs.SaasPropertiesResponseTerm'] = None,
                 term_id: Optional[str] = None):
        """
        saas properties
        :param str created: The created date of this resource.
        :param bool auto_renew: Whether the SaaS subscription will auto renew upon term end.
        :param bool is_free_trial: Whether the current term is a Free Trial term
        :param str last_modified: The last modifier date if this resource.
        :param str offer_id: The offer id.
        :param Mapping[str, str] payment_channel_metadata: The metadata about the SaaS subscription such as the AzureSubscriptionId and ResourceUri.
        :param str payment_channel_type: The Payment channel for the SaasSubscription.
        :param str publisher_id: The publisher id.
        :param str publisher_test_environment: The environment in the publisher side for this resource.
        :param float quantity: The seat count.
        :param str saas_resource_name: The SaaS resource name.
        :param str saas_session_id: The saas session id used for dev service migration request.
        :param str saas_subscription_id: The saas subscription id used for tenant to subscription level migration request.
        :param str sku_id: The plan id.
        :param str status: The SaaS Subscription Status.
        :param 'SaasPropertiesResponseTermArgs' term: The current Term object.
        :param str term_id: The current Term id.
        """
        pulumi.set(__self__, "created", created)
        if auto_renew is not None:
            pulumi.set(__self__, "auto_renew", auto_renew)
        if is_free_trial is not None:
            pulumi.set(__self__, "is_free_trial", is_free_trial)
        if last_modified is not None:
            pulumi.set(__self__, "last_modified", last_modified)
        if offer_id is not None:
            pulumi.set(__self__, "offer_id", offer_id)
        if payment_channel_metadata is not None:
            pulumi.set(__self__, "payment_channel_metadata", payment_channel_metadata)
        if payment_channel_type is not None:
            pulumi.set(__self__, "payment_channel_type", payment_channel_type)
        if publisher_id is not None:
            pulumi.set(__self__, "publisher_id", publisher_id)
        if publisher_test_environment is not None:
            pulumi.set(__self__, "publisher_test_environment", publisher_test_environment)
        if quantity is not None:
            pulumi.set(__self__, "quantity", quantity)
        if saas_resource_name is not None:
            pulumi.set(__self__, "saas_resource_name", saas_resource_name)
        if saas_session_id is not None:
            pulumi.set(__self__, "saas_session_id", saas_session_id)
        if saas_subscription_id is not None:
            pulumi.set(__self__, "saas_subscription_id", saas_subscription_id)
        if sku_id is not None:
            pulumi.set(__self__, "sku_id", sku_id)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if term is not None:
            pulumi.set(__self__, "term", term)
        if term_id is not None:
            pulumi.set(__self__, "term_id", term_id)

    @property
    @pulumi.getter
    def created(self) -> str:
        """
        The created date of this resource.
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter(name="autoRenew")
    def auto_renew(self) -> Optional[bool]:
        """
        Whether the SaaS subscription will auto renew upon term end.
        """
        return pulumi.get(self, "auto_renew")

    @property
    @pulumi.getter(name="isFreeTrial")
    def is_free_trial(self) -> Optional[bool]:
        """
        Whether the current term is a Free Trial term
        """
        return pulumi.get(self, "is_free_trial")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> Optional[str]:
        """
        The last modifier date if this resource.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter(name="offerId")
    def offer_id(self) -> Optional[str]:
        """
        The offer id.
        """
        return pulumi.get(self, "offer_id")

    @property
    @pulumi.getter(name="paymentChannelMetadata")
    def payment_channel_metadata(self) -> Optional[Mapping[str, str]]:
        """
        The metadata about the SaaS subscription such as the AzureSubscriptionId and ResourceUri.
        """
        return pulumi.get(self, "payment_channel_metadata")

    @property
    @pulumi.getter(name="paymentChannelType")
    def payment_channel_type(self) -> Optional[str]:
        """
        The Payment channel for the SaasSubscription.
        """
        return pulumi.get(self, "payment_channel_type")

    @property
    @pulumi.getter(name="publisherId")
    def publisher_id(self) -> Optional[str]:
        """
        The publisher id.
        """
        return pulumi.get(self, "publisher_id")

    @property
    @pulumi.getter(name="publisherTestEnvironment")
    def publisher_test_environment(self) -> Optional[str]:
        """
        The environment in the publisher side for this resource.
        """
        return pulumi.get(self, "publisher_test_environment")

    @property
    @pulumi.getter
    def quantity(self) -> Optional[float]:
        """
        The seat count.
        """
        return pulumi.get(self, "quantity")

    @property
    @pulumi.getter(name="saasResourceName")
    def saas_resource_name(self) -> Optional[str]:
        """
        The SaaS resource name.
        """
        return pulumi.get(self, "saas_resource_name")

    @property
    @pulumi.getter(name="saasSessionId")
    def saas_session_id(self) -> Optional[str]:
        """
        The saas session id used for dev service migration request.
        """
        return pulumi.get(self, "saas_session_id")

    @property
    @pulumi.getter(name="saasSubscriptionId")
    def saas_subscription_id(self) -> Optional[str]:
        """
        The saas subscription id used for tenant to subscription level migration request.
        """
        return pulumi.get(self, "saas_subscription_id")

    @property
    @pulumi.getter(name="skuId")
    def sku_id(self) -> Optional[str]:
        """
        The plan id.
        """
        return pulumi.get(self, "sku_id")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The SaaS Subscription Status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def term(self) -> Optional['outputs.SaasPropertiesResponseTerm']:
        """
        The current Term object.
        """
        return pulumi.get(self, "term")

    @property
    @pulumi.getter(name="termId")
    def term_id(self) -> Optional[str]:
        """
        The current Term id.
        """
        return pulumi.get(self, "term_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


