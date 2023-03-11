import sys
import os
import random
import gi

gi.require_version('Gtk', '4.0')
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, GLib
from datetime import datetime


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Things will go here

        self.date_format = "%I:%M %p"
        self.images = self.get_images()

        self.mainoverlay = Gtk.Overlay()
        self.picture = Gtk.Picture.new_for_filename(self.images[self.pos])

        self.time = Gtk.Label()
        markup = self.build_font(datetime.now().strftime(self.date_format))
        self.time.set_markup(markup)

        self.time.set_valign(Gtk.Align.START)
        self.time.set_halign(Gtk.Align.START)

        self.button = Gtk.Button(label="Push", opacity=0)
        self.button.connect('clicked', self.onclick)

        self.mainoverlay.add_overlay(self.picture)
        self.mainoverlay.add_overlay(self.time)
        self.mainoverlay.add_overlay(self.button)
        self.set_child(self.mainoverlay)

        GLib.timeout_add_seconds(0.2, self.ontick)

    def get_images(self):
        self.pos = 0
        photo_path = os.path.join(os.getcwd(), "photos")

        # Create the photos list with the full path
        photos = [os.path.join(photo_path, file) for file in os.listdir(photo_path)]
        random.shuffle(photos)
        return photos

    def build_font(self, text):
        size = self.get_allocated_width() / 25
        fontdesc = f"monospace regular {size}"

        return f'<span font_desc="{fontdesc}">{text}</span>'

    def onclick(self, evt):
        print("Check for more pictures!")
        self.images = self.get_images()
        self.picture.set_filename(self.images[self.pos])
        self.pos += 1

    def ontick(self):
        markup = self.build_font(datetime.now().strftime(self.date_format))
        self.time.set_markup(markup)

        # Only change the picture on the 5s. 
        if datetime.now().second % 5 != 0:
            return True

        # If we hit the end, read the directory and shuffle.
        if self.pos >= len(self.images):
            self.pos = 0
            self.images = self.get_images()

        self.picture.set_filename(self.images[self.pos])
        self.pos += 1

        return True


class Application(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.fullscreen()
        self.win.present()


def main():
    """ Run the main application"""
    app = Application()
    return app.run(sys.argv)


if __name__ == '__main__':
    main()
