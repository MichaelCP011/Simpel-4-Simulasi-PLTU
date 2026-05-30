# ==========================================
# KONSTANTA FISIKA & PARAMETER PLTU 300 MW
# ==========================================

# Parameter Batubara & Pembakaran
LHV_COAL = 17.5         # Nilai Kalor Bawah batubara (MJ/kg)
FURNACE_EFF = 0.88      # Efisiensi perpindahan panas
MAX_COAL_FEED = 220.0   # Kapasitas maksimum coal feeder (ton/jam)

# Parameter Boiler
BOILER_MASS = 50000.0   # Massa ekuivalen boiler & air (kg)
CP_BOILER = 0.5         # Kapasitas panas spesifik (MJ/kg°C)
NOMINAL_TEMP = 540.0    # Suhu desain uap utama (°C)
NOMINAL_PRESSURE = 165.0# Tekanan desain uap utama (Bar)
ENTHALPY_STEAM = 2.8    # Disesuaikan agar penyerapan panas seimbang dengan aliran

# Parameter Valve & Turbin
VALVE_CV = 28.0         # NAIK DRASTIS: Memperbesar kapasitas katup agar uap bisa mengalir
TURBINE_EFF = 0.85      # Efisiensi isentropik turbin uap
ENTHALPY_DROP_NOMINAL = 1.3 # Penurunan entalpi standar (MJ/kg)

# Parameter Generator & Condenser
GENERATOR_EFF = 0.98    # Efisiensi generator
CONDENSER_CP_WATER = 0.00418