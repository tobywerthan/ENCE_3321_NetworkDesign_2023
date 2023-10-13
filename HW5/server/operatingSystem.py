import os


def getCurrentDir():
    path = os.getcwd()


def runShellCommands():
    os.system("dir")


def listFiles():
    # Get current directory
    os.system("cd HW5")
    path = os.system("dir")

    # List all files in current directory
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                print(entry.name)


if __name__ == "__main__":
    # getCurrentDir()
    # runShellCommands()
    listFiles()
