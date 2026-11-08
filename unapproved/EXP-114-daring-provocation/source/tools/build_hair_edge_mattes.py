"""Bounded estimated edge decontamination in eye-overlap bands only.
Canonical binary source recuts remain available as exact provenance references.
Runtime rendered_asset variants replace only contaminated strand-edge RGBA.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy import ndimage as ndi
PROJECT=Path(__file__).resolve().parents[1];P=PROJECT/'rig_assets/canonical_hair';m=json.loads((P/'manifest.json').read_text());a=np.array(Image.open(PROJECT/m['source']).convert('RGBA'));h,w=a.shape[:2];y,x=np.mgrid[:h,:w];r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
zone=(((x>=417)&(x<=475))|((x>=690)&(x<=718)))&(y>=463)&(y<=501)
back=np.array(Image.open(P/'canonical_clean_backing.png')).astype(float)
# Local skin chroma reference, bounded to plausible peach; absent hidden
# source anatomy is not used as a color sample.
bg_delta=np.clip(back[:,:,1]-back[:,:,0],-65,-28)
union=np.zeros((h,w),bool);changed=np.zeros((h,w),bool)
relative_a_changed=np.zeros((h,w),bool)
restore_hair=np.array(Image.open(PROJECT/'canonical_sources/ownership_corrections/restore_visible_hair.png'))>0
for name,e in m['layers'].items():
 im=np.array(Image.open(P/e['asset']));owned=im[:,:,3]>0
 # Reproduce Candidate A algorithm directly from immutable canonical recuts;
 # no dependency on saved candidate PNGs or any prior execution output.
 if not name.startswith('gold_'):
  acore=owned&(g-r>=8)&(g-b>=3)&(g>=65)
  adist,aidx=ndi.distance_transform_edt(~acore,return_indices=True)
  azone=(((x>=417)&(x<=474))|((x>=654)&(x<=709)))&(y>=473)&(y<=501)
  aestimate=azone&owned&((ndi.distance_transform_edt(owned)<=3)|(g-r<8)|(g<65))
  aa=np.clip((2.5-adist)/2,0,1)
  im[aestimate,:3]=a[aidx[0][aestimate],aidx[1][aestimate],:3]
  im[aestimate,3]=(aa[aestimate]*255+.5).astype('uint8')
  union|=aestimate
 baseline_a=im.copy()
 if not name.startswith('gold_'):
  core=owned&(g-r>=5)&(g-b>=2)&(g>=55)
  dist,idx=ndi.distance_transform_edt(~core,return_indices=True)
  near_skin=ndi.distance_transform_edt(~((r-g>22)&(r-b>35)&(a[:,:,3]>0)))<=9
  eye_overlap=(((x>=405)&(x<=475))|((x>=654)&(x<=719)))&(y>=469)&(y<=501)
  estimate=zone&owned&((r-g>3)|((g<45)&(r<45)&eye_overlap))
  fdelta=g[idx[0],idx[1]]-r[idx[0],idx[1]]
  chroma_alpha=np.clip(((g-r)-bg_delta)/np.maximum(fdelta-bg_delta,1),0,1)
  alpha=np.minimum(np.clip((2.5-dist)/1.5,0,1),chroma_alpha)
  # Open-lash black fragments are not foreground hair outlines. Their dark
  # background is reconstructed independently by the eye object's underlay.
  alpha[(y>=469)&(y<=501)&(g<45)&(r<45)]=0
  alpha=ndi.gaussian_filter(alpha,sigma=.45)
  alpha[core]=1
  # Source true green remains unchanged; uncertain edge RGB is unpolluted
  # nearest own-strand source color, never skin blurred over hair.
  im[estimate,:3]=a[idx[0][estimate],idx[1][estimate],:3]
  im[estimate,3]=(alpha[estimate]*255+.5).astype('uint8')
  im[restore_hair&owned]=a[restore_hair&owned]
  changed|=np.any(im!=np.array(Image.open(P/e['asset'])),axis=2);union|=estimate
  relative_a_changed|=np.any(im!=baseline_a,axis=2)
 Image.fromarray(im).save(P/f'{name}_matted.png');Image.fromarray(im).crop(e['bounds']).save(P/f'{name}_matted_crop.png')
 e['rendered_asset']=f'{name}_matted_crop.png';e['rendered_full_asset']=f'{name}_matted.png'
 if 'hidden_underlap' in e:
  under=np.array(Image.open(P/f'{name}_underlap.png'));under[union]=0
  Image.fromarray(under).save(P/f'{name}_underlap_matted.png')
  ue=e['hidden_underlap'];orig=Image.open(P/ue['asset']);ox,oy=ue['crop_origin'];box=(ox,oy,ox+orig.width,oy+orig.height)
  Image.fromarray(under).crop(box).save(P/f'{name}_underlap_matted_crop.png')
  ue['rendered_asset']=f'{name}_underlap_matted_crop.png';ue['rendered_full_asset']=f'{name}_underlap_matted.png'
# All estimated masks are now known; clear only those masks in seam guards.
for name,e in m['layers'].items():
 if 'hidden_underlap' in e:
  under=np.array(Image.open(P/f'{name}_underlap.png'));under[union]=0
  Image.fromarray(under).save(P/f'{name}_underlap_matted.png')
  ue=e['hidden_underlap'];orig=Image.open(P/ue['asset']);ox,oy=ue['crop_origin']
  Image.fromarray(under).crop((ox,oy,ox+orig.width,oy+orig.height)).save(P/ue['rendered_asset'])
# Registered canonical closed artwork reveals short hair intervals hidden by
# the original open lash. Transfer only its green contour pixels to the nearest
# existing foreground hair owner, never to a moving lid or a skin patch.
ref=Image.fromarray(a.copy())
for file,xy in [('blink_R.png',(395,450)),('blink_L.png',(585,450))]:
 ref.alpha_composite(Image.open(PROJECT/'artwork'/file).convert('RGBA'),xy)
ref=np.array(ref);rr,gg,bb=ref[:,:,:3].astype(int).transpose(2,0,1)
original_hair=np.array(Image.open(P/'full_hair_exclusion_mask.png'))>0
reference_zone=(((x>=410)&(x<=475)&(y>=469)&(y<=505))|((x>=660)&(x<=725)&(y>=468)&(y<=505)))
continuation=reference_zone&~original_hair&(gg>rr+2)&(gg>bb+1)&(gg>45)
hair_names=[n for n in m['layers'] if not n.startswith('gold_')]
distances=[]
for name in hair_names:
 original=np.array(Image.open(P/m['layers'][name]['asset']))
 green=(original[:,:,3]>0)&(g>r+1)&(g>b+1)&(g>30)
 distances.append(ndi.distance_transform_edt(~green))
nearest=np.argmin(distances,axis=0)
# Recut the short contaminated crossings from the original registered closed
# art. Its complete contour, including AA against skin, exists at the same
# native coordinates. Do not combine alternating open/closed contour pixels.
core=reference_zone&(gg>rr+2)&(gg>bb+1)&(gg>35)
distance,core_idx=ndi.distance_transform_edt(~core,return_indices=True)
support=reference_zone&(distance<=1.5)
# The registered blink patch also repaints thick outer locks; those are not
# missing intervals. Keep their neutral source ownership exactly unchanged.
bulk=ndi.distance_transform_edt(core)>2.5
thin=ndi.distance_transform_edt(~bulk)>3.5
support &= thin
patch_band=reference_zone&thin
known_skin=(rr>gg+20)&(rr>bb+30)&(rr>170)&(gg>110)&~support
_,skin_idx=ndi.distance_transform_edt(~known_skin,return_indices=True)
background=ref[skin_idx[0],skin_idx[1],:3].astype(float)
for ch in range(3):background[:,:,ch]=ndi.gaussian_filter(background[:,:,ch],sigma=1.5)
foreground=ref[core_idx[0],core_idx[1],:3].astype(float)
fdelta=foreground[:,:,1]-foreground[:,:,0];bdelta=background[:,:,1]-background[:,:,0]
ref_alpha=np.clip(((gg-rr)-bdelta)/np.maximum(fdelta-bdelta,1),0,1)*support
ref_alpha[core]=1
ref_alpha=np.rint(ref_alpha*255)/255
ref_rgb=np.clip(np.rint((ref[:,:,:3]-background*(1-ref_alpha[:,:,None]))/np.maximum(ref_alpha[:,:,None],1/255)),0,255).astype('uint8')
ref_rgb[core]=ref[core,:3]
# Stable source-color padding, not skin RGB beneath transparent borders.
ref_rgb[~support]=foreground[~support].astype('uint8')
for i,name in enumerate(hair_names):
 e=m['layers'][name]
 im=np.array(Image.open(P/e['rendered_full_asset']))
 old=np.array(Image.open(P/e['asset']))[:,:,3]>0
 patch=patch_band&(old|support)
 im[patch]=0
 take=support&(nearest==i)
 im[take,:3]=ref_rgb[take];im[take,3]=(ref_alpha[take]*255).astype('uint8')
 Image.fromarray(im).save(P/e['rendered_full_asset'])
 Image.fromarray(im).crop(e['bounds']).save(P/e['rendered_asset'])
union|=patch_band&(original_hair|support)
Image.fromarray((support*255).astype('uint8')).save(P/'registered_closed_hair_crossing_matte.png')
union|=continuation
Image.fromarray((continuation*255).astype('uint8')).save(P/'registered_closed_hair_continuation_mask.png')
m['reference_continuations']={'pixels':int(continuation.sum()),'mask':'registered_closed_hair_continuation_mask.png','source':'artwork/blink_R.png at (395,450), artwork/blink_L.png at (585,450)','method':'Original registered closed-source green contour pixels, nearest existing foreground hair owner and its same rigid pivot. Native coordinates, no resize. This corrects the old open-lash occlusion at tiny strand crossings.'}

# The final crossing ownership is now known. Internal seam padding cannot
# remain visible where the foreground recut has deliberately exposed skin.
for name,e in m['layers'].items():
 if 'hidden_underlap' in e:
  u=e['hidden_underlap'];under=np.array(Image.open(P/u['rendered_full_asset']))
  under[union]=0
  Image.fromarray(under).save(P/u['rendered_full_asset'])
  ox,oy=u['crop_origin'];orig=Image.open(P/u['asset'])
  Image.fromarray(under).crop((ox,oy,ox+orig.width,oy+orig.height)).save(P/u['rendered_asset'])

combined=Image.new('RGBA',(w,h))
for e in m['layers'].values(): combined.alpha_composite(Image.open(P/e['rendered_full_asset']))
combined.save(P/'canonical_hair_matted_composite.png')
# A source-opaque skin/strand boundary must never become an ownership hole.
# Recover the stationary backing required beneath the exported hair matte:
# source = foreground * alpha + backing * (1 - alpha). This is bounded to
# otherwise uncovered original opaque texels and does not move or fade skin.
stack=Image.new('RGBA',(w,h))
for e in m['layers'].values():
 if 'hidden_underlap' in e:
  stack.alpha_composite(Image.open(P/e['hidden_underlap']['rendered_full_asset']))
for e in m['layers'].values():stack.alpha_composite(Image.open(P/e['rendered_full_asset']))
fg=np.array(stack).astype(float);background=np.array(Image.open(P/'canonical_clean_backing.png'))
opaque_source=(a[:,:,3]==255)
coverage_hole=opaque_source&(background[:,:,3]<255)&(fg[:,:,3]<255)
alpha=fg[:,:,3:4]/255
recovered=np.clip(np.rint((a[:,:,:3]-fg[:,:,:3]*alpha)/np.maximum(1-alpha,1/255)),0,255).astype('uint8')
background[coverage_hole,:3]=recovered[coverage_hole];background[coverage_hole,3]=255
Image.fromarray(background).save(P/'canonical_clean_backing.png')
Image.fromarray((coverage_hole*255).astype('uint8')).save(P/'recovered_opaque_backing_mask.png')
m['opaque_backing_recovery']={'pixels':int(coverage_hole.sum()),'mask':'recovered_opaque_backing_mask.png','method':'Stationary inverse source-over reconstruction only where original source was opaque and hair matte otherwise exposed an unowned boundary. Source RGB used as equality target; no moving skin.'}

union|=restore_hair
Image.fromarray((union*255).astype('uint8')).save(P/'estimated_hair_matte_mask.png')
assert not np.any(relative_a_changed&~(zone|restore_hair)), 'Mutation outside bounded Candidate A correction'
Image.fromarray((relative_a_changed*255).astype('uint8')).save(P/'candidate_a_correction_mask.png')
final_changed=np.zeros((h,w),bool)
for e in m['layers'].values():
 final_changed|=np.any(np.array(Image.open(P/e['rendered_full_asset']))!=np.array(Image.open(P/e['asset'])),axis=2)
m['edge_matte']={'script':'build_hair_edge_mattes.py','mask':'estimated_hair_matte_mask.png','visible_source_rgba_changed_pixels':int(final_changed.sum()),'estimated_mask_pixels':int(union.sum()),'native_source_registration':True,'provenance':'Bounded original-source edge mattes, registered closed-source thin-strand recuts in the eye crossings, valid-green hidden seam padding and stationary source-over backing recovery. Exact raw source recuts remain provenance references; rendered derivatives are not claimed pixel-identical original art.','neutral_exactness':'Only raw source recomposition is exact. Runtime crossing mattes and separately documented brow/hair continuations are bounded reconstructions.'}
m['reference_continuations']['method']='Registered canonical closed-source green hair contours and inferred alpha edges in the short eye-crossing intervals. Thick outer locks retain the neutral source. The pixels belong to the nearest existing hair owner and its original pivot. No animated image warp or width change.'

(P/'manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps(m['edge_matte'],indent=2))
