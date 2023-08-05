# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .action import *
from .alert_rule import *
from .bookmark import *
from .bookmark_relation import *
from .data_connector import *
from .get_action import *
from .get_alert_rule import *
from .get_bookmark import *
from .get_bookmark_relation import *
from .get_data_connector import *
from .get_entities_get_timeline import *
from .get_entity_insights import *
from .get_incident import *
from .get_incident_comment import *
from .get_incident_relation import *
from .get_product_setting import *
from .get_threat_intelligence_indicator import *
from .get_watchlist import *
from .incident import *
from .incident_comment import *
from .incident_relation import *
from .product_setting import *
from .threat_intelligence_indicator import *
from .watchlist import *
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
            if typ == "azure-nextgen:securityinsights/v20190101preview:Action":
                return Action(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:securityinsights/v20190101preview:AlertRule":
                return AlertRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:securityinsights/v20190101preview:Bookmark":
                return Bookmark(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:securityinsights/v20190101preview:BookmarkRelation":
                return BookmarkRelation(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:securityinsights/v20190101preview:DataConnector":
                return DataConnector(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:securityinsights/v20190101preview:Incident":
                return Incident(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:securityinsights/v20190101preview:IncidentComment":
                return IncidentComment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:securityinsights/v20190101preview:IncidentRelation":
                return IncidentRelation(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:securityinsights/v20190101preview:ProductSetting":
                return ProductSetting(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:securityinsights/v20190101preview:ThreatIntelligenceIndicator":
                return ThreatIntelligenceIndicator(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:securityinsights/v20190101preview:Watchlist":
                return Watchlist(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "securityinsights/v20190101preview", _module_instance)

_register_module()
