from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import os


class SettingsScreen(MDScreen):
    dark_mode = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ScrollView to allow vertical positioning from top
        scroll = ScrollView(size_hint=(1, 1))
        container = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20,
            size_hint_y=None
        )
        container.bind(minimum_height=container.setter("height"))

        # Horizontal row: Dark Mode label + Switch
        darkmode_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
        darkmode_label = MDLabel(text="Dark Mode", halign="left", size_hint_x=None, width=100)
        self.switch = MDSwitch(active=self.dark_mode)
        self.switch.bind(active=self.toggle_dark_mode)
        darkmode_row.add_widget(darkmode_label)
        darkmode_row.add_widget(self.switch)
        container.add_widget(darkmode_row)

        # Backup Button
        backup_button = MDRaisedButton(text="Backup Data", size_hint=(None, None), size=(150, 40))
        backup_button.bind(on_release=lambda x: self.backup_data())
        container.add_widget(backup_button)

        # PDF Report Button
        pdf_button = MDRaisedButton(text="Generate PDF Report", size_hint=(None, None), size=(200, 40))
        pdf_button.bind(on_release=lambda x: self.generate_pdf_report())
        container.add_widget(pdf_button)

        scroll.add_widget(container)
        self.add_widget(scroll)

    def toggle_dark_mode(self, instance, value):
        self.dark_mode = value
        if value:
            self.parent_app.theme_cls.theme_style = "Dark"
            Window.clearcolor = (0.1, 0.1, 0.1, 1)
        else:
            self.parent_app.theme_cls.theme_style = "Light"
            Window.clearcolor = (1, 1, 1, 1)

    def backup_data(self):
        print("Backup started...")
        import time
        time.sleep(1)
        print("Backup completed!")

    def generate_pdf_report(self):
        filename = f"settings_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(os.getcwd(), filename)

        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "App Settings Report")

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 100, f"Dark Mode Enabled: {'Yes' if self.dark_mode else 'No'}")
        c.drawString(50, height - 130, f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        c.showPage()
        c.save()

        print(f"PDF report generated: {filepath}")


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        screen = SettingsScreen()
        screen.parent_app = self
        return screen


if __name__ == "__main__":
    MyApp().run()
