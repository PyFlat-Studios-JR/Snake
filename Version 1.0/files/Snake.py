from tkinter import *
import time
import random

master = Tk()
master.geometry("800x500")
master.resizable(width = 0, height=0)
w = Canvas(master)
w.pack()
w.place(x=0, y=0, width=800, height=500)
for i in range(40):
    w.create_line(i*20,0, i*20,500)
    w.create_line(0,i*20, 800,i*20)
    
class Snake_Manager():
    def __init__(self, x,y):
        self.snake = []
        self.snakecord = []
        self.length_of_snake = 1
        self.x = x
        self.y = y
        self.obj = None
        self.dir = [0,0]
        self.cool = 3
        self.gameloop = True
        self.points = 0
    def change_dir(self, x, y):
        if self.gameloop:
            self.dir = [x,y]
    def move(self):
        x = self.dir[0]
        y = self.dir[1]
        if self.x + x*20 < 0 or self.x + x*20 > 780 or self.y + y*20 < 0 or self.y + y*20 > 480:
            self.lose()
            return
        
        self.x += x*20
        self.y += y*20
        for tile in self.snakecord[:-1]:
            if tile == (self.x,self.y):
                self.lose()
        self.remove_tile()
        self.add_tile()
    def add_tile(self):
        if self.length_of_snake > len(self.snake):
            self.obj = w.create_rectangle(self.x, self.y, self.x+20, self.y+20, fill="green")
            self.snake.append(self.obj)
            self.snakecord.append((self.x,self.y))
    def remove_tile(self):
        w.delete(self.snake[0])
        del self.snake[0]
        del self.snakecord[0]
    def update(self):
        self.add_tile()
        if self.cool <= 0:
            self.cool = 3
            self.move()
        else:
            self.cool -= 1
        
            
        if self.x == Apple.x and self.y == Apple.y:
            Apple.delete()
            Apple.ini()
            self.length_of_snake += 1
            self.points += 10
    def lose(self):
        self.gameloop = False
        w.destroy()
        l = Label(master, text="LOST!", fg="red",font="Calibri 50", justify ="center")
        l.place(y=20, width=800)
        p = Label(master, text="Points: " + str(self.points), fg="green",font="Calibri 50", justify ="center")
        p.place(y=150, width=800)
    def pause(self):
        self.gameloop = not self.gameloop
    
class Apple():
    x = 0
    y = 0
    obj = None
    def ini():
        Apple.x = random.randint(0,784)
        Apple.y = random.randint(0,484)
        Apple.x = round(Apple.x, -1)
        Apple.y = round(Apple.y, -1)
        if Apple.x % 20 != 0:
            Apple.x += 10
        if Apple.y % 20 != 0:
            Apple.y += 10
        
        Apple.obj = w.create_rectangle(Apple.x,Apple.y, Apple.x+20, Apple.y+20, fill="red")
    def delete():
        w.delete(Apple.obj)
game = True
def on_closing():
    global game
    game = False
    master.quit()
    master.destroy()
s = Snake_Manager(100,100)
Apple.ini()
master.protocol("WM_DELETE_WINDOW", on_closing)   
master.bind('<space>', lambda ev:s.pause())
master.bind('w', lambda ev:s.change_dir(0,-1), s.update())
master.bind('a', lambda ev:s.change_dir(-1,0), s.update())
master.bind('s', lambda ev:s.change_dir(0,1), s.update())
master.bind('d', lambda ev:s.change_dir(1,0), s.update())

while game:
    master.update()
    master.update_idletasks()
    if s.gameloop:
        s.update()
    time.sleep(0.02)
