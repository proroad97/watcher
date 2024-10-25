# Watcher , a simple script for spying your PC...

Installing this package, the 'watch' command will be available on your environment. You need to provide arguments to run the command. The program exits if not provide any argument. Run --help to learn the available options. 

If you want to run it in Linux system, you should first install Tkinter (apt-get install python3-tk).

If you want to send an email, a json file is needed with the neccessary credentials for message's initialization.
Sample file:
    {
        'To':'youremail@gmail.com',
        'From':'receiver@gmail.com',
        'port':587,
        'hostname':'smtp.gmail.com',
        'username':'youremail@gmail.com',
        'password':yourpassword
    }

## How to
This package have been created by using Pynput Listeners.

The MouseEvent/KeyboardEvent classes from 'events' module accepts any Iteratable of Callables and return a callback that passes properly the arguments provided from Pynput

The 'controllers' module provides two decorators that control how often a function is called. You can create more decorators in the same way.


