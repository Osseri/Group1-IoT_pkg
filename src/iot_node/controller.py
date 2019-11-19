# #!/usr/bin/python
# #-*-coding:utf-8-*-

# from iot_dyson.libpurecoollink.libpurecoollink.dyson import DysonAccount
# from iot_dyson.libpurecoollink.libpurecoollink.const import FanSpeed, FanMode, NightMode, Oscillation, \
#     FanState, StandbyMonitoring, QualityTarget, ResetFilter, HeatMode, \
#     FocusMode, HeatTarget

# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# # 파이썬3 lib 설치 필요
# # sudo pip3 install libpurecoollink


# class Controller:


#     def __init__(self):

#         # Dyson 계정 로그인
#         dyson_account = DysonAccount("skkang.robocare@gmail.com","robocare1122!","KR")
#         logged = dyson_account.login()

#         if not logged:
#             print('Unable to login to Dyson account')
#             exit(1)

#         # Dyson 계정에서 사용할 수있는 장치 나열
#         devices = dyson_account.devices()
#         # print(devices)

#         # 검색을 사용하여 첫 번째 기기에 연결
#         connected = devices[0].auto_connect()

#         # connected == 장치 사용 가능, 상태 값 사용 가능, 센서 값 사용 가능


#         # fan 속도 조절 (2)
#         devices[0].set_configuration(fan_mode=FanMode.OFF)
#         # devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_5)

#         # 회전 기능 (ON)
#         # devices[0].set_configuration(oscillation=Oscillation.OSCILLATION_OFF)

#         # # 야간 모드 (ON)
#         # devices[0].set_configuration(night_mode=NightMode.NIGHT_MODE_ON)

#         # # 슬립 타이머 (Set 10 minutes)
#         # devices[0].set_configuration(sleep_timer=10)

#         # # 슬립 타이머 끄기
#         # devices[0].set_configuration(sleep_timer=0)

#         # # Set quality target (for auto mode)
#         # devices[0].set_configuration(quality_target=QualityTarget.QUALITY_NORMAL)

#         # # Disable standby monitoring
#         # devices[0].set_configuration(standby_monitoring=StandbyMonitoring.STANDBY_MONITORING_OFF)


#         # ... connection do dyson account and to device ... #

#         # Disconnect
#         devices[0].disconnect()