from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
ROOT=Path('/mnt/agents/output')
REF=ROOT/'vtuber/reference'
REN=ROOT/'app/renders/phase_04'
OUT=ROOT/'vtuber/previews/phase_04'
BROWSER=ROOT/'app/assets/previews'
OUT.mkdir(parents=True,exist_ok=True); BROWSER.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(size,bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)
def crop(path,box): return Image.open(path).convert('RGB').crop(box)
def contain(im,size,bg=(234,235,231)):
    im=im.copy(); im.thumbnail(size,Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',size,bg); canvas.paste(im,((size[0]-im.width)//2,(size[1]-im.height)//2)); return canvas
def text(draw,xy,value,size=20,fill=(46,55,60),bold=False): draw.text(xy,value,font=font(size,bold),fill=fill)
def header(title,subtitle,width):
    im=Image.new('RGB',(width,150),(245,243,238)); d=ImageDraw.Draw(im)
    text(d,(42,24),title,34,bold=True); text(d,(42,76),subtitle,20,fill=(87,91,90))
    text(d,(42,112),'UNCHANGED SOURCE REFERENCE  ↔  BLENDER FEASIBILITY PROTOTYPE',15,fill=(155,113,48),bold=True)
    return im

def comparison(path,title,subtitle,rows,notes,kind):
    width=1900; row_h=390; height=150+len(rows)*row_h+150
    im=Image.new('RGB',(width,height),(245,243,238)); im.paste(header(title,subtitle,width),(0,0)); d=ImageDraw.Draw(im)
    text(d,(70,158),'REFERENCE CROP',17,bold=True); text(d,(995,158),'BLENDER CROP',17,bold=True)
    for i,(label,ref,blend) in enumerate(rows):
        y=195+i*row_h
        text(d,(70,y),label,21,bold=True); text(d,(995,y),label+' / PROTOTYPE',21,bold=True)
        im.paste(contain(ref,(830,300)),(70,y+35)); im.paste(contain(blend,(830,300)),(995,y+35))
        if i<len(rows)-1: d.line((55,y+355,width-55,y+355),fill=(213,207,194),width=2)
    y=height-130; d.rounded_rectangle((45,y,width-45,height-25),radius=12,fill=(232,230,220))
    for j,note in enumerate(notes): text(d,(70,y+18+j*32),'•  '+note,17,fill=(61,65,63))
    im.save(path)

eye_ref=REF/'RYO_MOD_eye-details_v001.png'
eye_rows=[
 ('NEUTRAL / ALMOND OPENING',crop(eye_ref,(0,0,512,512)),crop(REN/'prototype_neutral.png',(185,210,620,395))),
 ('FULL BLINK',crop(eye_ref,(0,512,512,1024)),crop(REN/'prototype_blink.png',(185,210,620,395))),
 ('THREE-QUARTER CONSTRUCTION',crop(eye_ref,(512,512,1024,1024)),crop(REN/'prototype_neutral_three_quarter.png',(95,215,450,405))),
 ('SIDE CONSTRUCTION',crop(eye_ref,(1024,512,1536,1024)),crop(REN/'prototype_blink_side.png',(45,205,330,390))),
]
comparison(OUT/'Phase 04 — Reference vs Blender Eyes.png','PHASE 04  /  EYE + BLINK FEASIBILITY','Eye opening, closure and oblique construction  •  interim inserts, not final anime facial materials',eye_rows,
 ['Blink now deforms the whites, irises, lids and lashes together; the former folded-lid corner artifact is corrected.','Eye shape, lash design, iris shading and final fitted textures still require production refinement against the artwork.'],'eyes')

mouth_ref=REF/'RYO_MOD_mouth-details_v001.png'
mouth_rows=[
 ('CLOSED / NEUTRAL',crop(mouth_ref,(40,80,472,400)),crop(REN/'prototype_neutral.png',(260,430,550,630))),
 ('JAW OPEN',crop(mouth_ref,(1060,70,1510,430)),crop(REN/'prototype_jaw_open.png',(260,420,550,660))),
 ('TEETH-VISIBLE SMILE',crop(mouth_ref,(40,590,472,925)),crop(REN/'prototype_smile.png',(260,430,550,630))),
 ('FUNNEL / O FORM',crop(mouth_ref,(550,590,990,925)),crop(REN/'prototype_funnel.png',(260,420,550,660))),
 ('THREE-QUARTER OPEN SMILE',crop(mouth_ref,(1060,580,1510,940)),crop(REN/'prototype_smile_jaw_three_quarter.png',(115,415,370,635))),
]
comparison(OUT/'Phase 04 — Reference vs Blender Mouth.png','PHASE 04  /  MOUTH + JAW FEASIBILITY','Closed, open, smile and funnel controls  •  separate oral insert plus real head jaw/smile keys',mouth_rows,
 ['The mouth aperture remains open in front, side and three-quarter tests, with separate teeth and tongue.','Oral contours, tooth/tongue surfaces and transitions are provisional; final joined topology and refined anime forms remain open.'],'mouth')

# Full neutral identity boundary board.
width=1900; height=1190
im=Image.new('RGB',(width,height),(245,243,238)); im.paste(header('PHASE 04  /  NEUTRAL IDENTITY BOUNDARY','The control prototype is readable as anime-inspired 3D, but final likeness is not yet approved',width),(0,0)); d=ImageDraw.Draw(im)
text(d,(70,165),'NEUTRAL BUST / REFERENCE',18,bold=True); text(d,(995,165),'NEUTRAL / BLENDER PROTOTYPE',18,bold=True)
im.paste(contain(Image.open(REF/'RYO_MOD_neutral-bust_front_v001.png'),(830,850)),(70,200))
im.paste(contain(Image.open(REN/'prototype_neutral.png'),(830,850)),(995,200))
d.rounded_rectangle((45,1070,width-45,1160),radius=12,fill=(232,230,220))
text(d,(70,1090),'•  Approval requested for control feasibility only—not final facial likeness, joined topology, production textures or ARKit coverage.',18,fill=(61,65,63))
im.save(OUT/'Phase 04 — Neutral Identity Boundary.png')

# Control contact sheet with all authored feasibility forms.
forms=[('NEUTRAL','prototype_neutral.png'),('FULL BLINK','prototype_blink.png'),('GAZE LEFT','prototype_gaze_left.png'),('JAW OPEN','prototype_jaw_open.png'),('SMILE','prototype_smile.png'),('SMILE + JAW','prototype_smile_jaw.png'),('FUNNEL','prototype_funnel.png'),('WIDE + GAZE UP','prototype_wide_gaze.png')]
w=2000; h=1390
sheet=Image.new('RGB',(w,h),(31,39,44)); d=ImageDraw.Draw(sheet)
text(d,(35,22),'PHASE 04  /  AUTHORED FACIAL CONTROL STATES',30,fill=(237,240,237),bold=True)
text(d,(35,68),'Eight static inspections from the editable Blender prototype',18,fill=(185,198,198))
for i,(label,name) in enumerate(forms):
    x=25+(i%4)*495; y=115+(i//4)*610
    sheet.paste(contain(Image.open(REN/name),(475,540),(48,55,58)),(x,y))
    text(d,(x+12,y+552),label,18,fill=(231,234,229),bold=True)
sheet.save(OUT/'Phase 04 — Facial Control Contact Sheet.png')

# Independent directional and one-sided controls.
forms=[('BLINK / CHARACTER LEFT','prototype_blink_left_only.png'),('BLINK / CHARACTER RIGHT','prototype_blink_right_only.png'),('GAZE RIGHT','prototype_gaze_right.png'),('GAZE UP','prototype_gaze_up.png'),('GAZE DOWN','prototype_gaze_down.png')]
w=2000; h=650
sheet=Image.new('RGB',(w,h),(31,39,44)); d=ImageDraw.Draw(sheet)
text(d,(35,22),'PHASE 04  /  INDEPENDENT CONTROL CHECKS',28,fill=(237,240,237),bold=True)
text(d,(35,64),'One-sided blink isolation and all four gaze directions',18,fill=(185,198,198))
for i,(label,name) in enumerate(forms):
    x=20+i*396
    sheet.paste(contain(Image.open(REN/name),(380,500),(48,55,58)),(x,110))
    text(d,(x+10,565),label,15,fill=(231,234,229),bold=True)
sheet.save(OUT/'Phase 04 — Independent Blink and Gaze.png')

for src,name in [
 (OUT/'Phase 04 — Reference vs Blender Eyes.png','phase4-eyes.png'),
 (OUT/'Phase 04 — Reference vs Blender Mouth.png','phase4-mouth.png'),
 (OUT/'Phase 04 — Neutral Identity Boundary.png','phase4-neutral.png'),
 (OUT/'Phase 04 — Facial Control Contact Sheet.png','phase4-controls.png'),
 (OUT/'Phase 04 — Independent Blink and Gaze.png','phase4-independent.png')]:
    Image.open(src).save(BROWSER/name)
print('Phase 4 comparison boards packaged.')
