from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.font_definitions import theme_font_styles
from kivymd import fonts_path

from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
import json
import requests

import plyer
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.button import MDRectangleFlatButton


Window.size = (310,500)


class Slope(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Builder.load_file("main.kv"))
        self.screen_manager.add_widget(Builder.load_file("login.kv"))
        self.screen_manager.add_widget(Builder.load_file("signup.kv"))
        self.screen_manager.add_widget(Builder.load_file("menu.kv"))
        #self.screen_manager.add_widget(Builder.load_file("checkin.kv"))
        self.screen_manager.add_widget(Builder.load_file("checkout.kv"))
        self.screen_manager.add_widget(Builder.load_file("manualcheckin.kv"))
        self.url = "https://smarthome-dip-default-rtdb.asia-southeast1.firebasedatabase.app/.json"
        return self.screen_manager

    def signup(self):
        signupEmail = self.screen_manager.get_screen('signupscreen').ids.signup_email.text
        signupPassword = self.screen_manager.get_screen('signupscreen').ids.signup_password.text
        signupUsername = self.screen_manager.get_screen('signupscreen').ids.signup_username.text
        
        if signupEmail.split() == [] or signupPassword.split() == [] or signupUsername.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        if len(signupUsername.split()) > 1:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Username', text='Please enter username without space',
                                   size_hint=(0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            print(signupEmail, signupPassword)
            signup_info = str(
                {f'\"{signupEmail}\":{{"Password":\"{signupPassword}\","Username":\"{signupUsername}\"}}'})
            signup_info = signup_info.replace(".", "-")
            signup_info = signup_info.replace("\'", "")
            to_database = json.loads(signup_info)
            print((to_database))
            requests.patch(url=self.url, json=to_database)
            self.screen_manager.get_screen('loginscreen').manager.current = 'loginscreen'

    auth = 'RjYQfhg6CBDjRoyGDJ3rPmHFLdwUctGvkDJDz2vZ'

    def login(self):
        loginEmail = self.screen_manager.get_screen('loginscreen').ids.login_email.text
        loginPassword = self.screen_manager.get_screen('loginscreen').ids.login_password.text

        self.login_check = False
        supported_loginEmail = loginEmail.replace('.', '-')
        supported_loginPassword = loginPassword.replace('.', '-')
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        emails = set()
        for key, value in data.items():
            emails.add(key)
        if supported_loginEmail in emails and supported_loginPassword == data[supported_loginEmail]['Password']:
            self.username = data[supported_loginEmail]['Username']
            self.login_check = True
            self.screen_manager.get_screen('menuscreen').manager.current = 'menuscreen'
        else:
            cancel_btn_username_dialogue = MDFlatButton(text='Okay', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Login', text='Incorrect Username/Password',
                                   size_hint=(0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            print("Wrong username/password")


    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def username_changer(self):
        if self.login_check:
            self.screen_manager.get_screen('menuscreen').ids.username_info.text = f"Welcome {self.username}"

    #On Save for DatePicker???
    def on_save(self, instance, value, name):
        print(instance, value, name)
        self.screen_manager.get_screen('manualcheckin').ids.date_picker.text = str(value)

    def get_date(self, date):
        self.manualcheckin.ids.date_picker = date
        self.screen_manager.get_screen('manualcheckin').ids.date_picker.text = str(self.manualcheckin)

    # Click Cancel
    def on_cancel(self, instance, value):
        pass

    #Date Picker - Manual Check In Screen
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    #Dialog to acknowledge items saved - Manual Check In Screen
    def show_text(self):
        cancel_btn_username_dialogue = MDFlatButton(text='Okay', on_release=self.close_username_dialog)
        self.dialog = MDDialog(title='Check In Items', text='Your items have been saved.',
                                   size_hint=(0.7, 0.2),buttons=[cancel_btn_username_dialogue])
        self.dialog.open()

    #Notification Code (import plyer)
    def show_notification(self):
        plyer.notification.notify(title='MyLittle Fridge', message="Your food is expiring!")

    #clearInput for after user have saved - Manual Check In Screen
    def clearInput(self):
        self.screen_manager.get_screen('manualcheckin').ids.name_item.text = ''
        self.screen_manager.get_screen('manualcheckin').ids.date_picker.text = 'Key In Expiration Date'

if __name__ == "__main__":
    LabelBase.register(name= "RobotoMedium",fn_regular= fonts_path + "Roboto-Medium.ttf", fn_italic= fonts_path +
                                                                     "Roboto-MediumItalic.ttf")
    Slope().run()