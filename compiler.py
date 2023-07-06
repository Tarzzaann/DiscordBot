import os
import time
import shutil


class TermColor:
    red = "\033[91m"
    green = "\033[92m"
    reset = "\033[0m"


class Compiler:
    def __init__(self):
        self.dev_mode = True
        self.base_path = "base"
        self.build_path = "_target"

    def compile(self):
        if os.path.exists(self.build_path):
            shutil.rmtree(self.build_path)
        else:
            os.mkdir(self.build_path)

        files = os.listdir()
        print("[{}{}{}-{}] Compiling...".format(TermColor.green, "COMPILER ", TermColor.reset, time.strftime(" %H:%M:%S")))
        for build in files:
            if build.endswith(".py"):
                shutil.copy(build, self.build_path)
        os.remove(f"{self.build_path}/compiler.py")


compiler = Compiler()
compiler.compile()
