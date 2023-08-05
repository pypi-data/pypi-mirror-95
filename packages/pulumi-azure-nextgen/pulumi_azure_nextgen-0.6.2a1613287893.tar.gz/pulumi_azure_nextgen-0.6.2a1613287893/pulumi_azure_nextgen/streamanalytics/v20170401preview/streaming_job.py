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

__all__ = ['StreamingJob']


class StreamingJob(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster: Optional[pulumi.Input[pulumi.InputType['ClusterInfoArgs']]] = None,
                 compatibility_level: Optional[pulumi.Input[Union[str, 'CompatibilityLevel']]] = None,
                 content_storage_policy: Optional[pulumi.Input[Union[str, 'ContentStoragePolicy']]] = None,
                 data_locale: Optional[pulumi.Input[str]] = None,
                 events_late_arrival_max_delay_in_seconds: Optional[pulumi.Input[int]] = None,
                 events_out_of_order_max_delay_in_seconds: Optional[pulumi.Input[int]] = None,
                 events_out_of_order_policy: Optional[pulumi.Input[Union[str, 'EventsOutOfOrderPolicy']]] = None,
                 externals: Optional[pulumi.Input[pulumi.InputType['ExternalArgs']]] = None,
                 functions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FunctionArgs']]]]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]] = None,
                 inputs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InputArgs']]]]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 job_storage_account: Optional[pulumi.Input[pulumi.InputType['JobStorageAccountArgs']]] = None,
                 job_type: Optional[pulumi.Input[Union[str, 'JobType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 output_error_policy: Optional[pulumi.Input[Union[str, 'OutputErrorPolicy']]] = None,
                 output_start_mode: Optional[pulumi.Input[Union[str, 'OutputStartMode']]] = None,
                 output_start_time: Optional[pulumi.Input[str]] = None,
                 outputs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OutputArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['StreamingJobSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 transformation: Optional[pulumi.Input[pulumi.InputType['TransformationArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A streaming job object, containing all information associated with the named streaming job.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ClusterInfoArgs']] cluster: The cluster which streaming jobs will run on.
        :param pulumi.Input[Union[str, 'CompatibilityLevel']] compatibility_level: Controls certain runtime behaviors of the streaming job.
        :param pulumi.Input[Union[str, 'ContentStoragePolicy']] content_storage_policy: Valid values are JobStorageAccount and SystemAccount. If set to JobStorageAccount, this requires the user to also specify jobStorageAccount property. .
        :param pulumi.Input[str] data_locale: The data locale of the stream analytics job. Value should be the name of a supported .NET Culture from the set https://msdn.microsoft.com/en-us/library/system.globalization.culturetypes(v=vs.110).aspx. Defaults to 'en-US' if none specified.
        :param pulumi.Input[int] events_late_arrival_max_delay_in_seconds: The maximum tolerable delay in seconds where events arriving late could be included.  Supported range is -1 to 1814399 (20.23:59:59 days) and -1 is used to specify wait indefinitely. If the property is absent, it is interpreted to have a value of -1.
        :param pulumi.Input[int] events_out_of_order_max_delay_in_seconds: The maximum tolerable delay in seconds where out-of-order events can be adjusted to be back in order.
        :param pulumi.Input[Union[str, 'EventsOutOfOrderPolicy']] events_out_of_order_policy: Indicates the policy to apply to events that arrive out of order in the input event stream.
        :param pulumi.Input[pulumi.InputType['ExternalArgs']] externals: The storage account where the custom code artifacts are located.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FunctionArgs']]]] functions: A list of one or more functions for the streaming job. The name property for each function is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        :param pulumi.Input[pulumi.InputType['IdentityArgs']] identity: Describes the system-assigned managed identity assigned to this job that can be used to authenticate with inputs and outputs.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InputArgs']]]] inputs: A list of one or more inputs to the streaming job. The name property for each input is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual input.
        :param pulumi.Input[str] job_name: The name of the streaming job.
        :param pulumi.Input[pulumi.InputType['JobStorageAccountArgs']] job_storage_account: The properties that are associated with an Azure Storage account with MSI
        :param pulumi.Input[Union[str, 'JobType']] job_type: Describes the type of the job. Valid modes are `Cloud` and 'Edge'.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[Union[str, 'OutputErrorPolicy']] output_error_policy: Indicates the policy to apply to events that arrive at the output and cannot be written to the external storage due to being malformed (missing column values, column values of wrong type or size).
        :param pulumi.Input[Union[str, 'OutputStartMode']] output_start_mode: This property should only be utilized when it is desired that the job be started immediately upon creation. Value may be JobStartTime, CustomTime, or LastOutputEventTime to indicate whether the starting point of the output event stream should start whenever the job is started, start at a custom user time stamp specified via the outputStartTime property, or start from the last event output time.
        :param pulumi.Input[str] output_start_time: Value is either an ISO-8601 formatted time stamp that indicates the starting point of the output event stream, or null to indicate that the output event stream will start whenever the streaming job is started. This property must have a value if outputStartMode is set to CustomTime.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OutputArgs']]]] outputs: A list of one or more outputs for the streaming job. The name property for each output is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual output.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[pulumi.InputType['StreamingJobSkuArgs']] sku: Describes the SKU of the streaming job. Required on PUT (CreateOrReplace) requests.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[pulumi.InputType['TransformationArgs']] transformation: Indicates the query and the number of streaming units to use for the streaming job. The name property of the transformation is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
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

            __props__['cluster'] = cluster
            __props__['compatibility_level'] = compatibility_level
            __props__['content_storage_policy'] = content_storage_policy
            __props__['data_locale'] = data_locale
            __props__['events_late_arrival_max_delay_in_seconds'] = events_late_arrival_max_delay_in_seconds
            __props__['events_out_of_order_max_delay_in_seconds'] = events_out_of_order_max_delay_in_seconds
            __props__['events_out_of_order_policy'] = events_out_of_order_policy
            __props__['externals'] = externals
            __props__['functions'] = functions
            __props__['identity'] = identity
            __props__['inputs'] = inputs
            if job_name is None and not opts.urn:
                raise TypeError("Missing required property 'job_name'")
            __props__['job_name'] = job_name
            __props__['job_storage_account'] = job_storage_account
            __props__['job_type'] = job_type
            __props__['location'] = location
            __props__['output_error_policy'] = output_error_policy
            __props__['output_start_mode'] = output_start_mode
            __props__['output_start_time'] = output_start_time
            __props__['outputs'] = outputs
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['transformation'] = transformation
            __props__['created_date'] = None
            __props__['etag'] = None
            __props__['job_id'] = None
            __props__['job_state'] = None
            __props__['last_output_event_time'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:streamanalytics:StreamingJob"), pulumi.Alias(type_="azure-nextgen:streamanalytics/latest:StreamingJob"), pulumi.Alias(type_="azure-nextgen:streamanalytics/v20160301:StreamingJob")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StreamingJob, __self__).__init__(
            'azure-nextgen:streamanalytics/v20170401preview:StreamingJob',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StreamingJob':
        """
        Get an existing StreamingJob resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return StreamingJob(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def cluster(self) -> pulumi.Output[Optional['outputs.ClusterInfoResponse']]:
        """
        The cluster which streaming jobs will run on.
        """
        return pulumi.get(self, "cluster")

    @property
    @pulumi.getter(name="compatibilityLevel")
    def compatibility_level(self) -> pulumi.Output[Optional[str]]:
        """
        Controls certain runtime behaviors of the streaming job.
        """
        return pulumi.get(self, "compatibility_level")

    @property
    @pulumi.getter(name="contentStoragePolicy")
    def content_storage_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Valid values are JobStorageAccount and SystemAccount. If set to JobStorageAccount, this requires the user to also specify jobStorageAccount property. .
        """
        return pulumi.get(self, "content_storage_policy")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> pulumi.Output[str]:
        """
        Value is an ISO-8601 formatted UTC timestamp indicating when the streaming job was created.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="dataLocale")
    def data_locale(self) -> pulumi.Output[Optional[str]]:
        """
        The data locale of the stream analytics job. Value should be the name of a supported .NET Culture from the set https://msdn.microsoft.com/en-us/library/system.globalization.culturetypes(v=vs.110).aspx. Defaults to 'en-US' if none specified.
        """
        return pulumi.get(self, "data_locale")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The current entity tag for the streaming job. This is an opaque string. You can use it to detect whether the resource has changed between requests. You can also use it in the If-Match or If-None-Match headers for write operations for optimistic concurrency.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="eventsLateArrivalMaxDelayInSeconds")
    def events_late_arrival_max_delay_in_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum tolerable delay in seconds where events arriving late could be included.  Supported range is -1 to 1814399 (20.23:59:59 days) and -1 is used to specify wait indefinitely. If the property is absent, it is interpreted to have a value of -1.
        """
        return pulumi.get(self, "events_late_arrival_max_delay_in_seconds")

    @property
    @pulumi.getter(name="eventsOutOfOrderMaxDelayInSeconds")
    def events_out_of_order_max_delay_in_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum tolerable delay in seconds where out-of-order events can be adjusted to be back in order.
        """
        return pulumi.get(self, "events_out_of_order_max_delay_in_seconds")

    @property
    @pulumi.getter(name="eventsOutOfOrderPolicy")
    def events_out_of_order_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates the policy to apply to events that arrive out of order in the input event stream.
        """
        return pulumi.get(self, "events_out_of_order_policy")

    @property
    @pulumi.getter
    def externals(self) -> pulumi.Output[Optional['outputs.ExternalResponse']]:
        """
        The storage account where the custom code artifacts are located.
        """
        return pulumi.get(self, "externals")

    @property
    @pulumi.getter
    def functions(self) -> pulumi.Output[Optional[Sequence['outputs.FunctionResponse']]]:
        """
        A list of one or more functions for the streaming job. The name property for each function is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        """
        return pulumi.get(self, "functions")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityResponse']]:
        """
        Describes the system-assigned managed identity assigned to this job that can be used to authenticate with inputs and outputs.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def inputs(self) -> pulumi.Output[Optional[Sequence['outputs.InputResponse']]]:
        """
        A list of one or more inputs to the streaming job. The name property for each input is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual input.
        """
        return pulumi.get(self, "inputs")

    @property
    @pulumi.getter(name="jobId")
    def job_id(self) -> pulumi.Output[str]:
        """
        A GUID uniquely identifying the streaming job. This GUID is generated upon creation of the streaming job.
        """
        return pulumi.get(self, "job_id")

    @property
    @pulumi.getter(name="jobState")
    def job_state(self) -> pulumi.Output[str]:
        """
        Describes the state of the streaming job.
        """
        return pulumi.get(self, "job_state")

    @property
    @pulumi.getter(name="jobStorageAccount")
    def job_storage_account(self) -> pulumi.Output[Optional['outputs.JobStorageAccountResponse']]:
        """
        The properties that are associated with an Azure Storage account with MSI
        """
        return pulumi.get(self, "job_storage_account")

    @property
    @pulumi.getter(name="jobType")
    def job_type(self) -> pulumi.Output[Optional[str]]:
        """
        Describes the type of the job. Valid modes are `Cloud` and 'Edge'.
        """
        return pulumi.get(self, "job_type")

    @property
    @pulumi.getter(name="lastOutputEventTime")
    def last_output_event_time(self) -> pulumi.Output[str]:
        """
        Value is either an ISO-8601 formatted timestamp indicating the last output event time of the streaming job or null indicating that output has not yet been produced. In case of multiple outputs or multiple streams, this shows the latest value in that set.
        """
        return pulumi.get(self, "last_output_event_time")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outputErrorPolicy")
    def output_error_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates the policy to apply to events that arrive at the output and cannot be written to the external storage due to being malformed (missing column values, column values of wrong type or size).
        """
        return pulumi.get(self, "output_error_policy")

    @property
    @pulumi.getter(name="outputStartMode")
    def output_start_mode(self) -> pulumi.Output[Optional[str]]:
        """
        This property should only be utilized when it is desired that the job be started immediately upon creation. Value may be JobStartTime, CustomTime, or LastOutputEventTime to indicate whether the starting point of the output event stream should start whenever the job is started, start at a custom user time stamp specified via the outputStartTime property, or start from the last event output time.
        """
        return pulumi.get(self, "output_start_mode")

    @property
    @pulumi.getter(name="outputStartTime")
    def output_start_time(self) -> pulumi.Output[Optional[str]]:
        """
        Value is either an ISO-8601 formatted time stamp that indicates the starting point of the output event stream, or null to indicate that the output event stream will start whenever the streaming job is started. This property must have a value if outputStartMode is set to CustomTime.
        """
        return pulumi.get(self, "output_start_time")

    @property
    @pulumi.getter
    def outputs(self) -> pulumi.Output[Optional[Sequence['outputs.OutputResponse']]]:
        """
        A list of one or more outputs for the streaming job. The name property for each output is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual output.
        """
        return pulumi.get(self, "outputs")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Describes the provisioning status of the streaming job.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.StreamingJobSkuResponse']]:
        """
        Describes the SKU of the streaming job. Required on PUT (CreateOrReplace) requests.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def transformation(self) -> pulumi.Output[Optional['outputs.TransformationResponse']]:
        """
        Indicates the query and the number of streaming units to use for the streaming job. The name property of the transformation is required when specifying this property in a PUT request. This property cannot be modify via a PATCH operation. You must use the PATCH API available for the individual transformation.
        """
        return pulumi.get(self, "transformation")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

