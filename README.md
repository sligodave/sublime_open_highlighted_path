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


