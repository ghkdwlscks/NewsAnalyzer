"""Writer: Jinchan Hwang <ghkdwlscks@gmail.com>
"""


from view.config_view import ConfigView


class ConfigController:
    """ConfigController object.

    Args:
        config (Config): Config object.
    """

    def __init__(self, config):
        self.config = config
        self.config_view = None

    def config_clicked(self, parent):
        """Open configuration window.

        Args:
            parent (ButtonView): ButtonView object.
        """

        self.config_view = ConfigView(self, parent)

    def update(self, section, option, value):
        """Update configurations.

        Args:
            section (str): Config section.
            option (str): Config option.
            value (str): Config value.
        """

        self.config.set(section, option, value)

    def save(self):
        """Save configurations file.
        """

        self.update("KEYWORDS", "INCLUDE", self.config_view.keywords_to_include.get())
        self.update("KEYWORDS", "EXCLUDE", self.config_view.keywords_to_exclude.get())
        self.update("FASTTEXT", "PATH", self.config_view.fasttext_path.get())

        with open(self.config.config_path, "w", encoding="utf-8") as config_file:
            config_file.write("; Writer: Jinchan Hwang <ghkdwlscks@gmail.com>\n\n")
            self.config.write(config_file)

    def keywords_to_include(self):
        """Returns keywords to include.

        Returns:
            str: Keywords to include split by commas.
        """

        return self.config.get("KEYWORDS", "INCLUDE")

    def keywords_to_exclude(self):
        """Returns keywords to exclude.

        Returns:
            str: Keywords to exclude split by commas.
        """

        return self.config.get("KEYWORDS", "EXCLUDE")

    def fasttext_path(self):
        """Returns pretrained FastText model path.

        Returns:
            str: Pretrained FastText model path.
        """

        return self.config.get("FASTTEXT", "PATH")
