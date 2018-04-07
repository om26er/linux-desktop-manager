# Linux Desktop Manager

This is a work in progress tool for Linux based systems allowing users to remotely manage their desktops.

The main idea is to run a background daemon on your desktop which is always connected to a remote server, the controller
lets say your Android phone then connects to that server and makes remote procedure calls on your desktop

Currently it only allows to lock the screen.

For ease of delivery I have chosen snaps as the medium for delivery of this tool, so the guide below uses snaps.

#### How to test

```
$ snap install crossbar
$ snap install http
$ snap install linux-desktop-manager --edge
```

Then just download this file <https://github.com/om26er/linux-desktop-manager/blob/master/config/config.json> to a
directory and in that same directory start crossbar using below command

```
$ crossbar start
```

In another terminal start LDM

```
$ linux-desktop-manager
```

Now to actually lock the screen or to check its state you need to know the machine id of your computer. On fairly newer
version of Linux distros that can be found inside `/etc/machine-id`

So to lock the screen, just call

```
http localhost:8080/call procedure=com.om26er.ldm.machine-<your_machine_id>.lock_screen
```

You can also check the screen lock status

```
http localhost:8080/call procedure=com.om26er.ldm.machine-<your_machine_id>.is_screen_locked
```
