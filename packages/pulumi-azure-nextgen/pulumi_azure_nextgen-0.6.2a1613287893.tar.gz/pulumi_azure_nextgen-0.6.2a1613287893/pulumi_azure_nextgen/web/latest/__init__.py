# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .app_service_environment import *
from .app_service_plan import *
from .app_service_plan_route_for_vnet import *
from .certificate import *
from .certificate_csr import *
from .connection import *
from .connection_gateway import *
from .custom_api import *
from .get_app_service_environment import *
from .get_app_service_plan import *
from .get_certificate import *
from .get_certificate_csr import *
from .get_connection import *
from .get_connection_gateway import *
from .get_custom_api import *
from .get_managed_hosting_environment import *
from .get_site_instance_deployment import *
from .get_site_instance_deployment_slot import *
from .get_static_site import *
from .get_web_app import *
from .get_web_app_deployment import *
from .get_web_app_deployment_slot import *
from .get_web_app_diagnostic_logs_configuration import *
from .get_web_app_domain_ownership_identifier import *
from .get_web_app_domain_ownership_identifier_slot import *
from .get_web_app_function import *
from .get_web_app_host_name_binding import *
from .get_web_app_host_name_binding_slot import *
from .get_web_app_hybrid_connection import *
from .get_web_app_hybrid_connection_slot import *
from .get_web_app_instance_function_slot import *
from .get_web_app_premier_add_on import *
from .get_web_app_premier_add_on_slot import *
from .get_web_app_private_endpoint_connection import *
from .get_web_app_public_certificate import *
from .get_web_app_public_certificate_slot import *
from .get_web_app_relay_service_connection import *
from .get_web_app_relay_service_connection_slot import *
from .get_web_app_site_extension import *
from .get_web_app_site_extension_slot import *
from .get_web_app_slot import *
from .get_web_app_slot_configuration_names import *
from .get_web_app_source_control import *
from .get_web_app_source_control_slot import *
from .get_web_app_swift_virtual_network_connection import *
from .get_web_app_swift_virtual_network_connection_slot import *
from .get_web_app_vnet_connection import *
from .get_web_app_vnet_connection_slot import *
from .list_app_service_plan_hybrid_connection_keys import *
from .list_connection_consent_links import *
from .list_custom_api_wsdl_interfaces import *
from .list_site_identifiers_assigned_to_host_name import *
from .list_static_site_build_function_app_settings import *
from .list_static_site_function_app_settings import *
from .list_static_site_secrets import *
from .list_static_site_users import *
from .list_web_app_auth_settings import *
from .list_web_app_auth_settings_slot import *
from .list_web_app_azure_storage_accounts import *
from .list_web_app_azure_storage_accounts_slot import *
from .list_web_app_backup_configuration import *
from .list_web_app_backup_configuration_slot import *
from .list_web_app_backup_status_secrets import *
from .list_web_app_backup_status_secrets_slot import *
from .list_web_app_connection_strings import *
from .list_web_app_connection_strings_slot import *
from .list_web_app_function_keys import *
from .list_web_app_function_keys_slot import *
from .list_web_app_function_secrets import *
from .list_web_app_function_secrets_slot import *
from .list_web_app_host_keys import *
from .list_web_app_host_keys_slot import *
from .list_web_app_hybrid_connection_keys import *
from .list_web_app_hybrid_connection_keys_slot import *
from .list_web_app_metadata import *
from .list_web_app_metadata_slot import *
from .list_web_app_publishing_credentials import *
from .list_web_app_publishing_credentials_slot import *
from .list_web_app_site_backups import *
from .list_web_app_site_backups_slot import *
from .list_web_app_site_push_settings import *
from .list_web_app_site_push_settings_slot import *
from .list_web_app_sync_function_triggers import *
from .list_web_app_sync_function_triggers_slot import *
from .list_web_application_settings import *
from .list_web_application_settings_slot import *
from .managed_hosting_environment import *
from .site_instance_deployment import *
from .site_instance_deployment_slot import *
from .static_site import *
from .web_app import *
from .web_app_auth_settings import *
from .web_app_auth_settings_slot import *
from .web_app_auth_settings_v2 import *
from .web_app_auth_settings_v2_slot import *
from .web_app_azure_storage_accounts import *
from .web_app_azure_storage_accounts_slot import *
from .web_app_backup_configuration import *
from .web_app_backup_configuration_slot import *
from .web_app_connection_strings import *
from .web_app_connection_strings_slot import *
from .web_app_deployment import *
from .web_app_deployment_slot import *
from .web_app_diagnostic_logs_configuration import *
from .web_app_domain_ownership_identifier import *
from .web_app_domain_ownership_identifier_slot import *
from .web_app_function import *
from .web_app_host_name_binding import *
from .web_app_host_name_binding_slot import *
from .web_app_hybrid_connection import *
from .web_app_hybrid_connection_slot import *
from .web_app_instance_function_slot import *
from .web_app_metadata import *
from .web_app_metadata_slot import *
from .web_app_premier_add_on import *
from .web_app_premier_add_on_slot import *
from .web_app_private_endpoint_connection import *
from .web_app_public_certificate import *
from .web_app_public_certificate_slot import *
from .web_app_relay_service_connection import *
from .web_app_relay_service_connection_slot import *
from .web_app_site_extension import *
from .web_app_site_extension_slot import *
from .web_app_site_push_settings import *
from .web_app_site_push_settings_slot import *
from .web_app_slot import *
from .web_app_slot_configuration_names import *
from .web_app_source_control import *
from .web_app_source_control_slot import *
from .web_app_swift_virtual_network_connection import *
from .web_app_swift_virtual_network_connection_slot import *
from .web_app_vnet_connection import *
from .web_app_vnet_connection_slot import *
from .web_application_settings import *
from .web_application_settings_slot import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from ... import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:web/latest:AppServiceEnvironment":
                return AppServiceEnvironment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:AppServicePlan":
                return AppServicePlan(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:AppServicePlanRouteForVnet":
                return AppServicePlanRouteForVnet(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:Certificate":
                return Certificate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:CertificateCsr":
                return CertificateCsr(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:Connection":
                return Connection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:ConnectionGateway":
                return ConnectionGateway(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:CustomApi":
                return CustomApi(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:ManagedHostingEnvironment":
                return ManagedHostingEnvironment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:SiteInstanceDeployment":
                return SiteInstanceDeployment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:SiteInstanceDeploymentSlot":
                return SiteInstanceDeploymentSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:StaticSite":
                return StaticSite(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebApp":
                return WebApp(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppAuthSettings":
                return WebAppAuthSettings(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppAuthSettingsSlot":
                return WebAppAuthSettingsSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppAuthSettingsV2":
                return WebAppAuthSettingsV2(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppAuthSettingsV2Slot":
                return WebAppAuthSettingsV2Slot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppAzureStorageAccounts":
                return WebAppAzureStorageAccounts(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppAzureStorageAccountsSlot":
                return WebAppAzureStorageAccountsSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppBackupConfiguration":
                return WebAppBackupConfiguration(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppBackupConfigurationSlot":
                return WebAppBackupConfigurationSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppConnectionStrings":
                return WebAppConnectionStrings(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppConnectionStringsSlot":
                return WebAppConnectionStringsSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppDeployment":
                return WebAppDeployment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppDeploymentSlot":
                return WebAppDeploymentSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppDiagnosticLogsConfiguration":
                return WebAppDiagnosticLogsConfiguration(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppDomainOwnershipIdentifier":
                return WebAppDomainOwnershipIdentifier(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppDomainOwnershipIdentifierSlot":
                return WebAppDomainOwnershipIdentifierSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppFunction":
                return WebAppFunction(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppHostNameBinding":
                return WebAppHostNameBinding(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppHostNameBindingSlot":
                return WebAppHostNameBindingSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppHybridConnection":
                return WebAppHybridConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppHybridConnectionSlot":
                return WebAppHybridConnectionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppInstanceFunctionSlot":
                return WebAppInstanceFunctionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppMetadata":
                return WebAppMetadata(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppMetadataSlot":
                return WebAppMetadataSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppPremierAddOn":
                return WebAppPremierAddOn(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppPremierAddOnSlot":
                return WebAppPremierAddOnSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppPrivateEndpointConnection":
                return WebAppPrivateEndpointConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppPublicCertificate":
                return WebAppPublicCertificate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppPublicCertificateSlot":
                return WebAppPublicCertificateSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppRelayServiceConnection":
                return WebAppRelayServiceConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppRelayServiceConnectionSlot":
                return WebAppRelayServiceConnectionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppSiteExtension":
                return WebAppSiteExtension(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppSiteExtensionSlot":
                return WebAppSiteExtensionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppSitePushSettings":
                return WebAppSitePushSettings(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppSitePushSettingsSlot":
                return WebAppSitePushSettingsSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppSlot":
                return WebAppSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppSlotConfigurationNames":
                return WebAppSlotConfigurationNames(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppSourceControl":
                return WebAppSourceControl(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppSourceControlSlot":
                return WebAppSourceControlSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppSwiftVirtualNetworkConnection":
                return WebAppSwiftVirtualNetworkConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppSwiftVirtualNetworkConnectionSlot":
                return WebAppSwiftVirtualNetworkConnectionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppVnetConnection":
                return WebAppVnetConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebAppVnetConnectionSlot":
                return WebAppVnetConnectionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebApplicationSettings":
                return WebApplicationSettings(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/latest:WebApplicationSettingsSlot":
                return WebApplicationSettingsSlot(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "web/latest", _module_instance)

_register_module()
