import os
import json
import time
import logging
import requests

DiscordSetupMessages = ""
DiscordBotMessages = ""


class SetupLogging:
    def __init__(self):
        self.logfile = f"base/config/logs/setup.log"

    def infologger(self, message):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", filename=self.logfile)
        infolog = logging.getLogger()
        infolog.info(message)

    def warninglogger(self, message):
        logging.basicConfig(level=logging.WARN, format="%(asctime)s %(levelname)s %(message)s", filename=self.logfile)
        warnlog = logging.getLogger()
        warnlog.info(message)

    def errorlogger(self, message):
        logging.basicConfig(level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s", filename=self.logfile)
        errorlog = logging.getLogger()
        errorlog.info(message)


class TermStyle:
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    blue = "\033[94m"
    purple = "\033[95m"
    cyan = "\033[96m"
    white = "\033[97m"
    reset = "\033[0m"

    SetupAscii = yellow + f"""
  _________       __              __________        __   
 /   _____/ _____/  |_ __ ________\______   \ _____/  |_ 
 \_____  \_/ __ \   __\  |  \____ \|    |  _//  _ \   __/
 /        \  ___/|  | |  |  /  |_> >    |   (  <_> )  |  
/_______  /\___  >__| |____/|   __/|______  /\____/|__|  
        \/     \/           |__|          \/             
    """ + reset


class Config:
    def __init__(self):
        self.Logger = SetupLogging()
        self.url_de = "https://raw.githubusercontent.com/Tarzzaann/DiscordBot/master/base/config/lang/lang_de.json"
        self.url_en = "https://raw.githubusercontent.com/Tarzzaann/DiscordBot/master/base/config/lang/lang_en.json"
        self.url_version = "https://raw.githubusercontent.com/Tarzzaann/DiscordBot/master/base/config/properties.json"
        self.config = "config.json"
        self.properties = "properties.json"
        self.lang_de = "lang_de.json"
        self.lang_en = "lang_en.json"
        self.logfile_path = "base/config/logs/"
        self.properties_path = f"base/config/{self.properties}"
        self.config_path = f"base/config/{self.config}"
        self.de_lang_path = f"base/config/lang/{self.lang_de}"
        self.en_lang_path = f"base/config/lang/{self.lang_en}"
        self.properties_data = {
            "version": "0.0.1",
        }
        self.config_data = {
            "DiscordBotConfig": {}
        }
        self.bot_path = ["base", "base/config", "base/config/logs", "base/config/lang"]
        self.check_bot_path = ["base", "base/config", self.config_path, self.properties_path,
                               "base/config/lang", self.de_lang_path, self.en_lang_path]

    def create_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config_data, f, indent=4)
            self.Logger.infologger(f"Created {self.config}")
            f.close()

    def update_config(self, key, value):
        with open(self.config_path, "r") as f:
            config = json.load(f)
            self.Logger.infologger(f"Read for update {self.config}")

            config["DiscordBotConfig"][key] = value

        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)
            self.Logger.infologger(f"Updated {self.config} | {key} -> {value}")
            f.close()

    def read_config(self):
        with open(self.config_path, "r") as f:
            config = json.load(f)
            self.Logger.infologger(f"Read {self.config}")
        return config

    def create_properties(self):
        with open(self.properties_path, "w") as f:
            json.dump(self.properties_data, f, indent=4)
            self.Logger.infologger(f"Created {self.properties}")
            f.close()

    def load_de(self):
        with open(self.de_lang_path, "r") as f:
            global DiscordSetupMessages, DiscordBotMessages
            langde = json.load(f)
            DiscordSetupMessages = langde["DiscordBotLangContent"]["DiscordLangCategory"]["DiscordSetupMessages"]
            DiscordBotMessages = langde["DiscordBotLangContent"]["DiscordLangCategory"]["DiscordBotMessages"]

    def load_en(self):
        with open(self.en_lang_path, "r") as f:
            global DiscordSetupMessages, DiscordBotMessages
            langen = json.load(f)
            DiscordSetupMessages = langen["DiscordBotLangContent"]["DiscordLangCategory"]["DiscordSetupMessages"]
            DiscordBotMessages = langen["DiscordBotLangContent"]["DiscordLangCategory"]["DiscordBotMessages"]


class Setup:
    def __init__(self):
        self.Config = Config()
        self.Logger = SetupLogging()
        self.BotSetup = DiscordBotConfig()
        self.msg_prefix = "[{}{}{}]".format(TermStyle.green, "SETUP", TermStyle.reset)
        self.msg_prefix_err = "[{}{}{}]".format(TermStyle.red, "ERROR", TermStyle.reset)
        self.write_prefix = TermStyle.cyan

    def get_language(self):
        lang = input("\r" + self.msg_prefix + " Choose your language (de/en): " + self.write_prefix)
        if lang == "de":
            dlde = requests.get(self.Config.url_de)
            with open(self.Config.de_lang_path, "wb") as f:
                f.write(dlde.content)
                f.close()
                self.Logger.infologger(f"Language set to de")
                self.Config.update_config("language", "de")
        elif lang == "en":
            dlen = requests.get(self.Config.url_en)
            with open(self.Config.en_lang_path, "wb") as f:
                f.write(dlen.content)
                f.close()
                self.Logger.infologger(f"Language set to en")
                self.Config.update_config("language", "en")
        else:
            self.Logger.errorlogger(f"Language not set. retry...")
            time.sleep(1)
            self.get_language()

    def load_language(self):
        if os.path.exists(self.Config.de_lang_path):
            self.Logger.infologger(f"Loading Language -> de | path: {self.Config.de_lang_path}")
            self.Config.load_de()
        elif os.path.exists(self.Config.en_lang_path):
            self.Logger.infologger(f"Loading Language -> en | path: {self.Config.en_lang_path}")
            self.Config.load_en()
        else:
            self.Logger.errorlogger(f"Language not found. retry...")
            input(self.msg_prefix_err + " Error language file not found.")
            exit()

    def create_structure(self):
        for folder in self.Config.bot_path:
            if not os.path.exists(folder):
                os.mkdir(folder)
            else:
                pass

    def create_enviroment(self):
        if self.get_version():
            self.get_language()
            self.load_language()
            self.Logger.infologger(f"Setup finished successfully, starting DiscordBotSetup...")
            self.BotSetup.check()
        else:
            self.Logger.errorlogger(f"Exiting...")
            input(self.msg_prefix_err + " Error version not up to date.")
            exit()

    def get_version(self):
        url_version = requests.get(self.Config.url_version).json()["version"]
        fetch_version = json.load(open(self.Config.properties_path, "r"))["version"]
        self.Logger.infologger(f"Checking Version")
        if url_version == fetch_version:
            self.Logger.infologger(f"Version is up to date -> {url_version}")
            return True
        else:
            self.Logger.errorlogger(f"Version is not up to date {fetch_version} " + "->" + f" {url_version}")
            self.Logger.errorlogger(f"Updating Version to -> {url_version}")
            return False

    def start(self):
        print(TermStyle.SetupAscii)
        print(f"\r{self.msg_prefix} Starting Setup...{TermStyle.reset}", end="", flush=True)
        time.sleep(1.9)
        print(f"\r{self.msg_prefix} Checking Version...{TermStyle.reset}", end="", flush=True)
        time.sleep(1.2)
        print(f"\r{self.msg_prefix} Creating folders...{TermStyle.reset}", end="", flush=True)
        time.sleep(1.2)
        print(f"\r{self.msg_prefix} Creating config...{TermStyle.reset}", end="", flush=True)
        time.sleep(1.2)
        print(f"\r{self.msg_prefix} Creating properties...\r\r{TermStyle.reset}", end="", flush=True)
        time.sleep(1.2)
        for folder in self.Config.check_bot_path:
            if not os.path.exists(folder):
                self.create_structure()
            else:
                pass
        self.Config.create_properties()
        self.Config.create_config()
        self.create_enviroment()


class DiscordBotConfig:
    def __init__(self):
        self.Config = Config()
        self.Logger = SetupLogging()
        self.write_prefix = TermStyle.cyan

    def setup_channels(self):
        channel_count = int(input(str(DiscordBotMessages["DiscordBotChannels"]
                                      .format(TermStyle.green, "SETUP", TermStyle.reset)) + self.write_prefix))
        if channel_count == 0:
            self.Logger.errorlogger(f"Setup failed, channel count can't be 0")
            input("")
            exit(1)

    def check(self):
        for files in self.Config.check_bot_path:
            if not os.path.exists(files):
                self.Logger.errorlogger(f"Setup failed, missing files -> {files}")
                if os.path.exists(files) == self.Config.de_lang_path or self.Config.en_lang_path:
                    self.Logger.errorlogger(f"missing files -> {files} | can be ignored")
                exit(1)
            else:
                self.start()
                break

    def start(self):
        self.setup_channels()


if __name__ == "__main__":
    Start = Setup()
    Conf = Config()
    Start.start()
