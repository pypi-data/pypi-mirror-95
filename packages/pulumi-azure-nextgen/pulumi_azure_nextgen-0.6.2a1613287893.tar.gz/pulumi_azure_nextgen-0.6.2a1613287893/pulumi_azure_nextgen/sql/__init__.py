# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .database import *
from .database_threat_detection_policy import *
from .database_vulnerability_assessment import *
from .database_vulnerability_assessment_rule_baseline import *
from .disaster_recovery_configuration import *
from .elastic_pool import *
from .failover_group import *
from .firewall_rule import *
from .geo_backup_policy import *
from .get_database import *
from .get_database_threat_detection_policy import *
from .get_database_vulnerability_assessment import *
from .get_database_vulnerability_assessment_rule_baseline import *
from .get_disaster_recovery_configuration import *
from .get_elastic_pool import *
from .get_failover_group import *
from .get_firewall_rule import *
from .get_geo_backup_policy import *
from .get_instance_failover_group import *
from .get_instance_pool import *
from .get_job import *
from .get_job_agent import *
from .get_job_credential import *
from .get_job_step import *
from .get_job_target_group import *
from .get_managed_database import *
from .get_managed_database_sensitivity_label import *
from .get_managed_database_vulnerability_assessment import *
from .get_managed_database_vulnerability_assessment_rule_baseline import *
from .get_managed_instance import *
from .get_managed_instance_administrator import *
from .get_managed_instance_azure_ad_only_authentication import *
from .get_managed_instance_key import *
from .get_managed_instance_private_endpoint_connection import *
from .get_managed_instance_vulnerability_assessment import *
from .get_private_endpoint_connection import *
from .get_sensitivity_label import *
from .get_server import *
from .get_server_azure_ad_administrator import *
from .get_server_azure_ad_only_authentication import *
from .get_server_communication_link import *
from .get_server_dns_alias import *
from .get_server_key import *
from .get_server_trust_group import *
from .get_server_vulnerability_assessment import *
from .get_sync_agent import *
from .get_sync_group import *
from .get_sync_member import *
from .get_transparent_data_encryption import *
from .get_virtual_network_rule import *
from .get_workload_classifier import *
from .get_workload_group import *
from .instance_failover_group import *
from .instance_pool import *
from .job import *
from .job_agent import *
from .job_credential import *
from .job_step import *
from .job_target_group import *
from .managed_database import *
from .managed_database_sensitivity_label import *
from .managed_database_vulnerability_assessment import *
from .managed_database_vulnerability_assessment_rule_baseline import *
from .managed_instance import *
from .managed_instance_administrator import *
from .managed_instance_azure_ad_only_authentication import *
from .managed_instance_key import *
from .managed_instance_private_endpoint_connection import *
from .managed_instance_vulnerability_assessment import *
from .private_endpoint_connection import *
from .sensitivity_label import *
from .server import *
from .server_azure_ad_administrator import *
from .server_azure_ad_only_authentication import *
from .server_communication_link import *
from .server_dns_alias import *
from .server_key import *
from .server_trust_group import *
from .server_vulnerability_assessment import *
from .sync_agent import *
from .sync_group import *
from .sync_member import *
from .transparent_data_encryption import *
from .virtual_network_rule import *
from .workload_classifier import *
from .workload_group import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    latest,
    v20140401,
    v20150501preview,
    v20170301preview,
    v20171001preview,
    v20180601preview,
    v20190601preview,
    v20200202preview,
    v20200801preview,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:sql:Database":
                return Database(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:DatabaseThreatDetectionPolicy":
                return DatabaseThreatDetectionPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:DatabaseVulnerabilityAssessment":
                return DatabaseVulnerabilityAssessment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:DatabaseVulnerabilityAssessmentRuleBaseline":
                return DatabaseVulnerabilityAssessmentRuleBaseline(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:DisasterRecoveryConfiguration":
                return DisasterRecoveryConfiguration(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ElasticPool":
                return ElasticPool(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:FailoverGroup":
                return FailoverGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:FirewallRule":
                return FirewallRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:GeoBackupPolicy":
                return GeoBackupPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:InstanceFailoverGroup":
                return InstanceFailoverGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:InstancePool":
                return InstancePool(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:Job":
                return Job(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:JobAgent":
                return JobAgent(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:JobCredential":
                return JobCredential(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:JobStep":
                return JobStep(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:JobTargetGroup":
                return JobTargetGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ManagedDatabase":
                return ManagedDatabase(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ManagedDatabaseSensitivityLabel":
                return ManagedDatabaseSensitivityLabel(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ManagedDatabaseVulnerabilityAssessment":
                return ManagedDatabaseVulnerabilityAssessment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ManagedDatabaseVulnerabilityAssessmentRuleBaseline":
                return ManagedDatabaseVulnerabilityAssessmentRuleBaseline(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ManagedInstance":
                return ManagedInstance(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ManagedInstanceAdministrator":
                return ManagedInstanceAdministrator(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ManagedInstanceAzureADOnlyAuthentication":
                return ManagedInstanceAzureADOnlyAuthentication(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ManagedInstanceKey":
                return ManagedInstanceKey(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ManagedInstancePrivateEndpointConnection":
                return ManagedInstancePrivateEndpointConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ManagedInstanceVulnerabilityAssessment":
                return ManagedInstanceVulnerabilityAssessment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:PrivateEndpointConnection":
                return PrivateEndpointConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:SensitivityLabel":
                return SensitivityLabel(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:Server":
                return Server(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ServerAzureADAdministrator":
                return ServerAzureADAdministrator(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ServerAzureADOnlyAuthentication":
                return ServerAzureADOnlyAuthentication(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ServerCommunicationLink":
                return ServerCommunicationLink(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ServerDnsAlias":
                return ServerDnsAlias(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ServerKey":
                return ServerKey(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ServerTrustGroup":
                return ServerTrustGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:ServerVulnerabilityAssessment":
                return ServerVulnerabilityAssessment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:SyncAgent":
                return SyncAgent(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:SyncGroup":
                return SyncGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:SyncMember":
                return SyncMember(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:TransparentDataEncryption":
                return TransparentDataEncryption(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:VirtualNetworkRule":
                return VirtualNetworkRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:WorkloadClassifier":
                return WorkloadClassifier(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:sql:WorkloadGroup":
                return WorkloadGroup(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "sql", _module_instance)

_register_module()
