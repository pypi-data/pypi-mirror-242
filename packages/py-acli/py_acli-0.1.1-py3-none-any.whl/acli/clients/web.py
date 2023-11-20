from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class WebCommand(Command):
    pass

@dataclass
class WebClient(Client):
    def execute(self, command: WebCommand):
        return super().do_execute(command)

# Variants for startServer
@dataclass
class StartServerOptions:
    """Optional parameters for action startServer"""
    path: str|None = None
    """Partial URL path."""
    port: str|None = None
    """Network server port. Normally should be in the user port range of 1024 to 49151 or the default HTTP port number 80."""
    file: str|None = None
    """Path to file based content or result output. For start action, it is the directory location for action script files and defaults to the current directory."""
    secret: str|None = None
    """Secret used to determine if the webhook payload's HMAC signature matches the data to be considered valid for processing. If no secret is configured or specified for the startServer action, signature matching will be skipped by the ACLI web server. For the request action, the secret will be used to produce a HMAC signature and pass it on a request header with key specified by the hmacHeader parameter."""
    hmac_header: str|None = None
    """Request header key to use for sending the HMAC hash. If not specified, no HMAC signature will be sent. Using HMAC requests needs to be coordinated with the web server that is going to handle the request. For example, the ACLI web server handles signatures passed with X-Hub-Signature, X-Gitlab-Token, and X-Signature header keys. Also, a custom hmacHeader can be defined on the startServer action."""
    token: str|None = None
    """A bearer token value used for HTTP Authorization header. If enabled for the server on the startServer action or configured for the managed server in the acli-service.properties file, the server will require requests provide the HTTP Authorization header that matches the server token value. Request made with the webRequest action to the managed server will automatically use the configured value."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class StartServer(WebCommand):
    """Start a ACLI web server. Port defaults to 7780 if not specified. Optionally, use the file parameter to specify the directory where automation scripts are located. Use continue to ignore an already started case. Options are available for restarting the server, waiting for the server to be active after being started including a wait timeout in milliseconds - '--options restart --options wait --options timeout=5000'."""
    options: StartServerOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "startServer"

# End Variants for startServer

# Variants for stopServer
@dataclass
class StopServerOptions:
    """Optional parameters for action stopServer"""
    path: str|None = None
    """Partial URL path."""
    port: str|None = None
    """Network server port. Normally should be in the user port range of 1024 to 49151 or the default HTTP port number 80."""
    token: str|None = None
    """A bearer token value used for HTTP Authorization header. If enabled for the server on the startServer action or configured for the managed server in the acli-service.properties file, the server will require requests provide the HTTP Authorization header that matches the server token value. Request made with the webRequest action to the managed server will automatically use the configured value."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class StopServer(WebCommand):
    """Stop ACLI web server. Use continue to ignore error when server believed to be stopped already. Options are available for waiting for the server to be ended - '--options wait'."""
    options: StopServerOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "stopServer"

# End Variants for stopServer

# Variants for webRequest
@dataclass
class WebRequestOptions:
    """Optional parameters for action webRequest"""
    url: str|None = None
    """URL for a web request. Defaults to the web server URL including the path setting. The web server URL will be added if the URL is a relative (partial) URL."""
    path: str|None = None
    """Partial URL path."""
    request_type: str|None = None
    """Type of a render request like GET, POST, PUT, DELETE, PATCH, HEAD."""
    data: str|None = None
    """JSON data for runFromJson. Post data for renderRequest. Action specific definition in some cases."""
    content_type: str|None = None
    """Content type for post data for a web request. Any suitable value can be specified. We have defines some special values for commonly used types: JSON, HTML, XML, URL_ENCODED, FORM_URL_ENCODED."""
    accept_type: str|None = None
    """Content type to accept for renderRequest if different than contentType."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    file: str|None = None
    """Path to file based content or result output. For start action, it is the directory location for action script files and defaults to the current directory."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    hmac_header: str|None = None
    """Request header key to use for sending the HMAC hash. If not specified, no HMAC signature will be sent. Using HMAC requests needs to be coordinated with the web server that is going to handle the request. For example, the ACLI web server handles signatures passed with X-Hub-Signature, X-Gitlab-Token, and X-Signature header keys. Also, a custom hmacHeader can be defined on the startServer action."""
    hmac_algorithm: str|None = None
    """Hash-based Message Authentication Code (HMAC) to used for sending requests if HMAC validation is desired. Supported algorithm names are HmacSHA1, HmacSHA224, HmacSHA256, HmacSHA384, HmacSHA512, and HmacMD5."""
    secret: str|None = None
    """Secret used to determine if the webhook payload's HMAC signature matches the data to be considered valid for processing. If no secret is configured or specified for the startServer action, signature matching will be skipped by the ACLI web server. For the request action, the secret will be used to produce a HMAC signature and pass it on a request header with key specified by the hmacHeader parameter."""
    token: str|None = None
    """A bearer token value used for HTTP Authorization header. If enabled for the server on the startServer action or configured for the managed server in the acli-service.properties file, the server will require requests provide the HTTP Authorization header that matches the server token value. Request made with the webRequest action to the managed server will automatically use the configured value."""

@dataclass
class WebRequest(WebCommand):
    """Make a HTTP web request. The response data is returned optionally modified by findReplace processing. Use '--pretty' to format returned JSON data in a more readable form. Also, for JSON data, you can use '--options setReplacementVariables'."""
    options: WebRequestOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "webRequest"

# End Variants for webRequest
