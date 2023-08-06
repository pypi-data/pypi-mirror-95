import ctypes
import sys


kernel = ctypes.windll.kernel32
pid = int(sys.argv[1])

kernel.FreeConsole()

# TODO: what if attach failed
kernel.AttachConsole(pid)

# TODO: improve readability, use constants
# Disable Ctrl-C handling for our program
kernel.SetConsoleCtrlHandler(None, 1)
kernel.GenerateConsoleCtrlEvent(0, 0)

sys.exit(0)
