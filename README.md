# Test-Stand-Control

## General Info
This is the control system for the liquid rocket test stand. It includes functionality for reading sensor data and moving the regulator motors.

## Setup
In order to operate the test stand, you will need two computers: a local one, for sending I/O, and a controller, which will be connected to I2C and GPIO components on the test stand.

The computers communicate via Ethernet, and need static IP addresses to function. Assign the ip `10.0.0.1/24` to the controller, and `10.0.0.x/24` to the local computer. `x` can be any number between 2 and 255. Connect the two computers directly with an ethernet cable, and you should be able to ping the controller from the local computer:

```
ping 10.0.0.1
```

On the test stand, clone the project to a local directory, and then run main.py:
```
git clone https://github.com/Alabama-Rocketry-Association/Test-Stand-Control
cd Test-Stand-Control
python3 main.py
```
On the local computer, clone the project to a local directory, and then run host.py:
```
git clone https://github.com/Alabama-Rocketry-Association/Test-Stand-Control
cd Test-Stand-Control
python3 host.py
```

## Usage
The local computer will be able to send commands to the controller. The connection can be tested with `ping`, and a list of all commands can be displayed with `help`

Some commands require parameters, which should be separated with a space. For example, `lox_inc 50` will turn the lox motor clockwise 50 degrees.

If either computer disconnects, restart the program, and they will automatically reconnect.