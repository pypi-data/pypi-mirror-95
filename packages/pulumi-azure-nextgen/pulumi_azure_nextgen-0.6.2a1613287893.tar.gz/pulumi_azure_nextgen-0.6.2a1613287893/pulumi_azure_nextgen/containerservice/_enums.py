# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AgentPoolMode',
    'AgentPoolType',
    'ConnectionStatus',
    'ContainerServiceOrchestratorTypes',
    'ContainerServiceVMSizeTypes',
    'Expander',
    'KubeletDiskType',
    'LicenseType',
    'LoadBalancerSku',
    'ManagedClusterSKUName',
    'ManagedClusterSKUTier',
    'NetworkMode',
    'NetworkPlugin',
    'NetworkPolicy',
    'OSDiskType',
    'OSType',
    'OpenShiftAgentPoolProfileRole',
    'OpenShiftContainerServiceVMSize',
    'OutboundType',
    'ResourceIdentityType',
    'ScaleSetEvictionPolicy',
    'ScaleSetPriority',
    'UpgradeChannel',
    'WeekDay',
]


class AgentPoolMode(str, Enum):
    """
    AgentPoolMode represents mode of an agent pool
    """
    SYSTEM = "System"
    USER = "User"


class AgentPoolType(str, Enum):
    """
    AgentPoolType represents types of an agent pool
    """
    VIRTUAL_MACHINE_SCALE_SETS = "VirtualMachineScaleSets"
    AVAILABILITY_SET = "AvailabilitySet"


class ConnectionStatus(str, Enum):
    """
    The private link service connection status.
    """
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DISCONNECTED = "Disconnected"


class ContainerServiceOrchestratorTypes(str, Enum):
    """
    The orchestrator to use to manage container service cluster resources. Valid values are Swarm, DCOS, and Custom.
    """
    SWARM = "Swarm"
    DCOS = "DCOS"
    CUSTOM = "Custom"
    KUBERNETES = "Kubernetes"


class ContainerServiceVMSizeTypes(str, Enum):
    """
    Size of agent VMs.
    """
    STANDARD_A1 = "Standard_A1"
    STANDARD_A10 = "Standard_A10"
    STANDARD_A11 = "Standard_A11"
    STANDARD_A1_V2 = "Standard_A1_v2"
    STANDARD_A2 = "Standard_A2"
    STANDARD_A2_V2 = "Standard_A2_v2"
    STANDARD_A2M_V2 = "Standard_A2m_v2"
    STANDARD_A3 = "Standard_A3"
    STANDARD_A4 = "Standard_A4"
    STANDARD_A4_V2 = "Standard_A4_v2"
    STANDARD_A4M_V2 = "Standard_A4m_v2"
    STANDARD_A5 = "Standard_A5"
    STANDARD_A6 = "Standard_A6"
    STANDARD_A7 = "Standard_A7"
    STANDARD_A8 = "Standard_A8"
    STANDARD_A8_V2 = "Standard_A8_v2"
    STANDARD_A8M_V2 = "Standard_A8m_v2"
    STANDARD_A9 = "Standard_A9"
    STANDARD_B2MS = "Standard_B2ms"
    STANDARD_B2S = "Standard_B2s"
    STANDARD_B4MS = "Standard_B4ms"
    STANDARD_B8MS = "Standard_B8ms"
    STANDARD_D1 = "Standard_D1"
    STANDARD_D11 = "Standard_D11"
    STANDARD_D11_V2 = "Standard_D11_v2"
    STANDARD_D11_V2_PROMO = "Standard_D11_v2_Promo"
    STANDARD_D12 = "Standard_D12"
    STANDARD_D12_V2 = "Standard_D12_v2"
    STANDARD_D12_V2_PROMO = "Standard_D12_v2_Promo"
    STANDARD_D13 = "Standard_D13"
    STANDARD_D13_V2 = "Standard_D13_v2"
    STANDARD_D13_V2_PROMO = "Standard_D13_v2_Promo"
    STANDARD_D14 = "Standard_D14"
    STANDARD_D14_V2 = "Standard_D14_v2"
    STANDARD_D14_V2_PROMO = "Standard_D14_v2_Promo"
    STANDARD_D15_V2 = "Standard_D15_v2"
    STANDARD_D16_V3 = "Standard_D16_v3"
    STANDARD_D16S_V3 = "Standard_D16s_v3"
    STANDARD_D1_V2 = "Standard_D1_v2"
    STANDARD_D2 = "Standard_D2"
    STANDARD_D2_V2 = "Standard_D2_v2"
    STANDARD_D2_V2_PROMO = "Standard_D2_v2_Promo"
    STANDARD_D2_V3 = "Standard_D2_v3"
    STANDARD_D2S_V3 = "Standard_D2s_v3"
    STANDARD_D3 = "Standard_D3"
    STANDARD_D32_V3 = "Standard_D32_v3"
    STANDARD_D32S_V3 = "Standard_D32s_v3"
    STANDARD_D3_V2 = "Standard_D3_v2"
    STANDARD_D3_V2_PROMO = "Standard_D3_v2_Promo"
    STANDARD_D4 = "Standard_D4"
    STANDARD_D4_V2 = "Standard_D4_v2"
    STANDARD_D4_V2_PROMO = "Standard_D4_v2_Promo"
    STANDARD_D4_V3 = "Standard_D4_v3"
    STANDARD_D4S_V3 = "Standard_D4s_v3"
    STANDARD_D5_V2 = "Standard_D5_v2"
    STANDARD_D5_V2_PROMO = "Standard_D5_v2_Promo"
    STANDARD_D64_V3 = "Standard_D64_v3"
    STANDARD_D64S_V3 = "Standard_D64s_v3"
    STANDARD_D8_V3 = "Standard_D8_v3"
    STANDARD_D8S_V3 = "Standard_D8s_v3"
    STANDARD_DS1 = "Standard_DS1"
    STANDARD_DS11 = "Standard_DS11"
    STANDARD_DS11_V2 = "Standard_DS11_v2"
    STANDARD_DS11_V2_PROMO = "Standard_DS11_v2_Promo"
    STANDARD_DS12 = "Standard_DS12"
    STANDARD_DS12_V2 = "Standard_DS12_v2"
    STANDARD_DS12_V2_PROMO = "Standard_DS12_v2_Promo"
    STANDARD_DS13 = "Standard_DS13"
    STANDARD_DS13_2_V2 = "Standard_DS13-2_v2"
    STANDARD_DS13_4_V2 = "Standard_DS13-4_v2"
    STANDARD_DS13_V2 = "Standard_DS13_v2"
    STANDARD_DS13_V2_PROMO = "Standard_DS13_v2_Promo"
    STANDARD_DS14 = "Standard_DS14"
    STANDARD_DS14_4_V2 = "Standard_DS14-4_v2"
    STANDARD_DS14_8_V2 = "Standard_DS14-8_v2"
    STANDARD_DS14_V2 = "Standard_DS14_v2"
    STANDARD_DS14_V2_PROMO = "Standard_DS14_v2_Promo"
    STANDARD_DS15_V2 = "Standard_DS15_v2"
    STANDARD_DS1_V2 = "Standard_DS1_v2"
    STANDARD_DS2 = "Standard_DS2"
    STANDARD_DS2_V2 = "Standard_DS2_v2"
    STANDARD_DS2_V2_PROMO = "Standard_DS2_v2_Promo"
    STANDARD_DS3 = "Standard_DS3"
    STANDARD_DS3_V2 = "Standard_DS3_v2"
    STANDARD_DS3_V2_PROMO = "Standard_DS3_v2_Promo"
    STANDARD_DS4 = "Standard_DS4"
    STANDARD_DS4_V2 = "Standard_DS4_v2"
    STANDARD_DS4_V2_PROMO = "Standard_DS4_v2_Promo"
    STANDARD_DS5_V2 = "Standard_DS5_v2"
    STANDARD_DS5_V2_PROMO = "Standard_DS5_v2_Promo"
    STANDARD_E16_V3 = "Standard_E16_v3"
    STANDARD_E16S_V3 = "Standard_E16s_v3"
    STANDARD_E2_V3 = "Standard_E2_v3"
    STANDARD_E2S_V3 = "Standard_E2s_v3"
    STANDARD_E32_16S_V3 = "Standard_E32-16s_v3"
    STANDARD_E32_8S_V3 = "Standard_E32-8s_v3"
    STANDARD_E32_V3 = "Standard_E32_v3"
    STANDARD_E32S_V3 = "Standard_E32s_v3"
    STANDARD_E4_V3 = "Standard_E4_v3"
    STANDARD_E4S_V3 = "Standard_E4s_v3"
    STANDARD_E64_16S_V3 = "Standard_E64-16s_v3"
    STANDARD_E64_32S_V3 = "Standard_E64-32s_v3"
    STANDARD_E64_V3 = "Standard_E64_v3"
    STANDARD_E64S_V3 = "Standard_E64s_v3"
    STANDARD_E8_V3 = "Standard_E8_v3"
    STANDARD_E8S_V3 = "Standard_E8s_v3"
    STANDARD_F1 = "Standard_F1"
    STANDARD_F16 = "Standard_F16"
    STANDARD_F16S = "Standard_F16s"
    STANDARD_F16S_V2 = "Standard_F16s_v2"
    STANDARD_F1S = "Standard_F1s"
    STANDARD_F2 = "Standard_F2"
    STANDARD_F2S = "Standard_F2s"
    STANDARD_F2S_V2 = "Standard_F2s_v2"
    STANDARD_F32S_V2 = "Standard_F32s_v2"
    STANDARD_F4 = "Standard_F4"
    STANDARD_F4S = "Standard_F4s"
    STANDARD_F4S_V2 = "Standard_F4s_v2"
    STANDARD_F64S_V2 = "Standard_F64s_v2"
    STANDARD_F72S_V2 = "Standard_F72s_v2"
    STANDARD_F8 = "Standard_F8"
    STANDARD_F8S = "Standard_F8s"
    STANDARD_F8S_V2 = "Standard_F8s_v2"
    STANDARD_G1 = "Standard_G1"
    STANDARD_G2 = "Standard_G2"
    STANDARD_G3 = "Standard_G3"
    STANDARD_G4 = "Standard_G4"
    STANDARD_G5 = "Standard_G5"
    STANDARD_GS1 = "Standard_GS1"
    STANDARD_GS2 = "Standard_GS2"
    STANDARD_GS3 = "Standard_GS3"
    STANDARD_GS4 = "Standard_GS4"
    STANDARD_GS4_4 = "Standard_GS4-4"
    STANDARD_GS4_8 = "Standard_GS4-8"
    STANDARD_GS5 = "Standard_GS5"
    STANDARD_GS5_16 = "Standard_GS5-16"
    STANDARD_GS5_8 = "Standard_GS5-8"
    STANDARD_H16 = "Standard_H16"
    STANDARD_H16M = "Standard_H16m"
    STANDARD_H16MR = "Standard_H16mr"
    STANDARD_H16R = "Standard_H16r"
    STANDARD_H8 = "Standard_H8"
    STANDARD_H8M = "Standard_H8m"
    STANDARD_L16S = "Standard_L16s"
    STANDARD_L32S = "Standard_L32s"
    STANDARD_L4S = "Standard_L4s"
    STANDARD_L8S = "Standard_L8s"
    STANDARD_M128_32MS = "Standard_M128-32ms"
    STANDARD_M128_64MS = "Standard_M128-64ms"
    STANDARD_M128MS = "Standard_M128ms"
    STANDARD_M128S = "Standard_M128s"
    STANDARD_M64_16MS = "Standard_M64-16ms"
    STANDARD_M64_32MS = "Standard_M64-32ms"
    STANDARD_M64MS = "Standard_M64ms"
    STANDARD_M64S = "Standard_M64s"
    STANDARD_NC12 = "Standard_NC12"
    STANDARD_NC12S_V2 = "Standard_NC12s_v2"
    STANDARD_NC12S_V3 = "Standard_NC12s_v3"
    STANDARD_NC24 = "Standard_NC24"
    STANDARD_NC24R = "Standard_NC24r"
    STANDARD_NC24RS_V2 = "Standard_NC24rs_v2"
    STANDARD_NC24RS_V3 = "Standard_NC24rs_v3"
    STANDARD_NC24S_V2 = "Standard_NC24s_v2"
    STANDARD_NC24S_V3 = "Standard_NC24s_v3"
    STANDARD_NC6 = "Standard_NC6"
    STANDARD_NC6S_V2 = "Standard_NC6s_v2"
    STANDARD_NC6S_V3 = "Standard_NC6s_v3"
    STANDARD_ND12S = "Standard_ND12s"
    STANDARD_ND24RS = "Standard_ND24rs"
    STANDARD_ND24S = "Standard_ND24s"
    STANDARD_ND6S = "Standard_ND6s"
    STANDARD_NV12 = "Standard_NV12"
    STANDARD_NV24 = "Standard_NV24"
    STANDARD_NV6 = "Standard_NV6"


class Expander(str, Enum):
    LEAST_WASTE = "least-waste"
    MOST_PODS = "most-pods"
    PRIORITY = "priority"
    RANDOM = "random"


class KubeletDiskType(str, Enum):
    """
    KubeletDiskType determines the placement of emptyDir volumes, container runtime data root, and Kubelet ephemeral storage. Currently allows one value, OS, resulting in Kubelet using the OS disk for data.
    """
    OS = "OS"


class LicenseType(str, Enum):
    """
    The licenseType to use for Windows VMs. Windows_Server is used to enable Azure Hybrid User Benefits for Windows VMs.
    """
    NONE = "None"
    WINDOWS_SERVER = "Windows_Server"


class LoadBalancerSku(str, Enum):
    """
    The load balancer sku for the managed cluster.
    """
    STANDARD = "standard"
    BASIC = "basic"


class ManagedClusterSKUName(str, Enum):
    """
    Name of a managed cluster SKU.
    """
    BASIC = "Basic"


class ManagedClusterSKUTier(str, Enum):
    """
    Tier of a managed cluster SKU.
    """
    PAID = "Paid"
    FREE = "Free"


class NetworkMode(str, Enum):
    """
    Network mode used for building Kubernetes network.
    """
    TRANSPARENT = "transparent"
    BRIDGE = "bridge"


class NetworkPlugin(str, Enum):
    """
    Network plugin used for building Kubernetes network.
    """
    AZURE = "azure"
    KUBENET = "kubenet"


class NetworkPolicy(str, Enum):
    """
    Network policy used for building Kubernetes network.
    """
    CALICO = "calico"
    AZURE = "azure"


class OSDiskType(str, Enum):
    """
    OS disk type to be used for machines in a given agent pool. Allowed values are 'Ephemeral' and 'Managed'. Defaults to 'Managed'. May not be changed after creation.
    """
    MANAGED = "Managed"
    EPHEMERAL = "Ephemeral"


class OSType(str, Enum):
    """
    OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
    """
    LINUX = "Linux"
    WINDOWS = "Windows"


class OpenShiftAgentPoolProfileRole(str, Enum):
    """
    Define the role of the AgentPoolProfile.
    """
    COMPUTE = "compute"
    INFRA = "infra"


class OpenShiftContainerServiceVMSize(str, Enum):
    """
    Size of agent VMs.
    """
    STANDARD_D2S_V3 = "Standard_D2s_v3"
    STANDARD_D4S_V3 = "Standard_D4s_v3"
    STANDARD_D8S_V3 = "Standard_D8s_v3"
    STANDARD_D16S_V3 = "Standard_D16s_v3"
    STANDARD_D32S_V3 = "Standard_D32s_v3"
    STANDARD_D64S_V3 = "Standard_D64s_v3"
    STANDARD_DS4_V2 = "Standard_DS4_v2"
    STANDARD_DS5_V2 = "Standard_DS5_v2"
    STANDARD_F8S_V2 = "Standard_F8s_v2"
    STANDARD_F16S_V2 = "Standard_F16s_v2"
    STANDARD_F32S_V2 = "Standard_F32s_v2"
    STANDARD_F64S_V2 = "Standard_F64s_v2"
    STANDARD_F72S_V2 = "Standard_F72s_v2"
    STANDARD_F8S = "Standard_F8s"
    STANDARD_F16S = "Standard_F16s"
    STANDARD_E4S_V3 = "Standard_E4s_v3"
    STANDARD_E8S_V3 = "Standard_E8s_v3"
    STANDARD_E16S_V3 = "Standard_E16s_v3"
    STANDARD_E20S_V3 = "Standard_E20s_v3"
    STANDARD_E32S_V3 = "Standard_E32s_v3"
    STANDARD_E64S_V3 = "Standard_E64s_v3"
    STANDARD_GS2 = "Standard_GS2"
    STANDARD_GS3 = "Standard_GS3"
    STANDARD_GS4 = "Standard_GS4"
    STANDARD_GS5 = "Standard_GS5"
    STANDARD_DS12_V2 = "Standard_DS12_v2"
    STANDARD_DS13_V2 = "Standard_DS13_v2"
    STANDARD_DS14_V2 = "Standard_DS14_v2"
    STANDARD_DS15_V2 = "Standard_DS15_v2"
    STANDARD_L4S = "Standard_L4s"
    STANDARD_L8S = "Standard_L8s"
    STANDARD_L16S = "Standard_L16s"
    STANDARD_L32S = "Standard_L32s"


class OutboundType(str, Enum):
    """
    The outbound (egress) routing method.
    """
    LOAD_BALANCER = "loadBalancer"
    USER_DEFINED_ROUTING = "userDefinedRouting"


class ResourceIdentityType(str, Enum):
    """
    The type of identity used for the managed cluster. Type 'SystemAssigned' will use an implicitly created identity in master components and an auto-created user assigned identity in MC_ resource group in agent nodes. Type 'None' will not use MSI for the managed cluster, service principal will be used instead.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    NONE = "None"


class ScaleSetEvictionPolicy(str, Enum):
    """
    ScaleSetEvictionPolicy to be used to specify eviction policy for Spot virtual machine scale set. Default to Delete.
    """
    DELETE = "Delete"
    DEALLOCATE = "Deallocate"


class ScaleSetPriority(str, Enum):
    """
    ScaleSetPriority to be used to specify virtual machine scale set priority. Default to regular.
    """
    SPOT = "Spot"
    REGULAR = "Regular"


class UpgradeChannel(str, Enum):
    """
    upgrade channel for auto upgrade.
    """
    RAPID = "rapid"
    STABLE = "stable"
    PATCH = "patch"
    NONE = "none"


class WeekDay(str, Enum):
    """
    A day in a week.
    """
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
