#!/usr/bin/env python
import cmd
from datetime import datetime
import sys

from models import Client, TimeCard
from settings import DATABASE as db

DATE_FORMAT = '%Y/%m/%d'
TIME_FORMAT = '%H:%M'

HEADER = ('id#', 'CLIENT', 'DATE', 'START', 'END')
TIMECARD = '{:^3}' + '{:^30}{:^15}{:^8}{:^8}'


def print_headers():
    print(TIMECARD.format(*HEADER))


class EditCmd(cmd.Cmd):
    prompt = '(edit)'
    timecard = None

    def __init__(self, arg=None):
        super(EditCmd, self).__init__()
        if arg:
            self.timecard = TimeCard.select().where(TimeCard.id == arg).get()
        else:
            self.timecard = TimeCard()

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
        print_headers()
        print(TIMECARD.format(
            self.timecard.id,
            self.timecard.client.name,
            self.timecard.date.strftime('%Y/%m/%d'),
            self.timecard.start.strftime('%H:%M'),
            self.timecard.end.strftime('%H:%M')))

    def do_return(self, arg):
        return True


class HourCmd(cmd.Cmd):
    prompt = '(hour)'

    def __init__(self, initialize=False):
        super(HourCmd, self).__init__()
        if initialize:
            db.create_tables([Client, TimeCard])

    def do_add(self, arg):
        cmd = EditCmd()
        cmd.cmdloop()
        # date = input('Date? (YYYY/MM/DD) ')
        # start = input('Start time? (HH:MM) ')
        # end = input('End time? (HH:MM) ')
        # client = Client.select().where(Client.slug == arg).get()
        # date_string = '2017/07/01'
        # date = datetime.strptime(date_string, DATE_FORMAT)

        # start_string = '06:00'
        # start = datetime.strptime(start_string, TIME_FORMAT)
        # end_string = '07:00'
        # end = datetime.strptime(end_string, TIME_FORMAT)
        # TimeCard(
        #     date=date.date(),
        #     start=start.time(),
        #     end=end.time(),
        #     client=client).save()

    def do_date(self, arg):
        print(datetime.date.today())

    def do_edit(self, arg):
        cmd = EditCmd(arg)
        cmd.cmdloop()

    def do_list(self, arg):
        tc_select = TimeCard.select()

        if arg:
            tc_select = tc_select.join(Client).where(Client.slug == arg)

        print_headers()
        for timecard in tc_select:
            print(TIMECARD.format(
                timecard.id,
                timecard.client.name,
                timecard.date.strftime('%Y/%m/%d'),
                timecard.start.strftime('%H:%M'),
                timecard.end.strftime('%H:%M')))
        print('end')

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
