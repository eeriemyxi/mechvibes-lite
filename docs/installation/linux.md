## Installation
!!! important
    Minimum Python version required is `3.10`. Please check by running `python3
    --version`.

Run the following command in a terminal:

```shell
user:~$ python3 -m pip install --local git+https://github.com/eeriemyxi/mechvibes-lite
```

Now you should be able to do `mvibes --version` from your terminal. If not then
I am afraid you have a messy Python setup on your system. However if everything
is fine then please follow the instructions from the next header.

## Getting Access to Input Events
This program uses [scan codes](https://en.wikipedia.org/wiki/Scancode) to detect
keyboard input. Scan codes are not readable to normal users out-of-the-box on
Linux. Below are various methods to get access to scan codes on Linux.

### Method I
This is the easier and less secure method of making scan codes readable for
processes running from your user account. First you need to add your user to the
`input` group:

```shell
user:~$ sudo usermod -aG input username
```
Replace `username` with your account's username.

Then log out and log back in. Now you should have read access to events in
`/dev/input/` directory. To test do [these
instructions](#testing-access-for-input-event).

### Method II
!!! warning 
    This method is more involved and requires you to understand what you
    are doing; please do not attempt it if all you do right now is copy-paste
    random commands into your terminal.

When you do `mvibes daemon` it automatically starts a `wskey` daemon unless told
otherwise. `wskey` daemon is essentially just a websocket server that sends the
input events to connected clients.

You can start a `wskey` daemon by doing `mvibes wskey daemon`.

The idea is to create another user, give it access to input events, then run the
`wskey` daemon from this account. This way your normal account is untouched and
is protected from the pitfalls of any program having access to the input events.
Once the `wskey` daemon is running on the second account, you can simply tell
`mvibes daemon` running on your usual account to use that websocket server to
receive input events from.

!!! note
    The instructions below are for Ubuntu. Please adapt them for your system yourself.

Create a new user:
```
usual-user:~$ sudo adduser second-user
```

`second-user` is the username of the second account. Please follow the
instructions given to you by this command.

Add the new user to `input` group:

```shell
usual-user:~$ sudo usermod -aG input second-user
```

Log out and log back in. Now make sure your new account can read input events by
reading [this](#testing-access-for-input-event). However instead of running
`evtest` do:

```shell
usual-user:~$ sudo -u second-user evtest
```

Create a system-wide configuration directory for Mechvibes Lite:
```shell
usual-user:~$ sudo cp -r ~/.config/mechvibes-lite/ /etc/mechvibes-lite
```

The command above will copy your local configuration file directory to `/etc`
folder. It is recommended that you put your `themes` folder within this directory
to not have issues with file permissions.

Install Mechvibes Lite on the new user account:

```shell
usual-user:~$ sudo apt install python3-venv
usual-user:~$ sudo -iu second-user
second-user:~$ python3 -m venv mvibes-venv
second-user:~$ source mvibes-venv/bin/activate
second-user:~$ pip install git+https://github.com/eeriemyxi/mechvibes-lite
second-user:~$ deactivate && exit
```

Now do this from the usual account to start the `wskey` server:

```shell
usual-user:~$ sudo -iu second-user mvibes-venv/bin/mvibes wskey daemon
```

### Method III
It would be possible to create a Linux container (using Docker, Podman, whatever
else) just for Mechvibes Lite then mount `/dev/input/` as read-only and then
just start the `wskey` server (make sure to forward the ports to the parent
system) or the whole app from the container (in that case you'd make sure to
have your display server accessible from within the container). However I have
no desire to make instructions for this. Contributions welcome.

## Testing Access for Input Event
Install `evtest` package:

```
user:~$ sudo apt install evtest
```

Run `evtest` then select a device from the list:
```
user:~$ evtest
No device specified, trying to scan all of /dev/input/event*
Not running as root, no devices may be available.
Available devices:
/dev/input/event0:      Power Button
/dev/input/event1:      Lid Switch
/dev/input/event2:      Power Button
/dev/input/event3:      AT Translated Set 2 keyboard
/dev/input/event4:      Video Bus
/dev/input/event5:      ETPS/2 Elantech Touchpad
...
```

Pick a relevant event and then press keys on your keyboard. You will see outputs
like this whenever you do:

```
Event: time 1734882562.361739, type 1 (EV_KEY), code 28 (KEY_ENTER), value 0
Event: time 1734882562.361739, -------------- SYN_REPORT ------------
Event: time 1734882563.472796, type 1 (EV_KEY), code 49 (KEY_N), value 1
Event: time 1734882563.472796, -------------- SYN_REPORT ------------
Event: time 1734882563.557881, type 1 (EV_KEY), code 49 (KEY_N), value 0
Event: time 1734882563.557881, -------------- SYN_REPORT ------------
Event: time 1734882563.726942, type 1 (EV_KEY), code 18 (KEY_E), value 1
Event: time 1734882563.726942, -------------- SYN_REPORT ------------
```

# What To Do Next?
Now that you access to input events, you will have to add `wskey.event_id`
option in your configuration file. More in-depth explanation is
[here](../configuration.md).
