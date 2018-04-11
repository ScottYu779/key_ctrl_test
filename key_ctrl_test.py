# Copyright (c) 2018 huituo
# author:yuhs <hongsong.yu2010@gmail.com>

## --------------------------------------------------------------------------
## Copyright (c) 2018 -      excavator, huituo
##
## $Date:        2018-01-25
## $Revision:    v0.1
##
## Project:      Motor Controller for minestar
## Author:       yuhs <hongsong.yu2010@gmail.com>
## --------------------------------------------------------------------------

#History:
# Version 0.1
#	Initial protopyte by yuhs
#


#!/usr/bin/env python
import roslib
roslib.load_manifest('key_ctrl_test')
import rospy

from msgs_ht.msg import Key_Ctrl_Data_Ht

import sys
import select
import termios
import tty
import std_srvs.srv

msg = """
Reading from the keyboard  and Publishing to Key_Ctrl_Data_Ht!
---------------------------
Moving around:
		w 
a		s		d
			up
left  stop	right


anything else : stop and brake


CTRL-C to quit
"""

moveBindings = {
    'w': (1, 0, 0),
    's': (0, 1, 0),
    'a': (1, 0, -1),
    'd': (1, 0, 1),
}


speedBindings = {
    'i': (1, 0),
    'k': (-1, 0),
    'l': (0, 1),
    'j': (0, -1),
}


def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key


def data_print(power_state, brake_state, turn, max_vel, max_steer_angular):
  	return "power_state:%s \t brake_state:%s \t turn:%s \t max_vel:%s \t max_steer_angular:%s" % (power_state, brake_state, turn, max_vel, max_steer_angular)


if __name__ == "__main__":
	settings = termios.tcgetattr(sys.stdin)

	pub_manual = rospy.Publisher('cmd_vel_manual', Key_Ctrl_Data_Ht, queue_size=1)
	rospy.init_node('teleop_twist_keyboard')

	speed = rospy.get_param("~speed", 2)
	turn = rospy.get_param("~turn", 1.0)

	power_state = 0
	brake_state = 0
	turn = 0
	max_vel = 0
	max_steer_angular = 0
	try:
		print msg

		while(1):
			key = getKey()
			if key in moveBindings.keys():
				power_state = moveBindings[key][0]
				brake_state = moveBindings[key][1]
				turn = moveBindings[key][2]

				print data_print(power_state, brake_state, turn,
				                 max_vel, max_steer_angular)
			elif key in speedBindings.keys():
				max_vel += speedBindings[key][0]
				max_steer_angular += speedBindings[key][1]

				print data_print(power_state, brake_state, turn,
				                 max_vel, max_steer_angular)
			else:
				power_state = 0
				brake_state = 0
				turn = 0
				max_vel = 0
				max_steer_angular = 0

				print data_print(power_state, brake_state, turn,
				                 max_vel, max_steer_angular)
			if (key == '\x03'):
				break

			Key_Ctrl_Data = Key_Ctrl_Data_Ht()
			Key_Ctrl_Data.power_state = power_state
			Key_Ctrl_Data.brake_state = brake_state
			Key_Ctrl_Data.turn = turn
			Key_Ctrl_Data.max_vel = max_vel
			Key_Ctrl_Data.max_steer_angular = max_steer_angular
			##print "test"
			pub_manual.publish(Key_Ctrl_Data)
	except:
		print "e"

	finally:
		Key_Ctrl_Data = Key_Ctrl_Data_Ht()
		pub_manual.publish(Key_Ctrl_Data)

		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
