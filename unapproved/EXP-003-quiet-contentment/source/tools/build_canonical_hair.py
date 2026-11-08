"""Deterministic native-coordinate source recuts. No scaling or source mutation.
Unknown occluded head anatomy is not invented. Only a 40px skin guard under
foreground locks is reconstructed, from nearest visible local skin samples.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ndi
PROJECT=Path(__file__).resolve().parents[1]
ROOT=PROJECT/'rig_assets/canonical_hair';ROOT.mkdir(parents=True,exist_ok=True)
SRC=PROJECT/'artwork/bust_base.png'
a=np.array(Image.open(SRC).convert('RGBA'));h,w=a.shape[:2];yy,xx=np.mgrid[:h,:w];rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1)
def poly(points):
 im=Image.new('L',(w,h));ImageDraw.Draw(im).polygon(points,fill=255);return np.array(im)>0
# Protect canonical face/ears, full original neck, and outfit. The protected face
# contains foreground strands; these are assigned below by source pigment.
face=poly([(476,338),(558,337),(605,379),(654,428),(696,478),(730,530),(738,563),(727,594),(700,608),(675,649),(648,676),(647,743),(681,806),(700,850),(436,850),(451,808),(477,763),(480,677),(447,646),(420,610),(394,599),(378,580),(377,548),(407,491),(430,440),(447,389)])
body=poly([(0,1383),(0,890),(300,850),(386,797),(414,765),(448,737),(477,729),(479,675),(649,675),(650,731),(680,741),(709,778),(749,815),(870,860),(1135,900),(1135,1383)])
# Existing canonical hanging earrings are excluded from hair ownership.
earring=np.zeros((h,w),bool)
for box in [(397,574,424,737),(703,572,730,737)]:
 x0,y0,x1,y1=box; gold=(r-g>7)&(r-b>18)&(a[:,:,3]>0)
 local=gold[y0:y1,x0:x1];labs,n=ndi.label(local);sizes=np.bincount(labs.ravel());sizes[0]=0;seed=labs==sizes.argmax()
 earring[y0:y1,x0:x1]=ndi.distance_transform_edt(~seed)<=2
# Hairpins are exact source recuts, not green-hair objects.
pinregion=(yy<319)&(xx>641)&(xx<811)&(yy>86)
gold=(r-g>9)&(r-b>25)&pinregion&(a[:,:,3]>0)
pins=ndi.binary_dilation(gold,iterations=2)&pinregion
hair=((yy<805)&~face&~body&~earring&~pins)
# Visible lock pigments inside the skin envelope. One pixel guard owns AA edge.
chrom=(g-r>0)&(g-b>-1)&(yy<790)
browkeep=poly([(462,446),(481,449),(501,455),(519,464),(538,478),(517,474),(496,468),(477,462),(462,459)])|poly([(604,458),(618,451),(638,445),(650,443),(655,453),(639,460),(620,467),(604,473)])
strand=ndi.binary_dilation(chrom&face&~browkeep,iterations=3)&face&~browkeep&~earring
hair|=strand
# Capture lower hair tips crossing the collar/neck envelope as well.
extra=chrom&~browkeep&~pins
# True gold earrings stay separate; source green fringe does not.
earring&=~chrom
hair|=extra
hair&=~pins&~earring
# Mask includes all source alpha, and keeps transparent RGB assigned nowhere.
hair&=a[:,:,3]>0;pins&=a[:,:,3]>0
# White highlights can carry a one-channel green bias. Exclude detached islands
# inside the face; only source-connected foreground locks own eye overlap.
labs,n=ndi.label(hair);sizes=np.bincount(labs.ravel());small=sizes[labs]<150
hair[small&face&(yy>=469)&(yy<=529)]=False
# Guard blended strand ink at cheek tips and roots, without claiming brow/eye
# interiors. This is a source recut, not a paint-over of facial structure.
edge=ndi.binary_dilation(hair,iterations=2)&face&~browkeep&~earring&~pins
edge&=~((yy>=469)&(yy<=529))
hair|=edge&(a[:,:,3]>0)
# Preserve all visible warm ear/cheek/neck skin outside the hand-drawn envelope.
# Only the narrow blended fringe adjacent to actual green hair can travel.
near_green=ndi.binary_dilation(chrom,iterations=3)
warm=(r-g>15)&(r-b>24)&(yy>335)&~near_green
hair[warm&~face]=False
# Explicit visible source tip traces capture low-saturation antialiasing that
# cannot be classified by green hue alone. These paths are native source recuts.
tip_paths=[([(588,497),(600,512),(614,524),(628,532)],7), ([(424,516),(431,533),(441,545),(450,551),(462,555)],7),
 ([(429,569),(442,579),(453,584),(465,587)],8),
 ([(432,595),(446,605),(463,612)],8),
 ([(715,514),(708,535),(699,547),(687,557),(674,561)],7),
 ([(705,560),(696,577),(684,588),(669,597)],8),
 ([(573,502),(580,513),(588,519),(599,521)],7),
 ([(594,521),(604,532),(615,539),(633,542)],8),
 ([(645,531),(659,541),(672,546),(684,547)],8)]
tip_im=Image.new('L',(w,h));tip_draw=ImageDraw.Draw(tip_im)
for points,width in tip_paths: tip_draw.line(points,fill=255,width=width+6,joint='curve')
tips=np.array(tip_im)>0
hair|=tips
Image.fromarray((tips*255).astype('uint8')).save(ROOT/'explicit_source_tip_mask.png')
# Eye worker audited exact source lashes; these belong only to eye objects.
lash_exclude=np.array(Image.open(PROJECT/'canonical_sources/hair_lash_exclusion.png').convert('L'))>0
hair[lash_exclude]=False
# Source dark eyeliner cannot travel as foreground hair. Restrict this trim
# to actual upper-lash eye regions; retain original green hair including AA.
for x0,x1 in [(410,533),(607,719)]:
 band=(xx>=x0)&(xx<x1)&(yy>=469)&(yy<499)
 hair[band&(g<45)&(r<45)]=False
# Independently audited visible facial landmarks have no hair ownership.
hair[(xx>=480)&(xx<=580)&(yy>=530)&(yy<=670)]=False
hair[(xx>=480)&(xx<=540)&(yy>=440)&(yy<=480)]=False
hair[(xx>=482)&(xx<=646)&(yy>=675)&(yy<=800)]=False
# Partition along visible strand-flow boundaries. Hidden continuation is unknown.
corrections=PROJECT/'canonical_sources/ownership_corrections'
skin_restore=np.array(Image.open(corrections/'restore_visible_skin.png'))>0
hair_restore=np.array(Image.open(corrections/'restore_visible_hair.png'))>0
hair&=~skin_restore;hair|=hair_restore
left=poly([(250,390),(402,281),(446,298),(445,405),(431,482),(442,544),(468,616),(466,668),(485,798),(250,810)])
right=poly([(703,374),(843,370),(846,813),(640,812),(651,670),(675,609),(703,558),(718,478)])
crown=poly([(240,0),(850,0),(850,290),(760,292),(712,237),(642,190),(583,166),(532,157),(505,176),(454,179),(384,226),(240,340)])
parts={};remain=hair.copy()
for name,region,pivot in [('temple_left',left,[425,407]),('temple_right',right,[721,420]),('crown_bun_rear',crown,[567,208]),('front_fringe',np.ones((h,w),bool),[529,218])]:
 mask=remain&region;remain&=~mask;parts[name]=(mask,pivot)
pendant=pins&(xx>=778)&(yy>=184)
parts['gold_hairsticks']=(pins&~pendant,[686,195])
parts['gold_hanging_ornament']=(pendant,[790,184])
owned=hair|pins
back=a.copy();back[owned]=0
# Local hidden guard exists only beneath opaque hair over adjacent face skin;
# never replace or move a visible source face/neck/outfit pixel.
eye_exclude=((xx>=408)&(xx<=536)&(yy>=475)&(yy<=535))|((xx>=603)&(xx<=722)&(yy>=474)&(yy<=533))
skin=face&(ndi.distance_transform_edt(~hair)>2)&~hair&~pins&~earring&~browkeep&~eye_exclude&(r-g>22)&(r-b>35)&(r>190)&(g>135)&(b>105)&(a[:,:,3]==255)&(yy<755)
dist,idx=ndi.distance_transform_edt(~skin,return_indices=True)
rigid_reveal_margin=ndi.distance_transform_edt(hair)<=16
guard=hair&((face&((dist<=40)|rigid_reveal_margin))|((dist<=12)&(yy>520)&(yy<750)))&(a[:,:,3]==255)
hidden=a[idx[0],idx[1]].astype(float)
for c in range(3): hidden[:,:,c]=ndi.gaussian_filter(hidden[:,:,c],sigma=3)
back[guard]=np.clip(hidden[guard],0,255).astype('uint8')
# Remaining backing has no source hair pixels, including external hair ink.
Image.fromarray(back).save(ROOT/'canonical_clean_backing.png')
Image.fromarray((hair*255).astype('uint8')).save(ROOT/'full_hair_exclusion_mask.png')
Image.fromarray((owned*255).astype('uint8')).save(ROOT/'full_hair_and_pins_exclusion_mask.png')
Image.fromarray((guard*255).astype('uint8')).save(ROOT/'estimated_hidden_skin_mask.png')
manifest={'canvas':[w,h],'source':'artwork/bust_base.png','source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'coordinate_system':'native source pixels, x right, y down; full-canvas assets at (0,0); scale 1','backing':'canonical_clean_backing.png','hair_exclusion_mask':'full_hair_exclusion_mask.png','layers':{},'limitations':['Single flattened source cannot reveal occluded scalp, rear-hair boundaries, or full hidden locks. No claim of recovered original hidden anatomy.','Partition paths are visible-source ownership seams, not complete hidden-strand topology. Restrict rigid rotations to small angles until seam guards are authored.','Hidden skin uses nearby source skin under foreground locks, with a 16-pixel rigid-motion reveal margin. Hair-hide exposes missing upper scalp rather than a redesigned head.','Earrings remain static canonical pixels in backing; not falsely presented as independently reconstructed accessories.', 'Existing source fringe/alpha artifacts are deliberately preserved in original extracted objects.']}
restored=Image.fromarray(back)
for name,(m,pivot) in parts.items():
 layer=np.zeros_like(a);layer[m]=a[m];Image.fromarray(layer).save(ROOT/f'{name}.png');Image.fromarray((m*255).astype('uint8')).save(ROOT/f'{name}_mask.png');restored=Image.alpha_composite(restored,Image.fromarray(layer))
 ys,xs=np.where(m);manifest['layers'][name]={'asset':f'{name}.png','mask':f'{name}_mask.png','pivot':pivot,'bounds':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'owned_pixels':int(m.sum()),'transform':'rigid only; no mesh deformation','cropped_asset':f'{name}_crop.png','crop_origin':[int(xs.min()),int(ys.min())]}

for name,(m,pivot) in parts.items():
 if name.startswith('gold_'): continue
 valid_core=m&(g-r>5)&(g-b>2)&(g>55)
 distance=ndi.distance_transform_edt(~m)
 _,nearest=ndi.distance_transform_edt(~valid_core,return_indices=True)
 guard_edge=(distance<=8)&~m&hair&(a[:,:,3]==255)
 under=np.zeros_like(a);under[guard_edge]=a[nearest[0][guard_edge],nearest[1][guard_edge]];under[guard_edge,3]=255
 Image.fromarray(under).save(ROOT/f'{name}_underlap.png')
 gy,gx=np.where(guard_edge);box=[int(gx.min()),int(gy.min()),int(gx.max()+1),int(gy.max()+1)]
 Image.fromarray(under).crop(tuple(box)).save(ROOT/f'{name}_underlap_crop.png')
 manifest['layers'][name]['hidden_underlap']={'asset':f'{name}_underlap_crop.png','crop_origin':box[:2],'pivot':pivot,'pixels':int(guard_edge.sum()),'provenance':'Estimated nearest valid own-green-core RGB within 8px internal source ownership seam only; hidden beneath canonical opaque hair at neutral. Render every underlap behind every owned hair layer, with its owner rigid transform.'}
for name,entry in manifest['layers'].items():
 Image.open(ROOT/entry['asset']).crop(tuple(entry['bounds'])).save(ROOT/entry['cropped_asset'])
restored.save(ROOT/'neutral_recomposed.png');out=np.array(restored);delta=np.abs(out.astype(int)-a.astype(int));pm=lambda t:t[:,:,:3].astype(float)*t[:,:,3:4]/255
report={'neutral_rgba_max_error':int(delta.max()),'neutral_changed_pixels':int(np.any(delta,axis=2).sum()),'neutral_premultiplied_max_error':float(np.abs(pm(out)-pm(a)).max()),'unchanged_visible_nonhair':bool(np.array_equal(back[~owned],a[~owned])),'exclusive_ownership':bool(np.max(sum(m.astype(int) for m,_ in parts.values()))==1),'hidden_skin_pixels':int(guard.sum()),'hair_owned_pixels':int(hair.sum()),'no_scaling':True}
manifest['validation']=report;(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(report,indent=2))
# Compositing proof shown on neutral gray, with face and neck at native widths.
sheet=Image.new('RGB',(w*3,h+30),'#555555');d=ImageDraw.Draw(sheet)
for n,(label,im) in enumerate([('CANONICAL',Image.fromarray(a)),('HAIR HIDDEN / LOCAL GUARDS',Image.fromarray(back)),('NATIVE RECOMPOSITION',restored)]):
 bg=Image.new('RGBA',(w,h),'#555555');bg.alpha_composite(im);sheet.paste(bg.convert('RGB'),(n*w,30));d.text((n*w+20,8),label,fill='white')
sheet.resize((1704,707)).save(ROOT/'hair_ownership_proof.png')
