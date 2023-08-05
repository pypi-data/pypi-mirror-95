# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._enums import *

__all__ = [
    'AzureADMetricsPropertiesFormatResponse',
    'LogSettingsResponse',
    'RetentionPolicyResponse',
]

@pulumi.output_type
class AzureADMetricsPropertiesFormatResponse(dict):
    def __init__(__self__, *,
                 provisioning_state: str):
        """
        :param str provisioning_state: The provisioning state of the resource.
        """
        pulumi.set(__self__, "provisioning_state", provisioning_state)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class LogSettingsResponse(dict):
    """
    Part of MultiTenantDiagnosticSettings. Specifies the settings for a particular log.
    """
    def __init__(__self__, *,
                 enabled: bool,
                 category: Optional[str] = None,
                 retention_policy: Optional['outputs.RetentionPolicyResponse'] = None):
        """
        Part of MultiTenantDiagnosticSettings. Specifies the settings for a particular log.
        :param bool enabled: A value indicating whether this log is enabled.
        :param str category: Name of a Diagnostic Log category for a resource type this setting is applied to. To obtain the list of Diagnostic Log categories for a resource, first perform a GET diagnostic settings operation.
        :param 'RetentionPolicyResponseArgs' retention_policy: The retention policy for this log.
        """
        pulumi.set(__self__, "enabled", enabled)
        if category is not None:
            pulumi.set(__self__, "category", category)
        if retention_policy is not None:
            pulumi.set(__self__, "retention_policy", retention_policy)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        A value indicating whether this log is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def category(self) -> Optional[str]:
        """
        Name of a Diagnostic Log category for a resource type this setting is applied to. To obtain the list of Diagnostic Log categories for a resource, first perform a GET diagnostic settings operation.
        """
        return pulumi.get(self, "category")

    @property
    @pulumi.getter(name="retentionPolicy")
    def retention_policy(self) -> Optional['outputs.RetentionPolicyResponse']:
        """
        The retention policy for this log.
        """
        return pulumi.get(self, "retention_policy")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RetentionPolicyResponse(dict):
    """
    Specifies the retention policy for the log.
    """
    def __init__(__self__, *,
                 days: int,
                 enabled: bool):
        """
        Specifies the retention policy for the log.
        :param int days: The number of days for the retention in days. A value of 0 will retain the events indefinitely.
        :param bool enabled: A value indicating whether the retention policy is enabled.
        """
        pulumi.set(__self__, "days", days)
        pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def days(self) -> int:
        """
        The number of days for the retention in days. A value of 0 will retain the events indefinitely.
        """
        return pulumi.get(self, "days")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        A value indicating whether the retention policy is enabled.
        """
        return pulumi.get(self, "enabled")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


