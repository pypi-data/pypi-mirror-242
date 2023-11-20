from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class MondayCommand(Command):
    pass

@dataclass
class MondayClient(RemoteClient):
    def execute(self, command: MondayCommand):
        return super().do_execute(command)

# Variants for addBoard
@dataclass
class AddBoardOptions:
    """Optional parameters for action addBoard"""
    workspace: str|None = None
    """Workspace"""
    type: str|None = None
    """Workspace types are open and closed. Board types are public, private, share. Column types are auto_number, checkbox, country, color_picker, creation_log, date, dependency, dropdown, email, file, hour, item_id, last_updated, link, location, long_text, numbers, people, phone, progress, rating, status, team, tags, text, timeline, time_tracking, vote, week, world_clock."""
    description: str|None = None
    """Item description."""
    wait: bool|None = None
    """Wait for an asynchronous activity to complete or reach a certain state before completing an action. Some actions may also support a timeout parameter that limits how long to wait. Most likely used in scripts where the next action can only be done after all aspects of the current action reach a known state. For monday.com, there are some rare occasions where something added by an action is not immediately visible by a following action. Using the wait parameter will automatically wait briefly in an attempt to avoid this situation."""

@dataclass
class AddBoard(MondayCommand):
    """Add a board to a workspace."""
    board: str
    """Board name or id."""
    options: AddBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addBoard"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addBoard

# Variants for addColumn
@dataclass
class AddColumnOptions:
    """Optional parameters for action addColumn"""
    workspace: str|None = None
    """Workspace"""
    description: str|None = None
    """Item description."""
    wait: bool|None = None
    """Wait for an asynchronous activity to complete or reach a certain state before completing an action. Some actions may also support a timeout parameter that limits how long to wait. Most likely used in scripts where the next action can only be done after all aspects of the current action reach a known state. For monday.com, there are some rare occasions where something added by an action is not immediately visible by a following action. Using the wait parameter will automatically wait briefly in an attempt to avoid this situation."""

@dataclass
class AddColumn(MondayCommand):
    """Add a column to a board."""
    board: str
    """Board name or id."""
    column: str
    """Column name for a board."""
    type: str
    """Workspace types are open and closed. Board types are public, private, share. Column types are auto_number, checkbox, country, color_picker, creation_log, date, dependency, dropdown, email, file, hour, item_id, last_updated, link, location, long_text, numbers, people, phone, progress, rating, status, team, tags, text, timeline, time_tracking, vote, week, world_clock."""
    options: AddColumnOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addColumn"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addColumn

# Variants for addGroup
@dataclass
class AddGroupOptions:
    """Optional parameters for action addGroup"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class AddGroup(MondayCommand):
    """Add a group to a board."""
    board: str
    """Board name or id."""
    group: str
    """Board group name."""
    options: AddGroupOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addGroup"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addGroup

# Variants for addItem
@dataclass
class AddItemOptions:
    """Optional parameters for action addItem"""
    workspace: str|None = None
    """Workspace"""
    group: str|None = None
    """Board group name."""
    wait: bool|None = None
    """Wait for an asynchronous activity to complete or reach a certain state before completing an action. Some actions may also support a timeout parameter that limits how long to wait. Most likely used in scripts where the next action can only be done after all aspects of the current action reach a known state. For monday.com, there are some rare occasions where something added by an action is not immediately visible by a following action. Using the wait parameter will automatically wait briefly in an attempt to avoid this situation."""

@dataclass
class AddItem(MondayCommand):
    """Add an item to a board."""
    board: str
    """Board name or id."""
    item: str
    """Item name or id."""
    options: AddItemOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addItem"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addItem

# Variants for addSubitem
@dataclass
class AddSubitemOptions:
    """Optional parameters for action addSubitem"""
    workspace: str|None = None
    """Workspace"""
    board: str|None = None
    """Board name or id."""
    wait: bool|None = None
    """Wait for an asynchronous activity to complete or reach a certain state before completing an action. Some actions may also support a timeout parameter that limits how long to wait. Most likely used in scripts where the next action can only be done after all aspects of the current action reach a known state. For monday.com, there are some rare occasions where something added by an action is not immediately visible by a following action. Using the wait parameter will automatically wait briefly in an attempt to avoid this situation."""

@dataclass
class AddSubitem(MondayCommand):
    """Add a subitem to an item."""
    item: str
    """Item name or id."""
    subitem: str
    """Subitem name or id."""
    options: AddSubitemOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addSubitem"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addSubitem

# Variants for addSubitemsColumn
@dataclass
class AddSubitemsColumnOptions:
    """Optional parameters for action addSubitemsColumn"""
    workspace: str|None = None
    """Workspace"""
    wait: bool|None = None
    """Wait for an asynchronous activity to complete or reach a certain state before completing an action. Some actions may also support a timeout parameter that limits how long to wait. Most likely used in scripts where the next action can only be done after all aspects of the current action reach a known state. For monday.com, there are some rare occasions where something added by an action is not immediately visible by a following action. Using the wait parameter will automatically wait briefly in an attempt to avoid this situation."""

@dataclass
class AddSubitemsColumn(MondayCommand):
    """Add a column to all subitems."""
    board: str
    """Board name or id."""
    column: str
    """Column name for a board."""
    type: str
    """Workspace types are open and closed. Board types are public, private, share. Column types are auto_number, checkbox, country, color_picker, creation_log, date, dependency, dropdown, email, file, hour, item_id, last_updated, link, location, long_text, numbers, people, phone, progress, rating, status, team, tags, text, timeline, time_tracking, vote, week, world_clock."""
    options: AddSubitemsColumnOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addSubitemsColumn"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addSubitemsColumn

# Variants for addTeamToWorkspace

@dataclass
class AddTeamToWorkspace(MondayCommand):
    """Add team to a workspace."""
    team: str
    """Team name."""
    workspace: str
    """Workspace"""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addTeamToWorkspace"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addTeamToWorkspace

# Variants for addUpdate
@dataclass
class AddUpdateOptions:
    """Optional parameters for action addUpdate"""
    board: str|None = None
    """Board name or id."""
    workspace: str|None = None
    """Workspace"""
    update: str|None = None
    """Update or Reply id or name"""
    wait: bool|None = None
    """Wait for an asynchronous activity to complete or reach a certain state before completing an action. Some actions may also support a timeout parameter that limits how long to wait. Most likely used in scripts where the next action can only be done after all aspects of the current action reach a known state. For monday.com, there are some rare occasions where something added by an action is not immediately visible by a following action. Using the wait parameter will automatically wait briefly in an attempt to avoid this situation."""

@dataclass
class AddUpdate(MondayCommand):
    """Adds an update to an item."""
    item: str
    """Item name or id."""
    text: str
    """Text for things like notifications or updates"""
    options: AddUpdateOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addUpdate"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addUpdate

# Variants for addUserToBoard
@dataclass
class AddUserToBoardOptions:
    """Optional parameters for action addUserToBoard"""
    type: str|None = None
    """Workspace types are open and closed. Board types are public, private, share. Column types are auto_number, checkbox, country, color_picker, creation_log, date, dependency, dropdown, email, file, hour, item_id, last_updated, link, location, long_text, numbers, people, phone, progress, rating, status, team, tags, text, timeline, time_tracking, vote, week, world_clock."""

@dataclass
class AddUserToBoard(MondayCommand):
    """Adds a user as a subscriber to a board or as an owner for a board."""
    user: str
    """User id or name for user management and other actions."""
    workspace: str
    """Workspace"""
    options: AddUserToBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addUserToBoard"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addUserToBoard

# Variants for addUserToWorkspace

@dataclass
class AddUserToWorkspace(MondayCommand):
    """Add user to a workspace."""
    user: str
    """User id or name for user management and other actions."""
    workspace: str
    """Workspace"""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addUserToWorkspace"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addUserToWorkspace

# Variants for addWorkspace
@dataclass
class AddWorkspaceOptions:
    """Optional parameters for action addWorkspace"""
    type: str|None = None
    """Workspace types are open and closed. Board types are public, private, share. Column types are auto_number, checkbox, country, color_picker, creation_log, date, dependency, dropdown, email, file, hour, item_id, last_updated, link, location, long_text, numbers, people, phone, progress, rating, status, team, tags, text, timeline, time_tracking, vote, week, world_clock."""
    description: str|None = None
    """Item description."""
    wait: bool|None = None
    """Wait for an asynchronous activity to complete or reach a certain state before completing an action. Some actions may also support a timeout parameter that limits how long to wait. Most likely used in scripts where the next action can only be done after all aspects of the current action reach a known state. For monday.com, there are some rare occasions where something added by an action is not immediately visible by a following action. Using the wait parameter will automatically wait briefly in an attempt to avoid this situation."""

@dataclass
class AddWorkspace(MondayCommand):
    """Add workspace."""
    workspace: str
    """Workspace"""
    options: AddWorkspaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addWorkspace"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addWorkspace

# Variants for archiveBoard
@dataclass
class ArchiveBoardOptions:
    """Optional parameters for action archiveBoard"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class ArchiveBoard(MondayCommand):
    """Archive board by name or id."""
    board: str
    """Board name or id."""
    options: ArchiveBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "archiveBoard"

# End Variants for archiveBoard

# Variants for copyBoard
@dataclass
class CopyBoardOptions:
    """Optional parameters for action copyBoard"""
    workspace: str|None = None
    """Workspace"""
    description: str|None = None
    """Item description."""
    copy_items: bool|None = None
    """Copy items when copying a board."""
    copy_updates: bool|None = None
    """When copying a board, copy board structure, items, and updates (limited to most recent 100 updates)."""

@dataclass
class CopyBoard(MondayCommand):
    """Copy a board to the same workspace by specifying the name parameter or to a different workspace by specifying the toWorkspace parameter. By default, only the structure of the board will be copied. Specify --copyItems to also copy board items. Specify --copyUpdates to copy items and their updates limited to the latest 100 updates."""
    board: str
    """Board name or id."""
    to_workspace: str
    """To workspace for copy related actions"""
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

# Variants for copyItem
@dataclass
class CopyItemOptions:
    """Optional parameters for action copyItem"""
    copy_updates: bool|None = None
    """When copying a board, copy board structure, items, and updates (limited to most recent 100 updates)."""
    workspace: str|None = None
    """Workspace"""
    board: str|None = None
    """Board name or id."""
    name: str|None = None
    """Name for things like items or boards."""
    to_workspace: str|None = None
    """To workspace for copy related actions"""
    to_board: str|None = None
    """To Board for copy related actions"""
    wait: bool|None = None
    """Wait for an asynchronous activity to complete or reach a certain state before completing an action. Some actions may also support a timeout parameter that limits how long to wait. Most likely used in scripts where the next action can only be done after all aspects of the current action reach a known state. For monday.com, there are some rare occasions where something added by an action is not immediately visible by a following action. Using the wait parameter will automatically wait briefly in an attempt to avoid this situation."""

@dataclass
class CopyItem(MondayCommand):
    """Copies an item by name or id. By default, the item will be copied to the same board. Otherwise, you can use the toBoard and toWorkspace parameters to select a different board. However, in this case, column values of items and sub-items will not be copied unless column names and types are identical. By default, the new item will have the same name as the original suffixed by (copy). However, you can specify another name by using the --name parameter which can contain the placeholder @itemName@ that will be replaced by the name of the copied item. Specify --copyUpdates to copy items and their updates limited to the latest 100 updates."""
    item: str
    """Item name or id."""
    options: CopyItemOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyItem"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for copyItem

# Variants for getAccessToken
@dataclass
class GetAccessTokenOptions:
    """Optional parameters for action getAccessToken"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""

@dataclass
class GetAccessToken(MondayCommand):
    """Get access token for authenticating remote access to monday.com. Resulting token should be used with --token for monday.com actions."""
    options: GetAccessTokenOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAccessToken"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAccessToken

# Variants for getActivityList
@dataclass
class GetActivityListOptions:
    """Optional parameters for action getActivityList"""
    workspace: str|None = None
    """Workspace"""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetActivityList(MondayCommand):
    """Get a list of board activities with regex filtering based on item or column name associated with the activity or change."""
    board: str
    """Board name or id."""
    options: GetActivityListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getActivityList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getActivityList

# Variants for getAuditLogList
@dataclass
class GetAuditLogListOptions:
    """Optional parameters for action getAuditLogList"""
    user: str|None = None
    """User id or name for user management and other actions."""
    data: str|None = None
    """JSON data for runFromJson. Post data for renderRequest. Action specific definition in some cases."""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetAuditLogList(MondayCommand):
    """Get a list of site audit entries with regex filtering on event name. Filter by user name or id using the user parameter. Use the data parameter for more advanced filtering using a JSON formatted string to represent filter conditions. See the filtering section in the monday.com Audit Log API documentation."""
    options: GetAuditLogListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAuditLogList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAuditLogList

# Variants for getBoard
@dataclass
class GetBoardOptions:
    """Optional parameters for action getBoard"""
    workspace: str|None = None
    """Workspace"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetBoard(MondayCommand):
    """Get board information."""
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

# Variants for getBoardList
@dataclass
class GetBoardListOptions:
    """Optional parameters for action getBoardList"""
    workspace: str|None = None
    """Workspace"""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetBoardList(MondayCommand):
    """Get a list of boards with regex filtering based on name. Use workspace parameter to filter by workspace."""
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
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBoardList

# Variants for getBoardViewList
@dataclass
class GetBoardViewListOptions:
    """Optional parameters for action getBoardViewList"""
    workspace: str|None = None
    """Workspace"""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetBoardViewList(MondayCommand):
    """Get a list of board views with regex filtering based on name."""
    board: str
    """Board name or id."""
    options: GetBoardViewListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBoardViewList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBoardViewList

# Variants for getColumn
@dataclass
class GetColumnOptions:
    """Optional parameters for action getColumn"""
    workspace: str|None = None
    """Workspace"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetColumn(MondayCommand):
    """Get board column by column name (title) or id."""
    board: str
    """Board name or id."""
    column: str
    """Column name for a board."""
    options: GetColumnOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getColumn"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getColumn

# Variants for getColumnList
@dataclass
class GetColumnListOptions:
    """Optional parameters for action getColumnList"""
    workspace: str|None = None
    """Workspace"""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetColumnList(MondayCommand):
    """Get a list of columns in a board with regex filtering based on name."""
    board: str
    """Board name or id."""
    options: GetColumnListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getColumnList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getColumnList

# Variants for getGraphqlResult
@dataclass
class GetGraphqlResultOptions:
    """Optional parameters for action getGraphqlResult"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    data: str|None = None
    """JSON data for runFromJson. Post data for renderRequest. Action specific definition in some cases."""
    name: str|None = None
    """Name for things like items or boards."""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetGraphqlResult(MondayCommand):
    """Get the result response from a GraphQL query or mutation request. If the query uses variables, some common variables will be automatically provided like $limit from the limit parameter. Other string variables can be provide by using one or more field parameters using ' key = value' syntax. If you need to provide an operation name especially when the query contains multiple named queries, use the name parameter. However, unfortunately, monday.com does not support setting the operation name nor having multiple operations specified with the query at the time of this note. Use '--query -' to get the query from standard input. Variable types other that strings must be provided with a JSON formatted data parameter. Use the simulate parameter to just log the query without running it."""
    query: str
    """GraphQL query or a reference to a built-in query by name."""
    options: GetGraphqlResultOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getGraphqlResult"

# End Variants for getGraphqlResult

# Variants for getGroup
@dataclass
class GetGroupOptions:
    """Optional parameters for action getGroup"""
    workspace: str|None = None
    """Workspace"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetGroup(MondayCommand):
    """Get group by group name (title) or id."""
    board: str
    """Board name or id."""
    group: str
    """Board group name."""
    options: GetGroupOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getGroup"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getGroup

# Variants for getGroupList
@dataclass
class GetGroupListOptions:
    """Optional parameters for action getGroupList"""
    workspace: str|None = None
    """Workspace"""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetGroupList(MondayCommand):
    """Get a list of groups in a board with regex filtering based on name."""
    board: str
    """Board name or id."""
    options: GetGroupListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getGroupList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getGroupList

# Variants for getItem
@dataclass
class GetItemOptions:
    """Optional parameters for action getItem"""
    board: str|None = None
    """Board name or id."""
    workspace: str|None = None
    """Workspace"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetItem(MondayCommand):
    """Get item by item name or id. The board parameter is required to lookup an item by name."""
    item: str
    """Item name or id."""
    options: GetItemOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getItem"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getItem

# Variants for getItemList
@dataclass
class GetItemListOptions:
    """Optional parameters for action getItemList"""
    workspace: str|None = None
    """Workspace"""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetItemList(MondayCommand):
    """Get a list of items in a board with regex filtering based on name."""
    board: str
    """Board name or id."""
    options: GetItemListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getItemList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getItemList

# Variants for getServerInfo
@dataclass
class GetServerInfoOptions:
    """Optional parameters for action getServerInfo"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetServerInfo(MondayCommand):
    """Get information about your monday.com account."""
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
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getServerInfo

# Variants for getSubitemList
@dataclass
class GetSubitemListOptions:
    """Optional parameters for action getSubitemList"""
    workspace: str|None = None
    """Workspace"""
    board: str|None = None
    """Board name or id."""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetSubitemList(MondayCommand):
    """Get a list of subitems in a board with regex filtering based on name."""
    item: str
    """Item name or id."""
    options: GetSubitemListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSubitemList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getSubitemList

# Variants for getTeam
@dataclass
class GetTeamOptions:
    """Optional parameters for action getTeam"""
    team: str|None = None
    """Team name."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetTeam(MondayCommand):
    """Get team information a specific team specified by name or id."""
    options: GetTeamOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getTeam"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getTeam

# Variants for getTeamList
@dataclass
class GetTeamListOptions:
    """Optional parameters for action getTeamList"""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetTeamList(MondayCommand):
    """Get a list of account teams with regex filtering based on name."""
    options: GetTeamListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getTeamList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getTeamList

# Variants for getUpdateList
@dataclass
class GetUpdateListOptions:
    """Optional parameters for action getUpdateList"""
    workspace: str|None = None
    """Workspace"""
    board: str|None = None
    """Board name or id."""
    item: str|None = None
    """Item name or id."""
    type: str|None = None
    """Workspace types are open and closed. Board types are public, private, share. Column types are auto_number, checkbox, country, color_picker, creation_log, date, dependency, dropdown, email, file, hour, item_id, last_updated, link, location, long_text, numbers, people, phone, progress, rating, status, team, tags, text, timeline, time_tracking, vote, week, world_clock."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetUpdateList(MondayCommand):
    """List of updates and replies from most to least recent. Use the type parameter to filter by update or reply."""
    options: GetUpdateListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getUpdateList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getUpdateList

# Variants for getUser
@dataclass
class GetUserOptions:
    """Optional parameters for action getUser"""
    user: str|None = None
    """User id or name for user management and other actions."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetUser(MondayCommand):
    """Get user information for current user by default or a specific user specified by the name or id using the user parameter."""
    options: GetUserOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getUser"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getUser

# Variants for getUserList
@dataclass
class GetUserListOptions:
    """Optional parameters for action getUserList"""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetUserList(MondayCommand):
    """Get a list of account users with regex filtering based on name."""
    options: GetUserListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getUserList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getUserList

# Variants for getWorkspace
@dataclass
class GetWorkspaceOptions:
    """Optional parameters for action getWorkspace"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetWorkspace(MondayCommand):
    """Get workspace information."""
    workspace: str
    """Workspace"""
    options: GetWorkspaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getWorkspace"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getWorkspace

# Variants for getWorkspaceList
@dataclass
class GetWorkspaceListOptions:
    """Optional parameters for action getWorkspaceList"""
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
    best_view: bool|None = None
    """For list actions, automatically provides easily readable display output. This limits the columns shown to the most likely needed that can be shown in a compact format on the terminal. The results are displayed in text format for easier viewing. The option is ignored if the outputType parameter is used."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetWorkspaceList(MondayCommand):
    """Get a list of workspaces with regex filtering based on name."""
    options: GetWorkspaceListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getWorkspaceList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getWorkspaceList

# Variants for likeUpdate
@dataclass
class LikeUpdateOptions:
    """Optional parameters for action likeUpdate"""
    workspace: str|None = None
    """Workspace"""
    board: str|None = None
    """Board name or id."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class LikeUpdate(MondayCommand):
    """Specifies that you like an update or reply. Specify the update parameter with the id of the update or reply."""
    item: str
    """Item name or id."""
    update: str
    """Update or Reply id or name"""
    options: LikeUpdateOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "likeUpdate"

# End Variants for likeUpdate

# Variants for moveItem
@dataclass
class MoveItemOptions:
    """Optional parameters for action moveItem"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class MoveItem(MondayCommand):
    """Move item by name or id to another group. Board is required to lookup an item or group by name."""
    board: str
    """Board name or id."""
    item: str
    """Item name or id."""
    group: str
    """Board group name."""
    options: MoveItemOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "moveItem"

# End Variants for moveItem

# Variants for moveItemToBoard
@dataclass
class MoveItemToBoardOptions:
    """Optional parameters for action moveItemToBoard"""
    workspace: str|None = None
    """Workspace"""
    board: str|None = None
    """Board name or id."""
    name: str|None = None
    """Name for things like items or boards."""
    to_workspace: str|None = None
    """To workspace for copy related actions"""
    mapping: Iterable[str]|str|None = None
    """Use to specify mapping between a source column and a target column for items using syntax source=target syntax. The left hand side of the equal sign (=) is the id or name of a source column. The right hand side is the id or name of the target column. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    submapping: Iterable[str]|str|None = None
    """Use to specify mapping between a source column and a target column for subitems using syntax source=target syntax. The left hand side of the equal sign (=) is the id or name of a source column. The right hand side is the id or name of the target column. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    to_group: str|None = None
    """To Group for copy or move related actions"""
    auto_column: bool|None = None
    """Automatically adds columns on some actions whose column or mapping parameter references a column that may not exist. Also, when an item has columns that do not exist in the receiving board, the columns are added. This is particularly useful for cloning or moving item operations when source and target boards have different column structures."""

@dataclass
class MoveItemToBoard(MondayCommand):
    """Moves item to another board."""
    item: str
    """Item name or id."""
    to_board: str
    """To Board for copy related actions"""
    options: MoveItemToBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "moveItemToBoard"

# End Variants for moveItemToBoard

# Variants for removeBoard
@dataclass
class RemoveBoardOptions:
    """Optional parameters for action removeBoard"""
    workspace: str|None = None
    """Workspace"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveBoard(MondayCommand):
    """Remove a board by name or id."""
    board: str
    """Board name or id."""
    options: RemoveBoardOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeBoard"

# End Variants for removeBoard

# Variants for removeColumn
@dataclass
class RemoveColumnOptions:
    """Optional parameters for action removeColumn"""
    workspace: str|None = None
    """Workspace"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveColumn(MondayCommand):
    """Remove a column by name or id."""
    board: str
    """Board name or id."""
    column: str
    """Column name for a board."""
    options: RemoveColumnOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeColumn"

# End Variants for removeColumn

# Variants for removeGroup
@dataclass
class RemoveGroupOptions:
    """Optional parameters for action removeGroup"""
    workspace: str|None = None
    """Workspace"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveGroup(MondayCommand):
    """Remove a group by name or id."""
    board: str
    """Board name or id."""
    group: str
    """Board group name."""
    options: RemoveGroupOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeGroup"

# End Variants for removeGroup

# Variants for removeItem
@dataclass
class RemoveItemOptions:
    """Optional parameters for action removeItem"""
    board: str|None = None
    """Board name or id."""
    workspace: str|None = None
    """Workspace"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveItem(MondayCommand):
    """Remove a item by name or id. Board is required to lookup an item by name."""
    item: str
    """Item name or id."""
    options: RemoveItemOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeItem"

# End Variants for removeItem

# Variants for removeTeamFromWorkspace

@dataclass
class RemoveTeamFromWorkspace(MondayCommand):
    """Remove team from a workspace."""
    team: str
    """Team name."""
    workspace: str
    """Workspace"""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeTeamFromWorkspace"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for removeTeamFromWorkspace

# Variants for removeUpdate
@dataclass
class RemoveUpdateOptions:
    """Optional parameters for action removeUpdate"""
    workspace: str|None = None
    """Workspace"""
    board: str|None = None
    """Board name or id."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveUpdate(MondayCommand):
    """Removes an Update or Reply. Specify the update parameter with the id of the update or reply. Specify no update parameter or @all to remove all updates for an item."""
    item: str
    """Item name or id."""
    update: str
    """Update or Reply id or name"""
    options: RemoveUpdateOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeUpdate"

# End Variants for removeUpdate

# Variants for removeUserFromBoard

@dataclass
class RemoveUserFromBoard(MondayCommand):
    """Remove user from a board."""
    user: str
    """User id or name for user management and other actions."""
    workspace: str
    """Workspace"""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeUserFromBoard"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for removeUserFromBoard

# Variants for removeUserFromWorkspace

@dataclass
class RemoveUserFromWorkspace(MondayCommand):
    """Remove user from a workspace."""
    user: str
    """User id or name for user management and other actions."""
    workspace: str
    """Workspace"""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeUserFromWorkspace"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for removeUserFromWorkspace

# Variants for removeWorkspace
@dataclass
class RemoveWorkspaceOptions:
    """Optional parameters for action removeWorkspace"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveWorkspace(MondayCommand):
    """Remove workspace by id."""
    workspace: str
    """Workspace"""
    options: RemoveWorkspaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeWorkspace"

# End Variants for removeWorkspace

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
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""

@dataclass
class RenderRequest(MondayCommand):
    """Render URL based request. URL can be a partial URL for monday.com. For accessing monday.com's GraphQL API, use '--url V2'. monday.com authentication is provided if available on the request when accessing monday.com URLs. The response data modified by optional findReplace processing is returned. Use '--pretty' to format returned JSON data in a more readable form."""
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
    workspace: str|None = None
    """Workspace"""
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
class RunFromBoardListGivenInput(MondayCommand):
    """Run actions for each board with regex filtering on board name equivalent to getBoardList."""
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
class RunFromBoardListGivenCommon(MondayCommand):
    """Run actions for each board with regex filtering on board name equivalent to getBoardList."""
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
class RunFromBoardListGivenFile(MondayCommand):
    """Run actions for each board with regex filtering on board name equivalent to getBoardList."""
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

# Variants for runFromBoardViewList
@dataclass
class RunFromBoardViewListOptions:
    """Optional parameters for action runFromBoardViewList"""
    workspace: str|None = None
    """Workspace"""
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
class RunFromBoardViewListGivenBoardAndInput(MondayCommand):
    """Run actions for each board view with regex filtering on board view name equivalent to getBoardViewList."""
    board: str
    """Board name or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromBoardViewListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBoardViewList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBoardViewListGivenBoardAndCommon(MondayCommand):
    """Run actions for each board view with regex filtering on board view name equivalent to getBoardViewList."""
    board: str
    """Board name or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromBoardViewListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBoardViewList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBoardViewListGivenBoardAndFile(MondayCommand):
    """Run actions for each board view with regex filtering on board view name equivalent to getBoardViewList."""
    board: str
    """Board name or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromBoardViewListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBoardViewList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromBoardViewList

# Variants for runFromColumnList
@dataclass
class RunFromColumnListOptions:
    """Optional parameters for action runFromColumnList"""
    workspace: str|None = None
    """Workspace"""
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
class RunFromColumnListGivenBoardAndInput(MondayCommand):
    """Run actions for each column with regex filtering on column name equivalent to getColumnList."""
    board: str
    """Board name or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromColumnListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromColumnList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromColumnListGivenBoardAndCommon(MondayCommand):
    """Run actions for each column with regex filtering on column name equivalent to getColumnList."""
    board: str
    """Board name or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromColumnListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromColumnList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromColumnListGivenBoardAndFile(MondayCommand):
    """Run actions for each column with regex filtering on column name equivalent to getColumnList."""
    board: str
    """Board name or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromColumnListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromColumnList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromColumnList

# Variants for runFromGraphqlResult
@dataclass
class RunFromGraphqlResultOptions:
    """Optional parameters for action runFromGraphqlResult"""
    data: str|None = None
    """JSON data for runFromJson. Post data for renderRequest. Action specific definition in some cases."""
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
class RunFromGraphqlResultGivenQueryAndListAndInput(MondayCommand):
    """Run actions based on the result of a GraphQL query used for replacement variables and list processing based on standard Json paths specified for list and list2 parameters. Refer to the getGraphqlResult action for more details on that aspect of this support. Similarly, this support is also similar to the runFromJson action. Actions can be specified using input, common, or file parameters. Replacement variables are defined from the JSON data using JsonPath naming convention with dot separators. See the JsonPath reference at https://github.com/json-path/JsonPath/blob/master/README.md."""
    query: str
    """GraphQL query or a reference to a built-in query by name."""
    list: str
    """Comma separated list of entries to populate the entry replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromGraphqlResultOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromGraphqlResult"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromGraphqlResultGivenQueryAndListAndCommon(MondayCommand):
    """Run actions based on the result of a GraphQL query used for replacement variables and list processing based on standard Json paths specified for list and list2 parameters. Refer to the getGraphqlResult action for more details on that aspect of this support. Similarly, this support is also similar to the runFromJson action. Actions can be specified using input, common, or file parameters. Replacement variables are defined from the JSON data using JsonPath naming convention with dot separators. See the JsonPath reference at https://github.com/json-path/JsonPath/blob/master/README.md."""
    query: str
    """GraphQL query or a reference to a built-in query by name."""
    list: str
    """Comma separated list of entries to populate the entry replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromGraphqlResultOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromGraphqlResult"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromGraphqlResultGivenQueryAndListAndFile(MondayCommand):
    """Run actions based on the result of a GraphQL query used for replacement variables and list processing based on standard Json paths specified for list and list2 parameters. Refer to the getGraphqlResult action for more details on that aspect of this support. Similarly, this support is also similar to the runFromJson action. Actions can be specified using input, common, or file parameters. Replacement variables are defined from the JSON data using JsonPath naming convention with dot separators. See the JsonPath reference at https://github.com/json-path/JsonPath/blob/master/README.md."""
    query: str
    """GraphQL query or a reference to a built-in query by name."""
    list: str
    """Comma separated list of entries to populate the entry replacement variable on runFromList. Single quote values containing a comma. Embedded quotes must be escaped."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromGraphqlResultOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromGraphqlResult"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromGraphqlResult

# Variants for runFromGroupList
@dataclass
class RunFromGroupListOptions:
    """Optional parameters for action runFromGroupList"""
    workspace: str|None = None
    """Workspace"""
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
class RunFromGroupListGivenBoardAndInput(MondayCommand):
    """Run actions for each group with regex filtering on group name equivalent to getGroupList."""
    board: str
    """Board name or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromGroupListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromGroupList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromGroupListGivenBoardAndCommon(MondayCommand):
    """Run actions for each group with regex filtering on group name equivalent to getGroupList."""
    board: str
    """Board name or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromGroupListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromGroupList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromGroupListGivenBoardAndFile(MondayCommand):
    """Run actions for each group with regex filtering on group name equivalent to getGroupList."""
    board: str
    """Board name or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromGroupListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromGroupList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromGroupList

# Variants for runFromItemList
@dataclass
class RunFromItemListOptions:
    """Optional parameters for action runFromItemList"""
    workspace: str|None = None
    """Workspace"""
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
class RunFromItemListGivenBoardAndInput(MondayCommand):
    """Run actions for each item with regex filtering on item name equivalent to getItemList."""
    board: str
    """Board name or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromItemListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromItemList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromItemListGivenBoardAndCommon(MondayCommand):
    """Run actions for each item with regex filtering on item name equivalent to getItemList."""
    board: str
    """Board name or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromItemListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromItemList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromItemListGivenBoardAndFile(MondayCommand):
    """Run actions for each item with regex filtering on item name equivalent to getItemList."""
    board: str
    """Board name or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromItemListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromItemList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromItemList

# Variants for runFromTeamList
@dataclass
class RunFromTeamListOptions:
    """Optional parameters for action runFromTeamList"""
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
class RunFromTeamListGivenInput(MondayCommand):
    """Run actions for each team with regex filtering on team name equivalent to getTeamList."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromTeamListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTeamList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromTeamListGivenCommon(MondayCommand):
    """Run actions for each team with regex filtering on team name equivalent to getTeamList."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromTeamListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTeamList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromTeamListGivenFile(MondayCommand):
    """Run actions for each team with regex filtering on team name equivalent to getTeamList."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromTeamListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTeamList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromTeamList

# Variants for runFromUserList
@dataclass
class RunFromUserListOptions:
    """Optional parameters for action runFromUserList"""
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
class RunFromUserListGivenInput(MondayCommand):
    """Run actions for each user with regex filtering on user name equivalent to getUserList."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromUserListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromUserList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromUserListGivenCommon(MondayCommand):
    """Run actions for each user with regex filtering on user name equivalent to getUserList."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromUserListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromUserList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromUserListGivenFile(MondayCommand):
    """Run actions for each user with regex filtering on user name equivalent to getUserList."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromUserListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromUserList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromUserList

# Variants for runFromWorkspaceList
@dataclass
class RunFromWorkspaceListOptions:
    """Optional parameters for action runFromWorkspaceList"""
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
class RunFromWorkspaceListGivenInput(MondayCommand):
    """Run actions for each workspace with regex filtering on workspace name equivalent to getWorkspaceList."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromWorkspaceListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWorkspaceList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromWorkspaceListGivenCommon(MondayCommand):
    """Run actions for each workspace with regex filtering on workspace name equivalent to getWorkspaceList."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromWorkspaceListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWorkspaceList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromWorkspaceListGivenFile(MondayCommand):
    """Run actions for each workspace with regex filtering on workspace name equivalent to getWorkspaceList."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromWorkspaceListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWorkspaceList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromWorkspaceList

# Variants for sendNotification
@dataclass
class SendNotificationOptions:
    """Optional parameters for action sendNotification"""
    user: str|None = None
    """User id or name for user management and other actions."""
    workspace: str|None = None
    """Workspace"""

@dataclass
class SendNotificationGivenTextAndBoard(MondayCommand):
    """Sends a notification related to a board, item, update, or reply to an update. If the user parameter is not specified, the current user will be used."""
    text: str
    """Text for things like notifications or updates"""
    board: str
    """Board name or id."""
    options: SendNotificationOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "sendNotification"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class SendNotificationGivenTextAndItem(MondayCommand):
    """Sends a notification related to a board, item, update, or reply to an update. If the user parameter is not specified, the current user will be used."""
    text: str
    """Text for things like notifications or updates"""
    item: str
    """Item name or id."""
    options: SendNotificationOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "sendNotification"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class SendNotificationGivenTextAndUpdate(MondayCommand):
    """Sends a notification related to a board, item, update, or reply to an update. If the user parameter is not specified, the current user will be used."""
    text: str
    """Text for things like notifications or updates"""
    update: str
    """Update or Reply id or name"""
    options: SendNotificationOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "sendNotification"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for sendNotification

# Variants for updateBoard
@dataclass
class UpdateBoardOptions:
    """Optional parameters for action updateBoard"""
    workspace: str|None = None
    """Workspace"""
    name: str|None = None
    """Name for things like items or boards."""
    description: str|None = None
    """Item description."""

@dataclass
class UpdateBoard(MondayCommand):
    """Change board name or description."""
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
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for updateBoard

# Variants for updateColumn
@dataclass
class UpdateColumnOptions:
    """Optional parameters for action updateColumn"""
    workspace: str|None = None
    """Workspace"""
    name: str|None = None
    """Name for things like items or boards."""
    description: str|None = None
    """Item description."""

@dataclass
class UpdateColumn(MondayCommand):
    """Change column title or description by column name or id."""
    board: str
    """Board name or id."""
    column: str
    """Column name for a board."""
    options: UpdateColumnOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateColumn"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for updateColumn

# Variants for updateItem
@dataclass
class UpdateItemOptions:
    """Optional parameters for action updateItem"""
    workspace: str|None = None
    """Workspace"""
    board: str|None = None
    """Board name or id."""
    name: str|None = None
    """Name for things like items or boards."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""

@dataclass
class UpdateItem(MondayCommand):
    """Change item name or other field values. Use multiple field parameters with 'name=value' syntax. Field can be the unique field id or the case sensitive field name. Item can be identified by item name or id. Board is required to lookup an item by name."""
    item: str
    """Item name or id."""
    options: UpdateItemOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateItem"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for updateItem
