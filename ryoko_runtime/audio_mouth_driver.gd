extends Node
# Amplitude-driven opening, not phoneme recognition or microphone capture.
var level=0.0
var raw_level=0.0
var active=false
var external=false
var mouth="REST"
var gain=4.8
var envelope=PackedFloat32Array()
var duration=0.0
var elapsed=0.0
var player:AudioStreamPlayer
var deterministic=false
var error_message=""

func _ready():
    player=AudioStreamPlayer.new()
    add_child(player)

func load_wav(path:String)->bool:
    stop()
    error_message=""
    var stream=AudioStreamWAV.load_from_file(path)
    if stream==null:
        error_message="Cannot load WAV: "+path
        return false
    if stream.format not in [AudioStreamWAV.FORMAT_8_BITS,AudioStreamWAV.FORMAT_16_BITS]:
        error_message="Use uncompressed 8-bit or 16-bit PCM WAV."
        return false
    var bytes_per_sample=2 if stream.format==AudioStreamWAV.FORMAT_16_BITS else 1
    var channels=2 if stream.stereo else 1
    var pcm=stream.data
    var frames=pcm.size()/(bytes_per_sample*channels)
    if frames==0 or stream.mix_rate<=0:
        error_message="Empty WAV."
        return false
    duration=float(frames)/stream.mix_rate
    envelope.clear()
    var window=max(1,int(stream.mix_rate*0.01))
    for start in range(0,frames,window):
        var energy=0.0
        var count=0
        for frame in range(start,min(start+window,frames)):
            for channel in range(channels):
                var index=(frame*channels+channel)*bytes_per_sample
                var sample=float(pcm.decode_s16(index))/32768.0 if bytes_per_sample==2 else float(pcm[index]-128)/128.0
                energy+=sample*sample
                count+=1
        envelope.append(sqrt(energy/max(1,count)))
    player.stream=stream
    return true

func play():
    if player.stream==null or envelope.is_empty():return false
    level=0.0;raw_level=0.0;elapsed=0.0;mouth="REST"
    active=true;external=false;player.play()
    return true

func set_level(value:float):
    if not is_finite(value):value=0.0
    if player.playing:player.stop()
    external=true;active=true;raw_level=clamp(value,0.0,1.0)

func stop():
    if player!=null:player.stop()
    active=false;external=false;level=0.0;raw_level=0.0;elapsed=0.0;mouth="REST"

func step(delta:float)->String:
    if not active:return "REST"
    if not external:
        if not deterministic and not player.playing:
            stop()
            return "REST"
        # Movie writer uses simulation time; normal playback uses the audio clock.
        var position=elapsed if deterministic else max(0.0,player.get_playback_position()+AudioServer.get_time_since_last_mix()-AudioServer.get_output_latency())
        if position>=duration-0.00001:
            stop()
            return "REST"
        raw_level=clamp(envelope[min(int(position/0.01),envelope.size()-1)]*gain,0.0,1.0)
        elapsed+=delta
    level=lerp(level,raw_level,1.0-exp(-max(delta,0.0)/(0.035 if raw_level>level else 0.09)))
    # Hysteresis stops rapid swaps around the boundaries.
    if level<0.045:mouth="REST"
    elif level>0.66:mouth="A"
    elif level>0.30 and mouth!="A":mouth="E"
    elif mouth=="A" and level<0.55:mouth="E"
    elif mouth=="E" and level<0.23:mouth="I"
    elif mouth=="REST" and level>0.075:mouth="I"
    return mouth
