# run/window
import pygame
import random
import customtkinter as ctk
from tkinter import *
from PIL import Image

from src.func import display_msg, message_window
from src.tools import screen_info, path, modify
from src.window import game

ctk.set_default_color_theme("dark-blue")
sc_ancho, sc_alto = screen_info.get_info()
pos_x = int(sc_ancho / 2)
pos_y = int(sc_alto / 2)
pygame.mixer.init()


# La clase Welcome representa la primera ventana a mostrar.
class Welcome(ctk.CTk):
    ctk.set_appearance_mode("dark")
    global pos_x, pos_y
    center: ctk.CTkFrame
    right: ctk.CTkFrame
    f_time: ctk.CTkFrame
    f_speed: ctk.CTkFrame
    f_message: ctk.CTkFrame
    f_mode: ctk.CTkFrame
    f_logo: ctk.CTkFrame
    f_label_msg: ctk.CTkFrame
    label_nasa_game: ctk.CTkLabel
    button_messages: ctk.CTkButton
    button_show_msg: ctk.CTkButton
    button_start: ctk.CTkButton
    mute_button: ctk.CTkButton
    game_time: ctk.CTkOptionMenu  # el tiempo de juego seleccionado por el jugador.
    game_mode: ctk.CTkOptionMenu  # el modo de juego seleccionado.
    game_speed: ctk.CTkOptionMenu  # tiempo de actualización de la pantalla.

    def __init__(self):
        super().__init__()
        pygame.mixer.music.load(path.resource_path('../main/music\\welcome_music.mp3'))
        if modify.get_variable('mute') == 'Mute':
            pygame.mixer.music.set_volume(0.2)
        else:
            pygame.mixer.music.set_volume(0.0)
        pygame.mixer.music.play(loops=-1, start=8.5, fade_ms=5000)
        self.title("Nasa Game")
        self.configure(fg_color='#2C3958')
        self.geometry(f"{846}x{510}+{pos_x - 450}+{pos_y - 300}")
        self.resizable(False, False)
        self.icon()
        self.frames()
        self.widgets()
        self.toplevel_window = None

    # establece un icono para la ventana.
    def icon(self):
        image_path = path.resource_path("Pictures\\icon.ico")
        self.iconbitmap(image_path)

    # monta los frames necesarios.
    def frames(self):
        # frames primarios
        self.center = ctk.CTkFrame(self,
                                   fg_color="transparent",
                                   height=310)

        self.center.pack(anchor='n',
                         fill='x',
                         expand=True)

        bottom = ctk.CTkFrame(self,
                              fg_color="transparent",
                              height=200)

        bottom.pack(anchor='s',
                    fill='both',
                    expand=True)

        # frames en bottom
        left = ctk.CTkFrame(bottom,
                            fg_color="transparent",
                            width=282,
                            height=200)

        start = ctk.CTkFrame(bottom,
                             fg_color='transparent',
                             width=282,
                             height=200)

        self.right = ctk.CTkFrame(bottom,
                                  fg_color="transparent",
                                  width=282,
                                  height=200)

        left.grid(row=0, column=0)
        start.grid_propagate(False)
        start.grid(row=0, column=1)
        self.right.grid(row=0, column=2)

        self.f_time = ctk.CTkFrame(left,
                                   fg_color='transparent',
                                   height=40,
                                   width=282)

        self.f_time.grid(row=0, column=0)

        ctk.CTkFrame(left, fg_color='transparent',
                     height=10,
                     width=282).grid(row=1,
                                     column=0)

        self.f_speed = ctk.CTkFrame(left,
                                    fg_color='transparent',
                                    height=40,
                                    width=282)

        self.f_speed.grid(row=2, column=0)

        ctk.CTkFrame(left,
                     fg_color='transparent',
                     height=10,
                     width=282).grid(row=3,
                                     column=0)

        self.f_mode = ctk.CTkFrame(left,
                                   fg_color='transparent',
                                   height=40,
                                   width=282)

        self.f_mode.grid(row=4, column=0)

        ctk.CTkFrame(left,
                     fg_color='transparent',
                     height=10,
                     width=282).grid(row=5,
                                     column=0)

        self.f_label_msg = ctk.CTkFrame(left,
                                        fg_color='transparent',
                                        height=20)

        self.f_label_msg.grid(row=6,
                              column=0)

        self.f_message = ctk.CTkFrame(left,
                                      fg_color='transparent',
                                      height=40,
                                      width=282)

        self.f_message.grid(row=7, column=0)

        ctk.CTkFrame(left, fg_color='transparent',
                     height=10,
                     width=282).grid(row=8,
                                     column=0)

        # frames en start
        ctk.CTkFrame(start,
                     fg_color='transparent',
                     height=10,
                     width=282).grid(row=0,
                                     column=0)

        self.f_logo = ctk.CTkFrame(start,
                                   fg_color='transparent',
                                   height=170,
                                   width=150)

        self.f_logo.grid(row=1, column=0, rowspan=8)

        ctk.CTkFrame(self.right,
                     fg_color='transparent',
                     height=100, width=282).grid(row=0, column=0)

    # crea y ubica los widgets necesarios.
    def widgets(self):
        # images
        nasa_game_img = ctk.CTkImage(light_image=Image.open(path.resource_path("Pictures\\NasaGame.png")),
                                     dark_image=Image.open(path.resource_path("Pictures\\NasaGame.png")),
                                     size=(600, 250))

        logo_tavo = ctk.CTkImage(light_image=Image.open(path.resource_path("Pictures\\logo_tavo.png")),
                                 dark_image=Image.open(path.resource_path("Pictures\\logo_tavo.png")),
                                 size=(150, 150))

        # labels
        self.label_nasa_game = ctk.CTkLabel(master=self.center,
                                            text="",
                                            image=nasa_game_img,
                                            fg_color="#2C3958",
                                            corner_radius=10)

        self.label_nasa_game.pack(anchor='n', fill='y', pady=30)

        # buttons
        self.button_start = ctk.CTkButton(self.f_logo,
                                          text="",
                                          fg_color='transparent',
                                          hover_color='#2b3755',
                                          image=logo_tavo,
                                          width=150,
                                          height=150,
                                          command=self.start_game)

        self.button_start.pack(anchor='center', side='top')

        self.mute_button = ctk.CTkButton(self.right,
                                         text=modify.get_variable('mute'),
                                         text_color='#dbaa62',
                                         fg_color='#394970',
                                         command=self.mute_unmute,
                                         border_color="#dbaa62",
                                         border_width=1,
                                         width=60)

        self.mute_button.grid(row=1, sticky='e', padx=10, pady=2)

        ctk.CTkButton(self.right, text="Exit",
                      text_color='#dbaa62',
                      fg_color='#394970',
                      command=self.destroy,
                      border_color="#dbaa62",
                      border_width=1,
                      width=60).grid(row=2, sticky='e', padx=10, pady=5)

        # opciones de juego
        ctk.CTkLabel(self.f_time,
                     text="Time:",
                     text_color='#dbaa62',
                     fg_color='transparent',
                     padx=7).grid(row=0, column=0)

        self.game_time = ctk.CTkOptionMenu(self.f_time,
                                           fg_color='#394970',
                                           text_color='#dbaa62',
                                           values=['15', '20', '30', '45'],
                                           width=50,
                                           height=20)

        self.game_time.set(modify.get_variable("time"))
        self.game_time.grid(row=0, column=1)

        ctk.CTkLabel(self.f_time,
                     text="minutes",
                     text_color='#dbaa62',
                     fg_color='transparent',
                     padx=7).grid(row=0, column=2)

        ctk.CTkLabel(self.f_speed,
                     text="Game Speed:",
                     text_color='#dbaa62',
                     fg_color='transparent',
                     padx=7).grid(row=0, column=0)

        self.game_speed = ctk.CTkOptionMenu(self.f_speed,
                                            fg_color='#394970',
                                            text_color='#dbaa62',
                                            values=['0.5', '1.0', '1.5', '2.0', '2.5', '3.0'],
                                            width=50,
                                            height=20)

        self.game_speed.set(modify.get_variable("speed"))
        self.game_speed.grid(row=0, column=1)
        ctk.CTkLabel(self.f_speed, text="seconds",
                     text_color='#dbaa62',
                     fg_color='transparent',
                     padx=7).grid(row=0, column=2)

        ctk.CTkLabel(self.f_label_msg, text='Messages', text_color='#dbaa62', fg_color='transparent').pack()

        self.button_messages = ctk.CTkButton(self.f_message,
                                             fg_color='#394970',
                                             text="Created",
                                             font=('Sans Serif', 13),
                                             text_color='#dbaa62',
                                             border_color="#dbaa62",
                                             border_width=1,
                                             command=self.window_message,
                                             width=38,
                                             height=25)

        self.button_show_msg = ctk.CTkButton(self.f_message,
                                             fg_color='#394970',
                                             text="Selected",
                                             text_color='#dbaa62',
                                             font=('Sans Serif', 13),
                                             border_color="#dbaa62",
                                             border_width=1,
                                             command=self.show_msg_top,
                                             width=38,
                                             height=25)

        self.button_messages.grid(column=0, row=0, padx=5)
        self.button_show_msg.grid(column=1, row=0, padx=5)

        ctk.CTkLabel(self.f_mode,
                     text="Mode:",
                     fg_color='transparent',
                     text_color='#dbaa62',
                     padx=7).grid(row=0, column=0)

        self.game_mode = ctk.CTkOptionMenu(self.f_mode,
                                           fg_color='#394970',
                                           text_color='#dbaa62',
                                           values=['ABC-Random',
                                                   'ABC-Ascending',
                                                   'ABC-Descending',
                                                   'ABC-Grouping 3',
                                                   'ABC-Grouping 4',
                                                   '123-Random',
                                                   '123-Ascending',
                                                   '123-Descending',
                                                   'Mixed-Random'],
                                           width=100,
                                           height=25)
        self.game_mode.set(modify.get_variable("mode"))
        self.game_mode.grid(row=0, column=1)

    # funcion del botón Mute/Unmute.
    def mute_unmute(self):
        if self.mute_button.cget('text') == 'Mute':
            pygame.mixer.music.set_volume(0)
            self.mute_button.configure(text='Unmute')
            modify.set_variable('mute', 'Unmute')
        else:
            pygame.mixer.music.set_volume(0.2)
            self.mute_button.configure(text='Mute')
            modify.set_variable('mute', 'Mute')

    # crea la ventana de mensajes.
    def window_message(self):
        self.buttons_disabled()
        message_window.message_top(self, pos_x, pos_y)

    def show_msg_top(self):
        # self.button_show_msg.configure(state='disabled')
        self.buttons_disabled()
        display_msg.show_msg_top(self, pos_x, pos_y)

    # acción del botón start.
    def start_game(self):
        music_option = [0.0, 267, 495, 700, 938]  # opciones de tiempo para iniciar la musica de fondo.
        try:
            modify.set_variable('time', self.game_time.get())
            modify.set_variable('mode', self.game_mode.get())
            modify.set_variable('speed', self.game_speed.get())
        except PermissionError:
            self.permission_error()
            return

        pygame.mixer.music.load(path.resource_path('music\\mix.mp3'))
        pygame.mixer.music.play(loops=-1, fade_ms=1000, start=random.choice(music_option))
        pygame.mixer.music.set_volume(0.5)
        self.withdraw()
        game.GameWindow(self)

    def buttons_disabled(self):
        self.button_start.configure(state='disabled')
        self.button_show_msg.configure(state='disabled')
        self.button_messages.configure(state='disabled')

    def buttons_enabled(self):
        self.button_start.configure(state='normal')
        self.button_show_msg.configure(state='normal')
        self.button_messages.configure(state='normal')

    def permission_error(self):
        window = Toplevel(self)
        window.configure(bg='#2C3958')
        window.title('Permission Error')
        msg = 'It was not possible to start the game because\n' \
              'Windows prevents it due to lack of permissions.\n' \
              'Please close the application and start it\n' \
              'in \'administrator mode\'.\n' \
              '(Right-click and "Run as administrator")'
        window.geometry(f"+{pos_y + 200}+{pos_x - 500}")
        window.resizable(False, False)
        window.transient(self)
        window.focus_set()
        ctk.CTkLabel(window, text=msg, justify='left').pack(anchor='center', padx=10, pady=10)
        ctk.CTkButton(window,
                      text='I get it',
                      command=self.destroy,
                      text_color='white',
                      fg_color='#394970',
                      border_color="white",
                      border_width=1,
                      width=60).pack(anchor='s', pady=5)


def run():
    wel = Welcome()
    wel.mainloop()
