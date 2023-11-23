from .textcolors import textcolors

class log:
    def fatul(text, exitcode=1, process=None):
        if process == None:
            processname = 'UNKNOWN'
        else:
            processname = process
        print(
            textcolors.RED
            + f"[{processname}] "
            + textcolors.BOLD
            + "[FATUL] "
            + text
            + " ("
            + str(exitcode)
            + ")"
            + textcolors.END
        )

    def error(text, process=None):
        if process == None:
            processname = 'UNKNOWN'
        else:
            processname = process
        print(textcolors.RED + "[ERROR] " + text + textcolors.END)

    def warning(text, process=None):
        if process == None:
            processname = 'UNKNOWN'
        else:
            processname = process
        print(textcolors.YELLOW + f"[{processname}] " + "[WARNING] " + text + textcolors.END)

    def success(text, process=None):
        if process == None:
            processname = 'UNKNOWN'
        else:
            processname = process
        print(textcolors.GREEN + f"[{processname}] " + "[SUCCESS] " + text + textcolors.END)

    def successblue(text, process=None):
        if process == None:
            processname = 'UNKNOWN'
        else:
            processname = process
        print(textcolors.BLUE + f"[{processname}] " + "[SUCCESS] " + text + textcolors.END)

    def successcyan(text, process=None):
        if process == None:
            processname = 'UNKNOWN'
        else:
            processname = process
        print(textcolors.CYAN + f"[{processname}] " + "[SUCCESS] " + text + textcolors.END)

    def log(text, process=None):
        if process == None:
            processname = 'UNKNOWN'
        else:
            processname = process
        print(f"[{processname}] " + "[INFO] " + text)

    def info(text, process=None):
        if process == None:
            processname = 'UNKNOWN'
        else:
            processname = process
        print(f"[{processname}] " + "[INFO] " + text)