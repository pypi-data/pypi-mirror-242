from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class BitbucketCommand(Command):
    pass

@dataclass
class BitbucketClient(RemoteClient):
    def execute(self, command: BitbucketCommand):
        return super().do_execute(command)

# Variants for addAccessToken

@dataclass
class AddAccessToken(BitbucketCommand):
    """Add a new access token for the current user."""
    name: str
    """Name of an item or entity."""
    permission: str
    """Global, project, or repository permission. Global permissions are: LICENSED_USER, PROJECT_CREATE, ADMIN. SYS_ADMIN. Project permissions are: PROJECT_READ, PROJECT_WRITE, REPO_CREATE, PROJECT_ADMIN. Repository permissions are: REPO_READ, REPO_WRITE, REPO_ADMIN. For addAccessToken, this parameter can be a comma separated list of a project permission and a repository permission. Note, REPO_CREATE requires Bitbucket 8.2 or higher."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addAccessToken"

# End Variants for addAccessToken

# Variants for addApplicationLink
@dataclass
class AddApplicationLinkOptions:
    """Optional parameters for action addApplicationLink"""
    name: str|None = None
    """Name of an item or entity."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class AddApplicationLink(BitbucketCommand):
    """Add an application link to another application. By default, both incoming and outgoing links are enabled and configured without impersonation (users are not shared). Use the options parameter to customize the behavior. Use '--options impersonate' to enable shared users. Other examples are '--options disableIncoming' and '--options disableOutgoing'. If another link of the same type already exists as primary, use '--options primary' to force the new link to be primary instead."""
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

# Variants for addBranch
@dataclass
class AddBranchOptions:
    """Optional parameters for action addBranch"""
    message: str|None = None
    """Commit message or similar."""

@dataclass
class AddBranch(BitbucketCommand):
    """Deprecated. Add repository branch starting at the specified commit id."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    branch: str
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    options: AddBranchOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addBranch"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addBranch

# Variants for addBranchRestriction
@dataclass
class AddBranchRestrictionOptions:
    """Optional parameters for action addBranchRestriction"""
    restriction: str|None = None
    """Branch restriction. Defaults to read-only. Restrictions are: read-only, no-deletes, fast-forward-only, pull-request-only."""
    matching_type: str|None = None
    """Branch matching type. Defaults to BRANCH. Types are: BRANCH, MODEL, PATTERN"""
    user_id: str|None = None
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    group: str|None = None
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""

@dataclass
class AddBranchRestriction(BitbucketCommand):
    """Add branch level restriction with optional exemptions for users and groups. Restriction defaults to read-only. Restriction applies to branches matching by branch name, pattern, or model. Default is matching on branch name. User exceptions can be specified by the userId parameter as a common separated list of user ids. Group exceptions can be specified by the group parameter as a common separated list of group names."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    branch: str
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
    options: AddBranchRestrictionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addBranchRestriction"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addBranchRestriction

# Variants for addGroup
@dataclass
class AddGroupOptions:
    """Optional parameters for action addGroup"""
    preserve_case: bool|None = None
    """Some actions like addUser and addGroup may automatically lowercase names usually because the construct is case insensitive on some hosting platforms. Use this switch to override the default behavior and preserve the case."""

@dataclass
class AddGroup(BitbucketCommand):
    """Add a new group."""
    group: str
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
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

# Variants for addLicense
@dataclass
class AddLicenseOptions:
    """Optional parameters for action addLicense"""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class AddLicenseGivenAppAndLicense(BitbucketCommand):
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
class AddLicenseGivenAppAndFile(BitbucketCommand):
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
class AddLicenses(BitbucketCommand):
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

# Variants for addReviewCondition
@dataclass
class AddReviewConditionOptions:
    """Optional parameters for action addReviewCondition"""
    repository: str|None = None
    """Repository slug, name, or id."""
    from_: str|None = None
    """Also known as a source reference. For repository pull request, a from branch reference. For commit list, a commit or reference to retrieve commits after (exclusive)."""
    matching_type: str|None = None
    """Branch matching type. Defaults to BRANCH. Types are: BRANCH, MODEL, PATTERN"""
    to: str|None = None
    """Also known as a target reference. For repository pull request, a to branch reference. For commit list, a commit or reference to retrieve commits before (inclusive)."""
    to_matching_type: str|None = None
    """Branch matching type for a target branch. Defaults to BRANCH. Types are: BRANCH, MODEL, PATTERN"""
    review_approval_count: str|None = None
    """Number of reviewers on the reviewer list that are required to approve the pull request before it can be merged. The number must be less than or equal to the number of default reviewers provided."""

@dataclass
class AddReviewCondition(BitbucketCommand):
    """Add a review condition with default reviewers for a project or repository."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    reviewers: str
    """Pull request reviewers. Comma separated list of user ids."""
    options: AddReviewConditionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addReviewCondition"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addReviewCondition

# Variants for addSshKey
@dataclass
class AddSshKeyOptions:
    """Optional parameters for action addSshKey"""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class AddSshKey(BitbucketCommand):
    """Add an SSH key for a user."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddSshKeyOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addSshKey"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addSshKey

# Variants for addUser
@dataclass
class AddUserOptions:
    """Optional parameters for action addUser"""
    user_full_name: str|None = None
    """User name for user management actions."""
    user_password: str|None = None
    """User password for user management actions."""
    notify: bool|None = None
    """Notify user after user is added."""
    preserve_case: bool|None = None
    """Some actions like addUser and addGroup may automatically lowercase names usually because the construct is case insensitive on some hosting platforms. Use this switch to override the default behavior and preserve the case."""

@dataclass
class AddUser(BitbucketCommand):
    """Add a new user."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    user_email: str
    """User email for user management actions."""
    options: AddUserOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addUser"

# End Variants for addUser

# Variants for addUserToGroup
@dataclass
class AddUserToGroupOptions:
    """Optional parameters for action addUserToGroup"""
    auto_group: bool|None = None
    """Groups are automatically added when referenced in add user functions."""
    preserve_case: bool|None = None
    """Some actions like addUser and addGroup may automatically lowercase names usually because the construct is case insensitive on some hosting platforms. Use this switch to override the default behavior and preserve the case."""

@dataclass
class AddUserToGroup(BitbucketCommand):
    """Add user to a group."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    group: str
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
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

# Variants for addWebhook
@dataclass
class AddWebhookOptions:
    """Optional parameters for action addWebhook"""
    events: Iterable[str]|str|None = None
    """Comma separated list of webhook events. Valid events may vary by Bitbucket version, hosting type, or other factors. Consult Atlassian documentation for latest details. Some known events are: repo:refs_changed, repo:forked, repo:comment:added, repo:comment:edited, repo:comment:deleted, mirror:repo_synchronized, pr:opened, pr:from_ref_updated, pr:modified, pr:reviewer:updated, pr:reviewer:approved, pr:reviewer:unapproved, pr:reviewer:needs_work, pr:merged, pr:declined, pr:deleted, pr:comment:added, pr:comment:edited, pr:comment:deleted"""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""

@dataclass
class AddWebhook(BitbucketCommand):
    """Add a user defined webhook. By default, the webhook will be enabled. Use '--options disable' to disable the webhook. By default, the webhook will send a payload body as part of the post to the url depending on the type of event. Use --options disable to disable the webhook. Use --options "secret=..." to set a data integrity verification string. For Post Webhooks for Bitbucket users, use '--options postWebhooks'."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    name: str
    """Name of an item or entity."""
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

# Variants for createBranch
@dataclass
class CreateBranchOptions:
    """Optional parameters for action createBranch"""
    message: str|None = None
    """Commit message or similar."""

@dataclass
class CreateBranch(BitbucketCommand):
    """Create repository branch starting at the specified commit id."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    branch: str
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    options: CreateBranchOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "createBranch"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for createBranch

# Variants for createProject
@dataclass
class CreateProjectOptions:
    """Optional parameters for action createProject"""
    name: str|None = None
    """Name of an item or entity."""
    description: str|None = None
    """Description."""
    public: bool|None = None
    """Allow the project to be visible to the public (users without a Bitbucket account)."""

@dataclass
class CreateProject(BitbucketCommand):
    """Create a new project."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    options: CreateProjectOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "createProject"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for createProject

# Variants for createPullRequest
@dataclass
class CreatePullRequestOptions:
    """Optional parameters for action createPullRequest"""
    name: str|None = None
    """Name of an item or entity."""
    description: str|None = None
    """Description."""
    reviewers: str|None = None
    """Pull request reviewers. Comma separated list of user ids."""

@dataclass
class CreatePullRequest(BitbucketCommand):
    """Create a new pull request."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    from_: str
    """Also known as a source reference. For repository pull request, a from branch reference. For commit list, a commit or reference to retrieve commits after (exclusive)."""
    to: str
    """Also known as a target reference. For repository pull request, a to branch reference. For commit list, a commit or reference to retrieve commits before (inclusive)."""
    pull_request: str
    """Pull request id or name."""
    options: CreatePullRequestOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "createPullRequest"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for createPullRequest

# Variants for createRepository
@dataclass
class CreateRepositoryOptions:
    """Optional parameters for action createRepository"""
    name: str|None = None
    """Name of an item or entity."""
    public: bool|None = None
    """Allow the project to be visible to the public (users without a Bitbucket account)."""
    forkable: bool|None = None
    """Allow a repository to be forkable."""

@dataclass
class CreateRepository(BitbucketCommand):
    """Create a new repository."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    options: CreateRepositoryOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "createRepository"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for createRepository

# Variants for declinePullRequest

@dataclass
class DeclinePullRequest(BitbucketCommand):
    """Decline a pull request."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    pull_request: str
    """Pull request id or name."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "declinePullRequest"

# End Variants for declinePullRequest

# Variants for deleteBranch
@dataclass
class DeleteBranchOptions:
    """Optional parameters for action deleteBranch"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class DeleteBranch(BitbucketCommand):
    """Delete a repository branch."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    branch: str
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
    options: DeleteBranchOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "deleteBranch"

# End Variants for deleteBranch

# Variants for deleteProject
@dataclass
class DeleteProjectOptions:
    """Optional parameters for action deleteProject"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class DeleteProject(BitbucketCommand):
    """Delete a project."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    options: DeleteProjectOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "deleteProject"

# End Variants for deleteProject

# Variants for deleteRepository
@dataclass
class DeleteRepositoryOptions:
    """Optional parameters for action deleteRepository"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class DeleteRepository(BitbucketCommand):
    """Delete a repository."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    options: DeleteRepositoryOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "deleteRepository"

# End Variants for deleteRepository

# Variants for disableApp

@dataclass
class DisableApp(BitbucketCommand):
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

# Variants for disableHook
@dataclass
class DisableHookOptions:
    """Optional parameters for action disableHook"""
    repository: str|None = None
    """Repository slug, name, or id."""

@dataclass
class DisableHook(BitbucketCommand):
    """Disable hook by name or key for a repository."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    hook: str
    """Hook name or key of the form 'plugin key:hook key'."""
    options: DisableHookOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "disableHook"

# End Variants for disableHook

# Variants for enableApp

@dataclass
class EnableApp(BitbucketCommand):
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

# Variants for enableHook
@dataclass
class EnableHookOptions:
    """Optional parameters for action enableHook"""
    repository: str|None = None
    """Repository slug, name, or id."""

@dataclass
class EnableHook(BitbucketCommand):
    """Enable hook by name or key for a project or repository scoped hook."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    hook: str
    """Hook name or key of the form 'plugin key:hook key'."""
    options: EnableHookOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "enableHook"

# End Variants for enableHook

# Variants for getAccessTokenList
@dataclass
class GetAccessTokenListOptions:
    """Optional parameters for action getAccessTokenList"""
    user: str|None = None
    """User name for remote access."""
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
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetAccessTokenList(BitbucketCommand):
    """Get a list of access tokens associated with a user with regex filtering on name."""
    options: GetAccessTokenListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAccessTokenList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAccessTokenList

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
class GetApp(BitbucketCommand):
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
class GetAppList(BitbucketCommand):
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
class GetApplicationLinkOptions:
    """Optional parameters for action getApplicationLink"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetApplicationLinkGivenName(BitbucketCommand):
    """Get information for an application link identified by name or url."""
    name: str
    """Name of an item or entity."""
    options: GetApplicationLinkOptions | None = None
    """ Action specific options """
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
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetApplicationLinkGivenUrl(BitbucketCommand):
    """Get information for an application link identified by name or url."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: GetApplicationLinkOptions | None = None
    """ Action specific options """
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
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getApplicationLink

# Variants for getApplicationLinkList
@dataclass
class GetApplicationLinkListOptions:
    """Optional parameters for action getApplicationLinkList"""
    type: str|None = None
    """Application link type."""
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
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetApplicationLinkList(BitbucketCommand):
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

# Variants for getAuditLogList
@dataclass
class GetAuditLogListOptions:
    """Optional parameters for action getAuditLogList"""
    start_date: str|None = None
    """Earliest date for date filtering. Default is to get the most recent entries."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
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
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetAuditLogList(BitbucketCommand):
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

# Variants for getBranch
@dataclass
class GetBranchOptions:
    """Optional parameters for action getBranch"""
    branch: str|None = None
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetBranch(BitbucketCommand):
    """Get repository branch information."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    options: GetBranchOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBranch"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBranch

# Variants for getBranchList
@dataclass
class GetBranchListOptions:
    """Optional parameters for action getBranchList"""
    order: str|None = None
    """Order returned. Branch ordering values: ALPHABETICAL, MODIFICATION"""
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
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetBranchList(BitbucketCommand):
    """List branches for a repository."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    options: GetBranchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBranchList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBranchList

# Variants for getBranchRestriction
@dataclass
class GetBranchRestrictionOptions:
    """Optional parameters for action getBranchRestriction"""
    restriction: str|None = None
    """Branch restriction. Defaults to read-only. Restrictions are: read-only, no-deletes, fast-forward-only, pull-request-only."""
    matching_type: str|None = None
    """Branch matching type. Defaults to BRANCH. Types are: BRANCH, MODEL, PATTERN"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetBranchRestrictionGivenProjectAndRepositoryAndId(BitbucketCommand):
    """Get branch level restriction by id or with specific restriction, matching type, and branch value. Restriction defaults to read-only. Restriction applies to branches matching by branch name, pattern, or model. Default is matching on branch name."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    options: GetBranchRestrictionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBranchRestriction"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetBranchRestrictionGivenProjectAndRepositoryAndBranch(BitbucketCommand):
    """Get branch level restriction by id or with specific restriction, matching type, and branch value. Restriction defaults to read-only. Restriction applies to branches matching by branch name, pattern, or model. Default is matching on branch name."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    branch: str
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
    options: GetBranchRestrictionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBranchRestriction"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBranchRestriction

# Variants for getBranchRestrictionList
@dataclass
class GetBranchRestrictionListOptions:
    """Optional parameters for action getBranchRestrictionList"""
    branch: str|None = None
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
    matching_type: str|None = None
    """Branch matching type. Defaults to BRANCH. Types are: BRANCH, MODEL, PATTERN"""
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
class GetBranchRestrictionList(BitbucketCommand):
    """List branch restrictions for a repository with optional filtering on matchingType, branch, and regex pattern matching on restriction."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    options: GetBranchRestrictionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBranchRestrictionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBranchRestrictionList

# Variants for getBuildStatusList
@dataclass
class GetBuildStatusListOptions:
    """Optional parameters for action getBuildStatusList"""
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
class GetBuildStatusList(BitbucketCommand):
    """Get a list of build status entries associated with a changeset id."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    options: GetBuildStatusListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getBuildStatusList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getBuildStatusList

# Variants for getCommit
@dataclass
class GetCommitOptions:
    """Optional parameters for action getCommit"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetCommit(BitbucketCommand):
    """Get commit information."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    options: GetCommitOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getCommit"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getCommit

# Variants for getCommitList
@dataclass
class GetCommitListOptions:
    """Optional parameters for action getCommitList"""
    from_: str|None = None
    """Also known as a source reference. For repository pull request, a from branch reference. For commit list, a commit or reference to retrieve commits after (exclusive)."""
    to: str|None = None
    """Also known as a target reference. For repository pull request, a to branch reference. For commit list, a commit or reference to retrieve commits before (inclusive)."""
    user_id: str|None = None
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is to get the most recent entries."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
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
class GetCommitList(BitbucketCommand):
    """List commits for a repository with regex filtering on comment. Additional filtering by from and to references (commitId, branch, or tags), author's user id (or name), and date ranges. For example, to get the commit list for a branch, set the to parameter the branch reference. Use '--options merges=' with include, exclude, or only value to control whether merge commits are included."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    options: GetCommitListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getCommitList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getCommitList

# Variants for getFileInfo
@dataclass
class GetFileInfoOptions:
    """Optional parameters for action getFileInfo"""
    revision: str|None = None
    """Repository revision id like a commit id, branch, tag, or special value like HEAD (for Git) and tip for Mercurial."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetFileInfo(BitbucketCommand):
    """Get information on a repository file at a default or specific revision."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    path: str
    """Source path."""
    options: GetFileInfoOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getFileInfo"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getFileInfo

# Variants for getFileList
@dataclass
class GetFileListOptions:
    """Optional parameters for action getFileList"""
    revision: str|None = None
    """Repository revision id like a commit id, branch, tag, or special value like HEAD (for Git) and tip for Mercurial."""
    descendents: bool|None = None
    """All descendent files for a directory."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
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
class GetFileList(BitbucketCommand):
    """Get file and directory list with regex filtering on path."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    path: str
    """Source path."""
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

# Variants for getGroupList
@dataclass
class GetGroupListOptions:
    """Optional parameters for action getGroupList"""
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
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetGroupList(BitbucketCommand):
    """List groups."""
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

# Variants for getHook
@dataclass
class GetHookOptions:
    """Optional parameters for action getHook"""
    repository: str|None = None
    """Repository slug, name, or id."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetHook(BitbucketCommand):
    """Get hook information by hook name or key for a project or repository scoped hook."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    hook: str
    """Hook name or key of the form 'plugin key:hook key'."""
    options: GetHookOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getHook"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getHook

# Variants for getHookList
@dataclass
class GetHookListOptions:
    """Optional parameters for action getHookList"""
    repository: str|None = None
    """Repository slug, name, or id."""
    enabled: bool|None = None
    """Subset to include enabled hooks in list of hooks."""
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
class GetHookList(BitbucketCommand):
    """Get a list of hooks available for a project or repository with regex filtering on key and name. Use the enabled parameter to list only enabled hooks."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    options: GetHookListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getHookList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getHookList

# Variants for getPermissionList
@dataclass
class GetPermissionListOptions:
    """Optional parameters for action getPermissionList"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetPermissionList(BitbucketCommand):
    """Get a list of global permissions."""
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

# Variants for getProject
@dataclass
class GetProjectOptions:
    """Optional parameters for action getProject"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetProject(BitbucketCommand):
    """Get project information."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    options: GetProjectOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getProject"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getProject

# Variants for getProjectList
@dataclass
class GetProjectListOptions:
    """Optional parameters for action getProjectList"""
    permission: str|None = None
    """Global, project, or repository permission. Global permissions are: LICENSED_USER, PROJECT_CREATE, ADMIN. SYS_ADMIN. Project permissions are: PROJECT_READ, PROJECT_WRITE, REPO_CREATE, PROJECT_ADMIN. Repository permissions are: REPO_READ, REPO_WRITE, REPO_ADMIN. For addAccessToken, this parameter can be a comma separated list of a project permission and a repository permission. Note, REPO_CREATE requires Bitbucket 8.2 or higher."""
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
class GetProjectList(BitbucketCommand):
    """Get a list of projects based on the selection criteria. Option to restrict to projects with a specific permission. Regex matching on project key or name."""
    options: GetProjectListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getProjectList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getProjectList

# Variants for getProjectPermissionList
@dataclass
class GetProjectPermissionListOptions:
    """Optional parameters for action getProjectPermissionList"""
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
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetProjectPermissionList(BitbucketCommand):
    """List permissions for a project."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    options: GetProjectPermissionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getProjectPermissionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getProjectPermissionList

# Variants for getPullRequest
@dataclass
class GetPullRequestOptions:
    """Optional parameters for action getPullRequest"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetPullRequest(BitbucketCommand):
    """Get pull request information."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    pull_request: str
    """Pull request id or name."""
    options: GetPullRequestOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPullRequest"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPullRequest

# Variants for getPullRequestList
@dataclass
class GetPullRequestListOptions:
    """Optional parameters for action getPullRequestList"""
    direction: str|None = None
    """Pull request list state. Valid directions are: INCOMING, OUTGOING."""
    state: str|None = None
    """Build status state or pull request list state. Build states are: SUCCESSFUL, FAILED, INPROGRESS. Pull request states are: OPEN, DECLINED, MERGED."""
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
class GetPullRequestList(BitbucketCommand):
    """List pull requests for a repository with regex filtering on name. Also, filtering by direction and state."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    options: GetPullRequestListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPullRequestList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPullRequestList

# Variants for getRepository
@dataclass
class GetRepositoryOptions:
    """Optional parameters for action getRepository"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetRepository(BitbucketCommand):
    """Get repository information."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    options: GetRepositoryOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getRepository"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getRepository

# Variants for getRepositoryList
@dataclass
class GetRepositoryListOptions:
    """Optional parameters for action getRepositoryList"""
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
class GetRepositoryList(BitbucketCommand):
    """Get a list of repositories with regex filtering on repository name and slug."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    options: GetRepositoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getRepositoryList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getRepositoryList

# Variants for getRepositoryPermissionList
@dataclass
class GetRepositoryPermissionListOptions:
    """Optional parameters for action getRepositoryPermissionList"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
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
class GetRepositoryPermissionList(BitbucketCommand):
    """List permissions for a repository."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    options: GetRepositoryPermissionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getRepositoryPermissionList"

# End Variants for getRepositoryPermissionList

# Variants for getReviewConditionList
@dataclass
class GetReviewConditionListOptions:
    """Optional parameters for action getReviewConditionList"""
    repository: str|None = None
    """Repository slug, name, or id."""
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
class GetReviewConditionList(BitbucketCommand):
    """List review conditions for a project or repository with regex filtering on from or to matching value."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    options: GetReviewConditionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getReviewConditionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getReviewConditionList

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
class GetServerInfo(BitbucketCommand):
    """Get information about the Bitbucket server."""
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

# Variants for getSource
@dataclass
class GetSourceOptions:
    """Optional parameters for action getSource"""
    revision: str|None = None
    """Repository revision id like a commit id, branch, tag, or special value like HEAD (for Git) and tip for Mercurial."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetSource(BitbucketCommand):
    """Get file data from a repository path at a default or specific revision. Normally for source text, but binary data can also be retrieved to a file."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    path: str
    """Source path."""
    options: GetSourceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSource"

# End Variants for getSource

# Variants for getSshKeyList
@dataclass
class GetSshKeyListOptions:
    """Optional parameters for action getSshKeyList"""
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
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetSshKeyList(BitbucketCommand):
    """List of SSH keys associated a user."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    options: GetSshKeyListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSshKeyList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getSshKeyList

# Variants for getUser
@dataclass
class GetUserOptions:
    """Optional parameters for action getUser"""
    user_id: str|None = None
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    reference: str|None = None
    """Reference to a replacement key value used to remember an action specific value like issue key, entity id, or similar so it can be referenced later. Each action that allows this parameter will specify that the reference parameter is valid for the action and the first entry listed for available replacement variables help text will be the value set. If you need access to a different replacement variable in your script, you will need to use the setReplacementVariables action after the action to set a new replacement variable of your choosing to one of the other available replacement variables."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetUser(BitbucketCommand):
    """Get user information for the current user or the user identified by the userId parameter if provided."""
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
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
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
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetUserList(BitbucketCommand):
    """List users or users in a group."""
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
class GetWebhookList(BitbucketCommand):
    """List user defined webhooks with regex filtering on webhook name. For Post Webhooks for Bitbucket users, use '--options postWebhooks'."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
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

# Variants for grantPermissions

@dataclass
class GrantPermissionsGivenPermissionAndUserId(BitbucketCommand):
    """Grant global permissions for one or more users or groups. Set permission parameter to one of the valid permissions. Valid permissions are LICENSED_USER, PROJECT_CREATE, ADMIN, and SYS_ADMIN listed in order of least permission to most permission."""
    permission: str
    """Global, project, or repository permission. Global permissions are: LICENSED_USER, PROJECT_CREATE, ADMIN. SYS_ADMIN. Project permissions are: PROJECT_READ, PROJECT_WRITE, REPO_CREATE, PROJECT_ADMIN. Repository permissions are: REPO_READ, REPO_WRITE, REPO_ADMIN. For addAccessToken, this parameter can be a comma separated list of a project permission and a repository permission. Note, REPO_CREATE requires Bitbucket 8.2 or higher."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "grantPermissions"

@dataclass
class GrantPermissionsGivenPermissionAndGroup(BitbucketCommand):
    """Grant global permissions for one or more users or groups. Set permission parameter to one of the valid permissions. Valid permissions are LICENSED_USER, PROJECT_CREATE, ADMIN, and SYS_ADMIN listed in order of least permission to most permission."""
    permission: str
    """Global, project, or repository permission. Global permissions are: LICENSED_USER, PROJECT_CREATE, ADMIN. SYS_ADMIN. Project permissions are: PROJECT_READ, PROJECT_WRITE, REPO_CREATE, PROJECT_ADMIN. Repository permissions are: REPO_READ, REPO_WRITE, REPO_ADMIN. For addAccessToken, this parameter can be a comma separated list of a project permission and a repository permission. Note, REPO_CREATE requires Bitbucket 8.2 or higher."""
    group: str
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "grantPermissions"

# End Variants for grantPermissions

# Variants for grantProjectPermissions
@dataclass
class GrantProjectPermissionsOptions:
    """Optional parameters for action grantProjectPermissions"""
    user_id: str|None = None
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    group: str|None = None
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""

@dataclass
class GrantProjectPermissions(BitbucketCommand):
    """Grant project level permissions for one or more users or groups using either the userId or group parameters. Set permission parameter to one of the valid permissions. Valid permissions are PROJECT_READ, PROJECT_WRITE, REPO_CREATE, and PROJECT_ADMIN listed in order of least permission to most permission. Alternatively, the project level default permission (only REPO_CREATE, PROJECT_WRITE, or PROJECT_READ) can be set. Note, REPO_CREATE requires Bitbucket 8.2 or higher."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    permission: str
    """Global, project, or repository permission. Global permissions are: LICENSED_USER, PROJECT_CREATE, ADMIN. SYS_ADMIN. Project permissions are: PROJECT_READ, PROJECT_WRITE, REPO_CREATE, PROJECT_ADMIN. Repository permissions are: REPO_READ, REPO_WRITE, REPO_ADMIN. For addAccessToken, this parameter can be a comma separated list of a project permission and a repository permission. Note, REPO_CREATE requires Bitbucket 8.2 or higher."""
    options: GrantProjectPermissionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "grantProjectPermissions"

# End Variants for grantProjectPermissions

# Variants for grantRepositoryPermissions

@dataclass
class GrantRepositoryPermissionsGivenProjectAndRepositoryAndPermissionAndUserId(BitbucketCommand):
    """Grant repository level permissions for one or more users or groups using either the userId or group parameters. Set permission parameter to one of the valid permissions. Valid permissions are REPO_READ, REPO_WRITE, or REPO_ADMIN listed in order of least permission to most permission."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    permission: str
    """Global, project, or repository permission. Global permissions are: LICENSED_USER, PROJECT_CREATE, ADMIN. SYS_ADMIN. Project permissions are: PROJECT_READ, PROJECT_WRITE, REPO_CREATE, PROJECT_ADMIN. Repository permissions are: REPO_READ, REPO_WRITE, REPO_ADMIN. For addAccessToken, this parameter can be a comma separated list of a project permission and a repository permission. Note, REPO_CREATE requires Bitbucket 8.2 or higher."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "grantRepositoryPermissions"

@dataclass
class GrantRepositoryPermissionsGivenProjectAndRepositoryAndPermissionAndGroup(BitbucketCommand):
    """Grant repository level permissions for one or more users or groups using either the userId or group parameters. Set permission parameter to one of the valid permissions. Valid permissions are REPO_READ, REPO_WRITE, or REPO_ADMIN listed in order of least permission to most permission."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    permission: str
    """Global, project, or repository permission. Global permissions are: LICENSED_USER, PROJECT_CREATE, ADMIN. SYS_ADMIN. Project permissions are: PROJECT_READ, PROJECT_WRITE, REPO_CREATE, PROJECT_ADMIN. Repository permissions are: REPO_READ, REPO_WRITE, REPO_ADMIN. For addAccessToken, this parameter can be a comma separated list of a project permission and a repository permission. Note, REPO_CREATE requires Bitbucket 8.2 or higher."""
    group: str
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "grantRepositoryPermissions"

# End Variants for grantRepositoryPermissions

# Variants for installApp
@dataclass
class InstallAppOptions:
    """Optional parameters for action installApp"""
    version: str|None = None
    """App version."""

@dataclass
class InstallAppGivenApp(BitbucketCommand):
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
class InstallAppGivenUrl(BitbucketCommand):
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
class InstallAppGivenFile(BitbucketCommand):
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

# Variants for mergePullRequest

@dataclass
class MergePullRequest(BitbucketCommand):
    """Merge a pull request."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    pull_request: str
    """Pull request id or name."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "mergePullRequest"

# End Variants for mergePullRequest

# Variants for removeAccessToken
@dataclass
class RemoveAccessTokenOptions:
    """Optional parameters for action removeAccessToken"""
    user: str|None = None
    """User name for remote access."""

@dataclass
class RemoveAccessToken(BitbucketCommand):
    """Remove an access token for a user by name or id. Defaults to current user. If there are multiple tokens with the same name, only the first one will be removed."""
    name: str
    """Name of an item or entity."""
    options: RemoveAccessTokenOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAccessToken"

# End Variants for removeAccessToken

# Variants for removeApplicationLink
@dataclass
class RemoveApplicationLinkOptions:
    """Optional parameters for action removeApplicationLink"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveApplicationLinkGivenName(BitbucketCommand):
    """Remove an application link identified by name or url."""
    name: str
    """Name of an item or entity."""
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
class RemoveApplicationLinkGivenUrl(BitbucketCommand):
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

# Variants for removeBranch
@dataclass
class RemoveBranchOptions:
    """Optional parameters for action removeBranch"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveBranch(BitbucketCommand):
    """Deprecated. Remove a repository branch."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    branch: str
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
    options: RemoveBranchOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeBranch"

# End Variants for removeBranch

# Variants for removeBranchRestriction
@dataclass
class RemoveBranchRestrictionOptions:
    """Optional parameters for action removeBranchRestriction"""
    matching_type: str|None = None
    """Branch matching type. Defaults to BRANCH. Types are: BRANCH, MODEL, PATTERN"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveBranchRestrictionGivenProjectAndRepositoryAndId(BitbucketCommand):
    """Remove branch level restriction by id or lookup based on restriction, branch, and matchingType. If id is provided, other parameters are ignored. Use @all for restriction to remove all restrictions matching branch with the specified matching type. Use continue to ignore not found errors."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    options: RemoveBranchRestrictionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeBranchRestriction"

@dataclass
class RemoveBranchRestrictionGivenProjectAndRepositoryAndRestriction(BitbucketCommand):
    """Remove branch level restriction by id or lookup based on restriction, branch, and matchingType. If id is provided, other parameters are ignored. Use @all for restriction to remove all restrictions matching branch with the specified matching type. Use continue to ignore not found errors."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    restriction: str
    """Branch restriction. Defaults to read-only. Restrictions are: read-only, no-deletes, fast-forward-only, pull-request-only."""
    options: RemoveBranchRestrictionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeBranchRestriction"

@dataclass
class RemoveBranchRestrictionGivenProjectAndRepositoryAndBranch(BitbucketCommand):
    """Remove branch level restriction by id or lookup based on restriction, branch, and matchingType. If id is provided, other parameters are ignored. Use @all for restriction to remove all restrictions matching branch with the specified matching type. Use continue to ignore not found errors."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    branch: str
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
    options: RemoveBranchRestrictionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeBranchRestriction"

# End Variants for removeBranchRestriction

# Variants for removeGroup
@dataclass
class RemoveGroupOptions:
    """Optional parameters for action removeGroup"""
    default_group: str|None = None
    """Default group to move users on removeGroup action."""

@dataclass
class RemoveGroup(BitbucketCommand):
    """Remove a group."""
    group: str
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
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

# Variants for removeLicense

@dataclass
class RemoveLicense(BitbucketCommand):
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

# Variants for removeReviewCondition
@dataclass
class RemoveReviewConditionOptions:
    """Optional parameters for action removeReviewCondition"""
    repository: str|None = None
    """Repository slug, name, or id."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveReviewCondition(BitbucketCommand):
    """Remove review condition from a project or repository."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    options: RemoveReviewConditionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeReviewCondition"

# End Variants for removeReviewCondition

# Variants for removeSshKey

@dataclass
class RemoveSshKey(BitbucketCommand):
    """Remove a specific SSH key by its id or label."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeSshKey"

# End Variants for removeSshKey

# Variants for removeSshKeys

@dataclass
class RemoveSshKeys(BitbucketCommand):
    """Remove all SSH keys for a user."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeSshKeys"

# End Variants for removeSshKeys

# Variants for removeUser

@dataclass
class RemoveUser(BitbucketCommand):
    """Remove a user."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
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
class RemoveUserFromGroup(BitbucketCommand):
    """Remove user from a group."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    group: str
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeUserFromGroup"

# End Variants for removeUserFromGroup

# Variants for removeWebhook

@dataclass
class RemoveWebhookGivenProjectAndRepositoryAndName(BitbucketCommand):
    """Remove a user defined webhook. For Post Webhooks for Bitbucket users, use '--options postWebhooks'."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    name: str
    """Name of an item or entity."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeWebhook"

@dataclass
class RemoveWebhookGivenProjectAndRepositoryAndId(BitbucketCommand):
    """Remove a user defined webhook. For Post Webhooks for Bitbucket users, use '--options postWebhooks'."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeWebhook"

# End Variants for removeWebhook

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
class RenderRequest(BitbucketCommand):
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

# Variants for revokePermissions
@dataclass
class RevokePermissionsOptions:
    """Optional parameters for action revokePermissions"""
    user_id: str|None = None
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    group: str|None = None
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""

@dataclass
class RevokePermissions(BitbucketCommand):
    """Revoke all project level permissions for one or more users or groups using either the userId or group parameters. Alternatively, the project level default permission can be revoked."""
    options: RevokePermissionsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "revokePermissions"

# End Variants for revokePermissions

# Variants for revokeProjectPermissions

@dataclass
class RevokeProjectPermissionsGivenProjectAndUserId(BitbucketCommand):
    """Revoke project level permissions for one or more users or groups."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "revokeProjectPermissions"

@dataclass
class RevokeProjectPermissionsGivenProjectAndGroup(BitbucketCommand):
    """Revoke project level permissions for one or more users or groups."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    group: str
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "revokeProjectPermissions"

# End Variants for revokeProjectPermissions

# Variants for revokeRepositoryPermissions

@dataclass
class RevokeRepositoryPermissionsGivenProjectAndRepositoryAndUserId(BitbucketCommand):
    """Revoke repository level permissions for one or more users or groups."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "revokeRepositoryPermissions"

@dataclass
class RevokeRepositoryPermissionsGivenProjectAndRepositoryAndGroup(BitbucketCommand):
    """Revoke repository level permissions for one or more users or groups."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    group: str
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "revokeRepositoryPermissions"

# End Variants for revokeRepositoryPermissions

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
class RunFromAppListGivenInput(BitbucketCommand):
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
class RunFromAppListGivenCommon(BitbucketCommand):
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
class RunFromAppListGivenFile(BitbucketCommand):
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
    """Application link type."""
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
class RunFromApplicationLinkListGivenInput(BitbucketCommand):
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
class RunFromApplicationLinkListGivenCommon(BitbucketCommand):
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
class RunFromApplicationLinkListGivenFile(BitbucketCommand):
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

# Variants for runFromBranchList
@dataclass
class RunFromBranchListOptions:
    """Optional parameters for action runFromBranchList"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    order: str|None = None
    """Order returned. Branch ordering values: ALPHABETICAL, MODIFICATION"""
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
class RunFromBranchListGivenProjectAndRepositoryAndInput(BitbucketCommand):
    """Run actions for branches for a repository with regex filtering on key or name."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromBranchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBranchList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBranchListGivenProjectAndRepositoryAndCommon(BitbucketCommand):
    """Run actions for branches for a repository with regex filtering on key or name."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromBranchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBranchList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBranchListGivenProjectAndRepositoryAndFile(BitbucketCommand):
    """Run actions for branches for a repository with regex filtering on key or name."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromBranchListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBranchList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromBranchList

# Variants for runFromBranchRestrictionList
@dataclass
class RunFromBranchRestrictionListOptions:
    """Optional parameters for action runFromBranchRestrictionList"""
    restriction: str|None = None
    """Branch restriction. Defaults to read-only. Restrictions are: read-only, no-deletes, fast-forward-only, pull-request-only."""
    matching_type: str|None = None
    """Branch matching type. Defaults to BRANCH. Types are: BRANCH, MODEL, PATTERN"""
    branch: str|None = None
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
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
class RunFromBranchRestrictionListGivenProjectAndRepositoryAndInput(BitbucketCommand):
    """Run actions for each branch restriction with filtering options like for getBranchRestrictionList."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromBranchRestrictionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBranchRestrictionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBranchRestrictionListGivenProjectAndRepositoryAndCommon(BitbucketCommand):
    """Run actions for each branch restriction with filtering options like for getBranchRestrictionList."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromBranchRestrictionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBranchRestrictionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromBranchRestrictionListGivenProjectAndRepositoryAndFile(BitbucketCommand):
    """Run actions for each branch restriction with filtering options like for getBranchRestrictionList."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromBranchRestrictionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromBranchRestrictionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromBranchRestrictionList

# Variants for runFromCommitList
@dataclass
class RunFromCommitListOptions:
    """Optional parameters for action runFromCommitList"""
    from_: str|None = None
    """Also known as a source reference. For repository pull request, a from branch reference. For commit list, a commit or reference to retrieve commits after (exclusive)."""
    to: str|None = None
    """Also known as a target reference. For repository pull request, a to branch reference. For commit list, a commit or reference to retrieve commits before (inclusive)."""
    user_id: str|None = None
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is to get the most recent entries."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
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
class RunFromCommitListGivenProjectAndRepositoryAndInput(BitbucketCommand):
    """Run actions for each commit for a repository with regex filtering like on getCommitList."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromCommitListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromCommitList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromCommitListGivenProjectAndRepositoryAndCommon(BitbucketCommand):
    """Run actions for each commit for a repository with regex filtering like on getCommitList."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromCommitListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromCommitList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromCommitListGivenProjectAndRepositoryAndFile(BitbucketCommand):
    """Run actions for each commit for a repository with regex filtering like on getCommitList."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromCommitListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromCommitList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromCommitList

# Variants for runFromGroupList
@dataclass
class RunFromGroupListOptions:
    """Optional parameters for action runFromGroupList"""
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
class RunFromGroupListGivenInput(BitbucketCommand):
    """Run actions for each group with regex filtering just like getGroupList."""
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
class RunFromGroupListGivenCommon(BitbucketCommand):
    """Run actions for each group with regex filtering just like getGroupList."""
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
class RunFromGroupListGivenFile(BitbucketCommand):
    """Run actions for each group with regex filtering just like getGroupList."""
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

# Variants for runFromHookList
@dataclass
class RunFromHookListOptions:
    """Optional parameters for action runFromHookList"""
    repository: str|None = None
    """Repository slug, name, or id."""
    enabled: bool|None = None
    """Subset to include enabled hooks in list of hooks."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
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
class RunFromHookListGivenProjectAndInput(BitbucketCommand):
    """Run actions for hooks available for a project or repository with regex filtering on key and name. Use the enabled parameter to list only enabled hooks. Use outputFormat 2 or higher to get the hookConfiguration replacement variable."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromHookListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromHookList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromHookListGivenProjectAndCommon(BitbucketCommand):
    """Run actions for hooks available for a project or repository with regex filtering on key and name. Use the enabled parameter to list only enabled hooks. Use outputFormat 2 or higher to get the hookConfiguration replacement variable."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromHookListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromHookList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromHookListGivenProjectAndFile(BitbucketCommand):
    """Run actions for hooks available for a project or repository with regex filtering on key and name. Use the enabled parameter to list only enabled hooks. Use outputFormat 2 or higher to get the hookConfiguration replacement variable."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromHookListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromHookList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromHookList

# Variants for runFromProjectList
@dataclass
class RunFromProjectListOptions:
    """Optional parameters for action runFromProjectList"""
    permission: str|None = None
    """Global, project, or repository permission. Global permissions are: LICENSED_USER, PROJECT_CREATE, ADMIN. SYS_ADMIN. Project permissions are: PROJECT_READ, PROJECT_WRITE, REPO_CREATE, PROJECT_ADMIN. Repository permissions are: REPO_READ, REPO_WRITE, REPO_ADMIN. For addAccessToken, this parameter can be a comma separated list of a project permission and a repository permission. Note, REPO_CREATE requires Bitbucket 8.2 or higher."""
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
class RunFromProjectListGivenInput(BitbucketCommand):
    """Run actions for projects with regex filtering on project key or name. Option to restrict to projects with a specific permission."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromProjectListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromProjectList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromProjectListGivenCommon(BitbucketCommand):
    """Run actions for projects with regex filtering on project key or name. Option to restrict to projects with a specific permission."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromProjectListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromProjectList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromProjectListGivenFile(BitbucketCommand):
    """Run actions for projects with regex filtering on project key or name. Option to restrict to projects with a specific permission."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromProjectListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromProjectList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromProjectList

# Variants for runFromPullRequestList
@dataclass
class RunFromPullRequestListOptions:
    """Optional parameters for action runFromPullRequestList"""
    direction: str|None = None
    """Pull request list state. Valid directions are: INCOMING, OUTGOING."""
    state: str|None = None
    """Build status state or pull request list state. Build states are: SUCCESSFUL, FAILED, INPROGRESS. Pull request states are: OPEN, DECLINED, MERGED."""
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
class RunFromPullRequestListGivenProjectAndRepositoryAndInput(BitbucketCommand):
    """Run actions for pull requests for a repository with regex filtering on name. Also, filtering by direction and state."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromPullRequestListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPullRequestList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPullRequestListGivenProjectAndRepositoryAndCommon(BitbucketCommand):
    """Run actions for pull requests for a repository with regex filtering on name. Also, filtering by direction and state."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromPullRequestListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPullRequestList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPullRequestListGivenProjectAndRepositoryAndFile(BitbucketCommand):
    """Run actions for pull requests for a repository with regex filtering on name. Also, filtering by direction and state."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromPullRequestListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPullRequestList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromPullRequestList

# Variants for runFromRepositoryList
@dataclass
class RunFromRepositoryListOptions:
    """Optional parameters for action runFromRepositoryList"""
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
class RunFromRepositoryListGivenProjectAndInput(BitbucketCommand):
    """Run actions for repositories in a project with regex filtering on name."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromRepositoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromRepositoryList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromRepositoryListGivenProjectAndCommon(BitbucketCommand):
    """Run actions for repositories in a project with regex filtering on name."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromRepositoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromRepositoryList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromRepositoryListGivenProjectAndFile(BitbucketCommand):
    """Run actions for repositories in a project with regex filtering on name."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromRepositoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromRepositoryList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromRepositoryList

# Variants for runFromReviewConditionList
@dataclass
class RunFromReviewConditionListOptions:
    """Optional parameters for action runFromReviewConditionList"""
    repository: str|None = None
    """Repository slug, name, or id."""
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
class RunFromReviewConditionListGivenProjectAndInput(BitbucketCommand):
    """Run actions for each review condition for a project or a repository."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromReviewConditionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromReviewConditionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromReviewConditionListGivenProjectAndCommon(BitbucketCommand):
    """Run actions for each review condition for a project or a repository."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromReviewConditionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromReviewConditionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromReviewConditionListGivenProjectAndFile(BitbucketCommand):
    """Run actions for each review condition for a project or a repository."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromReviewConditionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromReviewConditionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromReviewConditionList

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
class RunFromUserListGivenInput(BitbucketCommand):
    """Run action for each user with similar filtering as getUserList."""
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
class RunFromUserListGivenCommon(BitbucketCommand):
    """Run action for each user with similar filtering as getUserList."""
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
class RunFromUserListGivenFile(BitbucketCommand):
    """Run action for each user with similar filtering as getUserList."""
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
class RunFromWebhookListGivenProjectAndRepositoryAndInput(BitbucketCommand):
    """Run action for each webhook with regex filtering on webhook name. For Post Webhooks for Bitbucket users, use '--options postWebhooks'."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
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
class RunFromWebhookListGivenProjectAndRepositoryAndCommon(BitbucketCommand):
    """Run action for each webhook with regex filtering on webhook name. For Post Webhooks for Bitbucket users, use '--options postWebhooks'."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
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
class RunFromWebhookListGivenProjectAndRepositoryAndFile(BitbucketCommand):
    """Run action for each webhook with regex filtering on webhook name. For Post Webhooks for Bitbucket users, use '--options postWebhooks'."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
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

# Variants for setBuildStatus
@dataclass
class SetBuildStatusOptions:
    """Optional parameters for action setBuildStatus"""
    name: str|None = None
    """Name of an item or entity."""
    description: str|None = None
    """Description."""

@dataclass
class SetBuildStatus(BitbucketCommand):
    """Set the build status for a changeset id and key."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    key: str
    """Build key used for setting build status."""
    state: str
    """Build status state or pull request list state. Build states are: SUCCESSFUL, FAILED, INPROGRESS. Pull request states are: OPEN, DECLINED, MERGED."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: SetBuildStatusOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "setBuildStatus"

# End Variants for setBuildStatus

# Variants for uninstallApp
@dataclass
class UninstallAppOptions:
    """Optional parameters for action uninstallApp"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class UninstallApp(BitbucketCommand):
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

# Variants for updateBranchRestriction
@dataclass
class UpdateBranchRestrictionOptions:
    """Optional parameters for action updateBranchRestriction"""
    restriction: str|None = None
    """Branch restriction. Defaults to read-only. Restrictions are: read-only, no-deletes, fast-forward-only, pull-request-only."""
    matching_type: str|None = None
    """Branch matching type. Defaults to BRANCH. Types are: BRANCH, MODEL, PATTERN"""
    user_id: str|None = None
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
    group: str|None = None
    """Group name for user management and related actions. For some actions, a comma separated list of group names."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""

@dataclass
class UpdateBranchRestrictionGivenProjectAndRepositoryAndBranch(BitbucketCommand):
    """Update a branch level restriction with changes to exemptions for users and groups. Identify the branch restriction by id or by the same matching parameters as getBranchRestriction. By default, users or group or both specified by their respective parameters will be added to the existing exceptions. Use '--options remove' to remove users or group or both specified by their respective parameters. Use '--replace' to replace users or groups or both specified by their respective parameters. Use a blank parameter value to indicate no corresponding exceptions for remove and replace."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    branch: str
    """Branch id or name. For a branch permissions, it can represent a branch, branch pattern, or branching model."""
    options: UpdateBranchRestrictionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateBranchRestriction"

@dataclass
class UpdateBranchRestrictionGivenProjectAndRepositoryAndId(BitbucketCommand):
    """Update a branch level restriction with changes to exemptions for users and groups. Identify the branch restriction by id or by the same matching parameters as getBranchRestriction. By default, users or group or both specified by their respective parameters will be added to the existing exceptions. Use '--options remove' to remove users or group or both specified by their respective parameters. Use '--replace' to replace users or groups or both specified by their respective parameters. Use a blank parameter value to indicate no corresponding exceptions for remove and replace."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    options: UpdateBranchRestrictionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateBranchRestriction"

# End Variants for updateBranchRestriction

# Variants for updateHook
@dataclass
class UpdateHookOptions:
    """Optional parameters for action updateHook"""
    repository: str|None = None
    """Repository slug, name, or id."""

@dataclass
class UpdateHook(BitbucketCommand):
    """Update hook configuration by hook name or key for a project or repository scoped hook. Configuration must be represented as a JSON specific to the hook. Use getHookList to view existing configurations."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    hook: str
    """Hook name or key of the form 'plugin key:hook key'."""
    config: str
    """Hook configuration in JSON format."""
    options: UpdateHookOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateHook"

# End Variants for updateHook

# Variants for updateProject
@dataclass
class UpdateProjectOptions:
    """Optional parameters for action updateProject"""
    name: str|None = None
    """Name of an item or entity."""
    description: str|None = None
    """Description."""
    public: bool|None = None
    """Allow the project to be visible to the public (users without a Bitbucket account)."""
    private: bool|None = None
    """Allow the project to be visible only to users with permission. Default for new projects."""

@dataclass
class UpdateProject(BitbucketCommand):
    """Update a project."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    options: UpdateProjectOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateProject"

# End Variants for updateProject

# Variants for updatePullRequest
@dataclass
class UpdatePullRequestOptions:
    """Optional parameters for action updatePullRequest"""
    name: str|None = None
    """Name of an item or entity."""
    description: str|None = None
    """Description."""
    reviewers: str|None = None
    """Pull request reviewers. Comma separated list of user ids."""

@dataclass
class UpdatePullRequest(BitbucketCommand):
    """Update pull request information."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    pull_request: str
    """Pull request id or name."""
    options: UpdatePullRequestOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updatePullRequest"

# End Variants for updatePullRequest

# Variants for updateRepository
@dataclass
class UpdateRepositoryOptions:
    """Optional parameters for action updateRepository"""
    name: str|None = None
    """Name of an item or entity."""
    public: bool|None = None
    """Allow the project to be visible to the public (users without a Bitbucket account)."""
    private: bool|None = None
    """Allow the project to be visible only to users with permission. Default for new projects."""
    forkable: bool|None = None
    """Allow a repository to be forkable."""
    not_forkable: bool|None = None
    """Disallow a repository from being forkable. Default for new repositories."""

@dataclass
class UpdateRepository(BitbucketCommand):
    """Update repository information."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    options: UpdateRepositoryOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateRepository"

# End Variants for updateRepository

# Variants for updateReviewCondition
@dataclass
class UpdateReviewConditionOptions:
    """Optional parameters for action updateReviewCondition"""
    repository: str|None = None
    """Repository slug, name, or id."""
    review_approval_count: str|None = None
    """Number of reviewers on the reviewer list that are required to approve the pull request before it can be merged. The number must be less than or equal to the number of default reviewers provided."""

@dataclass
class UpdateReviewCondition(BitbucketCommand):
    """Update a review condition for a project or repository. Reviewers and reviewApprovalCount are the only values that can be updated."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
    reviewers: str
    """Pull request reviewers. Comma separated list of user ids."""
    options: UpdateReviewConditionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateReviewCondition"

# End Variants for updateReviewCondition

# Variants for updateUser
@dataclass
class UpdateUserOptions:
    """Optional parameters for action updateUser"""
    user_full_name: str|None = None
    """User name for user management actions."""
    user_email: str|None = None
    """User email for user management actions."""

@dataclass
class UpdateUser(BitbucketCommand):
    """Update user information."""
    user_id: str
    """User id for user management and related actions. For some actions, a comma separated list of user ids."""
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
    """Comma separated list of webhook events. Valid events may vary by Bitbucket version, hosting type, or other factors. Consult Atlassian documentation for latest details. Some known events are: repo:refs_changed, repo:forked, repo:comment:added, repo:comment:edited, repo:comment:deleted, mirror:repo_synchronized, pr:opened, pr:from_ref_updated, pr:modified, pr:reviewer:updated, pr:reviewer:approved, pr:reviewer:unapproved, pr:reviewer:needs_work, pr:merged, pr:declined, pr:deleted, pr:comment:added, pr:comment:edited, pr:comment:deleted"""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""

@dataclass
class UpdateWebhookGivenProjectAndRepositoryAndId(BitbucketCommand):
    """Update an existing user defined webhook. Use '--options enable' or '--options disable' to change the status of the webhook. Use --options "secret=..." to change the data integrity verification string. For Post Webhooks for Bitbucket users, use '--options postWebhooks'."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    id: str
    """Commit id, changeset id, branch restriction identifier, SSH key numeric or label identifier."""
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
class UpdateWebhookGivenProjectAndRepositoryAndName(BitbucketCommand):
    """Update an existing user defined webhook. Use '--options enable' or '--options disable' to change the status of the webhook. Use --options "secret=..." to change the data integrity verification string. For Post Webhooks for Bitbucket users, use '--options postWebhooks'."""
    project: str
    """Project key, name, or id. Project keys and names must be less than 64 characters long."""
    repository: str
    """Repository slug, name, or id."""
    name: str
    """Name of an item or entity."""
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
class ValidateLicense(BitbucketCommand):
    """Validates the ACLI Connector is enabled and licensed on the server."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "validateLicense"

# End Variants for validateLicense
