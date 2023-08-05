# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .environment import *
from .environment_setting import *
from .gallery_image import *
from .get_environment import *
from .get_environment_setting import *
from .get_gallery_image import *
from .get_global_user_environment import *
from .get_global_user_operation_batch_status import *
from .get_global_user_operation_status import *
from .get_global_user_personal_preferences import *
from .get_lab import *
from .get_lab_account import *
from .get_lab_account_regional_availability import *
from .get_user import *
from .lab import *
from .lab_account import *
from .list_global_user_environments import *
from .list_global_user_labs import *
from .user import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from ... import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:labservices/latest:Environment":
                return Environment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:labservices/latest:EnvironmentSetting":
                return EnvironmentSetting(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:labservices/latest:GalleryImage":
                return GalleryImage(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:labservices/latest:Lab":
                return Lab(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:labservices/latest:LabAccount":
                return LabAccount(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:labservices/latest:User":
                return User(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "labservices/latest", _module_instance)

_register_module()
