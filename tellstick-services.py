from flask import Flask, abort, redirect, url_for, render_template
import simplejson
import json
import optparse
import sys


TSS_NAME="tellstick-services"
TEST_MODE=False
EXT_MODE=True
app = Flask(__name__)


@app.route("/", methods=['GET'])
def start():
	"""Just the index request"""
	return render_template('index.html', devices=json.loads(status()))


@app.route("/status", methods=['GET'])
def status():
	"""On status request return the list of all devices and their status"""

	result = []
	number_of_devices = td.getNumberOfDevices()

	if (number_of_devices >= 0):
		for i in range(number_of_devices):
			device_id = td.getDeviceId(i)
			result.append(get_status_for_device(device_id))

		return json.dumps(result)
	else:
		# failed, return 503
		abort(503)


@app.route("/device/<int:device_id>", methods=['GET'])
def device_status(device_id):
	"""Get device status for device_id"""
	return json.dumps(get_status_for_device(device_id))


@app.route("/device/<int:device_id>/<command>", methods=['POST'])
def controll_device(device_id, command):
	"""Control device with device_id and command (on/off valid)"""
	supported_cmds = ['ON', 'OFF','on','off']
	if (command in supported_cmds):
		if (command.upper() == 'ON'):
			rc = td.turnOn(device_id)
		elif (command.upper() == 'OFF'):
			rc = td.turnOff(device_id)
		else:
			rc = -1

		if (rc == 0):
			return json.dumps(get_status_for_device(device_id))
		else:
			return json.dumps({'error':'failed to execute command'})

	else:
		return json.dumps({'error':'invalid command'})


def get_status_for_device(device_id):
	name = td.getName(device_id)
	status = td.lastSentCommand(device_id, readable = True)
	return {'deviceId':device_id,'deviceName':name,'status':status}

def init_opts():
	usage = "Support the following arguments"

	parser = optparse.OptionParser(usage = usage)
	parser.add_option("-d", "--debug",
						action="store_true", dest="debug",
						default=False,help="Run in debug mode")

	parser.add_option("-t", "--test",
						action="store_true", dest="testmode",
						default=False,help="Run in test mode, no interaction with telldusd")

	parser.add_option("-l", "--local",
						action="store_true", dest="local_only",
						default=False,help="Only run on localhost")

	return parser.parse_args()


def handle_opts():
	global TEST_MODE
	global EXT_MODE

	(options, args) =init_opts()
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
			td.init(defaultMethods = td.TELLSTICK_TURNON | td.TELLSTICK_TURNOFF)
		except OSError:
			if TEST_MODE:
				# we're on a machine without telldus installed, ok if simulation mode
				pass
			else:
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
