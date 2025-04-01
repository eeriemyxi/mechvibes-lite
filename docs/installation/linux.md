## Installation
!!! info
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

You may check whether you have access to the input events via the instructions
[here](#testing-access-for-input-event).

Once you confirm you have access to the input events, read
[here](#what-to-do-next).

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
The second method is to use a Docker container to run the Wskey daemon then
forward the port to the host machine. We will mount the `/dev/input` directory
as read-only in a privileged container for this method.

The project comes with a `compose.yml` and `Dockerfile` to remedy this method.

As a prerequisite, you will need to install Docker on your system. You can do so
by going to <https://www.docker.com/> and downloading the installer for your
platform. It is possible to follow this guide on all platforms supported by
Docker but we will be assuming that you use Linux.

!!! note 
    If you are an experienced Linux user, you may also try installing it
    from your package manager instead. 
    
Once installed, clone the source code of Mechvibes Lite using Git then CD to it:

```console
user:~$ git clone https://github.com/eeriemyxi/mechvibes-lite
user:~$ cd mechvibes-lite
```

!!! note 
    The commnad below assumes that you store your configuration at the
    standard configuration location, if not then you will have to modify the
    `volumes` section in the `compose.yml` section and the `Dockerfile` file
    too.

Then we run the Docker service like so:
```console
user:~$ docker compose -p wskey-server up -d
```

By default the server runs on the port `4958`. You can change it by exporting
`WSKEY_PORT` environment variable. Docker seem to support `.env` files too, but
I haven't tested.

!!! tip
    You can omit the `-d` (stands for `--detach`) when starting the service to avoid detaching it.

!!! tip
    To see if everything is working well for the Wskey server, you can then run:
    ```console
    user:~$ docker compose -p wskey-server logs -f
    ```
    This command should from anywhere due to `-p wskey-server logs`.

To connect to the Docker container, you can do something like this:
```console
user:~$ mvibes -LDEBUG --no-wskey --wskey-port 4958 daemon
```

That's all. Mechvibes Lite should now be able listen to your event id's key presses
(on the usual Linux installation).

### Method III
!!! warning 
    This method is more involved, do not attempt it unless you
    understand every step mentioned.

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

Create a new user:
```shell
usual-user:~$ sudo useradd -d /home/second-user -m second-user
```
`second-user` is the username of the second account. `/home/second-user` is the
path to the new user's home directory.

!!! info 
    On Debian-based systems (Ubuntu, Linux Mint, etc.), there is `adduser`
    command which is more interactive and beginner friendly:

    ```
    usual-user:~$ sudo adduser second-user
    ```
    
    Now answer the prompts on your screen.

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
