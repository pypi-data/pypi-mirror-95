# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ApplianceArtifactType',
    'ApplianceLockLevel',
    'ApplicationArtifactType',
    'ApplicationDefinitionArtifactName',
    'ApplicationLockLevel',
    'ApplicationManagementMode',
    'DeploymentMode',
    'JitApprovalMode',
    'JitApproverType',
    'ResourceIdentityType',
]


class ApplianceArtifactType(str, Enum):
    """
    The appliance artifact type.
    """
    TEMPLATE = "Template"
    CUSTOM = "Custom"


class ApplianceLockLevel(str, Enum):
    """
    The appliance lock level.
    """
    CAN_NOT_DELETE = "CanNotDelete"
    READ_ONLY = "ReadOnly"
    NONE = "None"


class ApplicationArtifactType(str, Enum):
    """
    The managed application definition artifact type.
    """
    NOT_SPECIFIED = "NotSpecified"
    TEMPLATE = "Template"
    CUSTOM = "Custom"


class ApplicationDefinitionArtifactName(str, Enum):
    """
    The managed application definition artifact name.
    """
    NOT_SPECIFIED = "NotSpecified"
    APPLICATION_RESOURCE_TEMPLATE = "ApplicationResourceTemplate"
    CREATE_UI_DEFINITION = "CreateUiDefinition"
    MAIN_TEMPLATE_PARAMETERS = "MainTemplateParameters"


class ApplicationLockLevel(str, Enum):
    """
    The managed application lock level.
    """
    CAN_NOT_DELETE = "CanNotDelete"
    READ_ONLY = "ReadOnly"
    NONE = "None"


class ApplicationManagementMode(str, Enum):
    """
    The managed application management mode.
    """
    NOT_SPECIFIED = "NotSpecified"
    UNMANAGED = "Unmanaged"
    MANAGED = "Managed"


class DeploymentMode(str, Enum):
    """
    The managed application deployment mode.
    """
    NOT_SPECIFIED = "NotSpecified"
    INCREMENTAL = "Incremental"
    COMPLETE = "Complete"


class JitApprovalMode(str, Enum):
    """
    JIT approval mode.
    """
    NOT_SPECIFIED = "NotSpecified"
    AUTO_APPROVE = "AutoApprove"
    MANUAL_APPROVE = "ManualApprove"


class JitApproverType(str, Enum):
    """
    The approver type.
    """
    USER = "user"
    GROUP = "group"


class ResourceIdentityType(str, Enum):
    """
    The identity type.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned, UserAssigned"
    NONE = "None"
