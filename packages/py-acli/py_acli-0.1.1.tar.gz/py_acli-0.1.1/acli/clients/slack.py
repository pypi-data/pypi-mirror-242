from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class SlackCommand(Command):
    pass

@dataclass
class SlackClient(RemoteClient):
    def execute(self, command: SlackCommand):
        return super().do_execute(command)

# Variants for addFile
@dataclass
class AddFileOptions:
    """Optional parameters for action addFile"""
    channel: str|None = None
    """Channel name or id."""
    text: str|None = None
    """Message text. Length is limited to 10000 characters."""
    file_name: str|None = None
    """Name of file when shared. Defaults to the name of the file represented by the file parameter."""

@dataclass
class AddFile(SlackCommand):
    """Add (upload) a file. Optionally, share with a channel."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddFileOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addFile"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addFile

# Variants for archiveChannel
@dataclass
class ArchiveChannelOptions:
    """Optional parameters for action archiveChannel"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class ArchiveChannel(SlackCommand):
    """Archive the channel. Use the continue parameter to ignore error if channel is already archived."""
    channel: str
    """Channel name or id."""
    options: ArchiveChannelOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "archiveChannel"

# End Variants for archiveChannel

# Variants for createChannel
@dataclass
class CreateChannelOptions:
    """Optional parameters for action createChannel"""
    topic: str|None = None
    """Channel topic."""
    owner: str|None = None
    """Channel owner by name or id."""
    access: str|None = None
    """Channel access setting. Valid values are: public, private"""
    auto_correct: bool|None = None
    """Automatically correct and trim values that exceed Slack length limits or contain invalid characters."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class CreateChannel(SlackCommand):
    """Create a new channel. Specify continue to ignore already exists error."""
    channel: str
    """Channel name or id."""
    options: CreateChannelOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "createChannel"

# End Variants for createChannel

# Variants for deleteChannel

@dataclass
class DeleteChannel(SlackCommand):
    """Delete a channel by name or id."""
    channel: str
    """Channel name or id."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "deleteChannel"

# End Variants for deleteChannel

# Variants for getChannel
@dataclass
class GetChannelOptions:
    """Optional parameters for action getChannel"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetChannel(SlackCommand):
    """Get channel information by name or id."""
    channel: str
    """Channel name or id."""
    options: GetChannelOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getChannel"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getChannel

# Variants for getChannelHistoryList
@dataclass
class GetChannelHistoryListOptions:
    """Optional parameters for action getChannelHistoryList"""
    from_: str|None = None
    """The earliest message id timestamp or date for a range of messages. Defaults to earliest possible. Combines with the to parameter for a non inclusive range. Refer to the id parameter for more information."""
    to: str|None = None
    """The latest message id timestamp or date for a range of messages. Defaults to latest possible. Combines with the to parameter for a non inclusive range. Refer to the id parameter for more information."""
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
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetChannelHistoryList(SlackCommand):
    """Get a list of messages for a channel matching regex filtering base on message text or content using blocks. Optional from and to parameters allow for additional filtering based on message id or date range. When a specific message id is used, use '--options inclusive' to include the specific message in the result. By default, at most 1000 entries are returned unless the limit parameter is explicitly set to something higher."""
    channel: str
    """Channel name or id."""
    options: GetChannelHistoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getChannelHistoryList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getChannelHistoryList

# Variants for getChannelList
@dataclass
class GetChannelListOptions:
    """Optional parameters for action getChannelList"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    include_private: bool|None = None
    """Include private channels in the list."""
    include_archived: bool|None = None
    """Include archived channels in the list."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetChannelList(SlackCommand):
    """Get a list of channel matching regex filtering on channel name and other selection criteria."""
    options: GetChannelListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getChannelList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getChannelList

# Variants for getFileList
@dataclass
class GetFileListOptions:
    """Optional parameters for action getFileList"""
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
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetFileList(SlackCommand):
    """Get a list of files matching regex filtering on file name and other selection criteria."""
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

# Variants for getMessage
@dataclass
class GetMessageOptions:
    """Optional parameters for action getMessage"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetMessage(SlackCommand):
    """Get message from a channel by id."""
    channel: str
    """Channel name or id."""
    id: str
    """Id of an item. For a message id, it is timestamp based like 1405894322.002768 where the number before the decimal is epoch time in seconds and the optional decimal part represents granularity to nanoseconds. @LAST is also valid for a message id to reference the last message in a channel."""
    options: GetMessageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getMessage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getMessage

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
class GetServerInfo(SlackCommand):
    """Get information about the Slack server."""
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

# Variants for removeFile
@dataclass
class RemoveFileOptions:
    """Optional parameters for action removeFile"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveFile(SlackCommand):
    """Remove a file by name or identifier."""
    name: str
    """Item name. In most cases, an item's id can be a substitute for a name. Example: channel, file, user. Channel names are restricted to 21 characters or less."""
    options: RemoveFileOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeFile"

# End Variants for removeFile

# Variants for removeMessage

@dataclass
class RemoveMessage(SlackCommand):
    """Remove message from a channel by id."""
    channel: str
    """Channel name or id."""
    id: str
    """Id of an item. For a message id, it is timestamp based like 1405894322.002768 where the number before the decimal is epoch time in seconds and the optional decimal part represents granularity to nanoseconds. @LAST is also valid for a message id to reference the last message in a channel."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeMessage"

# End Variants for removeMessage

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
class RenderRequest(SlackCommand):
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

# Variants for runFromChannelHistoryList
@dataclass
class RunFromChannelHistoryListOptions:
    """Optional parameters for action runFromChannelHistoryList"""
    from_: str|None = None
    """The earliest message id timestamp or date for a range of messages. Defaults to earliest possible. Combines with the to parameter for a non inclusive range. Refer to the id parameter for more information."""
    to: str|None = None
    """The latest message id timestamp or date for a range of messages. Defaults to latest possible. Combines with the to parameter for a non inclusive range. Refer to the id parameter for more information."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""
    clear_file_before_append: bool|None = None
    """For run actions, this option will automatically clear an existing file on the first append requested."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class RunFromChannelHistoryListGivenChannelAndInput(SlackCommand):
    """Run an action for each channel history entry matching selection criteria as defined for getChannelHistoryList."""
    channel: str
    """Channel name or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromChannelHistoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromChannelHistoryList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromChannelHistoryListGivenChannelAndCommon(SlackCommand):
    """Run an action for each channel history entry matching selection criteria as defined for getChannelHistoryList."""
    channel: str
    """Channel name or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromChannelHistoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromChannelHistoryList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromChannelHistoryListGivenChannelAndFile(SlackCommand):
    """Run an action for each channel history entry matching selection criteria as defined for getChannelHistoryList."""
    channel: str
    """Channel name or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromChannelHistoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromChannelHistoryList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromChannelHistoryList

# Variants for runFromChannelList
@dataclass
class RunFromChannelListOptions:
    """Optional parameters for action runFromChannelList"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    include_private: bool|None = None
    """Include private channels in the list."""
    include_archived: bool|None = None
    """Include archived channels in the list."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""
    clear_file_before_append: bool|None = None
    """For run actions, this option will automatically clear an existing file on the first append requested."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class RunFromChannelListGivenInput(SlackCommand):
    """Run an action for each channel matching regex filtering on channel name and other selection criteria."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromChannelListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromChannelList"

@dataclass
class RunFromChannelListGivenCommon(SlackCommand):
    """Run an action for each channel matching regex filtering on channel name and other selection criteria."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromChannelListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromChannelList"

@dataclass
class RunFromChannelListGivenFile(SlackCommand):
    """Run an action for each channel matching regex filtering on channel name and other selection criteria."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromChannelListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromChannelList"

# End Variants for runFromChannelList

# Variants for runFromFileList
@dataclass
class RunFromFileListOptions:
    """Optional parameters for action runFromFileList"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""
    clear_file_before_append: bool|None = None
    """For run actions, this option will automatically clear an existing file on the first append requested."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class RunFromFileListGivenInput(SlackCommand):
    """Run an action for each file matching regex filtering on file name and other selection criteria."""
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

@dataclass
class RunFromFileListGivenCommon(SlackCommand):
    """Run an action for each file matching regex filtering on file name and other selection criteria."""
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

@dataclass
class RunFromFileListGivenFile(SlackCommand):
    """Run an action for each file matching regex filtering on file name and other selection criteria."""
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

# End Variants for runFromFileList

# Variants for sendMessage
@dataclass
class SendMessageOptions:
    """Optional parameters for action sendMessage"""
    auto_split: bool|None = None
    """Automatically attempt to split message text that exceed Slack's maximum message length. Message text with lines within the length limit qualify for auto splitting."""
    pin: bool|None = None
    """Pin message to the channel."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class SendMessageGivenChannelAndText(SlackCommand):
    """Send message to a channel by name or id. File contents are appended to the message text. Message text is limited to 40000 characters - longer text will be automatically sent as a file. For simple text content, the text and file parameters will be used with the file content appended to the text parameter value. Use '--options markdown' to tell Slack to interpret the simple text as Slack markdown. Use '--options markdown=code' to have file content treated as a markdown code block (non-proportional font). Richer content can be defined using Slack blocks (JSON format) provided by one or more content parameters and the file parameter. Block compliant JSON will be included from the first content parameter, then the file parameter, and then the remaining content parameters. Simple text content parameters will be converted to simple text blocks as a convenience. When text is provided and the replace parameter is specified, a previous post starting with the same text will be removed before the new message is added. This is helpful for reporting use cases to prevent clutter in the channel. Refer to Slack documentation on block based content. Refer to the Slack markdown reference for the limited support provided for markdown content in Slack."""
    channel: str
    """Channel name or id."""
    text: str
    """Message text. Length is limited to 10000 characters."""
    options: SendMessageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "sendMessage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class SendMessageGivenChannelAndContent(SlackCommand):
    """Send message to a channel by name or id. File contents are appended to the message text. Message text is limited to 40000 characters - longer text will be automatically sent as a file. For simple text content, the text and file parameters will be used with the file content appended to the text parameter value. Use '--options markdown' to tell Slack to interpret the simple text as Slack markdown. Use '--options markdown=code' to have file content treated as a markdown code block (non-proportional font). Richer content can be defined using Slack blocks (JSON format) provided by one or more content parameters and the file parameter. Block compliant JSON will be included from the first content parameter, then the file parameter, and then the remaining content parameters. Simple text content parameters will be converted to simple text blocks as a convenience. When text is provided and the replace parameter is specified, a previous post starting with the same text will be removed before the new message is added. This is helpful for reporting use cases to prevent clutter in the channel. Refer to Slack documentation on block based content. Refer to the Slack markdown reference for the limited support provided for markdown content in Slack."""
    channel: str
    """Channel name or id."""
    content: Iterable[str]
    """Content for sendMessage. Either plain text or block JSON. First content is added before file content and any other content is added after file content."""
    options: SendMessageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "sendMessage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class SendMessageGivenChannelAndFile(SlackCommand):
    """Send message to a channel by name or id. File contents are appended to the message text. Message text is limited to 40000 characters - longer text will be automatically sent as a file. For simple text content, the text and file parameters will be used with the file content appended to the text parameter value. Use '--options markdown' to tell Slack to interpret the simple text as Slack markdown. Use '--options markdown=code' to have file content treated as a markdown code block (non-proportional font). Richer content can be defined using Slack blocks (JSON format) provided by one or more content parameters and the file parameter. Block compliant JSON will be included from the first content parameter, then the file parameter, and then the remaining content parameters. Simple text content parameters will be converted to simple text blocks as a convenience. When text is provided and the replace parameter is specified, a previous post starting with the same text will be removed before the new message is added. This is helpful for reporting use cases to prevent clutter in the channel. Refer to Slack documentation on block based content. Refer to the Slack markdown reference for the limited support provided for markdown content in Slack."""
    channel: str
    """Channel name or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: SendMessageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "sendMessage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for sendMessage

# Variants for shareFile
@dataclass
class ShareFileOptions:
    """Optional parameters for action shareFile"""
    text: str|None = None
    """Message text. Length is limited to 10000 characters."""

@dataclass
class ShareFile(SlackCommand):
    """Share an exist file identified by name or id with a channel. Use addFile if you need to add and share a file."""
    name: str
    """Item name. In most cases, an item's id can be a substitute for a name. Example: channel, file, user. Channel names are restricted to 21 characters or less."""
    channel: str
    """Channel name or id."""
    options: ShareFileOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "shareFile"

# End Variants for shareFile

# Variants for unarchiveChannel
@dataclass
class UnarchiveChannelOptions:
    """Optional parameters for action unarchiveChannel"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class UnarchiveChannel(SlackCommand):
    """Unarchive an archived channel. Use the continue parameter to ignore error if channel is not archived."""
    channel: str
    """Channel name or id."""
    options: UnarchiveChannelOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "unarchiveChannel"

# End Variants for unarchiveChannel

# Variants for updateChannel
@dataclass
class UpdateChannelOptions:
    """Optional parameters for action updateChannel"""
    name: str|None = None
    """Item name. In most cases, an item's id can be a substitute for a name. Example: channel, file, user. Channel names are restricted to 21 characters or less."""
    purpose: str|None = None
    """Channel purpose."""
    topic: str|None = None
    """Channel topic."""

@dataclass
class UpdateChannel(SlackCommand):
    """Update a channel's name, purpose, and topic."""
    channel: str
    """Channel name or id."""
    options: UpdateChannelOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateChannel"

# End Variants for updateChannel

# Variants for updateMessage
@dataclass
class UpdateMessageOptions:
    """Optional parameters for action updateMessage"""
    pin: bool|None = None
    """Pin message to the channel."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class UpdateMessageGivenChannelAndIdAndText(SlackCommand):
    """Update an existing channel message id. Parameters for modifying the existing message are similar to the sendMessage action."""
    channel: str
    """Channel name or id."""
    id: str
    """Id of an item. For a message id, it is timestamp based like 1405894322.002768 where the number before the decimal is epoch time in seconds and the optional decimal part represents granularity to nanoseconds. @LAST is also valid for a message id to reference the last message in a channel."""
    text: str
    """Message text. Length is limited to 10000 characters."""
    options: UpdateMessageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateMessage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class UpdateMessageGivenChannelAndIdAndContent(SlackCommand):
    """Update an existing channel message id. Parameters for modifying the existing message are similar to the sendMessage action."""
    channel: str
    """Channel name or id."""
    id: str
    """Id of an item. For a message id, it is timestamp based like 1405894322.002768 where the number before the decimal is epoch time in seconds and the optional decimal part represents granularity to nanoseconds. @LAST is also valid for a message id to reference the last message in a channel."""
    content: Iterable[str]
    """Content for sendMessage. Either plain text or block JSON. First content is added before file content and any other content is added after file content."""
    options: UpdateMessageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateMessage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class UpdateMessageGivenChannelAndIdAndFile(SlackCommand):
    """Update an existing channel message id. Parameters for modifying the existing message are similar to the sendMessage action."""
    channel: str
    """Channel name or id."""
    id: str
    """Id of an item. For a message id, it is timestamp based like 1405894322.002768 where the number before the decimal is epoch time in seconds and the optional decimal part represents granularity to nanoseconds. @LAST is also valid for a message id to reference the last message in a channel."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: UpdateMessageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateMessage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for updateMessage
