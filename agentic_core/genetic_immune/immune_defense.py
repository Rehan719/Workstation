from typing import List, Dict, Any

class ImmuneDefense:
    """
    Enhanced with digital twin’s threat predictions.
    """
    def __init__(self, anomaly_detector, digital_twin, ueg):
        self.anomaly_detector = anomaly_detector
        self.digital_twin = digital_twin
        self.ueg = ueg

    async def scan_threats(self, orchestrator=None) -> float:
        # 1. Analyse live API traffic
        live_anomalies = await self.anomaly_detector.scan() if hasattr(self.anomaly_detector, "scan") else 0.1
        # 2. Simulate attack scenarios in the twin
        twin_predictions = await self.digital_twin.predict_threats() if hasattr(self.digital_twin, "predict_threats") else []

        max_twin_risk = max([t["risk_score"] for t in twin_predictions]) if twin_predictions else 0.0
        combined_risk = 0.5 * live_anomalies + 0.5 * max_twin_risk

        threats = []
        if combined_risk > 0.8:
            await self.activate_countermeasures(combined_risk)
            threats.append({"source": "anomaly_detector", "data": {"risk_score": combined_risk}})
        return threats

    async def activate_countermeasures(self, risk_level: float):
        if self.ueg:
            await self.ueg.log("IMMUNE_RESPONSE_ACTIVATED", risk=risk_level)

    async def respond(self, threats: List[Dict[str, Any]]):
        for threat in threats:
            if threat.get("risk_score", 0) > 0.5:
                await self.activate_countermeasures(threat["risk_score"])
