#!/bin/sh

set +x

MACHINE_ID=$(python3 -c "import sys; from linux_desktop_manager.wamp.display_component import get_machine_id; sys.stdout.write(get_machine_id())")
qr $MACHINE_ID
