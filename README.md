# Watcher , a simple script for spying your PC...

Installing this package, you can run a 'watch' command. You need to provide neccessary arguments for where to store
the captured informations. The program exits if not provide any argument. Run --help to learn the available options. 

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