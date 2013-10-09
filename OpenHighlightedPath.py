
import os.path
import sublime_plugin
import sublime


def get_setting(
    setting,
    default=None,
    window=None,
    settings_file='OpenHighlightedPath.sublime-settings',
    project_settings='open_highlighted_path',
    settings_only=False,
    project_only=False
):
    """
    FIXME: Maybe cache the settings,
    rather than getting them every time.
    """
    window = window if window else sublime.active_window()
    if not settings_only:
        settings = window.project_data()
        if settings and project_settings:
            settings = settings.get(project_settings)
        if settings and setting in settings:
            return settings.get(setting)
    if not project_only:
        settings = sublime.load_settings(settings_file)
        if settings and settings.has(setting):
            return settings.get(setting)
    return default


def find_path_from_others(path, others):
    """
    Break up all paths in others and see if we can
    file a file that exists when prepended to "path".
    """
    if path.startswith('/'):
        path = path[1:]
    hits = []
    for other in others:
        sep = '/' if other.find('/') != -1 else '\\'
        path_pieces = other.split(sep)
        so_far = '/'
        for path_piece in path_pieces:
            so_far = os.path.join(so_far, path_piece)
            temp_path = os.path.join(so_far, path)
            if os.path.exists(temp_path):
                hits.append(temp_path)
    return hits


class OpenHighlightedPathCommand(sublime_plugin.TextCommand):
    def run(self, edit, path=None):
        if path is None:
            # get the current line and the current column
            sel = self.view.sel()
            try:
                region = sel[0]
            except IndexError:
                return
            if region.a == region.b:
                point = region.a
                line = self.view.line(point)
                col = self.view.rowcol(point)[1]
                text = self.view.substr(line)
                # Get the path by walking left and right from the current cursor location
                path = ''
                delimiters = get_setting('delimiters', ' "\'')
                if text:
                    # Walk left from point to end of path
                    for i in range(col - 1, -1, -1):
                        character = text[i]
                        if delimiters.find(character) != -1:
                            break
                        path = '%s%s' % (character, path)
                    # Walk right from point to end of path
                    for i in range(col, len(text)):
                        character = text[i]
                        if delimiters.find(character) != -1:
                            break
                        path = '%s%s' % (path, character)
            else:
                path = self.view.substr(region)
            path = path.strip()

        self.hits = []

        if os.path.exists(path) and not get_setting('exclude_literal', False):
            self.hits.append(path)

        # Try to find file based on other open files
        if not get_setting('exclude_current', False):
            others = [x.file_name() for x in self.view.window().views() if x.file_name()]
            self.hits.extend(find_path_from_others(path, others))

        # Try to find file based on the current project
        if not get_setting('exclude_project', False):
            others = []
            for folder in get_setting('folders', [], project_settings=None, project_only=True):
                folder = folder.get('path', '')
                if folder:
                    others.append(folder)
            self.hits.extend(find_path_from_others(path, others))

        # Try to find file based on settings base directories
        self.hits.extend(find_path_from_others(path, get_setting('base_directories', [])))

        self.hits = list(set(self.hits))

        if not self.hits:
            sublime.status_message('Could not find file "%s"' % path)
        elif len(self.hits) == 1:
            self.open_file(0)
        else:
            self.view.window().show_quick_panel(
                self.hits,
                self.open_file,
                on_highlight=lambda x: self.open_file(x, sublime.TRANSIENT)
            )

    def open_file(self, selection, flags=0):
        if selection != -1:
            self.view.window().open_file(self.hits[selection], flags)
