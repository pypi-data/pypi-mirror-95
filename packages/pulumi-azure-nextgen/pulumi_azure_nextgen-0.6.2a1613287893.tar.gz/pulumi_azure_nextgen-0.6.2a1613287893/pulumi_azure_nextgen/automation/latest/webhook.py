# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['Webhook']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:automation:Webhook'.""", DeprecationWarning)


class Webhook(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:automation:Webhook'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 expiry_time: Optional[pulumi.Input[str]] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 run_on: Optional[pulumi.Input[str]] = None,
                 runbook: Optional[pulumi.Input[pulumi.InputType['RunbookAssociationPropertyArgs']]] = None,
                 uri: Optional[pulumi.Input[str]] = None,
                 webhook_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Definition of the webhook type.
        Latest API Version: 2015-10-31.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account.
        :param pulumi.Input[str] expiry_time: Gets or sets the expiry time.
        :param pulumi.Input[bool] is_enabled: Gets or sets the value of the enabled flag of webhook.
        :param pulumi.Input[str] name: Gets or sets the name of the webhook.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] parameters: Gets or sets the parameters of the job.
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
        :param pulumi.Input[str] run_on: Gets or sets the name of the hybrid worker group the webhook job will run on.
        :param pulumi.Input[pulumi.InputType['RunbookAssociationPropertyArgs']] runbook: Gets or sets the runbook.
        :param pulumi.Input[str] uri: Gets or sets the uri.
        :param pulumi.Input[str] webhook_name: The webhook name.
        """
        pulumi.log.warn("Webhook is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:automation:Webhook'.")
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

            if automation_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'automation_account_name'")
            __props__['automation_account_name'] = automation_account_name
            __props__['expiry_time'] = expiry_time
            __props__['is_enabled'] = is_enabled
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            __props__['parameters'] = parameters
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['run_on'] = run_on
            __props__['runbook'] = runbook
            __props__['uri'] = uri
            if webhook_name is None and not opts.urn:
                raise TypeError("Missing required property 'webhook_name'")
            __props__['webhook_name'] = webhook_name
            __props__['creation_time'] = None
            __props__['description'] = None
            __props__['last_invoked_time'] = None
            __props__['last_modified_by'] = None
            __props__['last_modified_time'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:automation:Webhook"), pulumi.Alias(type_="azure-nextgen:automation/v20151031:Webhook")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Webhook, __self__).__init__(
            'azure-nextgen:automation/latest:Webhook',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Webhook':
        """
        Get an existing Webhook resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Webhook(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="expiryTime")
    def expiry_time(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the expiry time.
        """
        return pulumi.get(self, "expiry_time")

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Gets or sets the value of the enabled flag of the webhook.
        """
        return pulumi.get(self, "is_enabled")

    @property
    @pulumi.getter(name="lastInvokedTime")
    def last_invoked_time(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the last invoked time.
        """
        return pulumi.get(self, "last_invoked_time")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> pulumi.Output[Optional[str]]:
        """
        Details of the user who last modified the Webhook
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Gets or sets the parameters of the job that is created when the webhook calls the runbook it is associated with.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="runOn")
    def run_on(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the name of the hybrid worker group the webhook job will run on.
        """
        return pulumi.get(self, "run_on")

    @property
    @pulumi.getter
    def runbook(self) -> pulumi.Output[Optional['outputs.RunbookAssociationPropertyResponse']]:
        """
        Gets or sets the runbook the webhook is associated with.
        """
        return pulumi.get(self, "runbook")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the webhook uri.
        """
        return pulumi.get(self, "uri")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

