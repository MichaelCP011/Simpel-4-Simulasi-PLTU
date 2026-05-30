import config

class AirFlowSystem:
    def __init__(self):
        self.air_flow_pct = 65.0
        self.optimal_afr = 4.5
        self.efficiency_factor = 1.0
        
    def calculate_efficiency_factor(self, fuel_feed_tph, air_flow_pct):
        fuel_rate_kgs = fuel_feed_tph * (1000.0 / 3600.0)
        max_air_supply_kgs = 0.5 
        air_rate_kgs = (air_flow_pct / 100.0) * fuel_rate_kgs * max_air_supply_kgs
        
        if fuel_rate_kgs > 0:
            actual_afr = air_rate_kgs / fuel_rate_kgs
        else:
            actual_afr = 0
            
        if fuel_rate_kgs > 0.01:
            afr_ratio = actual_afr / self.optimal_afr
            efficiency_factor = 1.0 - 0.5 * ((afr_ratio - 1.0) ** 2)
            self.efficiency_factor = max(0.1, min(1.0, efficiency_factor))
        else:
            self.efficiency_factor = 0.0
            
        self.air_flow_pct = air_flow_pct
        return self.efficiency_factor

class BoilerWaterLevel:
    def __init__(self):
        self.water_level_pct = 80.0
        self.water_inlet_pct = 80.0
        
    def update(self, steam_flow_kgs, water_inlet_pct, dt=1.0):
        max_feedwater_rate_kgs = config.MAX_FEEDWATER_RATE_KGS
        feedwater_rate_kgs = (water_inlet_pct / 100.0) * max_feedwater_rate_kgs
        
        k_level = 300.0 # 1% level = 300 kg
        delta_level = ((feedwater_rate_kgs - steam_flow_kgs) / k_level) * dt
        
        self.water_level_pct += delta_level
        self.water_level_pct = max(0.0, min(100.0, self.water_level_pct))
        self.water_inlet_pct = water_inlet_pct
        return self.water_level_pct
    
    def get_temperature_impact(self):
        h_feedwater = config.ENTHALPY_FEED_WATER
        h_steam = config.ENTHALPY_STEAM_OUT
        heat_removal_per_kg = h_steam - h_feedwater
        
        actual_feedwater_kgs = (self.water_inlet_pct / 100.0) * config.MAX_FEEDWATER_RATE_KGS
        total_heat_removal_mw = actual_feedwater_kgs * heat_removal_per_kg
        
        dt_impact = -(total_heat_removal_mw * 1000) / (config.BOILER_MASS * config.CP_BOILER)
        return dt_impact