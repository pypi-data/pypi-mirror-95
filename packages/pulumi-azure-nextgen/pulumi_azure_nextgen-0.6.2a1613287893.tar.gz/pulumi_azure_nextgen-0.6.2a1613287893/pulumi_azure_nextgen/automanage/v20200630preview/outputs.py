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
    'AccountIdentityResponse',
    'ConfigurationProfileAssignmentComplianceResponse',
    'ConfigurationProfileAssignmentPropertiesResponse',
    'ConfigurationProfilePreferenceAntiMalwareResponse',
    'ConfigurationProfilePreferencePropertiesResponse',
    'ConfigurationProfilePreferenceVmBackupResponse',
]

@pulumi.output_type
class AccountIdentityResponse(dict):
    """
    Identity for the Automanage account.
    """
    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: Optional[str] = None):
        """
        Identity for the Automanage account.
        :param str principal_id: The principal id of Automanage account identity.
        :param str tenant_id: The tenant id associated with the Automanage account.
        :param str type: The type of identity used for the Automanage account. Currently, the only supported type is 'SystemAssigned', which implicitly creates an identity.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal id of Automanage account identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant id associated with the Automanage account.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of identity used for the Automanage account. Currently, the only supported type is 'SystemAssigned', which implicitly creates an identity.
        """
        return pulumi.get(self, "type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ConfigurationProfileAssignmentComplianceResponse(dict):
    """
    The compliance status for the configuration profile assignment.
    """
    def __init__(__self__, *,
                 update_status: str):
        """
        The compliance status for the configuration profile assignment.
        :param str update_status: The state of compliance, which only appears in the response.
        """
        pulumi.set(__self__, "update_status", update_status)

    @property
    @pulumi.getter(name="updateStatus")
    def update_status(self) -> str:
        """
        The state of compliance, which only appears in the response.
        """
        return pulumi.get(self, "update_status")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ConfigurationProfileAssignmentPropertiesResponse(dict):
    """
    Automanage configuration profile assignment properties.
    """
    def __init__(__self__, *,
                 provisioning_state: str,
                 account_id: Optional[str] = None,
                 compliance: Optional['outputs.ConfigurationProfileAssignmentComplianceResponse'] = None,
                 configuration_profile: Optional[str] = None,
                 configuration_profile_preference_id: Optional[str] = None,
                 target_id: Optional[str] = None):
        """
        Automanage configuration profile assignment properties.
        :param str provisioning_state: The state of onboarding, which only appears in the response.
        :param str account_id: The Automanage account ARM Resource URI
        :param 'ConfigurationProfileAssignmentComplianceResponseArgs' compliance: The configuration setting for the configuration profile.
        :param str configuration_profile: A value indicating configuration profile.
        :param str configuration_profile_preference_id: The configuration profile custom preferences ARM resource URI
        :param str target_id: The target VM resource URI
        """
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if compliance is not None:
            pulumi.set(__self__, "compliance", compliance)
        if configuration_profile is not None:
            pulumi.set(__self__, "configuration_profile", configuration_profile)
        if configuration_profile_preference_id is not None:
            pulumi.set(__self__, "configuration_profile_preference_id", configuration_profile_preference_id)
        if target_id is not None:
            pulumi.set(__self__, "target_id", target_id)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The state of onboarding, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[str]:
        """
        The Automanage account ARM Resource URI
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def compliance(self) -> Optional['outputs.ConfigurationProfileAssignmentComplianceResponse']:
        """
        The configuration setting for the configuration profile.
        """
        return pulumi.get(self, "compliance")

    @property
    @pulumi.getter(name="configurationProfile")
    def configuration_profile(self) -> Optional[str]:
        """
        A value indicating configuration profile.
        """
        return pulumi.get(self, "configuration_profile")

    @property
    @pulumi.getter(name="configurationProfilePreferenceId")
    def configuration_profile_preference_id(self) -> Optional[str]:
        """
        The configuration profile custom preferences ARM resource URI
        """
        return pulumi.get(self, "configuration_profile_preference_id")

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> Optional[str]:
        """
        The target VM resource URI
        """
        return pulumi.get(self, "target_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ConfigurationProfilePreferenceAntiMalwareResponse(dict):
    """
    Automanage configuration profile Antimalware preferences.
    """
    def __init__(__self__, *,
                 enable_real_time_protection: Optional[str] = None,
                 exclusions: Optional[Any] = None,
                 run_scheduled_scan: Optional[str] = None,
                 scan_day: Optional[str] = None,
                 scan_time_in_minutes: Optional[str] = None,
                 scan_type: Optional[str] = None):
        """
        Automanage configuration profile Antimalware preferences.
        :param str enable_real_time_protection: Enables or disables Real Time Protection
        :param Any exclusions: Extensions, Paths and Processes that must be excluded from scan
        :param str run_scheduled_scan: Enables or disables a periodic scan for antimalware
        :param str scan_day: Schedule scan settings day
        :param str scan_time_in_minutes: Schedule scan settings time
        :param str scan_type: Type of scheduled scan
        """
        if enable_real_time_protection is not None:
            pulumi.set(__self__, "enable_real_time_protection", enable_real_time_protection)
        if exclusions is not None:
            pulumi.set(__self__, "exclusions", exclusions)
        if run_scheduled_scan is not None:
            pulumi.set(__self__, "run_scheduled_scan", run_scheduled_scan)
        if scan_day is not None:
            pulumi.set(__self__, "scan_day", scan_day)
        if scan_time_in_minutes is not None:
            pulumi.set(__self__, "scan_time_in_minutes", scan_time_in_minutes)
        if scan_type is not None:
            pulumi.set(__self__, "scan_type", scan_type)

    @property
    @pulumi.getter(name="enableRealTimeProtection")
    def enable_real_time_protection(self) -> Optional[str]:
        """
        Enables or disables Real Time Protection
        """
        return pulumi.get(self, "enable_real_time_protection")

    @property
    @pulumi.getter
    def exclusions(self) -> Optional[Any]:
        """
        Extensions, Paths and Processes that must be excluded from scan
        """
        return pulumi.get(self, "exclusions")

    @property
    @pulumi.getter(name="runScheduledScan")
    def run_scheduled_scan(self) -> Optional[str]:
        """
        Enables or disables a periodic scan for antimalware
        """
        return pulumi.get(self, "run_scheduled_scan")

    @property
    @pulumi.getter(name="scanDay")
    def scan_day(self) -> Optional[str]:
        """
        Schedule scan settings day
        """
        return pulumi.get(self, "scan_day")

    @property
    @pulumi.getter(name="scanTimeInMinutes")
    def scan_time_in_minutes(self) -> Optional[str]:
        """
        Schedule scan settings time
        """
        return pulumi.get(self, "scan_time_in_minutes")

    @property
    @pulumi.getter(name="scanType")
    def scan_type(self) -> Optional[str]:
        """
        Type of scheduled scan
        """
        return pulumi.get(self, "scan_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ConfigurationProfilePreferencePropertiesResponse(dict):
    """
    Automanage configuration profile preference properties.
    """
    def __init__(__self__, *,
                 anti_malware: Optional['outputs.ConfigurationProfilePreferenceAntiMalwareResponse'] = None,
                 vm_backup: Optional['outputs.ConfigurationProfilePreferenceVmBackupResponse'] = None):
        """
        Automanage configuration profile preference properties.
        :param 'ConfigurationProfilePreferenceAntiMalwareResponseArgs' anti_malware: The custom preferences for Azure Antimalware.
        :param 'ConfigurationProfilePreferenceVmBackupResponseArgs' vm_backup: The custom preferences for Azure VM Backup.
        """
        if anti_malware is not None:
            pulumi.set(__self__, "anti_malware", anti_malware)
        if vm_backup is not None:
            pulumi.set(__self__, "vm_backup", vm_backup)

    @property
    @pulumi.getter(name="antiMalware")
    def anti_malware(self) -> Optional['outputs.ConfigurationProfilePreferenceAntiMalwareResponse']:
        """
        The custom preferences for Azure Antimalware.
        """
        return pulumi.get(self, "anti_malware")

    @property
    @pulumi.getter(name="vmBackup")
    def vm_backup(self) -> Optional['outputs.ConfigurationProfilePreferenceVmBackupResponse']:
        """
        The custom preferences for Azure VM Backup.
        """
        return pulumi.get(self, "vm_backup")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ConfigurationProfilePreferenceVmBackupResponse(dict):
    """
    Automanage configuration profile VM Backup preferences.
    """
    def __init__(__self__, *,
                 instant_rp_retention_range_in_days: Optional[int] = None,
                 retention_policy: Optional[str] = None,
                 schedule_policy: Optional[str] = None,
                 time_zone: Optional[str] = None):
        """
        Automanage configuration profile VM Backup preferences.
        :param int instant_rp_retention_range_in_days: Instant RP retention policy range in days
        :param str retention_policy: Retention policy with the details on backup copy retention ranges.
        :param str schedule_policy: Backup schedule specified as part of backup policy.
        :param str time_zone: TimeZone optional input as string. For example: Pacific Standard Time
        """
        if instant_rp_retention_range_in_days is not None:
            pulumi.set(__self__, "instant_rp_retention_range_in_days", instant_rp_retention_range_in_days)
        if retention_policy is not None:
            pulumi.set(__self__, "retention_policy", retention_policy)
        if schedule_policy is not None:
            pulumi.set(__self__, "schedule_policy", schedule_policy)
        if time_zone is not None:
            pulumi.set(__self__, "time_zone", time_zone)

    @property
    @pulumi.getter(name="instantRpRetentionRangeInDays")
    def instant_rp_retention_range_in_days(self) -> Optional[int]:
        """
        Instant RP retention policy range in days
        """
        return pulumi.get(self, "instant_rp_retention_range_in_days")

    @property
    @pulumi.getter(name="retentionPolicy")
    def retention_policy(self) -> Optional[str]:
        """
        Retention policy with the details on backup copy retention ranges.
        """
        return pulumi.get(self, "retention_policy")

    @property
    @pulumi.getter(name="schedulePolicy")
    def schedule_policy(self) -> Optional[str]:
        """
        Backup schedule specified as part of backup policy.
        """
        return pulumi.get(self, "schedule_policy")

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> Optional[str]:
        """
        TimeZone optional input as string. For example: Pacific Standard Time
        """
        return pulumi.get(self, "time_zone")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


