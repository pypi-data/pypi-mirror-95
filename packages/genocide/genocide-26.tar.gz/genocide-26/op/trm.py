# OPBOT - pure python3 IRC bot (op/trm.py)
#
# This file is placed in the Public Domain.

"terminal"

# imports

import atexit, sys, termios

# functions

def exec(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError as ex:
        print(str(ex))
    finally:
        termreset()

def termsetup(fd):
    return termios.tcgetattr(fd)

def termreset():
    if "old" in resume:
        try:
            termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])
        except termios.error:
            pass

def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = termsetup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass

# runtime

resume = {}
