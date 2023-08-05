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
    'ConfidentialLedgerCertUserResponse',
    'LedgerPropertiesResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class ConfidentialLedgerCertUserResponse(dict):
    """
    User cert and permissions associated with that user
    """
    def __init__(__self__, *,
                 cert: Optional[str] = None):
        """
        User cert and permissions associated with that user
        :param str cert: Base64 encoded public key of the user cert (.pem or .cer)
        """
        if cert is not None:
            pulumi.set(__self__, "cert", cert)

    @property
    @pulumi.getter
    def cert(self) -> Optional[str]:
        """
        Base64 encoded public key of the user cert (.pem or .cer)
        """
        return pulumi.get(self, "cert")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class LedgerPropertiesResponse(dict):
    """
    Additional Confidential Ledger properties.
    """
    def __init__(__self__, *,
                 identity_service_uri: str,
                 ledger_internal_namespace: str,
                 ledger_name: str,
                 ledger_uri: str,
                 provisioning_state: str,
                 cert_users: Optional[Sequence['outputs.ConfidentialLedgerCertUserResponse']] = None,
                 ledger_storage_account: Optional[str] = None,
                 ledger_type: Optional[str] = None):
        """
        Additional Confidential Ledger properties.
        :param str identity_service_uri: Endpoint for accessing network identity.
        :param str ledger_internal_namespace: Internal namespace for the Ledger
        :param str ledger_name: Unique name for the Confidential Ledger.
        :param str ledger_uri: Endpoint for calling Ledger Service.
        :param str provisioning_state: Provisioning state of Ledger Resource
        :param Sequence['ConfidentialLedgerCertUserResponseArgs'] cert_users: Array of all the cert based users who can access Confidential Ledger
        :param str ledger_storage_account: Name of the Blob Storage Account for saving ledger files
        :param str ledger_type: Type of Confidential Ledger
        """
        pulumi.set(__self__, "identity_service_uri", identity_service_uri)
        pulumi.set(__self__, "ledger_internal_namespace", ledger_internal_namespace)
        pulumi.set(__self__, "ledger_name", ledger_name)
        pulumi.set(__self__, "ledger_uri", ledger_uri)
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if cert_users is not None:
            pulumi.set(__self__, "cert_users", cert_users)
        if ledger_storage_account is not None:
            pulumi.set(__self__, "ledger_storage_account", ledger_storage_account)
        if ledger_type is not None:
            pulumi.set(__self__, "ledger_type", ledger_type)

    @property
    @pulumi.getter(name="identityServiceUri")
    def identity_service_uri(self) -> str:
        """
        Endpoint for accessing network identity.
        """
        return pulumi.get(self, "identity_service_uri")

    @property
    @pulumi.getter(name="ledgerInternalNamespace")
    def ledger_internal_namespace(self) -> str:
        """
        Internal namespace for the Ledger
        """
        return pulumi.get(self, "ledger_internal_namespace")

    @property
    @pulumi.getter(name="ledgerName")
    def ledger_name(self) -> str:
        """
        Unique name for the Confidential Ledger.
        """
        return pulumi.get(self, "ledger_name")

    @property
    @pulumi.getter(name="ledgerUri")
    def ledger_uri(self) -> str:
        """
        Endpoint for calling Ledger Service.
        """
        return pulumi.get(self, "ledger_uri")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of Ledger Resource
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="certUsers")
    def cert_users(self) -> Optional[Sequence['outputs.ConfidentialLedgerCertUserResponse']]:
        """
        Array of all the cert based users who can access Confidential Ledger
        """
        return pulumi.get(self, "cert_users")

    @property
    @pulumi.getter(name="ledgerStorageAccount")
    def ledger_storage_account(self) -> Optional[str]:
        """
        Name of the Blob Storage Account for saving ledger files
        """
        return pulumi.get(self, "ledger_storage_account")

    @property
    @pulumi.getter(name="ledgerType")
    def ledger_type(self) -> Optional[str]:
        """
        Type of Confidential Ledger
        """
        return pulumi.get(self, "ledger_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


