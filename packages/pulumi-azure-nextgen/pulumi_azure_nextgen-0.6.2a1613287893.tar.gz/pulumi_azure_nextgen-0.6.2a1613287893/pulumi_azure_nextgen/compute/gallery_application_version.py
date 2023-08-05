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

__all__ = ['GalleryApplicationVersion']


class GalleryApplicationVersion(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 gallery_application_name: Optional[pulumi.Input[str]] = None,
                 gallery_application_version_name: Optional[pulumi.Input[str]] = None,
                 gallery_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 publishing_profile: Optional[pulumi.Input[pulumi.InputType['GalleryApplicationVersionPublishingProfileArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Specifies information about the gallery Application Version that you want to create or update.
        API Version: 2020-09-30.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] gallery_application_name: The name of the gallery Application Definition in which the Application Version is to be created.
        :param pulumi.Input[str] gallery_application_version_name: The name of the gallery Application Version to be created. Needs to follow semantic version name pattern: The allowed characters are digit and period. Digits must be within the range of a 32-bit integer. Format: <MajorVersion>.<MinorVersion>.<Patch>
        :param pulumi.Input[str] gallery_name: The name of the Shared Application Gallery in which the Application Definition resides.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[pulumi.InputType['GalleryApplicationVersionPublishingProfileArgs']] publishing_profile: The publishing profile of a gallery image version.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
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

            if gallery_application_name is None and not opts.urn:
                raise TypeError("Missing required property 'gallery_application_name'")
            __props__['gallery_application_name'] = gallery_application_name
            if gallery_application_version_name is None and not opts.urn:
                raise TypeError("Missing required property 'gallery_application_version_name'")
            __props__['gallery_application_version_name'] = gallery_application_version_name
            if gallery_name is None and not opts.urn:
                raise TypeError("Missing required property 'gallery_name'")
            __props__['gallery_name'] = gallery_name
            __props__['location'] = location
            if publishing_profile is None and not opts.urn:
                raise TypeError("Missing required property 'publishing_profile'")
            __props__['publishing_profile'] = publishing_profile
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['replication_status'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:compute/latest:GalleryApplicationVersion"), pulumi.Alias(type_="azure-nextgen:compute/v20190301:GalleryApplicationVersion"), pulumi.Alias(type_="azure-nextgen:compute/v20190701:GalleryApplicationVersion"), pulumi.Alias(type_="azure-nextgen:compute/v20191201:GalleryApplicationVersion"), pulumi.Alias(type_="azure-nextgen:compute/v20200930:GalleryApplicationVersion")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(GalleryApplicationVersion, __self__).__init__(
            'azure-nextgen:compute:GalleryApplicationVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'GalleryApplicationVersion':
        """
        Get an existing GalleryApplicationVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return GalleryApplicationVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publishingProfile")
    def publishing_profile(self) -> pulumi.Output['outputs.GalleryApplicationVersionPublishingProfileResponse']:
        """
        The publishing profile of a gallery image version.
        """
        return pulumi.get(self, "publishing_profile")

    @property
    @pulumi.getter(name="replicationStatus")
    def replication_status(self) -> pulumi.Output['outputs.ReplicationStatusResponse']:
        """
        This is the replication status of the gallery image version.
        """
        return pulumi.get(self, "replication_status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

