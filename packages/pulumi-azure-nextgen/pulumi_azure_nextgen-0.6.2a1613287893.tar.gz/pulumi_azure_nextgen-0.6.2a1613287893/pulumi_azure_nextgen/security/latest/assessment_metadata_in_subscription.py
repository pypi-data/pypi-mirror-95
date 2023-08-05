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
from ._inputs import *

__all__ = ['AssessmentMetadataInSubscription']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:security:AssessmentMetadataInSubscription'.""", DeprecationWarning)


class AssessmentMetadataInSubscription(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:security:AssessmentMetadataInSubscription'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assessment_metadata_name: Optional[pulumi.Input[str]] = None,
                 assessment_type: Optional[pulumi.Input[Union[str, 'AssessmentType']]] = None,
                 category: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'Category']]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 implementation_effort: Optional[pulumi.Input[Union[str, 'ImplementationEffort']]] = None,
                 partner_data: Optional[pulumi.Input[pulumi.InputType['SecurityAssessmentMetadataPartnerDataArgs']]] = None,
                 preview: Optional[pulumi.Input[bool]] = None,
                 remediation_description: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[Union[str, 'Severity']]] = None,
                 threats: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'Threats']]]]] = None,
                 user_impact: Optional[pulumi.Input[Union[str, 'UserImpact']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Security assessment metadata
        Latest API Version: 2020-01-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] assessment_metadata_name: The Assessment Key - Unique key for the assessment type
        :param pulumi.Input[Union[str, 'AssessmentType']] assessment_type: BuiltIn if the assessment based on built-in Azure Policy definition, Custom if the assessment based on custom Azure Policy definition
        :param pulumi.Input[str] description: Human readable description of the assessment
        :param pulumi.Input[str] display_name: User friendly display name of the assessment
        :param pulumi.Input[Union[str, 'ImplementationEffort']] implementation_effort: The implementation effort required to remediate this assessment
        :param pulumi.Input[pulumi.InputType['SecurityAssessmentMetadataPartnerDataArgs']] partner_data: Describes the partner that created the assessment
        :param pulumi.Input[bool] preview: True if this assessment is in preview release status
        :param pulumi.Input[str] remediation_description: Human readable description of what you should do to mitigate this security issue
        :param pulumi.Input[Union[str, 'Severity']] severity: The severity level of the assessment
        :param pulumi.Input[Union[str, 'UserImpact']] user_impact: The user impact of the assessment
        """
        pulumi.log.warn("AssessmentMetadataInSubscription is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:security:AssessmentMetadataInSubscription'.")
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

            if assessment_metadata_name is None and not opts.urn:
                raise TypeError("Missing required property 'assessment_metadata_name'")
            __props__['assessment_metadata_name'] = assessment_metadata_name
            if assessment_type is None and not opts.urn:
                raise TypeError("Missing required property 'assessment_type'")
            __props__['assessment_type'] = assessment_type
            __props__['category'] = category
            __props__['description'] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__['display_name'] = display_name
            __props__['implementation_effort'] = implementation_effort
            __props__['partner_data'] = partner_data
            __props__['preview'] = preview
            __props__['remediation_description'] = remediation_description
            if severity is None and not opts.urn:
                raise TypeError("Missing required property 'severity'")
            __props__['severity'] = severity
            __props__['threats'] = threats
            __props__['user_impact'] = user_impact
            __props__['name'] = None
            __props__['policy_definition_id'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:security:AssessmentMetadataInSubscription"), pulumi.Alias(type_="azure-nextgen:security/v20190101preview:AssessmentMetadataInSubscription"), pulumi.Alias(type_="azure-nextgen:security/v20200101:AssessmentMetadataInSubscription")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AssessmentMetadataInSubscription, __self__).__init__(
            'azure-nextgen:security/latest:AssessmentMetadataInSubscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AssessmentMetadataInSubscription':
        """
        Get an existing AssessmentMetadataInSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return AssessmentMetadataInSubscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="assessmentType")
    def assessment_type(self) -> pulumi.Output[str]:
        """
        BuiltIn if the assessment based on built-in Azure Policy definition, Custom if the assessment based on custom Azure Policy definition
        """
        return pulumi.get(self, "assessment_type")

    @property
    @pulumi.getter
    def category(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "category")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Human readable description of the assessment
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        User friendly display name of the assessment
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="implementationEffort")
    def implementation_effort(self) -> pulumi.Output[Optional[str]]:
        """
        The implementation effort required to remediate this assessment
        """
        return pulumi.get(self, "implementation_effort")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="partnerData")
    def partner_data(self) -> pulumi.Output[Optional['outputs.SecurityAssessmentMetadataPartnerDataResponse']]:
        """
        Describes the partner that created the assessment
        """
        return pulumi.get(self, "partner_data")

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> pulumi.Output[str]:
        """
        Azure resource ID of the policy definition that turns this assessment calculation on
        """
        return pulumi.get(self, "policy_definition_id")

    @property
    @pulumi.getter
    def preview(self) -> pulumi.Output[Optional[bool]]:
        """
        True if this assessment is in preview release status
        """
        return pulumi.get(self, "preview")

    @property
    @pulumi.getter(name="remediationDescription")
    def remediation_description(self) -> pulumi.Output[Optional[str]]:
        """
        Human readable description of what you should do to mitigate this security issue
        """
        return pulumi.get(self, "remediation_description")

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Output[str]:
        """
        The severity level of the assessment
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter
    def threats(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "threats")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userImpact")
    def user_impact(self) -> pulumi.Output[Optional[str]]:
        """
        The user impact of the assessment
        """
        return pulumi.get(self, "user_impact")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

