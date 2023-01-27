# Has modes of driving such as arcade drive, tank drive, mecanum drive, etc.
# Those driving modes use the simpler functions that turn motors/drivetrains

from ctre import WPI_TalonFX
from rev import CANSparkMax
from utils import constants, math_functions
import math


class Drive:
   def __init__(self, _frontLeft : WPI_TalonFX, _frontRight : WPI_TalonFX, _middleLeft : CANSparkMax, _middleRight : CANSparkMax, _backLeft : WPI_TalonFX, _backRight : WPI_TalonFX):
      
      # Front and back mecanum wheels are powered Falcon500 motors
      self.frontLeft = _frontLeft
      self.frontRight = _frontRight
      self.backLeft = _backLeft
      self.backRight = _backRight

      # Middle omni wheels are powered by Neo550 motors
      self.middleRight = _middleRight
      self.middleLeft = _middleLeft

      # Constant wheel speed/voltages
      self.MIDDLE_WHEEL_SPEED = 3


   # set the speed of the wheels on the left of the robot and includes the middle wheels
   def setLeftSpeed(self, speed):
      # clamp the speed from -1 to 1
      speed = math_functions.clamp(speed, -1, 1)

      self.frontLeft.set(speed)
      self.backLeft.set(speed)
      self.middleRight.setVoltage(self.MIDDLE_WHEEL_SPEED)


   # set the speed of the wheels on the right of the robot and includes the middle wheels
   def setRightSpeed(self, speed):
      # clamp the speed from -1 to 1
      speed = math.functions.clamp(speed, -1, 1)

      self.frontRight.set(speed)
      self.backRight.set(speed)
      self.middleRight.setVoltage(self.MIDDLE_WHEEL_SPEED)


   def setSpeed(self, speed):
      self.setLeftSpeed(speed)
      self.setRightSpeed(speed)

   
   def arcadeDrive(self, x, y):
      pass


   def tankDrive(self, joystick_left, joystick_right):
      self.setLeftSpeed(joystick_left)
      self.setRightSpeed(joystick_right)


   def mecanumDrive(self, joystick_x, joystick_y):
      frontLeftSpeed = joystick_y + joystick_x
      frontRightSpeed = joystick_y - joystick_x
      backRightSpeed = frontLeftSpeed
      backLeftSpeed = frontRightSpeed

      steer = 0
      frontLeftSpeed -= steer
      frontRightSpeed += steer
      backLeftSpeed -= steer
      backRightSpeed += steer

      self.frontLeft.setSpeed(frontLeftSpeed)
      self.frontRight.setSpeed(frontRightSpeed)
      self.backLeft.setSpeed(backLeftSpeed)
      self.backRight.setSpeed(backRightSpeed)


   # Actual driving mode functions
   