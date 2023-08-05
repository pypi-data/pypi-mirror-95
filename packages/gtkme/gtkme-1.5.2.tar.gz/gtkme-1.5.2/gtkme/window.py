#
# Copyright 2012 Martin Owens <doctormo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#
"""
Wraps the gtk windows with something a little nicer.
"""
import logging
try:
    from xsdvalidate import Validator
except ImportError:
    Validator = None
from .main import FakeWidget, LoopDe
from gi.repository import Gtk, Gdk, GLib, GObject

PROPS = {
    'Box': ['expand', 'fill', 'padding', 'pack-type'],
    'Grid': ['top-attach', 'left-attach', 'height', 'width'],
    'Table': ['top-attach', 'left-attach', 'bottom-attach', 'right-attach'],
}

def protect(cls, *methods):
    """Simple check for protecting an inherrited class from having
    certain methods over-ridden"""
    if type(cls) != type:
        cls = type(cls)
    for method in methods:
        if method in cls.__dict__:
            raise RuntimeError("%s in %s has protected def %s()" \
                % (cls.__name__, cls.__module__, method))


class Window(object):
    """
    This wraps gtk windows and allows for having parent windows as well
    as callback events when done and optional quiting of the gtk stack.

    name = 'name-of-the-window'

    Should the window be the first loaded and end gtk when closed:

    primary = True/False

    A list of all the field elements in the window that should be given
    to the callback when exiting:

    fields = [ 'widget-name', ... ]

    """
    name    = None
    primary = True
    fields  = []

    def __init__(self, gapp, name=None):
        self.gapp = gapp
        self.name = name or self.name

        # Setup the gtk app connection
        self.w_tree = Gtk.Builder()
        self.widget = self.w_tree.get_object
        self.w_tree.set_translation_domain(gapp.app_name)
        self.w_tree.add_from_file(gapp.ui_file(self.name))

        # Setup the gtk builder window
        self.window = self.widget(self.name)
        if not self.window:
            raise Exception("Missing window widget '%s' from '%s'" % (
                self.name, gapp.ui_file(self.name)))

        # Give us a window id to track this window
        self.wid = str(hash(self.window))

    def extract(self):
        """Extract this window's container for use in other apps"""
        for child in self.window.get_children():
            self.window.remove(child)
            return child

    def init(self, parent=None, callback=None, **kwargs):
        if not 'replace' in kwargs:
            protect( self, 'destroy', 'exit', 'load_window', 'proto_window' )
        self.args     = kwargs
        # Set object defaults
        self.dead     = False
        self.parent   = parent
        self.callback = callback

        self.w_tree.connect_signals(self)

        # These are some generic convience signals
        self.window.connect('destroy', self.exit)

        # If we have a parent window, then we expect not to quit
        if self.parent:
            self.window.set_transient_for(self.parent)
            self.parent.set_sensitive(False)

        # We may have some more gtk widgets to setup
        self.load_widgets(**self.args)
        self.window.show()

    def __getattr__(self, name):
        """Catch signals with window names that need to be stripped."""
        # Be warned all ye who enter here, GTK will eat your errors and
        # exceptions and simply complain about missing signals. This happened
        # to me, don't let it happen to you!
        if self.name+'_' in name:
            function = name.replace(self.name+'_', '')
            return getattr(self, function)
        raise AttributeError("Window '%s' has no method or property '%s'" %(
            type(self).__name__, name))

    def load_window(self, name, *args, **kwargs):
        """Load child window, automatically sets parent"""
        kwargs['parent'] = self.window
        return self.gapp.load_window(name, *args, **kwargs)

    def load_window_extract(self, name, **kwargs):
        """Load a child window as a widget container"""
        window = self.gapp.proto_window(name)
        window.load_widgets(**kwargs)
        return window.extract()

    def load_widgets(self):
        """Child class should use this to create widgets"""
        pass

    def destroy(self, widget=None):
        """Destroy the window"""
        logging.debug("Destroying Window %s" % self.name)
        self.window.destroy()
        # We don't need to call self.exit(),
        # handeled by window event.

    def pre_exit(self):
        """Internal method for what to do when the window has died"""
        if self.callback:
            self.callback(self)

    def exit(self, widget=None):
        """Called when the window needs to exit."""
        if not widget or not isinstance(widget, Gtk.Window):
            self.destroy()
        # Clean up any required processes
        self.pre_exit()
        if self.parent:
            # We assume the parent didn't load another gtk loop
            self.parent.set_sensitive(True)
        # Exit our entire app if this is the primary window
        # Or just remove from parent window list, which may still exit.
        if self.primary:
            logging.debug("Exiting the application")
            self.gapp.exit()
        else:
            logging.debug("Removing Window %s from parent" % self.name)
            self.gapp.remove_window(self)
        # Now finish up what ever is left to do now the window is dead.
        self.dead = True
        self.post_exit()
        return widget

    def post_exit(self):
        """Called after we've killed the window"""
        pass

    def if_widget(self, name):
        """
        Attempt to get the widget from gtk, but if not return a fake that won't
        cause any trouble if we don't further check if it's real.
        """
        return self.widget(name) or FakeWidget(name)

    def clone_widget(self, widget, deep=False):
        """
        Attempt to create a clone of a widget named in the GtkBuilder. This is
        trying to use glade files as templates for sections of the code.
        """
        source = widget
        if isinstance(widget, str):
            source = self.widget(widget)
        dest = source.__class__()
        for setname in dir(source):
            if setname[:4] == "set_":
                value = None
                name = setname[4:]
                if name[:5] == 'from_':
                    name = name[5:]
                getname = 'get_' + name
                if name in ['buffer', 'data', 'parent']:
                    continue
                if hasattr(source, getname):
                    try:
                        value = getattr(source, getname)()
                    except TypeError:
                        continue
                elif hasattr(source, name):
                    value = getattr(source, name )
                if value == None:
                    continue
                if not isinstance(value, tuple):
                    value = tuple([value])
                try:
                    getattr(dest, setname)(*value)
                except TypeError:
                    continue
        if deep and isinstance(source, Gtk.Container):
            for child in source.get_children():
                self.clone_and_add(child, dest, True)
        return dest

    def clone_and_add(self, widget, container, deep=False):
        """Clones the widget and packs it into the container in the same way"""
        parent = widget.get_parent()
        nwidget = self.clone_widget(widget, deep=deep)
        container.add(nwidget)
        ctype = type(parent).__name__
        # Fix arangements and packing
        if ctype in PROPS.keys():
            for attach in PROPS[ctype]:
                # Introspection is very pokey.
                value = GObject.Value()
                value.init(GObject.TYPE_LONG)
                parent.child_get_property(widget, attach, value)
                container.child_set_property(nwidget, attach, value)

    def replace(self, old, new):
        """Replace the old widget with the new widget"""
        if isinstance(old, str):
            old = self.widget(old)
        if isinstance(new, str):
            new = self.widget(new)
        parent = old.get_parent()
        if parent is not None:
            parent.remove(old)
            parent.add(new)

    def double_click(self, widget, event):
        """This is the cope with gtk's rotten support for mouse events"""
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            return self.apply(widget)


class ChildWindow(Window):
    """
    Base class for child window objects, these child windows are typically
    window objects in the same gtk builder file as their parents. If you just want
    to make a window that interacts with a parent window, use the normal
    Window class and call with the optional parent attribute.
    """
    primary = False
