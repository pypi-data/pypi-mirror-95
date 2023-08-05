# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .data_controller import *
from .get_data_controller import *
from .get_postgres_instance import *
from .get_sql_managed_instance import *
from .get_sql_server import *
from .get_sql_server_instance import *
from .get_sql_server_registration import *
from .postgres_instance import *
from .sql_managed_instance import *
from .sql_server import *
from .sql_server_instance import *
from .sql_server_registration import *
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
            if typ == "azure-nextgen:azuredata/v20190724preview:DataController":
                return DataController(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:azuredata/v20190724preview:PostgresInstance":
                return PostgresInstance(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:azuredata/v20190724preview:SqlManagedInstance":
                return SqlManagedInstance(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:azuredata/v20190724preview:SqlServer":
                return SqlServer(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:azuredata/v20190724preview:SqlServerInstance":
                return SqlServerInstance(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:azuredata/v20190724preview:SqlServerRegistration":
                return SqlServerRegistration(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "azuredata/v20190724preview", _module_instance)

_register_module()
