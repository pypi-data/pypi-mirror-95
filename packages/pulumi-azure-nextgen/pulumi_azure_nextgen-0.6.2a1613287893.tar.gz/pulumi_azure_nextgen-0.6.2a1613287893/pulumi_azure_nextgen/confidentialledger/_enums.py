# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'LedgerType',
]


class LedgerType(str, Enum):
    """
    Type of Confidential Ledger
    """
    UNKNOWN = "Unknown"
    PUBLIC = "Public"
    PRIVATE = "Private"
