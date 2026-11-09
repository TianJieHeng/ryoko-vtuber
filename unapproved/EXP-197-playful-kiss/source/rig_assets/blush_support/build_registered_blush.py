#!/usr/bin/env python3
"""Reproduce fixed original-source cheek FX. No rig edits or animation generation.

Dependencies: Pillow, NumPy, SciPy (exact tested versions are in the manifest).
Run from any directory: python /path/to/build_registered_blush.py
Use --rig-root to point to a read-only compatible no-blush rig snapshot.
All authoring mask/resampling work is static. Runtime scale stays (1,1).
"""
from __future__ import annotations
import argparse, hashlib, json, platform
from pathlib import Path
import numpy as np
import PIL
from PIL import Image, ImageDraw
import scipy
from scipy.ndimage import distance_transform_edt, label

HERE = Path(__file__).resolve().parent
CANVAS = (1136, 1384)
SOURCE_HASHES = {
    'R': 'a818395e9cf1be5023edc62f2d79b24bb3ee19efe634e35639b2770d53536081',
    'L': '12efc27caceed6475110b7e17bee91044dda15da21f9a453923abda25a64a824',
}
CONFIG = {
    'screen_left': {'side':'R', 'crop':[114,196,789,581], 'size':[148,84], 'xy':[407,519],
                    'polygon':[[433,530],[519,534],[536,555],[531,596],[453,609],[428,578]]},
    'screen_right': {'side':'L', 'crop':[301,196,982,584], 'size':[148,84], 'xy':[577,519],
                     'polygon':[[598,532],[694,532],[710,566],[687,603],[600,597],[585,561]]},
}
PEAK = .55
EXPECTED_FOREGROUND_DEPS = {'hair_temple_left_underlap': {'file': 'rig_assets/object_face/hair_temple_left_underlap.png', 'sha256': '2d311a71cc9c65bbe10ebbfa2b70e5b4d4cc668014cc929e86763395f4903f29', 'xy': [291, 273], 'z': 60}, 'hair_temple_right_underlap': {'file': 'rig_assets/object_face/hair_temple_right_underlap.png', 'sha256': '7771f59562ac1ad5ec148b02206d8217c2b8242b03368788001583ef3ac4897e', 'xy': [646, 364], 'z': 60}, 'hair_front_fringe_underlap': {'file': 'rig_assets/object_face/hair_front_fringe_underlap.png', 'sha256': '8919277a16fc3c184c4692b44ad3d8d1c30f526910aaf587adddf00059b6f423', 'xy': [287, 150], 'z': 60}, 'hair_temple_left': {'file': 'rig_assets/object_face/hair_temple_left.png', 'sha256': 'c22b273e545520520693a62c84b63121918e7e460f4ff70eda671f9424be2ac1', 'xy': [250, 281], 'z': 70}, 'hair_temple_right': {'file': 'rig_assets/object_face/hair_temple_right.png', 'sha256': 'e22a1a00a96f91c295fc00e4719fd363b22f3983263bf9f5e1b6bac069f92601', 'xy': [647, 371], 'z': 70}, 'hair_front_fringe': {'file': 'rig_assets/smile_support/hair_front_fringe_eye_reassigned.png', 'sha256': 'f54b05fb8b12ea37367ee3ccc48f1e4439ae379adf0ca259de9ee59e41e213ad', 'xy': [41, 55], 'z': 70}}

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def bbox(a):
    y,x=np.where(a>0)
    return None if len(x)==0 else [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
def save_rgba(a,path):
    a=np.asarray(a,dtype=np.uint8).copy();a[a[...,3]==0]=0
    Image.fromarray(a).save(path)
def write_json(p,v): p.write_text(json.dumps(v,indent=2)+'\n')

def build(rig_root:Path):
    here=HERE; objects={}; source_files={}; checks={}
    face_manifest=rig_root/'rig_assets/object_face/manifest.json'
    fm=json.loads(face_manifest.read_text())
    assert fm['canvas']==list(CANVAS), fm['canvas']
    # Fixed keep-out from unchanged hair, including skin-colored pixels owned by
    # foreground hair. Using their alpha avoids painting through those pixels.
    trans=np.ones((CANVAS[1],CANVAS[0]),dtype=np.float64)
    deps=[]
    for key,e in fm['objects'].items():
        if int(e.get('z',0))<60: continue
        x,y=map(int,e['xy']);w,h=map(int,e['size'])
        if x+w<=407 or x>=725 or y+h<=519 or y>=603: continue
        rel='rig_assets/object_face/'+e['file']
        if key=='hair_front_fringe':
            rel='rig_assets/smile_support/hair_front_fringe_eye_reassigned.png'
        path=rig_root/rel
        expected=EXPECTED_FOREGROUND_DEPS[key]
        assert rel==expected['file'] and [x,y]==expected['xy'] and e['z']==expected['z'], key
        assert sha(path)==expected['sha256'], f'Foreground input hash mismatch: {key}'
        arr=np.asarray(Image.open(path).convert('RGBA'))
        assert arr.shape[:2]==(h,w)
        trans[y:y+h,x:x+w]*=1-arr[...,3]/255.0
        deps.append({'object':key,'file':rel,'sha256':sha(path),'xy':[x,y], 'z':e['z']})
    assert set(d['object'] for d in deps)==set(EXPECTED_FOREGROUND_DEPS)
    # A >1.5% foreground coverage keep-out plus a 12px inward linear feather
    # prevents a visible rectangular/beige notch at baked hair/skin ownership.
    exposed=trans>.985
    occlusion=np.rint((1-trans)*255).astype(np.uint8)
    Image.fromarray(occlusion).save(here/'authoring_foreground_alpha.png')
    for screen,c in CONFIG.items():
        side=c['side'];src=here/'source_originals'/f'RYO_FX_blush_character_{side}.png'
        assert sha(src)==SOURCE_HASHES[side],str(src)
        im=Image.open(src).convert('RGBA'); original=np.asarray(im);clean=original.copy()
        low=(clean[...,3]>0)&(clean[...,3]<4)
        clean[clean[...,3]<4]=0
        assert im.size==(1086,724)
        assert bbox(clean[...,3])==c['crop']
        # Premultiplied-alpha Lanczos prevents transparent RGB from contaminating
        # edge color. Source RGB is not recolored, repainted, or multiplied.
        registered=Image.fromarray(clean).crop(c['crop']).convert('RGBa').resize(
            tuple(c['size']),Image.Resampling.LANCZOS).convert('RGBA')
        raw=np.asarray(registered).copy();raw[raw[...,3]==0]=0
        raw_path=here/f'blush_{screen}_registered_unmasked.png';save_rgba(raw,raw_path)
        poly=Image.new('L',CANVAS,0);ImageDraw.Draw(poly).polygon(c['polygon'],fill=255)
        support=(np.asarray(poly)>0)&exposed
        distance=distance_transform_edt(support)
        full_mask=np.clip(distance/12.0,0,1)
        x,y=c['xy'];w,h=c['size'];mask=full_mask[y:y+h,x:x+w]
        # Quantize the auditable separate mask first; the baked texture is exactly
        # reproducible from raw RGBA times this 8-bit mask.
        mask8=np.rint(mask*255).astype(np.uint8)
        mask_path=here/f'blush_{screen}_cheek_mask.png'
        final=raw.copy();final[...,3]=np.rint(raw[...,3].astype(float)*mask8/255).astype(np.uint8)
        components_map,component_count=label(final[...,3]>0)
        sizes=np.bincount(components_map.ravel());sizes[0]=0
        main_label=int(sizes.argmax())
        removed_island_pixels=int(np.count_nonzero((components_map>0)&(components_map!=main_label)))
        mask8[(components_map>0)&(components_map!=main_label)]=0
        final[...,3]=np.rint(raw[...,3].astype(float)*mask8/255).astype(np.uint8)
        Image.fromarray(mask8).save(mask_path)
        final[final[...,3]==0]=0
        tex_path=here/f'blush_{screen}.png';save_rgba(final,tex_path)
        active=final[...,3]>0
        assert np.all(~active | exposed[y:y+h,x:x+w])
        assert np.all((final[...,3]>0)<=(mask8>0))
        yy,xx=np.where(active);gx=xx+x;gy=yy+y
        assert gy.min()>=530 and gy.max()<610
        assert (gx.max()<538) if screen=='screen_left' else (gx.min()>583)
        _,components=label(active)
        checks[screen]={'active_pixels':int(active.sum()),'support_components':int(components),
                        'removed_disconnected_low_alpha_island_pixels':removed_island_pixels,
                        'alpha_support_native_xyxy':[int(gx.min()),int(gy.min()),int(gx.max()+1),int(gy.max()+1)],
                        'stray_alpha_outside_cheek_mask':0,'overlap_eye_region_y_below_530':0,
                        'overlap_nose_corridor_x_538_through_583':0,'overlap_mouth_or_neck_y_610_plus':0,
                        'overlap_foreground_coverage_above_1_5_percent':0,
                        'fully_transparent_rgb_zero':bool(np.all(final[~active]==0))}
        crop=c['crop'];cw=crop[2]-crop[0];ch=crop[3]-crop[1]
        objects[screen]={'file':tex_path.name,'xy':c['xy'],'size':c['size'],
           'pivot':[x+w/2,y+h/2],'local_pivot':[w/2,h/2],
           'centered':False,'z':29,'runtime_scale':[1,1],'runtime_rotation':0,
           'runtime_transform_policy':'fixed position, rotation, texture and local unit scale; intensity only',
           'anatomical_side': 'character_right' if side=='R' else 'character_left',
           'source':str(src.relative_to(here)),'source_sha256':SOURCE_HASHES[side],
           'source_dimensions':[1086,724],'source_alpha_nonzero_bbox':[0,0,1086,724],
           'source_atlas_crop_xyxy':[0,0,1086,724] if side=='R' else [1086,0,2172,724],
           'source_strokes':3,'no_mirror':True,'source_crop_xyxy':crop,
           'alpha_cleanup':{'rule':'clear entire RGBA where source alpha < 4',
                            'discarded_nonzero_alpha_pixels':int(low.sum()),
                            'maximum_discarded_alpha':3},
           'authoring_resample':{'filter':'Pillow LANCZOS in premultiplied RGBa, then RGBA',
                                 'input_crop_size':[cw,ch],'output_size':c['size'],
                                 'fixed_scale_xy':[w/cw,h/ch]},
           'mask':{'file':mask_path.name,'sha256':sha(mask_path),
                   'polygon_native_xy':c['polygon'],'inward_feather_pixels':12,
                   'operation':'polygon intersect fixed foreground transmittance > 0.985; EDT/12 clamped; round to 8-bit',
                   'retained_support':'largest connected alpha component; discarded tiny mask-edge islands',
                   'removed_disconnected_island_pixels':removed_island_pixels,
                   'baked_into_texture_alpha':True,'apply_again_at_runtime':False},
           'unmasked_registered_file':raw_path.name,'unmasked_registered_file_required_for_runtime':False,
           'unmasked_registered_file_role':'reproducible diagnostic only; may be omitted from shipment',
           'sha256':sha(tex_path),
           'alpha_max':int(final[...,3].max()),'texture_support_local_xyxy':bbox(final[...,3])}
        source_files[src.name]=sha(src)
    manifest={'schema_version':1,'status':'local EXP-006 source registration candidate; user approval pending',
       'canvas':list(CANVAS),'coordinate_convention':'native canvas, top-left origin, x right, y down; screen sides are viewer sides',
       'objects':objects,'recommended_peak_intensity':PEAK,'allowed_runtime_intensity_range':[0,1],
       'runtime_integration':'Two separate effect sprites; z29 above stationary face z20, below eyes z31 and hair z60-80. No base-object texture or geometry changes.',
       'source_originals_retained':source_files,'fixed_registration_inferred':True,
       'provenance':{'asset_manifest_status':'separated_part_requires_2d_registration; no authored anchors',
          'source_atlas':'effects/sources/RYO_FX_blush_source_v001.png',
          'source_atlas_sha256':'9cdfb66936a8f83f18c839ba1e1560f3f1a35462a8013325b3a835c2a62ecb21',
          'reference_sheet_sha256':'59a58716099bdd126e7ab4a106fdfb5ae9b75471e4d4bdd0b978997428e1a848',
          'reference_panel_size':[418,418],'registration_source':'visual fit against supplied exact EXP-006 sheet and immutable no-blush native keyposes',
          'foreground_mask_inputs':deps,
          'authoring_foreground_alpha':{'file':'authoring_foreground_alpha.png','sha256':sha(here/'authoring_foreground_alpha.png'),
             'role':'reproducible diagnostic; regenerated from exact listed foreground inputs',
             'required_for_runtime_or_rebuild':False}},
       'reference_observations':[
          {'keypose':'KP01','relative_intensity':0.0,'observation':'Neutral, no visible hatching.'},
          {'keypose':'KP02','relative_intensity':0.0,'observation':'Anticipation, no clearly visible hatching. Slight color difference alone is not evidence of a new FX requirement.'},
          {'keypose':'KP03','relative_intensity':0.0,'observation':'Onset, no clearly visible hatching; at most a very faint warm wash.'},
          {'keypose':'KP04','relative_intensity':0.65,'observation':'Clear lighter cheek hatching and warm wash.'},
          {'keypose':'KP05','relative_intensity':1.0,'observation':'Strongest clear hatching and cheek wash; use recommended peak scalar.'},
          {'keypose':'KP06','relative_intensity':0.35,'observation':'Leak is noticeably reduced; no clear individual hatch lines, faint warm wash remains.'},
          {'keypose':'KP07','relative_intensity':0.0,'observation':'Recovery has no clear hatching.'},
          {'keypose':'KP08','relative_intensity':0.0,'observation':'Release has no clear hatching.'},
          {'keypose':'KP09','relative_intensity':0.0,'observation':'Neutral return, no clear hatching.'}],
       'limitations':[
          'Original FX have three long diagonal strokes per cheek; exact reference has many finer hatch marks. This registration preserves original art rather than inventing matching hatching.',
          'Original FX wash is pinker than the reference peach/orange wash. No recoloring was performed.',
          'Positions and cheek masks are inferred authoring registration, not recovered rig anchors.',
          'Foreground-hair images include skin-colored pixels. The fixed inward mask avoids their visible notch without modifying hair or painting through it.',
          'Static mask assessed against zero hair sway, which EXP-006 uses. Runtime layering still occludes with moving foreground hair; other performances need their own visual review.',
          'Static reference observations are not recovered animation timings.'],
       'builder':{'file':'build_registered_blush.py','sha256':sha(Path(__file__)),
          'python':platform.python_version(),'pillow':PIL.__version__,'numpy':np.__version__,'scipy':scipy.__version__}}
    write_json(here/'manifest.json',manifest)
    write_json(here/'registration_checks.json',{'passed':True,'checks':checks,'source_hashes_verified':True,
        'no_source_rgb_recoloring':True,'no_rig_files_written':True})
    print(json.dumps({'output':str(here),'objects':{k:{'file':v['file'],'xy':v['xy']} for k,v in objects.items()},'checks':checks},indent=2))
    return manifest

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rig-root',type=Path,default=HERE.parents[1])
    args=ap.parse_args();build(args.rig_root.resolve())
