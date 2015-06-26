#!/usr/bin/env python

import optparse
import time


def check_time(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False


def set_commands_for_sssr():
    print 'setting commands for sssr', options.sssr


def set_commands_for_time():
    print 'setting commands for time', options.time


if __name__ == '__main__':
    usage = 'Tool for creating an at job to turn on or off tellstick devices'

    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-c', '--command',
                      type='choice',
                      dest='command',
                      choices=['on', 'off'],
                      action='store',
                      help='Turn on or off')
    parser.add_option('-s', '--sssr',
                      action='store_true',
                      default=False,
                      help='Use sunset and sunrise for time')
    parser.add_option('-t', '--time',
                      action='store',
                      dest='time',
                      help='Use supplied time, ex 12:00')
    parser.add_option('-l', '--long',
                      action='store',
                      dest='long',
                      help='Longitude for location')
    parser.add_option('-a', '--lat',
                      action='store',
                      dest='lat',
                      help='Latitude for location')


(options, args) = parser.parse_args()

# print options
# print 'sssr:', options.sssr
# print 'time:', options.time

if (options.sssr and options.time is not None or
        options.time is None and not options.sssr):
    parser.error('you must use either time or sssr')

elif options.lat is None and options.long is None and options.time is None:
    parser.error('you need to set both lat and long')

elif options.sssr:
    # get on and off time from sunrise sunset
    set_commands_for_sssr()

elif options.time is not None and options.command is None:
    parser.error('you need to set command when using time')

if options.time is not None and options.command is not None:
    if check_time(options.time):
        # commands
        set_commands_for_time()
    else:
        parser.error('invalid time specified')


