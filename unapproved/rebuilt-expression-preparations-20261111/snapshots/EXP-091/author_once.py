"""Author a NEW reconstruction. Exclusive outputs; never mutate prior freezes."""
import hashlib
import json
from pathlib import Path
W = Path(__file__).resolve().parent

def pose(b=0, tilt=0, inner=0, blink=0, eyes=0, mouth=0, purse=0,
         press=0, corner=0, smile=0, blush=0):
    return dict(brow_screen_left=b, brow_screen_right=b,
                brow_tilt_screen_left=tilt, brow_tilt_screen_right=-tilt,
                brow_inner_lift_screen_left=inner, brow_inner_lift_screen_right=inner,
                blink_L=blink, blink_R=blink, eye_smile_L=eyes, eye_smile_R=eyes,
                mouth_open=mouth, mouth_purse=purse, mouth_lip_press=press,
                mouth_corner_lift=corner, mouth_smile=smile, blush_intensity=blush)

def build():
    anchors = [
        ('neutral', {}),
        ('taste_intake', pose(b=.06, tilt=-.10, inner=.06, mouth=.07, purse=.06)),
        ('sweet_recognition', pose(b=-.05, tilt=.15, inner=.16, blink=.12, eyes=.10,
                                  purse=.35, press=.40, corner=.20, smile=.04, blush=.40)),
        ('squeeze_build', pose(b=-.08, tilt=.25, inner=.25, blink=.32, eyes=.30,
                             purse=.65, press=.65, corner=.42, smile=.10, blush=.75)),
        ('sweet_overload', pose(b=-.08, tilt=.30, inner=.40, eyes=1.0,
                              purse=.78, press=.70, corner=.55, smile=.12, blush=.92)),
        ('overload_hold', pose(b=-.08, tilt=.30, inner=.40, eyes=1.0,
                             purse=.78, press=.70, corner=.55, smile=.12, blush=.92)),
        ('reopen_residual', pose(b=-.04, tilt=.15, inner=.18, blink=.18, eyes=.17,
                               purse=.40, press=.40, corner=.24, smile=.03, blush=.45)),
        ('settle', pose(b=-.01, tilt=.02, inner=.03, blink=.03,
                       purse=.10, press=.10, corner=.04, blush=.08)),
        ('neutral_return', {}),
    ]
    times = [(0, 0), (.2, 0), (.55, 1), (.9, 2), (1.25, 3), (1.65, 4),
             (2.25, 5), (2.75, 6), (3.3, 7), (3.75, 8), (4.0, 8)]
    entry = json.loads((W/'SOURCE_CATALOGUE_ENTRY.json').read_text())
    profile = dict(id='EXP-091', title='Overly Sweet Taste', duration=4.0,
        status='UNAPPROVED new reconstruction 20261111 r1; static numeric checks only; native review pending',
        intent=entry['distinctive_facial_intent'],
        scope='Unmodified approved39 shared rig. Existing smile-eye, independent blush FX, rigid brows and sealed purse/pressure/corner controls. Brief .07 mouth opening at KP2 closes before the sweet overload. No cheek compression, new pucker anatomy, kiss part, independent width, gaze, speech, body or hair acting.',
        timing_origin='New four-second reconstruction from the visually inspected recovered EXP-091 nine-panel sheet. Not restored old v2 and not recovered animation. Catalogue 1.9-second proposal remains reference-only.',
        interpolation='Unchanged cubic smoothstep with .30-second restart and .45-second release. Eleven timeline keys, nine panel anchors. New in-memory preview only; production registry unchanged.',
        source_catalogue_sha256='ded1b313c36b66daf46f3426288ef4670b04703497323314754bba18e872b2bf',
        keyframes=[dict(time=t, phase=anchors[n][0], values=anchors[n][1]) for t,n in times])
    plan = [dict(name=n, pose=p, source_panel=i+1, time=[0,.55,.9,1.25,1.65,2.25,2.75,3.3,3.75][i])
            for i,(n,p) in enumerate(anchors)]
    mapping = dict(reconstruction='NEW 20261111 r1; not restored old v2', pixels_inspected=True,
        sheet_filename=Path(entry['asset_production']['actual_path']).name,
        sheet_sha256=entry['asset_production']['sha256'], dimensions=[1159,1358],
        observations=[
            'KP1 neutral. KP2 slightly parts the mouth with little eye change.',
            'KP3-4 add cheek blush, upper-face strain, narrowed eyes and a small sealed pucker.',
            'KP5-6 have fully closed curved lashes, strong blush, raised inner-brow strain and a tiny sealed smile-pucker.',
            'KP7 eyes reopen while brow strain and small pressed mouth remain. KP8 fades near neutral; KP9 neutral.',
        ],
        panel_to_anchor={str(i+1):n for i,(n,p) in enumerate(anchors)},
        input_files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((W/'reference').glob('*.png'))},
        mapping={
            'curved_closed_eyes':'eye_smile_L/R 1.0 closes effective lids and shapes the existing smile-eye joints; ordinary blink is zero at peak.',
            'brow_strain':'Inner lift .40 plus opposed legacy tilt .30/- .30 and vertical -.08; existing rigid owners only, no central wrinkles or contour deformation.',
            'small_sealed_smile_pucker':'Purse .78, pressure .70, shared corner .55, smile .12. Zero opening at peak. Endpoints narrow by 10.92 source pixels each. Lips are 49.16 source pixels wide across the sampled 71-pixel span, so tiny source shape remains an approximation.',
            'blush':'Existing separate cheek-only blush layer .92; no new cheek geometry or custom hatch texture.',
            'intake':'Brief .07 opening at .55 seconds; completely closed at .90 seconds and through the remainder.',
        },
        caveats=[
            'Pure Python numbers do not establish rendered anatomy, source fidelity, perceptual distinctness or smoothness.',
            'A generic bashful smile is a source-fit failure even if numerical distances pass.',
            'No cheek compression, 3D lip protrusion, new pucker anatomy, source-specific brow curve, or reference hatch-density reconstruction.',
            'Existing purse raises a risk of a broad or merely rounded mouth; native detail must judge its scale and sealed contour.',
        ],
        pending_comparator_gates={
            'EXP-197':'Do not read as kiss: no kiss part, no prolonged forward kiss and no asymmetric reopening.',
            'EXP-160':'Do not read as shy laugh: no open laugh/pulses, no broad warm smile, preserve strained sweet-overload grimace.',
            'EXP-090':'Do not read as queasy: curved fully closed smile-eyes and blush distinguish; not merely heavy ordinary lids with purse.',
            'EXP-096':'Do not read as headache: curved smile-eye geometry and blush; not ordinary closed lids with severe lowered opposed brows.',
        }, approval='UNAPPROVED; source art acceptance is not candidate approval')
    return {'EXP-091.json':profile, 'plan.json':plan, 'SOURCE_MAP.json':mapping}

if __name__ == '__main__':
    outputs=build()
    if any((W/n).exists() for n in outputs):
        raise SystemExit('Refusing overwrite: create a fresh reconstruction revision.')
    for n,obj in outputs.items():
        with (W/n).open('x') as f: f.write(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    print('Created fresh UNAPPROVED EXP-091 r1 data and source mapping.')
