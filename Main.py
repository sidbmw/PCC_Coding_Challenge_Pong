# Author: Siddharth Natamai
# Version: 1.00.0


# !/usr/bin/env python
import sys
import PySimpleGUI as sg

import random
import time
from sys import exit as exit

player_1_Starting_Score = 0
player_2_Starting_Score = 0

num_Of_Rounds = 0
while num_Of_Rounds < 1:
    num_Of_Rounds = int(sg.PopupGetText('How many rounds would you like to play?'))


class Ball:
    def __init__(self, canvas, bat_1, bat_2, colour):
        self.canvas = canvas
        self.bat_1 = bat_1
        self.bat_2 = bat_2
        self.player_1_Score = player_1_Starting_Score
        self.player_2_Score = player_2_Starting_Score
        self.draw_P1 = None
        self.draw_P2 = None
        self.id = self.canvas.create_oval(10, 10, 35, 35, fill=colour)
        self.canvas.move(self.id, 327, 220)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.x = random.choice([-2.5, 2.5])
        self.y = -2.5

    def win_loss_check(self):
        winner = None
        if self.player_1_Score >= num_Of_Rounds:
            winner = 'Player Right Wins'
        if self.player_2_Score >= num_Of_Rounds:
            winner = 'Player Left Wins'
        return winner

    def updatep(self, val):
        self.canvas.delete(self.draw_P1)
        self.draw_P1 = self.canvas.create_text(170, 50, font=('freesansbold.ttf', 40), text=str(val), fill='white')

    def updatep1(self, val):
        self.canvas.delete(self.draw_P2)
        self.draw_P2 = self.canvas.create_text(550, 50, font=('freesansbold.ttf', 40), text=str(val), fill='white')

    def hit_bat(self, pos):
        bat_pos = self.canvas.coords(self.bat_1.id)
        if pos[2] >= bat_pos[0] and pos[0] <= bat_pos[2]:
            if bat_pos[1] <= pos[3] <= bat_pos[3]:
                return True
            return False

    def hit_bat2(self, pos):
        bat_pos = self.canvas.coords(self.bat_2.id)
        if pos[2] >= bat_pos[0] and pos[0] <= bat_pos[2]:
            if bat_pos[1] <= pos[3] <= bat_pos[3]:
                return True
            return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 4
        if pos[3] >= self.canvas_height:
            self.y = -4
        if pos[0] <= 0:
            self.player_1_Score += 1
            self.canvas.move(self.id, 327, 220)
            self.x = 4
            self.updatep1(self.player_1_Score)
        if pos[2] >= self.canvas_width:
            self.player_2_Score += 1
            self.canvas.move(self.id, -327, -220)
            self.x = -4
            self.updatep(self.player_2_Score)
        if self.hit_bat(pos):
            self.x = 4
        if self.hit_bat2(pos):
            self.x = -4


class PongBat():
    def __init__(self, canvas, colour, x, width=20, height=110):
        # x = 30, 670
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(
            x - width / 2, 200, x + width / 2, 200 + height,
            fill=colour)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.y = 0

    def up(self, evt):
        self.y = -5

    def down(self, evt):
        self.y = 5

    @property
    def curr_pos(self):
        pos = self.canvas.coords(self.id)
        return pos[1]

    def draw(self):
        self.canvas.move(self.id, 0, self.y)

        if self.curr_pos <= 0:
            self.y = 0
        if self.curr_pos >= 290:
            self.y = 0


def pong():
    layout = [[sg.Canvas(size=(700, 400), background_color='black', key='canvas')],
              [sg.T(''), sg.Button('Exit')]]

    window = sg.Window('Pong', return_keyboard_events=True).Layout(layout).Finalize()

    canvas = window.FindElement('canvas').TKCanvas

    bat_1 = PongBat(canvas, 'red', 30)
    bat_2 = PongBat(canvas, 'blue', 670)

    ball_1 = Ball(canvas, bat_1, bat_2, 'white')

    while True:
        ball_1.draw()
        bat_1.draw()
        bat_2.draw()

        event, values = window.Read(timeout=0)

        if event is None or event == 'Exit':
            exit(5)

        if event is not None:
            if event.startswith('Up') and bat_2.curr_pos > 0:
                bat_2.up(2)
            if event.startswith('Down') and bat_2.curr_pos < 290:
                bat_2.down(2)

        if event == 'w' and bat_1.curr_pos > 0:
            bat_1.up(2)
        if event == 's' and bat_1.curr_pos < 290:
            bat_1.down(2)

        if ball_1.win_loss_check():
            sg.Popup('Game Over', ball_1.win_loss_check() + ' won!!')
            break

        canvas.after(10)


if __name__ == '__main__':
    pong()
