#!/usr/bin/env python3
"""Socket-free EGL reconstruction of sampled Godot canvas draws.

This is NOT a native Godot screenshot or native GPU parity test. Animation,
attachment, geometry, material values and texture pixels come from Godot's
actual full_body_rig scene. Original canvas shader bodies execute unchanged
inside a small desktop GLSL wrapper on the installed Mesa software renderer.
No facial control/timeline mathematics or neutral composite is substituted.
"""
import argparse, ctypes as C, json, os, re, subprocess, time, gzip
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
os.environ.setdefault('MESA_SHADER_CACHE_DIR','/tmp/ryoko-face-mesa-cache')
os.environ.setdefault('LIBGL_ALWAYS_SOFTWARE','1')
HERE=Path(__file__).resolve().parent

class GL:
 def __init__(self,width,height):
  self.width,self.height=width,height
  self.e=C.CDLL('libEGL.so.1');self.g=C.CDLL('libGL.so.1')
  def ef(name,ret,*types):return self.fn(self.e,name,ret,*types)
  get=ef('eglGetProcAddress',C.c_void_p,C.c_char_p)
  display=C.CFUNCTYPE(C.c_void_p,C.c_uint,C.c_void_p,C.POINTER(C.c_int))(get(b'eglGetPlatformDisplayEXT'))(0x31DD,None,None)
  a,b=C.c_int(),C.c_int()
  assert ef('eglInitialize',C.c_uint,C.c_void_p,C.POINTER(C.c_int),C.POINTER(C.c_int))(display,C.byref(a),C.byref(b))
  assert ef('eglBindAPI',C.c_uint,C.c_uint)(0x30A2)
  attrs=(C.c_int*13)(0x3033,1,0x3040,8,0x3024,8,0x3023,8,0x3022,8,0x3021,8,0x3038)
  config,count=C.c_void_p(),C.c_int()
  assert ef('eglChooseConfig',C.c_uint,C.c_void_p,C.POINTER(C.c_int),C.POINTER(C.c_void_p),C.c_int,C.POINTER(C.c_int))(display,attrs,C.byref(config),1,C.byref(count)) and count.value
  ctx=ef('eglCreateContext',C.c_void_p,C.c_void_p,C.c_void_p,C.c_void_p,C.POINTER(C.c_int))(display,config,None,(C.c_int*1)(0x3038))
  surface=ef('eglCreatePbufferSurface',C.c_void_p,C.c_void_p,C.c_void_p,C.POINTER(C.c_int))(display,config,(C.c_int*5)(0x3057,width,0x3056,height,0x3038))
  assert ef('eglMakeCurrent',C.c_uint,C.c_void_p,C.c_void_p,C.c_void_p,C.c_void_p)(display,surface,surface,ctx)
  self.bind_functions()
  self.renderer=self.glGetString(0x1F01).decode()
  print('EGL offscreen renderer:',self.renderer,flush=True)
  self.glEnable(0x0BE2);self.glBlendFuncSeparate(0x0302,0x0303,1,0x0303)
  self.glPixelStorei(0x0CF5,1);self.glPixelStorei(0x0D05,1)
  self.vao=C.c_uint();self.glGenVertexArrays(1,C.byref(self.vao));self.glBindVertexArray(self.vao)
  self.vbo=C.c_uint();self.glGenBuffers(1,C.byref(self.vbo));self.glBindBuffer(0x8892,self.vbo)
  self.glEnableVertexAttribArray(0);self.glEnableVertexAttribArray(1)
  self.glVertexAttribPointer(0,2,0x1406,False,16,C.c_void_p(0));self.glVertexAttribPointer(1,2,0x1406,False,16,C.c_void_p(8))
  self.locations={};self.textures={};self.programs={};self.last_program=None
 def fn(self,lib,name,result,*types):
  f=getattr(lib,name);f.restype=result;f.argtypes=types;return f
 def bind_functions(self):
  U,I,F,P,S,B=C.c_uint,C.c_int,C.c_float,C.c_void_p,C.c_char_p,C.c_ubyte
  signatures={
   'glGetString':(S,U),'glGetError':(U,), 'glEnable':(None,U),'glBlendFuncSeparate':(None,U,U,U,U),
   'glPixelStorei':(None,U,I),'glViewport':(None,I,I,I,I),'glClearColor':(None,F,F,F,F),'glClear':(None,U),
   'glGenTextures':(None,I,P),'glBindTexture':(None,U,U),'glTexImage2D':(None,U,I,I,I,I,I,U,U,P),'glTexParameteri':(None,U,U,I),'glActiveTexture':(None,U),
   'glCreateShader':(U,U),'glShaderSource':(None,U,I,P,P),'glCompileShader':(None,U),'glGetShaderiv':(None,U,U,P),'glGetShaderInfoLog':(None,U,I,P,P),
   'glCreateProgram':(U,),'glAttachShader':(None,U,U),'glLinkProgram':(None,U),'glGetProgramiv':(None,U,U,P),'glGetProgramInfoLog':(None,U,I,P,P),'glUseProgram':(None,U),
   'glGetUniformLocation':(I,U,S),'glUniform1i':(None,I,I),'glUniform1f':(None,I,F),'glUniform2fv':(None,I,I,P),'glUniform3fv':(None,I,I,P),'glUniform4fv':(None,I,I,P),'glUniformMatrix3fv':(None,I,I,B,P),
   'glGenVertexArrays':(None,I,P),'glBindVertexArray':(None,U),'glGenBuffers':(None,I,P),'glBindBuffer':(None,U,U),'glBufferData':(None,U,C.c_ssize_t,P,U),'glEnableVertexAttribArray':(None,U),'glVertexAttribPointer':(None,U,I,U,B,I,P),'glDrawArrays':(None,U,I,I),
   'glReadPixels':(None,I,I,I,I,U,U,P),'glFinish':(None,),
  }
  for name,(result,*args) in signatures.items():setattr(self,name,self.fn(self.g,name,result,*args))
 def compile_shader(self,source,kind):
  shader=self.glCreateShader(kind);data=C.c_char_p(source.encode())
  self.glShaderSource(shader,1,C.byref(data),None);self.glCompileShader(shader)
  ok=C.c_int();self.glGetShaderiv(shader,0x8B81,C.byref(ok))
  if not ok.value:
   buf=C.create_string_buffer(20000);self.glGetShaderInfoLog(shader,len(buf),None,buf)
   raise RuntimeError(buf.value.decode()+'\n'+source)
  return shader
 def program(self,vertex,fragment):
  p=self.glCreateProgram()
  self.glAttachShader(p,self.compile_shader(vertex,0x8B31));self.glAttachShader(p,self.compile_shader(fragment,0x8B30));self.glLinkProgram(p)
  ok=C.c_int();self.glGetProgramiv(p,0x8B82,C.byref(ok))
  if not ok.value:
   buf=C.create_string_buffer(20000);self.glGetProgramInfoLog(p,len(buf),None,buf);raise RuntimeError(buf.value.decode())
  return p
 def loc(self,p,name):
  key=(p,name)
  if key not in self.locations:self.locations[key]=self.glGetUniformLocation(p,name.encode())
  return self.locations[key]
 def uniform(self,p,name,value,typ=None):
  loc=self.loc(p,name)
  if loc<0:return
  if typ in ('int','bool','sampler2D') or (typ is None and isinstance(value,(bool,int))):self.glUniform1i(loc,int(value))
  elif isinstance(value,(float,int)):self.glUniform1f(loc,float(value))
  else:
   a=np.asarray(value,dtype=np.float32)
   if a.size==9:self.glUniformMatrix3fv(loc,1,True,a.ctypes.data)
   else:getattr(self,'glUniform%dfv'%a.size)(loc,1,a.ctypes.data)
 def texture(self,key,path,nearest=False):
  cache=(key,nearest)
  if cache not in self.textures:
   im=Image.open(path).convert('RGBA');data=np.asarray(im,dtype=np.uint8)
   tex=C.c_uint();self.glGenTextures(1,C.byref(tex));self.glBindTexture(0x0DE1,tex)
   self.glTexParameteri(0x0DE1,0x2801,0x2600 if nearest else 0x2601);self.glTexParameteri(0x0DE1,0x2800,0x2600 if nearest else 0x2601)
   self.glTexParameteri(0x0DE1,0x2802,0x812F);self.glTexParameteri(0x0DE1,0x2803,0x812F)
   self.glTexImage2D(0x0DE1,0,0x8058,im.width,im.height,0,0x1908,0x1401,data.ctypes.data)
   self.textures[cache]=(tex.value,im.size)
  return self.textures[cache]

def pull_function(source,name):
 match=re.search(r'void\s+'+name+r'\s*\(\s*\)\s*\{',source)
 if not match:return source,''
 i=match.end();depth=1
 while depth:
  if source[i]=='{':depth+=1
  elif source[i]=='}':depth-=1
  i+=1
 return source[:match.start()]+source[i:],source[match.end():i-1]

def shader_wrappers(source):
 source=re.sub(r'//[^\n]*','',source)
 uniforms={m[1]:(m[0],m[2]) for m in re.findall(r'uniform\s+(\w+)\s+(\w+)\s*([^;]*);',source)}
 source=re.sub(r'\b(?:shader_type|render_mode)[^;]*;','',source)
 source=re.sub(r'(uniform\s+\w+\s+\w+)\s*:[^=;]*(?=[=;])',r'\1 ',source)
 source,vertex=pull_function(source,'vertex');source,fragment=pull_function(source,'fragment')
 vertex_source=re.sub(r'\bvarying\b','out',source)
 fragment_source=re.sub(r'\bvarying\b','in',source)
 header='#version 330 core\nuniform sampler2D TEXTURE;\nuniform vec2 TEXTURE_PIXEL_SIZE;\nuniform vec4 draw_modulate;\nvec2 UV;\nvec2 VERTEX;\nvec4 COLOR;\n'
 vs=header+'''layout(location=0) in vec2 in_position;
layout(location=1) in vec2 in_uv;
uniform mat3 draw_matrix;
uniform vec2 view_size;
out vec2 varying_uv;
'''+vertex_source+'''
void main(){VERTEX=in_position;UV=in_uv;COLOR=draw_modulate;
'''+vertex+'''
vec3 p=draw_matrix*vec3(VERTEX,1.0);gl_Position=vec4(p.x/view_size.x*2.0-1.0,1.0-p.y/view_size.y*2.0,0.0,1.0);varying_uv=UV;}
'''
 fs=header+'in vec2 varying_uv;\nout vec4 out_color;\n'+fragment_source+'''
void main(){UV=varying_uv;COLOR=texture(TEXTURE,UV)*draw_modulate;
'''+fragment+'\nout_color=COLOR;}\n'
 return vs,fs,uniforms

class Renderer:
 def __init__(self,folder,width=1024,height=1536):
  self.folder=Path(folder);self.data=json.loads((self.folder/'scene.json').read_text());self.gl=GL(width,height);self.meshes={};self.programs={}
  for key,shader in self.data['shaders'].items():
   vs,fs,uniforms=shader_wrappers((self.folder/shader['file']).read_text())
   self.programs[key]=(self.gl.program(vs,fs),uniforms)
  vs,fs,uniforms=shader_wrappers('')
  self.programs['default']=(self.gl.program(vs,fs),uniforms)
  self.background=(237/255,235/255,229/255,1)
  self.defaults={}
  for p,uniforms in self.programs.values():
   defaults={}
   for name,(typ,definition) in uniforms.items():
    if typ=='sampler2D':continue
    value=definition.split('=',1)[1].strip() if '=' in definition else '0'
    if typ.startswith('vec'):
     parts=[float(x.strip()) for x in re.sub(r'vec[234]\((.*)\)',r'\1',value).split(',')]
     defaults[name]=parts*int(typ[-1]) if len(parts)==1 else parts
    elif typ=='bool':defaults[name]=value=='true'
    elif typ=='int':defaults[name]=int(value)
    else:defaults[name]=float(value)
   self.defaults[p]=defaults
 def render(self,frame,camera=None):
  g=self.gl;g.glViewport(0,0,g.width,g.height);g.glClearColor(*self.background);g.glClear(0x4000)
  if camera is None:camera=np.eye(3)
  for idx in sorted(frame['draws'],key=lambda i:self.data['draw_states'][i]['z']):
   draw=self.data['draw_states'][idx];mat=draw['material'];p,uniforms=self.programs[mat.get('shader','default')]
   g.glUseProgram(p)
   a,b,c,d,x,y=draw['matrix'];m=camera@np.array([[a,c,x],[b,d,y],[0,0,1]])
   g.uniform(p,'draw_matrix',m);g.uniform(p,'view_size',[g.width,g.height]);g.uniform(p,'draw_modulate',draw['color'])
   key=draw['texture'];g.glActiveTexture(0x84C0);tex,size=g.texture(key,self.folder/self.data['textures'][key]['file'])
   g.glActiveTexture(0x84C0);g.glBindTexture(0x0DE1,tex);g.uniform(p,'TEXTURE',0,'sampler2D');g.uniform(p,'TEXTURE_PIXEL_SIZE',[1/size[0],1/size[1]])
   unit=1
   values=dict(self.defaults[p]);values.update(mat.get('uniforms',{}))
   for name,value in values.items():
    if isinstance(value,dict) and 'texture' in value:
     key=value['texture'];nearest='filter_nearest' in uniforms[name][1]
     g.glActiveTexture(0x84C0+unit);tex,_=g.texture(key,self.folder/self.data['textures'][key]['file'],nearest)
     g.glActiveTexture(0x84C0+unit);g.glBindTexture(0x0DE1,tex);g.uniform(p,name,unit,'sampler2D');unit+=1
    else:g.uniform(p,name,value,uniforms[name][0])
   # Unassigned uniforms retain their original shader declaration defaults per material.
   if idx not in self.meshes:
    if 'vertex_file' in draw:
     vertices=np.frombuffer(gzip.decompress((self.folder/draw['vertex_file']).read_bytes()),dtype='<f4').reshape(-1,2)
     uv=np.frombuffer(gzip.decompress((self.folder/draw['uv_file']).read_bytes()),dtype='<f4').reshape(-1,2)
     indexes=np.frombuffer(gzip.decompress((self.folder/draw['index_file']).read_bytes()),dtype='<i4')
    else:
     vertices=np.asarray(draw['vertices'],dtype=np.float32);uv=np.asarray(draw['uv'],dtype=np.float32)
     indexes=[]
     for poly in draw['triangles']:
      for i in range(1,len(poly)-1):indexes.extend([poly[0],poly[i],poly[i+1]])
    self.meshes[idx]=np.concatenate([vertices,uv],axis=1)[indexes].astype(np.float32)
   mesh=self.meshes[idx]
   if 'vertex_file' in draw:del self.meshes[idx]
   g.glBufferData(0x8892,mesh.nbytes,mesh.ctypes.data,0x88E0);g.glDrawArrays(4,0,len(mesh))
  result=np.empty((g.height,g.width,4),dtype=np.uint8)
  g.glReadPixels(0,0,g.width,g.height,0x1908,0x1401,result.ctypes.data)
  error=g.glGetError()
  if error:raise RuntimeError('OpenGL error '+hex(error))
  return Image.fromarray(result[::-1].copy(),'RGBA')

FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def presentation(canvas,frame,index,total,detail=None):
 image=Image.new('RGB',(1280,960),(25,31,37));d=ImageDraw.Draw(image)
 title=ImageFont.truetype(FONT,23);body=ImageFont.truetype(FONT,16);small=ImageFont.truetype(FONT,14)
 image.paste(canvas.convert('RGB').resize((558,837),Image.Resampling.LANCZOS),(24,82))
 image.paste(detail if detail is not None else canvas.crop((390,30,635,356.6667)).convert('RGB').resize((624,832),Image.Resampling.LANCZOS),(630,86))
 d.text((24,15),f"Ryoko / {frame['id']} / {frame['title']}",font=title,fill=(244,241,234))
 d.text((24,48),f"Full-body rig + approved live face  |  {frame['phase']}  |  {frame['time']:.2f} / {frame['duration']:.2f} s",font=body,fill=(142,230,205))
 d.text((630,65),'Same rig and frame / live face close-up',font=small,fill=(224,225,228))
 d.text((24,935),'Godot scene-state + original-shader reconstruction. Offscreen Mesa rendering, not native Godot capture.',font=small,fill=(213,217,223))
 return image

def detail_view(renderer,frame):
 scale=624/245
 camera=np.array([[scale,0,-390*scale],[0,scale,-30*scale],[0,0,1]])
 return renderer.render(frame,camera).crop((0,0,624,832)).convert('RGB')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--samples',default=str(HERE/'samples'));parser.add_argument('--output',default=str(HERE/'live_affection_full_body.mp4'));parser.add_argument('--still',type=int);parser.add_argument('--keyposes',action='store_true');args=parser.parse_args()
 r=Renderer(args.samples);frames=r.data['frames'];out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
 if args.still is not None:
  frame=frames[args.still];canvas=r.render(frame);result=presentation(canvas,frame,args.still,len(frames),detail_view(r,frame));result.save(out);canvas.save(out.with_name(out.stem+'_canvas.png'));print(out);return
 process=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x960','-r',str(r.data['fps']),'-i','-','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 start=time.monotonic();metrics=[];entry=None;neutral=None;peak_image=None
 for i,frame in enumerate(frames):
  canvas=r.render(frame);rgb=np.asarray(canvas.convert('RGB'))
  if entry is None or entry['id']!=frame['id']:
   if entry is not None:
    metrics.append(entry);peak_image.save(out.with_name(out.stem+'_'+entry['id']+'_peak.jpg'),quality=95)
   neutral=rgb.copy();entry={'id':frame['id'],'title':frame['title'],'authored_duration':frame['duration'],'frames':0,'face_roi':[445,128,580,236],'max_changed_face_pixels':0,'max_face_mae':0.0};peak_image=None
  delta=np.abs(rgb[128:236,445:580].astype(np.int16)-neutral[128:236,445:580].astype(np.int16))
  changed=int(np.any(delta>2,axis=2).sum());entry['frames']+=1
  if changed>entry['max_changed_face_pixels']:
   entry.update(max_changed_face_pixels=changed,peak_time=frame['time'],max_face_mae=float(delta.mean()))
   peak_image=presentation(canvas,frame,i,len(frames),detail_view(r,frame))
  entry['final_face_equal_neutral']=bool(np.array_equal(rgb[128:236,445:580],neutral[128:236,445:580]));entry['final_canvas_equal_neutral']=bool(np.array_equal(rgb,neutral));entry['final_pose_all_zero']=all(v==0 for v in frame['pose'].values());entry['final_phase']=frame['phase']
  result=presentation(canvas,frame,i,len(frames),detail_view(r,frame));process.stdin.write(result.tobytes())
  if i==0 or (i%30==0):print(f'{i+1}/{len(frames)} {frame["id"]} {time.monotonic()-start:.1f}s',flush=True)
  if i in (0,len(frames)//2,len(frames)-1):result.save(out.with_name(out.stem+f'_{i:05d}.jpg'),quality=95)
 if entry is not None:
  metrics.append(entry);peak_image.save(out.with_name(out.stem+'_'+entry['id']+'_peak.jpg'),quality=95)
 process.stdin.close()
 if process.wait():raise SystemExit('FFmpeg failed')
 report={'render_source':r.data['source'],'renderer':r.gl.renderer,'native_godot_capture':False,'shader_gpu_parity_verified':False,'frames':len(frames),'fps':r.data['fps'],'expressions':sorted(set(f['id'] for f in frames)),'face_pixel_checks':metrics,'all_faces_changed':all(e['max_changed_face_pixels']>0 for e in metrics),'all_returned_to_exact_neutral':all(e['final_face_equal_neutral'] and e['final_pose_all_zero'] for e in metrics)}
 out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(out)
if __name__=='__main__':main()
