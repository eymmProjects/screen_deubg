
import tkinter as tk
from tkinter import ttk
from math import sin, cos, pi

from modbus_sender import ModbusSerialSender
from parameter_entry import ParameterConverter
from pymodbus.client import ModbusSerialClient as ModbusClient



class ButtonSliderGUI:
    def __init__(self, root, modbus_sender):
        self.teach_mode_enabled = False
        self.root = root
        self.modbus_sender = modbus_sender

        self.auto_rotate_flag = False
        self.rotate_direction = "forward"

        root.title("Serial Port Configuration and Control")

        # Frames for layout
        config_frame = ttk.Frame(root)
        config_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        slider_frame = ttk.Frame(root)
        slider_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        control_frame = ttk.Frame(root)
        control_frame.grid(row=0, column=3, padx=20, pady=20, sticky="nsew")

        # Serial Port Configuration Widgets
        ttk.Label(config_frame, text="Port:").grid(row=0, column=0, pady=(10, 0), sticky="w")
        self.port_entry = ttk.Entry(config_frame)
        self.port_entry.insert(0, 'COM7')
        self.port_entry.grid(row=1, column=0, pady=(0, 10))

        ttk.Label(config_frame, text="Baud Rate:").grid(row=2, column=0, pady=(10, 0), sticky="w")
        self.baudrate_entry = ttk.Entry(config_frame)
        self.baudrate_entry.insert(0, '115200')
        self.baudrate_entry.grid(row=3, column=0, pady=(0, 10))

        ttk.Label(config_frame, text="Timeout:").grid(row=4, column=0, pady=(10, 0), sticky="w")
        self.timeout_entry = ttk.Entry(config_frame)
        self.timeout_entry.insert(0, '1')
        self.timeout_entry.grid(row=5, column=0, pady=(0, 10))

        self.open_button = ttk.Button(config_frame, text="Open Port", command=self.open_port)
        self.open_button.grid(row=6, column=0, pady=20)

        self.close_button = ttk.Button(config_frame, text="Close Port", command=self.close_port)
        self.close_button.grid(row=8, column=0, pady=5)

        # Status label
        self.status_label = ttk.Label(config_frame, text="")
        self.status_label.grid(row=7, column=0, pady=(0, 10))

        # Slider with Label
        ttk.Label(slider_frame, text="Control Value:").grid(row=0, column=0, pady=(10, 0), sticky="w")
        self.slider = ttk.Scale(slider_frame, from_=0, to=100, orient="horizontal", command=self.on_slider_change)
        self.slider.grid(row=1, column=0, pady=(0, 10))
        self.slider_value_label = ttk.Label(slider_frame, text="Value: 0")
        self.slider_value_label.grid(row=2, column=0, pady=(0, 10))

        # Control Buttons and Inputs
        ttk.Label(control_frame, text="Forward/Reverse Control").grid(row=0, column=0, pady=(10, 0), sticky="w")

        ttk.Label(control_frame, text="Parameter:").grid(row=1, column=0, pady=(10, 0), sticky="w")
        self.parameter_entry = ttk.Entry(control_frame)
        self.parameter_entry.grid(row=2, column=0, pady=(0, 10))

        self.forward_button = ttk.Button(control_frame, text="Forward", command=self.forward_action)
        self.forward_button.grid(row=3, column=0, pady=(10, 5))

        self.reverse_button = ttk.Button(control_frame, text="Reverse", command=self.reverse_action)
        self.reverse_button.grid(row=4, column=0, pady=(5, 20))

        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_action)
        self.stop_button.grid(row=5, column=0, pady=(5, 20))

        self.stop_button = ttk.Button(control_frame, text="Auto Rotate", command=self.auto_rotate)
        self.stop_button.grid(row=6, column=0, pady=(5, 20))


        # Frame for servo sliders and finger animation
        self.servo_and_animation_frame = ttk.Frame(root)
        self.servo_and_animation_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        # Canvas for finger animations
        self.canvas = tk.Canvas(self.servo_and_animation_frame, width=500, height=200)
        self.canvas.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Drawing initial fingers (rectangles for simplicity)
        self.fingers = []
        for i in range(5):
            finger = self.canvas.create_rectangle(50 + i*90, 150, 100 + i*90, 100, fill="blue")
            self.fingers.append(finger)

        # Create sliders for each servo motor
        self.servo_sliders = []
        self.servo_slider_labels = []
        for i in range(5):
            slider_frame = ttk.Frame(self.servo_and_animation_frame)
            slider_frame.grid(row=i+1, column=0, padx=20, pady=10, sticky="ew")

            ttk.Label(slider_frame, text=f"Servo {i+1}:").pack(side=tk.LEFT)
            slider = ttk.Scale(slider_frame, from_=0, to=100, orient="horizontal", command=lambda value, i=i: self.on_servo_slider_change(value, i))
            slider.pack(side=tk.LEFT, fill="x", expand=True)
            self.servo_sliders.append(slider)

            slider_value_label = ttk.Label(slider_frame, text="Value: 0")
            slider_value_label.pack(side=tk.LEFT)
            self.servo_slider_labels.append(slider_value_label)

        # Frame for the 360-degree control and its visualization
        self.degree_control_frame = ttk.Frame(root)
        self.degree_control_frame.grid(row=0, column=5, padx=20, pady=20, sticky="nsew")

        # Canvas for the 360-degree visualization
        self.degree_canvas = tk.Canvas(self.degree_control_frame, width=200, height=200)
        self.degree_canvas.pack()

        # Draw initial representation
        self.draw_initial_representation()

        # Slider for 360 degrees control
        self.degree_slider = ttk.Scale(self.degree_control_frame, from_=0, to=360, orient="horizontal", command=self.on_degree_slider_change)
        self.degree_slider.pack(fill="x", expand=True)
        ttk.Label(self.degree_control_frame, text="Angle (Degrees):").pack(before=self.degree_slider)


        # ---------------------------------------------------------------- Auto Debug Start
        # Slider Buttons and Inputs
        root.title("Teach Mode")



        # Auto debug frame
        teach_mode_frame = ttk.LabelFrame(root, text="Teach Mode", padding="5")
        teach_mode_frame.grid(row=1, column=5, sticky="ew")

        self.feedback_button = ttk.Button(teach_mode_frame, text="Toggle SON", command=self.toggle_son_action)
        self.feedback_button.grid(row=3, column=0)

        self.feedback_button = ttk.Button(teach_mode_frame, text="Toggle Teach Mode", command=self.toggle_teach_mode)
        self.feedback_button.grid(row=3, column=1)  # Adjust the row and column as needed


        self.feedback_button = ttk.Button(teach_mode_frame, text="Abs/Relative")
        self.feedback_button.grid(row=3, column=2)


        # Start Entry
        ttk.Label(teach_mode_frame, text="Pos/Low bit").grid(row=0, column=0, sticky="w")
        self.pos_low_entry = ttk.Entry(teach_mode_frame, width=6)
        self.pos_low_entry.grid(row=0, column=1, padx=(0, 20))
        self.pos_low_entry.insert(0, "0")

                # Delay (Sweep) Entry
        ttk.Label(teach_mode_frame, text="Target Speed").grid(row=0, column=2, sticky="w")
        self.target_speed = ttk.Entry(teach_mode_frame, width=6)
        self.target_speed.grid(row=0, column=3, padx=(0, 20))
        self.target_speed.insert(0, "1000")

        # Sweep Button
        self.run_btn= ttk.Button(teach_mode_frame, text="Run/Write",command=self.run_write_actions)
        self.run_btn.grid(row=0, column=5)

        #   ----------------------------------------------------------------  Auto Debug End 


        # ---------------------------------------------------------------- SPEED 

    def run_write_actions(self):
        self.set_target_speed()
        self.set_pos_low() 
    def set_target_speed(self):
        # Read the speed from the entry widget
        speed = self.target_speed.get()
        hex_speed= ParameterConverter.int_to_hex_string(speed)
        
        # Convert speed to int and prepare the Modbus command
        if hex_speed is not None:
            sendHex = f"01 06 01 29 {hex_speed}"
            self.modbus_sender.send_data(bytes.fromhex(sendHex))
            print(f"speed action with hex parameter: {sendHex}")

        else:
            print("Invalid speed")
            

    def set_pos_low(self):
        # Read the speed from the entry widget
        posLow = self.pos_low_entry.get()
        hex_posLow= ParameterConverter.int_to_hex_string(posLow)
        
        # Convert speed to int and prepare the Modbus command
        if hex_posLow is not None:
            sendHex = f"01 06 01 28 {hex_posLow}"
            self.modbus_sender.send_data(bytes.fromhex(sendHex))
            print(f"position action with hex parameter: {sendHex}")

            
        else:
            print("Invalid inputted number")








    def draw_initial_representation(self):
        self.degree_canvas.create_oval(10, 10, 190, 190, fill="white", outline="black")
        self.rotation_line = self.degree_canvas.create_line(100, 100, 100, 30, width=4, fill="red")  # Initial line position

    def on_degree_slider_change(self, value):
        angle = float(value)
        self.update_rotation_line(angle)

    def update_rotation_line(self, angle):
        angle_rad = (angle - 90) * (pi / 180)  # Adjust angle for canvas coordinates and convert to radians
        end_x = 100 + 70 * cos(angle_rad)
        end_y = 100 + 70 * sin(angle_rad)
        self.degree_canvas.coords(self.rotation_line, 100, 100, end_x, end_y)


    def on_servo_slider_change(self, value, servo_index):
        slider_value = int(float(value))
        self.servo_slider_labels[servo_index].config(text=f"Value: {slider_value}")

        # Move the finger based on the slider value
        # This simplistic approach directly links the slider value to the finger's height
        height_offset = slider_value * 1  # Adjust multiplier for desired effect
        self.canvas.coords(self.fingers[servo_index], 50 + servo_index*90, 150 - height_offset, 100 + servo_index*90, 150)
        
        # Here you would add the logic to send the servo command via Modbus
    
    def close_port(self):
        try:
            self.modbus_sender.close_connection()
            self.status_label.config(text="Port closed successfully.", foreground="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", foreground="red")

    def open_port(self):
        port = self.port_entry.get()
        baudrate = int(self.baudrate_entry.get())
        timeout = int(self.timeout_entry.get())

        try:
            self.modbus_sender.configure_port(port, baudrate, timeout)
            self.modbus_sender.open_connection()
            self.status_label.config(text="Port opened successfully.", foreground="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", foreground="red")

    def on_slider_change(self, event):
        slider_value = int(self.slider.get())
        self.slider_value_label.config(text=f"Value: {slider_value}")

    def forward_action(self):
        parameter = self.parameter_entry.get()
        #code = "01 06 02 02 03 E8"
        hex_parameter = ParameterConverter.int_to_hex_string(parameter)
        if hex_parameter is not None:
            sendHex = f"01 06 02 02 {hex_parameter}"
            print(f"Forward action with hex parameter: {hex_parameter}")
            print(f"send hex: {sendHex}")
            self.modbus_sender.send_data(bytes.fromhex(sendHex))
        else:
            print("Invalid parameter for forward action")

    def reverse_action(self):
        parameter = self.parameter_entry.get()
        hex_parameter = ParameterConverter.int_to_hex_string(ParameterConverter.convert_and_negate(parameter))
        if hex_parameter is not None:
            sendHex = f"01 06 02 02 {hex_parameter}"
            print(f"Reverse action with hex parameter: {hex_parameter}")
            print(f"send hex: {sendHex}")
            self.modbus_sender.send_data(bytes.fromhex(sendHex))
        else:
            print("Invalid parameter for Reverse action")

    def stop_action(self):
        sendHex = f"01 06 02 02 00 00"
        print(f"send hex: {sendHex}")
        print(f"stop button")
        self.modbus_sender.send_data(bytes.fromhex(sendHex))

    def auto_rotate(self):
        print(self.rotate_direction)
        if not self.auto_rotate_flag:
            self.auto_rotate_flag = True
            self.status_label.config(text="Auto-rotate started.", foreground="green")
            self.auto_rotate_step()
        else:
            self.auto_rotate_flag = False
            self.status_label.config(text="Auto-rotate stopped.", foreground="red")




    def auto_rotate_step(self):
        print(self.rotate_direction)
        if self.auto_rotate_flag:
            # Toggle between forward and reverse action based on rotate_direction
            if self.rotate_direction == "forward":
                self.forward_action()
                self.rotate_direction = "reverse"
            else:
                self.reverse_action()
                self.rotate_direction = "forward"

            # Schedule the next step. Adjust the delay (e.g., 2000 ms) as needed.
            self.root.after(2000, self.auto_rotate_step)




            
    # ---------------------------------------------------------------- for son toggle
    def toggle_son_action(self):
        if not hasattr(self, 'son_enabled') or not self.son_enabled:
            # Construct the command to enable SON
            sendHex = "01 06 00 0F 00 0F"  # Enable SON
            self.son_enabled = True
        else:
            # Construct the command to disable SON
            sendHex = "01 06 00 0F 00 00"  # Disable SON
            self.son_enabled = False

        print(f"SON {'enabled' if self.son_enabled else 'disabled'} with hex: {sendHex}")
        self.modbus_sender.send_data(bytes.fromhex(sendHex))


    # ---------------------------------------------------------------- for son toggle end
    

    # ---------------------------------------------------------------- for son toggle teach mode
        

        
    def toggle_teach_mode(self):
        # Toggle the Teach mode state
        if not self.teach_mode_enabled:
            # Construct the command to enable Teach mode
            sendHex = "01 06 01 26 00 03"  # Command to turn Teach mode on
        else:
            # Construct the command to disable Teach mode
            sendHex = "01 06 01 26 00 00"  # Command to turn Teach mode off
        
        # Toggle the state
        self.teach_mode_enabled = not self.teach_mode_enabled

        print(f"Teach mode {'enabled' if self.teach_mode_enabled else 'disabled'}")
        self.modbus_sender.send_data(bytes.fromhex(sendHex))

    # ---------------------------------------------------------------- for son toggle teach mode
    



    

if __name__ == "__main__":
    root = tk.Tk()

    modbus_sender = ModbusSerialSender(port='COM7', baudrate=115200, timeout=1)

    gui = ButtonSliderGUI(root, modbus_sender)
    # gui.update_speed_display() 

    root.mainloop()

    modbus_sender.close_connection()
