#!/usr/bin/env python3
"""Send one validated control object to a local running Godot rig.
Run Godot with -- --live-input. Use increasing seq values for its lifetime.
Example: python send_live.py --seq 1 '{"head_tilt":0.5,"mouth":"A"}'
Send updates more frequently than two seconds or the rig releases to neutral.
"""
import argparse,json,socket
p=argparse.ArgumentParser();p.add_argument('--seq',type=int,required=True);p.add_argument('controls');a=p.parse_args()
c=json.loads(a.controls)
if not isinstance(c,dict):p.error('controls must be a JSON object')
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:s.sendto(json.dumps({'seq':a.seq,'controls':c}).encode(),('127.0.0.1',9122))
