import logging

log = logging.getLogger(__name__)

APPNAME = 'Deluge'
REASON = 'Downloading torrents'

class DBusInhibitor:
    def __init__(self, name, path, interface, method=['Inhibit', 'UnInhibit']):
        self.name = name
        self.path = path
        self.interface_name = interface

        import dbus
        bus = dbus.SessionBus()
        devobj = bus.get_object(self.name, self.path)
        self.iface = dbus.Interface(devobj, self.interface_name)
        # Check we have the right attributes
        self._inhibit = getattr(self.iface, method[0])
        self._uninhibit = getattr(self.iface, method[1])

    def inhibit(self):
        log.info('Inhibit (prevent) suspend mode')
        self.cookie = self._inhibit(APPNAME, REASON)

    def uninhibit(self):
        log.info('Uninhibit (allow) suspend mode')
        self._uninhibit(self.cookie)

class GnomeSessionInhibitor(DBusInhibitor):
    TOPLEVEL_XID = 0
    INHIBIT_SUSPEND = 4

    def __init__(self):
        DBusInhibitor.__init__(self, 'org.gnome.SessionManager',
                               '/org/gnome/SessionManager',
                               'org.gnome.SessionManager',
                               ['Inhibit', 'Uninhibit'])

    def inhibit(self):
        log.info('Inhibit (prevent) suspend mode')
        self.cookie = self._inhibit(APPNAME,
                                    GnomeSessionInhibitor.TOPLEVEL_XID,
                                    REASON,
                                    GnomeSessionInhibitor.INHIBIT_SUSPEND)


if __name__ == "__main__":
    x=GnomeSessionInhibitor ()
    x.inhibit()
    input("Standby ist ausgesetzt")
