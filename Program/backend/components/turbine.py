import config

class Turbine:
    def __init__(self):
        self.p_mech_mw = 0.0

    def calculate_power(self, steam_flow_kgs, t_boiler, p_boiler):
        """
        Rumus: P_mech = m_steam * Delta_H * Efisiensi
        """
        # Penurunan entalpi dikoreksi berdasarkan deviasi suhu dan tekanan dari titik nominal
        temp_ratio = t_boiler / config.NOMINAL_TEMP
        press_ratio = p_boiler / config.NOMINAL_PRESSURE
        
        delta_h_actual = config.ENTHALPY_DROP_NOMINAL * temp_ratio * press_ratio
        
        # Daya mekanik yang dihasilkan (MW mekanik)
        self.p_mech_mw = steam_flow_kgs * delta_h_actual * config.TURBINE_EFF
        
        # Mencegah daya minus
        if self.p_mech_mw < 0:
            self.p_mech_mw = 0.0
            
        return self.p_mech_mw