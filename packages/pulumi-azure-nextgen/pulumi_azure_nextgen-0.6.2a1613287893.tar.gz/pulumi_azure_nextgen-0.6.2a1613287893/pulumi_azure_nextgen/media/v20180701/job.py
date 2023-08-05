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

__all__ = ['Job']


class Job(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 correlation_data: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 input: Optional[pulumi.Input[Union[pulumi.InputType['JobInputAssetArgs'], pulumi.InputType['JobInputClipArgs'], pulumi.InputType['JobInputHttpArgs'], pulumi.InputType['JobInputsArgs']]]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 outputs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JobOutputAssetArgs']]]]] = None,
                 priority: Optional[pulumi.Input[Union[str, 'Priority']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 transform_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A Job resource type. The progress and state can be obtained by polling a Job or subscribing to events using EventGrid.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The Media Services account name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] correlation_data: Customer provided key, value pairs that will be returned in Job and JobOutput state events.
        :param pulumi.Input[str] description: Optional customer supplied description of the Job.
        :param pulumi.Input[Union[pulumi.InputType['JobInputAssetArgs'], pulumi.InputType['JobInputClipArgs'], pulumi.InputType['JobInputHttpArgs'], pulumi.InputType['JobInputsArgs']]] input: The inputs for the Job.
        :param pulumi.Input[str] job_name: The Job name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JobOutputAssetArgs']]]] outputs: The outputs for the Job.
        :param pulumi.Input[Union[str, 'Priority']] priority: Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default is normal.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the Azure subscription.
        :param pulumi.Input[str] transform_name: The Transform name.
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

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__['account_name'] = account_name
            __props__['correlation_data'] = correlation_data
            __props__['description'] = description
            if input is None and not opts.urn:
                raise TypeError("Missing required property 'input'")
            __props__['input'] = input
            if job_name is None and not opts.urn:
                raise TypeError("Missing required property 'job_name'")
            __props__['job_name'] = job_name
            if outputs is None and not opts.urn:
                raise TypeError("Missing required property 'outputs'")
            __props__['outputs'] = outputs
            __props__['priority'] = priority
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if transform_name is None and not opts.urn:
                raise TypeError("Missing required property 'transform_name'")
            __props__['transform_name'] = transform_name
            __props__['created'] = None
            __props__['end_time'] = None
            __props__['last_modified'] = None
            __props__['name'] = None
            __props__['start_time'] = None
            __props__['state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:media:Job"), pulumi.Alias(type_="azure-nextgen:media/latest:Job"), pulumi.Alias(type_="azure-nextgen:media/v20180330preview:Job"), pulumi.Alias(type_="azure-nextgen:media/v20180601preview:Job"), pulumi.Alias(type_="azure-nextgen:media/v20200501:Job")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Job, __self__).__init__(
            'azure-nextgen:media/v20180701:Job',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Job':
        """
        Get an existing Job resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Job(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="correlationData")
    def correlation_data(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Customer provided key, value pairs that will be returned in Job and JobOutput state events.
        """
        return pulumi.get(self, "correlation_data")

    @property
    @pulumi.getter
    def created(self) -> pulumi.Output[str]:
        """
        The UTC date and time when the Job was created, in 'YYYY-MM-DDThh:mm:ssZ' format.
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Optional customer supplied description of the Job.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[str]:
        """
        The UTC date and time at which this Job finished processing.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def input(self) -> pulumi.Output[Any]:
        """
        The inputs for the Job.
        """
        return pulumi.get(self, "input")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> pulumi.Output[str]:
        """
        The UTC date and time when the Job was last updated, in 'YYYY-MM-DDThh:mm:ssZ' format.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def outputs(self) -> pulumi.Output[Sequence['outputs.JobOutputAssetResponse']]:
        """
        The outputs for the Job.
        """
        return pulumi.get(self, "outputs")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[Optional[str]]:
        """
        Priority with which the job should be processed. Higher priority jobs are processed before lower priority jobs. If not set, the default is normal.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[str]:
        """
        The UTC date and time at which this Job began processing.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the job.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

