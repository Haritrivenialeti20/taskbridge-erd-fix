from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
root=Path(__file__).resolve().parents[1]; out=root/'schema-verification.png'
W,H=1280,720; bg='#f5f7f4'; ink='#17222b'; muted='#6e7c83'; green='#18764b'; mint='#c9f0d7'; line='#dce4df'; white='#fff'
reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; f=lambda n,b=False: ImageFont.truetype(bold if b else reg,n)
im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
d.rectangle((0,0,W,76),fill=white); d.rectangle((52,24,92,61),fill=ink); d.text((61,31),'PG',font=f(12,True),fill=white); d.text((112,28),'TASKBRIDGE SCHEMA VERIFICATION',font=f(14,True),fill=ink)
d.text((58,122),'POSTGRESQL STRUCTURE',font=f(13,True),fill=green); d.text((58,157),'Three entities, two enforced relationships',font=f(39,True),fill=ink); d.text((60,214),'Verification harness confirms the corrected design and integrity constraints.',font=f(18),fill=muted)
items=[('users','PRIMARY KEY id · UNIQUE email · NOT NULL name'),('projects','PRIMARY KEY project_id · NOT NULL name'),('tasks','PRIMARY KEY task_id · FK user_id · FK project_id'),('integrity','orphan references rejected · 3 indexes present')]
d.rounded_rectangle((70,280,1210,620),radius=18,fill=white,outline=line,width=2)
for i,(h,b) in enumerate(items):
 y=315+i*70
 d.ellipse((103,y,139,y+36),fill=mint); d.text((113,y+8),'✓',font=f(15,True),fill=green); d.text((180,y+3),h,font=f(18,True),fill=ink); d.text((180,y+31),b,font=f(14),fill=muted)
d.text((70,658),'schema verification passed · valid insert accepted · invalid references rejected',font=f(15,True),fill=green)
im.save(out)
