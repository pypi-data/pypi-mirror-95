# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'ARecordResponse',
    'AaaaRecordResponse',
    'CnameRecordResponse',
    'MxRecordResponse',
    'PtrRecordResponse',
    'SoaRecordResponse',
    'SrvRecordResponse',
    'SubResourceResponse',
    'TxtRecordResponse',
]

@pulumi.output_type
class ARecordResponse(dict):
    """
    An A record.
    """
    def __init__(__self__, *,
                 ipv4_address: Optional[str] = None):
        """
        An A record.
        :param str ipv4_address: The IPv4 address of this A record.
        """
        if ipv4_address is not None:
            pulumi.set(__self__, "ipv4_address", ipv4_address)

    @property
    @pulumi.getter(name="ipv4Address")
    def ipv4_address(self) -> Optional[str]:
        """
        The IPv4 address of this A record.
        """
        return pulumi.get(self, "ipv4_address")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class AaaaRecordResponse(dict):
    """
    An AAAA record.
    """
    def __init__(__self__, *,
                 ipv6_address: Optional[str] = None):
        """
        An AAAA record.
        :param str ipv6_address: The IPv6 address of this AAAA record.
        """
        if ipv6_address is not None:
            pulumi.set(__self__, "ipv6_address", ipv6_address)

    @property
    @pulumi.getter(name="ipv6Address")
    def ipv6_address(self) -> Optional[str]:
        """
        The IPv6 address of this AAAA record.
        """
        return pulumi.get(self, "ipv6_address")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class CnameRecordResponse(dict):
    """
    A CNAME record.
    """
    def __init__(__self__, *,
                 cname: Optional[str] = None):
        """
        A CNAME record.
        :param str cname: The canonical name for this CNAME record.
        """
        if cname is not None:
            pulumi.set(__self__, "cname", cname)

    @property
    @pulumi.getter
    def cname(self) -> Optional[str]:
        """
        The canonical name for this CNAME record.
        """
        return pulumi.get(self, "cname")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class MxRecordResponse(dict):
    """
    An MX record.
    """
    def __init__(__self__, *,
                 exchange: Optional[str] = None,
                 preference: Optional[int] = None):
        """
        An MX record.
        :param str exchange: The domain name of the mail host for this MX record.
        :param int preference: The preference value for this MX record.
        """
        if exchange is not None:
            pulumi.set(__self__, "exchange", exchange)
        if preference is not None:
            pulumi.set(__self__, "preference", preference)

    @property
    @pulumi.getter
    def exchange(self) -> Optional[str]:
        """
        The domain name of the mail host for this MX record.
        """
        return pulumi.get(self, "exchange")

    @property
    @pulumi.getter
    def preference(self) -> Optional[int]:
        """
        The preference value for this MX record.
        """
        return pulumi.get(self, "preference")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class PtrRecordResponse(dict):
    """
    A PTR record.
    """
    def __init__(__self__, *,
                 ptrdname: Optional[str] = None):
        """
        A PTR record.
        :param str ptrdname: The PTR target domain name for this PTR record.
        """
        if ptrdname is not None:
            pulumi.set(__self__, "ptrdname", ptrdname)

    @property
    @pulumi.getter
    def ptrdname(self) -> Optional[str]:
        """
        The PTR target domain name for this PTR record.
        """
        return pulumi.get(self, "ptrdname")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SoaRecordResponse(dict):
    """
    An SOA record.
    """
    def __init__(__self__, *,
                 email: Optional[str] = None,
                 expire_time: Optional[float] = None,
                 host: Optional[str] = None,
                 minimum_ttl: Optional[float] = None,
                 refresh_time: Optional[float] = None,
                 retry_time: Optional[float] = None,
                 serial_number: Optional[float] = None):
        """
        An SOA record.
        :param str email: The email contact for this SOA record.
        :param float expire_time: The expire time for this SOA record.
        :param str host: The domain name of the authoritative name server for this SOA record.
        :param float minimum_ttl: The minimum value for this SOA record. By convention this is used to determine the negative caching duration.
        :param float refresh_time: The refresh value for this SOA record.
        :param float retry_time: The retry time for this SOA record.
        :param float serial_number: The serial number for this SOA record.
        """
        if email is not None:
            pulumi.set(__self__, "email", email)
        if expire_time is not None:
            pulumi.set(__self__, "expire_time", expire_time)
        if host is not None:
            pulumi.set(__self__, "host", host)
        if minimum_ttl is not None:
            pulumi.set(__self__, "minimum_ttl", minimum_ttl)
        if refresh_time is not None:
            pulumi.set(__self__, "refresh_time", refresh_time)
        if retry_time is not None:
            pulumi.set(__self__, "retry_time", retry_time)
        if serial_number is not None:
            pulumi.set(__self__, "serial_number", serial_number)

    @property
    @pulumi.getter
    def email(self) -> Optional[str]:
        """
        The email contact for this SOA record.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> Optional[float]:
        """
        The expire time for this SOA record.
        """
        return pulumi.get(self, "expire_time")

    @property
    @pulumi.getter
    def host(self) -> Optional[str]:
        """
        The domain name of the authoritative name server for this SOA record.
        """
        return pulumi.get(self, "host")

    @property
    @pulumi.getter(name="minimumTtl")
    def minimum_ttl(self) -> Optional[float]:
        """
        The minimum value for this SOA record. By convention this is used to determine the negative caching duration.
        """
        return pulumi.get(self, "minimum_ttl")

    @property
    @pulumi.getter(name="refreshTime")
    def refresh_time(self) -> Optional[float]:
        """
        The refresh value for this SOA record.
        """
        return pulumi.get(self, "refresh_time")

    @property
    @pulumi.getter(name="retryTime")
    def retry_time(self) -> Optional[float]:
        """
        The retry time for this SOA record.
        """
        return pulumi.get(self, "retry_time")

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> Optional[float]:
        """
        The serial number for this SOA record.
        """
        return pulumi.get(self, "serial_number")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SrvRecordResponse(dict):
    """
    An SRV record.
    """
    def __init__(__self__, *,
                 port: Optional[int] = None,
                 priority: Optional[int] = None,
                 target: Optional[str] = None,
                 weight: Optional[int] = None):
        """
        An SRV record.
        :param int port: The port value for this SRV record.
        :param int priority: The priority value for this SRV record.
        :param str target: The target domain name for this SRV record.
        :param int weight: The weight value for this SRV record.
        """
        if port is not None:
            pulumi.set(__self__, "port", port)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if target is not None:
            pulumi.set(__self__, "target", target)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        The port value for this SRV record.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def priority(self) -> Optional[int]:
        """
        The priority value for this SRV record.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def target(self) -> Optional[str]:
        """
        The target domain name for this SRV record.
        """
        return pulumi.get(self, "target")

    @property
    @pulumi.getter
    def weight(self) -> Optional[int]:
        """
        The weight value for this SRV record.
        """
        return pulumi.get(self, "weight")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SubResourceResponse(dict):
    """
    Reference to another subresource.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        Reference to another subresource.
        :param str id: Resource ID.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class TxtRecordResponse(dict):
    """
    A TXT record.
    """
    def __init__(__self__, *,
                 value: Optional[Sequence[str]] = None):
        """
        A TXT record.
        :param Sequence[str] value: The text value of this TXT record.
        """
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence[str]]:
        """
        The text value of this TXT record.
        """
        return pulumi.get(self, "value")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


