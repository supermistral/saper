from tkinter import *
import random
from functools import partial

root = Tk()
root.title('САПЕР')

width = 1000
height = 1500
size = 100
bomb_count = 7

root.geometry('%dx%d' %(width, height))

class Saper:
    def __init__(self):
        self.lang = IntVar()
        button1 = Radiobutton(root, text = 'Flag off', font = 'Arial 15', variable = self.lang, value = 1, width = 8, height = 4)
        button2 = Radiobutton(root, text = 'Flag on', font = 'Arial 15', variable = self.lang, value = 2, width = 8, height = 4)
        button1.place(x = 50, y = 0)
        button2.place(x = 300, y = 0)
        #print(self.lang.get())

        self.pole = {}
        self.bombs = []
        self.temp_list = []
        self.label_bomb_count = bomb_count
        self.label_bomb = Label(root, text = 'БОМБ\n%d' %self.label_bomb_count, font = 'Arial 30 bold', fg = 'orange', bg = 'white', width = 6, height = 2)
        self.label_bomb.place(x = 500, y = 0)

        for i in range(bomb_count):
            while 1:
                r1 = random.randint(0, width//size-1)
                r2 = random.randint(0, width//size-1)
                if not [r1, r2] in self.bombs:
                    self.bombs.append([r1, r2])
                    break
        for i in range(width//size):
            for j in range(width//size):
                #eval('button%d_%d = Button(root, bc = "grey")' %(i, j))
                if [i, j] in self.bombs:
                    button = Button(root, bg = "grey", width = 14, height = 7, command = lambda event = '', i = i, j = j: self.click_on_bomb(event, i, j)) #text = "%d - %d ТУТ" %(i, j), fg = 'orange', font = "Arial 30 bold", 
                else: button = Button(root, bg = "grey", width = 14, height = 7,  command = lambda event = '', i = i, j = j: self.click_without_flag(event, i, j))
                #action_with_arg = partial(action, arg)
                if [i, j] in self.bombs:
                    #eval('button%d_%d.bind("<Button-1>", )' %(i, j))
                    button.bind("<Button-1>")
                else:
                    #eval('button%d_%d.bind("<Button-1>", )' %(i, j))
                    button.bind("<Button-1>")
                #eval('self.pole[[i, j]] = [button%d_%d, 0]' %(i, j))
                self.pole[(i, j)] = [button, 0]
                button.place(x = i*100, y = j*100 + 100)
                #button.grid(row = i + 1, column = j)
                #button.pack(side = 'left')
        for i, j in self.bombs:
            for xpos in range(i - 1, i + 2):
                for ypos in range(j - 1, j + 2):
                    if not ([xpos, ypos] in self.bombs) and ((xpos, ypos) in list(self.pole.keys())):
                        self.pole[xpos, ypos][1] += 1
        #print(self.pole)
                    
    def click_without_flag(self, event, i, j):
        #print(i, j, end = '\n\n')
        if self.lang.get() == 1 or self.lang.get() == 0:
            if self.pole[(i, j)][1] != 0:
                self.change_config(i, j)
            else:
                for one in range(i-1, i+2):
                    for two in range(j-1, j+2):
                        if (one, two) in self.pole.keys() and (one, two) != (i, j):
                            #print(one, two)
                            self.change_config(one, two)
                            if self.pole[(one, two)][1] == 0 and not ((one, two) in self.temp_list):
                                self.temp_list.append((one, two))
                                #print(self.temp_list)
                                self.click_without_flag('nothing', one, two)
        elif self.pole[(i, j)][0]['text'] == 'Ф':
            self.pole[(i, j)][0].config(text = '', bg = 'grey')
            self.label_bomb_count += 1
            self.label_bomb.config(text = 'БОМБ\n%d' %self.label_bomb_count)
            
        else:
            self.pole[(i, j)][0].config(text = 'Ф', bg = 'white')
            self.label_bomb_count -= 1
            self.label_bomb.config(text = 'БОМБ\n%d' %self.label_bomb_count)

    def change_config(self, i, j):
        if self.lang.get() == 1 or self.lang.get() == 0:
            self.pole[(i, j)][0].config(text = '%d' %self.pole[(i, j)][1], font = 'Arial 43 bold', bg = 'white', width = 3, height = 1)
            if self.pole[(i, j)][1] == 0:
                self.pole[(i, j)][0].config(text = '')
            elif self.pole[(i, j)][1] == 1:
                self.pole[(i, j)][0].config(fg = 'blue')
            elif self.pole[(i, j)][1] == 2:
                self.pole[(i, j)][0].config(fg = 'green')
            elif self.pole[(i, j)][1] == 3:
                self.pole[(i, j)][0].config(fg = 'red')
        elif self.pole[(i, j)][0]['text'] == 'Ф':
            self.pole[(i, j)][0].config(text = '', bg = 'grey')
            self.label_bomb_count += 1
            self.label_bomb.config(text = 'БОМБ\n%d' %self.label_bomb_count)
        else:
            self.pole[(i, j)][0].config(text = 'Ф', bg = 'white')
            self.label_bomb_count -= 1
            self.label_bomb.config(text = 'БОМБ\n%d' %self.label_bomb_count)

    def click_on_bomb(self, event, i, j):
        global IN_GAME
        if self.lang.get() == 1 or self.lang.get() == 0:
            IN_GAME = False
            self.pole[(i, j)][0].config(text = "GG", bg = 'red')
        elif self.pole[(i, j)][0]['text'] == 'Ф':
            self.pole[(i, j)][0].config(text = '', bg = 'grey')
            self.label_bomb_count += 1
            self.label_bomb.config(text = 'БОМБ\n%d' %self.label_bomb_count)
        else:
            self.pole[(i, j)][0].config(text = 'Ф', bg = 'white')
            self.label_bomb_count -= 1
            self.label_bomb.config(text = 'БОМБ\n%d' %self.label_bomb_count)

            
def create_start_text():
    global start_text
    start_text = Label(root, text = 'START GAME', font = 'Arial 40', width = 20, height = 5, fg = 'red', bg = 'black')
    start_text.bind("<Button-1>", start_game)
    start_text.place(x = 0, y = 100)
    #return start_text

def start_game(event):
    global game
    game = Saper()
    if start_text:
        start_text.destroy()
    main()
    
def create_reset_label():
    global reset_label
    reset_label = Label(root, text = 'РЕСТАРТ', font = 'Arial 50', width = 8, height = 2, fg = 'red', bg = 'white')
    reset_label.bind('<Button-1>', restart_game)
    reset_label.place(x = 700, y = 0)
    for i, j in game.bombs:
        if game.pole[(i, j)][0]['text'] != 'GG':
            game.pole[(i, j)][0].config(bg = 'black')
    for i in game.pole.values():
        print(i)
        i[0].config(state = 'disabled')

def restart_game(event):
    global IN_GAME
    IN_GAME = True
    if reset_label:
        reset_label.destroy()
    start_game('nothing')

def main():
    #print(game)
    if IN_GAME and game.label_bomb_count != 0:
        root.after(200, main)
    else:
        create_reset_label()

#game = None
IN_GAME = True
#game = Saper()
create_start_text()

    
root.mainloop()
