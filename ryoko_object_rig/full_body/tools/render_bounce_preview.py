#!/usr/bin/env python3
"""Rasterize the actual sampled Godot spring-driven mesh triangles.

This is CPU video, NOT a native Godot capture. No spring curve or deform is
invented here: UVs, triangles, per-frame vertices, and global matrices come
from tests/sample_bounce.gd. The diagnostic head uses neutral source artwork.
"""
import argparse
import json
import math
import subprocess
from pathlib import Path
import numpy as np
from scipy.ndimage import map_coordinates
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'full_body'
OUT = BASE / 'review'

def matrix(values):
    a,b,c,d,x,y = values
    return np.array([[a,c,x],[b,d,y],[0,0,1]], dtype=float)

def place(canvas, source, values):
    m = matrix(values)
    points = m @ np.array([[0,0,1],[source.width,0,1],[0,source.height,1],[source.width,source.height,1]]).T
    left,top = np.floor(points[:2].min(axis=1)).astype(int)-1
    right,bottom = np.ceil(points[:2].max(axis=1)).astype(int)+1
    inv = np.linalg.inv(m) @ np.array([[1,0,left],[0,1,top],[0,0,1]])
    part = source.transform((right-left,bottom-top), Image.Transform.AFFINE, tuple(inv[:2].flatten()), Image.Resampling.BICUBIC)
    canvas.alpha_composite(part,(left,top))

def place_mesh(canvas, source, spec, vertices, values):
    local = np.array(vertices, dtype=np.float64)
    points = (matrix(values) @ np.column_stack([local,np.ones(len(local))]).T).T[:,:2]
    left,top = np.floor(points.min(axis=0)).astype(int)-1
    right,bottom = np.ceil(points.max(axis=0)).astype(int)+1
    width,height = right-left,bottom-top
    maps = np.full((2,height,width), -100., dtype=np.float32)
    uv = np.array(spec['uv'],dtype=np.float64)
    for indices in spec['triangles']:
        tri = points[indices]-[left,top]
        lo = np.maximum(np.floor(tri.min(axis=0)).astype(int),[0,0])
        hi = np.minimum(np.ceil(tri.max(axis=0)).astype(int),[width-1,height-1])
        if np.any(hi<lo): continue
        xx,yy = np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5)
        ab = np.column_stack([tri[1]-tri[0],tri[2]-tri[0]])
        if abs(np.linalg.det(ab))<1e-9:continue
        bary = np.linalg.inv(ab) @ np.array([xx.ravel()-tri[0,0], yy.ravel()-tri[0,1]])
        inside = (bary[0]>=-1e-5)&(bary[1]>=-1e-5)&(bary.sum(axis=0)<=1.00001)
        mapped = uv[indices[0]][:,None] + (uv[indices[1]]-uv[indices[0]])[:,None]*bary[0] + (uv[indices[2]]-uv[indices[0]])[:,None]*bary[1]
        region = maps[:,lo[1]:hi[1]+1,lo[0]:hi[0]+1]
        for channel in range(2):
            patch = region[channel].copy().reshape(-1)
            patch[inside] = mapped[1-channel,inside]-.5
            region[channel] = patch.reshape(xx.shape)
    # Premultiplied-alpha bilinear sampling avoids dark fringes on cutout edges.
    rendered = np.stack([map_coordinates(source[:,:,c],maps,order=1,mode='constant',cval=0,prefilter=False) for c in range(4)],axis=-1)
    rendered[:,:,:3] = np.divide(rendered[:,:,:3],rendered[:,:,3:4],out=np.zeros_like(rendered[:,:,:3]),where=rendered[:,:,3:4]>1e-5)
    part = Image.fromarray(np.uint8(np.clip(rendered*255,0,255)), 'RGBA')
    canvas.alpha_composite(part,(int(left),int(top)))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--still-frame',type=int)
    parser.add_argument('--samples',default='bounce_samples.json')
    args=parser.parse_args()
    manifest=json.loads((BASE/'registration.json').read_text())
    samples=json.loads((OUT/args.samples).read_text())
    assets={e['id']:Image.open(ROOT/e['file'][6:]).convert('RGBA') for e in manifest['layers']}
    mesh_textures={}
    for id in samples['meshes']:
        texture=np.asarray(assets[id],dtype=np.float32)/255.
        texture[:,:,:3]*=texture[:,:,3:4]
        mesh_textures[id]=texture
    head=Image.open(BASE/'pieces_v2/head_audit/neutral_head_complete.png').convert('RGBA')
    title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
    small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
    movie=OUT/'ryoko_small_bounce_jiggle_v1.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x960','-r',str(samples['fps']),'-i','-','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)]
    process=None if args.still_frame is not None else subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i,frame in enumerate(samples['frames']):
        if args.still_frame is not None and i!=args.still_frame:continue
        canvas=Image.new('RGBA',tuple(manifest['canvas']),(237,235,229,255))
        for e in sorted(manifest['layers'],key=lambda e:e['z']):
            id=e['id']
            if id in samples['meshes']:
                place_mesh(canvas,mesh_textures[id],samples['meshes'][id],frame['mesh_vertices'][id],frame['layers'][id])
            else:place(canvas,assets[id],frame['layers'][id])
        place(canvas,head,frame['head'])
        result=Image.new('RGB',(1280,960),(25,31,37))
        result.paste(canvas.convert('RGB').resize((568,852),Image.Resampling.LANCZOS),(24,76))
        result.paste(canvas.convert('RGB').crop((290,35,740,665)).resize((594,832),Image.Resampling.LANCZOS),(654,96))
        d=ImageDraw.Draw(result)
        d.text((24,14),'Ryoko / small bounce + spring jiggle / REVIEW',font=title,fill=(242,241,233))
        d.text((24,43),frame['phase'],font=small,fill=(132,224,203))
        d.text((654,76),'Same frame / chest and necklace detail',font=small,fill=(242,241,233))
        d.text((24,935),'Actual Godot spring simulation + mesh vertices. CPU-rendered preview, not native capture. Neutral face.',font=small,fill=(216,218,220))
        if process is None:
            path=OUT/f'bounce_frame_{i:04}.jpg';result.save(path,quality=95);print(path);return
        process.stdin.write(result.tobytes())
        if i in (0,33,39,82,88,240):result.save(OUT/f'bounce_frame_{i:04}.jpg',quality=94)
        if i%30==0:print(f'{i}/{len(samples["frames"])}',flush=True)
    process.stdin.close()
    if process.wait():raise SystemExit('FFmpeg encoding failed')
    print(movie)

if __name__=='__main__':main()
