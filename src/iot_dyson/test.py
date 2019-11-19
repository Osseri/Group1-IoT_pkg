from libpurecoollink.dyson import DysonAccount
from libpurecoollink.const import FanSpeed, FanMode, NightMode, Oscillation, \
    FanState, StandbyMonitoring, QualityTarget, ResetFilter, HeatMode, \
    FocusMode, HeatTarget

# Log to Dyson account
# Language is a two characters code (eg: FR)
dyson_account = DysonAccount("sjlee.robocare@gmail.com","sdfsdf1","KR")
logged = dyson_account.login()

if not logged:
    print('Unable to login to Dyson account')
    exit(1)

# List devices available on the Dyson account
devices = dyson_account.devices()
print('---------------------------------------')
print(devices)
print('---------------------------------------')
# Connect using discovery to the first device
connected = devices[0].auto_connect()

# connected == device available, state values are available, sensor values are available



# # ... connection do dyson account and to device ... #

# # Turn on the fan to speed 2
# devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_2)

# # Turn on oscillation
# devices[0].set_configuration(oscillation=Oscillation.OSCILLATION_ON)

# # Turn on night mode
# devices[0].set_configuration(night_mode=NightMode.NIGHT_MODE_ON)

# # Set 10 minutes sleep timer
# devices[0].set_configuration(sleep_timer=10)

# # Disable sleep timer
# devices[0].set_configuration(sleep_timer=0)

# # Set quality target (for auto mode)
# devices[0].set_configuration(quality_target=QualityTarget.QUALITY_NORMAL)

# # Disable standby monitoring
# devices[0].set_configuration(standby_monitoring=StandbyMonitoring.STANDBY_MONITORING_OFF)

# # Reset filter life
# devices[0].set_configuration(reset_filter=ResetFilter.RESET_FILTER)

# ## Cool+Hot devices only
# # Set Heat mode
# devices[0].set_configuration(heat_mode=HeatMode.HEAT_ON)
# # Set heat target
# devices[0].set_configuration(heat_target=HeatTarget.celsius(25))
# devices[0].set_configuration(heat_target=HeatTarget.fahrenheit(70))
# # Set fan focus mode
# devices[0].set_configuration(focus_mode=FocusMode.FOCUS_ON)



# Everything can be mixed in one call
devices[0].set_configuration(
    sleep_timer=0,
    fan_mode=FanMode.FAN,
    fan_speed=FanSpeed.FAN_SPEED_8,
    oscillation=Oscillation.OSCILLATION_ON,
    night_mode=NightMode.NIGHT_MODE_OFF,
    standby_monitoring=StandbyMonitoring.STANDBY_MONITORING_ON,
    quality_target=QualityTarget.QUALITY_HIGH)

# Disconnect
devices[0].disconnect()