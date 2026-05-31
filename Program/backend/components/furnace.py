import config 
from components .environmental_controls import AirFlowSystem 

class Furnace :
    def __init__ (self ):
        self .q_in_mw =0.0 
        self .air_flow_system =AirFlowSystem ()

    def calculate_heat (self ,coal_feed_tph ,air_flow_pct ):
        mass_flow_kgs =coal_feed_tph *(1000.0 /3600.0 )
        eff_factor =self .air_flow_system .calculate_efficiency_factor (coal_feed_tph ,air_flow_pct )
        self .q_in_mw =mass_flow_kgs *config .LHV_COAL *config .FURNACE_EFF *eff_factor 
        return self .q_in_mw 