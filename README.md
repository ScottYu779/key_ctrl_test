# teleop_twist_keyboard
Generic Keyboard Teleop for ROS.
added manual override control.
press d to publish cmd_vel on /cmd_vel_manual and request a service named /serial_bot_node/manual_cmd_srv for manual.
press a to publish on /cmd_vel.


#Launch
To run: `rosrun teleop_twist_keyboard teleop_twist_keyboard_new.py`

#Usage
```
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
		w 
a		s		d
		¡ü
¡û  stop	¡ú


anything else : stop and brake

esc to quit
```

