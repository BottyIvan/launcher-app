import math

class MathService:
    """Service to safely evaluate math expressions."""

    def __init__(self):
        # Create a dictionary with allowed math functions
        self.safe_dict = {
            k: getattr(math, k) for k in dir(math) if not k.startswith("__")
        }
        # Also add constants and basic functions
        self.safe_dict.update({
            "abs": abs,
            "round": round,
            "min": min,
            "max": max
        })

    def calculate(self, expression: str):
        """
        Safely evaluate a math expression using a restricted set of functions.

        Args:
            expression (str): The math expression to evaluate, e.g. "2+2*3".

        Returns:
            list: [result as string, None] if successful, or [None, error message] if evaluation fails.
        """
        try:
            # Evaluate the expression using only the allowed functions in self.safe_dict
            result = eval(expression, {"__builtins__": {}}, self.safe_dict)
            return [str(result), None]
        except Exception as e:
            # Print the error for debugging and return a user-friendly error message
            print(f"Math evaluation error: {e}")
            return [None, f"Error: Could not evaluate '{expression}'. Please check your input."]
