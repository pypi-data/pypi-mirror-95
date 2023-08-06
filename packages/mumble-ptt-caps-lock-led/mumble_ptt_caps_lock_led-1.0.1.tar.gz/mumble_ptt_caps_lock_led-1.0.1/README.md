# mumble_ptt_caps_lock_led
A python program to let the LED of your caps lock key display your mumble PTT state.

This is very nice if caps lock is also the PTT key.
To do that first disable the caos lock key: `setxkbmap -option ctrl:nocaps`

This program is split into two parts:
  - Script to update the LED using `/sys/`. This needs to be run as root.
  - Script to extract the PTT state from mumble.

The second script uses the dbus messages of mumble updating the taskbar icon.
For this to work, the taskbar icon needs to be enabled.
