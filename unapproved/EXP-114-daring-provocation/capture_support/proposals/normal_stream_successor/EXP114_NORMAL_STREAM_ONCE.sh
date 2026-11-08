#!/bin/sh
/usr/bin/python3 -B /workspace/scratch/42f2baf55663/daring_provocation_performance_work/proposals/normal_stream_successor/run_normal_stream.py normal --coordinator-godot-slot-granted --coordinator-display-lease-granted --independent-pre-render-review-approved > /workspace/scratch/42f2baf55663/daring_provocation_performance_work/evidence/CUA_NORMAL_STREAM_LAUNCH.log 2>&1
rc=$?
printf 'EXP114_NORMAL_PLAYBACK_EXIT=%s\n' "$rc" > /workspace/scratch/42f2baf55663/daring_provocation_performance_work/evidence/CUA_NORMAL_STREAM_LAUNCH_EXIT.txt
exit "$rc"
