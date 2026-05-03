class Regulator:
    """Hardened PID-based regulation for geospheric homeostasis."""
    def __init__(self, setpoint: float):
        self.setpoint = setpoint
        self.current = setpoint

    def update(self, observed: float) -> float:
        error = self.setpoint - observed
        # Proportional correction
        return error * 1.5
