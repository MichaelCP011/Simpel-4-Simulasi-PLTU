from threading import Event
from flask import Flask
from flask_socketio import SocketIO
from system_logic import PlantOrchestrator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pltu_secret_key!'
# Mengizinkan koneksi dari React
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global state untuk menyimpan input kontrol terakhir dari Frontend
control_state = {
    "fuel_feed": 190.0,
    "steam_valve": 76.0,
    "is_auto": False,
    "target_mw": 300.0
}

# --- PARAMETER PERCEPATAN WAKTU ---
# 1 detik di dunia nyata = 10 detik di dalam simulasi fisika
TIME_SCALE_FACTOR = 10.0 

# Inisiasi Orkestrator Fisika
plant = PlantOrchestrator()
background_thread = None
thread_stop_event = Event()

def simulation_loop():
    """
    Background Thread: Jantung simulasi.
    """
    print(f"[SYSTEM] Simulasi Termodinamika PLTU Dimulai (Speed: {TIME_SCALE_FACTOR}x)...")
    while not thread_stop_event.is_set():
        
        # ---------------------------------------------------------
        # AI / AUTO MODE (Proportional Controller Sederhana)
        # ---------------------------------------------------------
        if control_state["is_auto"]:
            current_mw = plant.generator.p_elec_mw
            error = control_state["target_mw"] - current_mw
            
            # Gain PID disesuaikan agar tidak terlalu agresif saat waktu dipercepat
            control_state["steam_valve"] += error * 0.05
            control_state["fuel_feed"] += error * 0.1
            
            # Limitasi fisik bukaan
            control_state["steam_valve"] = max(0.0, min(100.0, control_state["steam_valve"]))
            control_state["fuel_feed"] = max(0.0, min(220.0, control_state["fuel_feed"]))

        # ---------------------------------------------------------
        # EKSEKUSI FISIKA TERMODINAMIKA (TIME SCALED)
        # ---------------------------------------------------------
        sim_data = plant.update_step(
            fuel_feed_tph=control_state["fuel_feed"],
            valve_opening_pct=control_state["steam_valve"],
            dt=TIME_SCALE_FACTOR  # <-- Fisika dikalkulasi 10 detik lebih cepat!
        )

        sim_data["current_fuel"] = round(control_state["fuel_feed"], 1)
        sim_data["current_valve"] = round(control_state["steam_valve"], 1)

        # ---------------------------------------------------------
        # BROADCAST KE FRONTEND
        # ---------------------------------------------------------
        socketio.emit('sim_update', sim_data)
        
        # Waktu server tetap tidur 1 detik agar UI update dengan mulus
        socketio.sleep(1.0)

@socketio.on('connect')
def handle_connect(auth=None):
    print("[NETWORK] Frontend React Terhubung ke WebSocket!")
    global background_thread
    if background_thread is None:
        background_thread = socketio.start_background_task(simulation_loop)

@socketio.on('control_update')
def handle_control_update(data):
    for key in data:
        if key in control_state:
            control_state[key] = data[key]

@socketio.on('system_command')
def handle_system_command(command):
    """Menerima perintah START, STOP, dan ESTOP dari Frontend"""
    if command == "START" and not plant.is_tripped:
        plant.is_running = True
        print("[SYSTEM] Command diterima: START")
    elif command == "STOP":
        plant.is_running = False
        print("[SYSTEM] Command diterima: STOP")
    elif command == "ESTOP":
        plant.reset_plant()
        print("[SYSTEM] Command diterima: EMERGENCY STOP / RESET")

if __name__ == '__main__':
    print("[NETWORK] Memulai Server PLTU di port 5000...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)