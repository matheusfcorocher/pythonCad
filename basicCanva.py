from tkinter import *
import numpy as np
import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import itertools

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.c = Canvas(width=400, height=400, bg="white")
        self.click_number = 0
        self.x1 = 0
        self.y1 = 0
        self.dots = []

        #métodos e funções usadas para transladar um elemento
        self._drag_data = {"x": 0, "y": 0, "item": None}
        self.c.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.c.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.c.tag_bind("token", "<B1-Motion>", self.drag)

        #objeto que grava as escalas
        self.scale = DoubleVar()
        self.scale_rotation = DoubleVar()
        self.create_interface()


    def create_interface(self):
        '''Esse método cria o canvas e a caixa de ferramentas
        '''
        # self.c.pack()
        self.c.grid(row = 0, column = 1)
        frame1 = LabelFrame(self.master, text='Operações', bg="#4d94ff", fg="white", width=100)
        frame1.grid(row = 0, column = 0, padx = 2, sticky = "nsew")
        # frame.pack(side="left")
        
        #Operações em relação aos objetos 2D
        myButton5=Button(frame1, text = "Escala", command=lambda:self.button_click(5))
        myButton5.grid(row = 0, column = 0, padx = 2, sticky = "nsew")

        myButton7=Button(frame1, text='Rotação', command=lambda:self.button_click(7))
        myButton7.grid(row = 2, column = 0, padx = 2, sticky = "nsew")
        
        myScale1=Scale(frame1, label='Fator da escala', variable = self.scale, from_=-3, to=3, orient=HORIZONTAL)
        myScale1.grid(row = 3, column = 0, padx = 2, sticky = "nsew")
        
        myScale2=Scale(frame1, label='Graus de rotação', variable = self.scale_rotation, from_=-30, to=30, orient=HORIZONTAL)
        myScale2.grid(row = 4, column = 0, padx = 2, sticky = "nsew")
        
        myButton12=Button(frame1, text = "Gerar 3D", command=lambda:self.button_click(9))
        myButton12.grid(row = 5, column = 0, sticky = "nsew", pady = 10)

        frame2 = LabelFrame(self.master, text='Ferramentas', bg="#4d94ff", fg="white", width=300)
        frame2.grid(row = 1, column = 0, columnspan = 4, sticky = "w")

        #Os botões criados no frame
        myButton0=Button(frame2, text = "Seletor", command=lambda:self.button_click(0))
        myButton0.grid(row = 0, column = 1, sticky = "nsew")
        
        myButton1=Button(frame2, text = "Linha 2D", command=lambda:self.button_click(1))
        myButton1.grid(row = 0, column = 2, sticky = "nsew")

        myButton2=Button(frame2, text='Quadrado', command=lambda:self.button_click(2))
        myButton2.grid(row = 0, column = 3, sticky = "nsew")


        myButton3=Button(frame2, text='Círculo', command=lambda:self.button_click(3))
        myButton3.grid(row = 0, column = 4, sticky = "nsew")

        myButton4=Button(frame2, text='Triângulo', command=lambda:self.button_click(4))
        myButton4.grid(row = 0, column = 5, sticky = "nsew")
    #função 
    def button_click(self, number):
        '''Esse método apenas liga qual função deve ser executada para o botão esquerdo do mouse
           <Button-1> = botão esquerdo do mouse
           <Button-2> = botão do meio do mouse
        '''
        if number == 0:
            self.c.unbind('<Button-1>')
            self.c.bind('<Button-1>', self.select_object)
        elif number == 1:
            self.c.unbind('<Button-1>')
            self.c.bind('<Button-1>', self.draw_line)
        elif number == 2:
            self.c.unbind('<Button-1>')
            self.c.bind('<Button-1>', self.draw_square)
            self.click_number = 0
        elif number == 3:
            self.c.unbind('<Button-1>')
            self.c.bind('<Button-1>', self.draw_circle)
        elif number == 4:
            self.c.unbind('<Button-1>')
            self.c.bind('<Button-1>', self.draw_triangle)
        elif number == 5:
            self.c.unbind('<Button-1>')
            self.c.bind('<Button-1>', self.apply_scale)
        elif number == 7:
            self.c.unbind('<Button-1>')
            self.c.bind('<Button-1>', self.apply_rotation)
        elif number == 9:
            self.c.unbind('<Button-1>')
            self.c.bind('<Button-1>', self.create_3D)
        else:
            self.c.delete("all")

    def select_object(self, event):
        '''
            Método para selecionar um elemento no canvas
        '''
        self._drag_data['item'] = self.c.find_closest(event.x, event.y)[0]
    
    def draw_line(self, event):
        '''
            Método para criar linha com mouse
            Apenas precisa de 2 clicks
        '''
        if self.click_number == 0:
            self.x1=event.x
            self.y1=event.y
            self.click_number += 1
        else:
            x2=event.x
            y2=event.y
            self.c.create_line(self.x1, self.y1, x2, y2, fill='black', width = 5, tags=("token",))
            self.click_number = 0
    
    def draw_square(self, event):
        '''
            Método para criar quadrado com mouse
            Apenas precisa de 4 clicks
        '''
        self.dots.append([event.x, event.y])
        self.click_number += 1
        
        if self.click_number > 3:
            self.c.create_polygon(self.dots, fill='black', tags=("token",))
            self.click_number = 0
            self.dots = []
        
    def draw_circle(self, event):
        '''
            Método para criar círculo com mouse
            Apenas precisa de 2 clicks
        '''
        if self.click_number == 0:
            self.x1=event.x
            self.y1=event.y
            self.click_number += 1
        else:
            x2=event.x
            y2=event.y
            self.c.create_oval(self.x1, self.y1, x2, y2, tags=("token",))
            self.click_number = 0
    
    def draw_triangle(self, event):
        '''
            Método para criar triângulo com mouse
            Apenas precisa de 3 clicks
        '''
        self.dots.append([event.x, event.y])
        self.click_number += 1
        
        if self.click_number > 2:
            self.c.create_polygon(self.dots, fill='black', tags=("token",))
            self.click_number = 0
            self.dots = []
    
    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.c.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.c.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def apply_scale(self, event):
        factor = int(self.scale.get())
        coords = self.c.coords(self._drag_data['item'])
        new_coords = []
        center = self.center_obj()
        for x, y in pairwise(coords):
            #Depois pega o centro do objeto e adiciona com a variação no eixo
            new_x = round((x-center[0])*(factor/10+1))
            new_y = round((y-center[1])*(factor/10+1))
            new_coords.append(round(new_x+center[0]))
            new_coords.append(round(new_y+center[1]))
        self.c.coords(self._drag_data['item'], new_coords)
    
    def apply_rotation(self, event):
        angle = int(self.scale_rotation.get())
        coords = self.c.coords(self._drag_data['item'])
        rad = angle * (math.pi/180)
        cos_val = math.cos(rad)
        sen_val = math.sin(rad)
        new_coords = []
        center = self.center_obj()
        for x, y in pairwise(coords):
            new_x = (x-center[0]) * cos_val - (y-center[1]) * sen_val
            new_y = (x-center[0]) * sen_val + (y-center[1]) * cos_val

            new_coords.append(round(new_x+center[0]))
            new_coords.append(round(new_y+center[1]))
        self.c.coords(self._drag_data['item'], new_coords)
    
    def create_3D(self, event):
        self._drag_data['item'] = self.c.find_closest(event.x, event.y)[0]
        coords = self.c.coords(self._drag_data['item'])
        normalized_coords = self.normalize_coords(coords)
        View(normalized_coords, False)
    
    def normalize_coords(self, coords):
        """
            Esse método normaliza as coordenadas de um objeto
        """
        #source: https://stackoverflow.com/questions/3862096/2d-coordinate-normalization
        new_coords = []
        xs = []
        ys = []
        for x, y in pairwise(coords):
            xs.append(x)
            ys.append(y)
        
        diagonal_length = math.sqrt((max(xs) - min(xs))*(max(xs) - min(xs)) + (max(ys) - min(ys))*(max(ys) - min(ys)))

        for x, y in pairwise(coords):
            new_x = ((x-min(xs))/diagonal_length)
            new_y = ((y-min(ys))/diagonal_length)

            new_coords.append(float(format(new_x,".1f"))*10)
            new_coords.append(float(format(new_y,".1f"))*10)

        return new_coords

    def center_obj(self):
        coords = self.c.coords(self._drag_data['item'])
        center_object = []
        x_center = 0
        y_center = 0
        for x, y in pairwise(coords):
            x_center += x
            y_center += y
        x_center = x_center/(len(coords)/2)
        y_center = y_center/(len(coords)/2)
        center_object = [x_center, y_center]
        #Calcula o centro do objeto
        return center_object

def pairwise(it):
    """A função retorna o número atual e o próximo em uma tupla"""
    it = iter(it)
    while True:
        try:
            yield next(it), next(it)
        except StopIteration:
            # no more elements in the iterator
            return
            
class View():
    def __init__(self, normalized_coords, isLine):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display,pygame.DOUBLEBUF|pygame.OPENGL)
        gluPerspective(90, (display[0]/display[1]),0.1, 50.0 )
        glTranslatef(0.0, 0.0, -5)
        self.coords = normalized_coords
        self.isLine = isLine  
        print(self.coords)
        self.loop()

    def loop(self):
        while True:
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            if(len(self.coords) == 6):
                self.tetrahedric()
            elif(len(self.coords) == 4 and self.isLine == True):
                self.line3d()
            elif(len(self.coords) == 4 and self.isLine == False):
                self.sphere()
            else:
                self.Cube()
            pygame.display.flip()
            pygame.time.wait(10)
    
    def controls(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            glTranslatef(-0.5,0,0)
        if pressed[pygame.K_RIGHT]:
            glTranslatef(0.5,0,0)
        if pressed[pygame.K_UP]:
            glTranslatef(0,1,0)
        if pressed[pygame.K_DOWN]:
            glTranslatef(0,-1,0)
        if pressed[pygame.K_a]:
            glRotatef(5, -0.5, 0, 0)
        if pressed[pygame.K_d]:
            glRotatef(5, 0.5, 0, 0)
        if pressed[pygame.K_w]:
            glRotatef(5, 0, 1, 0)
        if pressed[pygame.K_s]:
            glRotatef(5, 0, -1, 0)
        if pressed[pygame.K_r]:
            glScalef(1.1, 1.1, 1.1)
        if pressed[pygame.K_f]:
            glScalef(0.5, 0.5, 0.5)
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def Cube(self):
        verticies = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
        )

        edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7)    
            )

        colors = (
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            )

        surfaces = (
            (0,1,2,3),
            (3,2,7,6),
            (6,7,5,4),
            (4,5,1,0),
            (1,5,7,2),
            (4,0,3,6)
            )

        def solidCube():
            glBegin(GL_QUADS)
            for surface in surfaces:
                x = 0
                for vertex in surface:
                    x+=1
                    glColor3fv(colors[x])
                    glVertex3fv(verticies[vertex])
            glEnd()

        def wireCube():
            glBegin(GL_LINES)
            for edge in edges:
                for vertex in edge:
                    glVertex3fv(verticies[vertex])
            glEnd()
        
        solidCube()
        wireCube()
        self.controls()

    def tetrahedric(self):
        glBegin(GL_TRIANGLES)

        #front triangle
        glColor4f(1.0, 0.0, 0.0, 1.0)
        glVertex3f(0.0, 5.0, 0.0)
        glVertex3f( -5.0, -5.0, 0.0)
        glVertex3f( 5.0,  -5.0, 0.0)

        #right side triangle
        glColor4f(0.0, 0.0, 1.0, 1.0)
        glVertex3f( 5.0,  -5.0, 0.0)
        glVertex3f(0.0, 5.0, 0.0)
        glVertex3f( 0.0,  -5.0, -5.0)

        #left side triangle
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glVertex3f( -5.0, -5.0, 0.0)
        glVertex3f(0.0, 5.0, 0.0)
        glVertex3f( 0.0,  -5.0, -5.0)

        #bottom triangle
        glColor4f(0.0, 1.0, 0.0, 1.0)
        glVertex3f( -5.0, -5.0, 0.0)
        glVertex3f( 5.0,  -5.0, 0.0)
        glVertex3f( 0.0,  -5.0, -5.0)

        glEnd()

        self.controls()
    
    def sphere(self):
        sphere = gluNewQuadric()
        glPushMatrix()
        glColor4f(0.5, 0.2, 0.2, 1) #Put color
        gluSphere(sphere, 1.0, 32, 16) #Draw sphere

        glPopMatrix()

        self.controls()
    
    def line3d(self):
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(10, 10, 10)
        glEnd()

        self.controls()



root = Tk()
root.title('Modelador simples')
app = Application(master=root)
app.mainloop()
        