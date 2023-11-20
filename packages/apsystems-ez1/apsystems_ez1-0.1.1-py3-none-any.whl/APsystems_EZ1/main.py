from APsystems_EZ1 import APsystemsEZ1M


# testing

# Initialize the connection to the inverter
inverter = APsystemsEZ1M("192.168.178.167")

# Get device information

device_info = inverter.get_total_energy_lifetime()
print("RESPONSE:", device_info)
device_info = inverter.get_alarm_info()
#device_info = inverter.set_max_power(110)
print("RESPONSE:", device_info)
#time.sleep(3)