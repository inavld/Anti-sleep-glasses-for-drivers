import argparse
import random
import serial
import cv2
import numpy as np
import time
from metadrive import MetaDriveEnv
from metadrive.component.sensors.rgb_camera import RGBCamera
from metadrive.constants import HELP_MESSAGE
from metadrive.examples import expert

SERIAL_PORT = "COM5" # MODIFY BASED ON YOUR PORT
BAUD_RATE = 9600

# === HELPER: Read Serial from Arduino ===
def read_eye_state(ser):
    state = None
    while ser.in_waiting > 0:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if "CLOSED" in line.upper():
                print("CLOSED")
                state = "closed"
            elif "OPEN" in line.upper():
                print("OPEN")
                state = "open"
            else:
                print(f"Unrecognized data: '{line}'")
        except UnicodeDecodeError:
            print("Serial decode error")
        except serial.SerialException:
            print("Serial port error")
    return state

if __name__ == "__main__":
    config = dict(
        use_render=True,
        manual_control=False,  
        traffic_density=0.1,
        num_scenarios=10000,
        random_agent_model=False,
        random_lane_width=True,
        random_lane_num=True,
        on_continuous_line_done=False,
        out_of_route_done=True,
        vehicle_config=dict(show_lidar=True, show_navi_mark=False, show_line_to_navi_mark=False),
        map=4,  
        start_seed=10,
    )
    # === Open Serial Connection ===
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print(f"Connected to Arduino on {SERIAL_PORT}")
    except Exception as e:
        print(f"ERROR! Could not open serial port: {e}")
        exit(1)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--observation", type=str, default="lidar", choices=["lidar", "rgb_camera"])
    args = parser.parse_args()
    if args.observation == "rgb_camera":
        config.update(
            dict(
                image_observation=True,
                sensors=dict(rgb_camera=(RGBCamera, 400, 300)),
                interface_panel=["rgb_camera", "dashboard"]
            )
        )
    env = MetaDriveEnv(config)
    try:
        o, _ = env.reset(seed=21)
        print(HELP_MESSAGE)
       
        env.agent.expert_takeover = True
        eyes_closed = False
        swerve_duration = 0
        SWERVE_MIN_STEPS = 20

        if args.observation == "rgb_camera":
            assert isinstance(o, dict)
            print("The observation is a dict with numpy arrays as values: ", {k: v.shape for k, v in o.items()})
        else:
            assert isinstance(o, np.ndarray)
            print("The observation is an numpy array with shape: ", o.shape)

        for i in range(1, 1000000000):
            state = read_eye_state(ser)
            if state == 'closed':
                if not eyes_closed:  # Transition: eyes open -> closed
                    eyes_closed = True
                    
                    env.agent.expert_takeover = False
                    swerve_duration = SWERVE_MIN_STEPS
                    print('Swerving...')
            elif state == 'open':
                if eyes_closed:  # Transition: eyes closed -> open
                    eyes_closed = False
                    env.agent.expert_takeover = True
                    swerve_duration = 0
                   
                    print('Self driving resumed')

            if swerve_duration > 0:
               
                # Controlled swerving to mimic manual deviation
                steer = random.choice([-1.0, 1.0])
                throttle = 1.0
                swerve_duration-= 1
                action = [steer, throttle]
                
            else:
                # Eyes open or swerving done: use expert mode 
                action = expert(vehicle=env.agent, deterministic=True)
                env.agent.expert_takeover = True
             


            o, r, tm, tc, info = env.step(action)
            # Debug to verify expert mode and car state
            print(f"Step {i}: Expert takeover: {env.current_track_agent.expert_takeover}, Action: {action}, Reward: {r}, Out of route: {info.get('out_of_route', False)}, Navigation: {info.get('navigation_command', 'N/A')}")

            env.render(
                text={
                    "Auto-Drive": "on" if env.current_track_agent.expert_takeover else "off",
                    "Current Observation": args.observation,
                    "Eye status": 'Closed' if eyes_closed else 'Open',
                }
            )
            print("Navigation information: ", info.get("navigation_command", "N/A"))

            if args.observation == "rgb_camera":
                cv2.imshow('RGB Image in Observation', o["image"][..., -1])
                cv2.waitKey(1)

            if (tm or tc) and info["arrive_dest"]:
                o, _ = env.reset(env.current_seed + 1)
                env.current_track_agent.expert_takeover = True
                eyes_closed = False
                swerve_steps_left = 0
    finally:
        ser.close()
        env.close()