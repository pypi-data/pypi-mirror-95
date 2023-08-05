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
    'HeaderFieldResponse',
    'WebTestGeolocationResponse',
    'WebTestPropertiesResponseConfiguration',
    'WebTestPropertiesResponseContentValidation',
    'WebTestPropertiesResponseRequest',
]

@pulumi.output_type
class HeaderFieldResponse(dict):
    """
    A header to add to the WebTest.
    """
    def __init__(__self__, *,
                 header_field_name: Optional[str] = None,
                 header_field_value: Optional[str] = None):
        """
        A header to add to the WebTest.
        :param str header_field_name: The name of the header.
        :param str header_field_value: The value of the header.
        """
        if header_field_name is not None:
            pulumi.set(__self__, "header_field_name", header_field_name)
        if header_field_value is not None:
            pulumi.set(__self__, "header_field_value", header_field_value)

    @property
    @pulumi.getter(name="headerFieldName")
    def header_field_name(self) -> Optional[str]:
        """
        The name of the header.
        """
        return pulumi.get(self, "header_field_name")

    @property
    @pulumi.getter(name="headerFieldValue")
    def header_field_value(self) -> Optional[str]:
        """
        The value of the header.
        """
        return pulumi.get(self, "header_field_value")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class WebTestGeolocationResponse(dict):
    """
    Geo-physical location to run a WebTest from. You must specify one or more locations for the test to run from.
    """
    def __init__(__self__, *,
                 location: Optional[str] = None):
        """
        Geo-physical location to run a WebTest from. You must specify one or more locations for the test to run from.
        :param str location: Location ID for the WebTest to run from.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Location ID for the WebTest to run from.
        """
        return pulumi.get(self, "location")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class WebTestPropertiesResponseConfiguration(dict):
    """
    An XML configuration specification for a WebTest.
    """
    def __init__(__self__, *,
                 web_test: Optional[str] = None):
        """
        An XML configuration specification for a WebTest.
        :param str web_test: The XML specification of a WebTest to run against an application.
        """
        if web_test is not None:
            pulumi.set(__self__, "web_test", web_test)

    @property
    @pulumi.getter(name="webTest")
    def web_test(self) -> Optional[str]:
        """
        The XML specification of a WebTest to run against an application.
        """
        return pulumi.get(self, "web_test")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class WebTestPropertiesResponseContentValidation(dict):
    """
    The collection of content validation properties
    """
    def __init__(__self__, *,
                 content_match: Optional[str] = None,
                 ignore_case: Optional[bool] = None,
                 pass_if_text_found: Optional[bool] = None):
        """
        The collection of content validation properties
        :param str content_match: Content to look for in the return of the WebTest.
        :param bool ignore_case: When set, this value makes the ContentMatch validation case insensitive.
        :param bool pass_if_text_found: When true, validation will pass if there is a match for the ContentMatch string.  If false, validation will fail if there is a match
        """
        if content_match is not None:
            pulumi.set(__self__, "content_match", content_match)
        if ignore_case is not None:
            pulumi.set(__self__, "ignore_case", ignore_case)
        if pass_if_text_found is not None:
            pulumi.set(__self__, "pass_if_text_found", pass_if_text_found)

    @property
    @pulumi.getter(name="contentMatch")
    def content_match(self) -> Optional[str]:
        """
        Content to look for in the return of the WebTest.
        """
        return pulumi.get(self, "content_match")

    @property
    @pulumi.getter(name="ignoreCase")
    def ignore_case(self) -> Optional[bool]:
        """
        When set, this value makes the ContentMatch validation case insensitive.
        """
        return pulumi.get(self, "ignore_case")

    @property
    @pulumi.getter(name="passIfTextFound")
    def pass_if_text_found(self) -> Optional[bool]:
        """
        When true, validation will pass if there is a match for the ContentMatch string.  If false, validation will fail if there is a match
        """
        return pulumi.get(self, "pass_if_text_found")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class WebTestPropertiesResponseRequest(dict):
    """
    The collection of request properties
    """
    def __init__(__self__, *,
                 follow_redirects: Optional[bool] = None,
                 headers: Optional[Sequence['outputs.HeaderFieldResponse']] = None,
                 http_verb: Optional[str] = None,
                 parse_dependent_requests: Optional[bool] = None,
                 request_body: Optional[str] = None,
                 request_url: Optional[str] = None):
        """
        The collection of request properties
        :param bool follow_redirects: Follow redirects for this web test.
        :param Sequence['HeaderFieldResponseArgs'] headers: List of headers and their values to add to the WebTest call.
        :param str http_verb: Http verb to use for this web test.
        :param bool parse_dependent_requests: Parse Dependent request for this WebTest.
        :param str request_body: Base64 encoded string body to send with this web test.
        :param str request_url: Url location to test.
        """
        if follow_redirects is not None:
            pulumi.set(__self__, "follow_redirects", follow_redirects)
        if headers is not None:
            pulumi.set(__self__, "headers", headers)
        if http_verb is not None:
            pulumi.set(__self__, "http_verb", http_verb)
        if parse_dependent_requests is not None:
            pulumi.set(__self__, "parse_dependent_requests", parse_dependent_requests)
        if request_body is not None:
            pulumi.set(__self__, "request_body", request_body)
        if request_url is not None:
            pulumi.set(__self__, "request_url", request_url)

    @property
    @pulumi.getter(name="followRedirects")
    def follow_redirects(self) -> Optional[bool]:
        """
        Follow redirects for this web test.
        """
        return pulumi.get(self, "follow_redirects")

    @property
    @pulumi.getter
    def headers(self) -> Optional[Sequence['outputs.HeaderFieldResponse']]:
        """
        List of headers and their values to add to the WebTest call.
        """
        return pulumi.get(self, "headers")

    @property
    @pulumi.getter(name="httpVerb")
    def http_verb(self) -> Optional[str]:
        """
        Http verb to use for this web test.
        """
        return pulumi.get(self, "http_verb")

    @property
    @pulumi.getter(name="parseDependentRequests")
    def parse_dependent_requests(self) -> Optional[bool]:
        """
        Parse Dependent request for this WebTest.
        """
        return pulumi.get(self, "parse_dependent_requests")

    @property
    @pulumi.getter(name="requestBody")
    def request_body(self) -> Optional[str]:
        """
        Base64 encoded string body to send with this web test.
        """
        return pulumi.get(self, "request_body")

    @property
    @pulumi.getter(name="requestUrl")
    def request_url(self) -> Optional[str]:
        """
        Url location to test.
        """
        return pulumi.get(self, "request_url")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


