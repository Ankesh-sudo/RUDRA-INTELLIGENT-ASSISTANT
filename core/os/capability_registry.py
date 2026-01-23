from typing import Iterable, Set

from core.os.control_capabilities import OSControlCapability


class CapabilityRegistry:
    """
    DAY 62 — OS CAPABILITY REGISTRY

    This registry is the single authoritative source of truth
    for what OS-level capabilities Rudra is allowed to reason about.

    IMPORTANT GUARANTEES:
    - Declarative only
    - No OS execution
    - No permission enforcement
    - No side effects
    - Safe to query from any layer
    """

    def __init__(self, allowed: Iterable[OSControlCapability] | None = None):
        """
        Initialize the capability registry.

        If `allowed` is None, all declared capabilities are allowed
        at the reasoning level (NOT execution level).
        """
        if allowed is None:
            self._allowed: Set[OSControlCapability] = set(OSControlCapability)
        else:
            self._allowed = set(allowed)

    # -------------------------------------------------
    # Core Queries
    # -------------------------------------------------

    def is_known(self, capability: OSControlCapability) -> bool:
        """
        Returns True if the capability exists in the enum.
        """
        return capability in OSControlCapability

    def is_allowed(self, capability: OSControlCapability) -> bool:
        """
        Returns True if the capability is allowed at the registry level.

        NOTE:
        - This does NOT mean execution is allowed
        - This does NOT mean permission is granted
        """
        return capability in self._allowed

    # -------------------------------------------------
    # Introspection (Read-Only)
    # -------------------------------------------------

    def list_allowed(self) -> Set[OSControlCapability]:
        """
        Returns a copy of allowed capabilities.
        """
        return set(self._allowed)

    def list_all(self) -> Set[OSControlCapability]:
        """
        Returns all known capabilities.
        """
        return set(OSControlCapability)

    # -------------------------------------------------
    # Safety Guards
    # -------------------------------------------------

    def assert_allowed(self, capability: OSControlCapability) -> None:
        """
        Raises an exception if the capability is not allowed.

        This is intended to be used by higher layers
        (e.g., planners or executors) as a hard guard.
        """
        if not self.is_allowed(capability):
            raise CapabilityNotAllowedError(
                f"OS capability not allowed: {capability.value}"
            )


# -------------------------------------------------
# Exceptions
# -------------------------------------------------

class CapabilityNotAllowedError(RuntimeError):
    """
    Raised when an OS capability is referenced but not allowed
    by the capability registry.
    """
    pass


# -------------------------------------------------
# Default Registry Instance (SAFE)
# -------------------------------------------------

DEFAULT_CAPABILITY_REGISTRY = CapabilityRegistry()
