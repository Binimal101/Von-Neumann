import datetime

def unpack_time():
	now = datetime.datetime.now(); hour, minute = now.hour, str(now.minute)
	ampm = "AM"
	#changes the time from military to standard
	if len(minute) == 1:
		minute = "0" + minute
	if hour > 12:
		ampm = "PM"
		hour -= 12
	elif hour == 12:
		ampm = "PM"
	elif hour == 0:
		hour = 12
		ampm = "AM"
	else:
		ampm = "AM"
	return hour, minute, ampm


def unpack_math(message):
	equation = ""
	look_for = "1234567890+-/*^.()"
	for char in message:
		equation = equation + (char if char in look_for else "")
	return equation