### 噴射糞GAME

###引入檔案
import pygame #引入pygame
import random #引入隨機模組
import os #引入os模組讓不同環境下都可以順利放到py裡面

###基本變數
FPS = 100 #畫面更新率
白 = (255,255,255)
黑 = (0,0,0)
紅 = (255,0,0)
綠 = (0,255,0)
藍 = (0,0,255)
黃 = (255,255,0)
紫 = (148,0,211)
Monster_Energy = (106,205,12)
WIDTH = 450
HEIGHT = 700
enter_key = pygame.K_RETURN

###遊戲初始化 & 創建視窗
pygame.init() #可將pygame的東西做初始化
pygame.mixer.init() #將音樂初始化
螢幕 = pygame.display.set_mode((WIDTH,HEIGHT)) #傳入一個元組，要寫兩個值為WIDTH度與HEIGHT度
pygame.display.set_caption("噴射糞GAME") #改變視窗標題
clock = pygame.time.Clock() #控制遊戲幀率的對象

### 載入圖片
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25,25))
player_mini_img.set_colorkey(黑)
pygame.display.set_icon(player_mini_img) # 遊戲icon圖示 因為此圖變數在這個上方，所以寫在這裡
rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
enemy_img = pygame.image.load(os.path.join("img","enemy.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet01.png")).convert()
rock_imgs = [] #石頭圖片列表
for i in range(6):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())
enemy_imgs = [] #敵人圖片列表
for i in range(3):
    enemy_imgs.append(pygame.image.load(os.path.join("img",f"enemy{i}.png")).convert())
expl_anim = {} #爆炸動畫字典
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(黑)
    expl_anim['lg'].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img,(30,30)))
    player_expl_img = pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(黑)
    expl_anim['player'].append(player_expl_img)
power_imgs = {} #掉落寶物字典
power_imgs['shield'] = pygame.image.load(os.path.join('img','shield1.png')).convert()
power_imgs['gun'] = pygame.image.load(os.path.join('img','enegy.png')).convert()

### 載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
boom_sound = pygame.mixer.Sound(os.path.join("sound","boom.mp3"))
die_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound",'background01.mp3'))
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1) #數字為播放次數

### 設置音量大小
shoot_sound.set_volume(0.7)
die_sound.set_volume(0.8)
boom_sound.set_volume(0.5)
gun_sound.set_volume(0.7)
shield_sound.set_volume(0.7)
for sound in expl_sounds:
    sound.set_volume(0.6)

### 載入字體
font_name = os.path.join('taipeisans.ttf')

### 自定義函式
def draw_text(surf,text,size,x,y): #寫在什麼平面，寫的文字，文字的大小，座標ＸＹ
    font = pygame.font.Font(font_name,size) #創建文字物件(字體，文字大小)
    text_surface = font.render(text , True, Monster_Energy) #渲染出來 （文字，是否抗鋸齒，文字顏色）
    text_rect = text_surface.get_rect() #文字做定位
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect) #畫的文字，位置

def new_rock(): #隕石自動更新函式
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def new_enemy(): #敵人自動更新函式
    e = Enemy()
    all_sprites.add(e)
    enemys.add(e)

def draw_health(surf, hp, x, y): # 血條函式 (想畫的平面，血量，畫的座標ＸＹ)
    if hp < 0: # 當生命值少於零，hp則等於零
        hp = 0
    BAR_LENGTH = 100 #生命條長度
    BAR_HEIGHT = 10 #生命條高度
    fill = (hp/100)*BAR_LENGTH #把身命條填滿多少
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT) #生命條外匡 （座標寬高）
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT) #填滿生命條
    pygame.draw.rect(surf, 紫,fill_rect) # 矩形 顏色 填滿
    pygame.draw.rect(surf,白,outline_rect,2) # 矩形 顏色 填滿 外匡像素

def draw_lives (surf, lives, img, x, y): #生命數函式(畫在哪個平面，剩餘幾條命，圖片類型，ＸＹ座標)
    for i in range(lives):
        img_rect = img.get_rect() #給圖一個矩形
        img_rect.x = x + 35*i # 每個生命圖間距
        img_rect.y = y
        surf.blit(img, img_rect) # 檔案類型 畫的位置是定位的地方

def draw_init(): #遊戲開始視窗
    螢幕.blit(background_img,(-200,0)) #增加背景到遊戲開始畫面
    draw_text(螢幕,'Raiden',54,WIDTH/2, HEIGHT/4-20)
    draw_text(螢幕,'FAKE',20,WIDTH/2, HEIGHT/4+60-20)
    draw_text(螢幕,'Press ENTER to start the game.',25,WIDTH/2, HEIGHT/2-20)
    draw_text(螢幕,'by RYUU WATOKI',18,WIDTH/2, HEIGHT*3/4-20)
    draw_text(螢幕,'Move with the left and right keys, shoot with the spacebar.',14,WIDTH/2, HEIGHT-40)


    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS) #這個函式是代表每秒執行幾次,傳入的值也稱為FPS
        #取得輸入
        for event in pygame.event.get(): #回傳發生所有的事件，會回傳一個列表
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP: #增加一個鍵盤指令
                if event.key == enter_key:
                    waiting = False
                    return False

###類別(繼承sprite.Sprite)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #摳內建初始函式
        self.image = pygame.transform.scale(player_img,(50,50)) #飛機圖片用函示來調整大小
        self.image.set_colorkey(黑) #將圖片某個顏色變成透明
        self.rect = self.image.get_rect()#定位圖片
        self.radius = 20
        # pygame.draw.circle(self.image, 紅,self.rect.center,self.radius)
        self.rect.centerx = WIDTH/2 #x軸位置
        self.rect.top = HEIGHT - 120 # HEIGHT在600-80 所以方塊HEIGHT度會對齊在720的位置
        self.speedx = 7 # Ｘ軸速度參數
        self.health = 100
        self.lives = 3 #生命數量
        self.hidden = False # 一開始設置“沒有”隱藏
        self.hide_time = 0  # 一開始設置隱藏時間“0”
        self.gun = 1 #子彈等級
        self.gun_time = 0 #子彈持續時間初始

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 12000: #子彈等級持續時間
            self.gun -= 1
            self.gun_time = now
        if self.hidden and now - self.hide_time > 1200:
            self.hidden = False
            self.rect.centerx = WIDTH/2 #x軸位置
            self.rect.top = HEIGHT - 120 # HEIGHT在600-80 所以方塊HEIGHT度會對齊在720的位置
        key_pressed = pygame.key.get_pressed() #控制鍵盤的函式，表示鍵盤有沒有被按下，如果有傳回布林值true
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx #若按右鍵，往右移動
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx #若按左鍵，往左移動
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1: #子彈等級1
                bullet = Bullet(self.rect.centerx,self.rect.top) #增加子彈的函式
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun == 2: #子彈等級2
                bullet1 = Bullet(self.rect.left,self.rect.centery) #發射座標
                bullet2 = Bullet(self.rect.right,self.rect.centery) #發射座標
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            elif self.gun == 3: #子彈等級3
                bullet1 = Bullet(self.rect.left-20,self.rect.centery+10) #發射座標
                bullet2 = Bullet(self.rect.right+20,self.rect.centery+10) #發射座標
                bullet3 = Bullet(self.rect.centerx,self.rect.top) #發射座標
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()
            elif self.gun == 4: #子彈等級4
                bullet1 = Bullet(self.rect.left-45,self.rect.centery+20) #發射座標
                bullet2 = Bullet(self.rect.right+45,self.rect.centery+20) #發射座標
                bullet3 = Bullet(self.rect.left+10,self.rect.top) #發射座標
                bullet4 = Bullet(self.rect.right-10,self.rect.top) #發射座標
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                shoot_sound.play()
            elif self.gun == 5: #子彈等級5
                bullet1 = Bullet(self.rect.left-20,self.rect.centery) #發射座標
                bullet2 = Bullet(self.rect.right+20,self.rect.centery) #發射座標
                bullet3 = Bullet(self.rect.left-65,self.rect.centery+20) #發射座標
                bullet4 = Bullet(self.rect.right+65,self.rect.centery+20) #發射座標
                bullet5 = Bullet(self.rect.centerx,self.rect.centery-10) #發射座標
                bullet6 = Bullet(self.rect.left-95,self.rect.centery+40) #發射座標
                bullet7 = Bullet(self.rect.right+95,self.rect.centery+40) #發射座標
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                all_sprites.add(bullet5)
                all_sprites.add(bullet6)
                all_sprites.add(bullet7)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                bullets.add(bullet5)
                bullets.add(bullet6)
                bullets.add(bullet7)
                shoot_sound.play()
            elif self.gun == 6: #子彈等級6
                bullet1 = Bullet(self.rect.left-20,self.rect.centery) #發射座標
                bullet2 = Bullet(self.rect.right+20,self.rect.centery) #發射座標
                bullet3 = Bullet(self.rect.left-60,self.rect.centery+20) #發射座標
                bullet4 = Bullet(self.rect.right+60,self.rect.centery+20) #發射座標
                bullet5 = Bullet(self.rect.centerx,self.rect.centery-10) #發射座標
                bullet6 = Bullet(self.rect.left-100,self.rect.centery+40) #發射座標
                bullet7 = Bullet(self.rect.right+100,self.rect.centery+40) #發射座標
                bullet8 = Bullet(self.rect.left-120,self.rect.centery+60) #發射座標
                bullet9 = Bullet(self.rect.right+120,self.rect.centery+60) #發射座標
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                all_sprites.add(bullet5)
                all_sprites.add(bullet6)
                all_sprites.add(bullet7)
                all_sprites.add(bullet8)
                all_sprites.add(bullet9)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                bullets.add(bullet5)
                bullets.add(bullet6)
                bullets.add(bullet7)
                bullets.add(bullet8)
                bullets.add(bullet9)
                shoot_sound.play()
            elif self.gun >= 7: #子彈等級7
                bullet1 = Bullet(self.rect.left-10,self.rect.centery) #發射座標
                bullet2 = Bullet(self.rect.right+10,self.rect.centery) #發射座標
                bullet3 = Bullet(self.rect.left-60,self.rect.centery+20) #發射座標
                bullet4 = Bullet(self.rect.right+60,self.rect.centery+20) #發射座標
                bullet5 = Bullet(self.rect.centerx,self.rect.centery-10) #發射座標
                bullet6 = Bullet(self.rect.left-90,self.rect.centery+40) #發射座標
                bullet7 = Bullet(self.rect.right+90,self.rect.centery+40) #發射座標
                bullet8 = Bullet(self.rect.left-130,self.rect.centery+60) #發射座標
                bullet9 = Bullet(self.rect.right+130,self.rect.centery+60) #發射座標
                bullet10 = Bullet(self.rect.left-180,self.rect.centery+80) #發射座標
                bullet11 = Bullet(self.rect.right+180,self.rect.centery+80) #發射座標
                bullet12 = Bullet(self.rect.left-210,self.rect.centery+100) #發射座標
                bullet13 = Bullet(self.rect.right+210,self.rect.centery+100) #發射座標
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                all_sprites.add(bullet5)
                all_sprites.add(bullet6)
                all_sprites.add(bullet7)
                all_sprites.add(bullet8)
                all_sprites.add(bullet9)
                all_sprites.add(bullet10)
                all_sprites.add(bullet11)
                all_sprites.add(bullet12)
                all_sprites.add(bullet13)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                bullets.add(bullet5)
                bullets.add(bullet6)
                bullets.add(bullet7)
                bullets.add(bullet8)
                bullets.add(bullet9)
                bullets.add(bullet10)
                bullets.add(bullet11)
                bullets.add(bullet12)
                bullets.add(bullet13)

                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+1000)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #摳內建初始函式
        self.image_ori = random.choice(rock_imgs) #增加原始圖檔讓圖片不失真 #加入石頭群
        self.image_ori.set_colorkey(黑) #增加原始圖檔讓圖片不失真
        self.image = self.image_ori.copy() #增加原始圖檔讓圖片不失真
        self.rect = self.image.get_rect()#定位圖片
        self.radius = self.rect.width *0.8/ 2
        # pygame.draw.circle(self.image_ori, 紅,self.rect.center,self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) #隨機Ｘ
        self.rect.y = random.randrange(-3500, -1150) #隨機Ｙ
        self.speedy = random.randrange(3, 5) #隨機y速度
        self.speedx = random.randrange(-4, 4) #隨機x速度
        self.total_degree = 0 
        self.rot_degree = random.randrange(-3, 3) #隨機旋轉速度

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center #給中心點一個變數
        self.rect = self.image.get_rect() # 給與重新定位的函式
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy # 每次更新Ｙ會加二也就是會慢慢掉下來
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.image_ori = random.choice(rock_imgs) #增加原始圖檔讓圖片不失真 #加入石頭群
            self.image_ori.set_colorkey(黑) #增加原始圖檔讓圖片不失真
            self.image = self.image_ori.copy() #增加原始圖檔讓圖片不失真
            self.rect = self.image.get_rect()#定位圖片
            self.radius = self.rect.width *0.8/ 2
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) #隨機Ｘ
            self.rect.y = random.randrange(-1500, -250) #隨機Ｙ
            self.speedy = random.randrange(5, 11) #隨機y速度
            self.speedx = random.randrange(-4, 4) #隨機x速度

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #摳內建初始函式
        self.image = random.choice(enemy_imgs)
        self.image.set_colorkey(黑)
        self.rect = self.image.get_rect()#定位圖片
        self.radius = int(self.rect.width *0.8/ 2)
        # pygame.draw.circle(self.image, 紅,self.rect.center,self.radius)
        self.rect.x = random.randrange(100, WIDTH +100 - self.rect.width) #隨機Ｘ
        self.rect.y = random.randrange(-2850, -1150) #隨機Ｙ
        self.speedy = random.randrange(2, 3) #隨機y速度
        self.speedx = random.randrange(-1, 1) #隨機x速度

    def update(self):
        self.rect.y += self.speedy # 每次更新Ｙ會加二也就是會慢慢掉下來
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) #隨機Ｘ
            self.rect.y = random.randrange(-450, -150) #隨機Ｙ
            self.speedy = random.randrange(2, 7) #隨機y速度
            self.speedx = random.randrange(-1, 2) #隨機x速度

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #摳內建初始函式
        self.image = bullet_img
        self.image.set_colorkey(黑)
        self.rect = self.image.get_rect()#定位圖片
        self.rect.centerx = x #增加中心Ｘ
        self.rect.bottom = y #底部為y軸
        self.speedy = -15 #子彈速度

    def update(self):
        self.rect.y += self.speedy # 每次更新Ｙ會加二也就是會慢慢掉下來
        if self.rect.bottom < 0: #增加一個判斷 子彈超越視窗則刪除子撣
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size): #傳入爆炸的中心點, 大或小爆炸size
        pygame.sprite.Sprite.__init__(self) 
        self.size = size #先存取大或小爆炸
        self.image = expl_anim[self.size][0] #爆炸的第0張圖片
        self.rect = self.image.get_rect()#定位圖片
        self.rect.center = center #爆炸為中心
        self.frame = 0 #代表更新第幾張塗片
        self.last_update = pygame.time.get_ticks() #記錄最後一次更新時間
        self.frame_rate = 30 #至少要經過毫秒數才會更新圖片

    def update(self):
        now = pygame.time.get_ticks() #代表現在的時間
        if now - self.last_update > self.frame_rate: #現在時間減去最後一次更新時間 若大於
            self.last_update = now #把最後一次更新的時間變成現在
            self.frame += 1 #圖片加一
            if self.frame == len(expl_anim[self.size]): #若抵達最後一張
                self.kill() #把爆炸圖片刪除
            else:
                self.image = expl_anim[self.size][self.frame] # 反之把圖片更新到下一張
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self) #摳內建初始函式
        self.type = random.choice(['shield','gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(黑)
        self.rect = self.image.get_rect()#定位圖片
        self.rect.center = center #增加時設為中心
        self.speedy = 2.5 #寶物往下掉，所以是正數

    def update(self):
        self.rect.y += self.speedy # 每次更新Ｙ會加二也就是會慢慢掉下來
        if self.rect.top > HEIGHT: #大於視窗後刪除
            self.kill()

###遊戲回圈(Game loop)
show_init = True #遊戲開始畫面
running = True #遊戲進行
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemys = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        rock = Rock()
        for i in range(12): #石頭數量
            new_rock()
        enemy = Enemy()
        for i in range(7): #敵人數量
            new_enemy()
        score = 0
        random_num = int(random.randint(2,5)*10/2)

    #遊戲更新率
    clock.tick(FPS) #這個函式是代表每秒執行幾次,傳入的值也稱為FPS

    #取得輸入
    for event in pygame.event.get(): #回傳發生所有的事件，會回傳一個列表
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #增加一個鍵盤指令
            if event.key == pygame.K_SPACE:
                player.shoot()

    #更新遊戲
    all_sprites.update() #執行sprites群裡面所有物件更新

    #子彈與敵人撞擊判斷
    bullets_enemy_hits = pygame.sprite.groupcollide(enemys, bullets, True, True)  
    for hit in bullets_enemy_hits:
        random.choice(expl_sounds).play()
        score += (hit.radius)*random_num
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.92: # 0~1 掉寶率100%~0%
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_enemy()

    #飛船與石頭撞擊判斷
    player_rock_hits = pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)
    for hit in player_rock_hits:
        new_rock()
        boom_sound.play()
        player.health -= hit.radius * 0.8 #傷害值
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0 : 
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.gun = 1
            player.hide()
    if player.lives == 0 and not (death_expl.alive()):
        show_init = True

    #飛船與敵人撞擊判斷
    player_enemy_hits = pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_circle)
    for hit in player_enemy_hits:
        new_enemy()
        boom_sound.play()
        player.health -= hit.radius * 1 #傷害值
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0 : 
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()
    if player.lives == 0 and not (death_expl.alive()):
        show_init = True

    #寶物與飛船碰撞判斷
    player_power_hits = pygame.sprite.spritecollide(player, powers, True)  
    for hit in player_power_hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()

    #畫面顯示
    螢幕.fill((黑)) #函式裡面要傳入一個元組 要寫三個值，分別代表RGB
    螢幕.blit(background_img,(-200,0)) #畫上背景在螢幕的左上角
    draw_text(螢幕,"score: "+str(score),18,WIDTH/2,10)
    draw_health(螢幕,player.health,5,18)
    draw_lives(螢幕,player.lives -1 ,player_mini_img,WIDTH - 100 , 18)
    all_sprites.draw(螢幕) #把all_sprites這個群組的東西畫在螢幕
    pygame.display.update() #畫面做更新

pygame.quit()