from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class AgileCloudCommand(Command):
    pass

@dataclass
class AgileCloudClient(RemoteClient):
    def execute(self, command: AgileCloudCommand):
        return super().do_execute(command)

# Variants for addBoardAdministrators

@dataclass
class AddBoardAdministratorsGivenBoardAndUserId(AgileCloudCommand):
    """Add users and groups as board administrators. Both userId and group can be specified as a comma separated list."""
    board: str
    """Board name or id."""
    user_id: str
    """User id for user management and other actions. For some actions, a comma separated list of ids. For Cloud, use an account id or a public name."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addBoardAdministrators"

@dataclass
class AddBoardAdministratorsGivenBoardAndGroup(AgileCloudCommand):
    """Add users and groups as board administrators. Both userId and group can be specified as a comma separated list."""
    board: str
    """Board name or id."""
    group: str
    """Group name. For some actions addUser, a comma separated list of group names."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addBoardAdministrators"

# End Variants for addBoardAdministrators

# Variants for addBoardColumn
@dataclass
class AddBoardColumnOptions:
    """Optional parameters for action addBoardColumn"""
    status: str|None = None
    """Board column status like to do, in progress, resolved."""
    status_category: str|None = None
    """Board column status category like to do, in progress, done."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class AddBoardColumn(AgileCloudCommand):
    """Use the board parameter for the board. Use the column parameter for the name of the new column. If '--options createAnother' is specified, a new column will be added even if a column exists with the same name. Use the status parameter for status to be mapped to the new column. The status parameter can be a comma separated list of status name or id. The status can be either unmapped or mapped with existing column. Use @default to auto create a status with same name as the new column. Auto creating status is only supported with project associated with simplified workflow. The statusCategory parameter is only used to specify the category of new status which is auto created by this action. Use @default to auto select the default undefined category."""
    board: str
    """Board name or id."""
    column: str
    """Board column name or id."""
    options: AddBoardColumnOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addBoardColumn"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addBoardColumn

# Variants for addIssuesToSprint
@dataclass
class AddIssuesToSprintOptions:
    """Optional parameters for action addIssuesToSprint"""
    jql: str|None = None
    """JQL query. Standard way to specify a search for issues."""
    issue: str|None = None
    """Issue key. For some actions, may be a comma separated list of issue keys."""

@dataclass
class AddIssuesToSprint(AgileCloudCommand):
    """Add issues to a sprint. Limit 50 issues. Use the sprint parameter for the sprint name or id. Use jql to identify issues to add or issue representing a comma separated list of issues or both."""
    sprint: str
    """Sprint name or id."""
    options: AddIssuesToSprintOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addIssuesToSprint"

# End Variants for addIssuesToSprint

# Variants for addQuickFilter
@dataclass
class AddQuickFilterOptions:
    """Optional parameters for action addQuickFilter"""
    description: str|None = None
    """Description."""

@dataclass
class AddQuickFilter(AgileCloudCommand):
    """Add a quick filter to a board. Specify a filter name and a JQL query."""
    board: str
    """Board name or id."""
    filter: str
    """Filter name or id."""
    jql: str
    """JQL query. Standard way to specify a search for issues."""
    options: AddQuickFilterOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addQuickFilter"

# End Variants for addQuickFilter

# Variants for completeSprint

@dataclass
class CompleteSprint(AgileCloudCommand):
    """To complete a sprint. Use the sprint parameter for the sprint name or id."""
    sprint: str
    """Sprint name or id."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "completeSprint"

# End Variants for completeSprint

# Variants for copyBoard
@dataclass
class CopyBoardOptions:
    """Optional parameters for action copyBoard"""
    name: str|None = None
    """Name of an item or entity."""
    reference: str|None = None
    """Reference to a replacement key value used to remember an action specific value like issue key, entity id, or similar so it can be referenced later. Each action that allows this parameter will specify that the reference parameter is valid for the action and the first entry listed for available replacement variables help text will be the value set. If you need access to a different replacement variable in your script, you will need to use the setReplacementVariables action after the action to set a new replacement variable of your choosing to one of the other available replacement variables."""

@dataclass
class CopyBoard(AgileCloudCommand):
    """Copy a board identified by the board name or id using the board parameter. Optionally, use the name parameter to specify the name of the new board."""
    board: str
    """Board name or id."""
    options: CopyBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyBoard"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for copyBoard

# Variants for createBoard
@dataclass
class CreateBoardOptions:
    """Optional parameters for action createBoard"""
    reference: str|None = None
    """Reference to a replacement key value used to remember an action specific value like issue key, entity id, or similar so it can be referenced later. Each action that allows this parameter will specify that the reference parameter is valid for the action and the first entry listed for available replacement variables help text will be the value set. If you need access to a different replacement variable in your script, you will need to use the setReplacementVariables action after the action to set a new replacement variable of your choosing to one of the other available replacement variables."""

@dataclass
class CreateBoardGivenBoardAndTypeAndFilter(AgileCloudCommand):
    """Create a board. Type is any supported type like scrum, kanban, or diy. If a filter is not provided, a filter will be automatically created from the  project parameter representing a comma separated list of projects. For Cloud, the location of the board will be set to the first project provided in the project parameter if provided. That means the board will be located on the board list in the project UI."""
    board: str
    """Board name or id."""
    type: str
    """Board type like scrum, kanban, or DIY (do it yourself)."""
    filter: str
    """Filter name or id."""
    options: CreateBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "createBoard"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class CreateBoardGivenBoardAndTypeAndProject(AgileCloudCommand):
    """Create a board. Type is any supported type like scrum, kanban, or diy. If a filter is not provided, a filter will be automatically created from the  project parameter representing a comma separated list of projects. For Cloud, the location of the board will be set to the first project provided in the project parameter if provided. That means the board will be located on the board list in the project UI."""
    board: str
    """Board name or id."""
    type: str
    """Board type like scrum, kanban, or DIY (do it yourself)."""
    project: str
    """Project key. In some cases, a comma separated list of project keys."""
    options: CreateBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "createBoard"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for createBoard

# Variants for createSprint
@dataclass
class CreateSprintOptions:
    """Optional parameters for action createSprint"""
    start_date: str|None = None
    """Start date of sprint."""
    end_date: str|None = None
    """End date of sprint."""
    reference: str|None = None
    """Reference to a replacement key value used to remember an action specific value like issue key, entity id, or similar so it can be referenced later. Each action that allows this parameter will specify that the reference parameter is valid for the action and the first entry listed for available replacement variables help text will be the value set. If you need access to a different replacement variable in your script, you will need to use the setReplacementVariables action after the action to set a new replacement variable of your choosing to one of the other available replacement variables."""

@dataclass
class CreateSprint(AgileCloudCommand):
    """Create a sprint by name for a board."""
    board: str
    """Board name or id."""
    sprint: str
    """Sprint name or id."""
    options: CreateSprintOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "createSprint"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for createSprint

# Variants for deleteBoard
@dataclass
class DeleteBoardOptions:
    """Optional parameters for action deleteBoard"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    delete_filter: bool|None = None
    """Attempt to delete the filter associated with the board. Filter must be a findable as a favorite filter."""

@dataclass
class DeleteBoard(AgileCloudCommand):
    """Delete a board. Use continue to ignore not found errors. Use the deleteFilter parameter to delete the filter associated with the board. Note that delete filter will also delete all boards associated with the filter."""
    board: str
    """Board name or id."""
    options: DeleteBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "deleteBoard"

# End Variants for deleteBoard

# Variants for deleteSprint
@dataclass
class DeleteSprintOptions:
    """Optional parameters for action deleteSprint"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class DeleteSprint(AgileCloudCommand):
    """Delete a sprint. Use the sprint parameter for sprint name or id. Use continue to ignore not found errors."""
    sprint: str
    """Sprint name or id."""
    options: DeleteSprintOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "deleteSprint"

# End Variants for deleteSprint

# Variants for getBoard
@dataclass
class GetBoardOptions:
    """Optional parameters for action getBoard"""
    type: str|None = None
    """Board type like scrum, kanban, or DIY (do it yourself)."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetBoard(AgileCloudCommand):
    """Get information about a board by board id or name."""
    board: str
    """Board name or id."""
    options: GetBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBoard"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBoard

# Variants for getBoardColumnList
@dataclass
class GetBoardColumnListOptions:
    """Optional parameters for action getBoardColumnList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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

@dataclass
class GetBoardColumnList(AgileCloudCommand):
    """List of board columns with optional filtering by regex on name."""
    board: str
    """Board name or id."""
    options: GetBoardColumnListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBoardColumnList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBoardColumnList

# Variants for getBoardList
@dataclass
class GetBoardListOptions:
    """Optional parameters for action getBoardList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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

@dataclass
class GetBoardList(AgileCloudCommand):
    """List of boards with optional filtering by regex on name."""
    options: GetBoardListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBoardList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBoardList

# Variants for getQuickFilter
@dataclass
class GetQuickFilterOptions:
    """Optional parameters for action getQuickFilter"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetQuickFilter(AgileCloudCommand):
    """Get information about a quick filter."""
    board: str
    """Board name or id."""
    filter: str
    """Filter name or id."""
    options: GetQuickFilterOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getQuickFilter"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getQuickFilter

# Variants for getQuickFilterList
@dataclass
class GetQuickFilterListOptions:
    """Optional parameters for action getQuickFilterList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
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
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetQuickFilterList(AgileCloudCommand):
    """Get quick filters list for a board."""
    board: str
    """Board name or id."""
    options: GetQuickFilterListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getQuickFilterList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getQuickFilterList

# Variants for getServerInfo
@dataclass
class GetServerInfoOptions:
    """Optional parameters for action getServerInfo"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetServerInfo(AgileCloudCommand):
    """Get information about the Jira."""
    options: GetServerInfoOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getServerInfo"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getServerInfo

# Variants for getSprint
@dataclass
class GetSprintOptions:
    """Optional parameters for action getSprint"""
    board: str|None = None
    """Board name or id."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetSprint(AgileCloudCommand):
    """Get information about a sprint. Use the sprint parameter for sprint name or id. Use the board parameter to lookup the sprint in a particular board."""
    sprint: str
    """Sprint name or id."""
    options: GetSprintOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSprint"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getSprint

# Variants for getSprintList
@dataclass
class GetSprintListOptions:
    """Optional parameters for action getSprintList"""
    board: str|None = None
    """Board name or id."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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

@dataclass
class GetSprintList(AgileCloudCommand):
    """List of sprints. If the board parameter is provided, get sprint list for the board. Otherwise, get sprint list for all boards."""
    options: GetSprintListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSprintList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getSprintList

# Variants for releaseVersion
@dataclass
class ReleaseVersionOptions:
    """Optional parameters for action releaseVersion"""
    board: str|None = None
    """Board name or id."""
    description: str|None = None
    """Description."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class ReleaseVersion(AgileCloudCommand):
    """Release a version for a board. Resets release date if provided. Defaults to current server date if release date\n\t is not set. Use continue to ignore error when that the version is already in the correct state."""
    project: str
    """Project key. In some cases, a comma separated list of project keys."""
    version: str
    """Release version name"""
    date: str
    """Release version date"""
    options: ReleaseVersionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "releaseVersion"

# End Variants for releaseVersion

# Variants for removeBoardColumn
@dataclass
class RemoveBoardColumnOptions:
    """Optional parameters for action removeBoardColumn"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveBoardColumn(AgileCloudCommand):
    """Remove board column by id or column name."""
    board: str
    """Board name or id."""
    column: str
    """Board column name or id."""
    options: RemoveBoardColumnOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeBoardColumn"

# End Variants for removeBoardColumn

# Variants for removeQuickFilter

@dataclass
class RemoveQuickFilter(AgileCloudCommand):
    """Remove a quick filter from a board."""
    board: str
    """Board name or id."""
    filter: str
    """Filter name or id."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeQuickFilter"

# End Variants for removeQuickFilter

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
class RenderRequest(AgileCloudCommand):
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

# Variants for runFromBoardList
@dataclass
class RunFromBoardListOptions:
    """Optional parameters for action runFromBoardList"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
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
class RunFromBoardListGivenInput(AgileCloudCommand):
    """Run actions for each board matching selection criteria similar to getBoardList."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromBoardListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBoardList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBoardListGivenCommon(AgileCloudCommand):
    """Run actions for each board matching selection criteria similar to getBoardList."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromBoardListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBoardList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBoardListGivenFile(AgileCloudCommand):
    """Run actions for each board matching selection criteria similar to getBoardList."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromBoardListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBoardList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromBoardList

# Variants for runFromQuickFilterList
@dataclass
class RunFromQuickFilterListOptions:
    """Optional parameters for action runFromQuickFilterList"""
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
class RunFromQuickFilterListGivenBoardAndInput(AgileCloudCommand):
    """Run actions for each board matching selection criteria similar to getQuickFilterList."""
    board: str
    """Board name or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromQuickFilterListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromQuickFilterList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromQuickFilterListGivenBoardAndCommon(AgileCloudCommand):
    """Run actions for each board matching selection criteria similar to getQuickFilterList."""
    board: str
    """Board name or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromQuickFilterListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromQuickFilterList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromQuickFilterListGivenBoardAndFile(AgileCloudCommand):
    """Run actions for each board matching selection criteria similar to getQuickFilterList."""
    board: str
    """Board name or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromQuickFilterListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromQuickFilterList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromQuickFilterList

# Variants for runFromSprintList
@dataclass
class RunFromSprintListOptions:
    """Optional parameters for action runFromSprintList"""
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
class RunFromSprintListGivenBoardAndInput(AgileCloudCommand):
    """Run actions for each sprint matching selection criteria similar to getSprintList."""
    board: str
    """Board name or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromSprintListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSprintList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromSprintListGivenBoardAndCommon(AgileCloudCommand):
    """Run actions for each sprint matching selection criteria similar to getSprintList."""
    board: str
    """Board name or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromSprintListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSprintList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromSprintListGivenBoardAndFile(AgileCloudCommand):
    """Run actions for each sprint matching selection criteria similar to getSprintList."""
    board: str
    """Board name or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromSprintListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSprintList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromSprintList

# Variants for setBoardAdministrators

@dataclass
class SetBoardAdministratorsGivenBoardAndUserId(AgileCloudCommand):
    """Set users and groups as board administrators replacing any previously configured administrators. Both userId and group can be specified as a comma separated list."""
    board: str
    """Board name or id."""
    user_id: str
    """User id for user management and other actions. For some actions, a comma separated list of ids. For Cloud, use an account id or a public name."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "setBoardAdministrators"

@dataclass
class SetBoardAdministratorsGivenBoardAndGroup(AgileCloudCommand):
    """Set users and groups as board administrators replacing any previously configured administrators. Both userId and group can be specified as a comma separated list."""
    board: str
    """Board name or id."""
    group: str
    """Group name. For some actions addUser, a comma separated list of group names."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "setBoardAdministrators"

# End Variants for setBoardAdministrators

# Variants for startSprint
@dataclass
class StartSprintOptions:
    """Optional parameters for action startSprint"""
    start_date: str|None = None
    """Start date of sprint."""
    end_date: str|None = None
    """End date of sprint."""

@dataclass
class StartSprint(AgileCloudCommand):
    """To start a sprint. Use the sprint parameter for the sprint name or id."""
    sprint: str
    """Sprint name or id."""
    options: StartSprintOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "startSprint"

# End Variants for startSprint

# Variants for updateBoard
@dataclass
class UpdateBoardOptions:
    """Optional parameters for action updateBoard"""
    name: str|None = None
    """Name of an item or entity."""
    filter: str|None = None
    """Filter name or id."""
    jql: str|None = None
    """JQL query. Standard way to specify a search for issues."""
    subquery: str|None = None
    """Kanban board sub-filter. Provide further filtering of issues for unreleased work."""
    estimation: str|None = None
    """Scrum board issue estimation statistic."""
    tracking: str|None = None
    """Scrum board time tracking. Provide way to track time against issues."""

@dataclass
class UpdateBoard(AgileCloudCommand):
    """Update the board configuration including name, filter, jql, subquery, estimation and time tracking. Use the estimation parameter for issue estimation statistic. Use the tracking parameter for issue time tracking. Set the tracking parameter to 'None' or @default to track issues with estimation statistic field. Set the tracking parameter to 'Remaining Estimate and Time Spent' or 'Remaining Time Estimate' to track issues with Jira's Remaining Estimate and Time Spent fields. No other values are supported for the tracking parameter."""
    board: str
    """Board name or id."""
    options: UpdateBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateBoard"

# End Variants for updateBoard

# Variants for updateBoardCard
@dataclass
class UpdateBoardCardOptions:
    """Optional parameters for action updateBoardCard"""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    card_type: str|None = None
    """Board card type. For kanban boards, it will be kanban board card. For scrum boards, it can be backlog card or active sprint card."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class UpdateBoardCard(AgileCloudCommand):
    """Update the board card configurations. Use this action to config the board card layout. Use the field parameter to update the list of extra fields shown in the card. Up to three extra fields are allowed. Use the cardType parameter to specify the card to update. For a kanban board, there is only one kanban board card type. The value of the cardType parameter will be defaulted to this type. For a scrum board, there are backlog card and active sprint card types. Set the cardType parameter to '@default' or 'sprint' to update the active sprint card. Set the cardType parameter to 'backlog' to update the backlog card. Set the cardType parameter to '@all' to update both cards together. Use '--options enableDaysInColumn' and '--options disableDaysInColumn' to enable and disable the 'Days in Column' visual indicator."""
    board: str
    """Board name or id."""
    options: UpdateBoardCardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateBoardCard"

# End Variants for updateBoardCard

# Variants for updateBoardColumn
@dataclass
class UpdateBoardColumnOptions:
    """Optional parameters for action updateBoardColumn"""
    name: str|None = None
    """Name of an item or entity."""
    status: str|None = None
    """Board column status like to do, in progress, resolved."""

@dataclass
class UpdateBoardColumn(AgileCloudCommand):
    """Update the board column including name and status. The status parameter is a comma separated list of status names or ids."""
    board: str
    """Board name or id."""
    column: str
    """Board column name or id."""
    options: UpdateBoardColumnOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateBoardColumn"

# End Variants for updateBoardColumn

# Variants for updateQuickFilter
@dataclass
class UpdateQuickFilterOptions:
    """Optional parameters for action updateQuickFilter"""
    name: str|None = None
    """Name of an item or entity."""
    jql: str|None = None
    """JQL query. Standard way to specify a search for issues."""
    description: str|None = None
    """Description."""

@dataclass
class UpdateQuickFilter(AgileCloudCommand):
    """Update a quick filter for a board. You can update the filter name, description, or JQL."""
    board: str
    """Board name or id."""
    filter: str
    """Filter name or id."""
    options: UpdateQuickFilterOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateQuickFilter"

# End Variants for updateQuickFilter

# Variants for updateSprint
@dataclass
class UpdateSprintOptions:
    """Optional parameters for action updateSprint"""
    state: str|None = None
    """Sprint state like future, active, closed."""
    name: str|None = None
    """Name of an item or entity."""
    start_date: str|None = None
    """Start date of sprint."""
    end_date: str|None = None
    """End date of sprint."""

@dataclass
class UpdateSprint(AgileCloudCommand):
    """Update sprint details. Use this action to update sprint details including name, state, start date and end date. Supported states are ACTIVE, FUTURE and CLOSED. Use the sprint parameter for the sprint name or id."""
    sprint: str
    """Sprint name or id."""
    options: UpdateSprintOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateSprint"

# End Variants for updateSprint

# Variants for validateLicense

@dataclass
class ValidateLicense(AgileCloudCommand):
    """Validates the ACLI Connector is enabled and licensed on the server."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "validateLicense"

# End Variants for validateLicense
