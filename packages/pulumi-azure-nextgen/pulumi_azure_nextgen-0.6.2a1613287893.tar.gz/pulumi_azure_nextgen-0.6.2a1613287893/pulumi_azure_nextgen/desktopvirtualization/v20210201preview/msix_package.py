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

__all__ = ['MSIXPackage']


class MSIXPackage(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 host_pool_name: Optional[pulumi.Input[str]] = None,
                 image_path: Optional[pulumi.Input[str]] = None,
                 is_active: Optional[pulumi.Input[bool]] = None,
                 is_regular_registration: Optional[pulumi.Input[bool]] = None,
                 last_updated: Optional[pulumi.Input[str]] = None,
                 msix_package_full_name: Optional[pulumi.Input[str]] = None,
                 package_applications: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MsixPackageApplicationsArgs']]]]] = None,
                 package_dependencies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MsixPackageDependenciesArgs']]]]] = None,
                 package_family_name: Optional[pulumi.Input[str]] = None,
                 package_name: Optional[pulumi.Input[str]] = None,
                 package_relative_path: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Schema for MSIX Package properties.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: User friendly Name to be displayed in the portal. 
        :param pulumi.Input[str] host_pool_name: The name of the host pool within the specified resource group
        :param pulumi.Input[str] image_path: VHD/CIM image path on Network Share.
        :param pulumi.Input[bool] is_active: Make this version of the package the active one across the hostpool. 
        :param pulumi.Input[bool] is_regular_registration: Specifies how to register Package in feed.
        :param pulumi.Input[str] last_updated: Date Package was last updated, found in the appxmanifest.xml. 
        :param pulumi.Input[str] msix_package_full_name: The version specific package full name of the MSIX package within specified hostpool
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MsixPackageApplicationsArgs']]]] package_applications: List of package applications. 
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MsixPackageDependenciesArgs']]]] package_dependencies: List of package dependencies. 
        :param pulumi.Input[str] package_family_name: Package Family Name from appxmanifest.xml. Contains Package Name and Publisher name. 
        :param pulumi.Input[str] package_name: Package Name from appxmanifest.xml. 
        :param pulumi.Input[str] package_relative_path: Relative Path to the package inside the image. 
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] version: Package Version found in the appxmanifest.xml. 
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

            __props__['display_name'] = display_name
            if host_pool_name is None and not opts.urn:
                raise TypeError("Missing required property 'host_pool_name'")
            __props__['host_pool_name'] = host_pool_name
            __props__['image_path'] = image_path
            __props__['is_active'] = is_active
            __props__['is_regular_registration'] = is_regular_registration
            __props__['last_updated'] = last_updated
            if msix_package_full_name is None and not opts.urn:
                raise TypeError("Missing required property 'msix_package_full_name'")
            __props__['msix_package_full_name'] = msix_package_full_name
            __props__['package_applications'] = package_applications
            __props__['package_dependencies'] = package_dependencies
            __props__['package_family_name'] = package_family_name
            __props__['package_name'] = package_name
            __props__['package_relative_path'] = package_relative_path
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['version'] = version
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:desktopvirtualization:MSIXPackage"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20200921preview:MSIXPackage"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20201019preview:MSIXPackage"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20201102preview:MSIXPackage"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20201110preview:MSIXPackage"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20210114preview:MSIXPackage")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MSIXPackage, __self__).__init__(
            'azure-nextgen:desktopvirtualization/v20210201preview:MSIXPackage',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MSIXPackage':
        """
        Get an existing MSIXPackage resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return MSIXPackage(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        User friendly Name to be displayed in the portal. 
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="imagePath")
    def image_path(self) -> pulumi.Output[Optional[str]]:
        """
        VHD/CIM image path on Network Share.
        """
        return pulumi.get(self, "image_path")

    @property
    @pulumi.getter(name="isActive")
    def is_active(self) -> pulumi.Output[Optional[bool]]:
        """
        Make this version of the package the active one across the hostpool. 
        """
        return pulumi.get(self, "is_active")

    @property
    @pulumi.getter(name="isRegularRegistration")
    def is_regular_registration(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies how to register Package in feed.
        """
        return pulumi.get(self, "is_regular_registration")

    @property
    @pulumi.getter(name="lastUpdated")
    def last_updated(self) -> pulumi.Output[Optional[str]]:
        """
        Date Package was last updated, found in the appxmanifest.xml. 
        """
        return pulumi.get(self, "last_updated")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="packageApplications")
    def package_applications(self) -> pulumi.Output[Optional[Sequence['outputs.MsixPackageApplicationsResponse']]]:
        """
        List of package applications. 
        """
        return pulumi.get(self, "package_applications")

    @property
    @pulumi.getter(name="packageDependencies")
    def package_dependencies(self) -> pulumi.Output[Optional[Sequence['outputs.MsixPackageDependenciesResponse']]]:
        """
        List of package dependencies. 
        """
        return pulumi.get(self, "package_dependencies")

    @property
    @pulumi.getter(name="packageFamilyName")
    def package_family_name(self) -> pulumi.Output[Optional[str]]:
        """
        Package Family Name from appxmanifest.xml. Contains Package Name and Publisher name. 
        """
        return pulumi.get(self, "package_family_name")

    @property
    @pulumi.getter(name="packageName")
    def package_name(self) -> pulumi.Output[Optional[str]]:
        """
        Package Name from appxmanifest.xml. 
        """
        return pulumi.get(self, "package_name")

    @property
    @pulumi.getter(name="packageRelativePath")
    def package_relative_path(self) -> pulumi.Output[Optional[str]]:
        """
        Relative Path to the package inside the image. 
        """
        return pulumi.get(self, "package_relative_path")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[str]]:
        """
        Package Version found in the appxmanifest.xml. 
        """
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

