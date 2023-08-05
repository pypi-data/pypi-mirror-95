# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .cluster import *
from .data_export import *
from .data_source import *
from .get_cluster import *
from .get_data_export import *
from .get_data_source import *
from .get_linked_service import *
from .get_linked_storage_account import *
from .get_saved_search import *
from .get_storage_insight_config import *
from .get_workspace import *
from .linked_service import *
from .linked_storage_account import *
from .saved_search import *
from .storage_insight_config import *
from .workspace import *
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
            if typ == "azure-nextgen:operationalinsights/v20200301preview:Cluster":
                return Cluster(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:operationalinsights/v20200301preview:DataExport":
                return DataExport(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:operationalinsights/v20200301preview:DataSource":
                return DataSource(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:operationalinsights/v20200301preview:LinkedService":
                return LinkedService(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:operationalinsights/v20200301preview:LinkedStorageAccount":
                return LinkedStorageAccount(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:operationalinsights/v20200301preview:SavedSearch":
                return SavedSearch(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:operationalinsights/v20200301preview:StorageInsightConfig":
                return StorageInsightConfig(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:operationalinsights/v20200301preview:Workspace":
                return Workspace(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "operationalinsights/v20200301preview", _module_instance)

_register_module()
