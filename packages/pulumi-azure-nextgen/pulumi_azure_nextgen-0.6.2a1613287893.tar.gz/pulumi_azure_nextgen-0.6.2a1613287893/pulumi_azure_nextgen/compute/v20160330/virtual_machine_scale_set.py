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

__all__ = ['VirtualMachineScaleSet']


class VirtualMachineScaleSet(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['VirtualMachineScaleSetIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 over_provision: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 upgrade_policy: Optional[pulumi.Input[pulumi.InputType['UpgradePolicyArgs']]] = None,
                 virtual_machine_profile: Optional[pulumi.Input[pulumi.InputType['VirtualMachineScaleSetVMProfileArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Describes a Virtual Machine Scale Set.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['VirtualMachineScaleSetIdentityArgs']] identity: The identity of the virtual machine scale set, if configured.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] name: The name of the VM scale set to create or update.
        :param pulumi.Input[bool] over_provision: Specifies whether the Virtual Machine Scale Set should be overprovisioned.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The virtual machine scale set sku.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[pulumi.InputType['UpgradePolicyArgs']] upgrade_policy: The upgrade policy.
        :param pulumi.Input[pulumi.InputType['VirtualMachineScaleSetVMProfileArgs']] virtual_machine_profile: The virtual machine profile.
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

            __props__['identity'] = identity
            __props__['location'] = location
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            __props__['over_provision'] = over_provision
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['upgrade_policy'] = upgrade_policy
            __props__['virtual_machine_profile'] = virtual_machine_profile
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:compute:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/latest:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20150615:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20160430preview:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20170330:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20171201:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20180401:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20180601:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20181001:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20190301:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20190701:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20191201:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20200601:VirtualMachineScaleSet"), pulumi.Alias(type_="azure-nextgen:compute/v20201201:VirtualMachineScaleSet")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualMachineScaleSet, __self__).__init__(
            'azure-nextgen:compute/v20160330:VirtualMachineScaleSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualMachineScaleSet':
        """
        Get an existing VirtualMachineScaleSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return VirtualMachineScaleSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.VirtualMachineScaleSetIdentityResponse']]:
        """
        The identity of the virtual machine scale set, if configured.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="overProvision")
    def over_provision(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether the Virtual Machine Scale Set should be overprovisioned.
        """
        return pulumi.get(self, "over_provision")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The virtual machine scale set sku.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="upgradePolicy")
    def upgrade_policy(self) -> pulumi.Output[Optional['outputs.UpgradePolicyResponse']]:
        """
        The upgrade policy.
        """
        return pulumi.get(self, "upgrade_policy")

    @property
    @pulumi.getter(name="virtualMachineProfile")
    def virtual_machine_profile(self) -> pulumi.Output[Optional['outputs.VirtualMachineScaleSetVMProfileResponse']]:
        """
        The virtual machine profile.
        """
        return pulumi.get(self, "virtual_machine_profile")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

