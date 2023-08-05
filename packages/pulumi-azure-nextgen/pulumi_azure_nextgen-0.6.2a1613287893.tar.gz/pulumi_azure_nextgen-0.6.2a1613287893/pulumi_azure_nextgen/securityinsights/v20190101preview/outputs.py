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

__all__ = [
    'ActivityTimelineItemResponseResult',
    'BookmarkTimelineItemResponseResult',
    'ClientInfoResponse',
    'EntityInsightItemResponseResult',
    'EntityInsightItemResponseQueryTimeIntervalResult',
    'GetInsightsErrorResponseResult',
    'GetInsightsResultsMetadataResponseResult',
    'IncidentAdditionalDataResponse',
    'IncidentInfoResponse',
    'IncidentLabelResponse',
    'IncidentOwnerInfoResponse',
    'InsightsTableResultResponseResult',
    'InsightsTableResultResponseColumnsResult',
    'SecurityAlertTimelineItemResponseResult',
    'TimelineAggregationResponseResult',
    'TimelineErrorResponseResult',
    'TimelineResultsMetadataResponseResult',
    'UserInfoResponse',
]

@pulumi.output_type
class ActivityTimelineItemResponseResult(dict):
    """
    Represents Activity timeline item.
    """
    def __init__(__self__, *,
                 bucket_end_time_utc: str,
                 bucket_start_time_utc: str,
                 content: str,
                 first_activity_time_utc: str,
                 kind: str,
                 last_activity_time_utc: str,
                 query_id: str,
                 title: str):
        """
        Represents Activity timeline item.
        :param str bucket_end_time_utc: The grouping bucket end time.
        :param str bucket_start_time_utc: The grouping bucket start time.
        :param str content: The activity timeline content.
        :param str first_activity_time_utc: The time of the first activity in the grouping bucket.
        :param str kind: The entity query kind type.
               Expected value is 'Activity'.
        :param str last_activity_time_utc: The time of the last activity in the grouping bucket.
        :param str query_id: The activity query id.
        :param str title: The activity timeline title.
        """
        pulumi.set(__self__, "bucket_end_time_utc", bucket_end_time_utc)
        pulumi.set(__self__, "bucket_start_time_utc", bucket_start_time_utc)
        pulumi.set(__self__, "content", content)
        pulumi.set(__self__, "first_activity_time_utc", first_activity_time_utc)
        pulumi.set(__self__, "kind", 'Activity')
        pulumi.set(__self__, "last_activity_time_utc", last_activity_time_utc)
        pulumi.set(__self__, "query_id", query_id)
        pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter(name="bucketEndTimeUTC")
    def bucket_end_time_utc(self) -> str:
        """
        The grouping bucket end time.
        """
        return pulumi.get(self, "bucket_end_time_utc")

    @property
    @pulumi.getter(name="bucketStartTimeUTC")
    def bucket_start_time_utc(self) -> str:
        """
        The grouping bucket start time.
        """
        return pulumi.get(self, "bucket_start_time_utc")

    @property
    @pulumi.getter
    def content(self) -> str:
        """
        The activity timeline content.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="firstActivityTimeUTC")
    def first_activity_time_utc(self) -> str:
        """
        The time of the first activity in the grouping bucket.
        """
        return pulumi.get(self, "first_activity_time_utc")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The entity query kind type.
        Expected value is 'Activity'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastActivityTimeUTC")
    def last_activity_time_utc(self) -> str:
        """
        The time of the last activity in the grouping bucket.
        """
        return pulumi.get(self, "last_activity_time_utc")

    @property
    @pulumi.getter(name="queryId")
    def query_id(self) -> str:
        """
        The activity query id.
        """
        return pulumi.get(self, "query_id")

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        The activity timeline title.
        """
        return pulumi.get(self, "title")


@pulumi.output_type
class BookmarkTimelineItemResponseResult(dict):
    """
    Represents bookmark timeline item.
    """
    def __init__(__self__, *,
                 azure_resource_id: str,
                 created_by: 'outputs.UserInfoResponse',
                 display_name: str,
                 end_time_utc: str,
                 kind: str,
                 labels: Sequence[str],
                 notes: str,
                 start_time_utc: str,
                 event_time: Optional[str] = None):
        """
        Represents bookmark timeline item.
        :param str azure_resource_id: The bookmark azure resource id.
        :param 'UserInfoResponseArgs' created_by: Describes a user that created the bookmark
        :param str display_name: The bookmark display name.
        :param str end_time_utc: The bookmark end time.
        :param str kind: The entity query kind type.
               Expected value is 'Bookmark'.
        :param Sequence[str] labels: List of labels relevant to this bookmark
        :param str notes: The notes of the bookmark
        :param str start_time_utc: TThe bookmark start time.
        :param str event_time: The bookmark event time.
        """
        pulumi.set(__self__, "azure_resource_id", azure_resource_id)
        pulumi.set(__self__, "created_by", created_by)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "end_time_utc", end_time_utc)
        pulumi.set(__self__, "kind", 'Bookmark')
        pulumi.set(__self__, "labels", labels)
        pulumi.set(__self__, "notes", notes)
        pulumi.set(__self__, "start_time_utc", start_time_utc)
        if event_time is not None:
            pulumi.set(__self__, "event_time", event_time)

    @property
    @pulumi.getter(name="azureResourceId")
    def azure_resource_id(self) -> str:
        """
        The bookmark azure resource id.
        """
        return pulumi.get(self, "azure_resource_id")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> 'outputs.UserInfoResponse':
        """
        Describes a user that created the bookmark
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The bookmark display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="endTimeUtc")
    def end_time_utc(self) -> str:
        """
        The bookmark end time.
        """
        return pulumi.get(self, "end_time_utc")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The entity query kind type.
        Expected value is 'Bookmark'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def labels(self) -> Sequence[str]:
        """
        List of labels relevant to this bookmark
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def notes(self) -> str:
        """
        The notes of the bookmark
        """
        return pulumi.get(self, "notes")

    @property
    @pulumi.getter(name="startTimeUtc")
    def start_time_utc(self) -> str:
        """
        TThe bookmark start time.
        """
        return pulumi.get(self, "start_time_utc")

    @property
    @pulumi.getter(name="eventTime")
    def event_time(self) -> Optional[str]:
        """
        The bookmark event time.
        """
        return pulumi.get(self, "event_time")


@pulumi.output_type
class ClientInfoResponse(dict):
    """
    Information on the client (user or application) that made some action
    """
    def __init__(__self__, *,
                 email: Optional[str] = None,
                 name: Optional[str] = None,
                 object_id: Optional[str] = None,
                 user_principal_name: Optional[str] = None):
        """
        Information on the client (user or application) that made some action
        :param str email: The email of the client.
        :param str name: The name of the client.
        :param str object_id: The object id of the client.
        :param str user_principal_name: The user principal name of the client.
        """
        if email is not None:
            pulumi.set(__self__, "email", email)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if object_id is not None:
            pulumi.set(__self__, "object_id", object_id)
        if user_principal_name is not None:
            pulumi.set(__self__, "user_principal_name", user_principal_name)

    @property
    @pulumi.getter
    def email(self) -> Optional[str]:
        """
        The email of the client.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the client.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> Optional[str]:
        """
        The object id of the client.
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter(name="userPrincipalName")
    def user_principal_name(self) -> Optional[str]:
        """
        The user principal name of the client.
        """
        return pulumi.get(self, "user_principal_name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class EntityInsightItemResponseResult(dict):
    """
    Entity insight Item.
    """
    def __init__(__self__, *,
                 chart_query_results: Optional[Sequence['outputs.InsightsTableResultResponseResult']] = None,
                 query_id: Optional[str] = None,
                 query_time_interval: Optional['outputs.EntityInsightItemResponseQueryTimeIntervalResult'] = None,
                 table_query_results: Optional['outputs.InsightsTableResultResponseResult'] = None):
        """
        Entity insight Item.
        :param Sequence['InsightsTableResultResponseArgs'] chart_query_results: Query results for table insights query.
        :param str query_id: The query id of the insight
        :param 'EntityInsightItemResponseQueryTimeIntervalArgs' query_time_interval: The Time interval that the query actually executed on.
        :param 'InsightsTableResultResponseArgs' table_query_results: Query results for table insights query.
        """
        if chart_query_results is not None:
            pulumi.set(__self__, "chart_query_results", chart_query_results)
        if query_id is not None:
            pulumi.set(__self__, "query_id", query_id)
        if query_time_interval is not None:
            pulumi.set(__self__, "query_time_interval", query_time_interval)
        if table_query_results is not None:
            pulumi.set(__self__, "table_query_results", table_query_results)

    @property
    @pulumi.getter(name="chartQueryResults")
    def chart_query_results(self) -> Optional[Sequence['outputs.InsightsTableResultResponseResult']]:
        """
        Query results for table insights query.
        """
        return pulumi.get(self, "chart_query_results")

    @property
    @pulumi.getter(name="queryId")
    def query_id(self) -> Optional[str]:
        """
        The query id of the insight
        """
        return pulumi.get(self, "query_id")

    @property
    @pulumi.getter(name="queryTimeInterval")
    def query_time_interval(self) -> Optional['outputs.EntityInsightItemResponseQueryTimeIntervalResult']:
        """
        The Time interval that the query actually executed on.
        """
        return pulumi.get(self, "query_time_interval")

    @property
    @pulumi.getter(name="tableQueryResults")
    def table_query_results(self) -> Optional['outputs.InsightsTableResultResponseResult']:
        """
        Query results for table insights query.
        """
        return pulumi.get(self, "table_query_results")


@pulumi.output_type
class EntityInsightItemResponseQueryTimeIntervalResult(dict):
    """
    The Time interval that the query actually executed on.
    """
    def __init__(__self__, *,
                 end_time: Optional[str] = None,
                 start_time: Optional[str] = None):
        """
        The Time interval that the query actually executed on.
        :param str end_time: Insight query end time
        :param str start_time: Insight query start time
        """
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[str]:
        """
        Insight query end time
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[str]:
        """
        Insight query start time
        """
        return pulumi.get(self, "start_time")


@pulumi.output_type
class GetInsightsErrorResponseResult(dict):
    """
    GetInsights Query Errors.
    """
    def __init__(__self__, *,
                 error_message: str,
                 kind: str,
                 query_id: Optional[str] = None):
        """
        GetInsights Query Errors.
        :param str error_message: the error message
        :param str kind: the query kind
        :param str query_id: the query id
        """
        pulumi.set(__self__, "error_message", error_message)
        pulumi.set(__self__, "kind", kind)
        if query_id is not None:
            pulumi.set(__self__, "query_id", query_id)

    @property
    @pulumi.getter(name="errorMessage")
    def error_message(self) -> str:
        """
        the error message
        """
        return pulumi.get(self, "error_message")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        the query kind
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="queryId")
    def query_id(self) -> Optional[str]:
        """
        the query id
        """
        return pulumi.get(self, "query_id")


@pulumi.output_type
class GetInsightsResultsMetadataResponseResult(dict):
    """
    Get Insights result metadata.
    """
    def __init__(__self__, *,
                 total_count: int,
                 errors: Optional[Sequence['outputs.GetInsightsErrorResponseResult']] = None):
        """
        Get Insights result metadata.
        :param int total_count: the total items found for the insights request
        :param Sequence['GetInsightsErrorResponseArgs'] errors: information about the failed queries
        """
        pulumi.set(__self__, "total_count", total_count)
        if errors is not None:
            pulumi.set(__self__, "errors", errors)

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        the total items found for the insights request
        """
        return pulumi.get(self, "total_count")

    @property
    @pulumi.getter
    def errors(self) -> Optional[Sequence['outputs.GetInsightsErrorResponseResult']]:
        """
        information about the failed queries
        """
        return pulumi.get(self, "errors")


@pulumi.output_type
class IncidentAdditionalDataResponse(dict):
    """
    Incident additional data property bag.
    """
    def __init__(__self__, *,
                 alert_product_names: Sequence[str],
                 alerts_count: int,
                 bookmarks_count: int,
                 comments_count: int,
                 tactics: Sequence[str]):
        """
        Incident additional data property bag.
        :param Sequence[str] alert_product_names: List of product names of alerts in the incident
        :param int alerts_count: The number of alerts in the incident
        :param int bookmarks_count: The number of bookmarks in the incident
        :param int comments_count: The number of comments in the incident
        :param Sequence[str] tactics: The tactics associated with incident
        """
        pulumi.set(__self__, "alert_product_names", alert_product_names)
        pulumi.set(__self__, "alerts_count", alerts_count)
        pulumi.set(__self__, "bookmarks_count", bookmarks_count)
        pulumi.set(__self__, "comments_count", comments_count)
        pulumi.set(__self__, "tactics", tactics)

    @property
    @pulumi.getter(name="alertProductNames")
    def alert_product_names(self) -> Sequence[str]:
        """
        List of product names of alerts in the incident
        """
        return pulumi.get(self, "alert_product_names")

    @property
    @pulumi.getter(name="alertsCount")
    def alerts_count(self) -> int:
        """
        The number of alerts in the incident
        """
        return pulumi.get(self, "alerts_count")

    @property
    @pulumi.getter(name="bookmarksCount")
    def bookmarks_count(self) -> int:
        """
        The number of bookmarks in the incident
        """
        return pulumi.get(self, "bookmarks_count")

    @property
    @pulumi.getter(name="commentsCount")
    def comments_count(self) -> int:
        """
        The number of comments in the incident
        """
        return pulumi.get(self, "comments_count")

    @property
    @pulumi.getter
    def tactics(self) -> Sequence[str]:
        """
        The tactics associated with incident
        """
        return pulumi.get(self, "tactics")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IncidentInfoResponse(dict):
    """
    Describes related incident information for the bookmark
    """
    def __init__(__self__, *,
                 incident_id: Optional[str] = None,
                 relation_name: Optional[str] = None,
                 severity: Optional[str] = None,
                 title: Optional[str] = None):
        """
        Describes related incident information for the bookmark
        :param str incident_id: Incident Id
        :param str relation_name: Relation Name
        :param str severity: The severity of the incident
        :param str title: The title of the incident
        """
        if incident_id is not None:
            pulumi.set(__self__, "incident_id", incident_id)
        if relation_name is not None:
            pulumi.set(__self__, "relation_name", relation_name)
        if severity is not None:
            pulumi.set(__self__, "severity", severity)
        if title is not None:
            pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter(name="incidentId")
    def incident_id(self) -> Optional[str]:
        """
        Incident Id
        """
        return pulumi.get(self, "incident_id")

    @property
    @pulumi.getter(name="relationName")
    def relation_name(self) -> Optional[str]:
        """
        Relation Name
        """
        return pulumi.get(self, "relation_name")

    @property
    @pulumi.getter
    def severity(self) -> Optional[str]:
        """
        The severity of the incident
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter
    def title(self) -> Optional[str]:
        """
        The title of the incident
        """
        return pulumi.get(self, "title")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IncidentLabelResponse(dict):
    """
    Represents an incident label
    """
    def __init__(__self__, *,
                 label_name: str,
                 label_type: str):
        """
        Represents an incident label
        :param str label_name: The name of the label
        :param str label_type: The type of the label
        """
        pulumi.set(__self__, "label_name", label_name)
        pulumi.set(__self__, "label_type", label_type)

    @property
    @pulumi.getter(name="labelName")
    def label_name(self) -> str:
        """
        The name of the label
        """
        return pulumi.get(self, "label_name")

    @property
    @pulumi.getter(name="labelType")
    def label_type(self) -> str:
        """
        The type of the label
        """
        return pulumi.get(self, "label_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IncidentOwnerInfoResponse(dict):
    """
    Information on the user an incident is assigned to
    """
    def __init__(__self__, *,
                 assigned_to: Optional[str] = None,
                 email: Optional[str] = None,
                 object_id: Optional[str] = None,
                 user_principal_name: Optional[str] = None):
        """
        Information on the user an incident is assigned to
        :param str assigned_to: The name of the user the incident is assigned to.
        :param str email: The email of the user the incident is assigned to.
        :param str object_id: The object id of the user the incident is assigned to.
        :param str user_principal_name: The user principal name of the user the incident is assigned to.
        """
        if assigned_to is not None:
            pulumi.set(__self__, "assigned_to", assigned_to)
        if email is not None:
            pulumi.set(__self__, "email", email)
        if object_id is not None:
            pulumi.set(__self__, "object_id", object_id)
        if user_principal_name is not None:
            pulumi.set(__self__, "user_principal_name", user_principal_name)

    @property
    @pulumi.getter(name="assignedTo")
    def assigned_to(self) -> Optional[str]:
        """
        The name of the user the incident is assigned to.
        """
        return pulumi.get(self, "assigned_to")

    @property
    @pulumi.getter
    def email(self) -> Optional[str]:
        """
        The email of the user the incident is assigned to.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> Optional[str]:
        """
        The object id of the user the incident is assigned to.
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter(name="userPrincipalName")
    def user_principal_name(self) -> Optional[str]:
        """
        The user principal name of the user the incident is assigned to.
        """
        return pulumi.get(self, "user_principal_name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class InsightsTableResultResponseResult(dict):
    """
    Query results for table insights query.
    """
    def __init__(__self__, *,
                 columns: Optional[Sequence['outputs.InsightsTableResultResponseColumnsResult']] = None,
                 rows: Optional[Sequence[Sequence[str]]] = None):
        """
        Query results for table insights query.
        :param Sequence['InsightsTableResultResponseColumnsArgs'] columns: Columns Metadata of the table
        :param Sequence[Sequence[str]] rows: Rows data of the table
        """
        if columns is not None:
            pulumi.set(__self__, "columns", columns)
        if rows is not None:
            pulumi.set(__self__, "rows", rows)

    @property
    @pulumi.getter
    def columns(self) -> Optional[Sequence['outputs.InsightsTableResultResponseColumnsResult']]:
        """
        Columns Metadata of the table
        """
        return pulumi.get(self, "columns")

    @property
    @pulumi.getter
    def rows(self) -> Optional[Sequence[Sequence[str]]]:
        """
        Rows data of the table
        """
        return pulumi.get(self, "rows")


@pulumi.output_type
class InsightsTableResultResponseColumnsResult(dict):
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 type: Optional[str] = None):
        """
        :param str name: the name of the colum
        :param str type: the type of the colum
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        the name of the colum
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        the type of the colum
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class SecurityAlertTimelineItemResponseResult(dict):
    """
    Represents security alert timeline item.
    """
    def __init__(__self__, *,
                 alert_type: str,
                 azure_resource_id: str,
                 display_name: str,
                 end_time_utc: str,
                 kind: str,
                 product_name: str,
                 severity: str,
                 start_time_utc: str,
                 time_generated: str):
        """
        Represents security alert timeline item.
        :param str alert_type: The name of the alert type.
        :param str azure_resource_id: The alert azure resource id.
        :param str display_name: The alert name.
        :param str end_time_utc: The alert end time.
        :param str kind: The entity query kind type.
               Expected value is 'SecurityAlert'.
        :param str product_name: The alert product name.
        :param str severity: The alert severity.
        :param str start_time_utc: The alert start time.
        :param str time_generated: The alert generated time.
        """
        pulumi.set(__self__, "alert_type", alert_type)
        pulumi.set(__self__, "azure_resource_id", azure_resource_id)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "end_time_utc", end_time_utc)
        pulumi.set(__self__, "kind", 'SecurityAlert')
        pulumi.set(__self__, "product_name", product_name)
        pulumi.set(__self__, "severity", severity)
        pulumi.set(__self__, "start_time_utc", start_time_utc)
        pulumi.set(__self__, "time_generated", time_generated)

    @property
    @pulumi.getter(name="alertType")
    def alert_type(self) -> str:
        """
        The name of the alert type.
        """
        return pulumi.get(self, "alert_type")

    @property
    @pulumi.getter(name="azureResourceId")
    def azure_resource_id(self) -> str:
        """
        The alert azure resource id.
        """
        return pulumi.get(self, "azure_resource_id")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The alert name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="endTimeUtc")
    def end_time_utc(self) -> str:
        """
        The alert end time.
        """
        return pulumi.get(self, "end_time_utc")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The entity query kind type.
        Expected value is 'SecurityAlert'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="productName")
    def product_name(self) -> str:
        """
        The alert product name.
        """
        return pulumi.get(self, "product_name")

    @property
    @pulumi.getter
    def severity(self) -> str:
        """
        The alert severity.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter(name="startTimeUtc")
    def start_time_utc(self) -> str:
        """
        The alert start time.
        """
        return pulumi.get(self, "start_time_utc")

    @property
    @pulumi.getter(name="timeGenerated")
    def time_generated(self) -> str:
        """
        The alert generated time.
        """
        return pulumi.get(self, "time_generated")


@pulumi.output_type
class TimelineAggregationResponseResult(dict):
    """
    timeline aggregation information per kind
    """
    def __init__(__self__, *,
                 count: int,
                 kind: str):
        """
        timeline aggregation information per kind
        :param int count: the total items found for a kind
        :param str kind: the query kind
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "kind", kind)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        the total items found for a kind
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        the query kind
        """
        return pulumi.get(self, "kind")


@pulumi.output_type
class TimelineErrorResponseResult(dict):
    """
    Timeline Query Errors.
    """
    def __init__(__self__, *,
                 error_message: str,
                 kind: str,
                 query_id: Optional[str] = None):
        """
        Timeline Query Errors.
        :param str error_message: the error message
        :param str kind: the query kind
        :param str query_id: the query id
        """
        pulumi.set(__self__, "error_message", error_message)
        pulumi.set(__self__, "kind", kind)
        if query_id is not None:
            pulumi.set(__self__, "query_id", query_id)

    @property
    @pulumi.getter(name="errorMessage")
    def error_message(self) -> str:
        """
        the error message
        """
        return pulumi.get(self, "error_message")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        the query kind
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="queryId")
    def query_id(self) -> Optional[str]:
        """
        the query id
        """
        return pulumi.get(self, "query_id")


@pulumi.output_type
class TimelineResultsMetadataResponseResult(dict):
    """
    Expansion result metadata.
    """
    def __init__(__self__, *,
                 aggregations: Sequence['outputs.TimelineAggregationResponseResult'],
                 total_count: int,
                 errors: Optional[Sequence['outputs.TimelineErrorResponseResult']] = None):
        """
        Expansion result metadata.
        :param Sequence['TimelineAggregationResponseArgs'] aggregations: timeline aggregation per kind
        :param int total_count: the total items found for the timeline request
        :param Sequence['TimelineErrorResponseArgs'] errors: information about the failure queries
        """
        pulumi.set(__self__, "aggregations", aggregations)
        pulumi.set(__self__, "total_count", total_count)
        if errors is not None:
            pulumi.set(__self__, "errors", errors)

    @property
    @pulumi.getter
    def aggregations(self) -> Sequence['outputs.TimelineAggregationResponseResult']:
        """
        timeline aggregation per kind
        """
        return pulumi.get(self, "aggregations")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        the total items found for the timeline request
        """
        return pulumi.get(self, "total_count")

    @property
    @pulumi.getter
    def errors(self) -> Optional[Sequence['outputs.TimelineErrorResponseResult']]:
        """
        information about the failure queries
        """
        return pulumi.get(self, "errors")


@pulumi.output_type
class UserInfoResponse(dict):
    """
    User information that made some action
    """
    def __init__(__self__, *,
                 email: str,
                 name: str,
                 object_id: Optional[str] = None):
        """
        User information that made some action
        :param str email: The email of the user.
        :param str name: The name of the user.
        :param str object_id: The object id of the user.
        """
        pulumi.set(__self__, "email", email)
        pulumi.set(__self__, "name", name)
        if object_id is not None:
            pulumi.set(__self__, "object_id", object_id)

    @property
    @pulumi.getter
    def email(self) -> str:
        """
        The email of the user.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the user.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> Optional[str]:
        """
        The object id of the user.
        """
        return pulumi.get(self, "object_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


