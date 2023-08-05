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
from ._inputs import *

__all__ = ['Link']


class Link(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 display_name: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 hub_name: Optional[pulumi.Input[str]] = None,
                 link_name: Optional[pulumi.Input[str]] = None,
                 mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TypePropertiesMappingArgs']]]]] = None,
                 operation_type: Optional[pulumi.Input['InstanceOperationType']] = None,
                 participant_property_references: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ParticipantPropertyReferenceArgs']]]]] = None,
                 reference_only: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 source_entity_type: Optional[pulumi.Input['EntityType']] = None,
                 source_entity_type_name: Optional[pulumi.Input[str]] = None,
                 target_entity_type: Optional[pulumi.Input['EntityType']] = None,
                 target_entity_type_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The link resource format.
        API Version: 2017-04-26.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] description: Localized descriptions for the Link.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] display_name: Localized display name for the Link.
        :param pulumi.Input[str] hub_name: The name of the hub.
        :param pulumi.Input[str] link_name: The name of the link.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TypePropertiesMappingArgs']]]] mappings: The set of properties mappings between the source and target Types.
        :param pulumi.Input['InstanceOperationType'] operation_type: Determines whether this link is supposed to create or delete instances if Link is NOT Reference Only.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ParticipantPropertyReferenceArgs']]]] participant_property_references: The properties that represent the participating profile.
        :param pulumi.Input[bool] reference_only: Indicating whether the link is reference only link. This flag is ignored if the Mappings are defined. If the mappings are not defined and it is set to true, links processing will not create or update profiles.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['EntityType'] source_entity_type: Type of source entity.
        :param pulumi.Input[str] source_entity_type_name: Name of the source Entity Type.
        :param pulumi.Input['EntityType'] target_entity_type: Type of target entity.
        :param pulumi.Input[str] target_entity_type_name: Name of the target Entity Type.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['description'] = description
            __props__['display_name'] = display_name
            if hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'hub_name'")
            __props__['hub_name'] = hub_name
            if link_name is None and not opts.urn:
                raise TypeError("Missing required property 'link_name'")
            __props__['link_name'] = link_name
            __props__['mappings'] = mappings
            __props__['operation_type'] = operation_type
            if participant_property_references is None and not opts.urn:
                raise TypeError("Missing required property 'participant_property_references'")
            __props__['participant_property_references'] = participant_property_references
            __props__['reference_only'] = reference_only
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if source_entity_type is None and not opts.urn:
                raise TypeError("Missing required property 'source_entity_type'")
            __props__['source_entity_type'] = source_entity_type
            if source_entity_type_name is None and not opts.urn:
                raise TypeError("Missing required property 'source_entity_type_name'")
            __props__['source_entity_type_name'] = source_entity_type_name
            if target_entity_type is None and not opts.urn:
                raise TypeError("Missing required property 'target_entity_type'")
            __props__['target_entity_type'] = target_entity_type
            if target_entity_type_name is None and not opts.urn:
                raise TypeError("Missing required property 'target_entity_type_name'")
            __props__['target_entity_type_name'] = target_entity_type_name
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['tenant_id'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:customerinsights/latest:Link"), pulumi.Alias(type_="azure-nextgen:customerinsights/v20170101:Link"), pulumi.Alias(type_="azure-nextgen:customerinsights/v20170426:Link")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Link, __self__).__init__(
            'azure-nextgen:customerinsights:Link',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Link':
        """
        Get an existing Link resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Link(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Localized descriptions for the Link.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Localized display name for the Link.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="linkName")
    def link_name(self) -> pulumi.Output[str]:
        """
        The link name.
        """
        return pulumi.get(self, "link_name")

    @property
    @pulumi.getter
    def mappings(self) -> pulumi.Output[Optional[Sequence['outputs.TypePropertiesMappingResponse']]]:
        """
        The set of properties mappings between the source and target Types.
        """
        return pulumi.get(self, "mappings")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="operationType")
    def operation_type(self) -> pulumi.Output[Optional[str]]:
        """
        Determines whether this link is supposed to create or delete instances if Link is NOT Reference Only.
        """
        return pulumi.get(self, "operation_type")

    @property
    @pulumi.getter(name="participantPropertyReferences")
    def participant_property_references(self) -> pulumi.Output[Sequence['outputs.ParticipantPropertyReferenceResponse']]:
        """
        The properties that represent the participating profile.
        """
        return pulumi.get(self, "participant_property_references")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="referenceOnly")
    def reference_only(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicating whether the link is reference only link. This flag is ignored if the Mappings are defined. If the mappings are not defined and it is set to true, links processing will not create or update profiles.
        """
        return pulumi.get(self, "reference_only")

    @property
    @pulumi.getter(name="sourceEntityType")
    def source_entity_type(self) -> pulumi.Output[str]:
        """
        Type of source entity.
        """
        return pulumi.get(self, "source_entity_type")

    @property
    @pulumi.getter(name="sourceEntityTypeName")
    def source_entity_type_name(self) -> pulumi.Output[str]:
        """
        Name of the source Entity Type.
        """
        return pulumi.get(self, "source_entity_type_name")

    @property
    @pulumi.getter(name="targetEntityType")
    def target_entity_type(self) -> pulumi.Output[str]:
        """
        Type of target entity.
        """
        return pulumi.get(self, "target_entity_type")

    @property
    @pulumi.getter(name="targetEntityTypeName")
    def target_entity_type_name(self) -> pulumi.Output[str]:
        """
        Name of the target Entity Type.
        """
        return pulumi.get(self, "target_entity_type_name")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[str]:
        """
        The hub name.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

