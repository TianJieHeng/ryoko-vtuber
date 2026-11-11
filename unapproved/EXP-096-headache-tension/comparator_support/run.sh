#!/bin/sh
set -e
cd /workspace/scratch/42f2baf55663
export HOME=$PWD/stunned_silence_work/local_environment/home XDG_CACHE_HOME=$PWD/stunned_silence_work/local_environment/cache XDG_CONFIG_HOME=$PWD/stunned_silence_work/local_environment/config XDG_DATA_HOME=$PWD/stunned_silence_work/local_environment/data LP_NUM_THREADS=2
godot --rendering-method gl_compatibility --audio-driver Dummy --path insight_integration_work/ryoko_object_rig --script $PWD/stunned_silence_work/runtime_parity/check.gd -- --capture > stunned_silence_work/runtime_parity/baseline.log 2>&1
godot --rendering-method gl_compatibility --audio-driver Dummy --path stunned_integration_work/ryoko_object_rig --script $PWD/stunned_silence_work/runtime_parity/check.gd -- --capture --patched > stunned_silence_work/runtime_parity/patched.log 2>&1
printf "RUNTIME_PARITY_EXIT=%s\n" "$?"
