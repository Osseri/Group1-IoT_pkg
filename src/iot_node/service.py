#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from std_msgs.msg import String
import threading
import rospy
import requests
import json
import time
import random

from singleton import Singleton
from iot_msgs.srv import IotRos, IotRosResponse

from iot_dyson.purecoollink import Purecoollink

from mihome.base import XiaomiConnection
from mihome.gateway import Gateway
from mihome.config_manager import YamlConfig

from pywebostv.discovery import *
from pywebostv.connection import *
from pywebostv.controls import *

class Service(Singleton):

    __iot_service_proxy = None
    __device = {
        "FAN":"req_fan", # 1
        "PLUG":"req_plug", # 1
        "LIFX":"req_lifx", # 1
        "BLIND":"req_blind", # 1
        "AIRJET":"req_airjet", # 1

        "XIAOMI":"req_xiaomi", # 3
        "LG":"req_lg" # 2
    }
    __xiaomi_status = {}


    def handle_service(self, srv):
        id_ = srv.id
        if '_' in srv.id:
            id_ = srv.id.split('_')[0]
        for key, value in self.__device.iteritems():
            print "id_: "+id_+", key: "+key+", value: "+value
            if id_.upper() == key:
                func = getattr(self, value)
                result = func(srv)
                print "result: " + str(result)
                resp_srv = IotRosResponse()
                resp_srv.result = result["result"]
                resp_srv.response.append(result["response"])
                return resp_srv


    def req_lg(self, srv):
        """
        ID: LG
        COMMAND: TV, BEAM
        """
        response = None
        if srv.command == "TV":
            store = {}
            store['client_key'] = 'ba9b616e04aa74690c5ceca73a5210a0'
            client = WebOSClient('192.168.111.3')
            client.connect()
            for status in client.register(store):
                if status == WebOSClient.PROMPTED:
                    print("Please accept the connect on the TV!")
                elif status == WebOSClient.REGISTERED:
                    print("Registration successful!")
        elif srv.command == "BEAM":
            store = {}
            store['client_key'] = '0bfefd95b58765e5454f4227a4781105'
            client = WebOSClient('192.168.111.16')
            client.connect()
            for status in client.register(store):
                if status == WebOSClient.PROMPTED:
                    print("Please accept the connect on the CineBeam!")
                elif status == WebOSClient.REGISTERED:
                    print("Registration successful!")
        time.sleep(5)
        media = MediaControl(client)
        media.set_volume(15)
        time.sleep(5)
        media.set_volume(5)
        time.sleep(5)
        system_control = SystemControl(client)
        system_control.power_off()
        report = {
            "result": True,
            "response": "Com"
        }
        return report


    def req_xiaomi(self, srv):
        """
        ID: XIAOMI
        COMMAND: MAGNET, PLUG, SENSORHT
        """
        response = None
        if srv.command == "MAGNET":
            response = json.dumps(self.__xiaomi_status["magnet"])
        elif srv.command == "PLUG":
            response = json.dumps(self.__xiaomi_status["plug"])
        elif srv.command == "SENSORHT":
            response = json.dumps(self.__xiaomi_status["sensorHT"])
        report = {
            "result": True,
            "response": response
        }
        return report


    def req_fan(self, srv):
        """
        ID: FAN
        COMMAND:(    ON   ), (OFF), (  OSC  )
        PARAM:  (1-10 or x), ( x ), (ON, OFF)
        """
        report = self.p.execute(srv)
        return report


    def req_plug(self, srv):
        """
        ID: PLUG
        COMMAND: (POWER), (INFO)
        PARAM:   ( 0, 1), ( x  )
        """
        report = {
            "result": False,
            "response": ""
        }
        url = 'https://thing.brunt.co:8080/thing/hub/'
        headers = {"apiKey":"8dd70b643458419798b0125a9c9ce40d38cf60f1e9cc4f11b76dc1b448fef1e8"}
        try:
            id_ = '9abcfb1fbf3448ef'
            if srv.command.upper() == "POWER":
                # TODO PUT - 사물 상태 바꾸기
                params = {"power":srv.param.pop()}
                data = json.dumps(params)
                response = requests.put(url+id_, headers=headers, data=data)
                report["result"] = True
                report["response"] = str(response)
            elif srv.command.upper() == "INFO":
                # TODO GET - 사물 정보 가져오기
                response = requests.get(url+id_, headers=headers)
                report["result"] = True
                report["response"] = str(json.loads(response.text))
            else:
                raise Exception("Wrong command")
        except Exception as e:
            report["response"] = str(e)
        return report


    def req_lifx(self, srv):
        """
        ID: LIFX
        COMMAND: ON, OFF
        PARAM: RED, BLUE, GREEN.....
        """
        report = {
            "result": False,
            "response": ""
        }
        try:
            token = 'c798c50932700b31248d6d28b32a4f515a47f47b0a1e641296b02484c652d794'
            headers = {
                "Authorization": "Bearer %s" % token,
            }
            param = ""
            for i in srv.param:
                param += i.lower()
            payload = {
                "power": srv.command.lower(),
                "color": param
            }
            response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)
            report["result"] = True
            report["response"] = str(response)
        except Exception as e:
            report["response"] = str(e)
        return report


    def req_blind(self, srv):
        """
        ID: BLIND
        COMMAND: UP, DOWN, MIDDLE, INFO
        """
        report = {
            "result": False,
            "response": ""
        }
        url = 'https://thing.brunt.co:8080/thing/hub/'
        headers = {"apiKey":"8dd70b643458419798b0125a9c9ce40d38cf60f1e9cc4f11b76dc1b448fef1e8"}
        try:
            id_ = '0015k63m45s1121e'
            if srv.command.upper() == "UP":
                params = {"requestPosition":"100"}
                data = json.dumps(params)
                response = requests.put(url+id_, headers=headers, data=data)
                report["result"] = True
                report["response"] = str(response)
            elif srv.command.upper() == "DOWN":
                params = {"requestPosition":"0"}
                data = json.dumps(params)
                response = requests.put(url+id_, headers=headers, data=data)
                report["result"] = True
                report["response"] = str(response)
            elif srv.command.upper() == "MIDDLE":
                params = {"requestPosition":"50"}
                data = json.dumps(params)
                response = requests.put(url+id_, headers=headers, data=data)
                report["result"] = True
                report["response"] = str(response)
            elif srv.command.upper() == "INFO":
                # TODO GET - 사물 정보 가져오기
                response = requests.get(url+id_, headers=headers)
                report["result"] = True
                report["response"] = str(json.loads(response.text))
            else:
                raise Exception("Wrong command")
        except Exception as e:
            report["response"] = str(e)
        return report
    

    def req_airjet(self, srv):
        """
        ID: AIRJET
        COMMAND: POWER, INFO
        PARAM: OFF, AUTO, 2, 3, TURBO
        """
        report = {
            "result": False,
            "response": ""
        }
        url = 'https://thing.brunt.co:8080/thing/hub/'
        param_list = [
            'OFF', 'AUTO', '2', '3', 'TURBO'
        ]
        headers = {"apiKey":"8dd70b643458419798b0125a9c9ce40d38cf60f1e9cc4f11b76dc1b448fef1e8"}
        try:
            id_ = '0017ch0w9nte0312'
            if srv.command.upper() == 'POWER':
                req_param = srv.param.pop().upper()
                if req_param in param_list:
                    params = {"power":str(param_list.index(req_param))}
                    data = json.dumps(params)
                    response = requests.put(url+id_, headers=headers, data=data)
                    report["result"] = True
                    report["response"] = str(response)
                else:
                    raise Exception("Wrong param")
            elif srv.command.upper() == 'INFO':
                response = requests.get(url+id_, headers=headers)
                report["result"] = True
                report["response"] = str(json.loads(response.text))
            else:
                raise Exception("Wrong command")
        except Exception as e:
            report["response"] = str(e)
        return report


    def xiaomi_thread(self, magnet, plug, sensor_ht):
        while True:
            magnetData = magnet.read()["data"]
            magnetStringToJson = json.loads(magnetData)
            plugData = plug.read()["data"]
            plugStringToJson = json.loads(plugData)
            sensorHTDate = sensor_ht.read()["data"]
            sensorHTStringToJson = json.loads(sensorHTDate)
            xiaomiStatus = {
                "magnet": {
                    "status": magnetStringToJson["status"]
                },
                "plug": {
                    "status": plugStringToJson["status"],
                    "inuse": plugStringToJson["inuse"]
                },
                "sensorHT": {
                    "temperature": int(sensorHTStringToJson["temperature"]) / 100,
                    "humidity": int(sensorHTStringToJson["humidity"]) / 100
                }
            }
            self.__xiaomi_status.update(xiaomiStatus)
            print '*****'
            print self.__xiaomi_status
            print '*****'
            time.sleep(5)


    def initXiaomi(self):
        conn = XiaomiConnection()
        gateway_data = {}
        gateway_data['sid'] = '7c49ebb41bc4'
        gateway_data['ip'] = '192.168.111.9'
        gateway_data['port'] = 9898
        gateway = Gateway(
            connection=conn,
            sid=gateway_data['sid'],
            ip=gateway_data['ip'],
            port=gateway_data['port']
        )
        gateway.register_subdevices()
        print '------------------------------'
        print gateway.connected_devices
        print '------------------------------'
        magnet = gateway.connected_devices['magnet'][0]
        plug = gateway.connected_devices['plug'][0]
        sensor_ht = gateway.connected_devices['sensor_ht'][1]
        t = threading.Thread(target=self.xiaomi_thread, args=(magnet, plug, sensor_ht))
        t.start()

    def __init__(self):
        self.initXiaomi()
        rospy.Service("/iot_ros/command", IotRos, self.handle_service)
        self.p = Purecoollink()
