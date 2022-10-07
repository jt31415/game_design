import pygame, math

def initialize():
  global w, game_space
  w=pygame.display.get_surface()
  game_space={'background': [255,255,255], 'sprites': []}

class Vector:
  def __init__(self,x,y):
    self.x=x
    self.y=y
  def move(self,dx,dy):
    self.x+=dx
    self.y+=dy
  def move_to_new(self,new_x,new_y):
    self.x=new_x
    self.y=new_y
  def copy(self):
    return V(self.x, self.y)
  def normalized(self, units=1):
      d=dist(self,V(0,0))
      if d:
          return V(self.x/d * units, self.y/d * units)
      else:
          return V(0,0)
    
  @property
  def aslist(self):
    return [self.x,self.y]
    
V=Vector

class Camera:
  def __init__(self,pos=[0,0],targets=None,type=0,padding=10):
    self.pos=pos
    self.goto=self.pos
    self.targets=targets
    self.type=type
    self.padding=padding

  def draw(self):
    raw_min_x=min([target.rect.left for target in self.targets])
    raw_min_y=min([target.rect.top for target in self.targets])
    raw_min=V(raw_min_x, raw_min_y)
    real_min=raw_min.copy()
    real_min.move(-self.padding, -self.padding)

    raw_max_x=min([target.rect.right for target in self.targets])
    raw_max_y=min([target.rect.bottom for target in self.targets])
    raw_max=V(raw_max_x, raw_max_y)
    real_max=raw_max.copy()
    real_max.move(self.padding, self.padding)

  def snap(self):
    self.pos=self.goto
    
  def update_pos(self):
    pass

class Button:
  def __init__(self,pos,text,onpress=lambda: print('default'),style=0,outline=False,outline_c=(0,0,0)):
    self.pos=pos
    self.text=text
    self.onpress=onpress
    self.style=style
    self.outline=outline
    self.outline_c=outline_c
  def draw(self):
    pass

class Map:
  def __init__(self,wi,he):
    self.size=[wi,he]
    self.m=[[0 for i in range(he)] for i in range(wi)]
  def set(self,pos,item):
    self.m[pos.x][pos.y]=item
  def get(self,pos):
    return self.m[pos.x][pos.y]
  def find(self,item):
    for y in range(self.size[1]):
      for x in range(self.size[0]):
        if self.get(V(x,y))==item:
          return V(x,y)
    return None
  def multifind(self,item):
    final=[]
    for y in range(self.size[1]):
      for x in range(self.size[0]):
        if self.get(V(x,y))==item:
          final.append(V(x,y))
    return final
  def visualize(self):
    for y in range(self.size[1]):
      for x in range(self.size[0]):
        print(self.get(V(x,y)),'\t',end='')
      print()
  def fill(self,item):
    self.m=[[item for i in range(self.size[1])] for i in range(size[0])]
  def dist(self,i1,i2):
    fi1=self.multifind(i1)
    fi2=self.multifind(i2)
    best=100
    if not fi1 or not fi2:
      return None
    else:
      for i in fi1:
        for j in fi2:
          calc=math.sqrt( abs(i.x-j.x)**2 + abs(i.y-j.y)**2 )
          if calc<best:
            best=calc
    return best

def darken_rect(rect):
  rect=pygame.Rect(rect)

def dist(p1,p2):
  return math.sqrt((p2.x-p1.x)**2 + (p2.y-p1.y)**2)

def delta(p1,p2):
  return V(p2.x - p1.x, p2.y - p1.y)

def add(p1,p2):
    return V(p1.x + p2.x, p1.y + p2.y)

def multiply(p1,p2):
    return V(p1.x * p2.x, p1.y * p2.y)

def divide(p1,p2):
    return V(p1.x / p2.x, p1.y / p2.y)

def between(p1,p2,fract=0.5):
  d=delta(p1, p2)
  return V(p1 + fract * d.x, p2 + fract * d.y)

def delta_to_degrees(dir):
  return (180 / math.pi) * -math.atan2(dir.y, dir.x)
    
# get relative position from a point in the game (the center is (0,0))
# basically an in-game point to an on-screen point
def get_rel(point, center, window_size):
    temp=delta(center, point)
    temp.x+=int(window_size[0]/2+0.5)
    temp.y+=int(window_size[1]/2+0.5)
    return temp

#from pygame wiki
def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2
    fontHeight = font.size('Jy')[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]
      
    return text

def centertext(font, t, color, surf, rect, aa=False, center='c'):
  s=font.render(t,aa,color)
  size=s.get_size()
  rect=pygame.Rect(rect)
  w,h=rect.size
  l,top=rect.left,rect.top
  if center=='c': # aligned to the center of the image
    pos=(l+w//2-size[0]//2,top+h//2-size[1]//2)
  elif center=='t': # aligned to the top center of the image
    pos=(l+w//2-size[0]//2,top+h//2)
  elif center=='b': # aligned to the bottom center of the image
    pos=(l+w//2-size[0]//2,top+h//2-size[1])
  else:
    print("unknown center argument")
  surf.blit(s,pos)