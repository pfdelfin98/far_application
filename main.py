import time
import cv2
import numpy as np
import requests
import sqlite3
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.config import Config
# from kivy.uix.floatlayout import FloatLay
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics.texture import Texture

from kivy.uix.floatlayout import FloatLayout

Window.size = (310, 670)

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()

class LoadingPage(Screen):
    def __init__(self, **kwargs):
        super(LoadingPage, self).__init__(**kwargs)
        Clock.schedule_once(self.change_screen, 2)

    def change_screen(self, dt):
        self.manager.current = 'startpage'

class StartPage(Screen):
    pass

class LoginPage(Screen):
    def login_user(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.manager.current = 'homemenu'
            App.get_running_app().current_user_email = email
        else:
            self.show_popup("Error", "Invalid Email or Password")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()

class RegisterPage(Screen):
    def register_user(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        confirm_password = self.ids.confirm_password_input.text

        if password != confirm_password:
            self.show_popup("Error", "Passwords do not match")
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            self.show_popup("Success", "Registration successful!")
            self.manager.current = 'loginpage'
        except sqlite3.IntegrityError:
            self.show_popup("Error", "Account already exists")
        finally:
            conn.close()

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()

class HomeMenu(Screen):
    def __init__(self, **kwargs):
        super(HomeMenu, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 1.0)

    def update_time(self, dt):
        current_time = time.strftime("%I:%M:%S %p")
        self.ids.clock_label.text = current_time

class FirstAidMenu1(Screen):
    pass

class FirstAidMenu2(Screen):
    pass

class FirstAidMenu3(Screen):
    pass

# class CameraMenu(Screen):
#     def __init__(self, **kwargs):
#         super(CameraMenu, self).__init__(**kwargs)
#         self.capture = None

#     def on_enter(self):
#         self.capture = cv2.VideoCapture(0)
#         Clock.schedule_interval(self.update, 1.0 / 30.0)

#     def on_leave(self):
#         if self.capture:
#             self.capture.release()
#             Clock.unschedule(self.update)

#     def update(self, dt):
#         ret, frame = self.capture.read()
#         if ret:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frame = cv2.flip(frame, 0)
#             self.current_frame = frame
#             texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
#             texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
#             self.ids.camera_display.texture = texture


class CameraMenu(Screen):
    def __init__(self, **kwargs):
        super(CameraMenu, self).__init__(**kwargs)
        self.capture = None
        self.is_camera_active = False

    def start_camera(self):
        if not self.is_camera_active:
            self.capture = cv2.VideoCapture(0)  # Open default camera
            if not self.capture.isOpened():
                print("Error: Could not open the camera.")
                return
            self.is_camera_active = True
            Clock.schedule_interval(self.update, 1 / 30)  # Update at 30 FPS

    def stop_camera(self):
        if self.is_camera_active:
            self.capture.release()  # Release the camera resource
            Clock.unschedule(self.update)  # Stop the update loop
            self.is_camera_active = False

    def update(self, dt):
        if self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                # Convert frame to texture
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
                self.ids.camera_display.texture = texture

    def on_leave(self):
        self.stop_camera()  # Stop the camera when the screen is left
   

                         
class ProcessingPage(Screen):
    def __init__(self, **kwargs):
        super(ProcessingPage, self).__init__(**kwargs)

class BruisePage(Screen):
    pass

class AbrasionPage(Screen):
    pass

class BurnPage(Screen):
    pass

class MinorWoundPage(Screen):
    pass

class BleedingPage(Screen):
    pass

class SprainPage(Screen):
    pass

class LacerationPage(Screen):
    pass

class PunctureWoundPage(Screen):
    pass

class BiteWoundPage(Screen):
    pass

class InflammationWoundPage(Screen):
    pass

class VenousWoundPage(Screen):
    pass

class PressureWoundPage(Screen):
    pass

class AmbulanceMenu1(Screen):
    pass

class AmbulanceMenu2(Screen):
    pass

class SettingsMenu1(Screen):
    def on_enter(self):
        # Display the logged in user's email and password
        email = App.get_running_app().current_user_email
        self.ids.email_label.text = f"{email}"
        
        # Fetch password from the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        password = cursor.fetchone()
        conn.close()
        
        if password:
            self.ids.password_label.text = f"{password[0]}"

class SettingsMenu2(Screen):
    def save_changes(self):
        email = self.ids.email_input.text
        new_password = self.ids.password_input.text
        confirm_password = self.ids.confirm_password_input.text

        current_email = App.get_running_app().current_user_email

        if new_password != confirm_password:
            self.show_popup("Error", "Passwords do not match")
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            # Update email and password in the database
            cursor.execute("UPDATE users SET email = ?, password = ? WHERE email = ?", (email, new_password, current_email))
            conn.commit()
            App.get_running_app().current_user_email = email  # Update the current user's email
            self.show_popup("Success", "Successfully Saved!")
            self.manager.current = 'settingsmenu1'
            # Update the email and password display in SettingsMenu1
            settings_menu1 = self.manager.get_screen('settingsmenu1')
            settings_menu1.ids.email_label.text = email
            settings_menu1.ids.password_label.text = new_password  # Update password display
        except sqlite3.Error as e:
            self.show_popup("Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()

class ScreenManagement(ScreenManager):
    pass

class WindowManager(ScreenManager):
    pass

file = Builder.load_file('FirstAidResponder.kv')

class FirstAidResponderApp(App):
    def build(self):
        self.icon = "asset/Logo.png"
        return file
    
FirstAidResponderApp().run()