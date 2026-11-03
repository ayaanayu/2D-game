"""NEBULA DEFENDER — arcade space shooter. Install pygame, then run: python main.py"""
import math, random, sys
from pathlib import Path
import pygame

WIDTH, HEIGHT, FPS = 960, 640, 60
PLAYER_SPEED, BULLET_SPEED, PLAYER_LIVES = 440, 690, 3
ENEMY_BASE_SPEED, ENEMY_SPAWN_BASE = 105, 1.05
BOSS_SCORE, BOSS_HEALTH = 120, 42
HIGH_SCORE_FILE = Path.home() / ".nebula_defender_highscore"
WHITE=(240,248,255); CYAN=(65,225,255); BLUE=(65,125,255)
PINK=(255,80,155); GOLD=(255,205,75); DARK=(5,8,27)

def clamp(v, lo, hi): return max(lo, min(hi, v))

def glow(dst, x, y, color, radius):
    s=pygame.Surface((radius*4,radius*4),pygame.SRCALPHA); c=(radius*2,radius*2)
    for r,a in ((radius*2,18),(int(radius*1.4),35),(radius,65)):
        pygame.draw.circle(s,(*color,a),c,r)
    dst.blit(s,(int(x-c[0]),int(y-c[1])))

class Starfield:
    def __init__(self):
        self.stars=[ [random.randrange(WIDTH),random.randrange(HEIGHT),random.uniform(1,3),random.uniform(25,90)] for _ in range(110)]
    def update(self,dt):
        for s in self.stars:
            s[1]+=s[3]*dt
            if s[1]>HEIGHT: s[0]=random.randrange(WIDTH); s[1]=0
    def draw(self,dst,t):
        for x,y,r,v in self.stars:
            k=.7+.3*math.sin(t*3+x*.03)
            pygame.draw.circle(dst,(int(70*k),int(140*k),int(210*k)),(int(x),int(y)),int(r))

class Particle:
    def __init__(self,x,y,color):
        a=random.random()*math.tau; v=random.uniform(65,240)
        self.x,self.y=x,y; self.vx,self.vy=math.cos(a)*v,math.sin(a)*v
        self.life=self.maxlife=random.uniform(.3,.75); self.color=color
    def update(self,dt):
        self.x+=self.vx*dt; self.y+=self.vy*dt; self.life-=dt
        self.vx*=.98; self.vy*=.98
    def draw(self,dst):
        if self.life>0: pygame.draw.circle(dst,self.color,(int(self.x),int(self.y)),max(1,int(4*self.life/self.maxlife)))

class Explosion:
    def __init__(self,x,y,color,big=False):
        self.particles=[Particle(x,y,color) for _ in range(42 if big else 18)]
    def update(self,dt):
        for p in self.particles:p.update(dt)
        self.particles=[p for p in self.particles if p.life>0]
    def draw(self,dst):
        for p in self.particles:p.draw(dst)

class Bullet:
    def __init__(self,x,y,vx=0,vy=-BULLET_SPEED,friendly=True):
        self.x,self.y,self.vx,self.vy=x,y,vx,vy; self.friendly=friendly; self.r=5
    def update(self,dt): self.x+=self.vx*dt; self.y+=self.vy*dt
    def draw(self,dst):
        c=CYAN if self.friendly else PINK; glow(dst,self.x,self.y,c,6)
        pygame.draw.line(dst,c,(int(self.x),int(self.y+9)),(int(self.x),int(self.y-9)),4)
    def gone(self): return self.y < -30 or self.y > HEIGHT+30 or self.x < -30 or self.x > WIDTH+30

class Player:
    def __init__(self):
        self.x=WIDTH/2; self.y=HEIGHT-76; self.speed=PLAYER_SPEED
        self.lives=PLAYER_LIVES; self.cool=0; self.rapid=0; self.shield=0; self.invuln=0
    def update(self,dt,d):
        self.x=clamp(self.x+d*self.speed*dt,32,WIDTH-32)
        self.cool=max(0,self.cool-dt); self.rapid=max(0,self.rapid-dt)
        self.shield=max(0,self.shield-dt); self.invuln=max(0,self.invuln-dt)
    def shoot(self):
        if self.cool:return []
        self.cool=.12 if self.rapid else .27
        return [Bullet(self.x-12,self.y-22),Bullet(self.x+12,self.y-22)]
    def hit(self):
        if self.shield or self.invuln:return False
        self.lives-=1; self.invuln=1.35; return True
    def draw(self,dst,t):
        if self.invuln and int(t*13)%2==0:return
        if self.shield: pygame.draw.circle(dst,BLUE,(int(self.x),int(self.y)),34,2)
        flame=14+5*math.sin(t*24)
        pygame.draw.polygon(dst,(255,135,50),[(self.x-9,self.y+17),(self.x,self.y+flame+18),(self.x+9,self.y+17)])
        pts=[(self.x,self.y-25),(self.x-25,self.y+20),(self.x-8,self.y+14),(self.x,self.y+20),(self.x+8,self.y+14),(self.x+25,self.y+20)]
        pygame.draw.polygon(dst,(70,185,255),pts); pygame.draw.polygon(dst,WHITE,pts,2)

class Enemy:
    SPECS={"scout":(1.25,1,10,(255,85,130),17),"fighter":(.82,2,20,(255,155,65),22),"tank":(.48,5,35,(180,110,255),27)}
    def __init__(self,x,kind,diff):
        self.x,self.y=x,-35; speed,hp,score,color,r=self.SPECS[kind]
        self.speed=ENEMY_BASE_SPEED*speed*diff; self.hp=self.maxhp=hp
        self.score,self.color,self.r=score,color,r; self.phase=random.random()*math.tau
    def update(self,dt,t):
        self.y+=self.speed*dt; self.x+=math.sin(t*1.8+self.phase)*28*dt
    def draw(self,dst):
        x,y,r=int(self.x),int(self.y),self.r; glow(dst,x,y,self.color,r)
        pts=[(x,y+r),(x-r,y-5),(x-r//2,y-r),(x,y-r//2),(x+r//2,y-r),(x+r,y-5)]
        pygame.draw.polygon(dst,self.color,pts); pygame.draw.polygon(dst,WHITE,pts,2)
        if self.maxhp>1:
            pygame.draw.rect(dst,(45,30,55),(x-r,y-r-9,2*r,4))
            pygame.draw.rect(dst,GOLD,(x-r,y-r-9,int(2*r*self.hp/self.maxhp),4))

class PowerUp:
    COLORS={"rapid":CYAN,"shield":BLUE,"health":(100,255,145)}
    def __init__(self,x,kind): self.x,self.y,self.kind=x,-20,kind
    def update(self,dt): self.y+=125*dt
    def draw(self,dst,t):
        c=self.COLORS[self.kind]; glow(dst,self.x,self.y,c,18)
        pygame.draw.circle(dst,c,(int(self.x),int(self.y)),14,3)
        f=pygame.font.Font(None,23).render({"rapid":"R","shield":"S","health":"+"}[self.kind],True,WHITE)
        dst.blit(f,f.get_rect(center=(int(self.x),int(self.y))))
    def apply(self,p):
        if self.kind=="rapid":p.rapid=8
        elif self.kind=="shield":p.shield=7
        else:p.lives=min(PLAYER_LIVES,p.lives+1)

class Boss:
    def __init__(self):
        self.x,self.y=WIDTH/2,-90; self.hp=self.maxhp=BOSS_HEALTH
        self.direction=1; self.timer=1; self.entered=False
    def update(self,dt):
        if not self.entered:
            self.y+=85*dt
            if self.y>=115:self.y=115; self.entered=True
        else:
            self.x+=self.direction*75*dt
            if self.x<115 or self.x>WIDTH-115:self.direction*=-1
        self.timer-=dt
        if self.entered and self.timer<=0:
            self.timer=1
            return [Bullet(self.x-35,self.y+30,-55,260,False),Bullet(self.x,self.y+38,0,290,False),Bullet(self.x+35,self.y+30,55,260,False)]
        return []
    def draw(self,dst):
        x,y=int(self.x),int(self.y); glow(dst,x,y,PINK,65)
        pts=[(x-90,y-20),(x-55,y-52),(x+55,y-52),(x+90,y-20),(x+70,y+42),(x,y+58),(x-70,y+42)]
        pygame.draw.polygon(dst,(135,45,105),pts); pygame.draw.polygon(dst,PINK,pts,3)
        pygame.draw.circle(dst,WHITE,(x,y+2),17)
        pygame.draw.rect(dst,(45,25,55),(350,25,260,12))
        pygame.draw.rect(dst,PINK,(350,25,int(260*max(0,self.hp)/self.maxhp),12))

class Game:
    def __init__(self):
        pygame.init(); pygame.display.set_caption("NEBULA DEFENDER")
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
        self.canvas=pygame.Surface((WIDTH,HEIGHT)); self.clock=pygame.time.Clock()
        self.font=pygame.font.Font(None,30); self.small=pygame.font.Font(None,23)
        self.big=pygame.font.Font(None,80); self.title=pygame.font.Font(None,92)
        try:self.best=int(HIGH_SCORE_FILE.read_text())
        except (OSError,ValueError):self.best=0
        self.stars=Starfield(); self.state="menu"; self.elapsed=0; self.reset()
    def reset(self):
        self.player=Player(); self.enemies=[]; self.bullets=[]; self.powers=[]; self.effects=[]
        self.boss=None; self.boss_spawned=False; self.score=0; self.spawn=0.5; self.power_timer=10
        self.shake=0; self.left=self.right=self.fire=False
    def label(self,dst,s,font,color,xy):
        img=font.render(str(s),True,color); dst.blit(img,img.get_rect(center=xy))
    def explode(self,x,y,c,big=False):
        self.effects.append(Explosion(x,y,c,big)); self.shake=max(self.shake,.25 if big else .08)
    def update(self,dt,keys):
        d=(keys[pygame.K_RIGHT] or keys[pygame.K_d] or self.right)-(keys[pygame.K_LEFT] or keys[pygame.K_a] or self.left)
        self.player.update(dt,d)
        if keys[pygame.K_SPACE] or self.fire:self.bullets+=self.player.shoot()
        diff=1+min(1.6,self.score/300); self.spawn-=dt
        if self.spawn<=0 and self.boss is None:
            kind=random.choices(["scout","fighter","tank"],[.58,.30,.12])[0]
            self.enemies.append(Enemy(random.randint(35,WIDTH-35),kind,1+min(1.8,self.score/260)))
            self.spawn=max(.28,ENEMY_SPAWN_BASE/diff)*random.uniform(.78,1.18)
        if self.score>=BOSS_SCORE and not self.boss_spawned:self.boss=Boss(); self.boss_spawned=True
        self.power_timer-=dt
        if self.power_timer<=0:
            self.powers.append(PowerUp(random.randint(35,WIDTH-35),random.choice(["rapid","shield","health"])))
            self.power_timer=random.uniform(13,19)
        for e in self.enemies:e.update(dt,self.elapsed)
        for b in self.bullets:b.update(dt)
        for p in self.powers:p.update(dt)
        for fx in self.effects:fx.update(dt)
        for b in [b for b in self.bullets if b.friendly]:
            for e in self.enemies:
                if math.hypot(b.x-e.x,b.y-e.y)<e.r+b.r:
                    b.y=-1000; e.hp-=1
                    if e.hp<=0:
                        self.score+=e.score; self.explode(e.x,e.y,e.color); self.enemies.remove(e)
                    break
        if self.boss:
            for b in [b for b in self.bullets if b.friendly]:
                if math.hypot(b.x-self.boss.x,b.y-self.boss.y)<88:
                    b.y=-1000; self.boss.hp-=1
                    if self.boss.hp<=0:
                        self.score+=150; self.explode(self.boss.x,self.boss.y,PINK,True); self.boss=None; break
        for b in [b for b in self.bullets if not b.friendly]:
            if math.hypot(b.x-self.player.x,b.y-self.player.y)<24:
                b.y=HEIGHT+1000
                if self.player.hit():self.explode(self.player.x,self.player.y,CYAN)
        for e in self.enemies[:]:
            if e.y>HEIGHT+e.r or math.hypot(e.x-self.player.x,e.y-self.player.y)<e.r+20:
                self.enemies.remove(e)
                if self.player.hit():self.explode(self.player.x,self.player.y,PINK)
        for p in self.powers[:]:
            if math.hypot(p.x-self.player.x,p.y-self.player.y)<31:p.apply(self.player); self.powers.remove(p)
            elif p.y>HEIGHT+25:self.powers.remove(p)
        if self.boss:self.bullets+=self.boss.update(dt)
        self.bullets=[b for b in self.bullets if not b.gone()]
        self.effects=[fx for fx in self.effects if fx.particles]
        if self.player.lives<=0:
            self.state="gameover"; self.best=max(self.best,self.score)
            try:HIGH_SCORE_FILE.write_text(str(self.best))
            except OSError:pass
    def button(self,rect,text,active=False):
        pygame.draw.rect(self.canvas,(35,130,180) if active else (25,55,95),rect,border_radius=14)
        pygame.draw.rect(self.canvas,(115,220,255),rect,2,border_radius=14)
        self.label(self.canvas,text,self.font,WHITE,rect.center)
    def hud(self):
        pygame.draw.rect(self.canvas,(8,18,45),(0,0,WIDTH,48))
        self.label(self.canvas,f"SCORE {self.score:05d}",self.font,WHITE,(105,25))
        self.label(self.canvas,f"BEST {max(self.best,self.score):05d}",self.small, (150,205,235),(480,25))
        self.label(self.canvas,"♥ "*self.player.lives,self.font,(255,100,145),(875,25))
        if self.player.rapid:self.label(self.canvas,f"RAPID {self.player.rapid:.1f}s",self.small,CYAN,(110,65))
        if self.player.shield:self.label(self.canvas,f"SHIELD {self.player.shield:.1f}s",self.small,BLUE,(850,65))
    def touch_buttons(self):
        self.button(pygame.Rect(25,HEIGHT-78,78,58),"◀",self.left)
        self.button(pygame.Rect(112,HEIGHT-78,78,58),"▶",self.right)
        self.button(pygame.Rect(WIDTH-125,HEIGHT-86,100,66),"FIRE",self.fire)
    def draw_game(self):
        self.canvas.fill(DARK); self.stars.draw(self.canvas,self.elapsed)
        for p in self.powers:p.draw(self.canvas,self.elapsed)
        for b in self.bullets:b.draw(self.canvas)
        for e in self.enemies:e.draw(self.canvas)
        if self.boss:self.boss.draw(self.canvas)
        self.player.draw(self.canvas,self.elapsed)
        for fx in self.effects:fx.draw(self.canvas)
        self.hud(); self.touch_buttons()
    def overlay(self,title,sub,foot):
        shade=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); shade.fill((3,7,22,190)); self.canvas.blit(shade,(0,0))
        self.label(self.canvas,title,self.big,WHITE,(480,250)); self.label(self.canvas,sub,self.font,CYAN,(480,320))
        self.label(self.canvas,foot,self.font,GOLD,(480,395))
    def render(self):
        if self.state=="menu":
            self.canvas.fill(DARK); self.stars.draw(self.canvas,self.elapsed)
            self.label(self.canvas,"NEBULA",self.title,CYAN,(480,205)); self.label(self.canvas,"DEFENDER",self.title,WHITE,(480,282))
            self.label(self.canvas,"A DEEP-SPACE SURVIVAL SHOOTER",self.font,(150,190,225),(480,345))
            self.label(self.canvas,"Press ENTER or tap to launch",self.font,GOLD,(480,430))
            self.label(self.canvas,"Move: A/D or arrows    Shoot: SPACE    Pause: P",self.small,WHITE,(480,490))
            self.label(self.canvas,f"PERSONAL BEST {self.best:05d}",self.font,CYAN,(480,545))
        else:
            self.draw_game()
            if self.state=="paused":self.overlay("PAUSED","Take a breather, pilot.","Press P or tap to resume")
            elif self.state=="gameover":
                self.overlay("SHIP LOST",f"Final score: {self.score}","Press ENTER or tap to play again")
                self.label(self.canvas,f"PERSONAL BEST {self.best:05d}",self.font,CYAN,(480,455))
        off=(random.randint(-5,5),random.randint(-4,4)) if self.shake>0 else (0,0)
        self.shake=max(0,self.shake-.01)
        w,h=self.screen.get_size(); scaled=pygame.transform.smoothscale(self.canvas,(max(1,w),max(1,h)))
        self.screen.fill((0,0,0)); self.screen.blit(scaled,off); pygame.display.flip()
    def pointer(self,pos,pressed):
        w,h=self.screen.get_size(); x=pos[0]*WIDTH/w; y=pos[1]*HEIGHT/h
        if self.state in ("menu","gameover"):
            if pressed:self.reset(); self.state="playing"
            return
        if self.state=="paused":
            if pressed:self.state="playing"
            return
        if y>HEIGHT-100:
            if x<105:self.left=pressed
            elif x<205:self.right=pressed
            elif x>WIDTH-145:self.fire=pressed
    def run(self):
        running=True
        while running:
            dt=min(self.clock.tick(FPS)/1000,.04); self.elapsed+=dt; self.stars.update(dt)
            keys=pygame.key.get_pressed()
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:running=False
                elif ev.type==pygame.VIDEORESIZE:self.screen=pygame.display.set_mode(ev.size,pygame.RESIZABLE)
                elif ev.type==pygame.KEYDOWN:
                    if ev.key in (pygame.K_ESCAPE,pygame.K_p):
                        if self.state=="playing":self.state="paused"
                        elif self.state=="paused":self.state="playing"
                        elif ev.key==pygame.K_ESCAPE:running=False
                    elif ev.key in (pygame.K_RETURN,pygame.K_KP_ENTER) and self.state in ("menu","gameover"):
                        self.reset(); self.state="playing"
                elif ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:self.pointer(ev.pos,True)
                elif ev.type==pygame.MOUSEBUTTONUP and ev.button==1:self.pointer(ev.pos,False)
                elif ev.type in (pygame.FINGERDOWN,pygame.FINGERUP,pygame.FINGERMOTION):
                    self.pointer((ev.x*self.screen.get_width(),ev.y*self.screen.get_height()),ev.type!=pygame.FINGERUP)
            if self.state=="playing":self.update(dt,keys)
            self.render()
        pygame.quit(); sys.exit()

if __name__=="__main__":Game().run()
