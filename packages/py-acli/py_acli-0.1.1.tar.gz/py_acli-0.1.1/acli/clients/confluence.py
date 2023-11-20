from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class ConfluenceCommand(Command):
    pass

@dataclass
class ConfluenceClient(RemoteClient):
    def execute(self, command: ConfluenceCommand):
        return super().do_execute(command)

# Variants for addApplicationLink
@dataclass
class AddApplicationLinkOptions:
    """Optional parameters for action addApplicationLink"""
    name: str|None = None
    """Space name or file name for attachment."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class AddApplicationLink(ConfluenceCommand):
    """Add an application link to another application. By default, both incoming and outgoing links are enabled and configured without impersonation (users are not shared). Use the options parameter to customize the behavior. Use '--options impersonate' to enable shared users for server. Other examples are '--options disableIncoming' and '--options disableOutgoing'. If another link of the same type already exists as primary, use '--options primary' to force the new link to be primary instead."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: AddApplicationLinkOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addApplicationLink"

# End Variants for addApplicationLink

# Variants for addAttachment
@dataclass
class AddAttachmentOptions:
    """Optional parameters for action addAttachment"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    mime: str|None = None
    """Attachment mime type if you want to override determination by file extension."""
    comment: str|None = None
    """Comment text."""
    minor: bool|None = None
    """Indicate minor update (no notifications) for a page update or attachment create."""
    labels: str|None = None
    """Comma separated list of labels."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class AddAttachmentGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Add an attachment to a page. Use minor to avoid notifications."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddAttachmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addAttachment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddAttachmentGivenSpaceAndTitleAndContentAndName(ConfluenceCommand):
    """Add an attachment to a page. Use minor to avoid notifications."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    content: str
    """Content for page, attachment, comment, or question."""
    name: str
    """Space name or file name for attachment."""
    options: AddAttachmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addAttachment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddAttachmentGivenIdAndFile(ConfluenceCommand):
    """Add an attachment to a page. Use minor to avoid notifications."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddAttachmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addAttachment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddAttachmentGivenIdAndContentAndName(ConfluenceCommand):
    """Add an attachment to a page. Use minor to avoid notifications."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    content: str
    """Content for page, attachment, comment, or question."""
    name: str
    """Space name or file name for attachment."""
    options: AddAttachmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addAttachment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addAttachment

# Variants for addAttachments
@dataclass
class AddAttachmentsOptions:
    """Optional parameters for action addAttachments"""
    recursive: bool|None = None
    """Include sub-directories."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    mime: str|None = None
    """Attachment mime type if you want to override determination by file extension."""
    comment: str|None = None
    """Comment text."""
    minor: bool|None = None
    """Indicate minor update (no notifications) for a page update or attachment create."""
    labels: str|None = None
    """Comma separated list of labels."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class AddAttachments(ConfluenceCommand):
    """Add multiple attachments from a directory matching a regex pattern. Use minor to avoid notifications. Use recursive to find files in sub-directories."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddAttachmentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addAttachments"

# End Variants for addAttachments

# Variants for addBlog
@dataclass
class AddBlogOptions:
    """Optional parameters for action addBlog"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    labels: str|None = None
    """Comma separated list of labels."""
    content2: str|None = None
    """Content for page added after content and file content."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    no_convert: bool|None = None
    """Do not convert content from wiki to storage format. Unless otherwise known, content is considered as wiki markup and converted."""
    markdown: bool|None = None
    """Attempt to convert rendered Markdown content to storage format. This may not work for all Markdown content. Consider using the markdown macro instead for a more accurate display of Markdown content in Confluence."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class AddBlogGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Add a blog entry."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addBlog"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddBlogGivenSpaceAndTitleAndContent(ConfluenceCommand):
    """Add a blog entry."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    content: str
    """Content for page, attachment, comment, or question."""
    options: AddBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addBlog"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addBlog

# Variants for addComment
@dataclass
class AddCommentOptions:
    """Optional parameters for action addComment"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    id: str|None = None
    """Numeric id of an item like a page, blog, or comment."""
    no_convert: bool|None = None
    """Do not convert content from wiki to storage format. Unless otherwise known, content is considered as wiki markup and converted."""
    markdown: bool|None = None
    """Attempt to convert rendered Markdown content to storage format. This may not work for all Markdown content. Consider using the markdown macro instead for a more accurate display of Markdown content in Confluence."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class AddCommentGivenSpaceAndTitleAndComment(ConfluenceCommand):
    """Add a comment to a page or blog. To add a threaded comment, specify parent comment id."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    comment: str
    """Comment text."""
    options: AddCommentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addComment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddCommentGivenSpaceAndTitleAndContent(ConfluenceCommand):
    """Add a comment to a page or blog. To add a threaded comment, specify parent comment id."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    content: str
    """Content for page, attachment, comment, or question."""
    options: AddCommentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addComment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddCommentGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Add a comment to a page or blog. To add a threaded comment, specify parent comment id."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddCommentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addComment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addComment

# Variants for addGroup
@dataclass
class AddGroupOptions:
    """Optional parameters for action addGroup"""
    preserve_case: bool|None = None
    """Some actions like addUser and addGroup may automatically lowercase names usually because the construct is case insensitive on some hosting platforms. Use this switch to override the default behavior and preserve the case."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class AddGroup(ConfluenceCommand):
    """Add a new group."""
    group: str
    """Group name. In the case of addUser, a comma separated list of group names."""
    options: AddGroupOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addGroup"

# End Variants for addGroup

# Variants for addLabels
@dataclass
class AddLabelsOptions:
    """Optional parameters for action addLabels"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str|None = None
    """Space name or file name for attachment."""
    version: str|None = None
    """Item version."""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""

@dataclass
class AddLabelsGivenSpaceAndLabels(ConfluenceCommand):
    """Add labels to a page, blog, space, or attachment. For an attachment, provide either the attachment numeric id or the attachment name together with a content id or space and title."""
    space: str
    """Space key. For some actions, a space name may also work."""
    labels: str
    """Comma separated list of labels."""
    options: AddLabelsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addLabels"

@dataclass
class AddLabelsGivenIdAndLabels(ConfluenceCommand):
    """Add labels to a page, blog, space, or attachment. For an attachment, provide either the attachment numeric id or the attachment name together with a content id or space and title."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    labels: str
    """Comma separated list of labels."""
    options: AddLabelsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addLabels"

# End Variants for addLabels

# Variants for addLicense
@dataclass
class AddLicenseOptions:
    """Optional parameters for action addLicense"""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class AddLicenseGivenAppAndLicense(ConfluenceCommand):
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
class AddLicenseGivenAppAndFile(ConfluenceCommand):
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
class AddLicenses(ConfluenceCommand):
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

# Variants for addPage
@dataclass
class AddPageOptions:
    """Optional parameters for action addPage"""
    parent: str|None = None
    """Parent page title or id. @home title references space's home page."""
    labels: str|None = None
    """Comma separated list of labels."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    content2: str|None = None
    """Content for page added after content and file content."""
    type: str|None = None
    """Application type, shortcut type, or similar depending on context."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    no_convert: bool|None = None
    """Do not convert content from wiki to storage format. Unless otherwise known, content is considered as wiki markup and converted."""
    markdown: bool|None = None
    """Attempt to convert rendered Markdown content to storage format. This may not work for all Markdown content. Consider using the markdown macro instead for a more accurate display of Markdown content in Confluence."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class AddPageGivenSpaceAndTitleAndContent(ConfluenceCommand):
    """Create or update a page. Content for the page is provided by one or more of the content, content2, and file parameters. If more than once of these is used, they ordering on the page is first the content parameter value, followed by a copy of the data from the file parameter, and then followed by the content2 parameter value. This allows you to wrap file content be before and after content which is important in many scenarios. For example, Confluence wiki macros can be used to wrap file content in this way. For instance, markdown content using the markdown macro like '--content "{markdown}" --file my.md --content2 "{markdown}"'. By default, content is treated as Confluence wiki markup. Use '--noConvert' to instead treat as simple text. To convert markdown content to Confluence native content, use '--markdown' with the warning that this may degrade the formatting and may need manual repair. For HTML content, you may want ACLI to automatically modify the HTML to convert some HTML constructs to Confluence native support like anchors and anchor links. Use '--modifyHtml' to request this support. HTML content may still need additional modification or manual repair for better migration to Confluence. Find replace parameters can be used to modify content prior to inserting into the page. This is an important technique for migrating content."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    content: str
    """Content for page, attachment, comment, or question."""
    options: AddPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addPage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddPageGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Create or update a page. Content for the page is provided by one or more of the content, content2, and file parameters. If more than once of these is used, they ordering on the page is first the content parameter value, followed by a copy of the data from the file parameter, and then followed by the content2 parameter value. This allows you to wrap file content be before and after content which is important in many scenarios. For example, Confluence wiki macros can be used to wrap file content in this way. For instance, markdown content using the markdown macro like '--content "{markdown}" --file my.md --content2 "{markdown}"'. By default, content is treated as Confluence wiki markup. Use '--noConvert' to instead treat as simple text. To convert markdown content to Confluence native content, use '--markdown' with the warning that this may degrade the formatting and may need manual repair. For HTML content, you may want ACLI to automatically modify the HTML to convert some HTML constructs to Confluence native support like anchors and anchor links. Use '--modifyHtml' to request this support. HTML content may still need additional modification or manual repair for better migration to Confluence. Find replace parameters can be used to modify content prior to inserting into the page. This is an important technique for migrating content."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addPage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addPage

# Variants for addPermissions
@dataclass
class AddPermissionsOptions:
    """Optional parameters for action addPermissions"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    id: str|None = None
    """Numeric id of an item like a page, blog, or comment."""
    children: bool|None = None
    """Immediate children for a page."""
    descendents: bool|None = None
    """All descendents for a page."""

@dataclass
class AddPermissionsGivenSpaceAndPermissionsAndGroup(ConfluenceCommand):
    """Add permissions to page, blog, or space. For page/blog permissions, use space and title or id of page. For blog permissions, use space and id of blog. Valid page/blog permissions are: [View, Edit]. For space permissions, a permission of @all can be used. Valid space permissions are: [VIEWSPACE, REMOVEOWNCONTENT, EDITSPACE, REMOVEPAGE, EDITBLOG, REMOVEBLOG, CREATEATTACHMENT, REMOVEATTACHMENT, COMMENT, REMOVECOMMENT, SETPAGEPERMISSIONS, REMOVEMAIL, EXPORTSPACE, SETSPACEPERMISSIONS]. Group or userId can also be a comma separated list of groups and userIds. Space permission support not available for Cloud."""
    space: str
    """Space key. For some actions, a space name may also work."""
    permissions: str
    """Comma separated list of permissions. Page permissions:  view, edit. Space permissions: viewspace, removeowncontent, editspace, removepage, editblog, removeblog, createattachment, removeattachment, comment, removecomment, setpagepermissions, removemail, exportspace, setspacepermissions."""
    group: str
    """Group name. In the case of addUser, a comma separated list of group names."""
    options: AddPermissionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addPermissions"

@dataclass
class AddPermissionsGivenSpaceAndPermissionsAndUserId(ConfluenceCommand):
    """Add permissions to page, blog, or space. For page/blog permissions, use space and title or id of page. For blog permissions, use space and id of blog. Valid page/blog permissions are: [View, Edit]. For space permissions, a permission of @all can be used. Valid space permissions are: [VIEWSPACE, REMOVEOWNCONTENT, EDITSPACE, REMOVEPAGE, EDITBLOG, REMOVEBLOG, CREATEATTACHMENT, REMOVEATTACHMENT, COMMENT, REMOVECOMMENT, SETPAGEPERMISSIONS, REMOVEMAIL, EXPORTSPACE, SETSPACEPERMISSIONS]. Group or userId can also be a comma separated list of groups and userIds. Space permission support not available for Cloud."""
    space: str
    """Space key. For some actions, a space name may also work."""
    permissions: str
    """Comma separated list of permissions. Page permissions:  view, edit. Space permissions: viewspace, removeowncontent, editspace, removepage, editblog, removeblog, createattachment, removeattachment, comment, removecomment, setpagepermissions, removemail, exportspace, setspacepermissions."""
    user_id: str
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    options: AddPermissionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addPermissions"

# End Variants for addPermissions

# Variants for addQuestion
@dataclass
class AddQuestionOptions:
    """Optional parameters for action addQuestion"""
    content: str|None = None
    """Content for page, attachment, comment, or question."""

@dataclass
class AddQuestion(ConfluenceCommand):
    """Add a question to Confluence Questions. Not available for Cloud."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    topic: str
    """Confluence Questions topic."""
    options: AddQuestionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addQuestion"

# End Variants for addQuestion

# Variants for addQuestionWatch

@dataclass
class AddQuestionWatchGivenId(ConfluenceCommand):
    """Set to watch a question for the current user. Use @all for title to set the watch all flag. Not available for Cloud."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addQuestionWatch"

@dataclass
class AddQuestionWatchGivenTitle(ConfluenceCommand):
    """Set to watch a question for the current user. Use @all for title to set the watch all flag. Not available for Cloud."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addQuestionWatch"

# End Variants for addQuestionWatch

# Variants for addShortcut
@dataclass
class AddShortcutOptions:
    """Optional parameters for action addShortcut"""
    name: str|None = None
    """Space name or file name for attachment."""

@dataclass
class AddShortcutGivenSpaceAndTitle(ConfluenceCommand):
    """Add a shortcut. Shortcuts show up on the UI. The shortcut name will be defaulted if name is not provided."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: AddShortcutOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addShortcut"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddShortcutGivenSpaceAndId(ConfluenceCommand):
    """Add a shortcut. Shortcuts show up on the UI. The shortcut name will be defaulted if name is not provided."""
    space: str
    """Space key. For some actions, a space name may also work."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: AddShortcutOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addShortcut"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddShortcutGivenSpaceAndUrl(ConfluenceCommand):
    """Add a shortcut. Shortcuts show up on the UI. The shortcut name will be defaulted if name is not provided."""
    space: str
    """Space key. For some actions, a space name may also work."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: AddShortcutOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addShortcut"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addShortcut

# Variants for addSpace
@dataclass
class AddSpaceOptions:
    """Optional parameters for action addSpace"""
    name: str|None = None
    """Space name or file name for attachment."""
    description: str|None = None
    """Descriptive text."""
    home: str|None = None
    """Title of home page for a space. Default for a new space is Home."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    blueprint: str|None = None
    """Space blueprint name or id used for addSpace to create non-personal spaces."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class AddSpaceGivenSpace(ConfluenceCommand):
    """Add a new space. Use '--continue' to ignore an already exists error. In the case of ignoring an existing space, you can also use '--options clearContent' to remove existing content."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: AddSpaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addSpace"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddSpaceGivenUserId(ConfluenceCommand):
    """Add a new space. Use '--continue' to ignore an already exists error. In the case of ignoring an existing space, you can also use '--options clearContent' to remove existing content."""
    user_id: str
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    options: AddSpaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addSpace"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addSpace

# Variants for addTopic
@dataclass
class AddTopicOptions:
    """Optional parameters for action addTopic"""
    description: str|None = None
    """Descriptive text."""
    featured: bool|None = None
    """Confluence Questions featured topic."""
    avatar: str|None = None
    """Topic avatar URL."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""

@dataclass
class AddTopicGivenTopic(ConfluenceCommand):
    """Add a Confluence Questions topic. Not available for Cloud."""
    topic: str
    """Confluence Questions topic."""
    options: AddTopicOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addTopic"

@dataclass
class AddTopicGivenName(ConfluenceCommand):
    """Add a Confluence Questions topic. Not available for Cloud."""
    name: str
    """Space name or file name for attachment."""
    options: AddTopicOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addTopic"

# End Variants for addTopic

# Variants for addTopicWatch

@dataclass
class AddTopicWatchGivenTopic(ConfluenceCommand):
    """Set to watch this topic for the current user. Not available for Cloud."""
    topic: str
    """Confluence Questions topic."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addTopicWatch"

@dataclass
class AddTopicWatchGivenId(ConfluenceCommand):
    """Set to watch this topic for the current user. Not available for Cloud."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addTopicWatch"

# End Variants for addTopicWatch

# Variants for addUser
@dataclass
class AddUserOptions:
    """Optional parameters for action addUser"""
    user_email: str|None = None
    """User email for user management actions."""
    user_full_name: str|None = None
    """User name for user management actions. Atlassian sometimes refers to this as display name."""
    user_password: str|None = None
    """User password for user management actions."""
    group: str|None = None
    """Group name. In the case of addUser, a comma separated list of group names."""
    auto_group: bool|None = None
    """Groups are automatically added when referenced in add user functions."""
    preserve_case: bool|None = None
    """Some actions like addUser and addGroup may automatically lowercase names usually because the construct is case insensitive on some hosting platforms. Use this switch to override the default behavior and preserve the case."""
    notify: bool|None = None
    """Notify user on addUser with a welcome message."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class AddUser(ConfluenceCommand):
    """Add a new user. Optionally add user to one or more groups as a comma separated list for the group parameter. Not available for Cloud."""
    user_id: str
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    options: AddUserOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addUser"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addUser

# Variants for addUserPicture
@dataclass
class AddUserPictureOptions:
    """Optional parameters for action addUserPicture"""
    mime: str|None = None
    """Attachment mime type if you want to override determination by file extension."""

@dataclass
class AddUserPicture(ConfluenceCommand):
    """Add a picture to the user's profile. Must be an image mime type. Not available for Cloud."""
    user_id: str
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddUserPictureOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addUserPicture"

# End Variants for addUserPicture

# Variants for addUserToGroup
@dataclass
class AddUserToGroupOptions:
    """Optional parameters for action addUserToGroup"""
    auto_group: bool|None = None
    """Groups are automatically added when referenced in add user functions."""
    preserve_case: bool|None = None
    """Some actions like addUser and addGroup may automatically lowercase names usually because the construct is case insensitive on some hosting platforms. Use this switch to override the default behavior and preserve the case."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class AddUserToGroup(ConfluenceCommand):
    """Add user to a group. Use --continue to avoid already is a member checking. This may also improve performance."""
    user_id: str
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    group: str
    """Group name. In the case of addUser, a comma separated list of group names."""
    options: AddUserToGroupOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addUserToGroup"

# End Variants for addUserToGroup

# Variants for addWatch
@dataclass
class AddWatchOptions:
    """Optional parameters for action addWatch"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    user_id: str|None = None
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    children: bool|None = None
    """Immediate children for a page."""
    descendents: bool|None = None
    """All descendents for a page."""

@dataclass
class AddWatchGivenSpace(ConfluenceCommand):
    """Add watch to page or space for a user. If userId is not provided, the current user will be used. On server, only the current user is valid for space watches."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: AddWatchOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addWatch"

@dataclass
class AddWatchGivenId(ConfluenceCommand):
    """Add watch to page or space for a user. If userId is not provided, the current user will be used. On server, only the current user is valid for space watches."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: AddWatchOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addWatch"

# End Variants for addWatch

# Variants for addWebhook
@dataclass
class AddWebhookOptions:
    """Optional parameters for action addWebhook"""
    events: Iterable[str]|str|None = None
    """Comma separated list of webhook events. Valid events may vary by Confluence version, hosting type, or other factors. Consult Atlassian documentation for latest details. Known events are attachment_created, attachment_removed, attachment_restored, attachment_trashed, attachment_updated, blog_created, blog_removed, blog_restored, blog_trashed, blog_updated, blueprint_page_created, comment_created, comment_removed, comment_updated, content_created, content_restored, content_trashed, content_updated, content_permissions_updated, group_created, group_removed, label_added, label_created, label_deleted, label_removed, page_children_reordered, page_created, page_moved, page_removed, page_restored, page_trashed, page_updated, space_created, space_logo_updated, space_permissions_updated, space permissions, space_removed, space_updated, theme_enabled, user_created, user_deactivated, user_followed, user_reactivated, user_removed."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class AddWebhook(ConfluenceCommand):
    """Add a user defined webhook. By default, the webhook will be enabled. Use '--options disable' to disable the webhook. By default, the webhook will send a payload body as part of the post to the URL depending on the type of event."""
    name: str
    """Space name or file name for attachment."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: AddWebhookOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addWebhook"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addWebhook

# Variants for convertToStorageFormat
@dataclass
class ConvertToStorageFormatOptions:
    """Optional parameters for action convertToStorageFormat"""
    content: str|None = None
    """Content for page, attachment, comment, or question."""
    content2: str|None = None
    """Content for page added after content and file content."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    input: Iterable[str]|str|None = None
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    markdown: bool|None = None
    """Attempt to convert rendered Markdown content to storage format. This may not work for all Markdown content. Consider using the markdown macro instead for a more accurate display of Markdown content in Confluence."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class ConvertToStorageFormat(ConfluenceCommand):
    """Convert wiki markup or markdown to Confluence storage format."""
    options: ConvertToStorageFormatOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "convertToStorageFormat"

# End Variants for convertToStorageFormat

# Variants for copyAttachment
@dataclass
class CopyAttachmentOptions:
    """Optional parameters for action copyAttachment"""
    new_space: str|None = None
    """New space key for copied or moved page."""
    new_title: str|None = None
    """New title of copied or renamed page."""
    target_server: str|None = None
    """Target server URL or site configuration reference for copy or publish requests."""
    minor: bool|None = None
    """Indicate minor update (no notifications) for a page update or attachment create."""

@dataclass
class CopyAttachmentGivenSpaceAndTitleAndName(ConfluenceCommand):
    """Copy page attachment to another page or server. Currently, the attachment name cannot be changed. Use minor to avoid notifications."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str
    """Space name or file name for attachment."""
    options: CopyAttachmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyAttachment"

@dataclass
class CopyAttachmentGivenIdAndName(ConfluenceCommand):
    """Copy page attachment to another page or server. Currently, the attachment name cannot be changed. Use minor to avoid notifications."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    name: str
    """Space name or file name for attachment."""
    options: CopyAttachmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyAttachment"

# End Variants for copyAttachment

# Variants for copyAttachments
@dataclass
class CopyAttachmentsOptions:
    """Optional parameters for action copyAttachments"""
    new_space: str|None = None
    """New space key for copied or moved page."""
    new_title: str|None = None
    """New title of copied or renamed page."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    target_server: str|None = None
    """Target server URL or site configuration reference for copy or publish requests."""
    minor: bool|None = None
    """Indicate minor update (no notifications) for a page update or attachment create."""

@dataclass
class CopyAttachmentsGivenSpaceAndTitle(ConfluenceCommand):
    """Copy page attachments to another page or server. All attachments are copied by default or can be filtered by using a regex pattern on the attachment title. Use minor to avoid notifications."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: CopyAttachmentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyAttachments"

@dataclass
class CopyAttachmentsGivenId(ConfluenceCommand):
    """Copy page attachments to another page or server. All attachments are copied by default or can be filtered by using a regex pattern on the attachment title. Use minor to avoid notifications."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: CopyAttachmentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyAttachments"

# End Variants for copyAttachments

# Variants for copyBlog
@dataclass
class CopyBlogOptions:
    """Optional parameters for action copyBlog"""
    new_space: str|None = None
    """New space key for copied or moved page."""
    new_title: str|None = None
    """New title of copied or renamed page."""
    to_day_of_month: str|None = None
    """For copied blog, day of month for blog entry. Defaults to dayOfMonth."""
    to_month: str|None = None
    """For copied blog, month for blog entry. Defaults to month."""
    to_year: str|None = None
    """For copied blog, year for blog entry. Defaults to year."""
    comment_prefix: str|None = None
    """Text added before copied comments or blogs. Replacement variables available are creator, createdTime, space, and title. Example: Originally posted by @creator@ on @createdTime@."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    copy_attachments: bool|None = None
    """Copy attachments when copying a page."""
    copy_comments: bool|None = None
    """Copy comments when copying a page."""
    copy_labels: bool|None = None
    """Copy labels when copying a page or space."""
    target_server: str|None = None
    """Target server URL or site configuration reference for copy or publish requests."""

@dataclass
class CopyBlogGivenSpaceAndTitleAndDayOfMonth(ConfluenceCommand):
    """Copy blog contents to another blog."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    day_of_month: str
    """Day of month for blog entry. Use negative values for going back to previous months."""
    options: CopyBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyBlog"

@dataclass
class CopyBlogGivenSpaceAndTitleAndMonth(ConfluenceCommand):
    """Copy blog contents to another blog."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    month: str
    """Month for blog entry. Defaults to current month."""
    options: CopyBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyBlog"

@dataclass
class CopyBlogGivenSpaceAndTitleAndYear(ConfluenceCommand):
    """Copy blog contents to another blog."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    year: str
    """Year for blog entry. Defaults to current year."""
    options: CopyBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyBlog"

# End Variants for copyBlog

# Variants for copyComments
@dataclass
class CopyCommentsOptions:
    """Optional parameters for action copyComments"""
    comment_prefix: str|None = None
    """Text added before copied comments or blogs. Replacement variables available are creator, createdTime, space, and title. Example: Originally posted by @creator@ on @createdTime@."""

@dataclass
class CopyCommentsGivenSpaceAndTitleAndNewSpace(ConfluenceCommand):
    """Copy all page comments to another page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    new_space: str
    """New space key for copied or moved page."""
    options: CopyCommentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyComments"

@dataclass
class CopyCommentsGivenSpaceAndTitleAndNewTitle(ConfluenceCommand):
    """Copy all page comments to another page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    new_title: str
    """New title of copied or renamed page."""
    options: CopyCommentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyComments"

@dataclass
class CopyCommentsGivenSpaceAndTitleAndTargetServer(ConfluenceCommand):
    """Copy all page comments to another page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    target_server: str
    """Target server URL or site configuration reference for copy or publish requests."""
    options: CopyCommentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyComments"

@dataclass
class CopyCommentsGivenIdAndNewSpace(ConfluenceCommand):
    """Copy all page comments to another page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    new_space: str
    """New space key for copied or moved page."""
    options: CopyCommentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyComments"

@dataclass
class CopyCommentsGivenIdAndNewTitle(ConfluenceCommand):
    """Copy all page comments to another page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    new_title: str
    """New title of copied or renamed page."""
    options: CopyCommentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyComments"

@dataclass
class CopyCommentsGivenIdAndTargetServer(ConfluenceCommand):
    """Copy all page comments to another page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    target_server: str
    """Target server URL or site configuration reference for copy or publish requests."""
    options: CopyCommentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyComments"

# End Variants for copyComments

# Variants for copyLabels
@dataclass
class CopyLabelsOptions:
    """Optional parameters for action copyLabels"""
    new_space: str|None = None
    """New space key for copied or moved page."""
    new_title: str|None = None
    """New title of copied or renamed page."""
    target_server: str|None = None
    """Target server URL or site configuration reference for copy or publish requests."""

@dataclass
class CopyLabels(ConfluenceCommand):
    """Copy all page labels to another page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: CopyLabelsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyLabels"

# End Variants for copyLabels

# Variants for copyPage
@dataclass
class CopyPageOptions:
    """Optional parameters for action copyPage"""
    parent: str|None = None
    """Parent page title or id. @home title references space's home page."""
    children: bool|None = None
    """Immediate children for a page."""
    descendents: bool|None = None
    """All descendents for a page."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    copy_attachments: bool|None = None
    """Copy attachments when copying a page."""
    copy_comments: bool|None = None
    """Copy comments when copying a page."""
    copy_labels: bool|None = None
    """Copy labels when copying a page or space."""
    copy_permissions: bool|None = None
    """Copy permissions when copying a page or space. Source permissions replace existing target permissions. Note Confluence page permissions are really done as restrictions."""
    copy_properties: bool|None = None
    """Copy entity properties when copying pages, pages, and spaces."""
    merge_permissions: bool|None = None
    """Merge permissions when copying a page or space. Source permissions take precedence."""
    comment_prefix: str|None = None
    """Text added before copied comments or blogs. Replacement variables available are creator, createdTime, space, and title. Example: Originally posted by @creator@ on @createdTime@."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    target_server: str|None = None
    """Target server URL or site configuration reference for copy or publish requests."""

@dataclass
class CopyPageGivenSpaceAndTitleAndNewSpaceAndReplaceTitle(ConfluenceCommand):
    """Copy contents to another page. Optionally copy children or all descendents as well. @title@ found in newTitle and parent parameters will be replaced with page title. Use replaceTitle to rename the target page. By default, find replace logic applies only to content. To also apply find replace logic to the title, use --options applyFindReplaceOnTitles. To retain the same parent title when copying to a new space, you can use @source for parent. Use --continue to ignore an already exists error on the target page for single page copies. When using --children or --descendents, --continue means to continue copying descendent pages even after errors copying one or more descendents and end with a summary error message."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    new_space: str
    """New space key for copied or moved page."""
    replace_title: str
    """Name of page to be replaced when copying a page with a different name."""
    options: CopyPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyPage"

@dataclass
class CopyPageGivenSpaceAndTitleAndNewTitleAndReplaceTitle(ConfluenceCommand):
    """Copy contents to another page. Optionally copy children or all descendents as well. @title@ found in newTitle and parent parameters will be replaced with page title. Use replaceTitle to rename the target page. By default, find replace logic applies only to content. To also apply find replace logic to the title, use --options applyFindReplaceOnTitles. To retain the same parent title when copying to a new space, you can use @source for parent. Use --continue to ignore an already exists error on the target page for single page copies. When using --children or --descendents, --continue means to continue copying descendent pages even after errors copying one or more descendents and end with a summary error message."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    new_title: str
    """New title of copied or renamed page."""
    replace_title: str
    """Name of page to be replaced when copying a page with a different name."""
    options: CopyPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyPage"

# End Variants for copyPage

# Variants for copyPageChildren
@dataclass
class CopyPageChildrenOptions:
    """Optional parameters for action copyPageChildren"""
    descendents: bool|None = None
    """All descendents for a page."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    copy_attachments: bool|None = None
    """Copy attachments when copying a page."""
    copy_comments: bool|None = None
    """Copy comments when copying a page."""
    copy_labels: bool|None = None
    """Copy labels when copying a page or space."""
    copy_permissions: bool|None = None
    """Copy permissions when copying a page or space. Source permissions replace existing target permissions. Note Confluence page permissions are really done as restrictions."""
    copy_properties: bool|None = None
    """Copy entity properties when copying pages, pages, and spaces."""
    merge_permissions: bool|None = None
    """Merge permissions when copying a page or space. Source permissions take precedence."""
    comment_prefix: str|None = None
    """Text added before copied comments or blogs. Replacement variables available are creator, createdTime, space, and title. Example: Originally posted by @creator@ on @createdTime@."""
    target_server: str|None = None
    """Target server URL or site configuration reference for copy or publish requests."""

@dataclass
class CopyPageChildren(ConfluenceCommand):
    """Copy children or all descendents of a page as descendents of another page. @title@ found in parent parameters will be replaced with page title. Does not copy main page, use copyPage for that."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    new_space: str
    """New space key for copied or moved page."""
    parent: str
    """Parent page title or id. @home title references space's home page."""
    options: CopyPageChildrenOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyPageChildren"

# End Variants for copyPageChildren

# Variants for copyPageHierarchy
@dataclass
class CopyPageHierarchyOptions:
    """Optional parameters for action copyPageHierarchy"""
    new_space: str|None = None
    """New space key for copied or moved page."""
    copy_attachments: bool|None = None
    """Copy attachments when copying a page."""
    copy_labels: bool|None = None
    """Copy labels when copying a page or space."""
    copy_permissions: bool|None = None
    """Copy permissions when copying a page or space. Source permissions replace existing target permissions. Note Confluence page permissions are really done as restrictions."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class CopyPageHierarchy(ConfluenceCommand):
    """Mimics the improved UI support for copy page with the include child pages option to copy an entire hierarchy of pages with the ability to modify the titles and other options. The options are different than similar support provided by copyPage and copyPageChildren - review the various options to select the right copy action for your needs. This is a single server based copy operation, so should be considerably faster for copying hierarchies with a large number of pages. Copying is asynchronous unless '--options wait' is specified. The hierarchy is copied as sub pages under the parent provided. Title manipulation options can be provided with the options parameter using one or more of titlePrefix, titleFind, and titleReplace. When copying to the same space, you must modify the titles to avoid title conflicts."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    parent: str
    """Parent page title or id. @home title references space's home page."""
    options: CopyPageHierarchyOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyPageHierarchy"

# End Variants for copyPageHierarchy

# Variants for copyPermissions
@dataclass
class CopyPermissionsOptions:
    """Optional parameters for action copyPermissions"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    new_space: str|None = None
    """New space key for copied or moved page."""
    new_title: str|None = None
    """New title of copied or renamed page."""
    merge_permissions: bool|None = None
    """Merge permissions when copying a page or space. Source permissions take precedence."""
    target_server: str|None = None
    """Target server URL or site configuration reference for copy or publish requests."""

@dataclass
class CopyPermissionsGivenSpace(ConfluenceCommand):
    """Copy page or space permissions from a page or space to another page or space. The permissions are replaced by default. Use mergePermissions to merge permissions."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: CopyPermissionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyPermissions"

@dataclass
class CopyPermissionsGivenId(ConfluenceCommand):
    """Copy page or space permissions from a page or space to another page or space. The permissions are replaced by default. Use mergePermissions to merge permissions."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: CopyPermissionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copyPermissions"

# End Variants for copyPermissions

# Variants for copySpace
@dataclass
class CopySpaceOptions:
    """Optional parameters for action copySpace"""
    name: str|None = None
    """Space name or file name for attachment."""
    description: str|None = None
    """Descriptive text."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""
    copy_blogs: bool|None = None
    """Copy blogs when copying a space."""
    copy_attachments: bool|None = None
    """Copy attachments when copying a page."""
    copy_labels: bool|None = None
    """Copy labels when copying a page or space."""
    copy_categories: bool|None = None
    """Copy space categories."""
    copy_comments: bool|None = None
    """Copy comments when copying a page."""
    copy_permissions: bool|None = None
    """Copy permissions when copying a page or space. Source permissions replace existing target permissions. Note Confluence page permissions are really done as restrictions."""
    copy_properties: bool|None = None
    """Copy entity properties when copying pages, pages, and spaces."""
    merge_permissions: bool|None = None
    """Merge permissions when copying a page or space. Source permissions take precedence."""
    comment_prefix: str|None = None
    """Text added before copied comments or blogs. Replacement variables available are creator, createdTime, space, and title. Example: Originally posted by @creator@ on @createdTime@."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class CopySpaceGivenSpaceAndNewSpace(ConfluenceCommand):
    """Creates a new space and copies pages to the new space. Other information can be copied as well based on other parameters. By default, find replace logic applies only to content. To also apply find replace logic to the title, use --options applyFindReplaceOnTitles."""
    space: str
    """Space key. For some actions, a space name may also work."""
    new_space: str
    """New space key for copied or moved page."""
    options: CopySpaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copySpace"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class CopySpaceGivenSpaceAndTargetServer(ConfluenceCommand):
    """Creates a new space and copies pages to the new space. Other information can be copied as well based on other parameters. By default, find replace logic applies only to content. To also apply find replace logic to the title, use --options applyFindReplaceOnTitles."""
    space: str
    """Space key. For some actions, a space name may also work."""
    target_server: str
    """Target server URL or site configuration reference for copy or publish requests."""
    options: CopySpaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "copySpace"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for copySpace

# Variants for disableApp

@dataclass
class DisableApp(ConfluenceCommand):
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
class EnableApp(ConfluenceCommand):
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

# Variants for exportData
@dataclass
class ExportDataOptions:
    """Optional parameters for action exportData"""
    space: str|None = None
    """Space key. For some actions, a space name may also work."""
    export_type: str|None = None
    """Export type (XML, HTML, PDF, CSV) for space export - default is XML if not specified. CSV export is only supported for Cloud version of Confluence. SPACE, PARTICIPANTS, GROUP, or USERS for export data - default is SPACE if not specified."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    group: str|None = None
    """Group name. In the case of addUser, a comma separated list of group names."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class ExportData(ConfluenceCommand):
    """Export data in a ACLI compatible script suitable for use with the run action normally on a different instance. Supported export types are SPACE, PARTICIPANTS, USERS, and GROUPS. SPACE is the default and provides space create actions including permissions. PARTICIPANTS means the set of users that participated in the creating or modifying content in a space. Use '--options includeContinue' to have generated actions include the --continue parameter where appropriate to ignore already exists errors. For exportType USERS, use '--options includeGroups' to have the addUser action include the group parameter. Also, exportType USERS supports the same filtering parameters as getUserList."""
    options: ExportDataOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "exportData"

# End Variants for exportData

# Variants for exportPage
@dataclass
class ExportPageOptions:
    """Optional parameters for action exportPage"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    descendents: bool|None = None
    """All descendents for a page."""
    children: bool|None = None
    """Immediate children for a page."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    new_space: str|None = None
    """New space key for copied or moved page."""
    new_title: str|None = None
    """New title of copied or renamed page."""
    labels: str|None = None
    """Comma separated list of labels."""
    target_server: str|None = None
    """Target server URL or site configuration reference for copy or publish requests."""
    comment: str|None = None
    """Comment text."""
    minor: bool|None = None
    """Indicate minor update (no notifications) for a page update or attachment create."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class ExportPageGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Export a single page or blog to a PDF. A page hierarchy can be exported, one page at a time, provided the file specified is a directory. Use @default or . for the file name portion of the file parameter to have it replaced with the page title and pdf extension. Use '--options addAttachment' to add the export as an attachment to the same page by default or to a page identified by newSpace and newTitle parameters. If @default is specified for file with the attachment option, no local file will be written. The attachment name is either given by the file parameter if provided or the title of the page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: ExportPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "exportPage"

@dataclass
class ExportPageGivenIdAndFile(ConfluenceCommand):
    """Export a single page or blog to a PDF. A page hierarchy can be exported, one page at a time, provided the file specified is a directory. Use @default or . for the file name portion of the file parameter to have it replaced with the page title and pdf extension. Use '--options addAttachment' to add the export as an attachment to the same page by default or to a page identified by newSpace and newTitle parameters. If @default is specified for file with the attachment option, no local file will be written. The attachment name is either given by the file parameter if provided or the title of the page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: ExportPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "exportPage"

# End Variants for exportPage

# Variants for exportSite
@dataclass
class ExportSiteOptions:
    """Optional parameters for action exportSite"""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    export_attachments: bool|None = None
    """Export attachments for site export. Automatically done for space exports."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class ExportSite(ConfluenceCommand):
    """Create a site export. For server, data is put into a file in the Confluence home/backups directory. For Cloud, data is available from backup manager screen or the file can optionally be copied to a local file if the file parameter is specified and permissions allow. Also for Cloud only, use the exportAttachments parameter to request the export contain attachments and similar data. Also for Cloud only, use --options backupForServer to create a backup suitable for import to a Server instance."""
    options: ExportSiteOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "exportSite"

# End Variants for exportSite

# Variants for exportSpace
@dataclass
class ExportSpaceOptions:
    """Optional parameters for action exportSpace"""
    export_type: str|None = None
    """Export type (XML, HTML, PDF, CSV) for space export - default is XML if not specified. CSV export is only supported for Cloud version of Confluence. SPACE, PARTICIPANTS, GROUP, or USERS for export data - default is SPACE if not specified."""

@dataclass
class ExportSpace(ConfluenceCommand):
    """Export a space to a file. Use an administrator level user as non-administrators may not have access to all pages."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: ExportSpaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "exportSpace"

# End Variants for exportSpace

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
class GetApp(ConfluenceCommand):
    """Get app information if installed. Use '--app @default' for the ACLI app."""
    app: str
    """App key."""
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
class GetAppList(ConfluenceCommand):
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

# Variants for getApplicationLink

@dataclass
class GetApplicationLinkGivenName(ConfluenceCommand):
    """Get information for an application link identified by name or url."""
    name: str
    """Space name or file name for attachment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getApplicationLink"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class GetApplicationLinkGivenUrl(ConfluenceCommand):
    """Get information for an application link identified by name or url."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getApplicationLink"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for getApplicationLink

# Variants for getApplicationLinkList
@dataclass
class GetApplicationLinkListOptions:
    """Optional parameters for action getApplicationLinkList"""
    type: str|None = None
    """Application type, shortcut type, or similar depending on context."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
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
class GetApplicationLinkList(ConfluenceCommand):
    """Get list of a application links with optional filtering on application type and regex filtering on the name or url. Use '--options excludeSystemLinks' to exclude system defined links. Example types: jira, confluence."""
    options: GetApplicationLinkListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getApplicationLinkList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getApplicationLinkList

# Variants for getAttachment
@dataclass
class GetAttachmentOptions:
    """Optional parameters for action getAttachment"""
    name: str|None = None
    """Space name or file name for attachment."""
    version: str|None = None
    """Item version."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetAttachmentGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Get a attachment data and put to a file. The page the attachment is on must be provided by space and title or page id. If the attachment name is not provided, it is derived from the file. A numeric attachment id can substitute for the attachment name."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: GetAttachmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAttachment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class GetAttachmentGivenIdAndFile(ConfluenceCommand):
    """Get a attachment data and put to a file. The page the attachment is on must be provided by space and title or page id. If the attachment name is not provided, it is derived from the file. A numeric attachment id can substitute for the attachment name."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: GetAttachmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAttachment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for getAttachment

# Variants for getAttachmentList
@dataclass
class GetAttachmentListOptions:
    """Optional parameters for action getAttachmentList"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetAttachmentListGivenCql(ConfluenceCommand):
    """Get list of all attachments (or those matching regex) for pages based on content search (like getContentList), space, or specific page id. @all can be used as a special value for the space parameter."""
    cql: str
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    options: GetAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAttachmentList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetAttachmentListGivenSpace(ConfluenceCommand):
    """Get list of all attachments (or those matching regex) for pages based on content search (like getContentList), space, or specific page id. @all can be used as a special value for the space parameter."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: GetAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAttachmentList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetAttachmentListGivenId(ConfluenceCommand):
    """Get list of all attachments (or those matching regex) for pages based on content search (like getContentList), space, or specific page id. @all can be used as a special value for the space parameter."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAttachmentList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAttachmentList

# Variants for getAttachmentVersionList
@dataclass
class GetAttachmentVersionListOptions:
    """Optional parameters for action getAttachmentVersionList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetAttachmentVersionListGivenIdAndName(ConfluenceCommand):
    """Get list of versions for an attachment identified by name. Identify the content containing the attachment by content id or space and title. The name parameter also accepts an attachment id. Optionally, filter by regex pattern on the version comment."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    name: str
    """Space name or file name for attachment."""
    options: GetAttachmentVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAttachmentVersionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetAttachmentVersionListGivenSpaceAndTitleAndName(ConfluenceCommand):
    """Get list of versions for an attachment identified by name. Identify the content containing the attachment by content id or space and title. The name parameter also accepts an attachment id. Optionally, filter by regex pattern on the version comment."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str
    """Space name or file name for attachment."""
    options: GetAttachmentVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAttachmentVersionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAttachmentVersionList

# Variants for getAuditLogList
@dataclass
class GetAuditLogListOptions:
    """Optional parameters for action getAuditLogList"""
    start_date: str|None = None
    """Earliest date for date filtering. Default is to get the most recent entries."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetAuditLogList(ConfluenceCommand):
    """Get a list of audit logs with optional regex filtering on log summary. Use startDate and endDate parameters for additional filtering based on log date range. Use '--options search=...' to filter by a simple text search on fields containing the given value. By default, at most 1000 entries are returned unless the limit parameter is explicitly set to something higher."""
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
    def supports_output_type() -> bool:
        return True

# End Variants for getAuditLogList

# Variants for getBlogList
@dataclass
class GetBlogListOptions:
    """Optional parameters for action getBlogList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    regex2: str|None = None
    """Regular expression for secondary content matching. In some cases, filtering on a secondary field may be needed."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
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
class GetBlogListGivenSpace(ConfluenceCommand):
    """Get list of blogs items with regex filtering on blog title. Use regex2 to additionally filter by matching on the content."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: GetBlogListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBlogList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetBlogListGivenLabels(ConfluenceCommand):
    """Get list of blogs items with regex filtering on blog title. Use regex2 to additionally filter by matching on the content."""
    labels: str
    """Comma separated list of labels."""
    options: GetBlogListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBlogList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBlogList

# Variants for getBlogSource
@dataclass
class GetBlogSourceOptions:
    """Optional parameters for action getBlogSource"""
    type: str|None = None
    """Application type, shortcut type, or similar depending on context."""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    after_sql: str|None = None
    """SQL to run after a successful action. Limited to specific actions at this time."""

@dataclass
class GetBlogSourceGivenSpaceAndTitle(ConfluenceCommand):
    """Get source for a blog entry. Same as getSource - see that action for more details."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetBlogSourceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBlogSource"

@dataclass
class GetBlogSourceGivenId(ConfluenceCommand):
    """Get source for a blog entry. Same as getSource - see that action for more details."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetBlogSourceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBlogSource"

# End Variants for getBlogSource

# Variants for getCommentList
@dataclass
class GetCommentListOptions:
    """Optional parameters for action getCommentList"""
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
class GetCommentListGivenSpaceAndTitle(ConfluenceCommand):
    """List of comment information for a page with regex filtering by content of the comment."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetCommentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getCommentList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetCommentListGivenId(ConfluenceCommand):
    """List of comment information for a page with regex filtering by content of the comment."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetCommentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getCommentList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getCommentList

# Variants for getCommentSource
@dataclass
class GetCommentSourceOptions:
    """Optional parameters for action getCommentSource"""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetCommentSource(ConfluenceCommand):
    """Get comment source."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetCommentSourceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getCommentSource"

# End Variants for getCommentSource

# Variants for getComments
@dataclass
class GetCommentsOptions:
    """Optional parameters for action getComments"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetCommentsGivenSpaceAndTitle(ConfluenceCommand):
    """Get a formatted string of comment text for a page or blog. By default all comments will be included or filter comments by regex on comment content."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetCommentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getComments"

@dataclass
class GetCommentsGivenId(ConfluenceCommand):
    """Get a formatted string of comment text for a page or blog. By default all comments will be included or filter comments by regex on comment content."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetCommentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getComments"

# End Variants for getComments

# Variants for getContent
@dataclass
class GetContentOptions:
    """Optional parameters for action getContent"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetContentGivenSpaceAndTitle(ConfluenceCommand):
    """Get information about a content object."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetContentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getContent"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetContentGivenId(ConfluenceCommand):
    """Get information about a content object."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetContentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getContent"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getContent

# Variants for getContentHistoryList
@dataclass
class GetContentHistoryListOptions:
    """Optional parameters for action getContentHistoryList"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    regex2: str|None = None
    """Regular expression for secondary content matching. In some cases, filtering on a secondary field may be needed."""
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
class GetContentHistoryListGivenSpaceAndTitle(ConfluenceCommand):
    """Get list of content versions with optional regex filtering on the modifier's user information (name, key, and display name). Additional filtering on content source (storage format) is possible by specifying the regex2 parameter. Normally used for pages and blogs but other content identified by id like an attachment may also work, however, for attachments, getAttachmentVersionList may be more appropriate."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetContentHistoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getContentHistoryList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetContentHistoryListGivenId(ConfluenceCommand):
    """Get list of content versions with optional regex filtering on the modifier's user information (name, key, and display name). Additional filtering on content source (storage format) is possible by specifying the regex2 parameter. Normally used for pages and blogs but other content identified by id like an attachment may also work, however, for attachments, getAttachmentVersionList may be more appropriate."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetContentHistoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getContentHistoryList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getContentHistoryList

# Variants for getContentList
@dataclass
class GetContentListOptions:
    """Optional parameters for action getContentList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    user_id: str|None = None
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    group: str|None = None
    """Group name. In the case of addUser, a comma separated list of group names."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
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
class GetContentList(ConfluenceCommand):
    """Get list of content based on CQL with regex filtering on content title. For Cloud, outputFormat 10 has been added to report on user or group permissions for accessing content. Specify with user or group parameters with user taking precedence and defaulting to @self. Warning, gathering access permissions takes significant time for larger content lists, use with caution."""
    cql: str
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    options: GetContentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getContentList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getContentList

# Variants for getEntityProperty
@dataclass
class GetEntityPropertyOptions:
    """Optional parameters for action getEntityProperty"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetEntityPropertyGivenSpaceAndTitleAndName(ConfluenceCommand):
    """Get entity property by name."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str
    """Space name or file name for attachment."""
    options: GetEntityPropertyOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getEntityProperty"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetEntityPropertyGivenIdAndName(ConfluenceCommand):
    """Get entity property by name."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    name: str
    """Space name or file name for attachment."""
    options: GetEntityPropertyOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getEntityProperty"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getEntityProperty

# Variants for getEntityPropertyList
@dataclass
class GetEntityPropertyListOptions:
    """Optional parameters for action getEntityPropertyList"""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetEntityPropertyListGivenSpaceAndTitle(ConfluenceCommand):
    """List issue properties for an issue with optional regex filtering by name."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetEntityPropertyListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getEntityPropertyList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetEntityPropertyListGivenId(ConfluenceCommand):
    """List issue properties for an issue with optional regex filtering by name."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetEntityPropertyListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getEntityPropertyList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getEntityPropertyList

# Variants for getGroupList
@dataclass
class GetGroupListOptions:
    """Optional parameters for action getGroupList"""
    user_id: str|None = None
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
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
class GetGroupList(ConfluenceCommand):
    """Get list of groups with optional filtering by group name. If a user id is provided, only list groups the user is a member of."""
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
    def supports_output_type() -> bool:
        return True

# End Variants for getGroupList

# Variants for getLabelList
@dataclass
class GetLabelListOptions:
    """Optional parameters for action getLabelList"""
    cql: str|None = None
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    id: str|None = None
    """Numeric id of an item like a page, blog, or comment."""
    space: str|None = None
    """Space key. For some actions, a space name may also work."""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    most_popular: bool|None = None
    """Request most popular labels."""
    recently_used: bool|None = None
    """Request recently used labels."""
    labels: str|None = None
    """Comma separated list of labels."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class GetLabelList(ConfluenceCommand):
    """Get list of labels globally or specific to content. Default is mostPopular with an option for recently used or related to a label. If parameters for a page or other content is provided, then all labels for that content will be listed. If cql is provided, it takes precedence over the other parameters and list labels for each piece of content satisfying the CQL query."""
    options: GetLabelListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getLabelList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getLabelList

# Variants for getPage
@dataclass
class GetPageOptions:
    """Optional parameters for action getPage"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class GetPageGivenSpaceAndTitle(ConfluenceCommand):
    """Get information about a page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetPageGivenId(ConfluenceCommand):
    """Get information about a page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPage

# Variants for getPageHistoryList
@dataclass
class GetPageHistoryListOptions:
    """Optional parameters for action getPageHistoryList"""
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
class GetPageHistoryListGivenSpaceAndTitle(ConfluenceCommand):
    """Deprecated. Use getContentHistoryList instead. Get list of revisions for a page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetPageHistoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPageHistoryList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetPageHistoryListGivenId(ConfluenceCommand):
    """Deprecated. Use getContentHistoryList instead. Get list of revisions for a page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetPageHistoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPageHistoryList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPageHistoryList

# Variants for getPageList
@dataclass
class GetPageListOptions:
    """Optional parameters for action getPageList"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    parent: str|None = None
    """Parent page title or id. @home title references space's home page."""
    ancestors: bool|None = None
    """Ancestors for a page."""
    descendents: bool|None = None
    """All descendents for a page."""
    children: bool|None = None
    """Immediate children for a page."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    regex2: str|None = None
    """Regular expression for secondary content matching. In some cases, filtering on a secondary field may be needed."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
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
class GetPageListGivenCql(ConfluenceCommand):
    """Get list of pages with regex filtering on page title. Either use cql directly to define the page list or the various other parameters that combine to define the page list including labels, space, id, or title. When the cql parameter is specified, the labels, space, id, and parent parameters are ignored. Options for including ancestors, children, or descendents are available when a specific page is specified. For example, when space and labels are both used, pages are selected from the space that have at last one of the labels. Use regex2 to additionally filter by matching on the content. Content filtering takes significant resources and time. @all can be used as a special value for the space parameter."""
    cql: str
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    options: GetPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPageList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetPageListGivenLabels(ConfluenceCommand):
    """Get list of pages with regex filtering on page title. Either use cql directly to define the page list or the various other parameters that combine to define the page list including labels, space, id, or title. When the cql parameter is specified, the labels, space, id, and parent parameters are ignored. Options for including ancestors, children, or descendents are available when a specific page is specified. For example, when space and labels are both used, pages are selected from the space that have at last one of the labels. Use regex2 to additionally filter by matching on the content. Content filtering takes significant resources and time. @all can be used as a special value for the space parameter."""
    labels: str
    """Comma separated list of labels."""
    options: GetPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPageList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetPageListGivenSpace(ConfluenceCommand):
    """Get list of pages with regex filtering on page title. Either use cql directly to define the page list or the various other parameters that combine to define the page list including labels, space, id, or title. When the cql parameter is specified, the labels, space, id, and parent parameters are ignored. Options for including ancestors, children, or descendents are available when a specific page is specified. For example, when space and labels are both used, pages are selected from the space that have at last one of the labels. Use regex2 to additionally filter by matching on the content. Content filtering takes significant resources and time. @all can be used as a special value for the space parameter."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: GetPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPageList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetPageListGivenId(ConfluenceCommand):
    """Get list of pages with regex filtering on page title. Either use cql directly to define the page list or the various other parameters that combine to define the page list including labels, space, id, or title. When the cql parameter is specified, the labels, space, id, and parent parameters are ignored. Options for including ancestors, children, or descendents are available when a specific page is specified. For example, when space and labels are both used, pages are selected from the space that have at last one of the labels. Use regex2 to additionally filter by matching on the content. Content filtering takes significant resources and time. @all can be used as a special value for the space parameter."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPageList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPageList

# Variants for getPageSource
@dataclass
class GetPageSourceOptions:
    """Optional parameters for action getPageSource"""
    type: str|None = None
    """Application type, shortcut type, or similar depending on context."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    after_sql: str|None = None
    """SQL to run after a successful action. Limited to specific actions at this time."""

@dataclass
class GetPageSourceGivenSpaceAndTitle(ConfluenceCommand):
    """Get page or blog source. Same as getSource - see that action for more details."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetPageSourceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPageSource"

@dataclass
class GetPageSourceGivenId(ConfluenceCommand):
    """Get page or blog source. Same as getSource - see that action for more details."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetPageSourceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPageSource"

# End Variants for getPageSource

# Variants for getPermissionList
@dataclass
class GetPermissionListOptions:
    """Optional parameters for action getPermissionList"""
    space: str|None = None
    """Space key. For some actions, a space name may also work."""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    user_id: str|None = None
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
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
class GetPermissionList(ConfluenceCommand):
    """Get list of all available, space, or page permissions. See getSpacePermissionList for more detailed space permissions. Use the userId parameter to restrict the list to permissions for a specific user."""
    options: GetPermissionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPermissionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPermissionList

# Variants for getQuestion
@dataclass
class GetQuestionOptions:
    """Optional parameters for action getQuestion"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetQuestionGivenId(ConfluenceCommand):
    """Get a question. Not available for Cloud."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetQuestionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getQuestion"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetQuestionGivenTitle(ConfluenceCommand):
    """Get a question. Not available for Cloud."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetQuestionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getQuestion"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getQuestion

# Variants for getQuestionList
@dataclass
class GetQuestionListOptions:
    """Optional parameters for action getQuestionList"""
    filter: str|None = None
    """Question search filter. Valid values are: POPULAR, RECENT, UNANSWERED."""
    topic: str|None = None
    """Confluence Questions topic."""
    user_id: str|None = None
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is to get the most recent entries."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
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
class GetQuestionList(ConfluenceCommand):
    """Get list of questions with regex selection on the question title. Filter by date using the startDate and endDate parameters with absolute dates or durations specified by a negative integer value with s (secs), m (mins), h (hours), or d (days). Examples are '--endDate -30d', '--endDate -7days', or '--endDate -1h'."""
    options: GetQuestionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getQuestionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getQuestionList

# Variants for getServerInfo
@dataclass
class GetServerInfoOptions:
    """Optional parameters for action getServerInfo"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetServerInfo(ConfluenceCommand):
    """Get information about the Confluence server."""
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

# Variants for getShortcutList
@dataclass
class GetShortcutListOptions:
    """Optional parameters for action getShortcutList"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class GetShortcutList(ConfluenceCommand):
    """Get list of shortcuts with regex filtering on name and url. Use --options parameter to filter by quick or main category of shortcuts."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: GetShortcutListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getShortcutList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getShortcutList

# Variants for getSource
@dataclass
class GetSourceOptions:
    """Optional parameters for action getSource"""
    type: str|None = None
    """Application type, shortcut type, or similar depending on context."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetSourceGivenSpaceAndTitle(ConfluenceCommand):
    """Get page or blog source. Storage is the default source type. Other types can be requested by using the type parameter and depends on your hosting platform. Examples are view, styled_view, export_view, anonymous_export_view, editor. On Cloud, the new atlas_doc_format type with ACLI alias of 'adf' is also available."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: GetSourceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSource"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class GetSourceGivenId(ConfluenceCommand):
    """Get page or blog source. Storage is the default source type. Other types can be requested by using the type parameter and depends on your hosting platform. Examples are view, styled_view, export_view, anonymous_export_view, editor. On Cloud, the new atlas_doc_format type with ACLI alias of 'adf' is also available."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetSourceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSource"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for getSource

# Variants for getSpace
@dataclass
class GetSpaceOptions:
    """Optional parameters for action getSpace"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetSpace(ConfluenceCommand):
    """Get space information."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: GetSpaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSpace"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getSpace

# Variants for getSpaceList
@dataclass
class GetSpaceListOptions:
    """Optional parameters for action getSpaceList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    regex2: str|None = None
    """Regular expression for secondary content matching. In some cases, filtering on a secondary field may be needed."""
    personal: bool|None = None
    """Include personal spaces."""
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
class GetSpaceList(ConfluenceCommand):
    """Get list of spaces with regex filtering on space key or name. Also, use regex2 for filtering on space categories. Use personal to extend to personal spaces."""
    options: GetSpaceListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSpaceList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getSpaceList

# Variants for getSpacePermissionList
@dataclass
class GetSpacePermissionListOptions:
    """Optional parameters for action getSpacePermissionList"""
    space: str|None = None
    """Space key. For some actions, a space name may also work."""
    personal: bool|None = None
    """Include personal spaces."""
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
class GetSpacePermissionList(ConfluenceCommand):
    """Get CSV list of user, group, and anonymous space permissions. The space parameter defaults to @all in which case the limit and regex parameters can be used to filter the spaces included in the list."""
    options: GetSpacePermissionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSpacePermissionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getSpacePermissionList

# Variants for getTopic
@dataclass
class GetTopicOptions:
    """Optional parameters for action getTopic"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetTopicGivenTopic(ConfluenceCommand):
    """Get information on a Confluence Questions topic. Not available for Cloud."""
    topic: str
    """Confluence Questions topic."""
    options: GetTopicOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getTopic"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetTopicGivenId(ConfluenceCommand):
    """Get information on a Confluence Questions topic. Not available for Cloud."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetTopicOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getTopic"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getTopic

# Variants for getTopicList
@dataclass
class GetTopicListOptions:
    """Optional parameters for action getTopicList"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class GetTopicList(ConfluenceCommand):
    """Get list of Confluence Questions topics with regex filtering on topic name and description."""
    options: GetTopicListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getTopicList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getTopicList

# Variants for getTrashList
@dataclass
class GetTrashListOptions:
    """Optional parameters for action getTrashList"""
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
class GetTrashList(ConfluenceCommand):
    """Get a list of trash contents for a space."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: GetTrashListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getTrashList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getTrashList

# Variants for getUser
@dataclass
class GetUserOptions:
    """Optional parameters for action getUser"""
    user_id: str|None = None
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    name: str|None = None
    """Space name or file name for attachment."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    reference: str|None = None
    """Reference to a replacement key value used to remember an action specific value like issue key, entity id, or similar so it can be referenced later. Each action that allows this parameter will specify that the reference parameter is valid for the action and the first entry listed for available replacement variables help text will be the value set. If you need access to a different replacement variable in your script, you will need to use the setReplacementVariables action after the action to set a new replacement variable of your choosing to one of the other available replacement variables."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetUser(ConfluenceCommand):
    """Get user information for the current user or the specific user requested."""
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
    group: str|None = None
    """Group name. In the case of addUser, a comma separated list of group names."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
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
class GetUserList(ConfluenceCommand):
    """Get list of users with optional regex filtering by user id. If a group is provided, only members of the group will be included. For Cloud, group defaults to confluence-users."""
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
    def supports_output_type() -> bool:
        return True

# End Variants for getUserList

# Variants for getWatchList
@dataclass
class GetWatchListOptions:
    """Optional parameters for action getWatchList"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class GetWatchListGivenSpace(ConfluenceCommand):
    """Get list of watchers on a page or space with regex filtering on user name."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: GetWatchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getWatchList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetWatchListGivenId(ConfluenceCommand):
    """Get list of watchers on a page or space with regex filtering on user name."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: GetWatchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getWatchList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getWatchList

# Variants for getWebhookList
@dataclass
class GetWebhookListOptions:
    """Optional parameters for action getWebhookList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetWebhookList(ConfluenceCommand):
    """List user defined webhooks with regex filtering on webhook name."""
    options: GetWebhookListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getWebhookList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getWebhookList

# Variants for hideShortcut
@dataclass
class HideShortcutOptions:
    """Optional parameters for action hideShortcut"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class HideShortcutGivenSpaceAndName(ConfluenceCommand):
    """Hide a shortcut by name or id. Only shortcuts in category main can be shown or hidden. Use --name @all to remove all space shortcuts. Shortcuts show up on the UI. Use continue to ignore not found errors."""
    space: str
    """Space key. For some actions, a space name may also work."""
    name: str
    """Space name or file name for attachment."""
    options: HideShortcutOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "hideShortcut"

@dataclass
class HideShortcutGivenSpaceAndId(ConfluenceCommand):
    """Hide a shortcut by name or id. Only shortcuts in category main can be shown or hidden. Use --name @all to remove all space shortcuts. Shortcuts show up on the UI. Use continue to ignore not found errors."""
    space: str
    """Space key. For some actions, a space name may also work."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: HideShortcutOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "hideShortcut"

# End Variants for hideShortcut

# Variants for installApp
@dataclass
class InstallAppOptions:
    """Optional parameters for action installApp"""
    version: str|None = None
    """Item version."""

@dataclass
class InstallAppGivenApp(ConfluenceCommand):
    """Install app via UPM. Use '--app @default' for the ACLI app. See UPM CLI documentation for installApp for more details."""
    app: str
    """App key."""
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
class InstallAppGivenUrl(ConfluenceCommand):
    """Install app via UPM. Use '--app @default' for the ACLI app. See UPM CLI documentation for installApp for more details."""
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
class InstallAppGivenFile(ConfluenceCommand):
    """Install app via UPM. Use '--app @default' for the ACLI app. See UPM CLI documentation for installApp for more details."""
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

# Variants for loadFiles
@dataclass
class LoadFilesOptions:
    """Optional parameters for action loadFiles"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    content: str|None = None
    """Content for page, attachment, comment, or question."""
    parent: str|None = None
    """Parent page title or id. @home title references space's home page."""
    user_id: str|None = None
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    group: str|None = None
    """Group name. In the case of addUser, a comma separated list of group names."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    no_convert: bool|None = None
    """Do not convert content from wiki to storage format. Unless otherwise known, content is considered as wiki markup and converted."""
    markdown: bool|None = None
    """Attempt to convert rendered Markdown content to storage format. This may not work for all Markdown content. Consider using the markdown macro instead for a more accurate display of Markdown content in Confluence."""

@dataclass
class LoadFiles(ConfluenceCommand):
    """Load directory and files into a page hierarchy. By default, files with mime types text/html, text/text, and text/markdown are converted to pages. All other files added as attachments. Text files are treated as wiki markup unless noConvert is specified. Markdown files are converted to html. HTML files are wrapped with a wiki style html macro. Use continue to skip over problematic files. The automatic page creation for certain mime types can be customized by specifying a comma separated list of zero or more types (text, html, markdown) on the autoPage option. Use '--option autoPage=' to prevent automatic page completely. Another example is to use '--option text,markdown' to have html files just added as attachments - this is important if you do not have the html macro installed on your instance."""
    space: str
    """Space key. For some actions, a space name may also work."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: LoadFilesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "loadFiles"

# End Variants for loadFiles

# Variants for login
@dataclass
class LoginOptions:
    """Optional parameters for action login"""
    user: str|None = None
    """User name for remote access. Cloud users are identified by email address."""

@dataclass
class Login(ConfluenceCommand):
    """Login to remote server. Server only. Blank will be returned for Cloud. Returns session token that can be used on subsequent requests with the login or loginFromStandardInput parameters."""
    password: str
    """User password for remote access. Cloud users need to use an API token for almost all cases and the preference is to provide the token with the token parameter. However, for compatibility reasons, we still allow the token to be provided using the password parameter."""
    options: LoginOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "login"

# End Variants for login

# Variants for logout

@dataclass
class Logout(ConfluenceCommand):
    """Server only. Nothing is done currently as Confluence does not support this. Blank is returned."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "logout"

# End Variants for logout

# Variants for modifyBlog
@dataclass
class ModifyBlogOptions:
    """Optional parameters for action modifyBlog"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    content: str|None = None
    """Content for page, attachment, comment, or question."""
    content2: str|None = None
    """Content for page added after content and file content."""
    input: Iterable[str]|str|None = None
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    labels: str|None = None
    """Comma separated list of labels."""
    comment: str|None = None
    """Comment text."""
    minor: bool|None = None
    """Indicate minor update (no notifications) for a page update or attachment create."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    no_convert: bool|None = None
    """Do not convert content from wiki to storage format. Unless otherwise known, content is considered as wiki markup and converted."""
    markdown: bool|None = None
    """Attempt to convert rendered Markdown content to storage format. This may not work for all Markdown content. Consider using the markdown macro instead for a more accurate display of Markdown content in Confluence."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class ModifyBlogGivenSpaceAndTitle(ConfluenceCommand):
    """Modify current blog content by adding content before (content or file parameters) or after (content2 parameter) current content and applying findReplace logic (based on how content source format)."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: ModifyBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "modifyBlog"

@dataclass
class ModifyBlogGivenId(ConfluenceCommand):
    """Modify current blog content by adding content before (content or file parameters) or after (content2 parameter) current content and applying findReplace logic (based on how content source format)."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: ModifyBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "modifyBlog"

# End Variants for modifyBlog

# Variants for modifyPage
@dataclass
class ModifyPageOptions:
    """Optional parameters for action modifyPage"""
    content: str|None = None
    """Content for page, attachment, comment, or question."""
    content2: str|None = None
    """Content for page added after content and file content."""
    input: Iterable[str]|str|None = None
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    labels: str|None = None
    """Comma separated list of labels."""
    comment: str|None = None
    """Comment text."""
    minor: bool|None = None
    """Indicate minor update (no notifications) for a page update or attachment create."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    no_convert: bool|None = None
    """Do not convert content from wiki to storage format. Unless otherwise known, content is considered as wiki markup and converted."""
    markdown: bool|None = None
    """Attempt to convert rendered Markdown content to storage format. This may not work for all Markdown content. Consider using the markdown macro instead for a more accurate display of Markdown content in Confluence."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class ModifyPageGivenSpaceAndTitle(ConfluenceCommand):
    """Modify current page content by adding content before (content or file parameters) or after (content2 parameter) current content and applying findReplace logic (based on page content XHTML source). If append is specified, the file content will go after the current content."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: ModifyPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "modifyPage"

@dataclass
class ModifyPageGivenId(ConfluenceCommand):
    """Modify current page content by adding content before (content or file parameters) or after (content2 parameter) current content and applying findReplace logic (based on page content XHTML source). If append is specified, the file content will go after the current content."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: ModifyPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "modifyPage"

# End Variants for modifyPage

# Variants for movePage
@dataclass
class MovePageOptions:
    """Optional parameters for action movePage"""
    parent: str|None = None
    """Parent page title or id. @home title references space's home page."""
    new_space: str|None = None
    """New space key for copied or moved page."""
    reference_page: str|None = None
    """Title or id of a reference page for a movePage operation used in combination with position."""
    position: str|None = None
    """Position option relative to the reference page for a movePage operation: above or below. Default is below."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class MovePageGivenSpaceAndTitle(ConfluenceCommand):
    """Move a page to a new space or parent. Also, this can order a page in relationship (above or below) to a reference page. Use the continue parameter to ignore parent or reference page not found errors."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: MovePageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "movePage"

@dataclass
class MovePageGivenId(ConfluenceCommand):
    """Move a page to a new space or parent. Also, this can order a page in relationship (above or below) to a reference page. Use the continue parameter to ignore parent or reference page not found errors."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: MovePageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "movePage"

# End Variants for movePage

# Variants for moveShortcut
@dataclass
class MoveShortcutOptions:
    """Optional parameters for action moveShortcut"""
    position: str|None = None
    """Position option relative to the reference page for a movePage operation: above or below. Default is below."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class MoveShortcut(ConfluenceCommand):
    """Move a shortcut by name. Shortcuts can only be moved within their specific category. Shortcut can be moved to a new position indicated by @first, @last, or after a referenced shortcut by name. Default is @last Note that quick shortcuts appear in reverse order on the UI. It is not known why Confluence does this currently :(. Use continue to ignore not found errors."""
    space: str
    """Space key. For some actions, a space name may also work."""
    name: str
    """Space name or file name for attachment."""
    options: MoveShortcutOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "moveShortcut"

# End Variants for moveShortcut

# Variants for publishPage
@dataclass
class PublishPageOptions:
    """Optional parameters for action publishPage"""
    parent: str|None = None
    """Parent page title or id. @home title references space's home page."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    content2: str|None = None
    """Content for page added after content and file content."""
    input: Iterable[str]|str|None = None
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    comment: str|None = None
    """Comment text."""
    minor: bool|None = None
    """Indicate minor update (no notifications) for a page update or attachment create."""
    no_convert: bool|None = None
    """Do not convert content from wiki to storage format. Unless otherwise known, content is considered as wiki markup and converted."""
    target_server: str|None = None
    """Target server URL or site configuration reference for copy or publish requests."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""

@dataclass
class PublishPageGivenSpaceAndTitleAndNewTitle(ConfluenceCommand):
    """Publish a page constructed from source content with special rendering support. Source page is identified by space and title parameters. Resulting page is stored in newSpace with newTitle where newSpace defaults to the source space. Alternatively, content can be provided directly via the content, content2, and/or file parameters if no title is provided."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    new_title: str
    """New title of copied or renamed page."""
    options: PublishPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "publishPage"

@dataclass
class PublishPageGivenSpaceAndContentAndNewTitle(ConfluenceCommand):
    """Publish a page constructed from source content with special rendering support. Source page is identified by space and title parameters. Resulting page is stored in newSpace with newTitle where newSpace defaults to the source space. Alternatively, content can be provided directly via the content, content2, and/or file parameters if no title is provided."""
    space: str
    """Space key. For some actions, a space name may also work."""
    content: str
    """Content for page, attachment, comment, or question."""
    new_title: str
    """New title of copied or renamed page."""
    options: PublishPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "publishPage"

@dataclass
class PublishPageGivenSpaceAndFileAndNewTitle(ConfluenceCommand):
    """Publish a page constructed from source content with special rendering support. Source page is identified by space and title parameters. Resulting page is stored in newSpace with newTitle where newSpace defaults to the source space. Alternatively, content can be provided directly via the content, content2, and/or file parameters if no title is provided."""
    space: str
    """Space key. For some actions, a space name may also work."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    new_title: str
    """New title of copied or renamed page."""
    options: PublishPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "publishPage"

@dataclass
class PublishPageGivenNewSpaceAndTitleAndNewTitle(ConfluenceCommand):
    """Publish a page constructed from source content with special rendering support. Source page is identified by space and title parameters. Resulting page is stored in newSpace with newTitle where newSpace defaults to the source space. Alternatively, content can be provided directly via the content, content2, and/or file parameters if no title is provided."""
    new_space: str
    """New space key for copied or moved page."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    new_title: str
    """New title of copied or renamed page."""
    options: PublishPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "publishPage"

@dataclass
class PublishPageGivenNewSpaceAndContentAndNewTitle(ConfluenceCommand):
    """Publish a page constructed from source content with special rendering support. Source page is identified by space and title parameters. Resulting page is stored in newSpace with newTitle where newSpace defaults to the source space. Alternatively, content can be provided directly via the content, content2, and/or file parameters if no title is provided."""
    new_space: str
    """New space key for copied or moved page."""
    content: str
    """Content for page, attachment, comment, or question."""
    new_title: str
    """New title of copied or renamed page."""
    options: PublishPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "publishPage"

@dataclass
class PublishPageGivenNewSpaceAndFileAndNewTitle(ConfluenceCommand):
    """Publish a page constructed from source content with special rendering support. Source page is identified by space and title parameters. Resulting page is stored in newSpace with newTitle where newSpace defaults to the source space. Alternatively, content can be provided directly via the content, content2, and/or file parameters if no title is provided."""
    new_space: str
    """New space key for copied or moved page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    new_title: str
    """New title of copied or renamed page."""
    options: PublishPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "publishPage"

# End Variants for publishPage

# Variants for removeAllPermissionsForGroup

@dataclass
class RemoveAllPermissionsForGroup(ConfluenceCommand):
    """Remove all permissions for a group."""
    group: str
    """Group name. In the case of addUser, a comma separated list of group names."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAllPermissionsForGroup"

# End Variants for removeAllPermissionsForGroup

# Variants for removeApplicationLink
@dataclass
class RemoveApplicationLinkOptions:
    """Optional parameters for action removeApplicationLink"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveApplicationLinkGivenName(ConfluenceCommand):
    """Remove an application link identified by name or url."""
    name: str
    """Space name or file name for attachment."""
    options: RemoveApplicationLinkOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeApplicationLink"

@dataclass
class RemoveApplicationLinkGivenUrl(ConfluenceCommand):
    """Remove an application link identified by name or url."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: RemoveApplicationLinkOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeApplicationLink"

# End Variants for removeApplicationLink

# Variants for removeAttachment

@dataclass
class RemoveAttachmentGivenSpaceAndTitleAndName(ConfluenceCommand):
    """Remove an attachment by name from the page identified by space and title or page id. A numeric attachment id can substitute for the attachment name."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str
    """Space name or file name for attachment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAttachment"

@dataclass
class RemoveAttachmentGivenIdAndName(ConfluenceCommand):
    """Remove an attachment by name from the page identified by space and title or page id. A numeric attachment id can substitute for the attachment name."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    name: str
    """Space name or file name for attachment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAttachment"

# End Variants for removeAttachment

# Variants for removeAttachmentVersion
@dataclass
class RemoveAttachmentVersionOptions:
    """Optional parameters for action removeAttachmentVersion"""
    version: str|None = None
    """Item version."""

@dataclass
class RemoveAttachmentVersionGivenSpaceAndTitleAndName(ConfluenceCommand):
    """Remove an attachment version by version number. Version defaults to 0. 0 for version number means remove the current version. If the version being removed is the only version, its removal means the attachment will be removed. Identify the page by space and title or page id. Identify the attachment using the name parameter and the attachment name or id."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str
    """Space name or file name for attachment."""
    options: RemoveAttachmentVersionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAttachmentVersion"

@dataclass
class RemoveAttachmentVersionGivenIdAndName(ConfluenceCommand):
    """Remove an attachment version by version number. Version defaults to 0. 0 for version number means remove the current version. If the version being removed is the only version, its removal means the attachment will be removed. Identify the page by space and title or page id. Identify the attachment using the name parameter and the attachment name or id."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    name: str
    """Space name or file name for attachment."""
    options: RemoveAttachmentVersionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAttachmentVersion"

# End Variants for removeAttachmentVersion

# Variants for removeAttachmentVersions
@dataclass
class RemoveAttachmentVersionsOptions:
    """Optional parameters for action removeAttachmentVersions"""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class RemoveAttachmentVersionsGivenSpaceAndTitleAndNameAndDate(ConfluenceCommand):
    """Remove multiple versions of an attachment. Use limit parameter to remove versions except for the last limit versions. Use date parameter to remove versions created before that date. Use regex parameter to remove versions whose comment matches the pattern. Use '--options just1=day' to remove versions except for the last version created each day and similarly for week, month, and year. If multiple criteria are specified, all must be met. A numeric attachment id can substitute for the attachment name. By default, a CSV output lists each attachment version indicating versions selected and why - use quiet parameter to suppress the output or the file parameter. Use the simulate parameter to log the details without running the removal so you can verify your selection criteria. Use @all for name to automatically repeat the request for each attachment on the page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str
    """Space name or file name for attachment."""
    date: str
    """Date specified in the default client date format or as defined by the dateFormat parameter"""
    options: RemoveAttachmentVersionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAttachmentVersions"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class RemoveAttachmentVersionsGivenSpaceAndTitleAndNameAndLimit(ConfluenceCommand):
    """Remove multiple versions of an attachment. Use limit parameter to remove versions except for the last limit versions. Use date parameter to remove versions created before that date. Use regex parameter to remove versions whose comment matches the pattern. Use '--options just1=day' to remove versions except for the last version created each day and similarly for week, month, and year. If multiple criteria are specified, all must be met. A numeric attachment id can substitute for the attachment name. By default, a CSV output lists each attachment version indicating versions selected and why - use quiet parameter to suppress the output or the file parameter. Use the simulate parameter to log the details without running the removal so you can verify your selection criteria. Use @all for name to automatically repeat the request for each attachment on the page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str
    """Space name or file name for attachment."""
    limit: str
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    options: RemoveAttachmentVersionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAttachmentVersions"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class RemoveAttachmentVersionsGivenSpaceAndTitleAndNameAndRegex(ConfluenceCommand):
    """Remove multiple versions of an attachment. Use limit parameter to remove versions except for the last limit versions. Use date parameter to remove versions created before that date. Use regex parameter to remove versions whose comment matches the pattern. Use '--options just1=day' to remove versions except for the last version created each day and similarly for week, month, and year. If multiple criteria are specified, all must be met. A numeric attachment id can substitute for the attachment name. By default, a CSV output lists each attachment version indicating versions selected and why - use quiet parameter to suppress the output or the file parameter. Use the simulate parameter to log the details without running the removal so you can verify your selection criteria. Use @all for name to automatically repeat the request for each attachment on the page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str
    """Space name or file name for attachment."""
    regex: str
    """Regular expression for condition matching or list filtering."""
    options: RemoveAttachmentVersionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAttachmentVersions"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class RemoveAttachmentVersionsGivenIdAndNameAndDate(ConfluenceCommand):
    """Remove multiple versions of an attachment. Use limit parameter to remove versions except for the last limit versions. Use date parameter to remove versions created before that date. Use regex parameter to remove versions whose comment matches the pattern. Use '--options just1=day' to remove versions except for the last version created each day and similarly for week, month, and year. If multiple criteria are specified, all must be met. A numeric attachment id can substitute for the attachment name. By default, a CSV output lists each attachment version indicating versions selected and why - use quiet parameter to suppress the output or the file parameter. Use the simulate parameter to log the details without running the removal so you can verify your selection criteria. Use @all for name to automatically repeat the request for each attachment on the page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    name: str
    """Space name or file name for attachment."""
    date: str
    """Date specified in the default client date format or as defined by the dateFormat parameter"""
    options: RemoveAttachmentVersionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAttachmentVersions"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class RemoveAttachmentVersionsGivenIdAndNameAndLimit(ConfluenceCommand):
    """Remove multiple versions of an attachment. Use limit parameter to remove versions except for the last limit versions. Use date parameter to remove versions created before that date. Use regex parameter to remove versions whose comment matches the pattern. Use '--options just1=day' to remove versions except for the last version created each day and similarly for week, month, and year. If multiple criteria are specified, all must be met. A numeric attachment id can substitute for the attachment name. By default, a CSV output lists each attachment version indicating versions selected and why - use quiet parameter to suppress the output or the file parameter. Use the simulate parameter to log the details without running the removal so you can verify your selection criteria. Use @all for name to automatically repeat the request for each attachment on the page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    name: str
    """Space name or file name for attachment."""
    limit: str
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    options: RemoveAttachmentVersionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAttachmentVersions"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class RemoveAttachmentVersionsGivenIdAndNameAndRegex(ConfluenceCommand):
    """Remove multiple versions of an attachment. Use limit parameter to remove versions except for the last limit versions. Use date parameter to remove versions created before that date. Use regex parameter to remove versions whose comment matches the pattern. Use '--options just1=day' to remove versions except for the last version created each day and similarly for week, month, and year. If multiple criteria are specified, all must be met. A numeric attachment id can substitute for the attachment name. By default, a CSV output lists each attachment version indicating versions selected and why - use quiet parameter to suppress the output or the file parameter. Use the simulate parameter to log the details without running the removal so you can verify your selection criteria. Use @all for name to automatically repeat the request for each attachment on the page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    name: str
    """Space name or file name for attachment."""
    regex: str
    """Regular expression for condition matching or list filtering."""
    options: RemoveAttachmentVersionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAttachmentVersions"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for removeAttachmentVersions

# Variants for removeBlog
@dataclass
class RemoveBlogOptions:
    """Optional parameters for action removeBlog"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveBlogGivenSpaceAndTitle(ConfluenceCommand):
    """Remove a blog entry. Use continue to ignore a not found error."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: RemoveBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeBlog"

@dataclass
class RemoveBlogGivenId(ConfluenceCommand):
    """Remove a blog entry. Use continue to ignore a not found error."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RemoveBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeBlog"

# End Variants for removeBlog

# Variants for removeComment
@dataclass
class RemoveCommentOptions:
    """Optional parameters for action removeComment"""
    descendents: bool|None = None
    """All descendents for a page."""

@dataclass
class RemoveComment(ConfluenceCommand):
    """Remove a specific comment."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RemoveCommentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeComment"

# End Variants for removeComment

# Variants for removeComments
@dataclass
class RemoveCommentsOptions:
    """Optional parameters for action removeComments"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""

@dataclass
class RemoveCommentsGivenSpaceAndTitle(ConfluenceCommand):
    """Remove all comments from a page or blog."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: RemoveCommentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeComments"

@dataclass
class RemoveCommentsGivenId(ConfluenceCommand):
    """Remove all comments from a page or blog."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RemoveCommentsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeComments"

# End Variants for removeComments

# Variants for removeContent
@dataclass
class RemoveContentOptions:
    """Optional parameters for action removeContent"""
    descendents: bool|None = None
    """All descendents for a page."""

@dataclass
class RemoveContent(ConfluenceCommand):
    """Remove content (pages, blogs) by id. Option to remove descendents."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RemoveContentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeContent"

# End Variants for removeContent

# Variants for removeContentVersion
@dataclass
class RemoveContentVersionOptions:
    """Optional parameters for action removeContentVersion"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""

@dataclass
class RemoveContentVersionGivenSpaceAndTitleAndVersion(ConfluenceCommand):
    """Remove a version from the revision history of some content like a page or blog. Server supports pages only."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    version: str
    """Item version."""
    options: RemoveContentVersionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeContentVersion"

@dataclass
class RemoveContentVersionGivenIdAndVersion(ConfluenceCommand):
    """Remove a version from the revision history of some content like a page or blog. Server supports pages only."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    version: str
    """Item version."""
    options: RemoveContentVersionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeContentVersion"

# End Variants for removeContentVersion

# Variants for removeContentVersions
@dataclass
class RemoveContentVersionsOptions:
    """Optional parameters for action removeContentVersions"""
    date: str|None = None
    """Date specified in the default client date format or as defined by the dateFormat parameter"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class RemoveContentVersionsGivenSpaceAndTitle(ConfluenceCommand):
    """Remove multiple versions from the revision history of some content like a page or blog. Server supports pages only. Use limit to remove versions except for the last limit versions. Use date to remove versions created before that date. Use regex parameter to remove versions whose edit message (comment) matches the pattern. Use '--options just1=day' to remove versions except for the last version created each day and similarly for week, month, and year. If multiple criteria are specified, all must be met. A numeric attachment id can substitute for the attachment name. By default, a CSV output lists each attachment version indicating versions selected and why - use quiet parameter to suppress the output. Use the simulate parameter to log the details without running the removal so you can verify your selection criteria."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: RemoveContentVersionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeContentVersions"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class RemoveContentVersionsGivenId(ConfluenceCommand):
    """Remove multiple versions from the revision history of some content like a page or blog. Server supports pages only. Use limit to remove versions except for the last limit versions. Use date to remove versions created before that date. Use regex parameter to remove versions whose edit message (comment) matches the pattern. Use '--options just1=day' to remove versions except for the last version created each day and similarly for week, month, and year. If multiple criteria are specified, all must be met. A numeric attachment id can substitute for the attachment name. By default, a CSV output lists each attachment version indicating versions selected and why - use quiet parameter to suppress the output. Use the simulate parameter to log the details without running the removal so you can verify your selection criteria."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RemoveContentVersionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeContentVersions"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for removeContentVersions

# Variants for removeEntityProperty
@dataclass
class RemoveEntityPropertyOptions:
    """Optional parameters for action removeEntityProperty"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveEntityPropertyGivenSpaceAndTitleAndName(ConfluenceCommand):
    """Remove an entity property name and value. Use continue parameter to ignore a not found error."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str
    """Space name or file name for attachment."""
    options: RemoveEntityPropertyOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeEntityProperty"

@dataclass
class RemoveEntityPropertyGivenIdAndName(ConfluenceCommand):
    """Remove an entity property name and value. Use continue parameter to ignore a not found error."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    name: str
    """Space name or file name for attachment."""
    options: RemoveEntityPropertyOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeEntityProperty"

# End Variants for removeEntityProperty

# Variants for removeGroup
@dataclass
class RemoveGroupOptions:
    """Optional parameters for action removeGroup"""
    default_group: str|None = None
    """Default group to move users on removeGroup action."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveGroup(ConfluenceCommand):
    """Remove a group."""
    group: str
    """Group name. In the case of addUser, a comma separated list of group names."""
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

# Variants for removeLabels
@dataclass
class RemoveLabelsOptions:
    """Optional parameters for action removeLabels"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str|None = None
    """Space name or file name for attachment."""
    version: str|None = None
    """Item version."""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""

@dataclass
class RemoveLabelsGivenSpaceAndLabels(ConfluenceCommand):
    """Remove labels from a page, blog, space, or attachment. For an attachment, provide either the attachment numeric id or a name together with a content id or space and title. Use @all for the labels parameter to remove all labels."""
    space: str
    """Space key. For some actions, a space name may also work."""
    labels: str
    """Comma separated list of labels."""
    options: RemoveLabelsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeLabels"

@dataclass
class RemoveLabelsGivenIdAndLabels(ConfluenceCommand):
    """Remove labels from a page, blog, space, or attachment. For an attachment, provide either the attachment numeric id or a name together with a content id or space and title. Use @all for the labels parameter to remove all labels."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    labels: str
    """Comma separated list of labels."""
    options: RemoveLabelsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeLabels"

# End Variants for removeLabels

# Variants for removeLicense

@dataclass
class RemoveLicense(ConfluenceCommand):
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

# Variants for removePage
@dataclass
class RemovePageOptions:
    """Optional parameters for action removePage"""
    descendents: bool|None = None
    """All descendents for a page."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemovePageGivenSpaceAndTitle(ConfluenceCommand):
    """Remove a page and, optionally, all descendents. Use continue to ignore a not found error."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: RemovePageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removePage"

@dataclass
class RemovePageGivenId(ConfluenceCommand):
    """Remove a page and, optionally, all descendents. Use continue to ignore a not found error."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RemovePageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removePage"

# End Variants for removePage

# Variants for removePageVersion

@dataclass
class RemovePageVersionGivenSpaceAndTitleAndVersion(ConfluenceCommand):
    """Deprecated. Use removeContentVersion. Remove a version from the revision history of a page."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    version: str
    """Item version."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removePageVersion"

@dataclass
class RemovePageVersionGivenIdAndVersion(ConfluenceCommand):
    """Deprecated. Use removeContentVersion. Remove a version from the revision history of a page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    version: str
    """Item version."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removePageVersion"

# End Variants for removePageVersion

# Variants for removePageVersions
@dataclass
class RemovePageVersionsOptions:
    """Optional parameters for action removePageVersions"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    date: str|None = None
    """Date specified in the default client date format or as defined by the dateFormat parameter"""
    simulate: bool|None = None
    """Simulate running actions. Log the action that would be taken."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class RemovePageVersionsGivenSpaceAndTitle(ConfluenceCommand):
    """Deprecated. Use removeContentVersions. Remove multiple versions from the revision history of a page. Use limit to remove versions except for the last limit versions. Use date to remove versions created before that date."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: RemovePageVersionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removePageVersions"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class RemovePageVersionsGivenId(ConfluenceCommand):
    """Deprecated. Use removeContentVersions. Remove multiple versions from the revision history of a page. Use limit to remove versions except for the last limit versions. Use date to remove versions created before that date."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RemovePageVersionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removePageVersions"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for removePageVersions

# Variants for removePermissions
@dataclass
class RemovePermissionsOptions:
    """Optional parameters for action removePermissions"""
    children: bool|None = None
    """Immediate children for a page."""
    descendents: bool|None = None
    """All descendents for a page."""

@dataclass
class RemovePermissionsGivenSpaceAndPermissionsAndTitleAndId(ConfluenceCommand):
    """Remove permissions from page or space. A permission of @all can be used. For page permissions, use space and title or page id. Valid page permissions are: [View, Edit]. Valid space permissions are: [VIEWSPACE, REMOVEOWNCONTENT, EDITSPACE, REMOVEPAGE, EDITBLOG, REMOVEBLOG, CREATEATTACHMENT, REMOVEATTACHMENT, COMMENT, REMOVECOMMENT, SETPAGEPERMISSIONS, REMOVEMAIL, EXPORTSPACE, SETSPACEPERMISSIONS]. Group or userId can also be a comma separated list of groups and users."""
    space: str
    """Space key. For some actions, a space name may also work."""
    permissions: str
    """Comma separated list of permissions. Page permissions:  view, edit. Space permissions: viewspace, removeowncontent, editspace, removepage, editblog, removeblog, createattachment, removeattachment, comment, removecomment, setpagepermissions, removemail, exportspace, setspacepermissions."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RemovePermissionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removePermissions"

@dataclass
class RemovePermissionsGivenSpaceAndPermissionsAndGroupAndUserId(ConfluenceCommand):
    """Remove permissions from page or space. A permission of @all can be used. For page permissions, use space and title or page id. Valid page permissions are: [View, Edit]. Valid space permissions are: [VIEWSPACE, REMOVEOWNCONTENT, EDITSPACE, REMOVEPAGE, EDITBLOG, REMOVEBLOG, CREATEATTACHMENT, REMOVEATTACHMENT, COMMENT, REMOVECOMMENT, SETPAGEPERMISSIONS, REMOVEMAIL, EXPORTSPACE, SETSPACEPERMISSIONS]. Group or userId can also be a comma separated list of groups and users."""
    space: str
    """Space key. For some actions, a space name may also work."""
    permissions: str
    """Comma separated list of permissions. Page permissions:  view, edit. Space permissions: viewspace, removeowncontent, editspace, removepage, editblog, removeblog, createattachment, removeattachment, comment, removecomment, setpagepermissions, removemail, exportspace, setspacepermissions."""
    group: str
    """Group name. In the case of addUser, a comma separated list of group names."""
    user_id: str
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    options: RemovePermissionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removePermissions"

# End Variants for removePermissions

# Variants for removeQuestion

@dataclass
class RemoveQuestionGivenId(ConfluenceCommand):
    """Remove a question from Confluence Questions. Not available for Cloud."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeQuestion"

@dataclass
class RemoveQuestionGivenTitle(ConfluenceCommand):
    """Remove a question from Confluence Questions. Not available for Cloud."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeQuestion"

# End Variants for removeQuestion

# Variants for removeQuestionWatch

@dataclass
class RemoveQuestionWatchGivenId(ConfluenceCommand):
    """Set to not watch a question for the current user. Use @all for title to set the unwatch all flag. Not available for Cloud."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeQuestionWatch"

@dataclass
class RemoveQuestionWatchGivenTitle(ConfluenceCommand):
    """Set to not watch a question for the current user. Use @all for title to set the unwatch all flag. Not available for Cloud."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeQuestionWatch"

# End Variants for removeQuestionWatch

# Variants for removeShortcut
@dataclass
class RemoveShortcutOptions:
    """Optional parameters for action removeShortcut"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveShortcutGivenSpaceAndName(ConfluenceCommand):
    """Remove a shortcut by name or id. Only one shortcut with that name will be removed. Only shortcuts in category quick can be removed. Use --name @all to remove all space shortcuts. Shortcuts show up on the UI. Use continue to ignore not found errors."""
    space: str
    """Space key. For some actions, a space name may also work."""
    name: str
    """Space name or file name for attachment."""
    options: RemoveShortcutOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeShortcut"

@dataclass
class RemoveShortcutGivenSpaceAndId(ConfluenceCommand):
    """Remove a shortcut by name or id. Only one shortcut with that name will be removed. Only shortcuts in category quick can be removed. Use --name @all to remove all space shortcuts. Shortcuts show up on the UI. Use continue to ignore not found errors."""
    space: str
    """Space key. For some actions, a space name may also work."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RemoveShortcutOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeShortcut"

# End Variants for removeShortcut

# Variants for removeSpace

@dataclass
class RemoveSpace(ConfluenceCommand):
    """Remove a space by key."""
    space: str
    """Space key. For some actions, a space name may also work."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeSpace"

# End Variants for removeSpace

# Variants for removeTopic

@dataclass
class RemoveTopicGivenTopic(ConfluenceCommand):
    """Remove a Confluence Questions topic. Not available for Cloud."""
    topic: str
    """Confluence Questions topic."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeTopic"

@dataclass
class RemoveTopicGivenId(ConfluenceCommand):
    """Remove a Confluence Questions topic. Not available for Cloud."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeTopic"

# End Variants for removeTopic

# Variants for removeTopicWatch

@dataclass
class RemoveTopicWatchGivenTopic(ConfluenceCommand):
    """Set to not watch this topic for the current user. Not available for Cloud."""
    topic: str
    """Confluence Questions topic."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeTopicWatch"

@dataclass
class RemoveTopicWatchGivenId(ConfluenceCommand):
    """Set to not watch this topic for the current user. Not available for Cloud."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeTopicWatch"

# End Variants for removeTopicWatch

# Variants for removeTrash
@dataclass
class RemoveTrashOptions:
    """Optional parameters for action removeTrash"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    id: str|None = None
    """Numeric id of an item like a page, blog, or comment."""

@dataclass
class RemoveTrash(ConfluenceCommand):
    """Permanently remove a single page or blogpost from trashed items or remove all trashed items for a space."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: RemoveTrashOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeTrash"

# End Variants for removeTrash

# Variants for removeUser
@dataclass
class RemoveUserOptions:
    """Optional parameters for action removeUser"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveUser(ConfluenceCommand):
    """Remote a user. Not available for Cloud."""
    user_id: str
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    options: RemoveUserOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeUser"

# End Variants for removeUser

# Variants for removeUserFromGroup
@dataclass
class RemoveUserFromGroupOptions:
    """Optional parameters for action removeUserFromGroup"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveUserFromGroup(ConfluenceCommand):
    """Remove user from a group."""
    user_id: str
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    group: str
    """Group name. In the case of addUser, a comma separated list of group names."""
    options: RemoveUserFromGroupOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeUserFromGroup"

# End Variants for removeUserFromGroup

# Variants for removeWatch
@dataclass
class RemoveWatchOptions:
    """Optional parameters for action removeWatch"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    user_id: str|None = None
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    children: bool|None = None
    """Immediate children for a page."""
    descendents: bool|None = None
    """All descendents for a page."""

@dataclass
class RemoveWatchGivenSpace(ConfluenceCommand):
    """Remove watch from page or space for a user. If userId is not provided, the current user will be used. On server, only the current user is valid for space watches."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: RemoveWatchOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeWatch"

@dataclass
class RemoveWatchGivenId(ConfluenceCommand):
    """Remove watch from page or space for a user. If userId is not provided, the current user will be used. On server, only the current user is valid for space watches."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RemoveWatchOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeWatch"

# End Variants for removeWatch

# Variants for removeWebhook

@dataclass
class RemoveWebhookGivenName(ConfluenceCommand):
    """Remove a user defined webhook."""
    name: str
    """Space name or file name for attachment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeWebhook"

@dataclass
class RemoveWebhookGivenId(ConfluenceCommand):
    """Remove a user defined webhook."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeWebhook"

# End Variants for removeWebhook

# Variants for renamePage
@dataclass
class RenamePageOptions:
    """Optional parameters for action renamePage"""
    new_title: str|None = None
    """New title of copied or renamed page."""
    parent: str|None = None
    """Parent page title or id. @home title references space's home page."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""

@dataclass
class RenamePageGivenSpaceAndTitle(ConfluenceCommand):
    """Rename or move a page. If newTitle is not provided, the new title will be determined from the existing title after applying any find and replace logic. Note that the space cannot be changed with this action - use movePage instead."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: RenamePageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "renamePage"

@dataclass
class RenamePageGivenId(ConfluenceCommand):
    """Rename or move a page. If newTitle is not provided, the new title will be determined from the existing title after applying any find and replace logic. Note that the space cannot be changed with this action - use movePage instead."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RenamePageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "renamePage"

# End Variants for renamePage

# Variants for render
@dataclass
class RenderOptions:
    """Optional parameters for action render"""
    id: str|None = None
    """Numeric id of an item like a page, blog, or comment."""
    space: str|None = None
    """Space key. For some actions, a space name may also work."""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    content: str|None = None
    """Content for page, attachment, comment, or question."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    clean: bool|None = None
    """Rendered data as a single block of HTML without the HTML preamble and styles."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class Render(ConfluenceCommand):
    """If content is specified, it is rendered in the context of the page identified by id or space parameters where title defaults to space home page. If no context is specified, content is rendered without context. If content is not specified, then the context page or blog is rendered. If content is '-', content is read from standard input. Find and replace is applied to the rendered content."""
    options: RenderOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "render"

# End Variants for render

# Variants for renderBlog
@dataclass
class RenderBlogOptions:
    """Optional parameters for action renderBlog"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    clean: bool|None = None
    """Rendered data as a single block of HTML without the HTML preamble and styles."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class RenderBlog(ConfluenceCommand):
    """Render a blog entry. See also renderPage."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: RenderBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "renderBlog"

# End Variants for renderBlog

# Variants for renderPage
@dataclass
class RenderPageOptions:
    """Optional parameters for action renderPage"""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    clean: bool|None = None
    """Rendered data as a single block of HTML without the HTML preamble and styles."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class RenderPageGivenSpaceAndTitle(ConfluenceCommand):
    """Render page or blog. By default, a styled view is rendered. Use the clean parameter to render a simple view. For advanced uses, '--options representation=...' can be used to requests a specific output representation of the page. Consult Confluence documentation for representations available for your instance."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    options: RenderPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "renderPage"

@dataclass
class RenderPageGivenId(ConfluenceCommand):
    """Render page or blog. By default, a styled view is rendered. Use the clean parameter to render a simple view. For advanced uses, '--options representation=...' can be used to requests a specific output representation of the page. Consult Confluence documentation for representations available for your instance."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: RenderPageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "renderPage"

# End Variants for renderPage

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
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""

@dataclass
class RenderRequestGivenUrl(ConfluenceCommand):
    """Render URL based request. URL can be a partial URL. The response data modified by optional findReplace processing is returned. Use '--pretty' to format returned JSON data in a more readable form. If content parameters are provided like space and title, replacement variables are available and if no URL is provided will default to render the page using '/pages/viewpage.action?pageId=@pageId@'."""
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
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RenderRequestGivenSpace(ConfluenceCommand):
    """Render URL based request. URL can be a partial URL. The response data modified by optional findReplace processing is returned. Use '--pretty' to format returned JSON data in a more readable form. If content parameters are provided like space and title, replacement variables are available and if no URL is provided will default to render the page using '/pages/viewpage.action?pageId=@pageId@'."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: RenderRequestOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "renderRequest"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for renderRequest

# Variants for restoreExport
@dataclass
class RestoreExportOptions:
    """Optional parameters for action restoreExport"""
    no_index: bool|None = None
    """Do not force re-index after restore."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class RestoreExport(ConfluenceCommand):
    """Restore export (import) from file in the Confluence home/restore directory. By default, the action waits and reports status. Use '--options noWait' to return immediately after the task has been submitted. Note that this action does not support a restore for a spaceExport generated file as there are no public API supporting such a feature. Restore of spaceExport files will need to be done via the Confluence Cloud web portal."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RestoreExportOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "restoreExport"

# End Variants for restoreExport

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
class RunFromAppListGivenInput(ConfluenceCommand):
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
class RunFromAppListGivenCommon(ConfluenceCommand):
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
class RunFromAppListGivenFile(ConfluenceCommand):
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

# Variants for runFromApplicationLinkList
@dataclass
class RunFromApplicationLinkListOptions:
    """Optional parameters for action runFromApplicationLinkList"""
    type: str|None = None
    """Application type, shortcut type, or similar depending on context."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class RunFromApplicationLinkListGivenInput(ConfluenceCommand):
    """Run actions for each application link. Filtering available like for getApplicationLinkList."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromApplicationLinkListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromApplicationLinkList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromApplicationLinkListGivenCommon(ConfluenceCommand):
    """Run actions for each application link. Filtering available like for getApplicationLinkList."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromApplicationLinkListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromApplicationLinkList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromApplicationLinkListGivenFile(ConfluenceCommand):
    """Run actions for each application link. Filtering available like for getApplicationLinkList."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromApplicationLinkListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromApplicationLinkList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromApplicationLinkList

# Variants for runFromAttachmentList
@dataclass
class RunFromAttachmentListOptions:
    """Optional parameters for action runFromAttachmentList"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class RunFromAttachmentListGivenCqlAndInput(ConfluenceCommand):
    """Run actions for attachments that match the same conditions as getAttachmentList. @all can be used as a special value for the space parameter."""
    cql: str
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentListGivenCqlAndCommon(ConfluenceCommand):
    """Run actions for attachments that match the same conditions as getAttachmentList. @all can be used as a special value for the space parameter."""
    cql: str
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentListGivenCqlAndFile(ConfluenceCommand):
    """Run actions for attachments that match the same conditions as getAttachmentList. @all can be used as a special value for the space parameter."""
    cql: str
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentListGivenSpaceAndInput(ConfluenceCommand):
    """Run actions for attachments that match the same conditions as getAttachmentList. @all can be used as a special value for the space parameter."""
    space: str
    """Space key. For some actions, a space name may also work."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentListGivenSpaceAndCommon(ConfluenceCommand):
    """Run actions for attachments that match the same conditions as getAttachmentList. @all can be used as a special value for the space parameter."""
    space: str
    """Space key. For some actions, a space name may also work."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentListGivenSpaceAndFile(ConfluenceCommand):
    """Run actions for attachments that match the same conditions as getAttachmentList. @all can be used as a special value for the space parameter."""
    space: str
    """Space key. For some actions, a space name may also work."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentListGivenIdAndInput(ConfluenceCommand):
    """Run actions for attachments that match the same conditions as getAttachmentList. @all can be used as a special value for the space parameter."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentListGivenIdAndCommon(ConfluenceCommand):
    """Run actions for attachments that match the same conditions as getAttachmentList. @all can be used as a special value for the space parameter."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentListGivenIdAndFile(ConfluenceCommand):
    """Run actions for attachments that match the same conditions as getAttachmentList. @all can be used as a special value for the space parameter."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromAttachmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromAttachmentList

# Variants for runFromAttachmentVersionList
@dataclass
class RunFromAttachmentVersionListOptions:
    """Optional parameters for action runFromAttachmentVersionList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class RunFromAttachmentVersionListGivenSpaceAndTitleAndInput(ConfluenceCommand):
    """Run actions for each version of an attachment that match the same conditions as getAttachmentVersionList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromAttachmentVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentVersionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentVersionListGivenSpaceAndTitleAndCommon(ConfluenceCommand):
    """Run actions for each version of an attachment that match the same conditions as getAttachmentVersionList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromAttachmentVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentVersionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentVersionListGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Run actions for each version of an attachment that match the same conditions as getAttachmentVersionList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromAttachmentVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentVersionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentVersionListGivenIdAndInput(ConfluenceCommand):
    """Run actions for each version of an attachment that match the same conditions as getAttachmentVersionList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromAttachmentVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentVersionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentVersionListGivenIdAndCommon(ConfluenceCommand):
    """Run actions for each version of an attachment that match the same conditions as getAttachmentVersionList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromAttachmentVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentVersionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromAttachmentVersionListGivenIdAndFile(ConfluenceCommand):
    """Run actions for each version of an attachment that match the same conditions as getAttachmentVersionList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromAttachmentVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromAttachmentVersionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromAttachmentVersionList

# Variants for runFromBlogList
@dataclass
class RunFromBlogListOptions:
    """Optional parameters for action runFromBlogList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    regex2: str|None = None
    """Regular expression for secondary content matching. In some cases, filtering on a secondary field may be needed."""
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
class RunFromBlogListGivenSpaceAndInput(ConfluenceCommand):
    """Run actions for each blog from a blog list based on the same parameters as getBlogList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromBlogListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBlogList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBlogListGivenSpaceAndCommon(ConfluenceCommand):
    """Run actions for each blog from a blog list based on the same parameters as getBlogList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromBlogListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBlogList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBlogListGivenSpaceAndFile(ConfluenceCommand):
    """Run actions for each blog from a blog list based on the same parameters as getBlogList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromBlogListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBlogList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBlogListGivenLabelsAndInput(ConfluenceCommand):
    """Run actions for each blog from a blog list based on the same parameters as getBlogList."""
    labels: str
    """Comma separated list of labels."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromBlogListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBlogList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBlogListGivenLabelsAndCommon(ConfluenceCommand):
    """Run actions for each blog from a blog list based on the same parameters as getBlogList."""
    labels: str
    """Comma separated list of labels."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromBlogListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBlogList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBlogListGivenLabelsAndFile(ConfluenceCommand):
    """Run actions for each blog from a blog list based on the same parameters as getBlogList."""
    labels: str
    """Comma separated list of labels."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromBlogListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBlogList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromBlogList

# Variants for runFromCommentList
@dataclass
class RunFromCommentListOptions:
    """Optional parameters for action runFromCommentList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class RunFromCommentListGivenSpaceAndTitleAndInput(ConfluenceCommand):
    """Run actions for each comment from a page. Filtering available like for getCommentList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromCommentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromCommentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromCommentListGivenSpaceAndTitleAndCommon(ConfluenceCommand):
    """Run actions for each comment from a page. Filtering available like for getCommentList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromCommentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromCommentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromCommentListGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Run actions for each comment from a page. Filtering available like for getCommentList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromCommentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromCommentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromCommentListGivenIdAndInput(ConfluenceCommand):
    """Run actions for each comment from a page. Filtering available like for getCommentList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromCommentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromCommentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromCommentListGivenIdAndCommon(ConfluenceCommand):
    """Run actions for each comment from a page. Filtering available like for getCommentList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromCommentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromCommentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromCommentListGivenIdAndFile(ConfluenceCommand):
    """Run actions for each comment from a page. Filtering available like for getCommentList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromCommentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromCommentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromCommentList

# Variants for runFromContentList
@dataclass
class RunFromContentListOptions:
    """Optional parameters for action runFromContentList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class RunFromContentListGivenCqlAndInput(ConfluenceCommand):
    """Run actions for each content item found from a content search (like getContentList)."""
    cql: str
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromContentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromContentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromContentListGivenCqlAndCommon(ConfluenceCommand):
    """Run actions for each content item found from a content search (like getContentList)."""
    cql: str
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromContentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromContentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromContentListGivenCqlAndFile(ConfluenceCommand):
    """Run actions for each content item found from a content search (like getContentList)."""
    cql: str
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromContentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromContentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromContentList

# Variants for runFromEntityPropertyList
@dataclass
class RunFromEntityPropertyListOptions:
    """Optional parameters for action runFromEntityPropertyList"""
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
class RunFromEntityPropertyListGivenSpaceAndTitleAndInput(ConfluenceCommand):
    """Run action for each entity property with optional regex filtering on name."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromEntityPropertyListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromEntityPropertyList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromEntityPropertyListGivenSpaceAndTitleAndCommon(ConfluenceCommand):
    """Run action for each entity property with optional regex filtering on name."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromEntityPropertyListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromEntityPropertyList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromEntityPropertyListGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Run action for each entity property with optional regex filtering on name."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromEntityPropertyListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromEntityPropertyList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromEntityPropertyListGivenIdAndInput(ConfluenceCommand):
    """Run action for each entity property with optional regex filtering on name."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromEntityPropertyListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromEntityPropertyList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromEntityPropertyListGivenIdAndCommon(ConfluenceCommand):
    """Run action for each entity property with optional regex filtering on name."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromEntityPropertyListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromEntityPropertyList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromEntityPropertyListGivenIdAndFile(ConfluenceCommand):
    """Run action for each entity property with optional regex filtering on name."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromEntityPropertyListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromEntityPropertyList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromEntityPropertyList

# Variants for runFromGroupList
@dataclass
class RunFromGroupListOptions:
    """Optional parameters for action runFromGroupList"""
    user_id: str|None = None
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
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
class RunFromGroupListGivenInput(ConfluenceCommand):
    """Run actions for each group matching selection criteria similar to getGroupList."""
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
class RunFromGroupListGivenCommon(ConfluenceCommand):
    """Run actions for each group matching selection criteria similar to getGroupList."""
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
class RunFromGroupListGivenFile(ConfluenceCommand):
    """Run actions for each group matching selection criteria similar to getGroupList."""
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

# Variants for runFromPageList
@dataclass
class RunFromPageListOptions:
    """Optional parameters for action runFromPageList"""
    cql: str|None = None
    """CQL content search. Cloud references is https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/. Server reference is https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/."""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
    parent: str|None = None
    """Parent page title or id. @home title references space's home page."""
    ancestors: bool|None = None
    """Ancestors for a page."""
    descendents: bool|None = None
    """All descendents for a page."""
    children: bool|None = None
    """Immediate children for a page."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    regex2: str|None = None
    """Regular expression for secondary content matching. In some cases, filtering on a secondary field may be needed."""
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
class RunFromPageListGivenLabelsAndInput(ConfluenceCommand):
    """Run actions for each page from a page list based on the same parameters as getPageList."""
    labels: str
    """Comma separated list of labels."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPageList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPageListGivenLabelsAndCommon(ConfluenceCommand):
    """Run actions for each page from a page list based on the same parameters as getPageList."""
    labels: str
    """Comma separated list of labels."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPageList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPageListGivenLabelsAndFile(ConfluenceCommand):
    """Run actions for each page from a page list based on the same parameters as getPageList."""
    labels: str
    """Comma separated list of labels."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPageList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPageListGivenSpaceAndInput(ConfluenceCommand):
    """Run actions for each page from a page list based on the same parameters as getPageList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPageList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPageListGivenSpaceAndCommon(ConfluenceCommand):
    """Run actions for each page from a page list based on the same parameters as getPageList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPageList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPageListGivenSpaceAndFile(ConfluenceCommand):
    """Run actions for each page from a page list based on the same parameters as getPageList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPageList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPageListGivenIdAndInput(ConfluenceCommand):
    """Run actions for each page from a page list based on the same parameters as getPageList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPageList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPageListGivenIdAndCommon(ConfluenceCommand):
    """Run actions for each page from a page list based on the same parameters as getPageList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPageList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPageListGivenIdAndFile(ConfluenceCommand):
    """Run actions for each page from a page list based on the same parameters as getPageList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromPageListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPageList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromPageList

# Variants for runFromQuestionList
@dataclass
class RunFromQuestionListOptions:
    """Optional parameters for action runFromQuestionList"""
    filter: str|None = None
    """Question search filter. Valid values are: POPULAR, RECENT, UNANSWERED."""
    topic: str|None = None
    """Confluence Questions topic."""
    user_id: str|None = None
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is to get the most recent entries."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
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
class RunFromQuestionListGivenInput(ConfluenceCommand):
    """Run actions for each question matching selection criteria similar to getQuestionList."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromQuestionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromQuestionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromQuestionListGivenCommon(ConfluenceCommand):
    """Run actions for each question matching selection criteria similar to getQuestionList."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromQuestionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromQuestionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromQuestionListGivenFile(ConfluenceCommand):
    """Run actions for each question matching selection criteria similar to getQuestionList."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromQuestionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromQuestionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromQuestionList

# Variants for runFromShortcutList
@dataclass
class RunFromShortcutListOptions:
    """Optional parameters for action runFromShortcutList"""
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
class RunFromShortcutListGivenSpaceAndInput(ConfluenceCommand):
    """Run actions for each shortcut matching selection criteria similar to getShortcutList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromShortcutListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromShortcutList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromShortcutListGivenSpaceAndCommon(ConfluenceCommand):
    """Run actions for each shortcut matching selection criteria similar to getShortcutList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromShortcutListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromShortcutList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromShortcutListGivenSpaceAndFile(ConfluenceCommand):
    """Run actions for each shortcut matching selection criteria similar to getShortcutList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromShortcutListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromShortcutList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromShortcutList

# Variants for runFromSpaceList
@dataclass
class RunFromSpaceListOptions:
    """Optional parameters for action runFromSpaceList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    regex2: str|None = None
    """Regular expression for secondary content matching. In some cases, filtering on a secondary field may be needed."""
    personal: bool|None = None
    """Include personal spaces."""
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
class RunFromSpaceListGivenInput(ConfluenceCommand):
    """Run actions for each space. Defaults to global spaces only. Filtering available like for getSpaceList."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromSpaceListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSpaceList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromSpaceListGivenCommon(ConfluenceCommand):
    """Run actions for each space. Defaults to global spaces only. Filtering available like for getSpaceList."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromSpaceListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSpaceList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromSpaceListGivenFile(ConfluenceCommand):
    """Run actions for each space. Defaults to global spaces only. Filtering available like for getSpaceList."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromSpaceListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromSpaceList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromSpaceList

# Variants for runFromTopicList
@dataclass
class RunFromTopicListOptions:
    """Optional parameters for action runFromTopicList"""
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
class RunFromTopicListGivenInput(ConfluenceCommand):
    """Run actions for each topic matching selection criteria similar to getTopicList."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromTopicListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTopicList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromTopicListGivenCommon(ConfluenceCommand):
    """Run actions for each topic matching selection criteria similar to getTopicList."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromTopicListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTopicList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromTopicListGivenFile(ConfluenceCommand):
    """Run actions for each topic matching selection criteria similar to getTopicList."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromTopicListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTopicList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromTopicList

# Variants for runFromTrashList
@dataclass
class RunFromTrashListOptions:
    """Optional parameters for action runFromTrashList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class RunFromTrashListGivenSpaceAndInput(ConfluenceCommand):
    """Run actions for each content item found from a spaces trash list like getTrashList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromTrashListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTrashList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromTrashListGivenSpaceAndCommon(ConfluenceCommand):
    """Run actions for each content item found from a spaces trash list like getTrashList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromTrashListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTrashList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromTrashListGivenSpaceAndFile(ConfluenceCommand):
    """Run actions for each content item found from a spaces trash list like getTrashList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromTrashListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTrashList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromTrashList

# Variants for runFromUserList
@dataclass
class RunFromUserListOptions:
    """Optional parameters for action runFromUserList"""
    group: str|None = None
    """Group name. In the case of addUser, a comma separated list of group names."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
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
class RunFromUserListGivenInput(ConfluenceCommand):
    """Run actions for each user."""
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
class RunFromUserListGivenCommon(ConfluenceCommand):
    """Run actions for each user."""
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
class RunFromUserListGivenFile(ConfluenceCommand):
    """Run actions for each user."""
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

# Variants for runFromWatchList
@dataclass
class RunFromWatchListOptions:
    """Optional parameters for action runFromWatchList"""
    title: str|None = None
    """Page, blog, or attachment title. @home title references space's home page."""
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
class RunFromWatchListGivenSpaceAndInput(ConfluenceCommand):
    """Run actions for each page or space watch matching selection criteria similar to getWatchList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromWatchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWatchList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromWatchListGivenSpaceAndCommon(ConfluenceCommand):
    """Run actions for each page or space watch matching selection criteria similar to getWatchList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromWatchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWatchList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromWatchListGivenSpaceAndFile(ConfluenceCommand):
    """Run actions for each page or space watch matching selection criteria similar to getWatchList."""
    space: str
    """Space key. For some actions, a space name may also work."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromWatchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWatchList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromWatchListGivenIdAndInput(ConfluenceCommand):
    """Run actions for each page or space watch matching selection criteria similar to getWatchList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromWatchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWatchList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromWatchListGivenIdAndCommon(ConfluenceCommand):
    """Run actions for each page or space watch matching selection criteria similar to getWatchList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromWatchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWatchList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromWatchListGivenIdAndFile(ConfluenceCommand):
    """Run actions for each page or space watch matching selection criteria similar to getWatchList."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromWatchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWatchList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromWatchList

# Variants for runFromWebhookList
@dataclass
class RunFromWebhookListOptions:
    """Optional parameters for action runFromWebhookList"""
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
class RunFromWebhookListGivenInput(ConfluenceCommand):
    """Run action for each webhook with regex filtering on webhook name."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromWebhookListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWebhookList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromWebhookListGivenCommon(ConfluenceCommand):
    """Run action for each webhook with regex filtering on webhook name."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromWebhookListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWebhookList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromWebhookListGivenFile(ConfluenceCommand):
    """Run action for each webhook with regex filtering on webhook name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromWebhookListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromWebhookList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromWebhookList

# Variants for setEntityProperty
@dataclass
class SetEntityPropertyOptions:
    """Optional parameters for action setEntityProperty"""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""

@dataclass
class SetEntityPropertyGivenSpaceAndTitleAndNameAndValue(ConfluenceCommand):
    """Set an entity property value for page or other content. Use --replace to replace an existing entry. Value must be valid JSON."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    name: str
    """Space name or file name for attachment."""
    value: str
    """Field value or condition value for matching."""
    options: SetEntityPropertyOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "setEntityProperty"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class SetEntityPropertyGivenIdAndNameAndValue(ConfluenceCommand):
    """Set an entity property value for page or other content. Use --replace to replace an existing entry. Value must be valid JSON."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    name: str
    """Space name or file name for attachment."""
    value: str
    """Field value or condition value for matching."""
    options: SetEntityPropertyOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "setEntityProperty"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for setEntityProperty

# Variants for showShortcut
@dataclass
class ShowShortcutOptions:
    """Optional parameters for action showShortcut"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class ShowShortcutGivenSpaceAndName(ConfluenceCommand):
    """Make visible a shortcut by name or id. Only shortcuts in category main can be shown or hidden. Use --name @all to show all available shortcuts. Shortcuts show up on the UI. Use continue to ignore not found errors."""
    space: str
    """Space key. For some actions, a space name may also work."""
    name: str
    """Space name or file name for attachment."""
    options: ShowShortcutOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "showShortcut"

@dataclass
class ShowShortcutGivenSpaceAndId(ConfluenceCommand):
    """Make visible a shortcut by name or id. Only shortcuts in category main can be shown or hidden. Use --name @all to show all available shortcuts. Shortcuts show up on the UI. Use continue to ignore not found errors."""
    space: str
    """Space key. For some actions, a space name may also work."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: ShowShortcutOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "showShortcut"

# End Variants for showShortcut

# Variants for storeBlog
@dataclass
class StoreBlogOptions:
    """Optional parameters for action storeBlog"""
    day_of_month: str|None = None
    """Day of month for blog entry. Use negative values for going back to previous months."""
    month: str|None = None
    """Month for blog entry. Defaults to current month."""
    year: str|None = None
    """Year for blog entry. Defaults to current year."""
    labels: str|None = None
    """Comma separated list of labels."""
    content2: str|None = None
    """Content for page added after content and file content."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    no_convert: bool|None = None
    """Do not convert content from wiki to storage format. Unless otherwise known, content is considered as wiki markup and converted."""
    markdown: bool|None = None
    """Attempt to convert rendered Markdown content to storage format. This may not work for all Markdown content. Consider using the markdown macro instead for a more accurate display of Markdown content in Confluence."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class StoreBlogGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Add or update a blog entry."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: StoreBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "storeBlog"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class StoreBlogGivenSpaceAndTitleAndContent(ConfluenceCommand):
    """Add or update a blog entry."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    content: str
    """Content for page, attachment, comment, or question."""
    options: StoreBlogOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "storeBlog"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for storeBlog

# Variants for storePage
@dataclass
class StorePageOptions:
    """Optional parameters for action storePage"""
    parent: str|None = None
    """Parent page title or id. @home title references space's home page."""
    labels: str|None = None
    """Comma separated list of labels."""
    comment: str|None = None
    """Comment text."""
    minor: bool|None = None
    """Indicate minor update (no notifications) for a page update or attachment create."""
    content2: str|None = None
    """Content for page added after content and file content."""
    type: str|None = None
    """Application type, shortcut type, or similar depending on context."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    no_convert: bool|None = None
    """Do not convert content from wiki to storage format. Unless otherwise known, content is considered as wiki markup and converted."""
    markdown: bool|None = None
    """Attempt to convert rendered Markdown content to storage format. This may not work for all Markdown content. Consider using the markdown macro instead for a more accurate display of Markdown content in Confluence."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class StorePageGivenSpaceAndTitleAndContent(ConfluenceCommand):
    """Create or update a page. Content for the page is provided by one or more of the content, content2, and file parameters. If more than once of these is used, they ordering on the page is first the content parameter value, followed by a copy of the data from the file parameter, and then followed by the content2 parameter value. This allows you to wrap file content be before and after content which is important in many scenarios. For example, Confluence wiki macros can be used to wrap file content in this way. For instance, markdown content using the markdown macro like '--content "{markdown}" --file my.md --content2 "{markdown}"'. By default, content is treated as Confluence wiki markup. Use '--noConvert' to instead treat as simple text. To convert markdown content to Confluence native content, use '--markdown' with the warning that this may degrade the formatting and may need manual repair. For HTML content, you may want ACLI to automatically modify the HTML to convert some HTML constructs to Confluence native support like anchors and anchor links. Use '--modifyHtml' to request this support. HTML content may still need additional modification or manual repair for better migration to Confluence. Find replace parameters can be used to modify content prior to inserting into the page. This is an important technique for migrating content."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    content: str
    """Content for page, attachment, comment, or question."""
    options: StorePageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "storePage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class StorePageGivenSpaceAndTitleAndFile(ConfluenceCommand):
    """Create or update a page. Content for the page is provided by one or more of the content, content2, and file parameters. If more than once of these is used, they ordering on the page is first the content parameter value, followed by a copy of the data from the file parameter, and then followed by the content2 parameter value. This allows you to wrap file content be before and after content which is important in many scenarios. For example, Confluence wiki macros can be used to wrap file content in this way. For instance, markdown content using the markdown macro like '--content "{markdown}" --file my.md --content2 "{markdown}"'. By default, content is treated as Confluence wiki markup. Use '--noConvert' to instead treat as simple text. To convert markdown content to Confluence native content, use '--markdown' with the warning that this may degrade the formatting and may need manual repair. For HTML content, you may want ACLI to automatically modify the HTML to convert some HTML constructs to Confluence native support like anchors and anchor links. Use '--modifyHtml' to request this support. HTML content may still need additional modification or manual repair for better migration to Confluence. Find replace parameters can be used to modify content prior to inserting into the page. This is an important technique for migrating content."""
    space: str
    """Space key. For some actions, a space name may also work."""
    title: str
    """Page, blog, or attachment title. @home title references space's home page."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: StorePageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "storePage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class StorePageGivenIdAndContent(ConfluenceCommand):
    """Create or update a page. Content for the page is provided by one or more of the content, content2, and file parameters. If more than once of these is used, they ordering on the page is first the content parameter value, followed by a copy of the data from the file parameter, and then followed by the content2 parameter value. This allows you to wrap file content be before and after content which is important in many scenarios. For example, Confluence wiki macros can be used to wrap file content in this way. For instance, markdown content using the markdown macro like '--content "{markdown}" --file my.md --content2 "{markdown}"'. By default, content is treated as Confluence wiki markup. Use '--noConvert' to instead treat as simple text. To convert markdown content to Confluence native content, use '--markdown' with the warning that this may degrade the formatting and may need manual repair. For HTML content, you may want ACLI to automatically modify the HTML to convert some HTML constructs to Confluence native support like anchors and anchor links. Use '--modifyHtml' to request this support. HTML content may still need additional modification or manual repair for better migration to Confluence. Find replace parameters can be used to modify content prior to inserting into the page. This is an important technique for migrating content."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    content: str
    """Content for page, attachment, comment, or question."""
    options: StorePageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "storePage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class StorePageGivenIdAndFile(ConfluenceCommand):
    """Create or update a page. Content for the page is provided by one or more of the content, content2, and file parameters. If more than once of these is used, they ordering on the page is first the content parameter value, followed by a copy of the data from the file parameter, and then followed by the content2 parameter value. This allows you to wrap file content be before and after content which is important in many scenarios. For example, Confluence wiki macros can be used to wrap file content in this way. For instance, markdown content using the markdown macro like '--content "{markdown}" --file my.md --content2 "{markdown}"'. By default, content is treated as Confluence wiki markup. Use '--noConvert' to instead treat as simple text. To convert markdown content to Confluence native content, use '--markdown' with the warning that this may degrade the formatting and may need manual repair. For HTML content, you may want ACLI to automatically modify the HTML to convert some HTML constructs to Confluence native support like anchors and anchor links. Use '--modifyHtml' to request this support. HTML content may still need additional modification or manual repair for better migration to Confluence. Find replace parameters can be used to modify content prior to inserting into the page. This is an important technique for migrating content."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: StorePageOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "storePage"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for storePage

# Variants for uninstallApp
@dataclass
class UninstallAppOptions:
    """Optional parameters for action uninstallApp"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class UninstallApp(ConfluenceCommand):
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

# Variants for updateComment
@dataclass
class UpdateCommentOptions:
    """Optional parameters for action updateComment"""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    input: Iterable[str]|str|None = None
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class UpdateCommentGivenIdAndComment(ConfluenceCommand):
    """Update contents of an existing comment identified by id. Use --comment @commentBody@ to replace the existing content with content determined by find and replace logic."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    comment: str
    """Comment text."""
    options: UpdateCommentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateComment"

@dataclass
class UpdateCommentGivenIdAndContent(ConfluenceCommand):
    """Update contents of an existing comment identified by id. Use --comment @commentBody@ to replace the existing content with content determined by find and replace logic."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    content: str
    """Content for page, attachment, comment, or question."""
    options: UpdateCommentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateComment"

@dataclass
class UpdateCommentGivenIdAndFile(ConfluenceCommand):
    """Update contents of an existing comment identified by id. Use --comment @commentBody@ to replace the existing content with content determined by find and replace logic."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: UpdateCommentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateComment"

# End Variants for updateComment

# Variants for updateSpace
@dataclass
class UpdateSpaceOptions:
    """Optional parameters for action updateSpace"""
    name: str|None = None
    """Space name or file name for attachment."""
    home: str|None = None
    """Title of home page for a space. Default for a new space is Home."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class UpdateSpaceGivenSpace(ConfluenceCommand):
    """Update space name, description, and home page. Space status (current or archived) can also be updated using '--options status=archived' or '--options status=current'."""
    space: str
    """Space key. For some actions, a space name may also work."""
    options: UpdateSpaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateSpace"

@dataclass
class UpdateSpaceGivenUserId(ConfluenceCommand):
    """Update space name, description, and home page. Space status (current or archived) can also be updated using '--options status=archived' or '--options status=current'."""
    user_id: str
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    options: UpdateSpaceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateSpace"

# End Variants for updateSpace

# Variants for updateTopic
@dataclass
class UpdateTopicOptions:
    """Optional parameters for action updateTopic"""
    description: str|None = None
    """Descriptive text."""
    featured: bool|None = None
    """Confluence Questions featured topic."""
    avatar: str|None = None
    """Topic avatar URL."""

@dataclass
class UpdateTopicGivenTopic(ConfluenceCommand):
    """Update an existing Confluence Questions topic. Not available for Cloud."""
    topic: str
    """Confluence Questions topic."""
    options: UpdateTopicOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateTopic"

@dataclass
class UpdateTopicGivenId(ConfluenceCommand):
    """Update an existing Confluence Questions topic. Not available for Cloud."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: UpdateTopicOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateTopic"

# End Variants for updateTopic

# Variants for updateUser
@dataclass
class UpdateUserOptions:
    """Optional parameters for action updateUser"""
    user_email: str|None = None
    """User email for user management actions."""
    user_full_name: str|None = None
    """User name for user management actions. Atlassian sometimes refers to this as display name."""
    user_password: str|None = None
    """User password for user management actions."""
    activate: bool|None = None
    """Activate user. Requires secure administrator sessions be off in you Security Configuration."""
    deactivate: bool|None = None
    """Deactivate user. Requires secure administrator sessions be off in you Security Configuration."""

@dataclass
class UpdateUser(ConfluenceCommand):
    """Update user information. Not available for Cloud."""
    user_id: str
    """User id for user management and other actions. Atlassian sometimes refers to this as user name. For Cloud, use an account id or a public name."""
    options: UpdateUserOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateUser"

# End Variants for updateUser

# Variants for updateWebhook
@dataclass
class UpdateWebhookOptions:
    """Optional parameters for action updateWebhook"""
    url: str|None = None
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    events: Iterable[str]|str|None = None
    """Comma separated list of webhook events. Valid events may vary by Confluence version, hosting type, or other factors. Consult Atlassian documentation for latest details. Known events are attachment_created, attachment_removed, attachment_restored, attachment_trashed, attachment_updated, blog_created, blog_removed, blog_restored, blog_trashed, blog_updated, blueprint_page_created, comment_created, comment_removed, comment_updated, content_created, content_restored, content_trashed, content_updated, content_permissions_updated, group_created, group_removed, label_added, label_created, label_deleted, label_removed, page_children_reordered, page_created, page_moved, page_removed, page_restored, page_trashed, page_updated, space_created, space_logo_updated, space_permissions_updated, space permissions, space_removed, space_updated, theme_enabled, user_created, user_deactivated, user_followed, user_reactivated, user_removed."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class UpdateWebhookGivenId(ConfluenceCommand):
    """Update an existing user defined webhook. Use '--options enable' or '--options disable' to change the status of the webhook."""
    id: str
    """Numeric id of an item like a page, blog, or comment."""
    options: UpdateWebhookOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateWebhook"

@dataclass
class UpdateWebhookGivenName(ConfluenceCommand):
    """Update an existing user defined webhook. Use '--options enable' or '--options disable' to change the status of the webhook."""
    name: str
    """Space name or file name for attachment."""
    options: UpdateWebhookOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateWebhook"

# End Variants for updateWebhook

# Variants for validateLicense

@dataclass
class ValidateLicense(ConfluenceCommand):
    """Validates the ACLI Connector is enabled and licensed on the server."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "validateLicense"

# End Variants for validateLicense
