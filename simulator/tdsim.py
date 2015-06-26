# deviceid, devicename, status

device1 = [1, 'Device 1', 'OFF']
device2 = [2, 'Device 2', 'OFF']
device3 = [3, 'Device 3', 'OFF']

unknown = [-1, 'UNKNOWN', '-']

devices = {0: device1, 1: device2, 2: device3}


def getNumberOfDevices():
    return len(devices)


def getDeviceId(i):
    if i in devices:
        return devices[i][0]
    else:
        return unknown[0]


def getDeviceIdFromStr(s):
    for i in devices.keys():
        if devices[i][1] == s:
            return devices[i][1]

    return unknown[1]


def getName(deviceId):
    for i in devices.keys():
        if (devices[i][0] == deviceId):
            return devices[i][1]

    return unknown[1]


def lastSentCommand(intDeviceId, methodsSupported=None, readable=False):
    for i in devices.keys():
        if devices[i][0] == intDeviceId:
            return devices[i][2]

    return unknown[2]


def turnOn(intDeviceId):
    if (intDeviceId != 3):
        update_device_status(intDeviceId, 'ON')
        return 0
    else:
        return 1


def turnOff(intDeviceId):
    update_device_status(intDeviceId, 'OFF')
    return 0


def update_device_status(intDeviceId, status):
    print 'updating device %s to status %s' % (intDeviceId, status)
    for i in range(getNumberOfDevices()):
        if devices[i][0] == intDeviceId:
            devices[i][2] = status
