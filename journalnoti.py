import sys
import dbus
from systemd import journal

def notify(summary, body='', app_name='', app_icon='edit-cut',
           timeout=5000, actions=[], hints=[], replaces_id=0):

    session_bus = dbus.SessionBus()
    obj = session_bus.get_object('org.freedesktop.Notifications',
                                 '/org/freedesktop/Notifications')
    interface = dbus.Interface(obj, 'org.freedesktop.Notifications')
    interface.Notify(app_name, replaces_id, app_icon,
                     summary, body, actions, hints, timeout)
                               
def loop(reader):
    while True:
        for event in reader:
            notify(event['MESSAGE'])
        reader.wait()

if __name__ == '__main__':
    r = journal.Reader()
    r.seek(0, journal.SEEK_END)
    loop(r)
