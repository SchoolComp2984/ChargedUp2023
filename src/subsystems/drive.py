# Has modes of driving such as arcade drive, tank drive, mecanum drive, etc.
# Those driving modes use the simpler functions that turn motors/drivetrains

from ctre import WPI_TalonFX
from rev import CANSparkMax
from utils import constants, math_functions, imutil, pid
import math


class Drive:
   def __init__(self, _frontLeft : WPI_TalonFX, _frontRight : WPI_TalonFX, _middleLeft : CANSparkMax, _middleRight : CANSparkMax, _backLeft : WPI_TalonFX, _backRight : WPI_TalonFX, _drive_imu : imutil.Imutil, _pid : pid.PID):
      
      # Front and back mecanum wheels are powered Falcon500 motors
      self.drive_p = 1
      self.drive_i = 0
      self.drive_d = 0
      self.drive_val = 0

      self.front_left = _frontLeft
      self.front_left_pid = pid.PID()
      self.front_left_pid.set_pid(self.drive_p, self.drive_i, self.drive_d, self.drive_val)

      self.front_right = _frontRight
      self.front_right_pid = pid.PID()
      self.front_right_pid.set_pid(self.drive_p, self.drive_i, self.drive_d, self.drive_val)

      self.back_left = _backLeft
      self.back_left_pid = pid.PID()
      self.back_left_pid.set_pid(self.drive_p, self.drive_i, self.drive_d, self.drive_val)

      self.back_right = _backRight
      self.back_right_pid = pid.PID()
      self.back_right_pid.set_pid(self.drive_p, self.drive_i, self.drive_d, self.drive_val)


      # Middle omni wheels are powered by Neo550 motors
      self.middle_right = _middleRight
      self.middle_left = _middleLeft

      # imu and pid stuff to be added below
      self.drive_imu = _drive_imu

      self.pid = _pid
      self.pid.set_pid(0.01, 0.0002, 0.05, 0)

      self.pid_secondary = _pid
      self.pid_secondary.set_pid(0.01, 0.0002, 0.05, 0)


   # set the speed of the wheels on the left of the robot and includes the middle wheels
   def set_left_speed(self, speed):
      # clamp the speed from -1 to 1
      speed = math_functions.clamp(speed, -1, 1)

      self.front_left.set(speed)
      self.back_left.set(speed)
      #self.middle_right.setVoltage(constants.DRIVE_MIDDLE_WHEEL_SPEED)


   # set the speed of the wheels on the right of the robot and includes the middle wheels
   def set_right_speed(self, speed):
      # clamp the speed from -1 to 1
      speed = math_functions.clamp(speed, -1, 1)

      self.front_right.set(speed)
      self.back_right.set(speed)
      #self.middle_right.setVoltage(constants.DRIVE_MIDDLE_WHEEL_SPEED)


   def set_speed(self, speed):
      self.set_left_speed(speed)
      self.set_right_speed(speed)


   def stop_drive(self):
      self.set_speed(0)

   def get_yaw(self):
      return self.drive_imu.getYaw()

   # DRIVE FUNCTIONS
   def arcade_drive(self, joystick_x, joystick_y):
      left_speed = (joystick_y - joystick_x) * constants.DRIVE_MOTOR_POWER_MULTIPLIER
      right_speed = (joystick_y + joystick_x) * constants.DRIVE_MOTOR_POWER_MULTIPLIER

      self.set_left_speed(left_speed)
      self.set_right_speed


   def tank_drive(self, joystick_left, joystick_right):
      self.set_left_speed(joystick_left)
      self.set_right_speed(joystick_right)


   def mecanum_drive(self, joystick_x, joystick_y):
      front_left_speed = joystick_y + joystick_x
      front_right_speed = joystick_y - joystick_x
      back_right_speed = front_left_speed
      back_left_speed = front_right_speed

      steer = 0
      front_left_speed -= steer
      front_right_speed += steer
      back_left_speed -= steer
      back_right_speed += steer

      # if we end up using this in the future, tune steer using PID instead of just setting it to zero

      # set middle wheel speeds to the average speed of the wheels on the respective sides
      # utilizes the additional power that the middle wheels offer without interfering with mecanum drive (hopefully)
      # might need to round down the avg values or set them to zero if they are in a small range close to 0
      middle_left_speed = (front_left_speed + back_left_speed) / 2
      middle_right_speed = (front_right_speed + back_right_speed) / 2

      self.front_left.set_speed(front_left_speed)
      self.middle_left.set_speed(middle_left_speed)
      self.back_left.set_speed(back_left_speed)

      self.front_right.set_speed(front_right_speed)
      self.middle_right.set_speed(middle_right_speed)
      self.back_right.set_speed(back_right_speed)


   def absolute_drive(self, speed, left_right, desired_angle, normal_drive, multiplier):
      # clamp the speed between -1 and 1 for safety purposes
      clamped_speed = math_functions.clamp(speed, -1, 1)
      
      # angle calculations
      current_angle = self.drive_imu.getYaw()
      delta_angle = desired_angle - current_angle
      # put delta_angle in a range from -180 to 180 degrees
      delta_angle = ((delta_angle + 180) % 360) - 180

      print(f"current angle = {current_angle}, desired_angle = {desired_angle}")

      # set "steer" to zero
      steer = 0

      if self.drive_imu.check_if_working():
            if normal_drive:
               steer = max(-1, min(1, self.pid.steer_pid(delta_angle)))
               #print(f"steer: {steer}")
            else:
               steer = math_functions.clamp(self.pid_secondary(delta_angle), -1, 1)

      #steer = 0

      # for next year have to manually make sure the signs are good its kinda weird sometimes   
      #self.front_left.set((clamped_speed - left_right - steer) * multiplier)
      #self.front_right.set((clamped_speed + left_right + steer) * multiplier)
      #self.back_left.set((clamped_speed + left_right - steer) * multiplier)
      #self.back_right.set((clamped_speed - left_right + steer) * multiplier)

      #self.front_left.set(-(clamped_speed + left_right + steer) * multiplier * 0.5)
      #self.front_right.set((clamped_speed - left_right - steer) * multiplier * 0.5)
      #self.back_left.set(-(clamped_speed - left_right + steer) * multiplier * 1)
      #self.back_right.set((clamped_speed + left_right - steer) * multiplier * 1)

      # speed = (-(clamped_speed + left_right + steer)) * multiplier
      # current_encoder = encoder()
      # error = (encoder - prev_encoder) - speed
      # front_left.set_motor_power(pid.arm_pid(error))
      # prev_encoder = current_encoder


      front_left_speed = (-(clamped_speed + left_right + steer) * multiplier)
      # end of 3/11 meeting starting PID control for drive

      self.front_left.set(-(clamped_speed + left_right + steer) * multiplier * 0.5)
      self.front_right.set((clamped_speed - left_right - steer) * multiplier * 0.5)
      self.back_left.set(-(clamped_speed - left_right + steer) * multiplier * 1)
      self.back_right.set((clamped_speed + left_right - steer) * multiplier * 1)

      # self.middle_left.setVoltage((clamped_speed + steer) * multiplier * 5)
      # self.middle_right.setVoltage((clamped_speed - steer) * multiplier * 5)