from dataclasses import dataclass
from acli.base.spec import Command, Client, RemoteClient
from acli.clients.options import LoggingOptions, CommonOptions
from typing import Iterable

@dataclass
class MarketplaceCommand(Command):
    pass

@dataclass
class MarketplaceClient(RemoteClient):
    def execute(self, command: MarketplaceCommand):
        return super().do_execute(command)

# Variants for addAsset
@dataclass
class AddAssetOptions:
    """Optional parameters for action addAsset"""
    name: str|None = None
    """Contact display name."""
    type: str|None = None
    """Metric type or feedback type. Valid metric types are churn, conversions, and renewals. Valid feedback types are disable or uninstall."""

@dataclass
class AddAssetGivenFile(MarketplaceCommand):
    """Upload a file to be added as a Marketplace jar or obr artifact or image asset. Name defaults to the file name unless the name parameter is used. Alternatively, artifacts can be loaded from a public URL. For image assets, specify a valid Marketplace image type using the type parameter. Marketplace assets are public and only findable by using the name returned from addAsset. The returned asset name is universally unique name."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: AddAssetOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addAsset"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class AddAssetGivenUrl(MarketplaceCommand):
    """Upload a file to be added as a Marketplace jar or obr artifact or image asset. Name defaults to the file name unless the name parameter is used. Alternatively, artifacts can be loaded from a public URL. For image assets, specify a valid Marketplace image type using the type parameter. Marketplace assets are public and only findable by using the name returned from addAsset. The returned asset name is universally unique name."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    options: AddAssetOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addAsset"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addAsset

# Variants for addVendorContact

@dataclass
class AddVendorContact(MarketplaceCommand):
    """Add a contact for a vendor. Name must be an Atlassian id user's email address."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    name: str
    """Contact display name."""
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addVendorContact"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addVendorContact

# Variants for addVersion
@dataclass
class AddVersionOptions:
    """Optional parameters for action addVersion"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""

@dataclass
class AddVersion(MarketplaceCommand):
    """Add a new version to an app. By default, the version is added with status private. The version parameter (also known as the build number) must be a unique positive number and represents an ordered and unique identifier for the version. If the app is not directly installable, provide a web site link URL or a binary download URL for the url parameter. Use '--url @last' to set the URL to the URL from the base version. Use '--options binary' if the link is to a binary. For an installable app, the hosting parameter must be provided and the url parameter should reference a Marketplace artifact asset name or partial URL created using the addAsset action or similar. Version name (usually following a user understandable name pattern like 5.3.0) will be taken from the version identified in the artifact when provided, otherwise it must be provided by the name parameter. Information is copied from the latest version of the app with the hosting specified and field parameters can be used to override specific values for the version. Specifically, releaseNotes, releaseSummary, and moreDetails can be set using something like '--field "releaseSummary=Many improvements and fixes"'. Other field values can also be set in the JSON representation of the version, but this is a user responsibility and not officially supported. It is recommended to set more complicated fields (like compatibility) in the UI after the new version is added."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    version: str
    """App version name or numeric key (build number). Defaults to @latest. The key is a unique identifier and defines version ordering."""
    url: str
    """Action specific setting. URL or partial URL for renderRequest. Database access URL for SQL related actions. URL for application link related actions."""
    hosting: str
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    options: AddVersionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "addVersion"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for addVersion

# Variants for exportData
@dataclass
class ExportDataOptions:
    """Optional parameters for action exportData"""
    type: str|None = None
    """Metric type or feedback type. Valid metric types are churn, conversions, and renewals. Valid feedback types are disable or uninstall."""
    app: str|None = None
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    search: str|None = None
    """Search string."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is since the beginning."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class ExportData(MarketplaceCommand):
    """Bulk export for Marketplace data. This uses bulk export support provided by Marketplace for the following export types: TRANSACTIONS, FREE_STARTER_TIER, LICENSES, LICENSE_EVENTS, and FEEDBACK. Marketplace supports either CSV or JSON format directly. By default, CSV is exported. Use the outputType parameter to request other formats. JSON will be directly from Marketplace. Other output types supported by ACLI are also allowed and will be converted from the CSV output. Database output is also support just like other ACLI list actions for CSV data with the various database related parameters. Marketplace provides filtering support for things like app, hosting, text search, start and end dates. Options available for license related exports are '--options includeAtlassianLicenses' and 'options withDataInsights'."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    export_type: str
    """The type of data to export."""
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

# Variants for getApp
@dataclass
class GetAppOptions:
    """Optional parameters for action getApp"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    include_archived: bool|None = None
    """Include archived apps if authorized."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetApp(MarketplaceCommand):
    """Get app detail information. Use app key or vendor and app name."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
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
    def supports_output_type() -> bool:
        return True

# End Variants for getApp

# Variants for getAppFeedbackList
@dataclass
class GetAppFeedbackListOptions:
    """Optional parameters for action getAppFeedbackList"""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    type: str|None = None
    """Metric type or feedback type. Valid metric types are churn, conversions, and renewals. Valid feedback types are disable or uninstall."""
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
class GetAppFeedbackListGivenApp(MarketplaceCommand):
    """Get a list of feedback entries from customer's disabling or uninstalling a specific app or all apps for a vendor. Optionally, filter with regex on the feedback message and using the type and hosting parameters. Additional options are available with --options includeAnonymous and --options reason=... with valid reasons: being bugs, cost, functionality, interface, other, reenabling, reinstalling, usefulness."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    options: GetAppFeedbackListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAppFeedbackList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

@dataclass
class GetAppFeedbackListGivenVendor(MarketplaceCommand):
    """Get a list of feedback entries from customer's disabling or uninstalling a specific app or all apps for a vendor. Optionally, filter with regex on the feedback message and using the type and hosting parameters. Additional options are available with --options includeAnonymous and --options reason=... with valid reasons: being bugs, cost, functionality, interface, other, reenabling, reinstalling, usefulness."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    options: GetAppFeedbackListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAppFeedbackList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAppFeedbackList

# Variants for getAppList
@dataclass
class GetAppListOptions:
    """Optional parameters for action getAppList"""
    last_updated: str|None = None
    """Filter list by only including items who's last updated date was on or after the specified date."""
    include_archived: bool|None = None
    """Include archived apps if authorized."""
    include_private: bool|None = None
    """Include private apps if authorized."""
    exclude_public: bool|None = None
    """Exclude public apps. Use this together with includePrivate to list only private apps."""
    only_atlassian_paid: bool|None = None
    """Only include apps that are Atlassian paid on app lists."""
    application: str|None = None
    """Search filtering on application. Available applications are: Jira, ServiceDesk, Confluence, Bitbucket, Crucible, Bamboo, Crowd."""
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
class GetAppListGivenVendor(MarketplaceCommand):
    """List of app for a specific vendor or from a search with regex filtering on app name or key. The includePrivate and excludePublic flags provide additional filtering options. For more advanced searches, there are additional filtering capabilities available including by application and by hosting."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
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

@dataclass
class GetAppListGivenSearchType(MarketplaceCommand):
    """List of app for a specific vendor or from a search with regex filtering on app name or key. The includePrivate and excludePublic flags provide additional filtering options. For more advanced searches, there are additional filtering capabilities available including by application and by hosting."""
    search_type: str
    """Type of app search. Defaults to BRIEF to get up to 10 matches. Valid values are brief, all, rating, trending, sales, new."""
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

@dataclass
class GetAppListGivenSearch(MarketplaceCommand):
    """List of app for a specific vendor or from a search with regex filtering on app name or key. The includePrivate and excludePublic flags provide additional filtering options. For more advanced searches, there are additional filtering capabilities available including by application and by hosting."""
    search: str
    """Search string."""
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

# Variants for getAppPrivacyAndSecurity
@dataclass
class GetAppPrivacyAndSecurityOptions:
    """Optional parameters for action getAppPrivacyAndSecurity"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    include_archived: bool|None = None
    """Include archived apps if authorized."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetAppPrivacyAndSecurity(MarketplaceCommand):
    """Get app detail privacy and security information in JSON format. Use app key or vendor and app name."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    options: GetAppPrivacyAndSecurityOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAppPrivacyAndSecurity"

# End Variants for getAppPrivacyAndSecurity

# Variants for getAppReviewList
@dataclass
class GetAppReviewListOptions:
    """Optional parameters for action getAppReviewList"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
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
class GetAppReviewList(MarketplaceCommand):
    """Deprecated. Use getReviewList instead."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    options: GetAppReviewListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAppReviewList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAppReviewList

# Variants for getApplicationList
@dataclass
class GetApplicationListOptions:
    """Optional parameters for action getApplicationList"""
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
class GetApplicationList(MarketplaceCommand):
    """List of Marketplace applications with regex filtering on name."""
    options: GetApplicationListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getApplicationList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getApplicationList

# Variants for getAsset
@dataclass
class GetAssetOptions:
    """Optional parameters for action getAsset"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetAsset(MarketplaceCommand):
    """Get Marketplace asset details by the unique asset name. For example, the name returned from addAsset."""
    name: str
    """Contact display name."""
    options: GetAssetOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getAsset"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getAsset

# Variants for getInstallHistoryList
@dataclass
class GetInstallHistoryListOptions:
    """Optional parameters for action getInstallHistoryList"""
    type: str|None = None
    """Metric type or feedback type. Valid metric types are churn, conversions, and renewals. Valid feedback types are disable or uninstall."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is since the beginning."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
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
class GetInstallHistoryList(MarketplaceCommand):
    """Get weekly install count history for an app. By default, the list will be active installs. History is ordered by date descending. Use type to subdivide counts by app version or host application version. Valid types are: active, appVersion, applicationVersion, applicationMajorVersion, applicationMinorVersion. The limit parameter controls the number of history entries in subdivision set."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    options: GetInstallHistoryListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getInstallHistoryList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getInstallHistoryList

# Variants for getLicense
@dataclass
class GetLicenseOptions:
    """Optional parameters for action getLicense"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetLicense(MarketplaceCommand):
    """Get license details by id lookup."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    license_id: str
    """License id also known as a SEN for support entitlement number."""
    options: GetLicenseOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getLicense"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getLicense

# Variants for getLicenseList
@dataclass
class GetLicenseListOptions:
    """Optional parameters for action getLicenseList"""
    last_updated: str|None = None
    """Filter list by only including items who's last updated date was on or after the specified date."""
    app: str|None = None
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    search: str|None = None
    """Search string."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is since the beginning."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
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
class GetLicenseList(MarketplaceCommand):
    """List of licenses with optional selection by app key, hosting type, text search, start date, end date, and regex filtering on company, contact name, or email. Plain text search is done against license fields as defined by Marketplace - license id, customer information and partner information. Start and end date filtering as defined by Marketplace appears to be by maintenance start date. Use '--options includeAtlassianLicenses' to include Atlassian generated licenses."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    options: GetLicenseListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getLicenseList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getLicenseList

# Variants for getPrice
@dataclass
class GetPriceOptions:
    """Optional parameters for action getPrice"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    category: str|None = None
    """Pricing category. Either live or pending. Defaults to live except setPrice defaults to pending."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetPrice(MarketplaceCommand):
    """Get price information for an app."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    edition: str
    """Price edition. ExamHosting type - either server or cloud. Defaults to server."""
    options: GetPriceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPrice"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPrice

# Variants for getPriceList
@dataclass
class GetPriceListOptions:
    """Optional parameters for action getPriceList"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    category: str|None = None
    """Pricing category. Either live or pending. Defaults to live except setPrice defaults to pending."""
    include_private: bool|None = None
    """Include private apps if authorized."""
    exclude_public: bool|None = None
    """Exclude public apps. Use this together with includePrivate to list only private apps."""
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
class GetPriceList(MarketplaceCommand):
    """List of price tier entries for an app with regex selection on edition. You can use @all for the app parameter together with the includePrivate and excludePublic filtering options. You can use @all for the hosting parameter, otherwise it will default to a hosting used by app of either server, cloud, or datacenter."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    options: GetPriceListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPriceList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPriceList

# Variants for getPricingInfo
@dataclass
class GetPricingInfoOptions:
    """Optional parameters for action getPricingInfo"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    category: str|None = None
    """Pricing category. Either live or pending. Defaults to live except setPrice defaults to pending."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetPricingInfo(MarketplaceCommand):
    """Get information about pricing setting and status for an app."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    options: GetPricingInfoOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPricingInfo"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPricingInfo

# Variants for getPromotionCodeAppList
@dataclass
class GetPromotionCodeAppListOptions:
    """Optional parameters for action getPromotionCodeAppList"""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
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
class GetPromotionCodeAppList(MarketplaceCommand):
    """Get a list of apps and related information associated with a promotion code. Identify a promotion by promotion id or a promotion name and hosting parameter for lookup. By default, all code and app combinations will be listed. Filter by a code using '--options code=...'. Filter by partial app key using the app parameter. Note that app key listed may contain a qualifier of '.cloud' or '.data-center'. Use '--options includeInactive' to include inactive promotions when doing name lookup by promotion name."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    promotion: str
    """Promotion name or id. Promotion names are not unique. The most recent promotion with name will be used. Use an id to get a more specific promotion. Ids are available using getPromotionList."""
    options: GetPromotionCodeAppListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPromotionCodeAppList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPromotionCodeAppList

# Variants for getPromotionCodeList
@dataclass
class GetPromotionCodeListOptions:
    """Optional parameters for action getPromotionCodeList"""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
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
class GetPromotionCodeList(MarketplaceCommand):
    """Get a list of promotion codes for a promotion using a promotion id or a promotion name and hosting parameter for lookup. Use '--options includeInactive' to include inactive promotions when doing name lookup by promotion name."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    promotion: str
    """Promotion name or id. Promotion names are not unique. The most recent promotion with name will be used. Use an id to get a more specific promotion. Ids are available using getPromotionList."""
    options: GetPromotionCodeListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPromotionCodeList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPromotionCodeList

# Variants for getPromotionList
@dataclass
class GetPromotionListOptions:
    """Optional parameters for action getPromotionList"""
    app: str|None = None
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
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
class GetPromotionList(MarketplaceCommand):
    """Get a list of promotions for a specific vendor and hosting with regex filtering on promotion name. Additional optional filtering by app key. Other filtering options can also be provided using the options parameter like '--options status=ACTIVE'. Promotions are returned ordered by start date descending. Use '--options reverse' to order by start date ascending. Use '--options includeInactive' to include inactive promotions in the list."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    hosting: str
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    options: GetPromotionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getPromotionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getPromotionList

# Variants for getReview
@dataclass
class GetReviewOptions:
    """Optional parameters for action getReview"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetReview(MarketplaceCommand):
    """Get a customer review for an app."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    review_id: str
    """Unique id for a review."""
    options: GetReviewOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getReview"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getReview

# Variants for getReviewList
@dataclass
class GetReviewListOptions:
    """Optional parameters for action getReviewList"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
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
class GetReviewList(MarketplaceCommand):
    """Get a list of customer reviews for an app with regex filtering by author name, review, and response. By default, reviews are sorted by most recent first. Use '--options sort=helpful' to sort by most helpful first."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    options: GetReviewListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getReviewList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getReviewList

# Variants for getSalesMetricList
@dataclass
class GetSalesMetricListOptions:
    """Optional parameters for action getSalesMetricList"""
    type: str|None = None
    """Metric type or feedback type. Valid metric types are churn, conversions, and renewals. Valid feedback types are disable or uninstall."""
    app: str|None = None
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is since the beginning."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
    options_: Iterable[str]|str|None = None
    """Client or action specific advanced options. Use multiple times for multiple option settings or a comma separated list."""
    limit: str|None = None
    """Maximum number of list entries to return. Some actions or environments may impose a smaller default limit."""
    regex: str|None = None
    """Regular expression for condition matching or list filtering."""
    columns: str|None = None
    """Column selection and ordering when action generates CSV output. A comma separated list of column numbers (1-based) or column names (case insensitive). Only columns provided by the selected outputFormat are available for selection. Invalid columns will be ignored."""
    select: Iterable[str]|str|None = None
    """Used for row selection by column value on list actions. The first colon (:) in the parameter value delineates the column name or number from a regex selection pattern. Each row's column value is used with the regex pattern to determined row inclusion in the final result. By default, row is included if the regex pattern is found in the column value. The options parameter can be set to one or more of the following to modify the default behavior: literal - to treat the regex string as a literal string, exact - to require an exact match of the value (not just a find!), negative - to reverse the condition so a match means exclude the row. Row selection takes place after all other action specific filtering conditions including the limit determination and so generally should not be used with the limit parameter."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetSalesMetricList(MarketplaceCommand):
    """Get a list of sales metrics like churn, renewals, and conversions for a specific vendor with regex filtering on app name or key. Filter to a specific app by providing the app key or name using the app parameter. Additional filtering by date is supported using the startDate and endDate parameters. By default, entire history is returned. Data is aggregated by month by default. Specify --options aggregation=week for week based aggregation. Use the type parameter to specify the metric type, otherwise, information for all types will be shown. Valid types are churn, conversions, and renewals. Metrics are returned starting with a special value of @all for app representing total across all vendor apps. The limit parameter, in this case, is the number of applications to list. Currently, Atlassian only provides these metrics for Cloud apps."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    options: GetSalesMetricListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getSalesMetricList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getSalesMetricList

# Variants for getTransaction
@dataclass
class GetTransactionOptions:
    """Optional parameters for action getTransaction"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetTransaction(MarketplaceCommand):
    """Get transaction details by id lookup."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    transaction_id: str
    """Transaction id. Normally looks like AT-12345678"""
    options: GetTransactionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getTransaction"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getTransaction

# Variants for getTransactionList
@dataclass
class GetTransactionListOptions:
    """Optional parameters for action getTransactionList"""
    last_updated: str|None = None
    """Filter list by only including items who's last updated date was on or after the specified date."""
    app: str|None = None
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    search: str|None = None
    """Search string."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is since the beginning."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
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
class GetTransactionList(MarketplaceCommand):
    """List of transactions with optional selection by app key, hosting type, text search, start date, end date, and regex filtering on company, contact name, or email. Plain text search is done against transaction fields as defined by Marketplace - transaction id, license id, customer information, and partner information. Start and end date filtering is defined by Marketplace and appears to be by sale date."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    options: GetTransactionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getTransactionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getTransactionList

# Variants for getVendor
@dataclass
class GetVendorOptions:
    """Optional parameters for action getVendor"""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""

@dataclass
class GetVendor(MarketplaceCommand):
    """Get vendor detail information."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    options: GetVendorOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getVendor"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getVendor

# Variants for getVendorContactList
@dataclass
class GetVendorContactListOptions:
    """Optional parameters for action getVendorContactList"""
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
class GetVendorContactList(MarketplaceCommand):
    """List of vendor contacts with regex filtering on name or display name."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    options: GetVendorContactListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getVendorContactList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getVendorContactList

# Variants for getVendorList
@dataclass
class GetVendorListOptions:
    """Optional parameters for action getVendorList"""
    has_public_apps: bool|None = None
    """List only vendors that have at least one public app. Adds app summary statistics to list entry."""
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
class GetVendorList(MarketplaceCommand):
    """List of vendors with regex filtering on name. Use '--options own' to include only vendors user is associated with. Use '--options text=...' to include only vendor who's name is a simple, case-insensitive text match. Note it is a performance advantage to use own or a text match in some cases. Also, we attempt to filter out invalid or private vendors that do not have other details available, some may be listed with output format 1, however, these will not appear for output format > 1."""
    options: GetVendorListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getVendorList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getVendorList

# Variants for getVersion
@dataclass
class GetVersionOptions:
    """Optional parameters for action getVersion"""
    version: str|None = None
    """App version name or numeric key (build number). Defaults to @latest. The key is a unique identifier and defines version ordering."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    output_type: str|None = None
    """CSV output from get list actions and pretty print output from get actions can optionally be converted to plain text, HTML, or json based on the value of this parameter. Output type slack will send a message to a slack channel specified by the channel parameter using a slack client configuration entry named 'slack' by default or a different site name by using '--options site=slack...'. Get actions also support the variables output type to set replacement variables for use in a ACLI run script. Valid values are: text, table, html, json, variables, slack."""
    file: str|None = None
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    append: bool|None = None
    """For some actions using the file parameter, append will append output to an existing file."""
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    output_format: str|None = None
    """Specify output format for list actions. Output format determines what columns are retrieved for the list. More columns usually take longer to retrieve."""

@dataclass
class GetVersion(MarketplaceCommand):
    """Get app version detail information. Version defaults to latest if not specified. Hosting defaults to all hosting types."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    options: GetVersionOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getVersion"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getVersion

# Variants for getVersionList
@dataclass
class GetVersionListOptions:
    """Optional parameters for action getVersionList"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    include_private: bool|None = None
    """Include private apps if authorized."""
    exclude_public: bool|None = None
    """Exclude public apps. Use this together with includePrivate to list only private apps."""
    only_atlassian_paid: bool|None = None
    """Only include apps that are Atlassian paid on app lists."""
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
class GetVersionList(MarketplaceCommand):
    """List of app versions for a specific app with regex filtering on version name or key. The includePrivate and excludePublic flags provide additional filtering options. You can use @all for the app parameter with some filtering: onlyAtlassianPaid filtering option and include only app lastUpdated on or after the lastUpdated parameter."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    options: GetVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "getVersionList"
    @staticmethod
    def supports_output_type() -> bool:
        return True

# End Variants for getVersionList

# Variants for removeAsset
@dataclass
class RemoveAssetOptions:
    """Optional parameters for action removeAsset"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveAsset(MarketplaceCommand):
    """Remove Marketplace asset by name."""
    name: str
    """Contact display name."""
    options: RemoveAssetOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeAsset"

# End Variants for removeAsset

# Variants for removeVendorContact
@dataclass
class RemoveVendorContactOptions:
    """Optional parameters for action removeVendorContact"""
    continue_: bool|None = None
    """Continue processing even after errors are encountered for run actions. Also used for some action to ignore certain errors like not found errors on remove actions and already exists errors on add actions."""

@dataclass
class RemoveVendorContact(MarketplaceCommand):
    """Remove a vendor contact by name or id."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    name: str
    """Contact display name."""
    options: RemoveVendorContactOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "removeVendorContact"

# End Variants for removeVendorContact

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
    encoding: str|None = None
    """Character encoding (character set) for text based file content - must be an encoding supported by your Java platform."""
    find_replace: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""
    find_replace_regex: Iterable[str]|str|None = None
    """Successively find and replace matching text with the find and replace values specified using find:replace syntax. The first colon (:) delineates the find value from the replace value. Single quote values containing a colon and then escape embedded quotes. The find value must be a valid regular regular expression and the replace value can contain replacement variables for capture groups like $1, $2, and so on. For some command shells, the $ may need to be escaped. Legacy support for a comma separated list deprecated in 9.0 has been removed in 9.3. You must now always use multiple parameters."""

@dataclass
class RenderRequest(MarketplaceCommand):
    """Render URL based request. URL can be a partial Marketplace URL. The response data modified by optional findReplace processing is returned. Use '--pretty' to format returned JSON data in a more readable form."""
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
    last_updated: str|None = None
    """Filter list by only including items who's last updated date was on or after the specified date."""
    include_archived: bool|None = None
    """Include archived apps if authorized."""
    include_private: bool|None = None
    """Include private apps if authorized."""
    exclude_public: bool|None = None
    """Exclude public apps. Use this together with includePrivate to list only private apps."""
    only_atlassian_paid: bool|None = None
    """Only include apps that are Atlassian paid on app lists."""
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
class RunFromAppListGivenVendorAndInput(MarketplaceCommand):
    """Run actions for each app with optional filtering equivalent to getAppList including regex on app name or key."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
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
class RunFromAppListGivenVendorAndCommon(MarketplaceCommand):
    """Run actions for each app with optional filtering equivalent to getAppList including regex on app name or key."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
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
class RunFromAppListGivenVendorAndFile(MarketplaceCommand):
    """Run actions for each app with optional filtering equivalent to getAppList including regex on app name or key."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
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

@dataclass
class RunFromAppListGivenSearchTypeAndInput(MarketplaceCommand):
    """Run actions for each app with optional filtering equivalent to getAppList including regex on app name or key."""
    search_type: str
    """Type of app search. Defaults to BRIEF to get up to 10 matches. Valid values are brief, all, rating, trending, sales, new."""
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
class RunFromAppListGivenSearchTypeAndCommon(MarketplaceCommand):
    """Run actions for each app with optional filtering equivalent to getAppList including regex on app name or key."""
    search_type: str
    """Type of app search. Defaults to BRIEF to get up to 10 matches. Valid values are brief, all, rating, trending, sales, new."""
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
class RunFromAppListGivenSearchTypeAndFile(MarketplaceCommand):
    """Run actions for each app with optional filtering equivalent to getAppList including regex on app name or key."""
    search_type: str
    """Type of app search. Defaults to BRIEF to get up to 10 matches. Valid values are brief, all, rating, trending, sales, new."""
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

@dataclass
class RunFromAppListGivenSearchAndInput(MarketplaceCommand):
    """Run actions for each app with optional filtering equivalent to getAppList including regex on app name or key."""
    search: str
    """Search string."""
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
class RunFromAppListGivenSearchAndCommon(MarketplaceCommand):
    """Run actions for each app with optional filtering equivalent to getAppList including regex on app name or key."""
    search: str
    """Search string."""
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
class RunFromAppListGivenSearchAndFile(MarketplaceCommand):
    """Run actions for each app with optional filtering equivalent to getAppList including regex on app name or key."""
    search: str
    """Search string."""
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

# Variants for runFromLicenseList
@dataclass
class RunFromLicenseListOptions:
    """Optional parameters for action runFromLicenseList"""
    last_updated: str|None = None
    """Filter list by only including items who's last updated date was on or after the specified date."""
    app: str|None = None
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    search: str|None = None
    """Search string."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is since the beginning."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
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
class RunFromLicenseListGivenVendorAndInput(MarketplaceCommand):
    """Run actions for each license with optional filtering equivalent to getLicenseList including regex on app name or key."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromLicenseListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromLicenseList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromLicenseListGivenVendorAndCommon(MarketplaceCommand):
    """Run actions for each license with optional filtering equivalent to getLicenseList including regex on app name or key."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromLicenseListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromLicenseList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromLicenseListGivenVendorAndFile(MarketplaceCommand):
    """Run actions for each license with optional filtering equivalent to getLicenseList including regex on app name or key."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromLicenseListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromLicenseList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromLicenseList

# Variants for runFromReviewList
@dataclass
class RunFromReviewListOptions:
    """Optional parameters for action runFromReviewList"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
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
class RunFromReviewListGivenAppAndInput(MarketplaceCommand):
    """Run actions for each customer review of an app with optional filtering and ordering similar to getReviewList."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromReviewListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromReviewList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromReviewListGivenAppAndCommon(MarketplaceCommand):
    """Run actions for each customer review of an app with optional filtering and ordering similar to getReviewList."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromReviewListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromReviewList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromReviewListGivenAppAndFile(MarketplaceCommand):
    """Run actions for each customer review of an app with optional filtering and ordering similar to getReviewList."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromReviewListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromReviewList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromReviewList

# Variants for runFromTransactionList
@dataclass
class RunFromTransactionListOptions:
    """Optional parameters for action runFromTransactionList"""
    last_updated: str|None = None
    """Filter list by only including items who's last updated date was on or after the specified date."""
    app: str|None = None
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    search: str|None = None
    """Search string."""
    start_date: str|None = None
    """Earliest date for date filtering. Default is since the beginning."""
    end_date: str|None = None
    """Latest date for date filtering. Defaults to now."""
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
class RunFromTransactionListGivenVendorAndInput(MarketplaceCommand):
    """Run actions for each transaction with optional filtering equivalent to getTransactionList including regex on app name or key."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromTransactionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTransactionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromTransactionListGivenVendorAndCommon(MarketplaceCommand):
    """Run actions for each transaction with optional filtering equivalent to getTransactionList including regex on app name or key."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromTransactionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTransactionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromTransactionListGivenVendorAndFile(MarketplaceCommand):
    """Run actions for each transaction with optional filtering equivalent to getTransactionList including regex on app name or key."""
    vendor: str
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromTransactionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromTransactionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromTransactionList

# Variants for runFromVendorList
@dataclass
class RunFromVendorListOptions:
    """Optional parameters for action runFromVendorList"""
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
class RunFromVendorListGivenInput(MarketplaceCommand):
    """Run actions for each vendor with optional filtering the same as getVendorList."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromVendorListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromVendorList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromVendorListGivenCommon(MarketplaceCommand):
    """Run actions for each vendor with optional filtering the same as getVendorList."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromVendorListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromVendorList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromVendorListGivenFile(MarketplaceCommand):
    """Run actions for each vendor with optional filtering the same as getVendorList."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromVendorListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromVendorList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromVendorList

# Variants for runFromVersionList
@dataclass
class RunFromVersionListOptions:
    """Optional parameters for action runFromVersionList"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    hosting: str|None = None
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    include_private: bool|None = None
    """Include private apps if authorized."""
    exclude_public: bool|None = None
    """Exclude public apps. Use this together with includePrivate to list only private apps."""
    only_atlassian_paid: bool|None = None
    """Only include apps that are Atlassian paid on app lists."""
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
class RunFromVersionListGivenAppAndInput(MarketplaceCommand):
    """Run actions for each app version with optional filtering the same as getVersionList."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    input: Iterable[str]
    """Line of input used in place of file data for run actions. One or more input parameters are used as lines instead of using the file parameter. In some cases requiring a file parameter, it may be necessary to use a special value of + to indicate to use the input parameters instead."""
    options: RunFromVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromVersionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromVersionListGivenAppAndCommon(MarketplaceCommand):
    """Run actions for each app version with optional filtering the same as getVersionList."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    common: str
    """Common parameter string added to all actions in the run script."""
    options: RunFromVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromVersionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

@dataclass
class RunFromVersionListGivenAppAndFile(MarketplaceCommand):
    """Run actions for each app version with optional filtering the same as getVersionList."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    file: str
    """Path to file based content or result output. For some action it may be a directory path. Use - for standard input. Use + for getting lines from 'input' parameters (deprecated)."""
    options: RunFromVersionListOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "runFromVersionList"
    @staticmethod
    def has_replacement_vars() -> bool:
        return True

# End Variants for runFromVersionList

# Variants for setPrice
@dataclass
class SetPriceOptions:
    """Optional parameters for action setPrice"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    field: Iterable[str]|str|None = None
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    category: str|None = None
    """Pricing category. Either live or pending. Defaults to live except setPrice defaults to pending."""

@dataclass
class SetPrice(MarketplaceCommand):
    """Set prices for an app for a hosting type defined for the app. Each hosting type defines specific unit count levels that must be set to a valid amount of US dollars (USD). The amount is for a commercial license. Atlassian calculates other license amounts from this value. Use field parameters to map units to amounts for all required unit counts. Price settings default to pending category. Expert discount is enabled by default. Use '--options expertDiscountOptOut' to avoid the default."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    hosting: str
    """Hosting type, one of server, cloud, or datacenter. As filter criteria, the default is @all. For pricing selection only server and cloud are valid and the default is server."""
    options: SetPriceOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "setPrice"

# End Variants for setPrice

# Variants for updateFields
@dataclass
class UpdateFieldsOptions:
    """Optional parameters for action updateFields"""
    vendor: str|None = None
    """Vendor name or numeric vendor id referred to as the vendor key. Recommend using the numeric vendor key where possible as it saves an expensive name lookup. The key is a unique identifier."""
    version: str|None = None
    """App version name or numeric key (build number). Defaults to @latest. The key is a unique identifier and defines version ordering."""

@dataclass
class UpdateFields(MarketplaceCommand):
    """Update app or version fields. Support setting string values for existing fields. One or more field parameters provide the JSON location to be updated and its value using 'location=value' syntax where the location is a JSON pointer (https://www.baeldung.com/json-pointer). For simple locations, think of it as a path through the json like '\tagline' for an app or '/vendorLinks/documentation' for an app version. An example is --field /vendorLinks/documentation=https://appfire.atlassian.net/wiki/display/MCLI. Use getApp or getVersion with '--outputType json --pretty' to see the JSON structure."""
    app: str
    """App name or key or partial key. Key or app key is another term for the older Atlassian plugin or add-on key. The key is a unique identifier."""
    field: Iterable[str]
    """Use to set client and construct specific fields or variables using name=value syntax. The first equal sign (=) delineates the name from it's value. This provides a more convenient and expandable alternative for setting fields or variables and is the recommended approach. Values are trimmed unless single quoted and single quoted strings will have single quotes removed."""
    options: UpdateFieldsOptions | None = None
    """ Action specific options """
    logging_options: LoggingOptions | None = None
    """ Logging options """
    common_options: CommonOptions | None = None
    """ Common options """

    @staticmethod
    def action():
        return "updateFields"

# End Variants for updateFields
