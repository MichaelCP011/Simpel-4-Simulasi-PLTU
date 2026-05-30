import config

class Furnace:
    def __init__(self):
        self.q_in_mw = 0.0

    def calculate_heat(self, coal_feed_tph):
        """
        Rumus: Qin = m_coal * LHV * efisiensi
        """
        # Konversi ton/jam menjadi kg/detik (kg/s)
        mass_flow_kgs = coal_feed_tph * (1000.0 / 3600.0)
        
        # Kalkulasi energi panas yang dihasilkan (MW thermal)
        self.q_in_mw = mass_flow_kgs * config.LHV_COAL * config.FURNACE_EFF
        return self.q_in_mw