#!/usr/bin/env python
import cmd
from datetime import datetime
import sys
import traceback

from peewee import SelectQuery

from models import Client, TimeCard
from settings import DATABASE as db

DATE_FORMAT = '%Y/%m/%d'
TIME_FORMAT = '%H:%M'

HEADER = ('id#', 'CLIENT', 'DATE', 'START', 'END')
TIMECARD = '{:^3}' + '{:^30}{:^15}{:^8}{:^8}'


def print_timecards(data):
    print(TIMECARD.format(*HEADER))
    if not isinstance(data, (list, SelectQuery)):
        data = [data]
    for timecard in data:
        print(TIMECARD.format(
            timecard.id,
            timecard.client.name,
            timecard.date.strftime('%Y/%m/%d'),
            timecard.start.strftime('%H:%M'),
            timecard.end.strftime('%H:%M')))


class EditCmd(cmd.Cmd):
    prompt = '(edit)'
    timecard = None

    def __init__(self, pk=None, client_slug=None):
        super(EditCmd, self).__init__()
        if pk:
            self.timecard = TimeCard.select().where(TimeCard.id == pk).get()
        if client_slug:
            client = Client.select().where(Client.slug == client_slug).get()
            self.timecard = TimeCard(client=client)

    def do_start(self, arg):
        self.timecard.start = datetime.strptime(arg, TIME_FORMAT)

    def do_end(self, arg):
        self.timecard.end = datetime.strptime(arg, TIME_FORMAT)

    def do_date(self, arg):
        self.timecard.date = datetime.strptime(arg, DATE_FORMAT)

    def do_listclient(self, arg):
        for client in Client.select():
            print(client.name + '(%s)' % client.slug)

    def do_client(self, arg):
        self.timecard.client = Client.select().where(Client.slug == arg).get()

    def do_save(self, arg):
        self.timecard.save()
        return True

    def do_print(self, arg):
        try:
            print_timecards(self.timecard)
        except Exception:
            traceback.print_exc()

    def do_delete(self, arg):
        delete = None
        print('Deleting:')
        self.do_print(arg)
        delete = True if input('Are you sure?[y/n] ') == 'y' else False
        if delete:
            self.timecard.delete_instance()
            print('Record deleted')
            return True

    def do_return(self, arg):
        return True


class HourCmd(cmd.Cmd):
    prompt = '(hour)'

    def __init__(self, initialize=False):
        super(HourCmd, self).__init__()
        if initialize:
            db.create_tables([Client, TimeCard])

    def do_add(self, arg):
        cmd = EditCmd(client_slug=arg)
        cmd.cmdloop()

    def do_date(self, arg):
        print(datetime.date.today())

    def do_edit(self, arg):
        cmd = EditCmd(pk=arg)
        cmd.cmdloop()

    def do_list(self, arg):
        tc_select = TimeCard.select()

        if arg:
            tc_select = tc_select.join(Client).where(Client.slug == arg)

        print_timecards(tc_select)

    def do_read(self, arg):
        print('read hours')

    def do_exit(self, arg):
        return True


if __name__ == '__main__':
    db.connect()
    initialize = False
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        initialize = True
    cmd = HourCmd(initialize)
    if initialize:
        Client(name='Coldwaterwave', slug='coldwaterwave').save()
        Client(name='Partner Fund Management', slug='pfm').save()
        Client(name='Teacheasy', slug='teacheasy').save()
    cmd.cmdloop()
