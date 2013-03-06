'''Pop up notifier icons when journal events happen'''

import sys
import dbus
import argparse
from systemd import journal

__version__ = '0.0.1'

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--version', action='version',
                    version=__version__)
parser.add_argument('-l', '--level', type=int, choices=range(8),
                    help='Filter messages by priority')

def notify(summary, body='', app_name='', app_icon='edit-cut',
           timeout=5000, actions=[], hints=[], replaces_id=0):

    session_bus = dbus.SessionBus()
    obj = session_bus.get_object('org.freedesktop.Notifications',
                                 '/org/freedesktop/Notifications')
    interface = dbus.Interface(obj, 'org.freedesktop.Notifications')
    interface.Notify(app_name, replaces_id, app_icon,
                     summary, body, actions, hints, timeout)

def create_reader(opts):
    r = journal.Reader()
    if opts.level:
        r.log_level(opts.level)
    return r

def loop(reader):
    while True:
        for event in reader:
            notify(event['MESSAGE'])
        reader.wait()

if __name__ == '__main__':
    opts = parser.parse_args()
    r = create_reader(opts)
    r.seek(0, journal.SEEK_END)
    loop(r)
