import pygame
from pygame import mixer
from fighter import player
import random  


mixer.init()
mixer.init()
pygame.init()
SCREEN_WIDTH=1700
SCREEN_HEIGHT=900
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Eternity")

clock=pygame.time.Clock()
FPS=60

timer=(104,34,139)
PURPLE=(104,34,139)
RED=(255,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
#game vals

intro_count=5
last_count_update=pygame.time.get_ticks()
score=[0,0]#player scores

round_over=False
ROUND_OVER_COOLDOWN   =6000

player1_size=80
player2_size=200


player1_scale=6
player2_scale=3.5

player1_offset=[35,33]
player2_offset=[87,70]

player1_data=[player1_size,player1_scale,player1_offset]
player2_data=[player2_size,player2_scale,player2_offset]




bg1_image=pygame.image.load("assets/images/backgrounds/b6.gif").convert_alpha()
bg2_image=pygame.image.load("assets/images/backgrounds/b9.jpg").convert_alpha()
bg3_image=pygame.image.load("assets/images/backgrounds/b11.png").convert_alpha()
bg4_image=pygame.image.load("assets/images/backgrounds/b3.jpg").convert_alpha()
rock=pygame.image.load("assets/images/backgrounds/.1.png").convert_alpha()

player1_sheet=pygame.image.load("assets/images/player1/Sprites/NightBorne.png").convert_alpha()
player2_sheet=pygame.image.load("assets/images/player2/Sprites/go.png").convert_alpha()


pygame.mixer.music.load("assets/audio/bgm.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0,5000)

samurai_bgm=pygame.mixer.Sound("assets/audio/samurai.wav")
undead_bgm=pygame.mixer.Sound("assets/audio/undead.wav")
samurai_bgm.set_volume(0.5)
undead_bgm.set_volume(0.5)

victory_img=pygame.image.load("assets/icons/dc.png").convert_alpha()

rock_imgs=[]
for i in range(0,13):
	rock_imgs.append(rock.subsurface((i*200,0,200,200)))


rock_sprite=pygame.sprite.Sprite()

rock_sprite.image=rock_imgs[0]
rock_sprite.rect=rock_sprite.image.get_rect()
rock_sprite.rect.x=SCREEN_WIDTH/2.22
rock_sprite.rect.y=SCREEN_HEIGHT/1.7

rock_speed=100
last_update=pygame.time.get_ticks()
level_index=0





player1_animation_steps=[9,6,12,5,23]
player2_animation_steps=[8,8,6,4,6]

count_font=pygame.font.Font("assets/fonts/font1.ttf",80)
score_font=pygame.font.Font("assets/fonts/font2.ttf",30)


def draw_text(text,font,text_col,x,y):
	img=font.render(text,True,text_col)
	screen.blit(img,(x,y))


def draw_bg(b):
	scale_bg=pygame.transform.scale(b,(SCREEN_WIDTH,SCREEN_HEIGHT))
	screen.blit(scale_bg,(0,0))

fighter_1=	player(1,300,SCREEN_HEIGHT-250,False,player1_data,player1_sheet,player1_animation_steps,undead_bgm)
fighter_2=  player(2,SCREEN_WIDTH-350,SCREEN_HEIGHT-250,True,player2_data,player2_sheet,player2_animation_steps,samurai_bgm)

def draw_health_bar(health,x,y):
	ratio =health/100
	
	pygame.draw.rect(screen,PURPLE,(x-5,y-5,410,40))
	pygame.draw.rect(screen,RED,(x,y,400,30))
	pygame.draw.rect(screen,GREEN,(x,y,400*ratio,30))
	

run =True
i=0

while run:
	
	b=[bg1_image,bg1_image,bg1_image,bg2_image,bg4_image,bg3_image,bg4_image]
	if b[i]==bg4_image:
		b[i]=bg1_image
	clock.tick(FPS)
	draw_bg(b[i])
	now = pygame.time.get_ticks()
	if now - last_update >= rock_speed :
		last_update = now
		rock_sprite.image = rock_imgs[(rock_imgs.index(rock_sprite.image) + 1) % len(rock_imgs)]
	screen.blit(rock_sprite.image,rock_sprite.rect)
	

	draw_health_bar(fighter_1.health,20,20)
	draw_health_bar(fighter_2.health,SCREEN_WIDTH-420,20)
	draw_text("P1: "+str(score[0]),score_font,PURPLE,20,60)
	draw_text("P2: "+str(score[1]),score_font,RED,SCREEN_WIDTH-95,60)

	#update countdown
	if intro_count<=0:
		print(intro_count)

		fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter_2,round_over)
		fighter_2.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter_1,round_over)
	else:
		
		draw_text(str(intro_count),count_font,timer,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

		if(pygame.time.get_ticks()-last_count_update)>=1000:
			intro_count-=1	
			last_count_update=pygame.time.get_ticks()
			
	


	fighter_1.update()
	fighter_2.update()

	fighter_1.draw(screen)
	fighter_2.draw(screen)


	#defeat of a player
	if round_over==False:
		if fighter_1.alive==False:
			score[1]+=1
			round_over=True
			round_over_time=pygame.time.get_ticks()

		elif fighter_2.alive==False:
			score[0]+=1
			round_over=True
			round_over_time=pygame.time.get_ticks()	
			

	else:
		screen.blit(victory_img,(225,-150))	
		if i<2:
			i+=1
		
				
			
		if pygame.time.get_ticks() - round_over_time>ROUND_OVER_COOLDOWN:
				round_over=False
				intro_count=5
				i+=1
				
					
				fighter_1=	player(1,300,SCREEN_HEIGHT-250,False,player1_data,player1_sheet,player1_animation_steps,undead_bgm)
				fighter_2=  player(2,SCREEN_WIDTH-350,SCREEN_HEIGHT-250,True,player2_data,player2_sheet,player2_animation_steps,samurai_bgm)
				print(i)	

		
				

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run=False
	pygame.display.update()
	print(i)
			
	
	pygame.display.update()
    
			
pygame.quit()			