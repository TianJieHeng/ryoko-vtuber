from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
ROOT=Path('/mnt/agents/output')
REF=ROOT/'vtuber/reference'; REN=ROOT/'app/renders/mesh_uv_textured_v001'; OUT=ROOT/'vtuber/previews/phase_03'; OUT.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(s,b=False):return ImageFont.truetype(BOLD if b else FONT,s)
def contain(im,size,bg=(235,236,233)):
 im=im.convert('RGB'); im.thumbnail(size,Image.Resampling.LANCZOS); c=Image.new('RGB',size,bg);c.paste(im,((size[0]-im.width)//2,(size[1]-im.height)//2));return c
def board(path,title,subtitle,panels,notes,width=2400,cell_w=385,cell_h=735):
 h=1110;im=Image.new('RGB',(width,h),(245,244,240));d=ImageDraw.Draw(im)
 d.text((45,30),title,font=font(38,True),fill=(31,43,48));d.text((45,82),subtitle,font=font(21),fill=(75,84,85))
 for i,(label,img) in enumerate(panels):
  x=45+i*cell_w;d.text((x,130),label,font=font(17,True),fill=(54,68,70));im.paste(contain(Image.open(img),(cell_w-24,cell_h)),(x,170))
 y=935;d.rounded_rectangle((40,y,width-40,h-35),radius=12,fill=(231,230,222))
 for j,note in enumerate(notes):d.text((65,y+22+j*43),'•  '+note,font=font(18),fill=(54,59,57))
 im.save(path)
front=REF/'RYO_MOD_fullbody_front_v001.png';side=REF/'RYO_MOD_fullbody_side_v001.png';back=REF/'RYO_MOD_fullbody_back_v001.png'
board(OUT/'Phase 03 — Reference vs Blender Full Body.png','PHASE 03  /  MODULAR SURFACE + FITTED TEXTURE CHECKPOINT','Approved reference ↔ Blender production foundation  •  silhouette, materials, UVs',
 [('FRONT / REFERENCE',front),('FRONT / BLENDER',REN/'matched_front.png'),('LEFT SIDE / REFERENCE',side),('LEFT SIDE / BLENDER',REN/'matched_left_side.png'),('BACK / REFERENCE',back),('BACK / BLENDER',REN/'matched_back.png')],
 ['Approved v002 silhouette is retained; semantic parts are labels for modular separation, not replacement geometry.','10 major parts: 140,767 triangles; 20 packed base-color/roughness maps; 13 accessory/core objects.','Open clothing/hair topology and generated skin shells are not deformation-certified. Facial/rig work has not started.'])
board(OUT/'Phase 03 — Reference vs Blender Face and Hair.png','PHASE 03  /  FACE + HAIR MATERIAL CHECKPOINT','Reference identity ↔ fitted-material Blender surface  •  expression work remains gated',
 [('NEUTRAL BUST / REFERENCE',REF/'RYO_MOD_neutral-bust_front_v001.png'),('HEAD / BLENDER',REN/'close_head_front.png'),('HAIR CONSTRUCTION / REFERENCE',REF/'RYO_DET-001_hair-construction_v002.png'),('REAR HAIR / BLENDER',REN/'close_hair_back.png')],
 ['The face remains a soft placeholder: no separate eyeballs, eyelid rig, mouth cavity, teeth, tongue, or ARKit shapes.','Hair and two-chopstick accessory placement are preserved; bun-core pieces remain temporary construction geometry.','Phase 4 must correct facial identity and demonstrate expression comparisons before facial approval.'],width=2000,cell_w=480)
board(OUT/'Phase 03 — Reference vs Blender Hands.png','PHASE 03  /  HAND SURFACE CHECKPOINT','Reference anatomy ↔ Blender neutral-pose hands  •  deformation topology still pending',
 [('HAND REFERENCE',REF/'RYO_DET-004_hands-pumps_v002.png'),('CHARACTER LEFT / BLENDER',REN/'close_hand_character_left.png'),('CHARACTER RIGHT / BLENDER',REN/'close_hand_character_right.png')],
 ['Neutral fingers and skin regions are preserved, but anatomical detail is simplified and nails/knuckle loops are not authored.','Skin shadow visibility is disabled for checkpoint rendering to suppress generated internal-shell artifacts.','Hand retopology, finger weights, and gesture deformation tests are required before rig certification.'],width=1800,cell_w=580)
board(OUT/'Phase 03 — UV Checker.png','PHASE 03  /  UV CHECKER EVIDENCE','Independent 0–1 UV space per major part  •  checker scale varies by island',
 [('FULL BODY / UV CHECKER',REN/'uv_checker_front.png'),('HEAD + HAIR / UV CHECKER',REN/'uv_checker_head.png')],
 ['All ten major parts have one UV layer and separate fitted base-color/roughness textures.','Smart-projected islands are fragmented and texel density is uneven; final facial/manual UV refinement remains open.'],width=1400,cell_w=650,cell_h=735)
# Orbit contact sheet.
orb=Image.new('RGB',(1600,1740),(20,27,31));d=ImageDraw.Draw(orb);d.text((28,20),'PHASE 03  /  BLENDER ORBIT — FITTED MATERIALS',font=font(25,True),fill=(229,236,237))
for i in range(8):
 im=contain(Image.open(REN/f'orbit_{i:02d}_deg_{i*45:03d}.png'),(390,390),(38,46,50));x=(i%4)*400;y=80+(i//4)*420;orb.paste(im,(x,y));d.text((x+12,y+392),f'{i*45:03d}°',font=font(16),fill=(196,213,215))
orb.save(OUT/'Phase 03 — Blender Orbit.png')
# Browser-ready copies.
browser=ROOT/'app/assets/previews';browser.mkdir(parents=True,exist_ok=True)
for src,name in [(OUT/'Phase 03 — Reference vs Blender Full Body.png','phase3-full-body.png'),(OUT/'Phase 03 — Reference vs Blender Face and Hair.png','phase3-face-hair.png'),(OUT/'Phase 03 — Reference vs Blender Hands.png','phase3-hands.png'),(OUT/'Phase 03 — UV Checker.png','phase3-uv-checker.png'),(OUT/'Phase 03 — Blender Orbit.png','phase3-orbit.png')]:Image.open(src).save(browser/name)
print('Phase 3 comparison and evidence boards packaged.')
