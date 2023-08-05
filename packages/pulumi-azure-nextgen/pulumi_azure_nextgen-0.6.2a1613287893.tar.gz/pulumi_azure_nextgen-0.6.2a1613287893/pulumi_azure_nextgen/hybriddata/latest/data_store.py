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
from ._inputs import *

__all__ = ['DataStore']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:hybriddata:DataStore'.""", DeprecationWarning)


class DataStore(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:hybriddata:DataStore'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 customer_secrets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CustomerSecretArgs']]]]] = None,
                 data_manager_name: Optional[pulumi.Input[str]] = None,
                 data_store_name: Optional[pulumi.Input[str]] = None,
                 data_store_type_id: Optional[pulumi.Input[str]] = None,
                 extended_properties: Optional[Any] = None,
                 repository_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input['State']] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Data store.
        Latest API Version: 2019-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CustomerSecretArgs']]]] customer_secrets: List of customer secrets containing a key identifier and key value. The key identifier is a way for the specific data source to understand the key. Value contains customer secret encrypted by the encryptionKeys.
        :param pulumi.Input[str] data_manager_name: The name of the DataManager Resource within the specified resource group. DataManager names must be between 3 and 24 characters in length and use any alphanumeric and underscore only
        :param pulumi.Input[str] data_store_name: The data store/repository name to be created or updated.
        :param pulumi.Input[str] data_store_type_id: The arm id of the data store type.
        :param Any extended_properties: A generic json used differently by each data source type.
        :param pulumi.Input[str] repository_id: Arm Id for the manager resource to which the data source is associated. This is optional.
        :param pulumi.Input[str] resource_group_name: The Resource Group Name
        :param pulumi.Input['State'] state: State of the data source.
        """
        pulumi.log.warn("DataStore is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:hybriddata:DataStore'.")
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['customer_secrets'] = customer_secrets
            if data_manager_name is None and not opts.urn:
                raise TypeError("Missing required property 'data_manager_name'")
            __props__['data_manager_name'] = data_manager_name
            if data_store_name is None and not opts.urn:
                raise TypeError("Missing required property 'data_store_name'")
            __props__['data_store_name'] = data_store_name
            if data_store_type_id is None and not opts.urn:
                raise TypeError("Missing required property 'data_store_type_id'")
            __props__['data_store_type_id'] = data_store_type_id
            __props__['extended_properties'] = extended_properties
            __props__['repository_id'] = repository_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if state is None and not opts.urn:
                raise TypeError("Missing required property 'state'")
            __props__['state'] = state
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:hybriddata:DataStore"), pulumi.Alias(type_="azure-nextgen:hybriddata/v20160601:DataStore"), pulumi.Alias(type_="azure-nextgen:hybriddata/v20190601:DataStore")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DataStore, __self__).__init__(
            'azure-nextgen:hybriddata/latest:DataStore',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DataStore':
        """
        Get an existing DataStore resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return DataStore(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="customerSecrets")
    def customer_secrets(self) -> pulumi.Output[Optional[Sequence['outputs.CustomerSecretResponse']]]:
        """
        List of customer secrets containing a key identifier and key value. The key identifier is a way for the specific data source to understand the key. Value contains customer secret encrypted by the encryptionKeys.
        """
        return pulumi.get(self, "customer_secrets")

    @property
    @pulumi.getter(name="dataStoreTypeId")
    def data_store_type_id(self) -> pulumi.Output[str]:
        """
        The arm id of the data store type.
        """
        return pulumi.get(self, "data_store_type_id")

    @property
    @pulumi.getter(name="extendedProperties")
    def extended_properties(self) -> pulumi.Output[Optional[Any]]:
        """
        A generic json used differently by each data source type.
        """
        return pulumi.get(self, "extended_properties")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the object.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="repositoryId")
    def repository_id(self) -> pulumi.Output[Optional[str]]:
        """
        Arm Id for the manager resource to which the data source is associated. This is optional.
        """
        return pulumi.get(self, "repository_id")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        State of the data source.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the object.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

