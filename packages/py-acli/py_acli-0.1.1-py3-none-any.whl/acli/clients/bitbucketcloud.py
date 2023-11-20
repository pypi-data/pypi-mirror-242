from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class BitbucketCloudCommand(Command):
    pass

@dataclass
class BitbucketCloudClient(RemoteClient):
    def execute(self, command: BitbucketCloudCommand):
        return super().do_execute(command)

# Variants for addDownload
@dataclass
class AddDownloadOptions:
    """Optional parameters for action addDownload"""
    workspace: str|None = None
    """Workspace"""
    name: str|None = None
    """Name of an item or entity."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class AddDownload(BitbucketCloudCommand):
    """Add a download file to a repository."""
    repository: str
    """Repository name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddDownloadOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addDownload"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addDownload

# Variants for addEnvironment
@dataclass
class AddEnvironmentOptions:
    """Optional parameters for action addEnvironment"""
    workspace: str|None = None
    """Workspace"""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class AddEnvironment(BitbucketCloudCommand):
    """Add deployment environment. Type must be one of Test, Staging, or Production. Premium plan users can use '--options adminOnly' to restrict who can deploy to this environment."""
    repository: str
    """Repository name."""
    environment: str
    """Deployment environment name or UUID."""
    type: str
    """Deployment environment type."""
    options: AddEnvironmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addEnvironment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addEnvironment

# Variants for addRunner
@dataclass
class AddRunnerOptions:
    """Optional parameters for action addRunner"""
    label: Iterable[str]|str|None = None
    """Use to set workspace or repository runner labels."""

@dataclass
class AddRunnerGivenWorkspaceAndName(BitbucketCloudCommand):
    """Add a pipeline runner to a workspace or repository. Exactly one platform label (linux, linux.shell, windows, macos) can be specified. Defaults to linux if none is provided. Also, self.hosted is added if not provided as required by Bitbucket."""
    workspace: str
    """Workspace"""
    name: str
    """Name of an item or entity."""
    options: AddRunnerOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addRunner"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddRunnerGivenRepositoryAndName(BitbucketCloudCommand):
    """Add a pipeline runner to a workspace or repository. Exactly one platform label (linux, linux.shell, windows, macos) can be specified. Defaults to linux if none is provided. Also, self.hosted is added if not provided as required by Bitbucket."""
    repository: str
    """Repository name."""
    name: str
    """Name of an item or entity."""
    options: AddRunnerOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addRunner"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addRunner

# Variants for addVariables
@dataclass
class AddVariablesOptions:
    """Optional parameters for action addVariables"""
    environment: str|None = None
    """Deployment environment name or UUID."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    property_file: str|None = None
    """Property file with database parameters, field mappings, or client specific information."""
    secured: bool|None = None
    """When adding and updating variables, this option will mark variables as secured so they are hidden from viewing."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""

@dataclass
class AddVariablesGivenWorkspace(BitbucketCloudCommand):
    """Add workspace, repository, or deployment environment variables. Use one or more field parameters where each field parameter is a key=value pair. Specify a secured variable by appending ':secured' like key=value:secured. To secure all variables added, use the secured parameter. Variables can also be added from a property file using the propertyFile parameter."""
    workspace: str
    """Workspace"""
    options: AddVariablesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addVariables"

@dataclass
class AddVariablesGivenRepository(BitbucketCloudCommand):
    """Add workspace, repository, or deployment environment variables. Use one or more field parameters where each field parameter is a key=value pair. Specify a secured variable by appending ':secured' like key=value:secured. To secure all variables added, use the secured parameter. Variables can also be added from a property file using the propertyFile parameter."""
    repository: str
    """Repository name."""
    options: AddVariablesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addVariables"

# End Variants for addVariables

# Variants for approveCommit
@dataclass
class ApproveCommitOptions:
    """Optional parameters for action approveCommit"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class ApproveCommit(BitbucketCloudCommand):
    """Approve a Commit."""
    repository: str
    """Repository name."""
    commit: str
    """Commit id. In many cases, you can also use a tag name."""
    options: ApproveCommitOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "approveCommit"

# End Variants for approveCommit

# Variants for approvePullRequest
@dataclass
class ApprovePullRequestOptions:
    """Optional parameters for action approvePullRequest"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class ApprovePullRequest(BitbucketCloudCommand):
    """Approve a pull request."""
    repository: str
    """Repository name."""
    pull_request: str
    """Plug request id."""
    options: ApprovePullRequestOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "approvePullRequest"

# End Variants for approvePullRequest

# Variants for createBranch
@dataclass
class CreateBranchOptions:
    """Optional parameters for action createBranch"""
    workspace: str|None = None
    """Workspace"""
    type: str|None = None
    """Deployment environment type."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class CreateBranch(BitbucketCloudCommand):
    """Create repository branch. Use from parameter to specify the source branch that this branch will be created from. Use type parameter to specify branch types, like Feature, Bugfix, Release etc. The final branch name will be combination of type and branch name with a slash. Use continue parameter to ignore when branch already exists."""
    repository: str
    """Repository name."""
    branch: str
    """Branch name."""
    from_: str
    """Also known as a source reference. For repository pull request, a from branch reference. For commit list, a commit or reference to retrieve commits after (exclusive)."""
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

# Variants for createCommit
@dataclass
class CreateCommitOptions:
    """Optional parameters for action createCommit"""
    workspace: str|None = None
    """Workspace"""
    name: str|None = None
    """Name of an item or entity."""
    user_id: str|None = None
    """User id user related actions. Must be a Atlassian Cloud account id or user UUID."""
    parent: str|None = None
    """Confluence page title for a parent page."""
    path: str|None = None
    """Source path."""
    data: str|None = None
    """JSON data for runFromJson. Post data for renderRequest. Action specific definition in some cases."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    branch: str|None = None
    """Branch name."""

@dataclass
class CreateCommit(BitbucketCloudCommand):
    """Create repository commit. Use parameter name for the commit message. If name is not provided, a system generated name will be used. Use parameter branch to specify the target branch of this commit. User required parameter path to specify the path of the repository file to be changed. Use parameter data or parameter file to provide new contents of the file. If parameter data and parameter file are not specified, the path specified repository file will be deleted."""
    repository: str
    """Repository name."""
    options: CreateCommitOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "createCommit"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for createCommit

# Variants for createProject
@dataclass
class CreateProjectOptions:
    """Optional parameters for action createProject"""
    name: str|None = None
    """Name of an item or entity."""
    description: str|None = None
    """Description."""
    public: bool|None = None
    """Allow the project to be visible to public (users without a Bitbucket account)."""
    private: bool|None = None
    """Allow the project to be visible only to users with permission. Default for new projects."""

@dataclass
class CreateProject(BitbucketCloudCommand):
    """Create a new project."""
    workspace: str
    """Workspace"""
    project: str
    """Project name or key assigned to the project."""
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
    workspace: str|None = None
    """Workspace"""
    description: str|None = None
    """Description."""
    to: str|None = None
    """Also known as a target reference. For repository pull request, a to branch reference. For commit list, a commit or reference to retrieve commits before (inclusive)."""
    reviewers: Iterable[str]|str|None = None
    """Pull request reviewers key, name or UUID."""

@dataclass
class CreatePullRequest(BitbucketCloudCommand):
    """Create a new pull request. Use parameter from to set the source branch. Use parameter to to set the target branch. The target branch will be defaulted to master branch if parameter to is not specified. Use parameter reviewers to provide comma separated list of reviewers for the pull request. Note the owner of the pull request cannot be in the reviewers list. Note if there is already an open pull request with provided source and target branch, that pull request will be updated."""
    repository: str
    """Repository name."""
    pull_request: str
    """Plug request id."""
    from_: str
    """Also known as a source reference. For repository pull request, a from branch reference. For commit list, a commit or reference to retrieve commits after (exclusive)."""
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

# Variants for declinePullRequest
@dataclass
class DeclinePullRequestOptions:
    """Optional parameters for action declinePullRequest"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class DeclinePullRequest(BitbucketCloudCommand):
    """Decline a pull request."""
    repository: str
    """Repository name."""
    pull_request: str
    """Plug request id."""
    options: DeclinePullRequestOptions | None = None
    """ Action specific options """
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
    workspace: str|None = None
    """Workspace"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class DeleteBranch(BitbucketCloudCommand):
    """Delete repository branch."""
    repository: str
    """Repository name."""
    branch: str
    """Branch name."""
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
class DeleteProject(BitbucketCloudCommand):
    """Delete project."""
    workspace: str
    """Workspace"""
    project: str
    """Project name or key assigned to the project."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "deleteProject"

# End Variants for deleteProject

# Variants for exportData
@dataclass
class ExportDataOptions:
    """Optional parameters for action exportData"""
    workspace: str|None = None
    """Workspace"""
    repository: str|None = None
    """Repository name."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class ExportData(BitbucketCloudCommand):
    """Export data in a ACLI compatible script suitable for use with the run action normally on a different instance. Supported export types are WORKSPACE and REPOSITORY. Use '--options includeContinue' to have generated actions include the --continue parameter where appropriate to ignore already exists errors."""
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

# Variants for getBranch
@dataclass
class GetBranchOptions:
    """Optional parameters for action getBranch"""
    workspace: str|None = None
    """Workspace"""
    repository: str|None = None
    """Repository name."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetBranch(BitbucketCloudCommand):
    """Get repository branch information."""
    branch: str
    """Branch name."""
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
    workspace: str|None = None
    """Workspace"""
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
class GetBranchList(BitbucketCloudCommand):
    """Get List of branches with optional regex filtering on name."""
    repository: str
    """Repository name."""
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

# Variants for getBuildStatusList
@dataclass
class GetBuildStatusListOptions:
    """Optional parameters for action getBuildStatusList"""
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
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetBuildStatusList(BitbucketCloudCommand):
    """Get a list of build status entries associated with a repository branch including Bitbucket pipelines, Bamboo builds, and other CI servers like AWS and Azure."""
    repository: str
    """Repository name."""
    branch: str
    """Branch name."""
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
    workspace: str|None = None
    """Workspace"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetCommit(BitbucketCloudCommand):
    """Get repository commit information."""
    repository: str
    """Repository name."""
    commit: str
    """Commit id. In many cases, you can also use a tag name."""
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
    workspace: str|None = None
    """Workspace"""
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
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""

@dataclass
class GetCommitList(BitbucketCloudCommand):
    """Get list of commits with optional regex filtering on commit message and commit id."""
    repository: str
    """Repository name."""
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

# Variants for getDeploymentList
@dataclass
class GetDeploymentListOptions:
    """Optional parameters for action getDeploymentList"""
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
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetDeploymentList(BitbucketCloudCommand):
    """Get a list of repository deployments matching the selection criteria and optional regex filtering on name, key (slug), or UUID. List is sorted with more recently started first. By default, at most 200 entries are returned unless the limit parameter is explicitly set to something higher."""
    repository: str
    """Repository name."""
    options: GetDeploymentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getDeploymentList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getDeploymentList

# Variants for getDownload
@dataclass
class GetDownloadOptions:
    """Optional parameters for action getDownload"""
    workspace: str|None = None
    """Workspace"""
    name: str|None = None
    """Name of an item or entity."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetDownload(BitbucketCloudCommand):
    """Get repository download file by name."""
    repository: str
    """Repository name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: GetDownloadOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getDownload"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for getDownload

# Variants for getDownloadList
@dataclass
class GetDownloadListOptions:
    """Optional parameters for action getDownloadList"""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    start_date: str|None = None
    """Earliest date for date filtering specified based on dateFormat parameter or a negative duration value. Durations are specified by negative numbers with postfix of 's' (seconds), 'm' (minutes), 'h' (hours), 'd' (days). Data after the postfix is ignored. Examples are: -1d, -10m."""
    end_date: str|None = None
    """Latest date for date filtering specified based on dateFormat parameter or a negative duration value. Defaults to now. Durations are specified by negative numbers with postfix of 's' (seconds), 'm' (minutes), 'h' (hours), 'd' (days). Data after the postfix is ignored. Examples are: -1d, -10m."""
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
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""

@dataclass
class GetDownloadListGivenWorkspace(BitbucketCloudCommand):
    """Get a list of downloads for a repository with regex filtering on download name. Filter by date using the startDate and endDate parameters with absolute dates or durations specified by a negative integer value with s (secs), m (mins), h (hours), or d (days). Examples are '--endDate -30d', '--endDate -7days', or '--endDate -1h'."""
    workspace: str
    """Workspace"""
    options: GetDownloadListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getDownloadList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetDownloadListGivenRepository(BitbucketCloudCommand):
    """Get a list of downloads for a repository with regex filtering on download name. Filter by date using the startDate and endDate parameters with absolute dates or durations specified by a negative integer value with s (secs), m (mins), h (hours), or d (days). Examples are '--endDate -30d', '--endDate -7days', or '--endDate -1h'."""
    repository: str
    """Repository name."""
    options: GetDownloadListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getDownloadList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getDownloadList

# Variants for getEnvironment
@dataclass
class GetEnvironmentOptions:
    """Optional parameters for action getEnvironment"""
    workspace: str|None = None
    """Workspace"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetEnvironment(BitbucketCloudCommand):
    """Get deployment environment by name or UUID."""
    repository: str
    """Repository name."""
    environment: str
    """Deployment environment name or UUID."""
    options: GetEnvironmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getEnvironment"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getEnvironment

# Variants for getEnvironmentList
@dataclass
class GetEnvironmentListOptions:
    """Optional parameters for action getEnvironmentList"""
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
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetEnvironmentList(BitbucketCloudCommand):
    """Get a list of repository deployment environments matching the selection criteria and optional regex filtering on name or UUID."""
    repository: str
    """Repository name."""
    options: GetEnvironmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getEnvironmentList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getEnvironmentList

# Variants for getFileList
@dataclass
class GetFileListOptions:
    """Optional parameters for action getFileList"""
    workspace: str|None = None
    """Workspace"""
    path: str|None = None
    """Source path."""
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
class GetFileList(BitbucketCloudCommand):
    """Get file and directory list with regex filtering on path."""
    repository: str
    """Repository name."""
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

# Variants for getPipeline
@dataclass
class GetPipelineOptions:
    """Optional parameters for action getPipeline"""
    workspace: str|None = None
    """Workspace"""
    wait: bool|None = None
    """Wait for an action to complete or response match a specific state value. If a timeout is provided, the wait is limited to the timeout value."""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
    timeout: str|None = None
    """Wait timeout in seconds. Use -1 to wait forever."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    branch: str|None = None
    """Branch name."""
    commit: str|None = None
    """Commit id. In many cases, you can also use a tag name."""
    selector: str|None = None
    """Selector pattern for pipelines. Used to match against pipeline definition names. Normally custom pipelines names. Specify blank for the default pipeline."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetPipeline(BitbucketCloudCommand):
    """Get pipeline by pipeline number or UUID. Use @LAST to get the last pipeline or combine with the commit parameter to find the last pipeline for the commit id, branch, or tag. This action supports wait and related parameters similar to the startPipeline action. See the startPipeline action for more information."""
    repository: str
    """Repository name."""
    pipeline: str
    """Pipeline number, UUID, or @last. Use @LAST to get the last pipeline or combine with the branch or commit parameter to find the last pipeline for the branch, commit id or tag."""
    options: GetPipelineOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPipeline"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPipeline

# Variants for getPipelineCache
@dataclass
class GetPipelineCacheOptions:
    """Optional parameters for action getPipelineCache"""
    workspace: str|None = None
    """Workspace"""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetPipelineCache(BitbucketCloudCommand):
    """Get pipeline cache archive by cache name or UUID."""
    repository: str
    """Repository name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    name: str
    """Name of an item or entity."""
    options: GetPipelineCacheOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPipelineCache"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for getPipelineCache

# Variants for getPipelineCacheList
@dataclass
class GetPipelineCacheListOptions:
    """Optional parameters for action getPipelineCacheList"""
    workspace: str|None = None
    """Workspace"""
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
class GetPipelineCacheList(BitbucketCloudCommand):
    """Get list of pipeline caches for a repository with regex filtering on path."""
    repository: str
    """Repository name."""
    options: GetPipelineCacheListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPipelineCacheList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPipelineCacheList

# Variants for getPipelineList
@dataclass
class GetPipelineListOptions:
    """Optional parameters for action getPipelineList"""
    workspace: str|None = None
    """Workspace"""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
    branch: str|None = None
    """Branch name."""
    commit: str|None = None
    """Commit id. In many cases, you can also use a tag name."""
    selector: str|None = None
    """Selector pattern for pipelines. Used to match against pipeline definition names. Normally custom pipelines names. Specify blank for the default pipeline."""
    start_date: str|None = None
    """Earliest date for date filtering specified based on dateFormat parameter or a negative duration value. Durations are specified by negative numbers with postfix of 's' (seconds), 'm' (minutes), 'h' (hours), 'd' (days). Data after the postfix is ignored. Examples are: -1d, -10m."""
    end_date: str|None = None
    """Latest date for date filtering specified based on dateFormat parameter or a negative duration value. Defaults to now. Durations are specified by negative numbers with postfix of 's' (seconds), 'm' (minutes), 'h' (hours), 'd' (days). Data after the postfix is ignored. Examples are: -1d, -10m."""
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
class GetPipelineList(BitbucketCloudCommand):
    """Get list of pipelines with regex filtering by selector. Additional filtering available with the branch, commit, selector, and state parameters. Date range filtering on pipeline start date is available using startDate and endDate parameters. When no filtering is explicitly used, the default will be to limit the results to the last 7 days - - the default is equivalent to using '--startDate -7d'. This protects against inadvertent use potentially taking many minutes if not longer on older sites Note that the commit parameter could reference a branch or tag. Normally ordered by descending pipeline id."""
    repository: str
    """Repository name."""
    options: GetPipelineListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPipelineList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPipelineList

# Variants for getPipelineStep
@dataclass
class GetPipelineStepOptions:
    """Optional parameters for action getPipelineStep"""
    workspace: str|None = None
    """Workspace"""
    wait: bool|None = None
    """Wait for an action to complete or response match a specific state value. If a timeout is provided, the wait is limited to the timeout value."""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
    timeout: str|None = None
    """Wait timeout in seconds. Use -1 to wait forever."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    branch: str|None = None
    """Branch name."""
    commit: str|None = None
    """Commit id. In many cases, you can also use a tag name."""
    selector: str|None = None
    """Selector pattern for pipelines. Used to match against pipeline definition names. Normally custom pipelines names. Specify blank for the default pipeline."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetPipelineStep(BitbucketCloudCommand):
    """Get pipeline step by name or UUID. This action supports wait and related parameters similar to the startPipelineStep action. See the startPipelineStep action for more information."""
    repository: str
    """Repository name."""
    pipeline: str
    """Pipeline number, UUID, or @last. Use @LAST to get the last pipeline or combine with the branch or commit parameter to find the last pipeline for the branch, commit id or tag."""
    step: str
    """Pipeline step."""
    options: GetPipelineStepOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPipelineStep"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPipelineStep

# Variants for getPipelineStepList
@dataclass
class GetPipelineStepListOptions:
    """Optional parameters for action getPipelineStepList"""
    workspace: str|None = None
    """Workspace"""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    branch: str|None = None
    """Branch name."""
    commit: str|None = None
    """Commit id. In many cases, you can also use a tag name."""
    selector: str|None = None
    """Selector pattern for pipelines. Used to match against pipeline definition names. Normally custom pipelines names. Specify blank for the default pipeline."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetPipelineStepList(BitbucketCloudCommand):
    """Get list of pipeline steps with regex filtering on step name."""
    repository: str
    """Repository name."""
    pipeline: str
    """Pipeline number, UUID, or @last. Use @LAST to get the last pipeline or combine with the branch or commit parameter to find the last pipeline for the branch, commit id or tag."""
    options: GetPipelineStepListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPipelineStepList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPipelineStepList

# Variants for getProject
@dataclass
class GetProjectOptions:
    """Optional parameters for action getProject"""
    workspace: str|None = None
    """Workspace"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetProject(BitbucketCloudCommand):
    """Get project information."""
    project: str
    """Project name or key assigned to the project."""
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
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetProjectList(BitbucketCloudCommand):
    """Get a list of projects which belongs to the given workspace."""
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

# Variants for getPullRequest
@dataclass
class GetPullRequestOptions:
    """Optional parameters for action getPullRequest"""
    workspace: str|None = None
    """Workspace"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetPullRequest(BitbucketCloudCommand):
    """Get pull request information under a repository."""
    repository: str
    """Repository name."""
    pull_request: str
    """Plug request id."""
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
    workspace: str|None = None
    """Workspace"""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
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
class GetPullRequestList(BitbucketCloudCommand):
    """Get List of pull requests for a user with optional filtering on repository, state and optional regex filtering on title,description."""
    repository: str
    """Repository name."""
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
    workspace: str|None = None
    """Workspace"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetRepository(BitbucketCloudCommand):
    """Get repository information."""
    repository: str
    """Repository name."""
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
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetRepositoryList(BitbucketCloudCommand):
    """Get a list of repositories matching the selection criteria and optional regex filtering on name or slug or UUID."""
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

# Variants for getRunner

@dataclass
class GetRunnerGivenWorkspaceAndName(BitbucketCloudCommand):
    """Get workspace or repository runner by name or UUID. If a name is not unique, the first runner found will be returned."""
    workspace: str
    """Workspace"""
    name: str
    """Name of an item or entity."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getRunner"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class GetRunnerGivenRepositoryAndName(BitbucketCloudCommand):
    """Get workspace or repository runner by name or UUID. If a name is not unique, the first runner found will be returned."""
    repository: str
    """Repository name."""
    name: str
    """Name of an item or entity."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getRunner"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for getRunner

# Variants for getRunnerList
@dataclass
class GetRunnerListOptions:
    """Optional parameters for action getRunnerList"""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""
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
class GetRunnerListGivenWorkspace(BitbucketCloudCommand):
    """Get list of pipeline runners for a workspace or a repository or both. Note that @all can be specified for the repository parameter to get runner information across all repositories in a workspace or all authorized."""
    workspace: str
    """Workspace"""
    options: GetRunnerListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getRunnerList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetRunnerListGivenRepository(BitbucketCloudCommand):
    """Get list of pipeline runners for a workspace or a repository or both. Note that @all can be specified for the repository parameter to get runner information across all repositories in a workspace or all authorized."""
    repository: str
    """Repository name."""
    options: GetRunnerListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getRunnerList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getRunnerList

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
class GetSource(BitbucketCloudCommand):
    """Get source."""
    workspace: str
    """Workspace"""
    repository: str
    """Repository name."""
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

# Variants for getUser
@dataclass
class GetUserOptions:
    """Optional parameters for action getUser"""
    user_id: str|None = None
    """User id user related actions. Must be a Atlassian Cloud account id or user UUID."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetUser(BitbucketCloudCommand):
    """Get user information for current user (default) or a specific user by using the userId parameter. Specify userId by Atlassian Cloud id or UUID. You cannot use the user account slug."""
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

# Variants for getVariableList
@dataclass
class GetVariableListOptions:
    """Optional parameters for action getVariableList"""
    environment: str|None = None
    """Deployment environment name or UUID."""
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
    reference: str|None = None
    """Reference to a replacement key value used to remember an action specific value like issue key, entity id, or similar so it can be referenced later. Each action that allows this parameter will specify that the reference parameter is valid for the action and the first entry listed for available replacement variables help text will be the value set. If you need access to a different replacement variable in your script, you will need to use the setReplacementVariables action after the action to set a new replacement variable of your choosing to one of the other available replacement variables."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetVariableListGivenWorkspace(BitbucketCloudCommand):
    """Get a list of workspace, repository, or deployment environment variables based on regex filtering on variable names. To get variables for all environments for a repository, set the environment parameter to @all."""
    workspace: str
    """Workspace"""
    options: GetVariableListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getVariableList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetVariableListGivenRepository(BitbucketCloudCommand):
    """Get a list of workspace, repository, or deployment environment variables based on regex filtering on variable names. To get variables for all environments for a repository, set the environment parameter to @all."""
    repository: str
    """Repository name."""
    options: GetVariableListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getVariableList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getVariableList

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
class GetWorkspace(BitbucketCloudCommand):
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
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""

@dataclass
class GetWorkspaceList(BitbucketCloudCommand):
    """Get a list of workspaces with regex filtering based on name or key."""
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
    def supports_output_type() -> bool:
        return True

# End Variants for getWorkspaceList

# Variants for mergePullRequest
@dataclass
class MergePullRequestOptions:
    """Optional parameters for action mergePullRequest"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class MergePullRequest(BitbucketCloudCommand):
    """Merge a pull request."""
    repository: str
    """Repository name."""
    pull_request: str
    """Plug request id."""
    options: MergePullRequestOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "mergePullRequest"

# End Variants for mergePullRequest

# Variants for publishSource
@dataclass
class PublishSourceOptions:
    """Optional parameters for action publishSource"""
    revision: str|None = None
    """Repository revision id like a commit id, branch, tag, or special value like HEAD (for Git) and tip for Mercurial."""
    parent: str|None = None
    """Confluence page title for a parent page."""
    replace: bool|None = None
    """Replace existing entity on add, create, or similar actions."""
    descendents: bool|None = None
    """All descendent files for a directory."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""

@dataclass
class PublishSource(BitbucketCloudCommand):
    """Publish source to Confluence. When the path represents a directory, all files included in the same file list filtering conditions as getFileList will be published to the page."""
    workspace: str
    """Workspace"""
    repository: str
    """Repository name."""
    path: str
    """Source path."""
    space: str
    """Confluence space key. For some actions, a space name may also work."""
    title: str
    """Source title."""
    target_server: str
    """Confluence site configuration reference for publish requests."""
    options: PublishSourceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "publishSource"

# End Variants for publishSource

# Variants for removeDownload
@dataclass
class RemoveDownloadOptions:
    """Optional parameters for action removeDownload"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class RemoveDownload(BitbucketCloudCommand):
    """Remove download from repository download area."""
    repository: str
    """Repository name."""
    name: str
    """Name of an item or entity."""
    options: RemoveDownloadOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeDownload"

# End Variants for removeDownload

# Variants for removeEnvironment
@dataclass
class RemoveEnvironmentOptions:
    """Optional parameters for action removeEnvironment"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class RemoveEnvironment(BitbucketCloudCommand):
    """Remove deployment environment by name or UUID."""
    repository: str
    """Repository name."""
    environment: str
    """Deployment environment name or UUID."""
    options: RemoveEnvironmentOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeEnvironment"

# End Variants for removeEnvironment

# Variants for removePipelineCache
@dataclass
class RemovePipelineCacheOptions:
    """Optional parameters for action removePipelineCache"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class RemovePipelineCache(BitbucketCloudCommand):
    """Remove a pipeline cache by name or UUID."""
    repository: str
    """Repository name."""
    name: str
    """Name of an item or entity."""
    options: RemovePipelineCacheOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removePipelineCache"

# End Variants for removePipelineCache

# Variants for removeRunner

@dataclass
class RemoveRunnerGivenWorkspaceAndName(BitbucketCloudCommand):
    """Remove pipeline runner from workspace or repository by name or UUID. If a name is not unique, the first runner found will be removed."""
    workspace: str
    """Workspace"""
    name: str
    """Name of an item or entity."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeRunner"

@dataclass
class RemoveRunnerGivenRepositoryAndName(BitbucketCloudCommand):
    """Remove pipeline runner from workspace or repository by name or UUID. If a name is not unique, the first runner found will be removed."""
    repository: str
    """Repository name."""
    name: str
    """Name of an item or entity."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeRunner"

# End Variants for removeRunner

# Variants for removeVariables
@dataclass
class RemoveVariablesOptions:
    """Optional parameters for action removeVariables"""
    environment: str|None = None
    """Deployment environment name or UUID."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    property_file: str|None = None
    """Property file with database parameters, field mappings, or client specific information."""

@dataclass
class RemoveVariablesGivenWorkspace(BitbucketCloudCommand):
    """Remove workspace, repository, or deployment environment variables. Specify the variable names using the field parameters. Variables can also be removed by keys specified in a property file using the propertyFile parameter."""
    workspace: str
    """Workspace"""
    options: RemoveVariablesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeVariables"

@dataclass
class RemoveVariablesGivenRepository(BitbucketCloudCommand):
    """Remove workspace, repository, or deployment environment variables. Specify the variable names using the field parameters. Variables can also be removed by keys specified in a property file using the propertyFile parameter."""
    repository: str
    """Repository name."""
    options: RemoveVariablesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeVariables"

# End Variants for removeVariables

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
class RenderRequest(BitbucketCloudCommand):
    """Render URL based request. URL can be a partial Bitbucket Cloud URL. The response data modified by optional findReplace processing is returned. Use '--pretty' to format returned JSON data in a more readable form."""
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

# Variants for restartPipeline
@dataclass
class RestartPipelineOptions:
    """Optional parameters for action restartPipeline"""
    workspace: str|None = None
    """Workspace"""
    wait: bool|None = None
    """Wait for an action to complete or response match a specific state value. If a timeout is provided, the wait is limited to the timeout value."""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
    timeout: str|None = None
    """Wait timeout in seconds. Use -1 to wait forever."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    branch: str|None = None
    """Branch name."""
    commit: str|None = None
    """Commit id. In many cases, you can also use a tag name."""
    selector: str|None = None
    """Selector pattern for pipelines. Used to match against pipeline definition names. Normally custom pipelines names. Specify blank for the default pipeline."""

@dataclass
class RestartPipeline(BitbucketCloudCommand):
    """Restart an existing pipeline. The wait and related parameters can be used with the same behavior as on the startPipeline action."""
    repository: str
    """Repository name."""
    pipeline: str
    """Pipeline number, UUID, or @last. Use @LAST to get the last pipeline or combine with the branch or commit parameter to find the last pipeline for the branch, commit id or tag."""
    options: RestartPipelineOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "restartPipeline"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for restartPipeline

# Variants for runFromBranchList
@dataclass
class RunFromBranchListOptions:
    """Optional parameters for action runFromBranchList"""
    workspace: str|None = None
    """Workspace"""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
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
class RunFromBranchListGivenRepositoryAndInput(BitbucketCloudCommand):
    """Run actions for branches for a repository with regex filtering on key or name."""
    repository: str
    """Repository name."""
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
class RunFromBranchListGivenRepositoryAndCommon(BitbucketCloudCommand):
    """Run actions for branches for a repository with regex filtering on key or name."""
    repository: str
    """Repository name."""
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
class RunFromBranchListGivenRepositoryAndFile(BitbucketCloudCommand):
    """Run actions for branches for a repository with regex filtering on key or name."""
    repository: str
    """Repository name."""
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

# Variants for runFromCommitList
@dataclass
class RunFromCommitListOptions:
    """Optional parameters for action runFromCommitList"""
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
class RunFromCommitListGivenRepositoryAndInput(BitbucketCloudCommand):
    """Run actions for commits with optional regex filtering on commit message and commit id."""
    repository: str
    """Repository name."""
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
class RunFromCommitListGivenRepositoryAndCommon(BitbucketCloudCommand):
    """Run actions for commits with optional regex filtering on commit message and commit id."""
    repository: str
    """Repository name."""
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
class RunFromCommitListGivenRepositoryAndFile(BitbucketCloudCommand):
    """Run actions for commits with optional regex filtering on commit message and commit id."""
    repository: str
    """Repository name."""
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

# Variants for runFromDeploymentList
@dataclass
class RunFromDeploymentListOptions:
    """Optional parameters for action runFromDeploymentList"""
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
class RunFromDeploymentListGivenRepositoryAndInput(BitbucketCloudCommand):
    """Run actions for each deployment associated with a repository with regex filtering on deployment name equivalent to getDeploymentList."""
    repository: str
    """Repository name."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromDeploymentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromDeploymentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromDeploymentListGivenRepositoryAndCommon(BitbucketCloudCommand):
    """Run actions for each deployment associated with a repository with regex filtering on deployment name equivalent to getDeploymentList."""
    repository: str
    """Repository name."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromDeploymentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromDeploymentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromDeploymentListGivenRepositoryAndFile(BitbucketCloudCommand):
    """Run actions for each deployment associated with a repository with regex filtering on deployment name equivalent to getDeploymentList."""
    repository: str
    """Repository name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromDeploymentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromDeploymentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromDeploymentList

# Variants for runFromDownloadList
@dataclass
class RunFromDownloadListOptions:
    """Optional parameters for action runFromDownloadList"""
    workspace: str|None = None
    """Workspace"""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    start_date: str|None = None
    """Earliest date for date filtering specified based on dateFormat parameter or a negative duration value. Durations are specified by negative numbers with postfix of 's' (seconds), 'm' (minutes), 'h' (hours), 'd' (days). Data after the postfix is ignored. Examples are: -1d, -10m."""
    end_date: str|None = None
    """Latest date for date filtering specified based on dateFormat parameter or a negative duration value. Defaults to now. Durations are specified by negative numbers with postfix of 's' (seconds), 'm' (minutes), 'h' (hours), 'd' (days). Data after the postfix is ignored. Examples are: -1d, -10m."""
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
class RunFromDownloadListGivenRepositoryAndInput(BitbucketCloudCommand):
    """Run actions for each download associated with a repository with regex filtering on download name and other filtering equivalent to getDownloadList."""
    repository: str
    """Repository name."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromDownloadListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromDownloadList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromDownloadListGivenRepositoryAndCommon(BitbucketCloudCommand):
    """Run actions for each download associated with a repository with regex filtering on download name and other filtering equivalent to getDownloadList."""
    repository: str
    """Repository name."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromDownloadListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromDownloadList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromDownloadListGivenRepositoryAndFile(BitbucketCloudCommand):
    """Run actions for each download associated with a repository with regex filtering on download name and other filtering equivalent to getDownloadList."""
    repository: str
    """Repository name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromDownloadListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromDownloadList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromDownloadList

# Variants for runFromEnvironmentList
@dataclass
class RunFromEnvironmentListOptions:
    """Optional parameters for action runFromEnvironmentList"""
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
class RunFromEnvironmentListGivenRepositoryAndInput(BitbucketCloudCommand):
    """Run actions for each deployment environment associated with a repository with regex filtering on environment name equivalent to getEnvironmentList."""
    repository: str
    """Repository name."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromEnvironmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromEnvironmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromEnvironmentListGivenRepositoryAndCommon(BitbucketCloudCommand):
    """Run actions for each deployment environment associated with a repository with regex filtering on environment name equivalent to getEnvironmentList."""
    repository: str
    """Repository name."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromEnvironmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromEnvironmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromEnvironmentListGivenRepositoryAndFile(BitbucketCloudCommand):
    """Run actions for each deployment environment associated with a repository with regex filtering on environment name equivalent to getEnvironmentList."""
    repository: str
    """Repository name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromEnvironmentListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromEnvironmentList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromEnvironmentList

# Variants for runFromPipelineList
@dataclass
class RunFromPipelineListOptions:
    """Optional parameters for action runFromPipelineList"""
    workspace: str|None = None
    """Workspace"""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
    branch: str|None = None
    """Branch name."""
    commit: str|None = None
    """Commit id. In many cases, you can also use a tag name."""
    selector: str|None = None
    """Selector pattern for pipelines. Used to match against pipeline definition names. Normally custom pipelines names. Specify blank for the default pipeline."""
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
class RunFromPipelineListGivenRepositoryAndInput(BitbucketCloudCommand):
    """Run actions for each pipeline with regex filtering on selector and other filtering equivalent to getPipelineList."""
    repository: str
    """Repository name."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromPipelineListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPipelineList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPipelineListGivenRepositoryAndCommon(BitbucketCloudCommand):
    """Run actions for each pipeline with regex filtering on selector and other filtering equivalent to getPipelineList."""
    repository: str
    """Repository name."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromPipelineListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPipelineList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPipelineListGivenRepositoryAndFile(BitbucketCloudCommand):
    """Run actions for each pipeline with regex filtering on selector and other filtering equivalent to getPipelineList."""
    repository: str
    """Repository name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromPipelineListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPipelineList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromPipelineList

# Variants for runFromPipelineStepList
@dataclass
class RunFromPipelineStepListOptions:
    """Optional parameters for action runFromPipelineStepList"""
    workspace: str|None = None
    """Workspace"""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
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
class RunFromPipelineStepListGivenRepositoryAndPipelineAndInput(BitbucketCloudCommand):
    """Run actions for each pipeline step with regex filtering on step name and other filtering equivalent to getPipelineStepList."""
    repository: str
    """Repository name."""
    pipeline: str
    """Pipeline number, UUID, or @last. Use @LAST to get the last pipeline or combine with the branch or commit parameter to find the last pipeline for the branch, commit id or tag."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromPipelineStepListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPipelineStepList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPipelineStepListGivenRepositoryAndPipelineAndCommon(BitbucketCloudCommand):
    """Run actions for each pipeline step with regex filtering on step name and other filtering equivalent to getPipelineStepList."""
    repository: str
    """Repository name."""
    pipeline: str
    """Pipeline number, UUID, or @last. Use @LAST to get the last pipeline or combine with the branch or commit parameter to find the last pipeline for the branch, commit id or tag."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromPipelineStepListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPipelineStepList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromPipelineStepListGivenRepositoryAndPipelineAndFile(BitbucketCloudCommand):
    """Run actions for each pipeline step with regex filtering on step name and other filtering equivalent to getPipelineStepList."""
    repository: str
    """Repository name."""
    pipeline: str
    """Pipeline number, UUID, or @last. Use @LAST to get the last pipeline or combine with the branch or commit parameter to find the last pipeline for the branch, commit id or tag."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromPipelineStepListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromPipelineStepList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromPipelineStepList

# Variants for runFromProjectList
@dataclass
class RunFromProjectListOptions:
    """Optional parameters for action runFromProjectList"""
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
class RunFromProjectListGivenInput(BitbucketCloudCommand):
    """Run actions for each project with regex filtering on project key or name equivalent to getProjectList."""
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
class RunFromProjectListGivenCommon(BitbucketCloudCommand):
    """Run actions for each project with regex filtering on project key or name equivalent to getProjectList."""
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
class RunFromProjectListGivenFile(BitbucketCloudCommand):
    """Run actions for each project with regex filtering on project key or name equivalent to getProjectList."""
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
    workspace: str|None = None
    """Workspace"""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
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
class RunFromPullRequestListGivenRepositoryAndInput(BitbucketCloudCommand):
    """Run actions for pull requests for a repository with regex filtering on name. Also, filtering by state."""
    repository: str
    """Repository name."""
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
class RunFromPullRequestListGivenRepositoryAndCommon(BitbucketCloudCommand):
    """Run actions for pull requests for a repository with regex filtering on name. Also, filtering by state."""
    repository: str
    """Repository name."""
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
class RunFromPullRequestListGivenRepositoryAndFile(BitbucketCloudCommand):
    """Run actions for pull requests for a repository with regex filtering on name. Also, filtering by state."""
    repository: str
    """Repository name."""
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
class RunFromRepositoryListGivenInput(BitbucketCloudCommand):
    """Run actions for each repository with regex filtering on repository key or name equivalent to getRepositoryList."""
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
class RunFromRepositoryListGivenCommon(BitbucketCloudCommand):
    """Run actions for each repository with regex filtering on repository key or name equivalent to getRepositoryList."""
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
class RunFromRepositoryListGivenFile(BitbucketCloudCommand):
    """Run actions for each repository with regex filtering on repository key or name equivalent to getRepositoryList."""
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

# Variants for runFromRunnerList
@dataclass
class RunFromRunnerListOptions:
    """Optional parameters for action runFromRunnerList"""
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
class RunFromRunnerListGivenWorkspaceAndInput(BitbucketCloudCommand):
    """Run actions for each pipeline runner from a list runners for workspace, repository, or both with parameters and filtering the same as getRunnerList."""
    workspace: str
    """Workspace"""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromRunnerListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromRunnerList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromRunnerListGivenWorkspaceAndCommon(BitbucketCloudCommand):
    """Run actions for each pipeline runner from a list runners for workspace, repository, or both with parameters and filtering the same as getRunnerList."""
    workspace: str
    """Workspace"""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromRunnerListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromRunnerList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromRunnerListGivenWorkspaceAndFile(BitbucketCloudCommand):
    """Run actions for each pipeline runner from a list runners for workspace, repository, or both with parameters and filtering the same as getRunnerList."""
    workspace: str
    """Workspace"""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromRunnerListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromRunnerList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromRunnerListGivenRepositoryAndInput(BitbucketCloudCommand):
    """Run actions for each pipeline runner from a list runners for workspace, repository, or both with parameters and filtering the same as getRunnerList."""
    repository: str
    """Repository name."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromRunnerListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromRunnerList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromRunnerListGivenRepositoryAndCommon(BitbucketCloudCommand):
    """Run actions for each pipeline runner from a list runners for workspace, repository, or both with parameters and filtering the same as getRunnerList."""
    repository: str
    """Repository name."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromRunnerListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromRunnerList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromRunnerListGivenRepositoryAndFile(BitbucketCloudCommand):
    """Run actions for each pipeline runner from a list runners for workspace, repository, or both with parameters and filtering the same as getRunnerList."""
    repository: str
    """Repository name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromRunnerListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromRunnerList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromRunnerList

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
class RunFromWorkspaceListGivenInput(BitbucketCloudCommand):
    """Run actions for each workspace with regex filtering on workspace key or name equivalent to getWorkspaceList."""
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
class RunFromWorkspaceListGivenCommon(BitbucketCloudCommand):
    """Run actions for each workspace with regex filtering on workspace key or name equivalent to getWorkspaceList."""
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
class RunFromWorkspaceListGivenFile(BitbucketCloudCommand):
    """Run actions for each workspace with regex filtering on workspace key or name equivalent to getWorkspaceList."""
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

# Variants for startPipeline
@dataclass
class StartPipelineOptions:
    """Optional parameters for action startPipeline"""
    workspace: str|None = None
    """Workspace"""
    selector: str|None = None
    """Selector pattern for pipelines. Used to match against pipeline definition names. Normally custom pipelines names. Specify blank for the default pipeline."""
    selector_type: str|None = None
    """Type of selector base on pipeline definitions like default, branches, custom, pull-requests, or tags. Specify if you need to override the default normally determined from other other parameters if it is an allowed combination."""
    wait: bool|None = None
    """Wait for an action to complete or response match a specific state value. If a timeout is provided, the wait is limited to the timeout value."""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
    reference: str|None = None
    """Reference to a replacement key value used to remember an action specific value like issue key, entity id, or similar so it can be referenced later. Each action that allows this parameter will specify that the reference parameter is valid for the action and the first entry listed for available replacement variables help text will be the value set. If you need access to a different replacement variable in your script, you will need to use the setReplacementVariables action after the action to set a new replacement variable of your choosing to one of the other available replacement variables."""
    timeout: str|None = None
    """Wait timeout in seconds. Use -1 to wait forever."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""

@dataclass
class StartPipelineGivenRepositoryAndBranch(BitbucketCloudCommand):
    """Start a pipeline run. Field parameters can be used to provide variable settings for a custom pipeline run. Use the wait parameter to wait for the pipeline to be at least at the PAUSED state (or other state provided by the state parameter). When waiting for a PAUSED or COMPLETED pipeline, the action will fail if the pipeline has a result that is not considered successful unless the continue parameter is specified. Alternatively, the same wait related parameters can a used on a separate getPipeline action enabling multiple pipelines to be started in a script without wait and then followed later by getPipeline with wait to handle results. Use reference parameter to set a specific replacement variable to pipeline number started by this action for later use in a script like for the alternative wait option."""
    repository: str
    """Repository name."""
    branch: str
    """Branch name."""
    options: StartPipelineOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "startPipeline"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class StartPipelineGivenRepositoryAndCommit(BitbucketCloudCommand):
    """Start a pipeline run. Field parameters can be used to provide variable settings for a custom pipeline run. Use the wait parameter to wait for the pipeline to be at least at the PAUSED state (or other state provided by the state parameter). When waiting for a PAUSED or COMPLETED pipeline, the action will fail if the pipeline has a result that is not considered successful unless the continue parameter is specified. Alternatively, the same wait related parameters can a used on a separate getPipeline action enabling multiple pipelines to be started in a script without wait and then followed later by getPipeline with wait to handle results. Use reference parameter to set a specific replacement variable to pipeline number started by this action for later use in a script like for the alternative wait option."""
    repository: str
    """Repository name."""
    commit: str
    """Commit id. In many cases, you can also use a tag name."""
    options: StartPipelineOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "startPipeline"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class StartPipelineGivenRepositoryAndPullRequest(BitbucketCloudCommand):
    """Start a pipeline run. Field parameters can be used to provide variable settings for a custom pipeline run. Use the wait parameter to wait for the pipeline to be at least at the PAUSED state (or other state provided by the state parameter). When waiting for a PAUSED or COMPLETED pipeline, the action will fail if the pipeline has a result that is not considered successful unless the continue parameter is specified. Alternatively, the same wait related parameters can a used on a separate getPipeline action enabling multiple pipelines to be started in a script without wait and then followed later by getPipeline with wait to handle results. Use reference parameter to set a specific replacement variable to pipeline number started by this action for later use in a script like for the alternative wait option."""
    repository: str
    """Repository name."""
    pull_request: str
    """Plug request id."""
    options: StartPipelineOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "startPipeline"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for startPipeline

# Variants for startPipelineStep
@dataclass
class StartPipelineStepOptions:
    """Optional parameters for action startPipelineStep"""
    workspace: str|None = None
    """Workspace"""
    wait: bool|None = None
    """Wait for an action to complete or response match a specific state value. If a timeout is provided, the wait is limited to the timeout value."""
    state: str|None = None
    """State of a pull request. Possible values are MERGED, SUPERSEDED, OPEN, DECLINED."""
    timeout: str|None = None
    """Wait timeout in seconds. Use -1 to wait forever."""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    redeploy: bool|None = None
    """Allow startPipelineStep action to redeploy a completed deployment step."""
    branch: str|None = None
    """Branch name."""
    commit: str|None = None
    """Commit id. In many cases, you can also use a tag name."""
    selector: str|None = None
    """Selector pattern for pipelines. Used to match against pipeline definition names. Normally custom pipelines names. Specify blank for the default pipeline."""

@dataclass
class StartPipelineStep(BitbucketCloudCommand):
    """Start a step for an existing pipeline. Use the continue parameter to ignore already started or similar invalid state errors. Use the wait parameter to wait for the pipeline step to be at least at the PAUSED state (or other state provided by the state parameter). When waiting for a PAUSED or COMPLETED pipeline step, the action will fail if the pipeline step has a result that is not considered successful unless the continue parameter is specified."""
    repository: str
    """Repository name."""
    pipeline: str
    """Pipeline number, UUID, or @last. Use @LAST to get the last pipeline or combine with the branch or commit parameter to find the last pipeline for the branch, commit id or tag."""
    options: StartPipelineStepOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "startPipelineStep"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for startPipelineStep

# Variants for stopPipeline
@dataclass
class StopPipelineOptions:
    """Optional parameters for action stopPipeline"""
    workspace: str|None = None
    """Workspace"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""
    branch: str|None = None
    """Branch name."""
    commit: str|None = None
    """Commit id. In many cases, you can also use a tag name."""
    selector: str|None = None
    """Selector pattern for pipelines. Used to match against pipeline definition names. Normally custom pipelines names. Specify blank for the default pipeline."""

@dataclass
class StopPipeline(BitbucketCloudCommand):
    """Stop a running pipeline by pipeline number or UUID. Use the continue parameter to ignore an already stopped pipeline."""
    repository: str
    """Repository name."""
    pipeline: str
    """Pipeline number, UUID, or @last. Use @LAST to get the last pipeline or combine with the branch or commit parameter to find the last pipeline for the branch, commit id or tag."""
    options: StopPipelineOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "stopPipeline"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for stopPipeline

# Variants for unapproveCommit
@dataclass
class UnapproveCommitOptions:
    """Optional parameters for action unapproveCommit"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class UnapproveCommit(BitbucketCloudCommand):
    """Unapprove a Commit."""
    repository: str
    """Repository name."""
    commit: str
    """Commit id. In many cases, you can also use a tag name."""
    options: UnapproveCommitOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "unapproveCommit"

# End Variants for unapproveCommit

# Variants for unapprovePullRequest
@dataclass
class UnapprovePullRequestOptions:
    """Optional parameters for action unapprovePullRequest"""
    workspace: str|None = None
    """Workspace"""

@dataclass
class UnapprovePullRequest(BitbucketCloudCommand):
    """Unapprove a pull request."""
    repository: str
    """Repository name."""
    pull_request: str
    """Plug request id."""
    options: UnapprovePullRequestOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "unapprovePullRequest"

# End Variants for unapprovePullRequest

# Variants for updateProject
@dataclass
class UpdateProjectOptions:
    """Optional parameters for action updateProject"""
    name: str|None = None
    """Name of an item or entity."""
    description: str|None = None
    """Description."""
    public: bool|None = None
    """Allow the project to be visible to public (users without a Bitbucket account)."""
    private: bool|None = None
    """Allow the project to be visible only to users with permission. Default for new projects."""

@dataclass
class UpdateProject(BitbucketCloudCommand):
    """Update an existing project."""
    workspace: str
    """Workspace"""
    project: str
    """Project name or key assigned to the project."""
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
    workspace: str|None = None
    """Workspace"""
    name: str|None = None
    """Name of an item or entity."""
    description: str|None = None
    """Description."""
    from_: str|None = None
    """Also known as a source reference. For repository pull request, a from branch reference. For commit list, a commit or reference to retrieve commits after (exclusive)."""
    to: str|None = None
    """Also known as a target reference. For repository pull request, a to branch reference. For commit list, a commit or reference to retrieve commits before (inclusive)."""
    reviewers: Iterable[str]|str|None = None
    """Pull request reviewers key, name or UUID."""

@dataclass
class UpdatePullRequest(BitbucketCloudCommand):
    """Update pull request information. Note if there is already an open pull request with provided source and target branch, that pull request will be updated."""
    repository: str
    """Repository name."""
    pull_request: str
    """Plug request id."""
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

# Variants for updateVariables
@dataclass
class UpdateVariablesOptions:
    """Optional parameters for action updateVariables"""
    environment: str|None = None
    """Deployment environment name or UUID."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    property_file: str|None = None
    """Property file with database parameters, field mappings, or client specific information."""
    secured: bool|None = None
    """When adding and updating variables, this option will mark variables as secured so they are hidden from viewing."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""

@dataclass
class UpdateVariablesGivenWorkspace(BitbucketCloudCommand):
    """Update workspace, repository, or deployment environment variables. Use one or more field parameters where each field parameter is a key=value pair. Specify a secured variable by appending ':secured' like key=value:secured. To secure all variables added or updated, use the secured parameter. Variables can also be updated from a property file using the propertyFile parameter."""
    workspace: str
    """Workspace"""
    options: UpdateVariablesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateVariables"

@dataclass
class UpdateVariablesGivenRepository(BitbucketCloudCommand):
    """Update workspace, repository, or deployment environment variables. Use one or more field parameters where each field parameter is a key=value pair. Specify a secured variable by appending ':secured' like key=value:secured. To secure all variables added or updated, use the secured parameter. Variables can also be updated from a property file using the propertyFile parameter."""
    repository: str
    """Repository name."""
    options: UpdateVariablesOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateVariables"

# End Variants for updateVariables
