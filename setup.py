import json
import logging
import os
import requests

custom_theme = ""
setup_prefix, error_prefix, ascii_setup, ascii_setup_bot = "", "", "", ""


class Console:
    def __init__(self):
        self.Config = Config()
        self.logger = SetupLogging()
        self.root_embed = """
  _________       __                    _____                       
 /   _____/ _____/  |_ __ ________     /     \   ____   ____  __ __ 
 \_____  \_/ __ \   __\  |  \____ \   /  \ /  \_/ __ \ /    \|  |  \
 /        \  ___/|  | |  |  /  |_> > /    Y    \  ___/|   |  \  |  /
/_______  /\___  >__| |____/|   __/  \____|__  /\___  >___|  /____/ 
        \/     \/           |__|             \/     \/     \/       
        """
        self.themes = ["default", "royal crimson"]
        self.themes_colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", "reset", "bold",
                              "underline", "blink", "reverse", "concealed", "bg_black", "bg_red", "bg_green",
                              "bg_yellow", "bg_blue", "bg_magenta", "bg_cyan", "bg_white"]
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

    def load(self):
        global setup_prefix, error_prefix, ascii_setup, ascii_setup_bot, custom_theme
        with open(self.config.path_theme_cth) as f:
            text = f.read()
            start_index = text.find("custom_theme =") + len("custom_theme =")
            end_index = text.find("\n", start_index)
            custom_theme = text[start_index:end_index].strip().strip('"')

        if os.path.exists(self.config.path_theme):
            with open(self.config.path_theme) as f:
                theme_data = json.load(f)
                setup_prefix_data = theme_data["Themes"][custom_theme]["SETUP_PREFIX"]
                error_prefix_data = theme_data["Themes"][custom_theme]["ERROR_PREFIX"]
                ascii_setup_bot_data = theme_data["Themes"][custom_theme]["ASCII_SETUP_BOT"]
                ascii_setup_data = theme_data["Themes"][custom_theme]["ASCII_SETUP"]

                if setup_prefix_data in self.themes_colors:
                    setup_prefix = getattr(self, setup_prefix_data)
                if error_prefix_data in self.themes_colors:
                    error_prefix = getattr(self, error_prefix_data)
                if ascii_setup_bot_data in self.themes_colors:
                    ascii_setup_bot = getattr(self, ascii_setup_bot_data)
                if ascii_setup_data in self.themes_colors:
                    ascii_setup = getattr(self, ascii_setup_data)
        else:
            self.logger.errorlogger("ERROR: Theme file not found. Exiting...")
            exit(1)

    def detect_theme(self):
        self.logger.infologger("Detecting Theme !")
        if custom_theme in self.themes:
            return True
        else:
            return False

    def loadtheme(self):
        if os.path.exists(self.config.path_theme) and os.path.exists(self.config.path_theme_cth):
            self.load()
        else:
            self.logger.errorlogger("ERROR: Theme file not found. Exiting...")
            exit(1)
        if self.detect_theme():
            self.logger.infologger(f"{custom_theme} Theme loaded !")
        else:
            self.logger.errorlogger(f"ERROR: Invalid theme: {custom_theme} ")
            exit(1)

    def printinfo(self, text):
        print("[{}SETUP{}] {}".format(setup_prefix, self.reset, text))

    def printerror(self, text):
        print("[{}ERROR{}] {}".format(error_prefix, self.reset, text))

    def printascii_bot(self):
        print(ascii_setup_bot + """
________  .__                              .___ __________        __   
\______ \ |__| ______ ____  ___________  __| _/ \______   \ _____/  |_ 
 |    |  \|  |/  ___// ___\/  _ \_  __ \/ __ |   |    |  _//  _ \   __
 |    `   \  |\___ \\  \__(  <_> )  | \/ /_/ |   |    |   (  <_> )  |  
/_______  /__/____  >\___  >____/|__|  \____ |   |______  /\____/|__|  
        \/        \/     \/                 \/          \/             
        """ + self.reset)

    def printascii_setup(self):
        print(ascii_setup_bot + """
________  .__                              .___   _________       __                
\______ \ |__| ______ ____  ___________  __| _/  /   _____/ _____/  |_ __ ________  
 |    |  \|  |/  ___// ___\/  _ \_  __ \/ __ |   \_____  \_/ __ \   __\  |  \_____
 |    `   \  |\___ \\  \__(  <_> )  | \/ /_/ |   /        \  ___/|  | |  |  /  |_> >
/_______  /__/____  >\___  >____/|__|  \____ |  /_______  /\___  >__| |____/|   __/ 
        \/        \/     \/                 \/          \/     \/           |__|            
        """ + self.reset)


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
        self.url_de = "https://raw.githubusercontent.com/Tarzzaann/DiscordBot/master/base/config/lang/lang_de.json"
        self.url_en = ""
        self.url_version = "https://raw.githubusercontent.com/Tarzzaann/DiscordBot/master/base/config/properties.json"
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
                "SetupConf": {},
                "TextChannels": {},
                "VoiceChannels": {},
                "NSFWChannels": {},
                "AnouncementChannels": {}
            }
        }
        self.theme_data = {
            "Themes": {
                "default": {
                    "SETUP_PREFIX": "green",
                    "ERROR_PREFIX": "red",
                    "ASCII_SETUP_BOT": "yellow",
                    "ASCII_SETUP": "yellow"
                },
                "royal crimson": {
                    "SETUP_PREFIX": "red",
                    "ERROR_PREFIX": "red",
                    "ASCII_SETUP_BOT": "red",
                    "ASCII_SETUP": "red"
                }
            }
        }
        self.theme_cth_data = 'custom_theme: "default"'
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
        with open(self.path_theme_cth, "w") as f:
            f.write(self.theme_cth_data)
            self.Logger.infologger(f"{self.file_cth_theme} created in -> {self.path_theme_cth}")
            f.close()

    def loadlang_de(self):
        global DiscordSetupMessages, DiscordBotMessages, DiscordBotSetupError
        with open(self.path_de_lang, "r") as f:
            langde = json.load(f)
            DiscordSetupMessages = langde["DiscordBotLangContent"]["DiscordBotLangCategory"]["DiscordBotSetupMessages"]
            DiscordBotMessages = langde["DiscordBotLangContent"]["DiscordBotLangCategory"]["DiscordSetupMessages"]
            DiscordBotSetupError = langde["DiscordBotLangContent"]["DiscordBotLangCategory"][
                "DiscordSetupErrorMessages"]

    def loadlang_en(self):
        global DiscordSetupMessages, DiscordBotMessages, DiscordBotSetupError
        with open(self.path_en_lang, "r") as f:
            langen = json.load(f)
            DiscordSetupMessages = langen["DiscordBotLangContent"]["DiscordBotLangCategory"]["DiscordBotSetupMessages"]
            DiscordBotMessages = langen["DiscordBotLangContent"]["DiscordBotLangCategory"]["DiscordSetupMessages"]
            DiscordBotSetupError = langen["DiscordBotLangContent"]["DiscordBotLangCategory"][
                "DiscordSetupErrorMessages"]


class Setup:
    def __init__(self):
        self.Config = Config()
        self.Logger = SetupLogging()
        self.Console = Console()

    def get_lanuage(self):
        lang = input("Language (de/en): ")
        if lang == "de":
            reqde = requests.get(self.Config.url_de)
            if reqde.status_code == 200:
                with open(self.Config.path_de_lang, "w") as f:
                    f.write(reqde.text)
                    f.close()
                    self.Logger.infologger("Language set to -> de")
                    self.Config.update_config("SetupConf", "language", "de")
        elif lang == "en":
            reqen = requests.get(self.Config.url_en)
            if reqen.status_code == 200:
                with open(self.Config.path_en_lang, "w") as f:
                    f.write(reqen.text)
                    f.close()
                    self.Logger.infologger("language seto to -> en")
                    self.Config.update_config("SetupConf", "language", "en")
        else:
            self.Logger.errorlogger("Language net set. retry...")
            self.get_lanuage()

    def load_language(self):
        if os.path.exists(self.Config.path_de_lang):
            self.Logger.infologger(f"Loading Language -> de | path: {self.Config.path_de_lang}")
            self.Config.loadlang_de()
        elif os.path.exists(self.Config.path_en_lang):
            self.Logger.infologger(f"Loading Language -> en | path {self.Config.path_en_lang}")
            self.Config.loadlang_en()
        else:
            self.Logger.errorlogger(f"Language not found")
            exit(1)

    def create_structure(self):
        for folder in self.Config.paths:
            if not os.path.exists(folder):
                os.mkdir(folder)
            else:
                pass

    def create_envirmoment(self):
        if self.get_version():
            self.get_lanuage()
            self.load_language()
        else:
            self.Logger.errorlogger("Version is not up to date")
            exit(1)

    def get_version(self):
        url_version = requests.get(self.Config.url_version).json()["version"]
        fetch_version = json.load(open(self.Config.path_properties, "r"))["version"]
        self.Logger.infologger(f"Checking Version")
        if url_version == fetch_version:
            self.Logger.infologger(f"Version is up to date -> {url_version}")
            return True
        else:
            self.Logger.errorlogger(f"Version is not up to date -> {fetch_version} -> new version: {url_version}")
            return False

    def menu(self):
        self.Logger.infologger("Entering Menu")

    def start(self):
        if not os.path.exists(self.Config.path_base):
            for folder in self.Config.path_check:
                if not os.path.exists(folder):
                    self.create_structure()
                else:
                    pass
            self.Config.create_properties()
            self.Config.create_config()
            self.Config.create_theme()
            self.create_envirmoment()
            self.Console.loadtheme()
        else:
            self.Console.loadtheme()
            self.menu()


Setup = Setup()
Setup.start()
