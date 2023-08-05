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

__all__ = ['Experiment']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:network:Experiment'.""", DeprecationWarning)


class Experiment(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:network:Experiment'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled_state: Optional[pulumi.Input[Union[str, 'State']]] = None,
                 endpoint_a: Optional[pulumi.Input[pulumi.InputType['EndpointArgs']]] = None,
                 endpoint_b: Optional[pulumi.Input[pulumi.InputType['EndpointArgs']]] = None,
                 experiment_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 profile_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Defines the properties of an Experiment
        Latest API Version: 2019-11-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the details or intents of the Experiment
        :param pulumi.Input[Union[str, 'State']] enabled_state: The state of the Experiment
        :param pulumi.Input[pulumi.InputType['EndpointArgs']] endpoint_a: The endpoint A of an experiment
        :param pulumi.Input[pulumi.InputType['EndpointArgs']] endpoint_b: The endpoint B of an experiment
        :param pulumi.Input[str] experiment_name: The Experiment identifier associated with the Experiment
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] profile_name: The Profile identifier associated with the Tenant and Partner
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.log.warn("Experiment is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:network:Experiment'.")
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
            __props__['enabled_state'] = enabled_state
            __props__['endpoint_a'] = endpoint_a
            __props__['endpoint_b'] = endpoint_b
            if experiment_name is None and not opts.urn:
                raise TypeError("Missing required property 'experiment_name'")
            __props__['experiment_name'] = experiment_name
            __props__['location'] = location
            if profile_name is None and not opts.urn:
                raise TypeError("Missing required property 'profile_name'")
            __props__['profile_name'] = profile_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['name'] = None
            __props__['resource_state'] = None
            __props__['script_file_uri'] = None
            __props__['status'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network:Experiment"), pulumi.Alias(type_="azure-nextgen:network/v20191101:Experiment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Experiment, __self__).__init__(
            'azure-nextgen:network/latest:Experiment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Experiment':
        """
        Get an existing Experiment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Experiment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the details or intents of the Experiment
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enabledState")
    def enabled_state(self) -> pulumi.Output[Optional[str]]:
        """
        The state of the Experiment
        """
        return pulumi.get(self, "enabled_state")

    @property
    @pulumi.getter(name="endpointA")
    def endpoint_a(self) -> pulumi.Output[Optional['outputs.EndpointResponse']]:
        """
        The endpoint A of an experiment
        """
        return pulumi.get(self, "endpoint_a")

    @property
    @pulumi.getter(name="endpointB")
    def endpoint_b(self) -> pulumi.Output[Optional['outputs.EndpointResponse']]:
        """
        The endpoint B of an experiment
        """
        return pulumi.get(self, "endpoint_b")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> pulumi.Output[str]:
        """
        Resource status.
        """
        return pulumi.get(self, "resource_state")

    @property
    @pulumi.getter(name="scriptFileUri")
    def script_file_uri(self) -> pulumi.Output[str]:
        """
        The uri to the Script used in the Experiment
        """
        return pulumi.get(self, "script_file_uri")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The description of Experiment status from the server side
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

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

