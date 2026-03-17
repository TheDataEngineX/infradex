"""InfraDEX — Infrastructure-as-Code for TheDataEngineX platform."""

from __future__ import annotations

try:
    from importlib.metadata import version

    __version__ = version("infradex")
except Exception:
    __version__ = "0.1.0"
