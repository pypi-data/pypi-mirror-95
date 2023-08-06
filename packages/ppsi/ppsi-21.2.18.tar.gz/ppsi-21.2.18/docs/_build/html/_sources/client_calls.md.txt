Unless otherwise stated, interactive actions are handled by [launcher_menus](https://github.com/pradyparanjpe/launcher-menus.git).

Help
----

Display help message about command.

```sh
ppsi --help

ppsi -h

ppsi help
```

For help about a subcommand ``sub``

```sh
ppsi sub -h
```

Remote connection
-------------------

SSH

Remote connection details are handled interactively.
PPSID temporarily remembers the remote machines that were contacted untill a restart.

```sh
ppsi remote
```

Passwords
-----------

[PASS](http://www.passwordstore.org/)

Recall and generate passwords.

```sh
ppsi pass
```

Wifi
-----

[NMCLI](https://wiki.gnome.org/Projects/NetworkManager)

Discovers available wifi networks, connects to selected network. Offers password if needed.

```sh
ppsi wifi
```

Bluetooth
---------

[BLUEZ](http://www.bluez.org/)

```sh
ppsi bluetooth
```

Same as wifi, but for bluetooth


Sway Window Manager Workspaces
-----------

[SWAYMSG](https://swaywm.org/)

### Back to Latest

Performs action similar to swaymsg back_and_forth
Switches to the latest workspace

```sh
ppsi workspace latest
```

### Jump to Oldest

Allows cycling through all workspaces in an order from the the oldest to the latest

Especially usefull after the order of workspaces has been reversed

```sh
ppsi workspace oldest
```

### Reverse workspace order

Reverse the registered order of workspaces so that the oldest workspace becomes the latest.

```sh
ppsi workspace reverse
```

### Update

Update a workspace action (new, switch, cycle, etc)

Called automatically after workspace action through ``ppsi client``

```sh
ppsi workspace update
```

Volume
--------

[PULSEAUDIO](https://www.freedesktop.org/wiki/Software/PulseAudio/)

Adjust volume of the currently active channel and show visible feedback using [wob](https://github.com/francma/wob)

### Increase

Increase volume by ``change``%
``change`` defaults to 2

```sh
ppsi vol + [change]

ppsi vol up [change]
```

### Decrease

Decrease volume by ``change``%
``change`` defaults to 2

```sh
ppsi vol - [change]

ppsi vol down [change]
```

### Mute

Mute the channel

```sh
ppsi vol 0

ppsi vol mute
```

Brightness
-----------

[LIGHT](https://haikarainen.github.io/light/)

Same as ``Volume`` other than the option ``mute``

```sh
ppsi light {+,-,up,down} [change]
```

System
-------

[SYSTEMD](https://systemd.io/)

System calls

### Suspend

Suspend session

```sh
ppsi system suspend
```

### Poweroff

Poweroff session

```sh
ppsi system poweroff
```

### Reboot

Reboot session

```sh
ppsi system reboot
```

### Reboot to UEFI

Reboot the system with a request to open UEFI (BIOS)

```sh
ppsi system bios_reboot
```

PPSI Daemon Communication
-----------------------------

Communicate with ppsid.

<span style="color: red; font-size: 1.5em">This feature doesn't work currently</span>

```sh
ppsi comm [reload|quit]
```
