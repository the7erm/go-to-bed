#!/usr/bin/env python

import gtk
import gobject

class NotifyWindow(gtk.Window):
    def __init__(self, message="", keep_above=True, close_after=None, 
                       full_screen=False, close_on_click=False, decorated=False):
        gtk.Window.__init__(self)
        self.set_default_size(600, 400)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_keep_above(keep_above)

        self.eb = gtk.EventBox()
        self.add(self.eb)

        self.vbox_container = gtk.VBox()
        self.eb.add(self.vbox_container)

        self.label = gtk.Label(message)
        self.vbox_container.pack_start(self.label)
        self.set_decorated(decorated)

        self.show_all()

        if keep_above:
            gobject.timeout_add(1000, self.ensure_above)

        if close_after:
            gobject.timeout_add(10000, self.destroy_window)

        if full_screen:
            self.fullscreen()

        if close_on_click or not close_after:
            self.eb.connect("button_press_event", self.on_button_press_event)

    def on_button_press_event(self, *args, **kwargs):
        print "on_button_press_event:", args, kwargs
        self.destroy()

    def destroy_window(self, *args, **kwargs):
        print "destroy_window:", args, kwargs
        self.destroy()
        return False


    def ensure_above(self, *args, **kwargs):
        print "ensure_above:", args, kwargs
        self.set_keep_above(True)
        return False

if __name__ == "__main__":
    w = NotifyWindow("Works", close_on_click=True)
    gtk.main()