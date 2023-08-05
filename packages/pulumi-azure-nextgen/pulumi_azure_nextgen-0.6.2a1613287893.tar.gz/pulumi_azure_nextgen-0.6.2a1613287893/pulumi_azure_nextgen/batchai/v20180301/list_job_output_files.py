# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = [
    'ListJobOutputFilesResult',
    'AwaitableListJobOutputFilesResult',
    'list_job_output_files',
]

@pulumi.output_type
class ListJobOutputFilesResult:
    """
    Values returned by the List operation.
    """
    def __init__(__self__, next_link=None, value=None):
        if next_link and not isinstance(next_link, str):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, "next_link", next_link)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="nextLink")
    def next_link(self) -> Optional[str]:
        """
        The continuation token.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Sequence['outputs.FileResponseResult']:
        """
        The collection of returned job directories and files.
        """
        return pulumi.get(self, "value")


class AwaitableListJobOutputFilesResult(ListJobOutputFilesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListJobOutputFilesResult(
            next_link=self.next_link,
            value=self.value)


def list_job_output_files(directory: Optional[str] = None,
                          job_name: Optional[str] = None,
                          linkexpiryinminutes: Optional[int] = None,
                          max_results: Optional[int] = None,
                          outputdirectoryid: Optional[str] = None,
                          resource_group_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListJobOutputFilesResult:
    """
    Use this data source to access information about an existing resource.

    :param str directory: The path to the directory.
    :param str job_name: The name of the job within the specified resource group. Job names can only contain a combination of alphanumeric characters along with dash (-) and underscore (_). The name must be from 1 through 64 characters long.
    :param int linkexpiryinminutes: The number of minutes after which the download link will expire.
    :param int max_results: The maximum number of items to return in the response. A maximum of 1000 files can be returned.
    :param str outputdirectoryid: Id of the job output directory. This is the OutputDirectory-->id parameter that is given by the user during Create Job.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['directory'] = directory
    __args__['jobName'] = job_name
    __args__['linkexpiryinminutes'] = linkexpiryinminutes
    __args__['maxResults'] = max_results
    __args__['outputdirectoryid'] = outputdirectoryid
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:batchai/v20180301:listJobOutputFiles', __args__, opts=opts, typ=ListJobOutputFilesResult).value

    return AwaitableListJobOutputFilesResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
