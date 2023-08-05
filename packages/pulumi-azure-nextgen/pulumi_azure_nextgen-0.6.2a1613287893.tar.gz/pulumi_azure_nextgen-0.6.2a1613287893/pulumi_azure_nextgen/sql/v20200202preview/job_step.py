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

__all__ = ['JobStep']


class JobStep(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[pulumi.InputType['JobStepActionArgs']]] = None,
                 credential: Optional[pulumi.Input[str]] = None,
                 execution_options: Optional[pulumi.Input[pulumi.InputType['JobStepExecutionOptionsArgs']]] = None,
                 job_agent_name: Optional[pulumi.Input[str]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 output: Optional[pulumi.Input[pulumi.InputType['JobStepOutputArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 step_id: Optional[pulumi.Input[int]] = None,
                 step_name: Optional[pulumi.Input[str]] = None,
                 target_group: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A job step.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['JobStepActionArgs']] action: The action payload of the job step.
        :param pulumi.Input[str] credential: The resource ID of the job credential that will be used to connect to the targets.
        :param pulumi.Input[pulumi.InputType['JobStepExecutionOptionsArgs']] execution_options: Execution options for the job step.
        :param pulumi.Input[str] job_agent_name: The name of the job agent.
        :param pulumi.Input[str] job_name: The name of the job.
        :param pulumi.Input[pulumi.InputType['JobStepOutputArgs']] output: Output destination properties of the job step.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[int] step_id: The job step's index within the job. If not specified when creating the job step, it will be created as the last step. If not specified when updating the job step, the step id is not modified.
        :param pulumi.Input[str] step_name: The name of the job step.
        :param pulumi.Input[str] target_group: The resource ID of the target group that the job step will be executed on.
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

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__['action'] = action
            if credential is None and not opts.urn:
                raise TypeError("Missing required property 'credential'")
            __props__['credential'] = credential
            __props__['execution_options'] = execution_options
            if job_agent_name is None and not opts.urn:
                raise TypeError("Missing required property 'job_agent_name'")
            __props__['job_agent_name'] = job_agent_name
            if job_name is None and not opts.urn:
                raise TypeError("Missing required property 'job_name'")
            __props__['job_name'] = job_name
            __props__['output'] = output
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__['server_name'] = server_name
            __props__['step_id'] = step_id
            if step_name is None and not opts.urn:
                raise TypeError("Missing required property 'step_name'")
            __props__['step_name'] = step_name
            if target_group is None and not opts.urn:
                raise TypeError("Missing required property 'target_group'")
            __props__['target_group'] = target_group
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql:JobStep"), pulumi.Alias(type_="azure-nextgen:sql/v20170301preview:JobStep"), pulumi.Alias(type_="azure-nextgen:sql/v20200801preview:JobStep")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(JobStep, __self__).__init__(
            'azure-nextgen:sql/v20200202preview:JobStep',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'JobStep':
        """
        Get an existing JobStep resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return JobStep(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output['outputs.JobStepActionResponse']:
        """
        The action payload of the job step.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def credential(self) -> pulumi.Output[str]:
        """
        The resource ID of the job credential that will be used to connect to the targets.
        """
        return pulumi.get(self, "credential")

    @property
    @pulumi.getter(name="executionOptions")
    def execution_options(self) -> pulumi.Output[Optional['outputs.JobStepExecutionOptionsResponse']]:
        """
        Execution options for the job step.
        """
        return pulumi.get(self, "execution_options")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def output(self) -> pulumi.Output[Optional['outputs.JobStepOutputResponse']]:
        """
        Output destination properties of the job step.
        """
        return pulumi.get(self, "output")

    @property
    @pulumi.getter(name="stepId")
    def step_id(self) -> pulumi.Output[Optional[int]]:
        """
        The job step's index within the job. If not specified when creating the job step, it will be created as the last step. If not specified when updating the job step, the step id is not modified.
        """
        return pulumi.get(self, "step_id")

    @property
    @pulumi.getter(name="targetGroup")
    def target_group(self) -> pulumi.Output[str]:
        """
        The resource ID of the target group that the job step will be executed on.
        """
        return pulumi.get(self, "target_group")

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

