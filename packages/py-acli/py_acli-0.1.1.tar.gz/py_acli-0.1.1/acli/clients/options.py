from dataclasses import dataclass
from typing import Iterable

@dataclass
class LoggingOptions:
    """Optional parameters for logging"""
    quiet: bool|None = None
    """Limit some output messages. Optional for all actions."""
    verbose: bool|None = None
    """Requests verbose output to help with problem determination. Optional for all actions."""
    debug: bool|None = None
    """Requests detail debug output especially useful for Support. Optional for all actions. Recommend first using verbose logging for problem determination."""

@dataclass
class CommonOptions:
    """Common options to lots of commands"""
    date_format: str|None = None
    """Format string for dates in Java SimpleDateFormat. Default for output is client date format. Default for date parsing is lenient starting with client date format and then some other standard formats based on JSON date format."""
    date_format2: str|None = None
    """Alternate format string for dates in Java SimpleDateFormat. Use specific (may be ignored), but normally used for date only fields to avoid longer dateFormat based output. Some uses default to yyyy-MM-dd."""
    help: bool|None = None
    """Shows a help message."""
    note: Iterable[str]|str|None = None
    """Documentation note that can be added to an action to aid understanding of the action and parameters. Note parameters will be ignored in processing."""
    pretty: bool|None = None
    """Format JSON output in a more readable form."""
    special: str|None = None
    """Ordered list of alternate characters for comma ( , ), colon ( : ), at ( @ ), quote ( ' ), and double quote ( " ) characters used for specialized processing of some specific parameters."""
    connection_timeout: str|None = None
    """Allow overriding environment settings for connect and read timeouts on URL connections. In milliseconds, 0 means infinite."""
    header: Iterable[str]|str|None = None
    """Custom request header added to remote requests. Allows for unique headers required in some environments or needed for specific requests. Header values may be sensitive like for authentication headers, so header values are masked in debug data similar to passwords and tokens."""
