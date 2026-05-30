import config
import math

class Valve:
    def __init__(self):
        self.steam_flow_kgs = 0.0

    def calculate_flow(self, valve_opening_pct, p_boiler, p_turbine=5.0):
        """
        Rumus: m_steam = Cv * (%_buka) * sqrt(P_boiler - P_turbine)
        """
        # Mencegah nilai akar negatif jika tekanan boiler anjlok
        dp = max(0.0, p_boiler - p_turbine)
        
        # Kalkulasi aliran massa (kg/s)
        self.steam_flow_kgs = config.VALVE_CV * (valve_opening_pct / 100.0) * math.sqrt(dp)
        return self.steam_flow_kgs