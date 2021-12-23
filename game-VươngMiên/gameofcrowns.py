#import pygame and os
import pygame
import os
os.environ['SDL_VIDEODRIVER']='windib'
pygame.init()


# Xác định một số màu
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
LIGHTBLUE    = (   133, 214,   255)

# xác định kích thước
WIN_WIDTH = 800
WIN_HEIGHT = 550
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

# đặt kích thước cửa sổ
size = (WIN_WIDTH, WIN_HEIGHT)

# tạo lớp camera
class Camera(object):
    def __init__(self, camera_func, width, height): # gọi chức năng máy ảnh và đặt máy ảnh hình chữ nhật
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target): # vì vậy máy ảnh đó sẽ có thể di chuyển
        return target.rect.move(self.state.topleft)

    def update(self, target): # cập nhật máy ảnh hình chữ nhật để di chuyển chế độ xem cấp độ
        self.state = self.camera_func(self.state, target.rect)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # dừng cuộn ở mép trái
    l = max(-(camera.width-WIN_WIDTH), l)   # dừng cuộn ở mép phải
    t = max(-(camera.height-WIN_HEIGHT), t) # dừng cuộn ở dưới cùng
    t = min(0, t)                           # dừng cuộn ở trên cùng
    return pygame.Rect(l, t, w, h)

# tạo lớp điều
class Thing(pygame.sprite.Sprite):
    def __init__(self): # sprite để khởi tạo tất cả các sprite
        pygame.sprite.Sprite.__init__(self)

# tạo lớp ký tự
class Character(Thing):
    def __init__(self, x, y):
        # sử dụng lớp thứ để khởi tạo ký tự sprite như một thực thể riêng biệt
        Thing.__init__(self)
        # đặt tốc độ thành 0
        self.xspeed = 0
        self.yspeed = 0
        # set ký tự hình chữ nhật sẽ được tạo từ góc trên cùng bên trái của màn hình
        self.onGround = False
        self.image = pygame.Surface((25,25))
        self.image.fill(WHITE)
        self.image.convert()
        self.rect = pygame.Rect(x, y, 25, 25)

    def update(self, up, left, right, platforms):
        if up:
            # chỉ nhảy nếu ở trên mặt đất
            if self.onGround: self.yspeed -= 9

        # cập nhật ký tự để di chuyển sang trái
        if left:
            self.xspeed = -8
        # cập nhật ký tự để di chuyển sang phải
        if right:
            self.xspeed = 8

        if not self.onGround:

            self.yspeed += 0.3
            # tốc độ rơi tối đa
            if self.yspeed > 100: self.yspeed = 100

        if not(left or right):
            self.xspeed = 0

        # cập nhật tăng vị trí ký tự theo hướng x
        self.rect.left += self.xspeed

        # va chạm trục x với nền tảng
        self.collide(self.xspeed, 0, platforms)

        # cập nhật vị trí ký tự tăng dần theo hướng y
        self.rect.top += self.yspeed

        # khi trong không khí
        self.onGround = False;

        # va chạm trục y với nền tảng
        self.collide(0, self.yspeed, platforms)

    # xác định va chạm
    def collide(self, xspeed, yspeed, platforms):
        for p in platforms: # cho mỗi nền tảng thông thường
            if pygame.sprite.collide_rect(self, p):# khi một nhân vật va chạm với nền tảng, hãy chặn đường dẫn của nhân vật:
                 # nếu di chuyển sang phải, phía bên phải của mô hình ký tự tương đương với phía bên trái của nền tảng
                if xspeed > 0:
                    self.rect.right = p.rect.left
                 # nếu di chuyển sang trái, bên trái của biểu tượng ký tự tương đương với bên phải của nền tảng
                if xspeed < 0:
                    self.rect.left = p.rect.right
                 # nếu rơi xuống, cạnh dưới cùng của mô hình ký tự tương đương với mặt trên của nền tảng
                if yspeed > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yspeed = 0
                 # nếu nhảy lên, mặt trên của mô hình ký tự tương đương với mặt dưới cùng của nền tảng
                if yspeed < 0:
                    self.rect.top = p.rect.bottom

# tạo lớp nền tảng
class Platform(Thing):
    def __init__(self, x, y):
        # sử dụng lớp thứ để khởi tạo sprite nền tảng như một thực thể riêng biệt
        Thing.__init__(self)
        # đặt hình chữ nhật lên màn hình
        self.image = pygame.Surface((25, 25))
        self.image.convert()
        self.image.fill(LIGHTBLUE)
        self.rect = pygame.Rect(x, y, 25, 25)

    def update(self): # nền tảng không cập nhật
        pass

# tạo lớp tiền xu
class coinSprite(Platform):
    def __init__(self, x, y): # sử dụng lớp nền tảng để khởi tạo coin sprite như một phần của thực thể nền tảng
        Platform.__init__(self, x, y)
        # đặt và tải hình ảnh cho coinsprite ra màn hình
        self.image = pygame.Surface((25, 25))
        self.image = pygame.image.load("coin.png")
        self.image = self.image.convert()
        #để cho đồng xu sprite có thuộc tính của một hình chữ nhật
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.centerx = x # đặt x tọa độ cho tâm của sprite
        self.rect.centery = y # đặt y tọa độ cho tâm của sprite

    def update(self):
        self.rect.center = pygame.image.load() # cập nhật sprite với hình ảnh

# tạo lớp lửa
class fireSprite(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y) # sử dụng lớp nền tảng để khởi tạo fire sprite ngoài thực thể nền tảng
         #set và tải hình ảnh để mất sprite ra màn hình
        self.image = pygame.Surface((25, 25))
        self.image = pygame.image.load("fireball.png")
        self.image = self.image.convert()

        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.center = pygame.image.load()

class winSprite(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)

        self.image = pygame.Surface((25, 25))
        self.image = pygame.image.load("winsprite.png")
        self.image = self.image.convert()

        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.center = pygame.image.load()
def gameWorld(level):

    global cameraX, cameraY

    timer = pygame.time.Clock()


    up = left = right = False


    bg = pygame.Surface((25,25))
    bg.convert()
    bg.fill(BLACK)

    # tạo một nhóm sprite cho tất cả các sprite
    allSprites = pygame.sprite.Group()

    # đặt ký tự vào một biến và để nó xuất hiện ở góc trên cùng bên trái của màn hình
    character = Character(25, 25)

    # tạo danh sách trống cho nền tảng, tiền xu, lửa và chiến thắng
    platforms = []
    coins = []
    fires = []
    wins = []

    # đặt biến x và y thành 0
    x = y = 0

    # tạo danh sách trống cho cấp thiết kế
    designlevel = []

    # đọc từ tệp game đã chọn và thêm từng dòng vào danh sách để tạo vị trí cho mỗi khối
    file = open(level,"r")
    world = file.readlines()
    for line in world:
        designlevel.append(line[:-1])

    # build the level
    for row in designlevel:
        for i in row:
            if i == "P": # sinh ra một nền tảng nơi luôn có chữ P trong danh sách thiết kế, thêm vào danh sách nền tảng và thêm vào tất cả nhóm sprite
                p = Platform(x, y)
                platforms.append(p)
                allSprites.add(p)
            if i == "C": # sinh ra một đồng xu khi có chữ C trong danh sách thiết kế, thêm vào danh sách đồng xu và thêm vào tất cả nhóm sprite
                c = coinSprite(x, y)
                coins.append(c)
                allSprites.add(c)
            if i == "F": # sinh ra ngọn lửa khi có chữ F trong danh sách thiết kế, thêm vào danh sách đám cháy và thêm vào tất cả nhóm sprite
                f = fireSprite(x, y)
                fires.append(f)
                allSprites.add(f)
            x += 25 # di chuyển các khối trong cấp độ trò chơi bằng màn hình camera
        y += 25
        x = 0


    total_level_width  = len(designlevel[0])*25
    total_level_height = len(designlevel)*25


    camera = Camera(complex_camera, total_level_width, total_level_height)


    allSprites.add(character)


    global score
    score = 0
    totalcoins = 0


    pygame.mixer.init()

    coin = pygame.mixer.Sound("coinsound.wav")
    jump = pygame.mixer.Sound("jumpsound.wav")
    pygame.mixer.music.load("amazinbgmusic.mp3")


    pygame.mixer.music.play(-1,0)


    #--------------Vòng lặp chương trình chính-------------
    done = False
    while not done:



        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                quit()


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up = True

                    pygame.mixer.Sound.play(jump)
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False


        for y in range(60):
            for x in range(100):
                screen.blit(bg, (x * 25, y * 25))


        for c in coins:
            if pygame.sprite.collide_rect(character, c):

                pygame.mixer.Sound.play(coin)

                c.rect.centerx = -10
                c.rect.centery = -10


                score += 4

                print :score
                totalcoins +=1

                if totalcoins == 25:
                    w = winSprite(2450, 250)
                    wins.append(w)
                    allSprites.add(w)



        for f in fires:
            if pygame.sprite.collide_rect(character,f):
                lose()



        for w in wins:
            if pygame.sprite.collide_rect(character,w):

                win()



        camera.update(character)


        character.update(up, left, right, platforms)


        for e in allSprites:
            screen.blit(e.image, camera.apply(e))



        pygame.display.update()

        # cập nhật màn hình sau 60S
        timer.tick(60)



def lose():

    losescreen=pygame.image.load("lose.jpg").convert()
    button1=pygame.image.load("playagainbutton.png").convert()
    button1.set_colorkey(WHITE)
    button2=pygame.image.load("playagainbutton2.png").convert()
    button2.set_colorkey(WHITE)

    scoreimage=pygame.image.load("score"+str(score)+".jpg").convert()
    scoreimage.set_colorkey(WHITE)


    pygame.mixer.init()
    pygame.mixer.music.load("losesound.wav")
    playagain = pygame.mixer.Sound("instructsound.wav")


    pygame.mixer.music.play(0)


    #-----------------Vòng lặp màn hình thua cuộc------------------------------
    done=False
    while not done:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                quit()


        screen.blit(losescreen, [0,0])
        screen.blit(button1, [300, 400])
        screen.blit(scoreimage,[300, 250])

        mouse=pygame.mouse.get_pos()
        mousex=mouse[0]
        mousey=mouse[1]


        if (300<mousex<500) and (400<mousey<500):
            screen.blit(button2, [300, 400])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    pygame.mixer.Sound.play(playagain)
                    done==True
                    levelselect(screen)

        pygame.display.flip()



def win():

    winscreen=pygame.image.load("win.jpg").convert()
    button1=pygame.image.load("playagainbutton.png").convert()
    button1.set_colorkey(WHITE)
    button2=pygame.image.load("playagainbutton2.png").convert()
    button2.set_colorkey(WHITE)
    screen.blit(button1, [300, 400])
    screen.blit(winscreen, [0,0])

    scoreimage=pygame.image.load("score"+str(score)+".jpg").convert()
    scoreimage.set_colorkey(WHITE)

    pygame.mixer.init()
    pygame.mixer.music.load("winsound.mp3")
    playagain = pygame.mixer.Sound("instructsound.wav")


    pygame.mixer.music.play(0)

    #-----------------Vòng lặp màn hình chiến thắng------------------------------
    done=False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                quit()


        mouse=pygame.mouse.get_pos()
        mousex=mouse[0]
        mousey=mouse[1]

        screen.blit(button1, [100,400])
        screen.blit(scoreimage, [300, 400])


        if (100<mousex<300) and (400<mousey<500):
            screen.blit(button2, [100, 400])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    pygame.mixer.Sound.play(playagain)
                    done==True
                    levelselect(screen)

        pygame.display.flip()



def Instructionscreen(screen):

    background_position = [0, 0]
    field_image = pygame.image.load("instructionscreen.jpg").convert()
    button1=pygame.image.load("startbutton.png").convert()
    button1.set_colorkey(WHITE)
    button2=pygame.image.load("startbutton2.png").convert()
    button2.set_colorkey(WHITE)
    screen.blit(field_image, background_position)
    screen.blit(button1, [100, 400])


    pygame.mixer.init()
    instructsound = pygame.mixer.Sound("instructsound.wav")
    pygame.mixer.music.load("coolbeansbgmusic.mp3")

    pygame.mixer.music.play(-1,0)

    #-----------------Vòng lặp màn hình hướng dẫn------------------------------
    instructions=True
    while instructions==True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instructions==False
                pygame.quit()
                quit()


        screen.blit(button1, [100, 400])

        mouse=pygame.mouse.get_pos()
        mousex=mouse[0]
        mousey=mouse[1]


        if (100<mousex<300) and (400<mousey<500):
            screen.blit(button2, [100, 400])
            if event.type == pygame.MOUSEBUTTONDOWN:

                pygame.mixer.Sound.play(instructsound)
                Instructionscreen==False
                levelselect(screen)

        pygame.display.flip()



def levelselect(screen):

    background=pygame.image.load("selectscreen.jpg").convert()
    level1=pygame.image.load("level1v1.png").convert()
    level1.set_colorkey(WHITE)
    level1_1=pygame.image.load("level1v2.png").convert()
    level1_1.set_colorkey(WHITE)
    level2=pygame.image.load("level2v1.png").convert()
    level2.set_colorkey(WHITE)
    level2_2=pygame.image.load("level2v2.png").convert()
    level2_2.set_colorkey(WHITE)
    level3=pygame.image.load("level3v1.png").convert()
    level3.set_colorkey(WHITE)
    level3_2=pygame.image.load("level3v2.png").convert()
    level3_2.set_colorkey(WHITE)

    pygame.mixer.init()
    instructsound = pygame.mixer.Sound("instructsound.wav")
    pygame.mixer.music.load("coolbeansbgmusic.mp3")


    pygame.mixer.music.play(-1,0)


    #----------------- Vòng lặp màn hình lựa chọn cấp độ  -----------------
    levelselectscreen=True
    while levelselectscreen==True:
        # cho phép người dùng đóng cửa sổ và tắt trò chơi
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                levelselectscreen==False
                pygame.quit()
                quit()

        # dán hình nền và nút
        screen.blit(background, [0,0])
        screen.blit(level1, [45,400])
        screen.blit(level3, [570, 400])
        screen.blit(level2, [300, 400])

        # lây tọa độ chuột
        mouse=pygame.mouse.get_pos()
        mousex=mouse[0]
        mousey=mouse[1]

        # nếu người dùng di chuyển qua nút, hãy đánh dấu nó, nếu người dùng nhấp vào nút sẽ tải cấp độ đã chọn
        if (45<mousex<245) and (400<mousey<500):
            screen.blit(level1_1, [45,400])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    pygame.mixer.Sound.play(instructsound)

                    levelselectscreen==False
                    gameWorld("designlevel.txt")
                    # tệp level 1
        if (570<mousex<770) and (400<mousey<500):
            screen.blit(level3_2, [570,400])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    pygame.mixer.Sound.play(instructsound)
                    # vòng lặp, trò chơi cuộc gọi
                    levelselectscreen==False
                    gameWorld("designlevel3.txt")
                    # tệp level 2
        if (300<mousex<500) and (400<mousey<500):
            screen.blit(level2_2, [300,400])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # phát hiệu ứng âm thanh bắt đầu
                    pygame.mixer.Sound.play(instructsound)
                    # vòng lặp, vòng lặp trò chơi cuộc gọi
                    levelselectscreen==False
                    gameWorld("designlevel2.txt")
                    # 3 tệp
        #cập nhật màn hình
        pygame.display.flip()



# màn hình bắt đầu ban đầu
def Startscreen(screen):
    #Tải tất cả các ảnh
    background_image = pygame.image.load("coolbackground.jpg").convert()
    startbutton=pygame.image.load("startbutton.png").convert()
    startbutton.set_colorkey(WHITE)
    startbutton2=pygame.image.load("startbutton2.png").convert()
    startbutton2.set_colorkey(WHITE)
    instrucbutton=pygame.image.load("instructionbutton.png").convert()
    instrucbutton.set_colorkey(WHITE)
    instrucbutton2=pygame.image.load("instructionbutton2.png").convert()
    instrucbutton2.set_colorkey(WHITE)

    # tải hiệu ứng âm thanh
    pygame.mixer.init()
    instructsound = pygame.mixer.Sound("instructsound.wav")
    pygame.mixer.music.load("coolbeansbgmusic.mp3")

    # phát nhạc nền
    pygame.mixer.music.play(-1,0)

    #-----------------Vòng lặp màn hình khởi động------------------------------
    startscreen=True
    while startscreen==True:
        # cho phép người dùng đóng cửa sổ và tắt trò chơi
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                startscreen==False
                pygame.quit()
                quit()

        # Tải và thiết lập đồ họa.
        background_position = [0, 0]

        # ảnh nền & nút trên màn hình
        screen.blit(background_image, background_position)
        screen.blit(startbutton, [43, 395])
        screen.blit(instrucbutton, [567, 395])

        # lấy tọa độ chuột
        mouse=pygame.mouse.get_pos()
        mousex=mouse[0]
        mousey=mouse[1]

        # nếu người dùng di chuyển qua nút, hãy đánh dấu nút đó, nếu người dùng nhấp vào nút sẽ tải màn hình đã chọn
        if (43<mousex<243) and (395<mousey<495):
            screen.blit(startbutton2, [43,395])
            if event.type == pygame.MOUSEBUTTONDOWN:
                # phát hiệu ứng âm thanh bắt đầu
                pygame.mixer.Sound.play(instructsound)
                startscreen==False
                levelselect(screen)
            # vòng lặp, màn hình chọn cấp cuộc gọi
        if (567<mousex<767) and (395<mousey<495):
            screen.blit(instrucbutton2, [567,395])
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Phát âm thanh hướng dẫn
                pygame.mixer.Sound.play(instructsound)
                startscreen==False
                Instructionscreen(screen)
                # vòng lặp, màn hình hướng dẫn cuộc gọi
                # cập nhật màn hình
        pygame.display.flip()



#Đặt tên màn hình và tạo cửa sổ
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Trò Chơi Crowns-Đi lấy Vương Miện")

try:
    #Bắt đầu trò chơi
    Startscreen(screen)

except: #xử lý ngoại lệ
    pass