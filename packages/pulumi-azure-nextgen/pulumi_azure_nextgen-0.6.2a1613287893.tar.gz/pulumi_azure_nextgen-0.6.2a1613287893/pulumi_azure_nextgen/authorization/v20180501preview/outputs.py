# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = [
    'AccessReviewInstanceResponse',
    'AccessReviewReviewerResponse',
]

@pulumi.output_type
class AccessReviewInstanceResponse(dict):
    """
    Access Review Instance.
    """
    def __init__(__self__, *,
                 id: str,
                 name: str,
                 status: str,
                 type: str,
                 end_date_time: Optional[str] = None,
                 start_date_time: Optional[str] = None):
        """
        Access Review Instance.
        :param str id: The access review instance id.
        :param str name: The access review instance name.
        :param str status: This read-only field specifies the status of an access review instance.
        :param str type: The resource type.
        :param str end_date_time: The DateTime when the review instance is scheduled to end.
        :param str start_date_time: The DateTime when the review instance is scheduled to be start.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "type", type)
        if end_date_time is not None:
            pulumi.set(__self__, "end_date_time", end_date_time)
        if start_date_time is not None:
            pulumi.set(__self__, "start_date_time", start_date_time)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The access review instance id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The access review instance name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        This read-only field specifies the status of an access review instance.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="endDateTime")
    def end_date_time(self) -> Optional[str]:
        """
        The DateTime when the review instance is scheduled to end.
        """
        return pulumi.get(self, "end_date_time")

    @property
    @pulumi.getter(name="startDateTime")
    def start_date_time(self) -> Optional[str]:
        """
        The DateTime when the review instance is scheduled to be start.
        """
        return pulumi.get(self, "start_date_time")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class AccessReviewReviewerResponse(dict):
    """
    Descriptor for what needs to be reviewed
    """
    def __init__(__self__, *,
                 principal_type: str,
                 principal_id: Optional[str] = None):
        """
        Descriptor for what needs to be reviewed
        :param str principal_type: The identity type : user/servicePrincipal
        :param str principal_id: The id of the reviewer(user/servicePrincipal)
        """
        pulumi.set(__self__, "principal_type", principal_type)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="principalType")
    def principal_type(self) -> str:
        """
        The identity type : user/servicePrincipal
        """
        return pulumi.get(self, "principal_type")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[str]:
        """
        The id of the reviewer(user/servicePrincipal)
        """
        return pulumi.get(self, "principal_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


