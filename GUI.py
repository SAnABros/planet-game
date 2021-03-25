import pygame
class Button():
	def __init__(self, col, rect, text=''):
		self.Color = col
		self.pos = pygame.Vector2(rect[0],rect[1])
		self.text = text
		self.size = pygame.Vector2(rect[2],rect[3])
		self.scale = 1
		self.textCol = (0,0,0)
	def draw(self,sc):
		x,y=self.pos.xy
		size=pygame.Vector2(self.size.xy)
		x -= size.x/2*self.scale
		y-=size.y/2*self.scale
		size.x*=self.scale
		size.y*=self.scale
		pygame.draw.rect(sc, self.Color, [x,y, size.x,size.y])
		c = self.Color
		c = [c[0],c[1],c[2]]
		c[0] /= 2
		c[1] /= 2
		c[2] /= 2
		pygame.draw.line(sc, c, (x, int(y-2*self.scale)), (int(x+size.x-self.scale/2), int(y-2*self.scale)), int(self.scale*4))
		pygame.draw.line(sc, c, (x, int(y+size.y-1+2*self.scale)), (int(x+size.x-self.scale/2), int(y+size.y-1+2*self.scale)), int(self.scale*4))
		pygame.draw.line(sc, c, (int(x-2*self.scale), y), (int(x-2*self.scale), y+size.y), int(self.scale*4))
		pygame.draw.line(sc, c, (int(x+size.x-1+2*self.scale), y), (int(x+size.x-1+2*self.scale), y+size.y), int(self.scale*4))
		shrift = pygame.font.Font('font.ttf', int(size.y)-4, bold=True) if size.y<size.x else pygame.font.Font('font.ttf', int(size.x/2)-4, bold=True)
		render = shrift.render(str(self.text), 0, self.textCol)
		sc.blit(render, (x+size.x/2-render.get_width()/2.1,y+size.y/2-render.get_height()/2.4))
	def OnMove(self):
		x,y=self.pos.xy
		size=pygame.Vector2(self.size.xy)
		x -= size.x/2*self.scale
		y-=size.y/2*self.scale
		size.x*=self.scale
		size.y*=self.scale
		button = pygame.Rect(x,y,size.x,size.y)
		mouse = pygame.Vector2(pygame.mouse.get_pos())
		return button.colliderect(mouse.xy, (1,1))
	def OnClick(self):
		if 1 in pygame.mouse.get_pressed():
			return Button.OnMove(self)