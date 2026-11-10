#!/bin/sh
# Default: headless numerical checks. Native capture is explicit and never overwrites.
set -eu
W=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export HOME="$W/local_environment/home" XDG_CACHE_HOME="$W/local_environment/cache" XDG_CONFIG_HOME="$W/local_environment/config" XDG_DATA_HOME="$W/local_environment/data" LP_NUM_THREADS=2
mkdir -p "$HOME" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME"
case "${1:---state}" in
  --state)
    godot --headless --path "$W/rig" --script "$W/render_motion.gd" > "$W/motion_state.log" 2>&1
    ;;
  --capture)
    if [ -e "$W/motion" ] || [ -e "$W/motion_checks.json" ]; then
      printf '%s\n' 'Preserve and inspect existing motion capture before another run.' >&2
      exit 2
    fi
    godot --rendering-method gl_compatibility --audio-driver Dummy --path "$W/rig" --script "$W/render_motion.gd" -- --capture > "$W/motion_native.log" 2>&1
    ;;
  *) printf '%s\n' 'Usage: run_motion.sh [--state | --capture]' >&2; exit 2 ;;
esac
printf 'MOTION_EXIT=0\n'
