class Wheel:

    def __init__(self):
        self.current_step = 0
        self.steps_per_face_spin = 500 #change this variable to however many steps needed per face change thingie

    def spin_wheel(self, future_step):
        forward = future_step - self.current_step
        backward = self.current_step - forward
        if future_step == self.current_step:
            return
        elif abs(forward) < abs(backward):
            Move_motor_steps(forward)    #function that Tim has to spin motor
            self.current_step = (self.current_step + forward) % (8*self.steps_per_face_spin)
            print(f"Spinning forward {forward} steps to face {future_step}")
        else:
            Move_motor_steps(backward)    #function that Tim has to spin motor
            self.current_step = (self.current_step + backward) % (8*self.steps_per_face_spin)
            print(f"Spinning backward {backward} steps to face {future_step}")
        return

    # Add a calibration method if we have time.
