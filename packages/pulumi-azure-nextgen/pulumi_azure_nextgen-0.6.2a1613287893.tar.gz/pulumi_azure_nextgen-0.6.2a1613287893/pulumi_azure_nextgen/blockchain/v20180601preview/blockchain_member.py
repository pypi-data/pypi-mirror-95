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

__all__ = ['BlockchainMember']


class BlockchainMember(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 blockchain_member_name: Optional[pulumi.Input[str]] = None,
                 consortium: Optional[pulumi.Input[str]] = None,
                 consortium_management_account_password: Optional[pulumi.Input[str]] = None,
                 consortium_member_display_name: Optional[pulumi.Input[str]] = None,
                 consortium_role: Optional[pulumi.Input[str]] = None,
                 firewall_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FirewallRuleArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[Union[str, 'BlockchainProtocol']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 validator_nodes_sku: Optional[pulumi.Input[pulumi.InputType['BlockchainMemberNodesSkuArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Payload of the blockchain member which is exposed in the request/response of the resource provider.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] blockchain_member_name: Blockchain member name.
        :param pulumi.Input[str] consortium: Gets or sets the consortium for the blockchain member.
        :param pulumi.Input[str] consortium_management_account_password: Sets the managed consortium management account password.
        :param pulumi.Input[str] consortium_member_display_name: Gets the display name of the member in the consortium.
        :param pulumi.Input[str] consortium_role: Gets the role of the member in the consortium.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FirewallRuleArgs']]]] firewall_rules: Gets or sets firewall rules
        :param pulumi.Input[str] location: The GEO location of the blockchain service.
        :param pulumi.Input[str] password: Sets the basic auth password of the blockchain member.
        :param pulumi.Input[Union[str, 'BlockchainProtocol']] protocol: Gets or sets the blockchain protocol.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: Gets or sets the blockchain member Sku.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags of the service which is a list of key value pairs that describes the resource.
        :param pulumi.Input[pulumi.InputType['BlockchainMemberNodesSkuArgs']] validator_nodes_sku: Gets or sets the blockchain validator nodes Sku.
        """
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

            if blockchain_member_name is None and not opts.urn:
                raise TypeError("Missing required property 'blockchain_member_name'")
            __props__['blockchain_member_name'] = blockchain_member_name
            __props__['consortium'] = consortium
            __props__['consortium_management_account_password'] = consortium_management_account_password
            __props__['consortium_member_display_name'] = consortium_member_display_name
            __props__['consortium_role'] = consortium_role
            __props__['firewall_rules'] = firewall_rules
            __props__['location'] = location
            __props__['password'] = password
            __props__['protocol'] = protocol
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['validator_nodes_sku'] = validator_nodes_sku
            __props__['consortium_management_account_address'] = None
            __props__['dns'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['public_key'] = None
            __props__['root_contract_address'] = None
            __props__['type'] = None
            __props__['user_name'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:blockchain:BlockchainMember")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(BlockchainMember, __self__).__init__(
            'azure-nextgen:blockchain/v20180601preview:BlockchainMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BlockchainMember':
        """
        Get an existing BlockchainMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return BlockchainMember(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def consortium(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the consortium for the blockchain member.
        """
        return pulumi.get(self, "consortium")

    @property
    @pulumi.getter(name="consortiumManagementAccountAddress")
    def consortium_management_account_address(self) -> pulumi.Output[str]:
        """
        Gets the managed consortium management account address.
        """
        return pulumi.get(self, "consortium_management_account_address")

    @property
    @pulumi.getter(name="consortiumManagementAccountPassword")
    def consortium_management_account_password(self) -> pulumi.Output[Optional[str]]:
        """
        Sets the managed consortium management account password.
        """
        return pulumi.get(self, "consortium_management_account_password")

    @property
    @pulumi.getter(name="consortiumMemberDisplayName")
    def consortium_member_display_name(self) -> pulumi.Output[Optional[str]]:
        """
        Gets the display name of the member in the consortium.
        """
        return pulumi.get(self, "consortium_member_display_name")

    @property
    @pulumi.getter(name="consortiumRole")
    def consortium_role(self) -> pulumi.Output[Optional[str]]:
        """
        Gets the role of the member in the consortium.
        """
        return pulumi.get(self, "consortium_role")

    @property
    @pulumi.getter
    def dns(self) -> pulumi.Output[str]:
        """
        Gets the dns endpoint of the blockchain member.
        """
        return pulumi.get(self, "dns")

    @property
    @pulumi.getter(name="firewallRules")
    def firewall_rules(self) -> pulumi.Output[Optional[Sequence['outputs.FirewallRuleResponse']]]:
        """
        Gets or sets firewall rules
        """
        return pulumi.get(self, "firewall_rules")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The GEO location of the blockchain service.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        """
        Sets the basic auth password of the blockchain member.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the blockchain protocol.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Gets or sets the blockchain member provision state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> pulumi.Output[str]:
        """
        Gets the public key of the blockchain member (default transaction node).
        """
        return pulumi.get(self, "public_key")

    @property
    @pulumi.getter(name="rootContractAddress")
    def root_contract_address(self) -> pulumi.Output[str]:
        """
        Gets the Ethereum root contract address of the blockchain.
        """
        return pulumi.get(self, "root_contract_address")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        Gets or sets the blockchain member Sku.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags of the service which is a list of key value pairs that describes the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the service - e.g. "Microsoft.Blockchain"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[str]:
        """
        Gets the auth user name of the blockchain member.
        """
        return pulumi.get(self, "user_name")

    @property
    @pulumi.getter(name="validatorNodesSku")
    def validator_nodes_sku(self) -> pulumi.Output[Optional['outputs.BlockchainMemberNodesSkuResponse']]:
        """
        Gets or sets the blockchain validator nodes Sku.
        """
        return pulumi.get(self, "validator_nodes_sku")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

