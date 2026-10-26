from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
OUT=Path('video_frames'); OUT.mkdir(exist_ok=True)
W,H=1280,720; bg='#f5f7f4'; ink='#17222b'; muted='#6e7c83'; green='#18764b'; mint='#c9f0d7'; line='#dce4df'; white='#fff'
reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; f=lambda n,b=False: ImageFont.truetype(bold if b else reg,n)
def base(k,t,s=''):
 im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im); d.rectangle((0,0,W,74),fill=white); d.rectangle((52,24,90,61),fill=ink); d.text((61,31),'TB',font=f(12,True),fill=white); d.text((110,28),'TASKBRIDGE ERD REVIEW',font=f(14,True),fill=ink); d.text((58,120),k.upper(),font=f(13,True),fill=green); d.text((58,157),t,font=f(40,True),fill=ink); d.text((60,216),s,font=f(18),fill=muted); return im,d
def save(im,n): im.save(OUT/f'{n:02d}.png')
im,d=base('Challenge 3','From ERD to PostgreSQL','Correcting a TaskBridge task-management model before implementation.')
d.rounded_rectangle((70,310,1210,585),radius=20,fill=white,outline=line,width=2)
for x,h,b in [(110,'USERS','identity'),(440,'PROJECTS','workspaces'),(770,'TASKS','assigned work')]:
 d.ellipse((x,370,x+62,432),fill=mint); d.text((x+18,387),'✓',font=f(28,True),fill=green); d.text((x,465),h,font=f(18,True),fill=ink); d.text((x,503),b,font=f(15),fill=muted)
save(im,1)
im,d=base('Flaws found','The blueprint needed integrity rules','Missing primary keys and foreign keys would let invalid data enter the database.')
for y,h,b in [(300,'USERS.ID','not marked as a primary key'),(390,'TASKS.USER_ID + PROJECT_ID','integers without references'),(480,'TASK_OWNER_NAME','redundant copy of user data')]:
 d.rounded_rectangle((78,y,1200,y+60),radius=11,fill=white,outline=line,width=2); d.text((105,y+19),h,font=f(15,True),fill=green); d.text((430,y+19),b,font=f(17),fill=ink)
save(im,2)
im,d=base('Corrected ERD','One user and one project per task','The corrected diagram makes both one-to-many relationships explicit.')
di=Image.open('corrected_erd.png').convert('RGB'); di.thumbnail((980,410)); im.paste(di,((W-di.width)//2,270)); save(im,3)
im,d=base('PostgreSQL mapping','Every ERD concept has a database equivalent','Entities become tables, identifiers become primary keys, and relationships become foreign keys.')
for y,h,b in [(300,'USERS','id SERIAL PRIMARY KEY · email UNIQUE NOT NULL'),(390,'PROJECTS','project_id SERIAL PRIMARY KEY · name NOT NULL'),(480,'TASKS','task_id PRIMARY KEY · user_id FK · project_id FK')]:
 d.rounded_rectangle((78,y,1200,y+60),radius=11,fill=white,outline=line,width=2); d.text((105,y+19),h,font=f(14,True),fill=green); d.text((390,y+19),b,font=f(16),fill=ink)
save(im,4)
im,d=base('Verification','Constraints behave as designed','Valid rows are accepted; duplicate emails and orphan references are rejected.')
ver=Image.open('schema-verification.png').convert('RGB'); ver.thumbnail((1040,330)); im.paste(ver,(120,280)); save(im,5)
im,d=base('Delivery','A schema that protects the model','The repository includes the corrected ERD, executable schema, README, and verification evidence.')
d.rounded_rectangle((70,320,1210,560),radius=20,fill=ink)
for i,(a,b) in enumerate([('3 tables','users, projects, tasks'),('2 FKs','task ownership + project membership'),('3 indexes','relationship lookups covered')]):
 y=360+i*58; d.text((110,y),a,font=f(20,True),fill=mint); d.text((590,y),b,font=f(19),fill=white)
d.text((70,640),'TaskBridge · Challenge 3 · ERD translated into PostgreSQL',font=f(15,True),fill=green); save(im,6)
