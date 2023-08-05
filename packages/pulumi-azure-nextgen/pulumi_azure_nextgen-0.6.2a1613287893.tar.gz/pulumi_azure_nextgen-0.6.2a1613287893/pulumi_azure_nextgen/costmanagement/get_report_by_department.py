# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'GetReportByDepartmentResult',
    'AwaitableGetReportByDepartmentResult',
    'get_report_by_department',
]

@pulumi.output_type
class GetReportByDepartmentResult:
    """
    A report resource.
    """
    def __init__(__self__, definition=None, delivery_info=None, format=None, id=None, name=None, schedule=None, tags=None, type=None):
        if definition and not isinstance(definition, dict):
            raise TypeError("Expected argument 'definition' to be a dict")
        pulumi.set(__self__, "definition", definition)
        if delivery_info and not isinstance(delivery_info, dict):
            raise TypeError("Expected argument 'delivery_info' to be a dict")
        pulumi.set(__self__, "delivery_info", delivery_info)
        if format and not isinstance(format, str):
            raise TypeError("Expected argument 'format' to be a str")
        pulumi.set(__self__, "format", format)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if schedule and not isinstance(schedule, dict):
            raise TypeError("Expected argument 'schedule' to be a dict")
        pulumi.set(__self__, "schedule", schedule)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def definition(self) -> 'outputs.ReportDefinitionResponse':
        """
        Has definition for the report.
        """
        return pulumi.get(self, "definition")

    @property
    @pulumi.getter(name="deliveryInfo")
    def delivery_info(self) -> 'outputs.ReportDeliveryInfoResponse':
        """
        Has delivery information for the report.
        """
        return pulumi.get(self, "delivery_info")

    @property
    @pulumi.getter
    def format(self) -> Optional[str]:
        """
        The format of the report being delivered.
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def schedule(self) -> Optional['outputs.ReportScheduleResponse']:
        """
        Has schedule information for the report.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetReportByDepartmentResult(GetReportByDepartmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetReportByDepartmentResult(
            definition=self.definition,
            delivery_info=self.delivery_info,
            format=self.format,
            id=self.id,
            name=self.name,
            schedule=self.schedule,
            tags=self.tags,
            type=self.type)


def get_report_by_department(department_id: Optional[str] = None,
                             report_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetReportByDepartmentResult:
    """
    Use this data source to access information about an existing resource.

    :param str department_id: Department ID
    :param str report_name: Report Name.
    """
    __args__ = dict()
    __args__['departmentId'] = department_id
    __args__['reportName'] = report_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:costmanagement:getReportByDepartment', __args__, opts=opts, typ=GetReportByDepartmentResult).value

    return AwaitableGetReportByDepartmentResult(
        definition=__ret__.definition,
        delivery_info=__ret__.delivery_info,
        format=__ret__.format,
        id=__ret__.id,
        name=__ret__.name,
        schedule=__ret__.schedule,
        tags=__ret__.tags,
        type=__ret__.type)
