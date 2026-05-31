import config 

class Generator :
    def __init__ (self ):
        self .p_elec_mw =0.0 

    def calculate_electrical_power (self ,p_mech_mw ):
        """
        Rumus: P_elec = P_mech * Efisiensi_Generator
        """
        self .p_elec_mw =p_mech_mw *config .GENERATOR_EFF 
        return self .p_elec_mw 