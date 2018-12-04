#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

version = '0.0.6'


import pyglet
from random import random
from calculating import *


SIZE = 5
WSIZE = 500



class Window(pyglet.window.Window):
    def __init__(self, wsize, table):
        super().__init__(wsize,wsize)
        pyglet.gl.glClearColor(0.75,0.75,0.75,0.1)
        self.label_size = wsize//SIZE
        self.active_label = False
        self.create_table(table)
        self.win_cond = False
        pyglet.clock.schedule_interval(self.draw_all, 1/5)

    def create_table(self,table):
        self.table = table
        self.create_labels()

    def create_labels(self):
        print('CREATE LABELS:')
        self.labels = []
        self.sum_labels = []
        self.win_label = pyglet.text.Label('WINRAR IS U',\
                                      font_name='Arial', font_size=self.label_size, \
                                      x=self.width//2, y=self.height//2,anchor_x='center', \
                                      anchor_y='center',color=(0,0,0,255))
        for i in range(self.table.size):
            for j in range(self.table.size):
                x_pos = i*self.label_size
                y_pos = j*self.label_size
                marg = self.label_size/5
                I=self.table.size-j-1
                J=i
                if self.table.final_numbers[I][J] != 0:
                    val = str(self.table.final_numbers[I,J])
                else:
                    val = ""
                new_label = pyglet.text.Label(val,\
                                              font_name='Arial', font_size=self.label_size//2, \
                                              x=x_pos+marg, y=y_pos+marg,anchor_x='left', \
                                              anchor_y='bottom')
                self.labels.append(new_label)
        print('created lbls number ', len(self.labels))

    def app_sum_label(self,groups,grp,X,Y):
        new_label = pyglet.text.Label(str(groups.gr_sums[grp][0])+str(groups.gr_sums[grp][1]),\
                                      font_name='Arial', font_size=self.label_size//5, \
                                      x=X, y=Y,anchor_x='left', \
                                      anchor_y='bottom',color=(0,0,0,255))
        self.sum_labels.append(new_label)

    def create_fields(self,groups):
        print('CREATE COLOR FIELDS')
        N = 0
        self.vertex_list = []
        for grp in groups.gr_cells:
            color = tuple(random.random() for i in range(3))
            for cell in grp:
                D = self.label_size
                X = cell[1]
                Y = self.table.size - cell[0] -1
                cord00 = [X*D,Y*D]
                cord10 = [X*D+D,Y*D]
                cord11 = [X*D+D,Y*D+D]
                cord01 = [X*D,Y*D+D]
                self.vertex_list.append([cord00,cord10,cord11,cord01,color])
            self.app_sum_label(groups,N,X*D,Y*D)
            N+=1


    def draw_pol(self):
        for cell in self.vertex_list:
            pyglet.gl.glColor3f(*cell[4])
            pyglet.gl.glBegin(pyglet.gl.GL_POLYGON)
            pyglet.gl.glVertex2f(cell[0][0],cell[0][1])
            pyglet.gl.glVertex2f(cell[1][0],cell[1][1])
            pyglet.gl.glVertex2f(cell[2][0],cell[2][1])
            pyglet.gl.glVertex2f(cell[3][0],cell[3][1])
            pyglet.gl.glEnd()

    def draw_active_label(self):
        D = self.label_size
        X,Y = self.active_label[0],self.active_label[1]
        pyglet.gl.glColor3f(255,0,0)
        pyglet.gl.glLineWidth(3)
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_LOOP)
        pyglet.gl.glVertex2f(X*D,Y*D)
        pyglet.gl.glVertex2f(X*D+D,Y*D)
        pyglet.gl.glVertex2f(X*D+D,Y*D+D)
        pyglet.gl.glVertex2f(X*D,Y*D+D)
        pyglet.gl.glEnd()

    def draw_all(self,dt):
        self.clear()
        self.draw_pol()
        if self.active_label != False:
            self.draw_active_label()
        for lbl in self.labels:
            lbl.draw()
        for lbl in self.sum_labels:
            lbl.draw()
        if self.win_cond:
            self.win_label.draw()

    def wincond(self):
        print("CHECK WIN COND")
        if numpy.array_equal(self.table.final_numbers,self.table.new_numbers):
            self.win_cond = True

    def on_mouse_press(self, x, y, button, modifiers):
        I = x//self.label_size
        J = y//self.label_size
        Y = I
        X = self.table.size - J -1
        if button == pyglet.window.mouse.LEFT:
            if self.table.final_numbers[X][Y] == 0:
                self.active_label = [I,J,X,Y]
        elif button == pyglet.window.mouse.RIGHT:
            self.table.final_numbers[X][Y] = 0
            N = I*self.table.size + J
            self.labels[N].text = ""

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        elif symbol == pyglet.window.key.BACKSPACE:
            if self.active_label:
                I,J,X,Y = self.active_label[0],self.active_label[1],\
                          self.active_label[2],self.active_label[3]
                self.table.final_numbers[X][Y] = 0
                N = I*self.table.size + J
                self.labels[N].text = ""

        elif symbol == pyglet.window.key.R:
            self.win_cond = False
            table = Table(SIZE)
            grps = Groups(table)
            p1.create_table(table)
            p1.create_fields(grps)

        if self.active_label != False:
            if 48 <= int(symbol) <= 57:
                val = symbol - 48
                I = self.active_label[0]
                J = self.active_label[1]
                X = self.active_label[2]
                Y = self.active_label[3]
                N = I*self.table.size + J
                self.labels[N].text = self.labels[N].text + str(val)
                self.table.final_numbers[X][Y] = int(self.labels[N].text)
        self.wincond()

table = Table(SIZE)
grps = Groups(table)
p1 = Window(WSIZE,table)
p1.create_fields(grps)



if __name__ == '__main__':
    pyglet.app.run()
