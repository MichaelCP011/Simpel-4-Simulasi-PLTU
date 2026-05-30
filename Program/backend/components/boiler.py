import config

class Boiler:
    def __init__(self):
        # Mulai simulasi dalam keadaan operasional penuh
        self.temperature = config.NOMINAL_TEMP
        self.pressure = config.NOMINAL_PRESSURE

    def update(self, q_in_mw, steam_flow_out_kgs, dt=1.0):
        """
        Rumus ODE Kapasitas Panas: dT = (Qin - Qout) / (M * Cp) * dt
        Rumus Tekanan Gas: P = P_awal * (T/T_nominal)^k
        """
        # Energi yang keluar dibawa oleh aliran uap ke turbin
        q_out_mw = steam_flow_out_kgs * config.ENTHALPY_STEAM
        
        # Perubahan suhu per detik (delta T)
        dt_temp = ((q_in_mw - q_out_mw) / (config.BOILER_MASS * config.CP_BOILER)) * dt
        self.temperature += dt_temp

        # Batas minimum agar suhu tidak turun di bawah suhu ruang
        if self.temperature < 30.0:
            self.temperature = 30.0

        # Tekanan bereaksi terhadap suhu (pendekatan persamaan kurva saturasi/gas ideal)
        if self.temperature > 100.0:
            self.pressure = config.NOMINAL_PRESSURE * ((self.temperature / config.NOMINAL_TEMP) ** 4)
        else:
            self.pressure = 1.0  # Tekanan atmosfer

        return self.temperature, self.pressure