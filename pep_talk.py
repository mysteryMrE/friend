from abc import ABC
import tkinter as tk


# TODO: not a clean thing to have abstract class without abstract methods, but it is to stop instantiation
class PepTalk(ABC):
    def __init__(self, message: str):
        self.message = message

    def get_display_message(self):
        return self.message
