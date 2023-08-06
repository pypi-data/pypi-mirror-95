Source Code
================

[![source](https://github.githubassets.com/favicons/favicon.png)](https://github.com/pradyparanjpe/ppsi.git)
[Repository](https://github.com/pradyparanjpe/ppsi.git)

Documentation
=================

[![Documentation Status](https://readthedocs.org/projects/ppsi/badge/?version=latest)](https://ppsi.readthedocs.io/en/latest/?badge=latest)

===================================================================================

Installation
=============

MS Windows
----------

  - **Sorry**

Apple MacOS/OSX
---------------

  - **Please consider using a fancy paid App**

Linux
-----

  - Use python's pip to [install locally](#pip) for the user or ask ``pspman`` to do it.
  - *DO NOT INSTALL SYSTEMWIDE (ROOT)*.
  - You shouldn't have to supply root previleges or user-password during installation.

### Prerequisites
  - Enable pango markup language in tilingWM configuration file
  - Install an emoji font such as google-noto-emoji-color-fonts.noarch
  - Install:
    - python3 (obviously)
    - sway (obviously)
    - systemd
    - nmcli (NetworkManager)
    - bluez
    - pass
    - wob
    - pulseaudio
    - light
    - waypipe

### pip
Use python's package distribution "pip"

```sh
pip install --user ppsi
```

### pspman

Use [pspman](https://github.com/pradyparanjpe/pspman.git) for pre-releases, auto-updates and management

```sh
pspman -i https://github.com/pradyparanjpe/ppsi.git
```

Uninstallation
--------------

### Uninstall using pip

```sh
pip uninstall ppsi
```

### pspman

If pspman was used for installation, delete ppsi repository clone

```sh
pspman -d ppsi
```

===============================================================

What it does
=================

provides a python interface for
- workspace-specific keybindings for `$mod+Shift+Return`
- remote [ssh/waypipe]
- password-manager [pass]
- wifi [nmcli]
- bluetooth [bluez]
- reboot [systemd]
- poweroff [systemd]
- bios_reboot [systemd]
- suspend [systemd]
- volume [pulseaudio]
- brightness [ light]
- bar (a simple info-bar) showing:
  - OS Name
  - Network Speeds
  - Current IP
  - RAM Usage
  - CPU Usage
  - Core Temperature
  - Battery
  - Time

=====================================================================

Usage
======

pspbar
-------

Use subpackage ``pspbar`` as a minimalistic bar
  ```sh
  pspbar -m 10 1
  ```

configure
-----------

Copy [ppsi.yml](ppsi/server/config/ppsi.yml) to ``${HOME}/.config/sway/ppsi.yml``

pip generally installs packages in /home/.local/lib

```sh
cp "${HOME}/.local/lib/python$(python --version | awk '{print $2}' | cut -d '.' -f 1,2)/site-packages/ppsi/server/config/ppsi.yml" "${HOME}/.config/sway/ppsi.yml"
```

If ppsi somehow got installed system-wide [*this is highly discouraged*], use the following instead
```sh
cp "/usr/local/lib/python$(python --version | awk '{print $2}' | cut -d '.' -f 1,2)/site-packages/ppsi/server/config/ppsi.yml" "${HOME}/.config/sway/ppsi.yml"
```
modify it to [suitably](#configuration)

server
-------

Arrange to run the server ``ppsid`` every time sway boots by adding following to sway's config

```sh
exec --no-startup-id ppsid
```
  
Test ``ppsi`` it in command-line, bind ppsi commands to suitable keys see section [COMMANDS](#id4) below

===================================================================================

Configuration
==============

ppsi.yml
---------
ppsi.yml should

- be provided in command line OR
- be located in `.config/sway` OR
- be located in `SWAYROOT` which is

  - provided in command line OR
  - is an environment variable

- ppsi format:

  - 3 JSON objects

      1. primary keybinding:
      ```yaml
      primary-kb: $mod+Shift+Return
      ```

      2. workspaces:

      ```yaml
      workspaces:
        ws1:
          bind:
            primary: <command>
        ...
      ```

      2. remote:
      ```yaml
      remote:
        users:
        - root
        - guest
        ...
        hosts:
        - localhost
        - www.remote.com
        ...
      ```
