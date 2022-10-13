"""Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>
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

        self.lastest_fasttext_model = None
        self.update_load_button = None

    def config_clicked(self, parent, lastest_fasttext_model, update_load_button):
        """Open configuration window.

        Args:
            parent (NewsButtonView): NewsButtonView object.
            lastest_fasttext_model (str): Lastest fastText model loaded.
            update_load_button (Callable[str, str], None)
        """

        self.config_view = ConfigView(self, parent, padx=10, pady=10)

        self.lastest_fasttext_model = lastest_fasttext_model
        self.update_load_button = update_load_button

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

        self.update("KEYWORDS", "INCLUDE", self.config_view.configs["keywords_to_include"].get())
        self.update("KEYWORDS", "EXCLUDE", self.config_view.configs["keywords_to_exclude"].get())
        self.update("FASTTEXT", "PATH", self.config_view.configs["fasttext_path"].get())
        self.update(
            "FASTTEXT",
            "TRAIN",
            "true" if self.config_view.configs["train_enabled"].get() else "false"
        )
        self.update("FASTTEXT", "TRAINED_MODEL", self.config_view.configs["trained_model"].get())

        with open(self.config.config_path, "w", encoding="utf-8") as config_file:
            config_file.write("; Writer: Jinchan Hwang <jchwang@yonsei.ac.kr>\n\n")
            self.config.write(config_file)

        self.update_load_button(
            self.lastest_fasttext_model, self.config_view.configs["fasttext_path"].get()
        )

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
        """Returns pretrained fastText model path.

        Returns:
            str: Pretrained fastText model path.
        """

        return self.config.get("FASTTEXT", "PATH")

    def train_enabled(self):
        """Returns whether fastText model training enabled.

        Returns:
            bool: Whether fastText model training enabled.
        """

        return self.config.getboolean("FASTTEXT", "TRAIN")

    def trained_model(self):
        """Returns trained model name.

        Returns:
            str: Trained model name.
        """

        return self.config.get("FASTTEXT", "TRAINED_MODEL")
