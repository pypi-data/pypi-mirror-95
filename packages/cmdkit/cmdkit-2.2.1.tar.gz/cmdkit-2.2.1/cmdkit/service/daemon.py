# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Implementation of abstract base class for daemon services."""


# standard libs
import os
import sys
import time
import atexit
import signal
import abc
import logging


log = logging.getLogger(__name__)


class Daemon(abc.ABC):
    """Abstract base class for Daemon processes."""

    _pidfile: str  # path to file for saving process ID

    def __init__(self, pidfile: str) -> None:
        """
        Initialization. You must call `.start()` to begin execution.

        Arguments
        ---------
        pidfile: str
            Path to a process ID file. This file is created with
            the process ID so it can be stopped later.
        """
        self.pidfile = pidfile

    def daemonize(self) -> None:
        """Daemonize class. UNIX double fork mechanism."""

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)  # exit first parent
        except OSError:
            log.critical('failed to create first fork')
            sys.exit(6)

        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)  # exit second parent
        except OSError:
            log.critical('failed to create second fork')
            sys.exit(6)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # automatically remove pidfile at exit
        atexit.register(self.__remove_pidfile)

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as fh:
            fh.write(pid)

    def __remove_pidfile(self) -> None:
        """Remove the process ID file."""
        os.remove(self.pidfile)

    def start(self) -> None:
        """Start the daemon."""
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            log.error(f'daemon already running ({pid}), {self.pidfile} exists')
            sys.exit(1)

        self.daemonize()
        self.run()

    def stop(self) -> None:
        """Stop the daemon."""

        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            return  # not an error in a restart

        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)

        except OSError as error:
            err_msg = str(error.args)
            if 'no such process' in err_msg.lower():
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                log.error(f'could not stop daemon')
                sys.exit(6)

    def restart(self) -> None:
        """Restart the daemon."""
        self.stop()
        self.start()

    @abc.abstractmethod
    def run(self) -> None:
        """Entry point for daemon service."""
        raise NotImplementedError()
