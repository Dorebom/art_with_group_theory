from matplotlib import colors
import matplotlib
from numpy.random import *
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

class SingleLine():
    def __init__(self):
        self.init_line()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal', adjustable='box')

    def init_line(self, num=12):
        self.halt_signal = False
        self.old_num = 3
        self.current_x = 0.0
        self.current_y = 0.0
        self.seq_x = np.array(deepcopy(self.current_x))
        self.seq_y = np.array(deepcopy(self.current_y))
        self.move_distance = randint(1,100)
        self.num = num
        self.line_size = randint(1,10) * 0.1

    def update(self):
        new_num = self.generate_num()
        check_num = (new_num + self.old_num) % self.num 
        if check_num == 0:
            self.halt_signal = True
        else:
            self.current_x += np.sin(2.0 * np.pi * check_num / self.num)
            self.current_y += np.cos(2.0 * np.pi * check_num / self.num)
            self.store_pos(self.current_x, self.current_y)

        self.old_num = check_num

    def generate_num(self):
        val = randint(self.num)
        return val

    def store_pos(self, x, y):
        self.seq_x = np.append(self.seq_x, x) 
        self.seq_y = np.append(self.seq_y, y) 

    def generate_line(self, num=12):
        self.init_line(num)

        self.center_x = randint(1, 100)
        self.center_y = randint(1, 100)

        while(self.halt_signal == False):
            self.update()

        move_time = self.seq_x.size
        loop_time = move_time % num
        if loop_time == 0:
            loop_time = num

        clear_code = move_time/(2 * num)
        if clear_code > 1.0:
            clear_code = 1.0
        clear_code *= 0.5

        color_code = rand(3)
        max_color = np.amax(color_code)
        color_code = color_code / max_color
        for i in range(3):
            if color_code[i] < 0.5:
                color_code[i] = 0.5
        color_code = np.append(color_code *(loop_time/num), clear_code)
        for i in range(3):
            if color_code[i] < 0.3:
                color_code[i] = 0.3

        rotate_angle = 2 * np.pi / loop_time
        rotate_mat = np.array([[np.cos(rotate_angle), -np.sin(rotate_angle)],[np.sin(rotate_angle), np.cos(rotate_angle)]])

        for i in range(loop_time):
            if move_time > 1:
                for j in range(move_time):
                    temp_x = self.seq_x[j]
                    temp_y = self.seq_y[j]
                    temp_a = np.dot(rotate_mat, np.array([temp_x, temp_y]))
                    self.seq_x[j] = temp_a[0]
                    self.seq_y[j] = temp_a[1]
                plt.plot(self.seq_x + self.center_x, self.seq_y + self.center_y, linewidth=self.line_size, color=color_code)

    def save_fig(self):
        plt.savefig('figure01.png', format="png", dpi=1200)


if __name__ == "__main__":
    Drawer = SingleLine()

    for i in range(100):
        Drawer.generate_line(19)

    Drawer.save_fig()
