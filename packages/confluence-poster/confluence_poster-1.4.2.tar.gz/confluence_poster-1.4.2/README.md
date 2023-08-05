# Description

Supplementary script for writing Confluence articles in
local editor. Uses information from the config to post the article content to Confluence.

May be used either on its own:

    $ confluence_poster post-page

Or as a filter:

    $ cat file.md | confluence_poster --file-format markdown post-page

# Getting started

## Installation

1. Install the project from PyPI:

    ```console
    $ pip install confluence-poster
    ```

2. Create the config manually
([sample available in repo](https://github.com/VTimofeenko/confluence_poster/blob/master/config.toml)) or run `confluence_poster create-config` to run a configuration wizard

Alternatively, install `app-text/confluence_poster` from [nitratesky overlay](https://github.com/VTimofeenko/nitratesky).

## Sample usage

User edits the page text and keeps it in file `page1.md`.
Two files `attachment1.docx` and `attachment2.docx` need to be attached to the page.

Given the following files in the current directory:

```
├── attachment1.docx
├── attachment2.png
├── poster_config.toml
└── page1.md
```

`poster_config.toml` contains:

```toml
[pages]
[pages.page1]
page_title = "Some page"
page_file = "page1.md"
page_space = "SPACE"
```

config inside `${HOME}/.config/confluence_poster/` contains the authentication information and the Confluence URL.

Running

```console
$ confluence_poster --config poster_config.toml post-page --upload-files attachment1.docx attachment2.png
```

will attempt to locate the page on Confluence, update its content with the text in `page1.md` and attach the files to it.

If the script cannot locate the page by title, it will prompt the user to create it, optionally under a parent page.

# Details

**Usage**:

```console
$ confluence_poster [OPTIONS] COMMAND [ARGS]...
```

**General Options**:

* `--version`: Show version and exit.
* `--config PATH`: The file containing configuration. If not specified - config.toml from the same directory is used  [default: config.toml]
* `--page-title TEXT`: Override page title from config. Applicable if there is only one page.
* `--parent-page-title TEXT`: Provide a parent title to search for. Applicable if there is only one page.
* `--page-file PATH`: Provide the path to the file containing page text. Allows passing '-' to read from stdin.
* `--password TEXT`: Supply the password in command line.  [env var: CONFLUENCE_PASSWORD]
* `--force`: Force overwrite the pages. Skips all checks for different author of the updated page. To set for individual pages you can specify field 'force_overwrite' in config.
* `--force-create`: Disable prompts to create pages. Script could still prompt for a parent page.
* `--minor-edit`: Do not notify watchers of pages updates. Not enabled by default.
* `--report`: Print report at the end of the run. Not enabled by default.
* `--debug`: Enable debug logging. Not enabled by default.
* `--quiet`: Suppresses certain output.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

These options can be specified for any `COMMAND` except for  `create-config` which ignores these options.

**Commands**:

* `convert-markdown`: Converts single page text to html.
* `create-config`: Runs configuration wizard.
* `post-page`: Posts the content of the pages.
* `validate`: Validates the provided settings.

# Commands
## `confluence_poster post-page`

Posts the content of the pages.

**Usage**:

```console
$ confluence_poster post-page [OPTIONS] [FILES]...
```

**Options**:

* `--upload-files`: Upload list of files.
* `--version-comment TEXT`: Provider version comment.
* `--create-in-space-root`: Create the page in space root.
* `--file-format [confluencewiki|markdown|html|None]`: File format of the file with the page content. If provided at runtime - can only be applied to a single page. If set to 'None'(default) - script will try to guess it during the run.
* `--help`: Show this message and exit.

## `confluence_poster validate`

Validates the provided settings. If 'online' flag is passed - tries to fetch the space from the config using the
supplied credentials.

**Usage**:

```console
$ confluence_poster validate [OPTIONS]
```

**Options**:

* `--online`: Test the provided authentication settings on the actual instance of Confluence.
* `--help`: Show this message and exit.

## `confluence_poster create-config`

Runs configuration wizard. The wizard guides through setting up values for configuration file.

**Options**:

* `--local-only`: Create config only in the local folder.
* `--home-only`: Create config only in the $XDG_CONFIG_HOME.
* `--help`: Show this message and exit.


# Configuration file format

By default the confluence_poster tries to look for configuration file `config.toml` in the directory where it is invoked and in
$XDG_CONFIG_HOME. The format is as follows:

```toml
# If the page was not updated by the username specified here, throw an error.
# If this setting is omitted - username from auth section is used for checks.
author = "author_username"

[pages]
[pages.default]
# Space key. E.g. for space "local-dev" the space key is "LOC"
# Space defined here will be used if a page section below does not specify it
page_space = "DEFAULT_SPACE_KEY"
[pages.page1]
# The title of the page
page_title = "Some page title"
# The filename with page content
page_file = "some_file.confluencewiki"
# If specified - overrides the default page_space
page_space = "some_space_key"
# If specified as "true" - username check is always skipped for this page
force_overwrite = false
# If specified - the page will be created without looking for a parent under specified parent
page_parent_title = "Parent page title"
# If specified - script will convert the text in the file before posting it. If not specified - script will try to guess it based on file extension.
page_file_format = "confluencewiki"

[pages.page2]
page_title = "Some other page title"
page_file = "some_other_file.confluencewiki"

[auth]
# URL of Confluence instance
confluence_url = "https://confluence.local"
# Username for authentication
username = "confluence_username"
# Password may also be supplied through --password option or from an environment variable CONFLUENCE_PASSWORD
password = "confluence_password"
# Whether the Confluence instance is a "cloud" one
is_cloud = false

```

**Note on password and Cloud instances**: if Confluence instance is hosted by Atlassian, the password is the API token.
Follow instructions at [this link](https://confluence.atlassian.com/cloud/api-tokens-938839638.html).

# File formats

confluence_poster supports the following formats for posting pages:
* [Confluencewiki](https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html)
* Markdown
* Html

The format may be specified explicitly in the configuration file, passed during the runtime, or the script will try to guess it by the file extension.

# Contrib directory

There are shell completions for bash and zsh (generated through [typer](typer.tiangolo.com/)) as well as a sample of
[git post-commit hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

# See also

* [Vim confluencewiki syntax](https://www.vim.org/scripts/script.php?script_id=1994)
* [Paste confluence image in vim](https://github.com/VTimofeenko/confluencewiki-img-paste.vim)
* [Atlassian python API](https://atlassian-python-api.readthedocs.io/en/latest/) (On [Github](https://github.com/atlassian-api/atlassian-python-api))