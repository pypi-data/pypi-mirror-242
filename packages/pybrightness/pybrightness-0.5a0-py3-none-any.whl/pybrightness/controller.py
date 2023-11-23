"""Parent module to control brightness."""

import subprocess
from typing import Union, List

from .module import settings, commands

OS_ERROR = OSError("Package is unsupported in %s" % settings.operating_system)


def _run(cmd: Union[str, List[str]]) -> None:
    """Runs the command using subprocess module.

    Args:
        cmd: Command to run.
    """
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def increase() -> None:
    """Increases the brightness to maximum."""
    if settings.operating_system == "Darwin":
        for _ in range(32):
            _run(commands.MAC_INCREASE)
    elif settings.operating_system == "Windows":
        _run(["powershell", commands.WINDOWS.format(l=100)])
    elif settings.operating_system == "Linux":
        _run(f"echo {settings.root_password} | sudo -S brightnessctl s 100 > /dev/null")
    else:
        raise OS_ERROR


def decrease() -> None:
    """Decreases the brightness to minimum."""
    if settings.operating_system == "Darwin":
        for _ in range(32):
            _run(commands.MAC_DECREASE)
    elif settings.operating_system == "Windows":
        _run(["powershell", commands.WINDOWS.format(l=0)])
    elif settings.operating_system == "Linux":
        _run(f"echo {settings.root_password} | sudo -S brightnessctl s 0 > /dev/null")
    else:
        raise OS_ERROR


def custom(percent: int = 50) -> None:
    """Set brightness to a custom level.

    - | Since package uses in-built apple script (for macOS), the only way to achieve this is to set the
      | brightness to absolute minimum/maximum and increase/decrease the required % from there.

    Args:
        percent: Percentage of brightness to be set.
    """
    assert 0 <= percent <= 100, "value should be between 0 and 100"
    if settings.operating_system == "Darwin":
        decrease()
        for _ in range(round((32 * int(percent)) / 100)):
            _run(commands.MAC_INCREASE)
    elif settings.operating_system == "Windows":
        _run(["powershell", commands.WINDOWS.format(l=percent)])
    elif settings.operating_system == "Linux":
        _run(f"echo {settings.root_password} | sudo -S brightnessctl s {percent} > /dev/null")
    else:
        raise OS_ERROR
