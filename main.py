from tkinter import *
import serial
from time import sleep
from PIL import Image, ImageTk, ImageOps
import random
import keyboard
from random import *
from playsound import playsound

port = serial.Serial('COM3', baudrate=115200, timeout=0)

pre_value = 0


def get_value():
    global pre_value
    try:
        value = port.read(7)
        if 7 > len(value) > 0:
            value = str(value).replace("'", '')
            value = value.replace('b', '')
            if int(value) > 2300:
                value = "2300"
            pre_value = value
            if int(value) < 20 and int(pre_value) > 100:
                return pre_value
            return value
        else:
            return pre_value
    except:
        pass


window = Tk()
window.geometry('800x500')
window.title('Potentiometer Game')
window.resizable(False, False)

ghoul_sprite = ghoul_sprite = Image.open('ghoul idle/row-1-column-1.png')
spiked_ball_sprite = Image.open('Pixel Adventure 1/Free/Traps/Spiked Ball/Spiked Ball1.png').resize((64, 64))
spiked_ball_sprite_tk = ImageTk.PhotoImage(spiked_ball_sprite)



background_tk  = ImageTk.PhotoImage(Image.open('blue-sky-background-pixel-art-style_475147-2665.png').resize((2000, 1000)))
ground_tk = ImageTk.PhotoImage(Image.open('ground.png').resize((1000, 500)))

canvas = Canvas(window, width=800, height=500)
canvas.pack(fill='both', expand=True)
canvas.create_image(0, 0, image=background_tk)
canvas.create_image(500, 650, image=ground_tk)

player_sprite = Image.open('idle/row-1-column-1.png').resize((64, 64))
player_sprite_tk = ImageTk.PhotoImage(player_sprite)

game_over = Label(canvas, text="Game Over \rYou lasted 30 seconds")

a = 1
score = 0
seconds = 0
ennemies_spawn_rate = 10
x_player = 400
y_player = 300
x_spiked_ball = 0
y_spiked_ball = -30
was_moving_right = True
jumping = 0
spiked_ball_life_time = 0
is_game_over = False
admin_invincibility = False
invincibility = False
attacking = 0
x_ennemies = []
is_big_ennemy = False
big_ennemy_x = -100
is_big_ennemy_going_right = True
is_big_ennemy_attacking = 0
big_ennemy_life = 3
big_ennemy_dying = 0
protecting = 0
protecting_delay = 0
is_big_ennemy_taking_damage = 0
ghoul_lifetime = 0
ghoul_spawning = 0
ghoul_despawning = 0
ghoul_x = 0
ghoul_y = 0
projectile_lifetime = 0
projectile_x = 0
projectile_y = 0
is_projectile_from_right = True
projectile_sprite = Image.open('projectile.png')
big_jump_delay = 0
herobrine_lifetime = 0




while not is_game_over:
    a +=1
    print(big_jump_delay)

    #moving right
    if attacking == 0 and (keyboard.is_pressed('d')) and protecting == 0:
        x_player += 15
        player_sprite = Image.open('knight walk/row-1-column-'+str((a%16)+1)+'.png').resize((192, 192))
        was_moving_right = True

    #moving left
    elif attacking == 0 and (keyboard.is_pressed('q')) and protecting == 0:
        x_player -= 15
        player_sprite = Image.open('knight walk/row-1-column-' + str((a%16)+1) + '.png').resize((192, 192))
        was_moving_right = False

    #idle right
    elif was_moving_right:
        player_sprite = Image.open('knight idle/row-1-column-' + str((a%9)+1) + '.png').resize((192, 192))

    #idle left
    elif not was_moving_right:
        player_sprite = Image.open('knight idle/row-1-column-' + str((a%9)+1) + '.png').resize((192, 192))

    #activate attacking
    if keyboard.is_pressed('n') and attacking == 0 and y_player == 370 and protecting == 0:
        attacking = 7

    #attacking to right
    if attacking != 0 and was_moving_right:
        attacking -= 1
        player_sprite = Image.open('knight speed attack/row-1-column-' + str(7-attacking) + '.png').resize((192, 192))

    #attacking to left
    if attacking != 0 and not was_moving_right:
        attacking -= 1
        player_sprite = Image.open('knight speed attack/row-1-column-' + str(7-attacking) + '.png').resize((192, 192))


    #activate jump
    if y_player == 370 and keyboard.is_pressed('space') and attacking == 0 and protecting == 0:
        jumping = 5

    if keyboard.is_pressed('z') and attacking == 0 and protecting == 0 and big_jump_delay == 0:
        jumping += 7
        big_jump_delay = 100

    #jumping
    if jumping != 0:
        jumping -= 1
        y_player -= 45
        player_sprite = Image.open('Jump sprite.png').resize((192, 192))

    #gravity
    if y_player < 370:
        y_player += 20

    #anti glitch in the ground
    if y_player > 370:
        y_player = 370

    #invisible barrier right
    if x_player > 775:
        x_player = 775

    #invisible barrier left
    if x_player < 25:
        x_player = 25

    #spawn of spikedball
    if randint(0, 100) == 12 and spiked_ball_life_time == 0:
        y_spiked_ball = -50
        x_spiked_ball = randint(50, 750)
        spiked_ball_life_time = 26

    #fall of spikeball
    if spiked_ball_life_time != 0:
        spiked_ball_sprite   = Image.open('Pixel Adventure 1/Free/Traps/Spiked Ball/Spiked Ball'+str((a % 2)+1)+'.png').resize((128, 128))
        spiked_ball_sprite = ImageOps.mirror(spiked_ball_sprite)
        spiked_ball_sprite_tk = ImageTk.PhotoImage(spiked_ball_sprite)
        canvas.create_image(x_spiked_ball, y_spiked_ball, image=spiked_ball_sprite_tk)
        spiked_ball_life_time -= 1
        y_spiked_ball += 16.3

    #death by spikedball
    if abs(y_player-y_spiked_ball) < 60 and abs(x_player-x_spiked_ball) < 60:
        is_game_over = True

    #spawn of ennemy
    if randint(0, 68-ennemies_spawn_rate) == 10:
        x_ennemies.append(-100)



    #moving ennemies
    if x_ennemies != []:
        for i in range(len(x_ennemies)):
            x_ennemies[i] += randint(10, 17)

    for i in x_ennemies:
        # ennemy kills player

        if abs(i - x_player) < 20 and y_player > 330:
            is_game_over = True

        #despawn ennemy if too far
        if i > 900:
            del x_ennemies[x_ennemies.index(i)]



    #draw ennemies
    if x_ennemies != []:
        ennemy_sprite = Image.open('Run/row-1-column-'+str((a%12)+1)+'.png').resize((64, 64))
        ennemy_sprite_tk = ImageTk.PhotoImage(ennemy_sprite)
        for ennemy in x_ennemies:
            canvas.create_image(x_ennemies[x_ennemies.index(ennemy)], 370, image=ennemy_sprite_tk)

    #remove "shadow ennemy bug"
    if x_ennemies == []:
        ennemy_sprite = Image.open('Nothing.png').resize((64, 64))
        ennemy_sprite_tk = ImageTk.PhotoImage(ennemy_sprite)
        canvas.create_image(400, 370, image=ennemy_sprite_tk)

    #kill ennemies
    if 7 - attacking == 5:
        if was_moving_right:
            for i in x_ennemies:
                if i > x_player and i < x_player + 150:
                    del x_ennemies[x_ennemies.index(i)]
                    score += 100
            if big_ennemy_x > x_player and big_ennemy_x < x_player + 150:
                big_ennemy_life -= 1
                is_big_ennemy_taking_damage = 2


        else:
            for i in x_ennemies:
                if i < x_player and i > x_player - 150:
                    del x_ennemies[x_ennemies.index(i)]
                    score += 100
            if big_ennemy_x < x_player and big_ennemy_x > x_player - 150:
                big_ennemy_life -= 1
                is_big_ennemy_taking_damage = 2



    #spawn big ennemy
    if not is_big_ennemy and randint(0, 1000-ennemies_spawn_rate) == 0:
        is_big_ennemy = True
        if randint(1, 2) == 1:
            big_ennemy_x = -100
            is_big_ennemy_going_right = True
        else:
            big_ennemy_x = 900
            is_big_ennemy_going_right = False
        is_big_ennemy_attacking = 0
        big_ennemy_life = 5

    #move big ennemy
    if is_big_ennemy:
        if big_ennemy_dying == 0:
            if randint(1, 50) == 1:
                is_big_ennemy_going_right = not is_big_ennemy_going_right
            if big_ennemy_life < 1:
                big_ennemy_dying = 23
            if big_ennemy_x > 850:
                is_big_ennemy_going_right = False
            if big_ennemy_x < -50:
                is_big_ennemy_going_right = True

            if randint(0, 10) == 1 and is_big_ennemy_attacking == 0:
                is_big_ennemy_attacking = 12

            if is_big_ennemy_attacking != 0:
                is_big_ennemy_attacking -= 1
                if is_big_ennemy_going_right:
                    if x_player > big_ennemy_x and(x_player - big_ennemy_x) < 100 and y_player > 245 and 12-is_big_ennemy_attacking == 10:
                        is_game_over = True
                if not is_big_ennemy_going_right:
                    if x_player < big_ennemy_x and(x_player - big_ennemy_x) > -100 and y_player > 245 and 12-is_big_ennemy_attacking == 10:
                        is_game_over = True

                big_ennemy_sprite = Image.open('big ennemy attack/row-1-column-' + str(12-is_big_ennemy_attacking) + '.png').resize((200, 200))
                if not is_big_ennemy_going_right:
                    big_ennemy_x -= 30
                big_ennemy_x += 15


            if is_big_ennemy_attacking == 0:
                big_ennemy_sprite = Image.open('big ennemy run/row-1-column-' + str((a % 12) + 1) + '.png').resize((200, 200))
                if is_big_ennemy_going_right:
                    big_ennemy_x += 20
                if not is_big_ennemy_going_right:
                    big_ennemy_x -= 20
        else:
            big_ennemy_dying -= 1
            big_ennemy_sprite = Image.open('big ennemy death/row-1-column-' + str(23 - big_ennemy_dying) + '.png').resize((200, 200))
            if big_ennemy_dying == 0:
                is_big_ennemy = False
                big_ennemy_sprite = Image.open('Nothing.png').resize((200, 200))
                score += 1000


        if is_big_ennemy_taking_damage > 0:
            big_ennemy_sprite = Image.open('big ennemy hurt/row-1-column-3.png').resize((200, 200))
            is_big_ennemy_taking_damage -= 1
            sleep(0.05)

        #draw big ennemy
        if not is_big_ennemy_going_right:
            big_ennemy_sprite = ImageOps.mirror(big_ennemy_sprite)
        big_ennemy_sprite_tk = ImageTk.PhotoImage(big_ennemy_sprite)
        canvas.create_image(big_ennemy_x, 345, image=big_ennemy_sprite_tk)

    #spawning ghoul
    if ghoul_lifetime == 0 and randint(0, 100-ennemies_spawn_rate) == 1 and projectile_lifetime == 0:
        ghoul_lifetime = 60
        ghoul_spawning = 7
        ghoul_x = (50+700*randint(0, 1))
        ghoul_y = randint(260, 350)

    if ghoul_spawning > 0:
        ghoul_spawning -= 1
        ghoul_sprite = Image.open('ghoul spawn/row-1-column-'+str(7-ghoul_spawning)+'.png')


    if ghoul_lifetime > 0 and ghoul_spawning == 0 and ghoul_despawning == 0:
        ghoul_lifetime -= 1
        ghoul_sprite = Image.open('ghoul idle/row-1-column-'+str((a%4)+1)+'.png')
        if ghoul_lifetime == 0:
            ghoul_despawning = 7

    if ghoul_despawning > 0:
        ghoul_despawning -= 1
        ghoul_sprite = Image.open('ghoul despawn/row-1-column-'+str(7-ghoul_despawning)+'.png')

    if ghoul_lifetime == 0 and ghoul_despawning == 0:
        ghoul_sprite = Image.open('Nothing.png')

    if ghoul_lifetime <31 and ghoul_lifetime > 23:
        ghoul_sprite = Image.open('ghoul attack/row-1-column-'+str(31-ghoul_lifetime)+'.png')


    if ghoul_x < 500:
        ghoul_sprite = ImageOps.mirror(ghoul_sprite)
        is_projectile_from_right = False
    else:
        is_projectile_from_right = True

    if ghoul_lifetime == 26:
        projectile_y = ghoul_y
        projectile_x = ghoul_x
        projectile_lifetime = 50
        projectile_sprite = Image.open('projectile.png')
        if not is_projectile_from_right:
            projectile_sprite = ImageOps.mirror(projectile_sprite)






    if projectile_lifetime != 0:
        projectile_lifetime -= 1
        if is_projectile_from_right:
            projectile_x -= 19
        else:
            projectile_x += 19

        projectile_sprite = projectile_sprite.resize((120, 70))
        projectile_sprite_tk = ImageTk.PhotoImage(projectile_sprite)
        canvas.create_image(projectile_x, projectile_y, image=projectile_sprite_tk)




    ghoul_sprite = ghoul_sprite.resize((100, 100))
    ghoul_sprite_tk = ImageTk.PhotoImage(ghoul_sprite)
    canvas.create_image(ghoul_x, ghoul_y, image=ghoul_sprite_tk)

    if herobrine_lifetime == 0 and randint(0, 200) == 1:
        herobrine_lifetime =  1

    #protecting
    if protecting == 0 and keyboard.is_pressed('k') and protecting_delay == 0:
        protecting = (5)

    if protecting > 0:
        protecting -= 1
        invincibility = True
        player_sprite = Image.open('knight protect/row-1-column-'+str((a%3)+1)+'.png').resize((200, 200))
        if protecting == 0:
            protecting_delay = 50

    if protecting == 0:
        invincibility = False


    if not keyboard.is_pressed('k'):
        protecting = 0

    if protecting_delay > 0:
        protecting_delay -= 1

    if big_jump_delay > 0:
        big_jump_delay -= 1







    if invincibility:
        is_game_over = False

    if abs(projectile_x - x_player) < 58 and abs(projectile_y - y_player) < 50:
        is_game_over = True

    if admin_invincibility:
        is_game_over = False

    if not was_moving_right:
        player_sprite = ImageOps.mirror(player_sprite)

    player_sprite_tk = ImageTk.PhotoImage(player_sprite)
    canvas.create_image(x_player, y_player, image=player_sprite_tk)
    seconds += 0.05
    sleep(0.05)
    window.update()





print('Game Over')
canvas.create_text(400, 200, text="Game Over", font='Helvetica 40 bold')
canvas.create_text(400, 250, text="Score "+str(score), font='Helvetica 30 bold')
canvas.create_text(400, 300, text='You lasted '+str(round(seconds, 1))+' seconds', font='Helvetica 30 bold')
while y_player < 370:
    y_player += 20
y_player = 370
if was_moving_right:
    for i in range(9):
        player_sprite = Image.open('knight fall/row-1-column-' + str(i + 1) + '.png').resize((192, 192))
        player_sprite_tk = ImageTk.PhotoImage(player_sprite)
        canvas.create_image(x_player, y_player, image=player_sprite_tk)
        sleep(0.1)
        window.update()

if not was_moving_right:
    for i in range(9):
        player_sprite = Image.open('knight fall/row-1-column-' + str(i + 1) + '.png').resize((192, 192))
        player_sprite = ImageOps.mirror(player_sprite)
        player_sprite_tk = ImageTk.PhotoImage(player_sprite)
        canvas.create_image(x_player, y_player, image=player_sprite_tk)
        sleep(0.1)
        window.update()
window.mainloop()


