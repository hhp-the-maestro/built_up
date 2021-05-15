#! usr/bin/env/python3

# importing necessary modules
import os
import time
import shelve
import sys

# try importing pynput except give hint and exit program

try:
    from pynput.keyboard import Key, Controller
except ModuleNotFoundError:
    print('\033[91m'+"Module Not Found: 'pynput'\nhint: 'pip install pynput'")

# global variables

i, pid = 0, None
shelfy = shelve.open('file_track')
shelfy['first_run'] = 1
shelfy['is_error'] = 0
shelfy.close()

# functions

'''read the file 'filename' and store it as a list of strings
and store it for file tracking and updating'''


def read_original_file(filename):
    py_file = open(f'{filename}', 'r')

    # get each line of the file in a list
    lines = py_file.readlines()

    shelf = shelve.open('file_track')
    shelf['last_save'] = lines
    shelf['no_err_run'] = 0
    shelf.close()

    return lines

# write the list of strings from the read_file to the dupe_file and debug_file


def write_dupe_file(get_lines):
    lines = get_lines

    # create a dupe file
    dupe_file = open('dupe.py', 'w')
    dupe_file.write('\nimport multiprocessing\n')

    ''' write the entire original python file into 
        the dupe file with try and except to avoid errors'''

    dupe_file.writelines(lines)
    dupe_file.write('\nmain()')

    debug_file = open('debug.py', 'w')
    debug_file.write('\nimport multiprocessing, sys\n')
    debug_file.writelines(lines)
    insert_line = "\np = multiprocessing.Process(target=main, name='main')"
    debug_file.write(insert_line)
    debug_file.write("\np.start()\np.terminate()")

# runs debug file checks for error decision making running decisioned file


def run():
    shelf = shelve.open('file_track')
    os.system('python3 debug.py > log.txt 2>&1')
    # os.system("pkill -f 'python3 dupe.py'")
    file = open('log.txt', 'r')
    content = file.read()
    file.close()
    file = open('log.txt', 'w')
    file.close()
    if 'Error' in content:
        if shelf['first_run'] == 1:
            print('\033[91m' + 'Error: while Initializing file\nhint: hot_reloader.helper()')
            shelf['first_run'] = -1
            shelf.close()
            return
        if shelf['is_error'] == 0:
            print('\033[91m' + "There is an 'Error'...file tracking....")
            shelf['is_error'] = 1
        os.system('python3 no_error_file.py &')
        shelf['no_err_run'] = 1
        shelf.close()
    else:
        if shelf['is_error'] == 1:
            print('\033[92m' + "'Error'..'Debugged'")
            shelf['is_error'] = 0
        os.system('python3 dupe.py &')
        no_error = shelf['last_save']
        shelf.close()
        no_error_file = open('no_error_file.py', 'w')
        no_error_file.writelines(no_error)
        no_error_file.write('\nmain()')
        no_error_file.close()

# save the file 'filename'


def save_file():
    keyboard = Controller()
    keyboard.press(Key.ctrl_l)
    keyboard.press('s')
    keyboard.release('s')
    keyboard.release(Key.ctrl_l)

# get the active keyboard focus using xdotool 'sudo apt-get install xdotool'


def get_active_screen():
    # '2>&1' -> send both output and error to the same file
    os.system("xdotool getwindowfocus getwindowname > log.txt 2>&1")
    screen = 0
    file = open('log.txt', 'r')
    name = file.readline()
    file.close()
    if '.py' in name:
        screen = 1
    elif 'not found' in name:
        print('\033[91m' + "'xdotool': not found\n hint: 'sudo apt-get install xdotool")
        sys.exit()
    file = open('log.txt', 'w')
    file.close()
    return screen

# kill the running file


def get_kill(pid_):
    os.system(f"kill {pid_} >> log.txt 2>&1")
    file = open('log.txt', 'w')
    file.close()

# get the process id for the running file 'filename'


def get_pid():
    global pid
    shelf = shelve.open('file_track')
    was_error_file_run = shelf['no_err_run']

    if was_error_file_run == 1:
        os.system("pgrep -f 'python3 no_error_file.py' > log.txt 2>&1")
        shelf['no_err_run'] = 0
        shelf.close()
    else:
        os.system("pgrep -f 'python3 dupe.py'> log.txt 2>&1")

        shelf.close()
    file = open('log.txt', 'r')
    pid = file.readline()
    file.close()
    file = open('log.txt', 'w')
    file.close()
    return pid

# packing all the above functions in order to make the hot re_loader work


def re_loader(filename):
    while True:
        try:
            global i, pid
            lines = read_original_file(filename)
            write_dupe_file(lines)
            screen = get_active_screen()
            if screen == 1:
                save_file()
                run()
                time.sleep(0.7)
                if i == 1:
                    get_kill(int(pid))
                pid = get_pid()
                time.sleep(2.5)
            i = 1
            shelf = shelve.open('file_track')
            if shelf['first_run'] == -1:
                break
            shelf['first_run'] = 0
            shelf.close()
        except KeyboardInterrupt:
            os.system("pkill -f 'python3 dupe.py' 2> log.txt")
            os.system("pkill -f 'python3 no_error_file.py' 2> log.txt")
            break
    sys.exit()

# the helper function which contains information how to use the hot_reloader


def helper():
    print('\033[92m' + '\t\t\t\t\t\t\thot_reloader\n\t\t\t\t\t\t\t\t\t - by hhp (Hari Hara Prasad)')
    print('\033[94m' + f"The hot reloader was made to get a nearly similar feel of working in google's flutter dev\n"
                       f"hot reloader, the reloader saves your file, reloads it and neglects any errors in\n"
                       f"your program by tracking the version of your file with no errors. It is very appealing while\n"
                       f"doing app developement with pyqt, kivy, tkinter, etc. where you don't need to run your \n"
                       f"program each and every time for minimal testing of your developement.")

    print('\033[94m' + "\nthe program was set, to get, run only on linux and the program must be imported and run\n"
                       "from a seperate file and that's it you can do your developement while running your program\n"
                       "along side with this hot_reloader. while doing app development your keyboard focus should\n"
                       "in your IDE or the .py file to run the reloader or else it pauses updating")

    print('USAGE: __________________________________________________________________________')

    print('\033[94m' + '''\nIncase you have a python file like this,\n''')
    print('\033[95m' + '\t\tscript.py\n\n')
    print('\033[96m' + 'import...\nclass X():\n\tdef...\n\t\tpass\n\tdef...\n\t\tpass')
    print('\033[94m' + "\nyou should always have a function main through which your entire program runs and you \n"
                       "should not call the function main() anywhere in your program")
    print('\033[96m' + '\ndef main():\n\trun = X()')
    print('\033[94m' + 'you should provide a file which can  run without any errors. after successfully initializingr\n'
                       'the hot reloader , you can write codes on your file where errors do not disturb the reloader')
    print('\033[94m' + 'Now create a new file for example sample.py and,')
    print('\033[95m' + '\n\t\tsample.py\t\t\n')
    print('\033[96m' + "\nimport hot_reloader\nhot_reloader.re_loader('script.py')")
    print('\033[94m' + "\n\nThe program seems to run only on linux, As for sure the program is set not to run into\n"
                       "errors, even running errors won't disturb the reloader it updates as soon you debug the error\n"
                       "you don't need to get worried about it coz running the reloader is simple")

# ____________________________end of program____________________________________________________________________________
