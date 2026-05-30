from components.furnace import Furnace
from components.boiler import Boiler
from components.valve import Valve
from components.turbine import Turbine
from components.generator import Generator

class PlantOrchestrator:
    def __init__(self):
        self.furnace = Furnace()
        self.boiler = Boiler()
        self.valve = Valve()
        self.turbine = Turbine()
        self.generator = Generator()

        # Status keamanan & operasional sistem
        self.health_point = 100.0
        self.is_tripped = False
        self.is_running = False  # Default saat aplikasi menyala adalah mati (STANDBY)
        self.alarms = []

    def reset_plant(self):
        """Fungsi Emergency Stop / Reset untuk memulihkan sistem yang terminated"""
        self.health_point = 100.0
        self.is_tripped = False
        self.is_running = False
        self.boiler.temperature = 540.0
        self.boiler.pressure = 165.0
        self.alarms.clear()

    def update_step(self, fuel_feed_tph, valve_opening_pct, dt=1.0):
        # Jika sistem trip atau sedang stop, paksa input bahan bakar dan katup menjadi 0
        if self.is_tripped or not self.is_running:
            fuel_feed_tph = 0.0
            valve_opening_pct = 0.0

        q_in = self.furnace.calculate_heat(fuel_feed_tph)
        steam_flow = self.valve.calculate_flow(valve_opening_pct, self.boiler.pressure)
        t_boiler, p_boiler = self.boiler.update(q_in, steam_flow, dt)
        p_mech = self.turbine.calculate_power(steam_flow, t_boiler, p_boiler)
        mw_out = self.generator.calculate_electrical_power(p_mech)

        self._check_safety_limits(t_boiler, p_boiler)

        # Jika stop, output murni 0
        if not self.is_running and not self.is_tripped:
            mw_out = 0.0
            steam_flow = 0.0

        return {
            "mw_out": round(mw_out, 2),
            "steam_press": round(p_boiler, 1),
            "boiler_temp": round(t_boiler, 1),
            "steam_flow": round(steam_flow, 1),
            "health": round(self.health_point, 1),
            "is_tripped": self.is_tripped,
            "is_running": self.is_running,
            "alarms": self.alarms
        }

    def _check_safety_limits(self, temp, press):
        self.alarms.clear()
        if temp > 560.0:
            self.alarms.append("HIGH TEMP ALARM")
            self.health_point -= 0.5
        if press > 185.0:
            self.alarms.append("OVERPRESSURE ALARM")
            self.health_point -= 1.0
        
        if self.health_point <= 0:
            self.health_point = 0.0
            self.is_tripped = True
            self.is_running = False
            self.alarms.append("SYSTEM TRIPPED - CRITICAL FAILURE")