from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class SystemCommand(Command):
    pass

@dataclass
class SystemClient(Client):
    def execute(self, command: SystemCommand):
        return super().do_execute(command)

# Variants for clearSecureProperties
@dataclass
class ClearSecurePropertiesOptions:
    """Optional parameters for action clearSecureProperties"""
    force: bool|None = None
    """Forces the current action to run without prompting for confirmation."""

@dataclass
class ClearSecureProperties(SystemCommand):
    """ Clears all secure properties by deleting the current user's secure properties file. Use with caution, this action CANNOT be undone! Prompts the user to confirm the action unless the --force parameter is provided."""
    options: ClearSecurePropertiesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "clearSecureProperties"

# End Variants for clearSecureProperties

# Variants for copyFiles
@dataclass
class CopyFilesOptions:
    """Optional parameters for action copyFiles"""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""

@dataclass
class CopyFiles(SystemCommand):
    """Copy a single file or files selected from a directory with regex filtering on path name. Use the file parameter to direct output to a target file or directory. When append is used, data will be appended to the target file if it already exists. If requested, find and replace logic will be applied to the source data before processing provided the file is text (has text mime type). Similarly, replacement variables will automatically be replaced with their values. Use continue to continue copying files from a directory even after there is an error copying a file."""
    source_file: str
    """Source file or directory for a copy operation or similar."""
    options: CopyFilesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyFiles"

# End Variants for copyFiles

# Variants for exportSecureProperties
@dataclass
class ExportSecurePropertiesOptions:
    """Optional parameters for action exportSecureProperties"""
    exclude: Iterable[str]|str|None = None
    """A regex for key names to exclude."""
    include: Iterable[str]|str|None = None
    """A regex for key names to include."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""

@dataclass
class ExportSecureProperties(SystemCommand):
    """Exports secure properties from the user's own secure property file to an external file with a different password. Use the --replace parameter to overwrite existing values and the --exclude or --include parameters to filter."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: ExportSecurePropertiesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "exportSecureProperties"

# End Variants for exportSecureProperties

# Variants for getFileList
@dataclass
class GetFileListOptions:
    """Optional parameters for action getFileList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetFileList(SystemCommand):
    """Get system file list from a directory with regex filtering on file path and satisfying other selection criteria. Use the directory parameter to identify the absolute or relative path to search for files matching selection criteria."""
    directory: str
    """System file directory."""
    options: GetFileListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getFileList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getFileList

# Variants for getFileMonitorList
@dataclass
class GetFileMonitorListOptions:
    """Optional parameters for action getFileMonitorList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetFileMonitorList(SystemCommand):
    """Get list of file system events monitored for a given directory with regex filtering on file path and satisfying other selection criteria. Note that results are only produced once the monitor is stopped by either timeout or limit."""
    directory: str
    """System file directory."""
    events: Iterable[str]
    """Comma separated list of file system events. Valid events may create, modify, and delete."""
    options: GetFileMonitorListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getFileMonitorList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getFileMonitorList

# Variants for getSecureProperty
@dataclass
class GetSecurePropertyOptions:
    """Optional parameters for action getSecureProperty"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""

@dataclass
class GetSecureProperty(SystemCommand):
    """Gets a property from the current user's secure secure properties file. Use --outputFormat 1 to test for existence and --outputFormat 2 to also return the associated value if present."""
    name: str
    """Name of an item or entity."""
    options: GetSecurePropertyOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSecureProperty"

# End Variants for getSecureProperty

# Variants for getSecurePropertyList
@dataclass
class GetSecurePropertyListOptions:
    """Optional parameters for action getSecurePropertyList"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    include: Iterable[str]|str|None = None
    """A regex for key names to include."""
    exclude: Iterable[str]|str|None = None
    """A regex for key names to exclude."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetSecurePropertyList(SystemCommand):
    """Gets the list of properties in the current user's secure properties file. Use --outputFormat 1 to list entry names and --outputFormat 2 to also return the associated secret values if present."""
    options: GetSecurePropertyListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSecurePropertyList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getSecurePropertyList

# Variants for getUpgradeInfo
@dataclass
class GetUpgradeInfoOptions:
    """Optional parameters for action getUpgradeInfo"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetUpgradeInfo(SystemCommand):
    """Get information about upgrades available for ACLI."""
    options: GetUpgradeInfoOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getUpgradeInfo"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getUpgradeInfo

# Variants for importSecureProperties
@dataclass
class ImportSecurePropertiesOptions:
    """Optional parameters for action importSecureProperties"""
    exclude: Iterable[str]|str|None = None
    """A regex for key names to exclude."""
    include: Iterable[str]|str|None = None
    """A regex for key names to include."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""

@dataclass
class ImportSecureProperties(SystemCommand):
    """Imports secure properties from an external file with a different password to the user's own secure property file. Use the --replace parameter to overwrite existing values and the --exclude or --include parameters to filter."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: ImportSecurePropertiesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "importSecureProperties"

# End Variants for importSecureProperties

# Variants for removeSecureProperty

@dataclass
class RemoveSecureProperty(SystemCommand):
    """Remove a property from the current user's secure properties file."""
    name: str
    """Name of an item or entity."""
    force: bool
    """Forces the current action to run without prompting for confirmation."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeSecureProperty"

# End Variants for removeSecureProperty

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
    user: str|None = None
    """User name for basic authentication on a render request."""
    password: str|None = None
    """User password for basic authentication on a render request."""
    token: str|None = None
    """OAuth or similar authentication token."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class RenderRequest(SystemCommand):
    """Render URL based request. URL can be a partial URL. The response data modified by optional findReplace processing is returned. Use '--pretty' to format returned JSON data in a more readable form."""
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

# Variants for return
@dataclass
class ReturnOptions:
    """Optional parameters for action return"""
    type: str|None = None
    """Type of installation update request."""
    comment: str|None = None
    """Comment text."""
    value: str|None = None
    """Field value or condition value for matching."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class Return(SystemCommand):
    """Return from the current script level with type normal (default) or type error. Normal error handling occurs for a script running another script. The return can be conditioned based on the value and regex parameters just like the runIf action."""
    options: ReturnOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "return"

# End Variants for return

# Variants for runFromFileList
@dataclass
class RunFromFileListOptions:
    """Optional parameters for action runFromFileList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""
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
class RunFromFileListGivenDirectoryAndInput(SystemCommand):
    """Run actions for each file from a directory with regex filtering on file path and satisfying other selection criteria similar to getFileList. Run actions from a file, list of input parameters, or standard input similar to the run action. Use the directory parameter to identify the absolute or relative path to search for files matching selection criteria."""
    directory: str
    """System file directory."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromFileListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromFileList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromFileListGivenDirectoryAndCommon(SystemCommand):
    """Run actions for each file from a directory with regex filtering on file path and satisfying other selection criteria similar to getFileList. Run actions from a file, list of input parameters, or standard input similar to the run action. Use the directory parameter to identify the absolute or relative path to search for files matching selection criteria."""
    directory: str
    """System file directory."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromFileListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromFileList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromFileListGivenDirectoryAndFile(SystemCommand):
    """Run actions for each file from a directory with regex filtering on file path and satisfying other selection criteria similar to getFileList. Run actions from a file, list of input parameters, or standard input similar to the run action. Use the directory parameter to identify the absolute or relative path to search for files matching selection criteria."""
    directory: str
    """System file directory."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromFileListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromFileList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromFileList

# Variants for runFromFileMonitorList
@dataclass
class RunFromFileMonitorListOptions:
    """Optional parameters for action runFromFileMonitorList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    timeout: str|None = None
    """Timeout in seconds. Use -1 to wait forever."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""
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
class RunFromFileMonitorListGivenDirectoryAndEventsAndInput(SystemCommand):
    """Run actions for system file events from a directory with regex filtering on file path and satisfying other selection criteria similar to getFileList. Run actions from a file, list of input parameters, or standard input similar to the run action. Use the directory parameter to identify the absolute or relative path to monitor for events. Valid events are create, delete, and modify. Specify one or more event parameters. Use the limit or timeout parameter to control automatic stopping of the monitor process."""
    directory: str
    """System file directory."""
    events: Iterable[str]
    """Comma separated list of file system events. Valid events may create, modify, and delete."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromFileMonitorListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromFileMonitorList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromFileMonitorListGivenDirectoryAndEventsAndCommon(SystemCommand):
    """Run actions for system file events from a directory with regex filtering on file path and satisfying other selection criteria similar to getFileList. Run actions from a file, list of input parameters, or standard input similar to the run action. Use the directory parameter to identify the absolute or relative path to monitor for events. Valid events are create, delete, and modify. Specify one or more event parameters. Use the limit or timeout parameter to control automatic stopping of the monitor process."""
    directory: str
    """System file directory."""
    events: Iterable[str]
    """Comma separated list of file system events. Valid events may create, modify, and delete."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromFileMonitorListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromFileMonitorList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromFileMonitorListGivenDirectoryAndEventsAndFile(SystemCommand):
    """Run actions for system file events from a directory with regex filtering on file path and satisfying other selection criteria similar to getFileList. Run actions from a file, list of input parameters, or standard input similar to the run action. Use the directory parameter to identify the absolute or relative path to monitor for events. Valid events are create, delete, and modify. Specify one or more event parameters. Use the limit or timeout parameter to control automatic stopping of the monitor process."""
    directory: str
    """System file directory."""
    events: Iterable[str]
    """Comma separated list of file system events. Valid events may create, modify, and delete."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromFileMonitorListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromFileMonitorList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromFileMonitorList

# Variants for setSecureProperty
@dataclass
class SetSecurePropertyOptions:
    """Optional parameters for action setSecureProperty"""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""

@dataclass
class SetSecureProperty(SystemCommand):
    """Set a property in the current user's secure secure properties file. Use --replace to overwrite."""
    name: str
    """Name of an item or entity."""
    secret: str
    """A secret value to be stored in the secure properties keystore."""
    options: SetSecurePropertyOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "setSecureProperty"

# End Variants for setSecureProperty

# Variants for updateInstallation
@dataclass
class UpdateInstallationOptions:
    """Optional parameters for action updateInstallation"""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""

@dataclass
class UpdateInstallation(SystemCommand):
    """Updates an ACLI installation. When type NEW is requested, file is required to be a directory reference where the installation directory will be installed. Use ~ for the file parameter to locate the installation directory in your user home directory."""
    type: str
    """Type of installation update request."""
    options: UpdateInstallationOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateInstallation"

# End Variants for updateInstallation

# Variants for updatePropertyFile
@dataclass
class UpdatePropertyFileOptions:
    """Optional parameters for action updatePropertyFile"""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""

@dataclass
class UpdatePropertyFile(SystemCommand):
    """Add, update, or remove properties from a property file. If the property file does not exist, an attempt will be made to create it. Special values for the propertyFile parameter are '@config' and '@service' for the ACLI configuration properties and ACLI service configuration properties respectfully. Use one or more field parameters where each field parameter is a key=value pair. An existing property with the same key will be replaced with the new value otherwise a new property will be added with the value. Properties with blank values will be removed. Comments and include references will be preserved."""
    property_file: str
    """Property file with database parameters, field mappings, or client specific information."""
    options: UpdatePropertyFileOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updatePropertyFile"

# End Variants for updatePropertyFile

# Variants for writeFile
@dataclass
class WriteFileOptions:
    """Optional parameters for action writeFile"""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class WriteFileGivenFileAndData(SystemCommand):
    """Save data or input lines into a file. For example, this can be used to create a temporary run script. If the file already exists, either use the replace or append parameters to avoid an error. Options are available to show or run the file after it it saved using '--options show' or '--options run'."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    data: str
    """JSON data for runFromJson. Post data for renderRequest. Action specific definition in some cases."""
    options: WriteFileOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "writeFile"

@dataclass
class WriteFileGivenFileAndInput(SystemCommand):
    """Save data or input lines into a file. For example, this can be used to create a temporary run script. If the file already exists, either use the replace or append parameters to avoid an error. Options are available to show or run the file after it it saved using '--options show' or '--options run'."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: WriteFileOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "writeFile"

# End Variants for writeFile
