"""Compatibility wrapper for the original STFA script name.

The original bobyellow/SpaceTimeFlowLISA repository used this file name under
Code/. Import core.SpaceTimeFlowLISA or core.FlowLISA from new code.
"""

from core.SpaceTimeFlowLISA import execSpaceTimeFLOWLISA

__all__ = ["execSpaceTimeFLOWLISA"]
