from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class CliCommand(Command):
    pass

@dataclass
class CliClient(Client):
    def execute(self, command: CliCommand):
        return super().do_execute(command)

# Variants for getAutomation
@dataclass
class GetAutomationOptions:
    """Optional parameters for action getAutomation"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
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
    channel: str|None = None
    """Channel name or id to use for slack output type on get actions."""

@dataclass
class GetAutomationGivenName(CliCommand):
    """Get information for an automations specified by name or directory or both. An automation is a directory containing a 'automation.yaml' description and optional ACLI script files or related resources."""
    name: str
    """Name of an item or entity."""
    options: GetAutomationOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAutomation"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetAutomationGivenDirectory(CliCommand):
    """Get information for an automations specified by name or directory or both. An automation is a directory containing a 'automation.yaml' description and optional ACLI script files or related resources."""
    directory: str
    """Usually a reference to a local file system directory. Also, for automation related actions, it can be a repository directory reference or a reference to a Bitbucket Cloud site configuration used to access repository based automations. A site reference is made using the site name prefixed with '@' character."""
    options: GetAutomationOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAutomation"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAutomation

# Variants for getAutomationList
@dataclass
class GetAutomationListOptions:
    """Optional parameters for action getAutomationList"""
    directory: str|None = None
    """Usually a reference to a local file system directory. Also, for automation related actions, it can be a repository directory reference or a reference to a Bitbucket Cloud site configuration used to access repository based automations. A site reference is made using the site name prefixed with '@' character."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
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
    channel: str|None = None
    """Channel name or id to use for slack output type on get actions."""

@dataclass
class GetAutomationList(CliCommand):
    """Get a list of automations with regex filtering on name. An automation is a directory containing a 'automation.yaml' description and optional ACLI script files or related resources."""
    options: GetAutomationListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAutomationList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAutomationList

# Variants for getClientInfo
@dataclass
class GetClientInfoOptions:
    """Optional parameters for action getClientInfo"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class GetClientInfo(CliCommand):
    """Get information about this client."""
    options: GetClientInfoOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getClientInfo"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getClientInfo

# Variants for getReplacementVariableList
@dataclass
class GetReplacementVariableListOptions:
    """Optional parameters for action getReplacementVariableList"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
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
    channel: str|None = None
    """Channel name or id to use for slack output type on get actions."""

@dataclass
class GetReplacementVariableList(CliCommand):
    """Get a list of replacement variable names and values with regex filtering on name. This action is only useful within a run script where replacement variables are remembered."""
    options: GetReplacementVariableListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getReplacementVariableList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getReplacementVariableList

# Variants for getSqlResultList
@dataclass
class GetSqlResultListOptions:
    """Optional parameters for action getSqlResultList"""
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
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    channel: str|None = None
    """Channel name or id to use for slack output type on get actions."""

@dataclass
class GetSqlResultListGivenSqlAndDatabase(CliCommand):
    """Get a list of results from a dynamic SQL query."""
    sql: str
    """SQL select statement used to generate a run script."""
    database: str
    """Database name or reference to a ACLI configuration entry when proceeded with an @ symbol. When referencing a configuration entry, the entry should contain appropriate parameters for for defining access to the database including url and, when necessary, dbUser and dbPassword authentication parameters."""
    options: GetSqlResultListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSqlResultList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetSqlResultListGivenSqlAndUrl(CliCommand):
    """Get a list of results from a dynamic SQL query."""
    sql: str
    """SQL select statement used to generate a run script."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: GetSqlResultListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSqlResultList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetSqlResultListGivenFileAndDatabase(CliCommand):
    """Get a list of results from a dynamic SQL query."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    database: str
    """Database name or reference to a ACLI configuration entry when proceeded with an @ symbol. When referencing a configuration entry, the entry should contain appropriate parameters for for defining access to the database including url and, when necessary, dbUser and dbPassword authentication parameters."""
    options: GetSqlResultListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSqlResultList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetSqlResultListGivenFileAndUrl(CliCommand):
    """Get a list of results from a dynamic SQL query."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: GetSqlResultListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSqlResultList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getSqlResultList

# Variants for help

@dataclass
class Help(CliCommand):
    """Show general help information for the client including actions and parameters. When used on a partial action string, action specific help will be shown."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "help"

# End Variants for help

# Variants for provideFeedback

@dataclass
class ProvideFeedback(CliCommand):
    """Provide feedback, comments, and suggestions to ACLI developers based on your experience with the product. We appreciate all feedback in the spirit of continuous improvement in helping customers with their tasks. For specific product issues and immediate help, please submit a request to our support portal at https://apps.appf.re/acli-support."""
    comment: str
    """Comment text."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "provideFeedback"

# End Variants for provideFeedback

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
class RenderRequest(CliCommand):
    """Deprecated. Use the webRequest action from the web client instead. Render URL based request. URL can be a partial URL. The response data is returned optionally modified by findReplace processing. Use '--pretty' to format returned JSON data in a more readable form. Also, for JSON data, you can use '--options setReplacementVariables'."""
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

# Variants for run
@dataclass
class RunOptions:
    """Optional parameters for action run"""
    common: str|None = None
    """Common parameter string added to all actions in the run script."""
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

@dataclass
class RunGivenInput(CliCommand):
    """Run actions from a file, list of input parameters, or standard input (default). Use one or more field parameters to set replacement variables that can be used in run script actions. This makes it possible to parameterize the script so it can be applied to more general use cases. For example, '--field project=MYPROJECT'. This capability is available for all run type actions."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "run"

@dataclass
class RunGivenFile(CliCommand):
    """Run actions from a file, list of input parameters, or standard input (default). Use one or more field parameters to set replacement variables that can be used in run script actions. This makes it possible to parameterize the script so it can be applied to more general use cases. For example, '--field project=MYPROJECT'. This capability is available for all run type actions."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "run"

# End Variants for run

# Variants for runAutomation
@dataclass
class RunAutomationOptions:
    """Optional parameters for action runAutomation"""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    input: Iterable[str]|str|None = None
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    common: str|None = None
    """Common parameter string added to all actions in the run script."""
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

@dataclass
class RunAutomationGivenName(CliCommand):
    """Run an automation identified by name or directory or both."""
    name: str
    """Name of an item or entity."""
    options: RunAutomationOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runAutomation"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunAutomationGivenDirectory(CliCommand):
    """Run an automation identified by name or directory or both."""
    directory: str
    """Usually a reference to a local file system directory. Also, for automation related actions, it can be a repository directory reference or a reference to a Bitbucket Cloud site configuration used to access repository based automations. A site reference is made using the site name prefixed with '@' character."""
    options: RunAutomationOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runAutomation"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runAutomation

# Variants for runFromAutomationList
@dataclass
class RunFromAutomationListOptions:
    """Optional parameters for action runFromAutomationList"""
    directory: str|None = None
    """Usually a reference to a local file system directory. Also, for automation related actions, it can be a repository directory reference or a reference to a Bitbucket Cloud site configuration used to access repository based automations. A site reference is made using the site name prefixed with '@' character."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
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
class RunFromAutomationListGivenListAndInput(CliCommand):
    """Run actions for each automation with regex filtering on name equivalent to getAutomationList."""
    list: str
    """Comma separated list of entries to populate the entry replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromAutomationListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAutomationList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAutomationListGivenListAndCommon(CliCommand):
    """Run actions for each automation with regex filtering on name equivalent to getAutomationList."""
    list: str
    """Comma separated list of entries to populate the entry replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromAutomationListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAutomationList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAutomationListGivenListAndFile(CliCommand):
    """Run actions for each automation with regex filtering on name equivalent to getAutomationList."""
    list: str
    """Comma separated list of entries to populate the entry replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromAutomationListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAutomationList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromAutomationList

# Variants for runFromCsv
@dataclass
class RunFromCsvOptions:
    """Optional parameters for action runFromCsv"""
    property_file: str|None = None
    """Property file with database parameters, field mappings, or client specific information."""
    common: str|None = None
    """Common parameter string added to all actions in the run script."""
    input: Iterable[str]|str|None = None
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
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

@dataclass
class RunFromCsv(CliCommand):
    """Run actions generated from a CSV file. The default behavior is that each column name that matches a valid parameter for the client generates a parameter with value matching the column value for the row being process. Alternatively, use '--options setReplacementVariables' to change the behavior to set a replacement variable whose key (case sensitive) is the column name with blanks removed and whose value is the value matching the column value for the row being processed."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromCsvOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromCsv"

# End Variants for runFromCsv

# Variants for runFromJson
@dataclass
class RunFromJsonOptions:
    """Optional parameters for action runFromJson"""
    list: str|None = None
    """Comma separated list of entries to populate the entry replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
    list2: str|None = None
    """Comma separated list of entries to populate the entry2 replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
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
class RunFromJsonGivenDataAndCommon(CliCommand):
    """Run actions based on JSON data used for replacement variables and list processing based on standard Json paths specified for list and list2 parameters. Valid JSON data must be provided using the data parameter or file parameter. Actions can be specified using input, common, or file (when not used for data) parameters. Replacement variables are defined from the JSON data using JsonPath naming convention with dot separators. See the JsonPath reference at https://github.com/json-path/JsonPath/blob/master/README.md."""
    data: str
    """JSON data for runFromJson. Post data for renderRequest. Action specific definition in some cases."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromJsonOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromJson"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromJsonGivenDataAndInput(CliCommand):
    """Run actions based on JSON data used for replacement variables and list processing based on standard Json paths specified for list and list2 parameters. Valid JSON data must be provided using the data parameter or file parameter. Actions can be specified using input, common, or file (when not used for data) parameters. Replacement variables are defined from the JSON data using JsonPath naming convention with dot separators. See the JsonPath reference at https://github.com/json-path/JsonPath/blob/master/README.md."""
    data: str
    """JSON data for runFromJson. Post data for renderRequest. Action specific definition in some cases."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromJsonOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromJson"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromJsonGivenFileAndCommon(CliCommand):
    """Run actions based on JSON data used for replacement variables and list processing based on standard Json paths specified for list and list2 parameters. Valid JSON data must be provided using the data parameter or file parameter. Actions can be specified using input, common, or file (when not used for data) parameters. Replacement variables are defined from the JSON data using JsonPath naming convention with dot separators. See the JsonPath reference at https://github.com/json-path/JsonPath/blob/master/README.md."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromJsonOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromJson"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromJsonGivenFileAndInput(CliCommand):
    """Run actions based on JSON data used for replacement variables and list processing based on standard Json paths specified for list and list2 parameters. Valid JSON data must be provided using the data parameter or file parameter. Actions can be specified using input, common, or file (when not used for data) parameters. Replacement variables are defined from the JSON data using JsonPath naming convention with dot separators. See the JsonPath reference at https://github.com/json-path/JsonPath/blob/master/README.md."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromJsonOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromJson"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromJson

# Variants for runFromList
@dataclass
class RunFromListOptions:
    """Optional parameters for action runFromList"""
    list2: str|None = None
    """Comma separated list of entries to populate the entry2 replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
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
class RunFromListGivenListAndInput(CliCommand):
    """Run actions for each entry in a list with corresponding entry replacement variable. When file is provided, each action in the file augmented by the common parameter will be run for each entry. Otherwise, just the action specified by the common parameter will be run. When available, list2 entries provide values for the entry2 replacement variable. By default, the entry2 replacement variable is set in parallel with entry replacement variables for each action run. However, if '--options listProcessing=serial' is specified, each combination of entries from list and list2 will cause an action to run. Use one or more field parameters to set replacement variables that can be used in run script actions. This makes it possible to parameterize the script so it can be applied to more general use cases. For example, '--field project=MYPROJECT'."""
    list: str
    """Comma separated list of entries to populate the entry replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromListGivenListAndCommon(CliCommand):
    """Run actions for each entry in a list with corresponding entry replacement variable. When file is provided, each action in the file augmented by the common parameter will be run for each entry. Otherwise, just the action specified by the common parameter will be run. When available, list2 entries provide values for the entry2 replacement variable. By default, the entry2 replacement variable is set in parallel with entry replacement variables for each action run. However, if '--options listProcessing=serial' is specified, each combination of entries from list and list2 will cause an action to run. Use one or more field parameters to set replacement variables that can be used in run script actions. This makes it possible to parameterize the script so it can be applied to more general use cases. For example, '--field project=MYPROJECT'."""
    list: str
    """Comma separated list of entries to populate the entry replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromListGivenListAndFile(CliCommand):
    """Run actions for each entry in a list with corresponding entry replacement variable. When file is provided, each action in the file augmented by the common parameter will be run for each entry. Otherwise, just the action specified by the common parameter will be run. When available, list2 entries provide values for the entry2 replacement variable. By default, the entry2 replacement variable is set in parallel with entry replacement variables for each action run. However, if '--options listProcessing=serial' is specified, each combination of entries from list and list2 will cause an action to run. Use one or more field parameters to set replacement variables that can be used in run script actions. This makes it possible to parameterize the script so it can be applied to more general use cases. For example, '--field project=MYPROJECT'."""
    list: str
    """Comma separated list of entries to populate the entry replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromList

# Variants for runFromPropertyFile
@dataclass
class RunFromPropertyFileOptions:
    """Optional parameters for action runFromPropertyFile"""
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
class RunFromPropertyFileGivenPropertyFileAndInput(CliCommand):
    """Run actions for each entry from a (Java) property file."""
    property_file: str
    """Property file with database parameters, field mappings, or client specific information."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromPropertyFileOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPropertyFile"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPropertyFileGivenPropertyFileAndCommon(CliCommand):
    """Run actions for each entry from a (Java) property file."""
    property_file: str
    """Property file with database parameters, field mappings, or client specific information."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromPropertyFileOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPropertyFile"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPropertyFileGivenPropertyFileAndFile(CliCommand):
    """Run actions for each entry from a (Java) property file."""
    property_file: str
    """Property file with database parameters, field mappings, or client specific information."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromPropertyFileOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPropertyFile"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromPropertyFile

# Variants for runFromSql
@dataclass
class RunFromSqlOptions:
    """Optional parameters for action runFromSql"""
    db_user: str|None = None
    """Database user name. Defaults to the same as the user parameter."""
    db_password: str|None = None
    """Database user password. Defaults to password."""
    property_file: str|None = None
    """Property file with database parameters, field mappings, or client specific information."""
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

@dataclass
class RunFromSqlGivenSqlAndFileAndDatabase(CliCommand):
    """Run actions generated by SQL provided by the sql parameter, a file, or standard input. Replacement variables will be set representing each column (case sensitive, blanks removed) in the result set and the corresponding column value for each row processed."""
    sql: str
    """SQL select statement used to generate a run script."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    database: str
    """Database name or reference to a ACLI configuration entry when proceeded with an @ symbol. When referencing a configuration entry, the entry should contain appropriate parameters for for defining access to the database including url and, when necessary, dbUser and dbPassword authentication parameters."""
    options: RunFromSqlOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSql"

@dataclass
class RunFromSqlGivenSqlAndFileAndUrl(CliCommand):
    """Run actions generated by SQL provided by the sql parameter, a file, or standard input. Replacement variables will be set representing each column (case sensitive, blanks removed) in the result set and the corresponding column value for each row processed."""
    sql: str
    """SQL select statement used to generate a run script."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: RunFromSqlOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSql"

@dataclass
class RunFromSqlGivenSqlAndCommonAndDatabase(CliCommand):
    """Run actions generated by SQL provided by the sql parameter, a file, or standard input. Replacement variables will be set representing each column (case sensitive, blanks removed) in the result set and the corresponding column value for each row processed."""
    sql: str
    """SQL select statement used to generate a run script."""
    common: str
    """Common parameter string added to all actions in the run script."""
    database: str
    """Database name or reference to a ACLI configuration entry when proceeded with an @ symbol. When referencing a configuration entry, the entry should contain appropriate parameters for for defining access to the database including url and, when necessary, dbUser and dbPassword authentication parameters."""
    options: RunFromSqlOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSql"

@dataclass
class RunFromSqlGivenSqlAndCommonAndUrl(CliCommand):
    """Run actions generated by SQL provided by the sql parameter, a file, or standard input. Replacement variables will be set representing each column (case sensitive, blanks removed) in the result set and the corresponding column value for each row processed."""
    sql: str
    """SQL select statement used to generate a run script."""
    common: str
    """Common parameter string added to all actions in the run script."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: RunFromSqlOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSql"

@dataclass
class RunFromSqlGivenSqlAndInputAndDatabase(CliCommand):
    """Run actions generated by SQL provided by the sql parameter, a file, or standard input. Replacement variables will be set representing each column (case sensitive, blanks removed) in the result set and the corresponding column value for each row processed."""
    sql: str
    """SQL select statement used to generate a run script."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    database: str
    """Database name or reference to a ACLI configuration entry when proceeded with an @ symbol. When referencing a configuration entry, the entry should contain appropriate parameters for for defining access to the database including url and, when necessary, dbUser and dbPassword authentication parameters."""
    options: RunFromSqlOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSql"

@dataclass
class RunFromSqlGivenSqlAndInputAndUrl(CliCommand):
    """Run actions generated by SQL provided by the sql parameter, a file, or standard input. Replacement variables will be set representing each column (case sensitive, blanks removed) in the result set and the corresponding column value for each row processed."""
    sql: str
    """SQL select statement used to generate a run script."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: RunFromSqlOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSql"

# End Variants for runFromSql

# Variants for runIf
@dataclass
class RunIfOptions:
    """Optional parameters for action runIf"""
    value: str|None = None
    """Field value or condition value for matching."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    common: str|None = None
    """Common parameter string added to all actions in the run script."""
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

@dataclass
class RunIfGivenRegexAndFile(CliCommand):
    """Run actions only if a regex based condition is met. Other parameters and behavior are the same as the run action. By default the regex is used for a find of the value parameter. The options parameter can be set to one or more of the following to modify the default behavior. literal - to treat the regex string as a literal string, exact - to require an exact match of the value, negative - to reverse the condition so a match means do NOT run action. In addition, use '--regex ""' to match on an empty string. Use one or more field parameters to set replacement variables that can be used in run script actions. This makes it possible to parameterize the script so it can be applied to more general use cases. For example, '--field project=MYPROJECT'."""
    regex: str
    """Regular expression for condition matching or list filtering."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunIfOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runIf"

@dataclass
class RunIfGivenRegexAndInput(CliCommand):
    """Run actions only if a regex based condition is met. Other parameters and behavior are the same as the run action. By default the regex is used for a find of the value parameter. The options parameter can be set to one or more of the following to modify the default behavior. literal - to treat the regex string as a literal string, exact - to require an exact match of the value, negative - to reverse the condition so a match means do NOT run action. In addition, use '--regex ""' to match on an empty string. Use one or more field parameters to set replacement variables that can be used in run script actions. This makes it possible to parameterize the script so it can be applied to more general use cases. For example, '--field project=MYPROJECT'."""
    regex: str
    """Regular expression for condition matching or list filtering."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunIfOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runIf"

# End Variants for runIf

# Variants for setReplacementVariables
@dataclass
class SetReplacementVariablesOptions:
    """Optional parameters for action setReplacementVariables"""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    value: str|None = None
    """Field value or condition value for matching."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class SetReplacementVariables(CliCommand):
    """Set one or more replacement variables specified using field parameters with name=value syntax or loaded from a property file. Value specified replaces any previously set variable with the same name including values set by other actions that set replacement variables. This is an example to save a previously set value, use '--field myIssue=@issue@'. Find and replace logic is applied to the value before setting the variable providing a way to manipulate values in a script. Variables are available only within the scope of the run script they were set in. If a regex based condition is provide using the regex and value parameters, the variables will only be set if the regex condition is met. By default, the regex is used for a find of the value parameter. The options parameter can be set to one or more of the following to modify the default behavior - literal - to treat the regex string as a literal string, exact - to require an exact match of the value, negative - to reverse the condition so a match means do NOT set the variables. In addition, use blank for the regex parameter to match on an empty string."""
    options: SetReplacementVariablesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "setReplacementVariables"

# End Variants for setReplacementVariables

# Variants for sleep
@dataclass
class SleepOptions:
    """Optional parameters for action sleep"""
    value: str|None = None
    """Field value or condition value for matching."""

@dataclass
class Sleep(CliCommand):
    """Sleep a number of seconds. Defaults to 1 second. Use in ACLI scripts that may need to wait before proceeding to the next action. For instance, waiting for server to complete updating search indexes or polling type scenarios."""
    options: SleepOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "sleep"

# End Variants for sleep
