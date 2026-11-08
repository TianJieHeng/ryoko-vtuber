#!/usr/bin/env python3
"""Brow-only D repair. No edits to project or shared eye builder.
Solve one harmonic skin field over an expanded neighborhood, preserving shaded
warm-skin anchors. Paint only full brow ownership minus explicit foreground hair.
"""
from pathlib import Path
import json,hashlib,argparse
import numpy as np
from PIL import Image,ImageDraw
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.ndimage import distance_transform_edt
PROJECT=Path(__file__).resolve().parents[1]
P=PROJECT/'rig_assets/canonical_brows';P.mkdir(parents=True,exist_ok=True)
SRC=PROJECT/'artwork/bust_base.png'
EYES=PROJECT/'rig_assets/canonical_eyes';HAIR=PROJECT/'rig_assets/canonical_hair/full_hair_exclusion_mask.png'
CONFIG={'screen_left':(460,442,540,479),'screen_right':(601,440,658,474)}

def reconstruct_brow_skin(source_rgba,full_ownership,foreground_hair,box,side,margin=24):
    """Drop-in function. Returns local uint8 RGB, effective ownership, guard mask.
    full_ownership is the existing full-canvas corrected brow feature mask.
    foreground_hair is full-canvas original hair exclusion/ownership.
    A fixed geometric guard reinstates the thin foreground strand at brow roots.
    No RGB threshold excludes shaded warm skin; r>70 only rejects near-black ink.
    """
    H,W=source_rgba.shape[:2];x0,y0,x1,y1=box
    ax=max(0,x0-margin);ay=max(0,y0-margin);bx=min(W,x1+margin);by=min(H,y1+margin)
    Y,X=np.mgrid[ay:by,ax:bx];rgb=source_rgba[ay:by,ax:bx,:3].astype(float)
    hair=foreground_hair[ay:by,ax:bx].astype(bool).copy()
    near=(Y>=y0-5)&(Y<y1+5)
    if side=='screen_left':root_guard=near&(X<464)&(X>=452)
    else:root_guard=near&(X>=631+0.8*(Y-430))&(X<675)
    hair|=root_guard
    owned=full_ownership[ay:by,ax:bx].astype(bool)&~hair
    warm=(rgb[:,:,0]>rgb[:,:,1]+12)&(rgb[:,:,0]>rgb[:,:,2]+20)&(rgb[:,:,0]>70)
    known=warm&~hair&~full_ownership[ay:by,ax:bx].astype(bool)
    unknown=~known
    ids=np.full(unknown.shape,-1,int);ids[unknown]=np.arange(unknown.sum())
    ys,xs=np.where(unknown);N=len(ys);A=lil_matrix((N,N),dtype=float);rhs=np.zeros((N,3))
    h,w=unknown.shape
    for i,(y,x) in enumerate(zip(ys,xs)):
        degree=0
        for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
            ny,nx=y+dy,x+dx
            if not(0<=ny<h and 0<=nx<w):continue
            degree+=1
            if unknown[ny,nx]:A[i,ids[ny,nx]]=-1
            else:rhs[i]+=rgb[ny,nx]
        A[i,i]=degree
    solved=rgb.copy();solved[unknown]=spsolve(A.tocsr(),rhs)
    local=np.s_[y0-ay:y1-ay,x0-ax:x1-ax]
    return np.clip(np.rint(solved[local]),0,255).astype('uint8'),owned[local],root_guard[local],known[local]

def matte_exact(source,bg,mask):
    sf=source.astype(float);bf=bg.astype(float)
    core=mask&(sf[:,:,0]-sf[:,:,1]<15)
    ink=np.median(sf[core],axis=0)
    alpha=np.clip(np.max((bf-sf)/np.maximum(bf-ink,1),axis=2),0,1)
    alpha=np.maximum(alpha,np.clip(np.max((sf-bf)/np.maximum(255-bf,1),axis=2),0,1))
    a=np.rint(alpha*255).astype(int);a[core]=255;a[~mask]=0
    needs=mask&np.any(source!=bg,axis=2);a[needs]=np.maximum(a[needs],1)
    fg=np.zeros_like(source)
    for _ in range(256):
        aa=a[:,:,None]/255
        raw=np.rint((sf-bf*(1-aa))/np.maximum(aa,1/255))
        fg=np.clip(raw,0,255).astype('uint8')
        composed=np.rint(fg*aa+bf*(1-aa)).astype('uint8')
        bad=mask&np.any(composed!=source,axis=2)&(a<255)
        if not bad.any():break
        a[bad]+=1
    # Zero-alpha texels borrow nearest real foreground, preventing GPU green/skin bleed.
    valid=a>25
    if valid.any():
        idx=distance_transform_edt(~valid,return_distances=False,return_indices=True);zero=a==0
        fg[zero]=fg[idx[0][zero],idx[1][zero]]
    return np.dstack((fg,a.astype('uint8'))),core

def main():
    global P,SRC,EYES,HAIR
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=SRC)
    parser.add_argument('--hair-mask',type=Path,default=HAIR)
    parser.add_argument('--eyes-dir',type=Path,default=EYES,help='Directory containing corrected full brow ownership masks.')
    parser.add_argument('--output-dir',type=Path,default=P)
    args=parser.parse_args();SRC=args.source;HAIR=args.hair_mask;EYES=args.eyes_dir;P=args.output_dir;P.mkdir(parents=True,exist_ok=True)
    src=np.array(Image.open(SRC).convert('RGBA'));H,W=src.shape[:2]
    hair=np.array(Image.open(HAIR).convert('L'))>0
    base=Image.fromarray(src);neutral=base.copy();hidden=base.copy()
    owned_full=np.zeros((H,W),bool);guard_full=np.zeros((H,W),bool)
    report={'source':'artwork/bust_base.png','source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'method':'Expanded-neighborhood sparse harmonic solve with shaded warm skin anchors; no uniform pale seed. Existing corrected brow ownership preserved separately; rendered/cleared ownership excludes explicit foreground hair guard.','objects':{},'stats':{}}
    data={}
    for side,box in CONFIG.items():
        x0,y0,x1,y1=box;localmask=np.array(Image.open(EYES/f'brow_{side}_ownership_mask.png').convert('L'))>0
        full=np.zeros((H,W),bool);full[y0:y1,x0:x1]=localmask
        skin,effective,guard,known=reconstruct_brow_skin(src,full,hair,box,side)
        raw=src[y0:y1,x0:x1,:3]
        brow,core=matte_exact(raw,skin,effective)
        sk=np.dstack((skin,(effective*255).astype('uint8')))
        Image.fromarray(brow).save(P/f'brow_{side}.png');Image.fromarray(sk).save(P/f'brow_skin_{side}.png')
        transfer=guard&localmask&~hair[y0:y1,x0:x1]
        Image.fromarray(np.dstack((raw,(transfer*255).astype('uint8')))).save(P/f'brow_root_hair_{side}.png')
        Image.fromarray(np.dstack((skin,(transfer*255).astype('uint8')))).save(P/f'brow_root_hair_backing_{side}.png')
        for name,mask in [('full_feature_ownership',localmask),('effective_ownership',effective),('foreground_hair_guard',guard&localmask),('inferred_matte',effective&~core),('warm_skin_anchors',known)]:
            Image.fromarray((mask*255).astype('uint8')).save(P/f'brow_{side}_{name}.png')
        owned_full[y0:y1,x0:x1]|=effective;guard_full[y0:y1,x0:x1]|=guard&localmask
        hidden.alpha_composite(Image.fromarray(sk),(x0,y0))
        data[side]=(box,brow,sk)
        report['objects'][side]={'brow':f'brow_{side}.png','skin':f'brow_skin_{side}.png','xy':[x0,y0],'size':[x1-x0,y1-y0],'pivot':[(x0+x1)/2,(y0+y1)/2],'full_feature_ownership':f'brow_{side}_full_feature_ownership.png','effective_ownership':f'brow_{side}_effective_ownership.png','foreground_hair_guard':f'brow_{side}_foreground_hair_guard.png'}
        report['objects'][side]['ownership_transfer']={'hair_asset':f'brow_root_hair_{side}.png','stationary_backing_fill':f'brow_root_hair_backing_{side}.png','owner':'front_fringe','owner_pivot':[529,218],'suggested_z':90,'pixels':int(transfer.sum()),'rule':'Remove these original pixels from brow ownership and stationary raw backing. Paint provided stationary skin fill underneath, then draw original source RGBA hair companion above brows with the same rigid transform/visibility as front_fringe. Do not leave these pixels transparent or unowned.'}
        report['stats'][side]={'full_feature_pixels':int(localmask.sum()),'cleared_brow_pixels':int(effective.sum()),'foreground_hair_pixels_excluded':int((guard&localmask).sum()),'skin_min_rgb':skin[effective].min(0).tolist(),'skin_max_rgb':skin[effective].max(0).tolist()}
    neutral=hidden.copy();raised=hidden.copy()
    for side,(box,brow,sk) in data.items():
        x0,y0,x1,y1=box;neutral.alpha_composite(Image.fromarray(brow),(x0,y0));raised.alpha_composite(Image.fromarray(brow),(x0,y0-10))
    # Static foreground source restores its own pixels above raised brows. The
    # newly explicit guard stays source-owned; no tan fill is painted through it.
    guards=hair|guard_full
    for im in [neutral,raised]:
        ar=np.array(im);ar[guards]=src[guards];im.paste(Image.fromarray(ar))
    diff=np.abs(np.array(neutral).astype(int)-src.astype(int))
    report['neutral_validation']={'changed_pixels':int(np.any(diff,axis=2).sum()),'maximum_channel_error':int(diff.max()),'skin_changes_outside_effective_ownership':int(np.any(np.array(hidden)!=src,axis=2)[~owned_full].sum()),'painted_skin_hair_overlap':int((owned_full&hair).sum())}
    for name,im in [('neutral',neutral),('hidden',hidden),('raised',raised)]:im.save(P/f'brow_d_{name}.png')
    Image.fromarray((owned_full*255).astype('uint8')).save(P/'brow_removal_mask.png');Image.fromarray((guard_full*255).astype('uint8')).save(P/'foreground_hair_guard_additions.png')
    sheet=Image.new('RGB',(1050,600),'#dddddd');draw=ImageDraw.Draw(sheet)
    for i,(name,im) in enumerate([('canonical',Image.fromarray(src)),('D hidden (hair protected)',hidden),('D raised10px (foreground hair restored)',raised),('D neutral recompose',neutral)]):
        sheet.paste(im.crop((400,430,750,473)).resize((1050,129)),(0,i*150+21));draw.text((5,i*150+4),name,fill='black')
    sheet.save(P/'brow_d_comparison_3x.png')
    (P/'manifest.json').write_text(json.dumps(report,indent=2));print(json.dumps(report['neutral_validation']))
if __name__=='__main__':main()
