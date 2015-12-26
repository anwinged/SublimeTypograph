import sublime
import sublime_plugin

from .lib.mdash import Typograph


__author__ = 'Anton Vakhrushev'
__email__ = 'anwinged@ya.ru'


PLUGIN_NAME = 'Typograph'

DEFAULT_SETTINGS = {
    'rules' = {}
}


class TypographSelectionCommand(sublime_plugin.TextCommand):
    """Process selections of html text"""

    def run(self, edit):
        """Executes command"""
        settings = self.__get_settings()
        rules = settings.get('rules', {})

        typograph = Typograph(rules)

        for region in self.view.sel():
            regionText = self.view.substr(region)
            processed = typograph.process(regionText).strip()
            self.view.replace(edit, region, processed)

    def __get_settings(self):
        """Loads plugin settings"""
        local_settings = self.__get_local_settings()
        project_settings = self.__get_project_settings()
        self.__merge_settings(local_settings, project_settings)
        return local_settings

    def __get_local_settings(self):
        """Returns local settings"""
        filename = self.__get_settings_filename()
        settings = sublime.load_settings(filename)
        local_settings = DEFAULT_SETTINGS.copy()

        for key in DEFAULT_SETTINGS:
            local_settings[key] = settings.get(key)

        return local_settings

    def __get_project_settings(self):
        """Return project settings"""
        return self.view.settings().get(PLUGIN_NAME, {})

    def __get_settings_filename(self):
        """Returns plugin settings filename"""
        return '{}.sublime-settings'.format(PLUGIN_NAME)

    def __merge_settings(self, local_settings, project_settings):
        """Overrides local settings with project settings"""
        for key in project_settings:
            if key in DEFAULT_SETTINGS:
                local_settings[key] = project_settings[key]
            else:
                print('{}: invalid key "{}" in project settings'.format(PLUGIN_NAME, key))
