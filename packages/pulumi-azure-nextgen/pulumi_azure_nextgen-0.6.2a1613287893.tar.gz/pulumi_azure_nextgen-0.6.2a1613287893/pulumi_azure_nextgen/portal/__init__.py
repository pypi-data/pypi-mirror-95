# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .console import *
from .console_with_location import *
from .dashboard import *
from .get_console import *
from .get_console_with_location import *
from .get_dashboard import *
from .get_tenant_configuration import *
from .get_user_settings import *
from .get_user_settings_with_location import *
from .list_list_tenant_configuration_violation import *
from .tenant_configuration import *
from .user_settings import *
from .user_settings_with_location import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    latest,
    v20150801preview,
    v20181001,
    v20181001preview,
    v20190101preview,
    v20200901preview,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:portal:Console":
                return Console(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:portal:ConsoleWithLocation":
                return ConsoleWithLocation(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:portal:Dashboard":
                return Dashboard(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:portal:TenantConfiguration":
                return TenantConfiguration(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:portal:UserSettings":
                return UserSettings(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:portal:UserSettingsWithLocation":
                return UserSettingsWithLocation(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "portal", _module_instance)

_register_module()
