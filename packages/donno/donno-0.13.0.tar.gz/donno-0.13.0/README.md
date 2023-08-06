# Donno

A simple note-take CLI application.

## Features

* Easy note management: add, update, list, remove note;
* Organize notes in hierarchical notebooks;
* Full featured formating support: you can add rich texts (markdown),
  mathematical formula (mathjax, LaTeX), images, attachments, ...
  All will be rendered and displayed lively in your browser
  through [pandoc](https://pandoc.org/);
* Powerful and fast full-text search. Get all information at your fingers;
* Safe and secure: all notes are saved in plain texts (markdown). You own your data.
  You can view and update your notes without any specific applications
  but a text editor when necessary. All notes store in private git repository;
* Live in console: git style APIs. No need to learn a new GUI app.
  Get your notes anytime, anywhere: Linux, macOS, Windows (through WSL),
  Android (by Termux), SSH, ...

## Install

`pip install donno`

## Usage

```
don add        # create a new note
don list       # list notes in all notebooks
don list-notebooks    # list existing notebooks in alphabet order
don search nim thunder    # search notes contains "nim" and "thunder"
don edit 3     # edit note #3 in note list or searching results
don delete 3   # delete note #3 in note list or searching results
don backup     # backup notes to remote repository
don restore    # restore notes from remote repository
don preview 3  # preview note #3 in console editor
don pv 3       # preview note #3 in browser
don ads -b Tech -n nim -t config -c compile  # advanced search, see below for explanations
don s '(python.*program|learning.*algorithm)'  # search notes with regex, see below for explanations
don publish    # publish notes to blog
```

Note:

* Most long commands have aliases (abbreviation) for convenience.
  For example, `a` for add, `l` for list, `s` for search,
  `ads` for `advanced-search`, etc. Get alias of a command with `-h` option.
* The command options have 2 forms: full and abbreviation.
  For example, in command `ads`, `-b` is the abbr. of `--book`,
  `-t`: `--tag`, `-n`: `--name`, etc.
* To use `pv` command, [pandoc](https://pandoc.org/) and a browser is necessary.
  Install pandoc on Debian/Ubuntu/Mint with `apt install pandoc`.

## Add attachments in a note

You can add attachments in your notes.
They could be image files, which are added by `![<image-file-name>]()`,
or other files, which are added by  `[<attachment-file-name>]()`
(without exclamation mark ahead, like common markdown links).

The attachment file specified in the link must exist in the folder you add the
note (the folder you run `don a`),
or "attachment file not exists" error will be raised.

### Under the hood

When you save a note and quit the editor,
donno will scan all `[<filename>]()` pattern in the note.
If the <filename>s exist in the current folder,
donno do the following things:

1. Generate a <internal-name> for each attachment;
1. Copy each file to <notes-repo>/resources folder (get the path of
   <notes-repo> with `don conf get repo`)
   with their <internal-name>s;
1. Update the link in the note from `[<filename>]()` to `[<filename>](<internal-name>)`

The <internal-name> is composed of 5 parts:

1. Prefix `resources/`, for all attachments are saved in this folder in <notes-repo>
1. <note-name>
1. `att`
1. Order number
1. File extension of original file

For example, if you add the following attachments in the note with filename
*note201118140711.md*:
```
![myimage.png]()
[mydoc.pdf]()
```

They  will be updated to:
```
![myimage.png](resources/note201118140711att1.png)
[mydoc.pdf](resources/note201118140711att2.pdf)
```

If the attachment file doesn't exist in the current folder,
donno will give a warning:
```
File myimage.png does not exist in the current folder.
You can run `don e ...` at the folder where myimage.png exists.
```

## Configuration

File path: ~/.config/donno/config.json

### Configuration Items

#### General

* app_home: root folder of donno data files. Default: ~/.donno
* repo: folder to save all note files and resource files. Default: $app_home/repo
* editor: which application to use to create/update note. Default: `nvim`
* viewer: which application to use to view notes in console. Default: `nvim -R`
* default_notebook: default notebook name for a new note. Default: `/Diary`
* logging level: debug or info(default)
* editor_envs: environment variables of the editor. For example,
  env `XDG_CONFIG_HOME` is used by neovim to load config/plugins to parse markdown files.
  Default: `~/.config`

#### Blog

* url: blog url
* publish_cmd: command to publish notes to blog

### Manage Configurations

```
don conf get                # list all current configurations
don conf get edtior         # get which editor to use
don conf set editor nvim    # set the editor, make sure you've installed it
don conf set default_notebook /Diary/2020

# set nested attribute:
don conf set editor_envs.XDG_CONFIG_HOME $HOME/Documents/sources/vimrcs/text

# restore default values of configurations:
don conf restore
```

## Update and uninstall

```
pip install --upgrade donno
pip uninstall donno
```

## Import & Export between Other Note-taking Apps

Supported import formats:

* Joplin

Supported export formats:

* JSON
* markdown

Examples:

Import notes from Joplin:
```
jop export --format json jopdb
don imports jopdb --source-type joplin
```

Export notes as JSON files and save into folder *donno_export*:
```
don exports --type json
```

List parameters with `don export -h` and `don import -h`.

## Advanced search

To search notes with more details, use *advanced-search* command.
For example, to search notes in notebook *Tech*, and "nim" in title,
"config" in tags, "compile" in contents:
```
don ads -b Tech -n nim -t config -c compile
```

which is abbreviation form of:
```
don advanced-search --book Tech --name nim --tag config --content compile
```

You can also use regex in search term.
For example, to search notes contains "python...program" *or* "learning...algorithm":
```
don s '(python.*program|learning.*algorithm)'
```

## Some notes

### Install in virtual environment

For those who don't want install apps in global environment,
install it in a virtual environment:
```
mkdir ~/apps/donno
cd ~/apps/donno
python -m venv env
. env/bin/activate
pip install donno

cat << EOF >> ~/.zshrc
function dn() {
  source $HOME/apps/donno/env/bin/activate
  don $@
  deactivate
}
EOF
```

Now the command is `dn` instead of `don`.

## Roadmap

### In developing

1. Advanced search function: search by title, tag, notebook and content

1. Search with regular expression

### On schedule

1. Basic publishing module: publish to blog, such as github.io

1. Advanced publishing function: publish specific note, or notes in specific notebook

### Completed

1. Basic note-taking functions: add, delete, list, search, view, update notes

1. Configuration module: see [Configuration](#configuration);

1. Preview: render markdown notes to HTML and previewed in browser

1. Support adding attachments into notes, especially images

1. Add logging system, distinguish application (for end user) and debugging (for developer) logs

1. Notebook management: list notebooks, list notes in specified notebook

1. Synchronize notes between hosts (based on VCS, such as git)

1. Import/Export from/to other open source note-taking apps,
   such as [Joplin](https://joplinapp.org/)

