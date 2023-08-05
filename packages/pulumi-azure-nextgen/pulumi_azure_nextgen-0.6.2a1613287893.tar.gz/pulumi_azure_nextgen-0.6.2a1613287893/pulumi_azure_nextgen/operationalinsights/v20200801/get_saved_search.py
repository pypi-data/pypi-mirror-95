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
    'GetSavedSearchResult',
    'AwaitableGetSavedSearchResult',
    'get_saved_search',
]

@pulumi.output_type
class GetSavedSearchResult:
    """
    Value object for saved search results.
    """
    def __init__(__self__, category=None, display_name=None, etag=None, function_alias=None, function_parameters=None, id=None, name=None, query=None, tags=None, type=None, version=None):
        if category and not isinstance(category, str):
            raise TypeError("Expected argument 'category' to be a str")
        pulumi.set(__self__, "category", category)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if function_alias and not isinstance(function_alias, str):
            raise TypeError("Expected argument 'function_alias' to be a str")
        pulumi.set(__self__, "function_alias", function_alias)
        if function_parameters and not isinstance(function_parameters, str):
            raise TypeError("Expected argument 'function_parameters' to be a str")
        pulumi.set(__self__, "function_parameters", function_parameters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if query and not isinstance(query, str):
            raise TypeError("Expected argument 'query' to be a str")
        pulumi.set(__self__, "query", query)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, float):
            raise TypeError("Expected argument 'version' to be a float")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def category(self) -> str:
        """
        The category of the saved search. This helps the user to find a saved search faster. 
        """
        return pulumi.get(self, "category")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        Saved search display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        The ETag of the saved search.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="functionAlias")
    def function_alias(self) -> Optional[str]:
        """
        The function alias if query serves as a function.
        """
        return pulumi.get(self, "function_alias")

    @property
    @pulumi.getter(name="functionParameters")
    def function_parameters(self) -> Optional[str]:
        """
        The optional function parameters if query serves as a function. Value should be in the following format: 'param-name1:type1 = default_value1, param-name2:type2 = default_value2'. For more examples and proper syntax please refer to https://docs.microsoft.com/en-us/azure/kusto/query/functions/user-defined-functions.
        """
        return pulumi.get(self, "function_parameters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def query(self) -> str:
        """
        The query expression for the saved search.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.TagResponse']]:
        """
        The tags attached to the saved search.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> Optional[float]:
        """
        The version number of the query language. The current version is 2 and is the default.
        """
        return pulumi.get(self, "version")


class AwaitableGetSavedSearchResult(GetSavedSearchResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSavedSearchResult(
            category=self.category,
            display_name=self.display_name,
            etag=self.etag,
            function_alias=self.function_alias,
            function_parameters=self.function_parameters,
            id=self.id,
            name=self.name,
            query=self.query,
            tags=self.tags,
            type=self.type,
            version=self.version)


def get_saved_search(resource_group_name: Optional[str] = None,
                     saved_search_id: Optional[str] = None,
                     workspace_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSavedSearchResult:
    """
    Use this data source to access information about an existing resource.

    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str saved_search_id: The id of the saved search.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['savedSearchId'] = saved_search_id
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:operationalinsights/v20200801:getSavedSearch', __args__, opts=opts, typ=GetSavedSearchResult).value

    return AwaitableGetSavedSearchResult(
        category=__ret__.category,
        display_name=__ret__.display_name,
        etag=__ret__.etag,
        function_alias=__ret__.function_alias,
        function_parameters=__ret__.function_parameters,
        id=__ret__.id,
        name=__ret__.name,
        query=__ret__.query,
        tags=__ret__.tags,
        type=__ret__.type,
        version=__ret__.version)
