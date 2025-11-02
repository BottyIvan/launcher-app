"""Mathematical expression evaluation service.

This module provides safe evaluation of mathematical expressions
using a restricted set of functions from the math module.
"""

import math
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class MathService:
    """Service to safely evaluate mathematical expressions.

    Attributes:
        safe_dict: Dictionary of allowed functions and constants for evaluation
    """

    def __init__(self) -> None:
        """Initialize the MathService with safe math functions."""
        # Create a dictionary with allowed math functions
        self.safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
        # Also add constants and basic functions
        self.safe_dict.update({"abs": abs, "round": round, "min": min, "max": max})

    def calculate(self, expression: str) -> Tuple[Optional[str], Optional[str]]:
        """Safely evaluate a mathematical expression.

        Args:
            expression: The math expression to evaluate, e.g. "2+2*3"

        Returns:
            Tuple of (result_string, error_message). If successful, returns
            (result, None). If evaluation fails, returns (None, error_message).
        """
        try:
            # Evaluate the expression using only the allowed functions in self.safe_dict
            result = eval(expression, {"__builtins__": {}}, self.safe_dict)
            return (str(result), None)
        except Exception as e:
            # Log the error for debugging and return a user-friendly error message
            logger.error(f"Math evaluation error for expression='{expression}': {e}")
            return (None, f"Error: Could not evaluate '{expression}'. Please check your input.")
