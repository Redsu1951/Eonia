import pygame
class player():
  def __init__(self,player,x,y,flip,data,sprite_sheet,animation_steps,sound):
    self.player=player
    self.size=data[0]

    self.image_scale=data[1]
    self.offset=data[2]
    self.flip=flip
    self.animation_list=self.load_images(sprite_sheet,animation_steps)
    self.action=0#0:idle(0) #1:run(1) #2:jump(part of attack)(2) #3:attack1(2) #4: attack2(2) #5:hit(3) #6:death(4)
    self.frame_index=0
    self.image=self.animation_list[self.action][self.frame_index]
    self.update_time=pygame.time.get_ticks()
    self.rect=pygame.Rect((x,y,80,180))
    self.vel_y=0 
    self.running=False
    self.jump=False
    self.attacking=False
    self.attack_type=0
    self.attack_cooldown=0
    self.hit=False
    self.sound=sound
    self.health=100
    self.alive=True
    
    
  

  def load_images(self,sprite_sheet,animation_steps):
    animation_list=[]
    for y,animation in enumerate(animation_steps):
      temp_img_list=[]
      for i in range(animation):
        temp_img=sprite_sheet.subsurface(i*self.size,y*self.size,self.size,self.size) 
        temp_img_list.append(pygame.transform.scale(temp_img,(self.size*self.image_scale,self.size*self.image_scale)))
      animation_list.append(temp_img_list)   
    
    return animation_list  
       

  
  def move(self,screen_width,screen_height,surface,target,round_over):
    SPEED=10
    GRAVITY=2
    dx=0
    dy=0
    self.running=False
    self.attack_type=0

    key=pygame.key.get_pressed()

    if self.attacking==False and self.alive==True and round_over==False:

      if self.player==1:
        if key[pygame.K_a]:
          dx=-SPEED

          self.running=True
        if key[pygame.K_d]:
          dx=SPEED 
          self.running=True

        if key[pygame.K_w] and self.jump==False:
          self.vel_y=-40
          self.jump=True

      #attack  
        if key[pygame.K_r] or key[pygame.K_t]:


          self.attack(target)
          if key[pygame.K_r]:
            self.attack_type=1

          if key[pygame.K_t]:
            self.attack_type=2  


      if self.player==2:
        if key[pygame.K_LEFT]:
          dx=-SPEED

          self.running=True
        if key[pygame.K_RIGHT]:
          dx=SPEED 
          self.running=True

        if key[pygame.K_UP] and self.jump==False:
          self.vel_y=-40
          self.jump=True

      #attack  
        if key[pygame.K_KP1] or key[pygame.K_KP2]:


          self.attack(target)
          if key[pygame.K_KP1]:
            self.attack_type=1

          if key[pygame.K_KP2]:
            self.attack_type=2       


    self.vel_y+=GRAVITY  
    dy+=self.vel_y  
      
    if self.rect.left+dx<20:
      dx=20-self.rect.left

    if self.rect.right+dx>screen_width-20:
      dx=screen_width-20-self.rect.right  

    if self.rect.bottom +dy>screen_height-70:
      self.vel_y=0 
      self.jump=False
      dy=screen_height-70-self.rect.bottom

    #face eachother
    if target.rect.centerx>self.rect.centerx and self.alive==True:
      self.flip=False
    else:
      self.flip=True    

    #attack cooldown
    if self.attack_cooldown>0:
      self.attack_cooldown-=1  

    #updating their positions
      
    self.rect.x+=dx   
    self.rect.y+=dy

  def update(self):
    

    if self.health<=0:
      self.health = 0
      self.alive=False
      self.update_action(4)
    elif self.hit==True:
      self.update_action(3)#5:hit
      
    elif self.attacking ==True:

      if self.attack_type==1:
        self.update_action(2)#attack1

      elif self.attack_type==2:
        self.update_action(2)#attack2

    elif self.jump==True:
      self.update_action(2)

    elif self.running==True:
      self.update_action(1)

    else:
      self.update_action(0)  

    animaation_cooldown=50

    self.image=self.animation_list[self.action][self.frame_index]
    
    if pygame.time.get_ticks() -self.update_time > animaation_cooldown:
      self.frame_index+=1
      self.update_time=pygame.time.get_ticks()

    if self.frame_index >= len(self.animation_list[self.action]):

      if self.alive ==False:
        self.frame_index = len(self.animation_list[self.action])-1
      else:  

        self.frame_index=0

      #checking if attack done
      if self.action==2 :
        self.attacking=False
        self.attack_cooldown=20
      #damage taken
      if self.action==3:
        self.hit=False

        self.attacking=False
        self.attack_cooldown=20  
 

  def attack(self,target):
    if self.attack_cooldown==0:

      self.sound.play()
      self.attacking=True
      attacking_rect=pygame.Rect(self.rect.centerx-(3*self.rect.width*self.flip),self.rect.y, 2*self.rect.width,self.rect.height)
      

      if attacking_rect.colliderect(target.rect):
        print("Damaged")
        target.health-=5
        target.hit=True
      

  def update_action(self,new_action):

    if new_action != self.action:
      self.action=new_action

      self.frame_index=0
      self.update_time=pygame.time.get_ticks()


  def draw(self,surface):
    img=pygame.transform.flip(self.image,self.flip,False)
    
    surface.blit(img,(self.rect.x-(self.offset[0]*self.image_scale),self.rect.y-(self.offset[1]*self.image_scale)))