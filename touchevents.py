#!/usr/bin/python2 -tt
# Joakim Wesslen

import sys

"""
A program to translate touch input events from a device.
"""

def usage():
	print 50*"-"
	print "Usage description:"
	print "adb shell getevent | python touchevents.py event9"
	print "adb shell getevent -t | python touchevents.py event9"
	print 50*"-"


def decode_ev_type(evt):
	'''
	get the event type string
	'''
	evt = int(evt, 16)
	if evt == 0x00:
		evts = 'EV_SYN'
	elif evt == 0x01:
		evts = 'EV_KEY'
	elif evt == 0x02:
		evts = 'EV_REL'
	elif evt == 0x03:
		evts = 'EV_ABS'
	elif evt == 0x04:
		evts = 'EV_MSC'
	elif evt == 0x05:
		evts = 'EV_SW'
	elif evt == 0x11:
		evts = 'EV_LED'
	elif evt == 0x12:
		evts = 'EV_SND'
	elif evt == 0x14:
		evts = 'EV_REP'
	elif evt == 0x15:
		evts = 'EV_FF'
	elif evt == 0x16:
		evts = 'EV_PWR'
	elif evt == 0x17:
		evts = 'EV_FF_STATUS'
	elif evt == 0x1f:
		evts = 'EV_MAX'
	elif evt == 0x20:
		evts = 'EV_CNT'
	else:
		evts = 'UNKNOWN EV TYPE (%d)' % evt
	return evts


def decode_ev_key_code(code):
	'''
	get the event key code string
	'''
	code = int(code, 16)
	if code == 0x14a:
		cs = 'BTN_TOUCH'
	else:
		cs = 'UNKNOWN KEY CODE (%s)' % code
	return cs


def decode_ev_abs_code(code):
	'''
	get the event abs code string
	'''
	code = int(code, 16)
	if code == 0x00:
		cs = 'ABS_X'
	elif code == 0x01:
		cs = 'ABS_Y'
	elif code == 0x02:
		cs = 'ABS_Z'
	elif code == 0x18:
		cs = 'ABS_PRESSURE'
	elif code == 0x19:
		cs = 'ABS_DISTANCE'
	elif code == 0x1c:
		cs = 'ABS_TOOL_WIDTH'
	elif code == 0x20:
		cs = 'ABS_VOLUME'
	elif code == 0x28:
		cs = 'ABS_MISC'
	elif code == 0x30:
		cs = 'ABS_MT_TOUCH_MAJOR'
	elif code == 0x31:
		cs = 'ABS_MT_TOUCH_MINOR'
	elif code == 0x32:
		cs = 'ABS_MT_WIDTH_MAJOR'
	elif code == 0x33:
		cs = 'ABS_MT_WIDTH_MINOR'
	elif code == 0x34:
		cs = 'ABS_MT_ORIENTATION'
	elif code == 0x35:
		cs = 'ABS_MT_POSITION_X'
	elif code == 0x36:
		cs = 'ABS_MT_POSITION_Y'
	elif code == 0x37:
		cs = 'ABS_MT_TOOL_TYPE'
	elif code == 0x38:
		cs = 'ABS_MT_BLOB_ID'
	elif code == 0x39:
		cs = 'ABS_MT_TRACKING_ID'
	elif code == 0x3a:
		cs = 'ABS_MT_PRESSURE'
	elif code == 0x3f:
		cs = 'ABS_MAX'
	elif code == 0x40:
		cs = 'ABS_CNT'
	else:
		cs = 'UNKNOWN ABS CODE (%s)' % code
	return cs


def decode_ev_syn_code(code):
	'''
	get the event syn code string
	'''
	code = int(code, 16)
	if code == 0x00:
		cs = 'SYN_REPORT'
	elif code == 0x01:
		cs = 'SYN_CONFIG'
	elif code == 0x02:
		cs = 'SYN_MT_REPORT'
	else:
		cs = 'UNKNOWN SYN CODE (%d)' % code
	return cs


def decode_event_line(line):
	'''
	Decode the line with event data
	'''
	event_type = line[21:24]
	evt = decode_ev_type(event_type)

	event_code = line[25:29]
	if evt == 'EV_ABS':
		evc = decode_ev_abs_code(event_code)
	elif evt == 'EV_KEY':
		evc = decode_ev_key_code(event_code)
	elif evt == 'EV_SYN':
		evc = decode_ev_syn_code(event_code)
	else:
		evc = 'UNKNOWN EV TYPE CODE (%d)' % evt

	event_value = line[30:38]
	if evc == 'SYN_REPORT':
		evv = str(int(event_value, 16)) + '\n\n'
	else:
		evv = str(int(event_value, 16)) + '\n'

	res = evt + ' ' + evc + ' ' + evv
	return res


def main():
	# Event to look for
	ev = '/dev/input/' + sys.argv[1] + ': '
	# Parse an event from STDIN.
	for line in sys.stdin:
		t = line.find(ev)
		if t == 0:
			ret = decode_event_line(line)
			print ret
		if t > 0:
			timestamp = line[:t]
			ret = decode_event_line(line[t:])
			print timestamp + ret


if __name__ == '__main__':
	main()

