sublime_open_highlighted_path
=============================

Sublime Text plugin/shortcut to open the file path that is currently under the cursor.

You basically, place the cursor on a path or portion of a path to a file in a view,
the plugin will try to find the path using four different methods:

1. Is the path a path to an existant file in it's own right?
2. Using the currently open files and their paths, can we find files that match the path under the cursor?
3. Using the current project and it's paths, can we find the files that match the path under the cursor?
4. Using the supplied base paths from the settings, can we find the files that match the path under the cursor?

If more than one file is found you will be presented with the options to select from.


## Installation:


### Git

Clone this repository into your Sublime Text *Packages* directory.

    git clone https://github.com/sligodave/sublime_open_highlighted_path.git OpenHighlightedPath


## Configure:

### Settings file:

In the file:

Packages/User/OpenHighlightedPath.sublime-settings

You probably won't need to change the "delimiters", they are used to identify the path when a cursor is placed in a path, rather than a path being selected.

```json
{
    // Characters that signal the start or end of a path.
    // If these aren't set, the start and end of the line is used.
    "delimiters": " '\"",
    // List of other paths to use as a base path when trying to find a file
    "base_directories": [
    ],
    // Don't test if supplied path is actually a path in it's own right
    "exclude_literal": false,
    // Don't test path based on currently opened files
    "exclude_current": false,
    // Don't test path based on projects directories
    "exclude_project": false
}
```


### Project file:

In your current project file, you can also add aliases:

```json
{
	"folders":
	[
		{
		}
	],
	"open_highlighted_path":
	{
		// Characters that signal the start or end of a path.
		// If these aren't set, the start and end of the line is used.
		"delimiters": " '\"",
		// List of other paths to use as a base path when trying to find a file
		"base_directories": [
		],
		// Don't test if supplied path is actually a path in it's own right
		"exclude_literal": false,
		// Don't test path based on currently opened files
		"exclude_current": false,
		// Don't test path based on projects directories
		"exclude_project": false
	}
}
```


## Usage:

### With GoTo Anywhere command:

    "Open Highlighted Path"


### Keyboard shortcuts:

OSX/Linux/Windows

```json
[
	{ "keys": ["ctrl+alt+p"], "command": "open_highlighted_path" }
]
```


## Issues and suggestions:

Fire on any issues or suggestions you have.


## Copyright and license
Copyright 2013 David Higgins

[MIT License](LICENSE)
