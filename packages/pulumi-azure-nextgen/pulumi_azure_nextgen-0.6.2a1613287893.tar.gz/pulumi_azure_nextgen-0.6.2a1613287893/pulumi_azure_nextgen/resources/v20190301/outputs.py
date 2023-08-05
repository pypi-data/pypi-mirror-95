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
    'AliasPathTypeResponse',
    'AliasTypeResponse',
    'BasicDependencyResponse',
    'DebugSettingResponse',
    'DependencyResponse',
    'DeploymentPropertiesExtendedResponse',
    'IdentityResponse',
    'IdentityResponseUserAssignedIdentities',
    'OnErrorDeploymentExtendedResponse',
    'ParametersLinkResponse',
    'PlanResponse',
    'ProviderResourceTypeResponse',
    'ProviderResponse',
    'ResourceGroupPropertiesResponse',
    'SkuResponse',
    'TemplateLinkResponse',
]

@pulumi.output_type
class AliasPathTypeResponse(dict):
    """
    The type of the paths for alias. 
    """
    def __init__(__self__, *,
                 api_versions: Optional[Sequence[str]] = None,
                 path: Optional[str] = None):
        """
        The type of the paths for alias. 
        :param Sequence[str] api_versions: The API versions.
        :param str path: The path of an alias.
        """
        if api_versions is not None:
            pulumi.set(__self__, "api_versions", api_versions)
        if path is not None:
            pulumi.set(__self__, "path", path)

    @property
    @pulumi.getter(name="apiVersions")
    def api_versions(self) -> Optional[Sequence[str]]:
        """
        The API versions.
        """
        return pulumi.get(self, "api_versions")

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        """
        The path of an alias.
        """
        return pulumi.get(self, "path")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class AliasTypeResponse(dict):
    """
    The alias type. 
    """
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 paths: Optional[Sequence['outputs.AliasPathTypeResponse']] = None):
        """
        The alias type. 
        :param str name: The alias name.
        :param Sequence['AliasPathTypeResponseArgs'] paths: The paths for an alias.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if paths is not None:
            pulumi.set(__self__, "paths", paths)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The alias name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def paths(self) -> Optional[Sequence['outputs.AliasPathTypeResponse']]:
        """
        The paths for an alias.
        """
        return pulumi.get(self, "paths")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class BasicDependencyResponse(dict):
    """
    Deployment dependency information.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None,
                 resource_name: Optional[str] = None,
                 resource_type: Optional[str] = None):
        """
        Deployment dependency information.
        :param str id: The ID of the dependency.
        :param str resource_name: The dependency resource name.
        :param str resource_type: The dependency resource type.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the dependency.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[str]:
        """
        The dependency resource name.
        """
        return pulumi.get(self, "resource_name")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[str]:
        """
        The dependency resource type.
        """
        return pulumi.get(self, "resource_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class DebugSettingResponse(dict):
    def __init__(__self__, *,
                 detail_level: Optional[str] = None):
        """
        :param str detail_level: Specifies the type of information to log for debugging. The permitted values are none, requestContent, responseContent, or both requestContent and responseContent separated by a comma. The default is none. When setting this value, carefully consider the type of information you are passing in during deployment. By logging information about the request or response, you could potentially expose sensitive data that is retrieved through the deployment operations.
        """
        if detail_level is not None:
            pulumi.set(__self__, "detail_level", detail_level)

    @property
    @pulumi.getter(name="detailLevel")
    def detail_level(self) -> Optional[str]:
        """
        Specifies the type of information to log for debugging. The permitted values are none, requestContent, responseContent, or both requestContent and responseContent separated by a comma. The default is none. When setting this value, carefully consider the type of information you are passing in during deployment. By logging information about the request or response, you could potentially expose sensitive data that is retrieved through the deployment operations.
        """
        return pulumi.get(self, "detail_level")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class DependencyResponse(dict):
    """
    Deployment dependency information.
    """
    def __init__(__self__, *,
                 depends_on: Optional[Sequence['outputs.BasicDependencyResponse']] = None,
                 id: Optional[str] = None,
                 resource_name: Optional[str] = None,
                 resource_type: Optional[str] = None):
        """
        Deployment dependency information.
        :param Sequence['BasicDependencyResponseArgs'] depends_on: The list of dependencies.
        :param str id: The ID of the dependency.
        :param str resource_name: The dependency resource name.
        :param str resource_type: The dependency resource type.
        """
        if depends_on is not None:
            pulumi.set(__self__, "depends_on", depends_on)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter(name="dependsOn")
    def depends_on(self) -> Optional[Sequence['outputs.BasicDependencyResponse']]:
        """
        The list of dependencies.
        """
        return pulumi.get(self, "depends_on")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the dependency.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[str]:
        """
        The dependency resource name.
        """
        return pulumi.get(self, "resource_name")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[str]:
        """
        The dependency resource type.
        """
        return pulumi.get(self, "resource_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class DeploymentPropertiesExtendedResponse(dict):
    """
    Deployment properties with additional details.
    """
    def __init__(__self__, *,
                 correlation_id: str,
                 provisioning_state: str,
                 timestamp: str,
                 debug_setting: Optional['outputs.DebugSettingResponse'] = None,
                 dependencies: Optional[Sequence['outputs.DependencyResponse']] = None,
                 mode: Optional[str] = None,
                 on_error_deployment: Optional['outputs.OnErrorDeploymentExtendedResponse'] = None,
                 outputs: Optional[Any] = None,
                 parameters: Optional[Any] = None,
                 parameters_link: Optional['outputs.ParametersLinkResponse'] = None,
                 providers: Optional[Sequence['outputs.ProviderResponse']] = None,
                 template: Optional[Any] = None,
                 template_link: Optional['outputs.TemplateLinkResponse'] = None):
        """
        Deployment properties with additional details.
        :param str correlation_id: The correlation ID of the deployment.
        :param str provisioning_state: The state of the provisioning.
        :param str timestamp: The timestamp of the template deployment.
        :param 'DebugSettingResponseArgs' debug_setting: The debug setting of the deployment.
        :param Sequence['DependencyResponseArgs'] dependencies: The list of deployment dependencies.
        :param str mode: The deployment mode. Possible values are Incremental and Complete.
        :param 'OnErrorDeploymentExtendedResponseArgs' on_error_deployment: The deployment on error behavior.
        :param Any outputs: Key/value pairs that represent deployment output.
        :param Any parameters: Deployment parameters. Use only one of Parameters or ParametersLink.
        :param 'ParametersLinkResponseArgs' parameters_link: The URI referencing the parameters. Use only one of Parameters or ParametersLink.
        :param Sequence['ProviderResponseArgs'] providers: The list of resource providers needed for the deployment.
        :param Any template: The template content. Use only one of Template or TemplateLink.
        :param 'TemplateLinkResponseArgs' template_link: The URI referencing the template. Use only one of Template or TemplateLink.
        """
        pulumi.set(__self__, "correlation_id", correlation_id)
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        pulumi.set(__self__, "timestamp", timestamp)
        if debug_setting is not None:
            pulumi.set(__self__, "debug_setting", debug_setting)
        if dependencies is not None:
            pulumi.set(__self__, "dependencies", dependencies)
        if mode is not None:
            pulumi.set(__self__, "mode", mode)
        if on_error_deployment is not None:
            pulumi.set(__self__, "on_error_deployment", on_error_deployment)
        if outputs is not None:
            pulumi.set(__self__, "outputs", outputs)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if parameters_link is not None:
            pulumi.set(__self__, "parameters_link", parameters_link)
        if providers is not None:
            pulumi.set(__self__, "providers", providers)
        if template is not None:
            pulumi.set(__self__, "template", template)
        if template_link is not None:
            pulumi.set(__self__, "template_link", template_link)

    @property
    @pulumi.getter(name="correlationId")
    def correlation_id(self) -> str:
        """
        The correlation ID of the deployment.
        """
        return pulumi.get(self, "correlation_id")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The state of the provisioning.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def timestamp(self) -> str:
        """
        The timestamp of the template deployment.
        """
        return pulumi.get(self, "timestamp")

    @property
    @pulumi.getter(name="debugSetting")
    def debug_setting(self) -> Optional['outputs.DebugSettingResponse']:
        """
        The debug setting of the deployment.
        """
        return pulumi.get(self, "debug_setting")

    @property
    @pulumi.getter
    def dependencies(self) -> Optional[Sequence['outputs.DependencyResponse']]:
        """
        The list of deployment dependencies.
        """
        return pulumi.get(self, "dependencies")

    @property
    @pulumi.getter
    def mode(self) -> Optional[str]:
        """
        The deployment mode. Possible values are Incremental and Complete.
        """
        return pulumi.get(self, "mode")

    @property
    @pulumi.getter(name="onErrorDeployment")
    def on_error_deployment(self) -> Optional['outputs.OnErrorDeploymentExtendedResponse']:
        """
        The deployment on error behavior.
        """
        return pulumi.get(self, "on_error_deployment")

    @property
    @pulumi.getter
    def outputs(self) -> Optional[Any]:
        """
        Key/value pairs that represent deployment output.
        """
        return pulumi.get(self, "outputs")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Any]:
        """
        Deployment parameters. Use only one of Parameters or ParametersLink.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="parametersLink")
    def parameters_link(self) -> Optional['outputs.ParametersLinkResponse']:
        """
        The URI referencing the parameters. Use only one of Parameters or ParametersLink.
        """
        return pulumi.get(self, "parameters_link")

    @property
    @pulumi.getter
    def providers(self) -> Optional[Sequence['outputs.ProviderResponse']]:
        """
        The list of resource providers needed for the deployment.
        """
        return pulumi.get(self, "providers")

    @property
    @pulumi.getter
    def template(self) -> Optional[Any]:
        """
        The template content. Use only one of Template or TemplateLink.
        """
        return pulumi.get(self, "template")

    @property
    @pulumi.getter(name="templateLink")
    def template_link(self) -> Optional['outputs.TemplateLinkResponse']:
        """
        The URI referencing the template. Use only one of Template or TemplateLink.
        """
        return pulumi.get(self, "template_link")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IdentityResponse(dict):
    """
    Identity for the resource.
    """
    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: Optional[str] = None,
                 user_assigned_identities: Optional[Mapping[str, 'outputs.IdentityResponseUserAssignedIdentities']] = None):
        """
        Identity for the resource.
        :param str principal_id: The principal ID of resource identity.
        :param str tenant_id: The tenant ID of resource.
        :param str type: The identity type.
        :param Mapping[str, 'IdentityResponseUserAssignedIdentitiesArgs'] user_assigned_identities: The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of resource identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.IdentityResponseUserAssignedIdentities']]:
        """
        The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IdentityResponseUserAssignedIdentities(dict):
    def __init__(__self__, *,
                 client_id: str,
                 principal_id: str):
        """
        :param str client_id: The client id of user assigned identity.
        :param str principal_id: The principal id of user assigned identity.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The client id of user assigned identity.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal id of user assigned identity.
        """
        return pulumi.get(self, "principal_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class OnErrorDeploymentExtendedResponse(dict):
    """
    Deployment on error behavior with additional details.
    """
    def __init__(__self__, *,
                 provisioning_state: str,
                 deployment_name: Optional[str] = None,
                 type: Optional[str] = None):
        """
        Deployment on error behavior with additional details.
        :param str provisioning_state: The state of the provisioning for the on error deployment.
        :param str deployment_name: The deployment to be used on error case.
        :param str type: The deployment on error behavior type. Possible values are LastSuccessful and SpecificDeployment.
        """
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if deployment_name is not None:
            pulumi.set(__self__, "deployment_name", deployment_name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The state of the provisioning for the on error deployment.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="deploymentName")
    def deployment_name(self) -> Optional[str]:
        """
        The deployment to be used on error case.
        """
        return pulumi.get(self, "deployment_name")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The deployment on error behavior type. Possible values are LastSuccessful and SpecificDeployment.
        """
        return pulumi.get(self, "type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ParametersLinkResponse(dict):
    """
    Entity representing the reference to the deployment parameters.
    """
    def __init__(__self__, *,
                 uri: str,
                 content_version: Optional[str] = None):
        """
        Entity representing the reference to the deployment parameters.
        :param str uri: The URI of the parameters file.
        :param str content_version: If included, must match the ContentVersion in the template.
        """
        pulumi.set(__self__, "uri", uri)
        if content_version is not None:
            pulumi.set(__self__, "content_version", content_version)

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        The URI of the parameters file.
        """
        return pulumi.get(self, "uri")

    @property
    @pulumi.getter(name="contentVersion")
    def content_version(self) -> Optional[str]:
        """
        If included, must match the ContentVersion in the template.
        """
        return pulumi.get(self, "content_version")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class PlanResponse(dict):
    """
    Plan for the resource.
    """
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 product: Optional[str] = None,
                 promotion_code: Optional[str] = None,
                 publisher: Optional[str] = None,
                 version: Optional[str] = None):
        """
        Plan for the resource.
        :param str name: The plan ID.
        :param str product: The offer ID.
        :param str promotion_code: The promotion code.
        :param str publisher: The publisher ID.
        :param str version: The plan's version.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if product is not None:
            pulumi.set(__self__, "product", product)
        if promotion_code is not None:
            pulumi.set(__self__, "promotion_code", promotion_code)
        if publisher is not None:
            pulumi.set(__self__, "publisher", publisher)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The plan ID.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def product(self) -> Optional[str]:
        """
        The offer ID.
        """
        return pulumi.get(self, "product")

    @property
    @pulumi.getter(name="promotionCode")
    def promotion_code(self) -> Optional[str]:
        """
        The promotion code.
        """
        return pulumi.get(self, "promotion_code")

    @property
    @pulumi.getter
    def publisher(self) -> Optional[str]:
        """
        The publisher ID.
        """
        return pulumi.get(self, "publisher")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        The plan's version.
        """
        return pulumi.get(self, "version")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ProviderResourceTypeResponse(dict):
    """
    Resource type managed by the resource provider.
    """
    def __init__(__self__, *,
                 aliases: Optional[Sequence['outputs.AliasTypeResponse']] = None,
                 api_versions: Optional[Sequence[str]] = None,
                 capabilities: Optional[str] = None,
                 locations: Optional[Sequence[str]] = None,
                 properties: Optional[Mapping[str, str]] = None,
                 resource_type: Optional[str] = None):
        """
        Resource type managed by the resource provider.
        :param Sequence['AliasTypeResponseArgs'] aliases: The aliases that are supported by this resource type.
        :param Sequence[str] api_versions: The API version.
        :param str capabilities: The additional capabilities offered by this resource type.
        :param Sequence[str] locations: The collection of locations where this resource type can be created.
        :param Mapping[str, str] properties: The properties.
        :param str resource_type: The resource type.
        """
        if aliases is not None:
            pulumi.set(__self__, "aliases", aliases)
        if api_versions is not None:
            pulumi.set(__self__, "api_versions", api_versions)
        if capabilities is not None:
            pulumi.set(__self__, "capabilities", capabilities)
        if locations is not None:
            pulumi.set(__self__, "locations", locations)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter
    def aliases(self) -> Optional[Sequence['outputs.AliasTypeResponse']]:
        """
        The aliases that are supported by this resource type.
        """
        return pulumi.get(self, "aliases")

    @property
    @pulumi.getter(name="apiVersions")
    def api_versions(self) -> Optional[Sequence[str]]:
        """
        The API version.
        """
        return pulumi.get(self, "api_versions")

    @property
    @pulumi.getter
    def capabilities(self) -> Optional[str]:
        """
        The additional capabilities offered by this resource type.
        """
        return pulumi.get(self, "capabilities")

    @property
    @pulumi.getter
    def locations(self) -> Optional[Sequence[str]]:
        """
        The collection of locations where this resource type can be created.
        """
        return pulumi.get(self, "locations")

    @property
    @pulumi.getter
    def properties(self) -> Optional[Mapping[str, str]]:
        """
        The properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "resource_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ProviderResponse(dict):
    """
    Resource provider information.
    """
    def __init__(__self__, *,
                 id: str,
                 registration_policy: str,
                 registration_state: str,
                 resource_types: Sequence['outputs.ProviderResourceTypeResponse'],
                 namespace: Optional[str] = None):
        """
        Resource provider information.
        :param str id: The provider ID.
        :param str registration_policy: The registration policy of the resource provider.
        :param str registration_state: The registration state of the resource provider.
        :param Sequence['ProviderResourceTypeResponseArgs'] resource_types: The collection of provider resource types.
        :param str namespace: The namespace of the resource provider.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "registration_policy", registration_policy)
        pulumi.set(__self__, "registration_state", registration_state)
        pulumi.set(__self__, "resource_types", resource_types)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="registrationPolicy")
    def registration_policy(self) -> str:
        """
        The registration policy of the resource provider.
        """
        return pulumi.get(self, "registration_policy")

    @property
    @pulumi.getter(name="registrationState")
    def registration_state(self) -> str:
        """
        The registration state of the resource provider.
        """
        return pulumi.get(self, "registration_state")

    @property
    @pulumi.getter(name="resourceTypes")
    def resource_types(self) -> Sequence['outputs.ProviderResourceTypeResponse']:
        """
        The collection of provider resource types.
        """
        return pulumi.get(self, "resource_types")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        """
        The namespace of the resource provider.
        """
        return pulumi.get(self, "namespace")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ResourceGroupPropertiesResponse(dict):
    """
    The resource group properties.
    """
    def __init__(__self__, *,
                 provisioning_state: str):
        """
        The resource group properties.
        :param str provisioning_state: The provisioning state. 
        """
        pulumi.set(__self__, "provisioning_state", provisioning_state)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state. 
        """
        return pulumi.get(self, "provisioning_state")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SkuResponse(dict):
    """
    SKU for the resource.
    """
    def __init__(__self__, *,
                 capacity: Optional[int] = None,
                 family: Optional[str] = None,
                 model: Optional[str] = None,
                 name: Optional[str] = None,
                 size: Optional[str] = None,
                 tier: Optional[str] = None):
        """
        SKU for the resource.
        :param int capacity: The SKU capacity.
        :param str family: The SKU family.
        :param str model: The SKU model.
        :param str name: The SKU name.
        :param str size: The SKU size.
        :param str tier: The SKU tier.
        """
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if model is not None:
            pulumi.set(__self__, "model", model)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        The SKU capacity.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def family(self) -> Optional[str]:
        """
        The SKU family.
        """
        return pulumi.get(self, "family")

    @property
    @pulumi.getter
    def model(self) -> Optional[str]:
        """
        The SKU model.
        """
        return pulumi.get(self, "model")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The SKU name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def size(self) -> Optional[str]:
        """
        The SKU size.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def tier(self) -> Optional[str]:
        """
        The SKU tier.
        """
        return pulumi.get(self, "tier")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class TemplateLinkResponse(dict):
    """
    Entity representing the reference to the template.
    """
    def __init__(__self__, *,
                 uri: str,
                 content_version: Optional[str] = None):
        """
        Entity representing the reference to the template.
        :param str uri: The URI of the template to deploy.
        :param str content_version: If included, must match the ContentVersion in the template.
        """
        pulumi.set(__self__, "uri", uri)
        if content_version is not None:
            pulumi.set(__self__, "content_version", content_version)

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        The URI of the template to deploy.
        """
        return pulumi.get(self, "uri")

    @property
    @pulumi.getter(name="contentVersion")
    def content_version(self) -> Optional[str]:
        """
        If included, must match the ContentVersion in the template.
        """
        return pulumi.get(self, "content_version")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


