#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import random
import numpy

PROB_NUMB_VIS = 0.5

PROB_DEV = 0.5
PROB_MIN = 0.5
PROB_MULT = 0.3

#GRPS PROBS:
PROB_1 = 0.5
PROB_2 = 0.2

class Table(object):
    def __init__(self,size):
        self.size = size
        self.create_table()
        self.create_fin_numbers()

    def create_table(self):
        self.numbers = numpy.zeros([self.size,self.size],dtype=numpy.int16)
        for i in range(self.size):
            for j in range(self.size):
                self.numbers[i,j]=-1
        self.method5()
        self.randomize_raws()

    def method5(self):
        print('GENERATE NUMBERS:')
        rand_str = [i for i in range(self.size)]
        random.shuffle(rand_str)
        print('starting string: ', rand_str)
        for i in range(self.size):
            for n in range(len(rand_str)):
                rand_str[n]=(rand_str[n])%self.size+1
            for j in range(self.size):
                choice = rand_str[j]
                self.numbers[i,j] = choice
            
            print('new string: ', rand_str)
        print('table: ')
        print(self.numbers)

    def randomize_raws(self):
        print('RANDOMIZE RAWS:')
        rand_str = [i for i in range(self.size)]
        random.shuffle(rand_str)
        print('rand seed: ', rand_str)
        self.new_numbers = numpy.zeros([self.size,self.size],dtype=numpy.int16)
        i = 0
        for el in rand_str:
            for j in range(self.size):
                self.new_numbers[el][j] = self.numbers[i][j]
            i+=1
        print('final table: ')
        print(self.new_numbers)
    
    def create_fin_numbers(self):
        self.final_numbers = numpy.zeros([self.size,self.size],dtype=numpy.int16)
        for i in range(self.size):
            for j in range(self.size):
                if random.random() < PROB_NUMB_VIS:
                    self.final_numbers[i][j] = self.new_numbers[i][j]
                else:
                    self.final_numbers[i][j] = 0

class Groups(object):
    def __init__(self,table):
        print('CREATE GROUPS:')
        self.table = table
        self.grid = numpy.zeros([table.size,table.size],dtype=numpy.int16)
        self.size = table.size
        self.groups = []
        self.main_cells = []
        self.create_groups()
        print('Groups:')
        print(self.grid)
        self.create_sum_groups()

    def create_groups(self):
        group_num = 1
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    self.grid[i][j] = group_num
                    self.groups.append(group_num)
                    self.main_cells.append((i,j))
                    if i<self.table.size-1:
                        if random.random() < PROB_1:
                            if self.grid[i+1][j]==0:
                                self.grid[i+1][j]=group_num
                                if j < self.table.size-1 and i < self.table.size-1:
                                    if random.random() < PROB_2:
                                        if self.grid[i+1][j+1]==0:
                                            self.grid[i+1][j+1] = group_num
                                if i < self.table.size-2:
                                    if random.random() < PROB_1:
                                        if self.grid[i+2][j]==0:
                                            self.grid[i+2][j] = group_num
                    if j<self.table.size-1:
                        if random.random() < PROB_1:
                            if self.grid[i][j+1]==0:
                                self.grid[i][j+1]=group_num
                                if j < self.table.size-1 and i < self.table.size-1:
                                    if random.random() < PROB_2:
                                        if self.grid[i+1][j+1]==0:
                                            self.grid[i+1][j+1] = group_num
                                if j < self.table.size-2:
                                    if random.random() < PROB_1:
                                        if self.grid[i][j+2]==0:
                                            self.grid[i][j+2] = group_num
                    group_num+=1

    def create_sum_groups(self):
        print('CREATE SUM GROUPS')
        gr_numbers = [[] for i in range(len(self.groups))]
        gr_cells = [[] for i in range(len(self.groups))]
        for i in range(self.size):
            for j in range(self.size):
                gr_numbers[self.grid[i][j]-1].append(self.table.new_numbers[i][j])
                gr_cells[self.grid[i][j]-1].append([i,j])
        gr_sums = []
        n = 1
        for grp in gr_numbers:
            if len(grp) == 1:
                gr_sums.append(["",""])
            else:
                if devide_group(grp):
                    gr_sums.append(["/",devide_group(grp)])
                elif min_group(grp):
                    gr_sums.append(["-",min_group(grp)])
                elif random.random() < PROB_MULT:
                    gr_sums.append(["x",mult_group(grp)])
                else:
                    gr_sums.append(["+",sum_group(grp)])
                n+=1
        self.gr_sums = gr_sums
        self.gr_cells = gr_cells
    
def sum_group(group):
    summ = 0
    for N in group:
        summ+=N
    return summ

def mult_group(group):
    mult = 1
    for el in group:
        mult*=el
    return mult

def min_group(group):
    l = list(group)
    gr_max = max(l)
    l.remove(gr_max)
    for el in l:
        gr_max -= el
    if gr_max >=0:
        return gr_max
    else:
        return False

def devide_group(group):
    l = list(group)
    a1 = max(l)
    l.remove(a1)
    mult = 1
    for el in l:
        mult *= el
    if a1%mult == 0:
        return a1//mult
    else:
        return False
    

