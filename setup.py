import os
import json
import time
import logging
import requests

custom_theme = ""
setup_prefix = ""
error_prefix = ""
ascii_setup_bot = ""
ascii_setup = ""


class TermStyle:
    def __init__(self):
        self.themes = ["default", "dark", "purble"]
        self.themes_colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", "reset"]
        self.config = Config()
        self.reset = "\033[0m"
        self.bold = "\033[1m"
        self.underline = "\033[4m"
        self.blink = "\033[5m"
        self.reverse = "\033[7m"
        self.concealed = "\033[8m"
        self.black = "\033[30m"
        self.red = "\033[31m"
        self.green = "\033[32m"
        self.yellow = "\033[33m"
        self.blue = "\033[34m"
        self.magenta = "\033[35m"
        self.cyan = "\033[36m"
        self.white = "\033[37m"
        self.bg_black = "\033[40m"
        self.bg_red = "\033[41m"
        self.bg_green = "\033[42m"
        self.bg_yellow = "\033[43m"
        self.bg_blue = "\033[44m"
        self.bg_magenta = "\033[45m"
        self.bg_cyan = "\033[46m"
        self.bg_white = "\033[47m"
        self.setup_prefix = f"SETUP"
        self.err_prefix = f"ERROR"

    def load(self):
        global custom_theme, setup_prefix, error_prefix, ascii_setup_bot, ascii_setup
        with open(self.config.path_theme_cth) as f:
            text = f.read()
            start_index = text.find("custom_theme =") + len("custom_theme =")
            end_index = text.find("\n", start_index)
            custom_theme = text[start_index:end_index].strip().strip('"')

        with open(self.config.path_theme) as f:
            theme_data = json.load(f)
            setup_prefix = theme_data["Themes"][custom_theme]["SETUP_PREFIX"]
            error_prefix = theme_data["Themes"][custom_theme]["ERROR_PREFIX"]
            ascii_setup_bot = theme_data["Themes"][custom_theme]["ASCII_SETUP_BOT"]
            ascii_setup = theme_data["Themes"][custom_theme]["ASCII_SETUP"]

            if setup_prefix in self.themes_colors:
                setup_prefix = eval(f"self.{setup_prefix}")

            if error_prefix in self.themes_colors:
                error_prefix = eval(f"self.{error_prefix}")

            if ascii_setup_bot in self.themes_colors:
                ascii_setup_bot = eval(f"self.{ascii_setup_bot}")

            if ascii_setup in self.themes_colors:
                ascii_setup = eval(f"self.{ascii_setup}")

    def detect_theme(self):
        if custom_theme in self.themes:
            return custom_theme
        else:
            return False

    def loadtheme(self):
        try:
            self.load()
        except Exception as e:
            input("[" + self.red + self.err_prefix + self.reset + "] " + str(e) + " not found!")
            exit(1)
        if self.detect_theme():
            theme = self.detect_theme()
            print(theme + " theme loaded!")
        else:
            pass

    def printascii_botsetup(self):
        return """
  _________       __              __________        __   
 /   _____/ _____/  |_ __ ________\______   \ _____/  |_ 
 \_____  \_/ __ \   __\  |  \____ \|    |  _//  _ \   __/
 /        \  ___/|  | |  |  /  |_> >    |   (  <_> )  |  
/_______  /\___  >__| |____/|   __/|______  /\____/|__|  
        \/     \/           |__|          \/             
        """

    def printascii_setup(self):
        return """
  _________       __           
 /   _____/ _____/  |_ __ ________
 \_____  \_/ __ \   __\  |  \____ \\
 /        \  ___/|  | |  |  /  |_ > 
/_______  /\___  >__| |____/|   __/
        \/     \/           |__|                    
        """


class SetupLogging:
    def __init__(self):
        self.logfile = "base/config/logs/setup.log"

    def infologger(self, message):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", filename=self.logfile)
        infolog = logging.getLogger()
        infolog.info(message)

    def warninglogger(self, message):
        logging.basicConfig(level=logging.WARN, format="%(asctime)s %(levelname)s %(message)s", filename=self.logfile)
        warnlog = logging.getLogger()
        warnlog.warning(message)

    def errorlogger(self, message):
        logging.basicConfig(level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s", filename=self.logfile)
        errorlog = logging.getLogger()
        errorlog.error(message)


class Config:
    def __init__(self):
        self.Logger = SetupLogging()
        self.url_de = ""
        self.url_en = ""
        self.url_version = ""
        self.url_errcodes_de = ""
        self.url_errcodes_en = ""
        self.file_cth_theme = "theme.cth"
        self.file_theme = "themes.json"
        self.file_config = "config.json"
        self.file_properties = "properties.json"
        self.file_lang_de = "lang_de.json"
        self.file_lang_en = "lang_en.json"
        self.file_errcodes_de = "errcodes_de.json"
        self.file_errcodes_en = "errcodes_en.json"
        self.path_base = "base"
        self.path_theme_cth = f"base/config/theme/{self.file_cth_theme}"
        self.path_theme = f"base/config/theme/{self.file_theme}"
        self.path_logfile = "base/config/logs"
        self.path_properties = f"base/config/{self.file_properties}"
        self.path_config = f"base/config/{self.file_config}"
        self.path_de_lang = f"base/config/lang/{self.file_lang_de}"
        self.path_en_lang = f"base/config/lang/{self.file_lang_en}"
        self.path_error_codes_en = f"base/config/stores/{self.file_errcodes_en}"
        self.path_error_code_de = f"base/config/stores/{self.file_errcodes_de}"
        self.properties_data = {
            "version": "v0.0.1-aplha.1"
        }
        self.config_data = {
            "DiscordBotConfig": {
                "TextChannels": {},
                "VoiceChannels": {},
                "NSFWChannels": {},
                "AnouncementChannels": {},
            }
        }
        self.theme_data = {
            "Themes": {}
        }
        self.paths = ["base", "base/config", "base/config/lang", "base/config/logs", "base/config/stores",
                      "base/config/theme"]
        self.path_check = ["base/config", "base/config/lang", "base/config/logs", "base/config/stores",
                           "base/config/theme",
                           self.path_config, self.path_de_lang, self.path_en_lang, self.path_error_code_de,
                           self.path_error_codes_en, self.path_properties, self.path_logfile]

    def create_config(self):
        with open(self.path_config, "w") as f:
            json.dump(self.config_data, f, indent=4)
            self.Logger.infologger(f"{self.file_config} created in -> {self.path_config}")
            f.close()

    def update_config(self, obj, key, value):
        with open(self.path_config, "r") as f:
            config = json.load(f)
            config["DiscordBotConfig"][obj][key] = value

        with open(self.path_config, "w") as f:
            json.dump(config, f, indent=4)
            self.Logger.infologger(f"{self.file_config} updated -> {self.path_config} -> {obj} -> {key} -> {value}")
            f.close()

    def read_config(self):
        with open(self.path_config, "r") as f:
            config = json.load(f)
            self.Logger.infologger(f"{self.file_config} read -> {self.path_config}")
            f.close()
        return config

    def create_properties(self):
        with open(self.path_properties, "w") as f:
            json.dump(self.properties_data, f, indent=4)
            self.Logger.infologger(f"{self.file_properties} created in -> {self.path_properties}")
            f.close()

    def create_theme(self):
        with open(self.path_theme, "w") as f:
            json.dump(self.theme_data, f, indent=4)
            self.Logger.infologger(f"{self.file_theme} created in -> {self.path_theme}")
            f.close()

    def loadlang_de(self):
        with open(self.path_de_lang, "r") as f:
            langde = json.load(f)

    def loadlang_en(self):
        with open(self.path_en_lang, "r") as f:
            langen = json.load(f)


Start = TermStyle()
Start.loadtheme()
