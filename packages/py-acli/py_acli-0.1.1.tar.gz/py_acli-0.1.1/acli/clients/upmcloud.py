from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class UpmCloudCommand(Command):
    pass

@dataclass
class UpmCloudClient(RemoteClient):
    def execute(self, command: UpmCloudCommand):
        return super().do_execute(command)

# Variants for addLicense
@dataclass
class AddLicenseOptions:
    """Optional parameters for action addLicense"""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class AddLicenseGivenAppAndLicense(UpmCloudCommand):
    """Add a license to an installed app for Server. For Cloud, add a private license token for an app."""
    app: str
    """App key. In some cases, app name can be used as well."""
    license: str
    """App license key."""
    options: AddLicenseOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addLicense"

@dataclass
class AddLicenseGivenAppAndFile(UpmCloudCommand):
    """Add a license to an installed app for Server. For Cloud, add a private license token for an app."""
    app: str
    """App key. In some cases, app name can be used as well."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddLicenseOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addLicense"

# End Variants for addLicense

# Variants for addLicenses
@dataclass
class AddLicensesOptions:
    """Optional parameters for action addLicenses"""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class AddLicenses(UpmCloudCommand):
    """Add a license for each app installed on the instance that has an Atlassian app license referenced in the directory specified by the file parameter. License files must be named after the apps key with or without an extension."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddLicensesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addLicenses"

# End Variants for addLicenses

# Variants for disableApp

@dataclass
class DisableApp(UpmCloudCommand):
    """Disable an app."""
    app: str
    """App key. In some cases, app name can be used as well."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "disableApp"

# End Variants for disableApp

# Variants for enableApp

@dataclass
class EnableApp(UpmCloudCommand):
    """Enable an app."""
    app: str
    """App key. In some cases, app name can be used as well."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "enableApp"

# End Variants for enableApp

# Variants for getApp
@dataclass
class GetAppOptions:
    """Optional parameters for action getApp"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetApp(UpmCloudCommand):
    """Get information for an installed app."""
    app: str
    """App key. In some cases, app name can be used as well."""
    options: GetAppOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getApp"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getApp

# Variants for getAppList
@dataclass
class GetAppListOptions:
    """Optional parameters for action getAppList"""
    include_disabled: bool|None = None
    """To include disabled apps in list."""
    include_system: bool|None = None
    """To include system apps in app list."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetAppList(UpmCloudCommand):
    """Get a list of installed apps with regex filtering on name or key. By default, only enabled, user installed apps are included."""
    options: GetAppListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAppList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAppList

# Variants for installApp
@dataclass
class InstallAppOptions:
    """Optional parameters for action installApp"""
    wait: bool|None = None
    """Wait for operation to finish processing before completing action."""
    version: str|None = None
    """App version name or number that uniquely identifies a specific Marketplace version."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""

@dataclass
class InstallAppGivenApp(UpmCloudCommand):
    """Install an app using a url or file or Marketplace app key. If an app key is used and version is not provided, it will default to @compatible provided we can determine the latest compatible version for the server version. If a compatible version cannot be determined (like for EAP releases), default will be latest version. If @default is used for the file parameter, an attempt will be made to find an obr or jar file in the standard Maven or Gradle target directory. When doing a Marketplace install by app key or the requested version is provided, the actual app version will be confirmed to match the requested version in order to catch unsuccessful downgrade attempts. UPM will not downgrade an already installed app. For many cases, it is best to uninstall first. Use either run the uninstallAddon action separately before or use --options uninstall if the app parameter is provided or file is @default. UPM may fail indicating the file is invalid when installing by URL from some websites like Confluence. Avoid the error by using --options download to first download to the local file system and then install."""
    app: str
    """App key. In some cases, app name can be used as well."""
    options: InstallAppOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "installApp"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class InstallAppGivenUrl(UpmCloudCommand):
    """Install an app using a url or file or Marketplace app key. If an app key is used and version is not provided, it will default to @compatible provided we can determine the latest compatible version for the server version. If a compatible version cannot be determined (like for EAP releases), default will be latest version. If @default is used for the file parameter, an attempt will be made to find an obr or jar file in the standard Maven or Gradle target directory. When doing a Marketplace install by app key or the requested version is provided, the actual app version will be confirmed to match the requested version in order to catch unsuccessful downgrade attempts. UPM will not downgrade an already installed app. For many cases, it is best to uninstall first. Use either run the uninstallAddon action separately before or use --options uninstall if the app parameter is provided or file is @default. UPM may fail indicating the file is invalid when installing by URL from some websites like Confluence. Avoid the error by using --options download to first download to the local file system and then install."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: InstallAppOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "installApp"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class InstallAppGivenFile(UpmCloudCommand):
    """Install an app using a url or file or Marketplace app key. If an app key is used and version is not provided, it will default to @compatible provided we can determine the latest compatible version for the server version. If a compatible version cannot be determined (like for EAP releases), default will be latest version. If @default is used for the file parameter, an attempt will be made to find an obr or jar file in the standard Maven or Gradle target directory. When doing a Marketplace install by app key or the requested version is provided, the actual app version will be confirmed to match the requested version in order to catch unsuccessful downgrade attempts. UPM will not downgrade an already installed app. For many cases, it is best to uninstall first. Use either run the uninstallAddon action separately before or use --options uninstall if the app parameter is provided or file is @default. UPM may fail indicating the file is invalid when installing by URL from some websites like Confluence. Avoid the error by using --options download to first download to the local file system and then install."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: InstallAppOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "installApp"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for installApp

# Variants for removeLicense

@dataclass
class RemoveLicense(UpmCloudCommand):
    """Remove license from an installed app for Server. For Cloud, remove private license token for an app."""
    app: str
    """App key. In some cases, app name can be used as well."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeLicense"

# End Variants for removeLicense

# Variants for renderRequest
@dataclass
class RenderRequestOptions:
    """Optional parameters for action renderRequest"""
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
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class RenderRequest(UpmCloudCommand):
    """Render URL based request. URL can be a partial URL. The response data is returned optionally modified by findReplace processing. Use '--pretty' to format returned JSON data in a more readable form. Also, for JSON data, you can use '--options setReplacementVariables'."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: RenderRequestOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "renderRequest"

# End Variants for renderRequest

# Variants for runFromAppList
@dataclass
class RunFromAppListOptions:
    """Optional parameters for action runFromAppList"""
    include_disabled: bool|None = None
    """To include disabled apps in list."""
    include_system: bool|None = None
    """To include system apps in app list."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    clear_file_before_append: bool|None = None
    """For run actions, this option will automatically clear an existing file on the first append requested."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class RunFromAppListGivenInput(UpmCloudCommand):
    """Run an action for each app matching the same filtering options as with getAppList."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromAppListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAppList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAppListGivenCommon(UpmCloudCommand):
    """Run an action for each app matching the same filtering options as with getAppList."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromAppListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAppList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAppListGivenFile(UpmCloudCommand):
    """Run an action for each app matching the same filtering options as with getAppList."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromAppListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAppList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromAppList

# Variants for uninstallApp
@dataclass
class UninstallAppOptions:
    """Optional parameters for action uninstallApp"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class UninstallApp(UpmCloudCommand):
    """Uninstall the app. If @default is specified, an attempt will be made to find an appropriate value by looking for an Atlassian app descriptor file with the value specified."""
    app: str
    """App key. In some cases, app name can be used as well."""
    options: UninstallAppOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "uninstallApp"

# End Variants for uninstallApp
