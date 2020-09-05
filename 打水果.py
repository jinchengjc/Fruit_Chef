from pygame import *
import pygame
import random


def main():
    # --- 加载变量和素材 ---
    BLACK = (0, 0, 0)
    WHITE = (235, 255, 255)
    GREEN = (0, 200, 0)
    YELLOW = (241, 255, 0)
    BLUE = (80, 255, 239)
    PURPLE = (0, 200, 255)
    RED = (237, 28, 36)
    strawberrys = {}
    BG = {}
    Health = {}
    Number = {}
    for i in range(10):
        Number[i] = transform.scale(image.load('{}.png'.format(i)), (30, 40))
    for i in range(1, 8, 1):
        BG[i] = transform.scale(image.load('BG{}.png'.format(i)), (1366, 768))
    for i in range(1, 9, 1):
        strawberrys[i] = transform.scale(image.load('strawberry{}.png'.format(i)), (50, 50))
    for i in range(6):
        Health[i] = transform.scale(image.load('health {}.png'.format(i)), (220, 44))
    score_image = transform.scale(image.load('score.png'), (130, 35))
    combo_image = transform.scale(image.load('combo.png'), (140, 35))
    shadow_image = transform.scale(image.load('strawberry1.png'), (50, 50))
    level_up_image = transform.scale(image.load('level up.png'), (170, 35))
    perfect_image = transform.scale(image.load('combo.png'), (140, 35))
    global level, FPS, score, score_count, Spawn_interval, \
        velocity, Loop_Count, game_over, clock, combo, max_combo, health, Starting

    Starting_Position_Left = [0, 683]
    Starting_Position_Right = [1366, 683]
    Starting_Position_Top = [683, 0]

    Left = 1
    Right = 2
    Top = 3

    # --- 开启准备工作 ---
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    mixer.init()
    init()
    AllEnemyElements = sprite.Group()
    clock = pygame.time.Clock()
    screen = display.set_mode([1366, 768])
    caption = display.set_caption('Super Bug Max')

    # --- 准备音乐 ---
    Cutting_Sound = pygame.mixer.Sound("score.wav")
    Hit_Sound = pygame.mixer.Sound("smb_breakblock.wav")
    Death_Sound = pygame.mixer.Sound("gameover.wav")
    Replay_Sound = pygame.mixer.Sound('1up.wav')
    Replay_Confirm_Sound = pygame.mixer.Sound('lvlup.wav')

    def Start_Menu():
        global game_over, Starting
        Starting = True
        BG = transform.scale(image.load('BG.PNG'), (1366, 768))
        screen.blit(BG, (0, 0))
        font = pygame.font.Font('freesansbold.ttf', 50)
        switch = 1
        count = 0
        greeting = font.render('Press SPACE to Play', True, WHITE)
        greetingrect = greeting.get_rect()
        greetingrect.center = (683, 460)
        while Starting:
            clock.tick(30)
            count += 1
            if count == 21:
                count = 1

                if switch == 1:
                    switch = 2
                    screen.blit(greeting, greetingrect)
                else:
                    switch = 1
                    screen.blit(BG, (0, 0))

            display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Starting = False
                    game_over = True
                    break
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Starting = False
                        game_over = True
                        break
                    if event.key == K_SPACE:
                        Replay_Confirm_Sound.play()
                        clock.tick(1.2)
                        Starting = False
                        game_over = False
                        break

    Start_Menu()

    def game():
        global level, FPS, score, score_count, Spawn_interval, \
            velocity, Loop_Count, game_over, clock, combo, max_combo, health, Starting

        combo = 0
        max_combo = 0
        health = 5
        Loop_Count = 0

        velocity = 9
        Spawn_interval = 40

        FPS = 60
        level = 1
        score = 0
        score_count = 0

        # --- game start ---

        mixer.music.load("BGM.mp3")
        mixer.music.play(loops=-1)

        class Enemy(sprite.Sprite):

            def __init__(self, direction):
                super().__init__()

                self.image = image.load('strawberry1.png')
                self.direction = direction

                # Make our top-left corner the passed-in location.
                self.rect = self.image.get_rect()
                if direction == Left:
                    self.rect.x = Starting_Position_Left[0]
                    self.rect.y = Starting_Position_Left[1]
                elif direction == Right:
                    self.rect.x = Starting_Position_Right[0]
                    self.rect.y = Starting_Position_Right[1]
                elif direction == Top:
                    self.rect.x = Starting_Position_Top[0]
                    self.rect.y = Starting_Position_Top[1]

            def update(self):
                # --- 移动 ---
                if self.direction == Left:
                    Movement_Left = [velocity, 0]
                    self.rect.x += Movement_Left[0]
                    self.rect.y += Movement_Left[1]
                elif self.direction == Right:
                    Movement_Right = [-1 * velocity, 0]
                    self.rect.x += Movement_Right[0]
                    self.rect.y += Movement_Right[1]
                elif self.direction == Top:
                    Movement_Top = [0, velocity]
                    self.rect.x += Movement_Top[0]
                    self.rect.y += Movement_Top[1]

                # --- 动图 ---
                if self.direction == Right:
                    self.image = strawberrys[8 - Loop_Count % 8]
                else:
                    self.image = strawberrys[Loop_Count % 8 + 1]

        class Target_shadow(sprite.Sprite):

            def __init__(self, direction):
                super().__init__()
                self.direction = direction
                self.image = shadow_image
                self.rect = self.image.get_rect()
                colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
                assert isinstance(colorImage, object)
                colorImage.fill(GREEN)
                self.image.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                if self.direction == Left:
                    self.rect.x = 683 - 75
                    self.rect.y = 683
                elif self.direction == Right:
                    self.rect.x = 683 + 75
                    self.rect.y = 683
                elif self.direction == Top:
                    self.rect.x = 683
                    self.rect.y = 683 - 75

        class level_up_animation(sprite.Sprite):

            def __init__(self):
                super().__init__()
                self.count = 0
                self.image = level_up_image
                self.rect = self.image.get_rect()
                self.rect.x = 1100
                self.rect.y = 50

            def update(self):
                self.count += 1
                if self.count > 20:
                    self.rect.y = 50 - 3 * (self.count - 20)

                if self.count > 70:
                    self.kill()
                    AllNoneEnemyElements.remove(self)

        # --- Final Setup before game loop ---
        target1 = Target_shadow(Left)
        target2 = Target_shadow(Right)
        target3 = Target_shadow(Top)
        AllNoneEnemyElements = sprite.Group()
        AllNoneEnemyElements.add(target1, target2, target3)
        Health_Bar = sprite.Sprite()
        Health_Bar.image = Health[5]
        Health_Bar.rect = Health_Bar.image.get_rect()
        Health_Bar.rect.x = 25
        Health_Bar.rect.y = 20
        AllNoneEnemyElements.add(Health_Bar)
        Combo = sprite.Sprite()
        Combo.image = combo_image
        Combo.rect = Combo.image.get_rect()
        Combo.rect.x = 35
        Combo.rect.y = 120
        AllNoneEnemyElements.add(Combo)
        Score = sprite.Sprite()
        Score.image = score_image
        Score.rect = Score.image.get_rect()
        Score.rect.x = 35
        Score.rect.y = 70
        AllNoneEnemyElements.add(Score)

        number1 = sprite.Sprite()
        number1.image = Number[0]
        number1.rect = number1.image.get_rect()
        number1.rect.x = 170
        number1.rect.y = 70
        AllNoneEnemyElements.add(number1)

        number2 = sprite.Sprite()
        number2.image = Number[0]
        number2.rect = number2.image.get_rect()
        number2.rect.x = 190
        number2.rect.y = 70
        AllNoneEnemyElements.add(number2)

        number3 = sprite.Sprite()
        number3.image = Number[0]
        number3.rect = number3.image.get_rect()
        number3.rect.x = 170
        number3.rect.y = 120
        AllNoneEnemyElements.add(number3)

        number4 = sprite.Sprite()
        number4.image = Number[0]
        number4.rect = number4.image.get_rect()
        number4.rect.x = 190
        number4.rect.y = 120
        AllNoneEnemyElements.add(number4)

        def toggle_background_picture():
            if level < 8:
                screen.blit(BG[level], (0, 0))
            else:
                screen.blit(BG[7], (0, 0))

        def Scoring():
            global score, score_count, level, velocity, Spawn_interval, combo
            score += 1
            combo += 1
            if score < 100:
                number2.image = Number[score % 10]
                number1.image = Number[int(score % 100 / 10)]
            if combo < 100:
                number4.image = Number[combo % 10]
                number3.image = Number[int(combo % 100 / 10)]

            score_count += 1
            if score_count == 8:
                Levelup = level_up_animation()
                AllNoneEnemyElements.add(Levelup)
                level += 1
                score_count = 0
                if Spawn_interval > 8:
                    Spawn_interval = int(Spawn_interval / 1.12)
                if velocity < 25:
                    velocity = 9 + level ** 0.4 - 1

            Cutting_Sound.play()

        def Cut_Left():
            for ene in AllEnemyElements:
                if 683 - 110 < ene.rect.x < 683 - 40 and ene.rect.y == 683:
                    AllEnemyElements.remove(ene)
                    Scoring()

        def Cut_Right():
            for ene in AllEnemyElements:
                if 683 + 110 > ene.rect.x > 683 + 40 and ene.rect.y == 683:
                    AllEnemyElements.remove(ene)
                    Scoring()

        def Cut_Up():
            for ene in AllEnemyElements:
                if 683 - 110 < ene.rect.y < 683 - 40 and ene.rect.x == 683:
                    AllEnemyElements.remove(ene)
                    Scoring()

        def Hit():
            global health, max_combo, combo
            AllEnemyElements.remove(ene)
            Hit_Sound.play()
            health -= 1
            if health >= 0:
                Health_Bar.image = Health[health]
                AllNoneEnemyElements.add(Health_Bar)
            if max_combo < combo:
                max_combo = combo
            combo = 0

        def Game_Over_Screen():
            AllNoneEnemyElements.empty()
            AllEnemyElements.empty()
            BG = transform.scale(image.load('BG.PNG'), (1366, 768))
            screen.blit(BG, (0, 0))
            font = pygame.font.Font('freesansbold.ttf', 32)
            font2 = pygame.font.Font('freesansbold.ttf', 50)
            text1 = transform.scale(image.load('game over.png'), (400, 200))
            text1Rect = text1.get_rect()
            text1Rect.center = (680, 200)

            text2 = font.render('Score: {}   Max Combo: {}'.format(score, max_combo), True, WHITE)
            text2Rect = text2.get_rect()
            text2Rect.center = (680, 330)

            text3 = font.render('Press Esc to Quit', True, WHITE)
            text3Rect = text3.get_rect()
            text3Rect.center = (680, 390)

            text4 = font2.render('OR HIT SPACE TO TRY AGAIN!!!', True, WHITE)
            text4Rect = text4.get_rect()
            text4Rect.center = (680, 470)
            center = [(680 + 7, 470 - 10), (680 - 6, 470 + 2), (680 + 1, 470 + 5), (680 - 1, 470 - 12)]

            mixer.music.stop()
            Death_Sound.play()

            screen.blit(text1, text1Rect)
            display.flip()
            clock.tick(0.5)
            screen.blit(text2, text2Rect)
            display.flip()
            clock.tick(0.85)
            screen.blit(text3, text3Rect)
            display.flip()
            clock.tick(0.5)
            screen.blit(text4, text4Rect)
            display.flip()
            Replay_Sound.play()

            waiting = True
            count = 0
            count_loop = 0
            global game_over, Starting
            while waiting:

                clock.tick(20)

                text4 = font2.render('OR HIT SPACE TO TRY AGAIN!!!', True, BLACK)
                screen.blit(text4, text4Rect)
                count_loop += 1
                count += 1
                if count_loop == 4:
                    count_loop = 0
                text4Rect.center = center[count_loop]
                text4 = font2.render('OR HIT SPACE TO TRY AGAIN!!!', True, WHITE)
                screen.blit(text4, text4Rect)
                display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        break
                    if event.type == KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            waiting = False
                            break
                        if event.key == K_SPACE and count > 20:
                            Replay_Confirm_Sound.play()
                            clock.tick(1.2)
                            Starting = False
                            game()
                            waiting = False
                            break
            game_over = True

        # --- the game loop ---
        while not game_over:

            Loop_Count += 1

            if Loop_Count % Spawn_interval == 1:
                direction = random.choice([Left, Right, Top])
                enemy = Enemy(direction)
                AllEnemyElements.add(enemy)

            # --- update projectiles and get hit ---
            for ene in AllEnemyElements:
                ene.update()
                if 1366 / 2 - 25 < ene.rect.x < 1366 / 2 + 25 and 683 - 25 < ene.rect.y < 683 + 25:
                    Hit()
            for ele in AllNoneEnemyElements:
                ele.update()
            toggle_background_picture()

            AllNoneEnemyElements.draw(screen)

            AllEnemyElements.draw(screen)

            display.flip()

            clock.tick(FPS)

            if health < 0:
                Game_Over_Screen()
                game_over = True
                break

            # --- 读手动拉闸 ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    break
                # --- 读键盘 ---
                if event.type == pygame.KEYDOWN:

                    # --- 拉闸 ---
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        break
                    # --- 读上下左右 ---
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        Cut_Left()
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        Cut_Right()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        Cut_Up()
                    if event.key == K_DOWN:
                        Game_Over_Screen()
                        game_over = True
                        break
        pygame.quit()

    game()


if __name__ == '__main__':
    main()
