# deviceid, devicename, status

device1 = [1,'Device 1','OFF']
device2 = [2,'Device 2','OFF']
device3 = [3,'Device 3','OFF']

unknown = [-1,'UNKNOWN','-']

devices = {0:device1,1:device2,2:device3}

def getNumberOfDevices():
    return len(devices)


def getDeviceId(i):
    if devices.has_key(i):
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
        if devices[i][0] == deviceId:
            return devices[i][1]
    else:
        return unknown[1]


def lastSentCommand(intDeviceId, methodsSupported = None, readable = False):
    for i in devices.keys():
        if devices[i][0] == intDeviceId:
            return devices[i][2]

    return unknown[2]


def turnOn(intDeviceId):
    update_device_status(intDeviceId,'ON')
    return 0


def turnOff(intDeviceId):
    update_device_status(intDeviceId,'OFF')
    return 0


def update_device_status(intDeviceId, status):
    for i in range(getNumberOfDevices()):
        if devices[i][0] == intDeviceId:
            devices[i][2] = status
