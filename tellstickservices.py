from flask import Flask, abort, render_template, make_response
from flask import jsonify
import optparse
import sys


TSS_NAME = "tellstick-services"
TEST_MODE = False
EXT_MODE = True
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    """Just the index request"""
    return render_template('index.html', devices=get_devices())


@app.route("/devices", methods=['GET'])
def devices():
    """On devices request return the list of all devices"""

    number_of_devices = td.getNumberOfDevices()

    if (number_of_devices >= 0):
        return jsonify(items=get_devices())
    else:
        # failed, return 503
        abort(503)


@app.route("/devices/<int:device_id>", methods=['GET'])
def device(device_id):
    """Get device status for device_id"""
    if (existing_device(device_id)):
        return jsonify(get_device_info(device_id))
    else:
        return make_response(jsonify({'error': 'invalid device_id'}), 400)


@app.route("/devices/<int:device_id>/<command>", methods=['POST'])
def controll_device(device_id, command):
    """Control device with device_id and command (on/off valid)"""
    supported_cmds = ['ON', 'OFF', 'on', 'off']

    if (not existing_device(device_id)):
        return make_response(jsonify({'error': 'invalid device_id'}), 400)

    if (command in supported_cmds):
        if (command.upper() == 'ON'):
            rc = td.turnOn(device_id)
        elif (command.upper() == 'OFF'):
            rc = td.turnOff(device_id)
        else:
            rc = -1

            if (rc == 0):
                return jsonify(get_device_info(device_id))
            else:
                return make_response(jsonify(
                    {'error': 'failed to execute command',
                     'deviceId': device_id}), 500)

    else:
        return make_response(jsonify({'error': 'invalid command'}), 400)


def existing_device(device_id):
    for device in get_devices():
        if (device['deviceId'] == device_id):
            return True
        return False


def get_devices():
    result = []
    number_of_devices = td.getNumberOfDevices()

    if (number_of_devices >= 0):
        for i in range(number_of_devices):
            device_id = td.getDeviceId(i)
            result.append(get_device_info(device_id))

        return result


def get_device_info(device_id):
    name = td.getName(device_id)
    status = td.lastSentCommand(device_id, readable=True)
    return {'deviceId': device_id, 'deviceName': name, 'status': status}


def init_opts():
    usage = "Support the following arguments"

    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      default=False, help="Run in debug mode")

    parser.add_option("-t", "--test",
                      action="store_true", dest="testmode",
                      default=False,
                      help="Run in test mode, no interaction with telldusd")

    parser.add_option("-l", "--local",
                      action="store_true", dest="local_only",
                      default=False, help="Only run on localhost")

    return parser.parse_args()


def handle_opts():
    global TEST_MODE
    global EXT_MODE

    (options, args) = init_opts()
    if options.debug:
        print "starting in debug mode"
        app.debug = True

    if options.testmode:
        print "starting in test mode, no interactin with telldus"
        TEST_MODE = True

    if options.local_only:
            EXT_MODE = False


def app_init():
    global TEST_MODE
    global td

    if TEST_MODE:
        print "loading simulator"
        import simulator
        td = simulator.tdsim

    else:
        try:
            print "loading pytelldus"
            import pytelldus
            td = pytelldus.td
            td.init(defaultMethods=td.TELLSTICK_TURNON | td.TELLSTICK_TURNOFF)
        except OSError:
            # exit since we can't work without telldusd
            print "Can't load telldus libs"
            sys.exit(1)


if __name__ == "__main__":
    handle_opts()
    app_init()
    if EXT_MODE:
        app.run(host='0.0.0.0')
else:
    app.run()
