shader_type canvas_item;
uniform vec2 origin;
uniform vec2 rigid_offset=vec2(0.0);
uniform float opening=0.0;
uniform float smile=0.0;
uniform float spread=0.0;
uniform float purse=0.0;
uniform float corner_lift=0.0;
uniform bool lip=false;
uniform bool upper_lip=false;
uniform bool underlip_shadow=false;
uniform sampler2D seam_texture : filter_linear, repeat_disable;
void fragment(){
 vec4 pixel=texture(TEXTURE,UV);
 vec2 p=origin+UV/ TEXTURE_PIXEL_SIZE+rigid_offset;
 float d=56.0*opening;
 float seam=620.0+texture(seam_texture,vec2(clamp((spread==0.0 ? (p.x-525.0) : (39.5+(p.x-564.5)/(1.0+20.0*spread/35.5)))/80.0,0.0,1.0),0.5)).r*63.75;
 if(purse>0.0){seam=620.0+texture(seam_texture,vec2(clamp((39.5+(p.x-564.5)/(1.0+20.0*spread/35.5-14.0*purse/35.5))/80.0,0.0,1.0),0.5)).r*63.75;}
 float fraction=clamp((p.y-633.0)/56.0,0.0,1.0);
 float width=mix(38.0-12.0*opening,35.5,smile)+20.0*spread;
 if(purse>0.0){width-=14.0*purse;}
 float half_width=width;
 float side=clamp((half_width-abs(p.x-564.5))/.7,0.0,1.0);
 if(lip){
   // Source-derived seam ownership with spatial lower-contour coverage.
   // Both original owners remain rigid; only their true overlap contributes
   // to upper source-over compensation.
   float local_seam=texture(seam_texture,vec2(UV.x,0.5)).r*63.75;
   float sx=UV.x/TEXTURE_PIXEL_SIZE.x;
   float lower_owner=smoothstep(local_seam+.45,local_seam+1.55,UV.y/TEXTURE_PIXEL_SIZE.y)*smoothstep(8.5,9.5,sx)*(1.0-smoothstep(69.5,70.5,sx));
   if(!underlip_shadow){
     float lower_alpha=pixel.a*lower_owner;
     if(upper_lip){
       // Same spatial seam rule as the separately jointed smile owners.
       // The lower owner is rigidly translated54*opening; query its native
       // source contour at this pixel, never warp this owner's pigment UV.
       vec2 peer=vec2(sx,UV.y/TEXTURE_PIXEL_SIZE.y-54.0*opening);
       float peer_alpha=0.0;
       if(peer.y>=0.0 && peer.y<=45.0){
         float peer_weight=smoothstep(local_seam+.45,local_seam+1.55,peer.y)*smoothstep(8.5,9.5,sx)*(1.0-smoothstep(69.5,70.5,sx));
         float ph=clamp(abs(p.x-564.5)/width,0.0,1.0);
         float curve=sqrt(max(0.0,1.0-pow(ph,4.0)));
         float gap=54.0*opening+1.0-56.0*opening*curve;
         float ellipse=pow((p.x-564.5)/(50.0-30.0*pow(opening,1.6)),2.0)+pow((peer.y-20.0)/(100.0-89.0*pow(opening,1.6)),2.0);
         peer_alpha=texture(TEXTURE,peer*TEXTURE_PIXEL_SIZE).a*peer_weight*(1.0-smoothstep(.82,1.0,ellipse))*(1.0-smoothstep(1.0,6.0,gap));
       }
       pixel.a=clamp((pixel.a-lower_alpha)/max(1.0-peer_alpha,.000001),0.0,1.0);
     }
     else{pixel.a=lower_alpha;}
   }
   if(!underlip_shadow){
   float target=40.0-(upper_lip ? 14.0 : 26.0)*pow(opening,1.6);
   float mask=clamp((target+2.0-abs(p.x-564.5))/.7,0.0,1.0);
   // Upper lip silhouette stays exactly at its original native width.
   if(!upper_lip){
     float hx=clamp(abs(p.x-564.5)/width,0.0,1.0);
     float boundary_curve=sqrt(max(0.0,1.0-pow(hx,4.0)));
     float contact_gap=54.0*opening+1.0-56.0*opening*boundary_curve;
     float ly=UV.y/TEXTURE_PIXEL_SIZE.y;
     float ellipse_h=100.0-89.0*pow(opening,1.6);
     float ellipse_w=50.0-30.0*pow(opening,1.6);
     float ellipse=pow((p.x-564.5)/ellipse_w,2.0)+pow((ly-20.0)/ellipse_h,2.0);
     pixel.a*=(1.0-smoothstep(.82,1.0,ellipse))*(1.0-smoothstep(1.0,6.0,contact_gap));
   }
   }
 }else{
   float horizontal=clamp(abs(p.x-564.5)/width,0.0,1.0);
   float curve=sqrt(max(0.0,1.0-pow(horizontal,4.0)));
   float smile_curve=pow(max(0.0,1.0-horizontal*horizontal),.72);
   float lifted_seam=seam-4.0*spread-(4.0+5.0*spread)*smile*pow(horizontal,1.5)-12.0*corner_lift*pow(clamp(abs((p.x-564.5)/(35.5+20.0*spread)),0.0,1.0),3.0);
   curve=mix(curve,smile_curve,smile);
   if(purse>0.0){
    float r=clamp(abs((p.x-564.5)/(35.5+20.0*spread-14.0*purse)),0.0,1.0);
    lifted_seam+=purse*(4.0+8.0*r*r);
    curve=mix(curve,sqrt(max(0.0,1.0-horizontal*horizontal)),purse);
   }
   float aperture=clamp(min(p.y-lifted_seam,lifted_seam+d*curve-p.y)/1.0,0.0,1.0);
   pixel.a*=aperture*side;
 }
 COLOR=pixel;
}
