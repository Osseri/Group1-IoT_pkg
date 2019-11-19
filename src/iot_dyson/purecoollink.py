#!/usr/bin/env python3
#-*-coding:utf-8-*-

from iot_dyson.libpurecoollink.libpurecoollink.dyson import DysonAccount
from iot_dyson.libpurecoollink.libpurecoollink.const import FanSpeed, FanMode, NightMode, Oscillation, \
    FanState, StandbyMonitoring, QualityTarget, ResetFilter, HeatMode, \
    FocusMode, HeatTarget

import urllib3
import time
# ignore InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 파이썬3 lib 설치 필요
# sudo pip3 install libpurecoollink


class Purecoollink:


    def __init__(self):
        
        """
        ID: FAN
        COMMAND:(    ON   ), (OFF), (  OSC  )
        PARAM:  (1-10 or x), ( x ), (ON, OFF)

        """

        # Dyson 계정 로그인
        dyson_account = DysonAccount("skkang.robocare@gmail.com","robocare1122!","KR")
        logged = dyson_account.login()
        print '-'
        print logged # True
        if not logged:
            report["result"] = False
            report["response"] = 'Unable to login to Dyson account'
            return report

        # Dyson 계정에서 사용할 수있는 장치 나열
        self.devices = dyson_account.devices()

        # for device in self.devices:
        #     print device
        # 검색을 사용하여 첫 번째 기기에 연결
        print '-'
        print self.devices # [DysonPureCoolLink(serial=SS2-KR-JKA1158A,active=True,name=휴게실,version=21.04.03,auto_update=True,new_version_available=False,product_type=475,network_device=None)]
        print '-'
        # connected = self.devices[0].auto_connect()
        connected = self.devices[0].connect("192.168.43.234")
        print connected # True 접속, False 접속 불가
        print '-'
        # connected == 장치 사용 가능, 상태 값 사용 가능, 센서 값 사용 가능


    def execute(self, srv):

        report = {
            "result": True,
            "response": ""
        }


        try:
            if srv.command.upper() == "OFF":
                # fan 속도 조절 (2)
                self.devices[0].set_configuration(fan_mode=FanMode.OFF)
            elif srv.command.upper() == "ON":
                if not srv.param:
                    self.devices[0].set_configuration(fan_mode=FanMode.FAN)
                else:
                    speed = srv.param.pop()
                    if speed == "1":
                        self.devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_1)
                    elif speed == "2":
                        self.devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_2)
                    elif speed == "3":
                        self.devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_3)
                    elif speed == "4":
                        self.devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_4)
                    elif speed == "5":
                        self.devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_5)
                    elif speed == "6":
                        self.devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_6)
                    elif speed == "7":
                        self.devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_7)
                    elif speed == "8":
                        self.devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_8)
                    elif speed == "9":
                        self.devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_9)
                    elif speed == "10":
                        self.devices[0].set_configuration(fan_mode=FanMode.FAN, fan_speed=FanSpeed.FAN_SPEED_10)
            elif srv.command.upper() == "OSC":
                # 회전 기능 (ON)
                oscillation = srv.param.pop().upper()
                if oscillation == "ON":
                    self.devices[0].set_configuration(oscillation=Oscillation.OSCILLATION_ON)
                elif oscillation == "OFF":
                    self.devices[0].set_configuration(oscillation=Oscillation.OSCILLATION_OFF)
        except Exception as e:
            report["result"] = False
            report["response"] = str(e)
            return report



        # # 야간 모드 (ON)
        # self.devices[0].set_configuration(night_mode=NightMode.NIGHT_MODE_ON)

        # # 슬립 타이머 (Set 10 minutes)
        # self.devices[0].set_configuration(sleep_timer=10)

        # # 슬립 타이머 끄기
        # self.devices[0].set_configuration(sleep_timer=0)

        # # Set quality target (for auto mode)
        # self.devices[0].set_configuration(quality_target=QualityTarget.QUALITY_NORMAL)

        # # Disable standby monitoring
        # self.devices[0].set_configuration(standby_monitoring=StandbyMonitoring.STANDBY_MONITORING_OFF)


        # ... connection do dyson account and to device ... #

        # Disconnect
        # self.devices[0].disconnect()

        return report
