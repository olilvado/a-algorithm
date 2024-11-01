#!/usr/bin/env python
# coding: utf-8

import json
import time
import utils
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/aStarConnection', methods=['POST'])
def main():

    #key = request.json.get('key')
    key = '1'
    if key == '0': # 정지 신호를 줄 경우
        utils.on_ship_control(key)
        return jsonify({"stop": "ship stop (on_ship_control)"}), 200
    elif key == '1':
        inputWaypoint = json.loads(request.json.get('waypoints', None))

        if inputWaypoint is None: # 유효한 웨이포인트가 있을 때 출력(그냥 확인용)
            return jsonify({"error": "No waypoints provided"}), 400
        elif inputWaypoint:
            print("Received inputWaypoint:", inputWaypoint)

        # 초기화
        utils.init_simulation()
        utils.init_waypoints_and_obstacles(inputWaypoint)
        full_route_lats, full_route_lons = utils.init_route()

        coordinates = [
            {"lat": lat, "lng": lon}
            for lat, lon in zip(full_route_lats, full_route_lons)
        ]
        return jsonify(coordinates)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 모든 IP에서 접근 가능하도록 설정
