from threading import Event
from flask import Flask
from flask_socketio import SocketIO
from system_logic import PlantOrchestrator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pltu_secret_key!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

control_state = {
    "fuel_feed": 190.0, "steam_valve": 76.0,
    "water_inlet": 80.0, "air_flow": 65.0, # BARU
    "is_auto": False, "target_mw": 300.0
}

TIME_SCALE_FACTOR = 10.0
plant = PlantOrchestrator()
background_thread = None
thread_stop_event = Event()

def simulation_loop():
    print(f"[SYSTEM] Simulasi Termodinamika PLTU Dimulai (Speed: {TIME_SCALE_FACTOR}x)...")
    while not thread_stop_event.is_set():
        if control_state["is_auto"]:
            error = control_state["target_mw"] - plant.generator.p_elec_mw
            control_state["steam_valve"] += error * 0.05
            control_state["fuel_feed"] += error * 0.1
            
            # AI Menyeimbangkan Water Level (Target 72%)
            level_error = 72.0 - plant.boiler.water_level.water_level_pct
            control_state["water_inlet"] += level_error * 0.08
            
            # AI Menyeimbangkan Udara dengan Batubara (AFR Optimal)
            control_state["air_flow"] += (control_state["fuel_feed"] - control_state["air_flow"]) * 0.12
            
            for key in ["steam_valve", "water_inlet", "air_flow"]:
                control_state[key] = max(0.0, min(100.0, control_state[key]))
            control_state["fuel_feed"] = max(0.0, min(220.0, control_state["fuel_feed"]))

        sim_data = plant.update_step(
            fuel_feed_tph=control_state["fuel_feed"],
            valve_opening_pct=control_state["steam_valve"],
            water_inlet_pct=control_state["water_inlet"],
            air_flow_pct=control_state["air_flow"],
            dt=TIME_SCALE_FACTOR
        )

        sim_data["current_fuel"] = round(control_state["fuel_feed"], 1)
        sim_data["current_valve"] = round(control_state["steam_valve"], 1)
        sim_data["current_water_inlet"] = round(control_state["water_inlet"], 1)
        sim_data["current_air_flow"] = round(control_state["air_flow"], 1)

        socketio.emit('sim_update', sim_data)
        socketio.sleep(1.0)

@socketio.on('connect')
def handle_connect(auth=None):
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
    if command == "START" and not plant.is_tripped: plant.is_running = True
    elif command == "STOP": plant.is_running = False
    elif command == "ESTOP": plant.reset_plant()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)