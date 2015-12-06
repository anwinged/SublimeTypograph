import sublime
import sublime_plugin

from .lib.artlebedev import RemoteTypograf


__author__ = 'Anton Vakhrushev'
__email__ = 'anwinged@ya.ru'


PLUGIN_NAME = 'Typograph'

DEFAULT_SETTINGS = {
    'type': 'html',
    'breaks': False,
    'paragraphs': False,
    'max_no_break': 3,
}


class TypographSelectionCommand(sublime_plugin.TextCommand):
    """
    Process selections of html text
    """

    def run(self, edit):

        settings = self.get_settings()

        typograf = RemoteTypograf()
        typograf.htmlEntities()
        typograf.br(settings['breaks'])
        typograf.p(settings['paragraphs'])
        typograf.nobr(settings['max_no_break'])

        for region in self.view.sel():
            processed = typograf.processText(self.view.substr(region))            
            self.view.replace(edit, region, processed)


    def get_settings(self):
        """
        Load plugin settings
        """
        settings = sublime.load_settings('{}.sublime-settings'.format(PLUGIN_NAME))
        project_settings = self.view.settings().get(PLUGIN_NAME, {})
        local_settings = DEFAULT_SETTINGS.copy()

        for key in DEFAULT_SETTINGS:
            local_settings[key] = settings.get(key)

        for key in project_settings:
            if key in DEFAULT_SETTINGS:
                local_settings[key] = project_settings[key]
            else:
                print('{}: invalid key "{}" in project settings'.format(PLUGIN_NAME, key))

        return local_settings
