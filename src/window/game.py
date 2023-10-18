import random
from tkinter import *

import pygame
from PIL import Image

import customtkinter as ctk
# contiene la funcion get_info usada para obtener el tamaño de pantalla actual.
from src.tools import modify, screen_info, path

sc_ancho, sc_alto = screen_info.get_info()


# usada para mostrar el tiempo de juego actual.
def milisegundos_a_minutos(milisegundos):
    minutos = int(milisegundos / 60000)
    segundos = int((milisegundos % 60000) / 1000)
    if segundos < 10:
        segundos = f"0{segundos}"
    if minutos < 10:
        minutos = f"0{minutos}"
    return f"{minutos}:{segundos}"


# GameWindow es una ventana top level de Welcome donde actua el juego.
class GameWindow(ctk.CTkToplevel):
    size_flechas = (int(sc_ancho * (1 / 5)),
                    int(sc_alto * (1 / 5)))

    size_image = int(sc_ancho * (1 / 3))

    right: ctk.CTkFrame
    time_frame: ctk.CTkFrame
    msg: ctk.CTkFrame
    flecha_left: ctk.CTkFrame
    flecha_right: ctk.CTkFrame
    frame_letra: ctk.CTkFrame

    label_time: ctk.CTkLabel
    label_imagen: ctk.CTkLabel
    label_derecha: ctk.CTkLabel
    label_izquierda: ctk.CTkLabel
    label_msg: ctk.CTkLabel

    image_pause: ctk.CTkImage
    image_resume: ctk.CTkImage

    pause_button: ctk.CTkButton
    exit_button: ctk.CTkButton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paused = False
        self.time_to_play = int(float(modify.get_variable('time')) * 60000)

        self.letters_option = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', "L",
                               "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        self.numbers_option = [str(i) for i in range(1, 100)]

        self.group_of_three = ['A', 'B', 'C', 'X', 'Y', 'Z', 'D', 'E', 'F', 'U', 'V', "W", "G", "H", "I",
                               "R", "S", "T", "J", "K", "L", "O", "P", "Q", "M", "N"]

        self.group_of_four = ['A', 'B', 'C', 'D', 'W', 'X', 'Y', 'Z', 'E', 'F', 'G', "H", "S", "T", "U", "V",
                              "I", "J", "K", "L", "O", "P", "Q", "R", "M", "N"]
        self.index_image = 0

        self.showed_images = []

        self.finish_image = ctk.CTkImage(light_image=Image.open(
            path.resource_path(
                'Pictures\\finish_image.png')),
            dark_image=Image.open(
                path.resource_path('Pictures\\finish_image.png')),
            size=(self.size_image,
                  self.size_image))

        self.current_direction = random.choice(["r", "l", "b"])
        self.mode = modify.get_variable('mode')
        self.current_image = self.first_image()
        self.speed = int(float(modify.get_variable('speed')) * 1000) - 350
        self.msg_timer = int(int(float(modify.get_variable('msg_timer')) * 1000) / 2)
        self.mode = modify.get_variable('mode')
        self.messages_list = modify.get_messages(
            path.resource_path('config-ng\\show_msg.txt'))
        self.num_msg = len(self.messages_list)
        self.showed_msgs = []
        self.showed_time = 350

        self.configure(fg_color="#E6E6E6")
        self.title("Game")
        self.attributes('-fullscreen', True)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.wm_frames()
        self.widgets()
        self.after(self.msg_timer, self.show_message)
        self.after(500, self.update_clock)
        self.bind("<space>", lambda event: self.pause_game())

    # acción del botón de pausa.
    def pause_game(self):
        if self.paused:
            self.paused = False
            self.pause_button.configure(image=self.image_pause)
            pygame.mixer.music.unpause()
        else:
            self.paused = True
            self.pause_button.configure(image=self.image_resume)
            pygame.mixer.music.pause()

    # crea y ubica los frames necesarios.
    def wm_frames(self):
        height_top = int(sc_alto * (2 / 3))

        center = ctk.CTkFrame(self, fg_color='transparent', height=height_top)
        center.pack(fill='x', anchor='center', side='top')

        ctk.CTkFrame(center, fg_color='transparent', width=20).grid(row=0, column=0)

        self.flecha_left = ctk.CTkFrame(center,
                                        fg_color='transparent',
                                        width=self.size_flechas[0],
                                        height=self.size_flechas[1])
        self.flecha_left.grid(row=0,
                              column=1,
                              padx=10,
                              sticky='w')

        self.grid_columnconfigure(0, weight=1)

        self.frame_letra = ctk.CTkFrame(center,
                                        fg_color='transparent',
                                        width=self.size_image,
                                        height=self.size_image)

        self.frame_letra.grid(row=0,
                              column=2,
                              columnspan=2,
                              sticky='nsew')

        self.grid_columnconfigure(1, weight=1)

        self.flecha_right = ctk.CTkFrame(center,
                                         fg_color='transparent',
                                         width=self.size_flechas[0],
                                         height=self.size_flechas[1])

        self.flecha_right.grid(row=0,
                               column=4,
                               sticky='e',
                               padx=10)

        self.grid_columnconfigure(3, weight=1)

        self.msg = ctk.CTkFrame(self, fg_color='transparent')

        self.msg.pack(fill='both',
                      side='top',
                      anchor='center')

        self.time_frame = ctk.CTkFrame(self,
                                       fg_color='transparent',
                                       width=int(sc_ancho / 6) - 100)

        self.time_frame.pack(fill='y',
                             side='left',
                             anchor='w')

        self.right = ctk.CTkFrame(self,
                                  fg_color='transparent',
                                  width=int(sc_ancho / 6) - 100)

        self.right.pack(fill='y',
                        side='right',
                        anchor='se')

    # crea los widgets como labels y botones.
    def widgets(self):
        image_path = 'Pictures\\' + self.current_image + ".png"
        izqu_path = 'Pictures\\left.png'
        der_path = 'Pictures\\right.png'

        letra = ctk.CTkImage(light_image=Image.open(path.resource_path(image_path)),
                             dark_image=Image.open(path.resource_path(image_path)),
                             size=(self.size_image, self.size_image))

        derecha = ctk.CTkImage(light_image=Image.open(path.resource_path(der_path)),
                               dark_image=Image.open(path.resource_path(der_path)),
                               size=self.size_flechas)

        izquierda = ctk.CTkImage(light_image=Image.open(path.resource_path(izqu_path)),
                                 dark_image=Image.open(path.resource_path(izqu_path)),
                                 size=self.size_flechas)

        self.label_izquierda = ctk.CTkLabel(self.flecha_left,
                                            image=izquierda,
                                            text='')

        self.label_derecha = ctk.CTkLabel(self.flecha_right,
                                          image=derecha,
                                          text='')

        self.label_imagen = ctk.CTkLabel(self.frame_letra,
                                         image=letra,
                                         text='')

        self.label_msg = ctk.CTkLabel(self.msg,
                                      text="",
                                      font=('Arial Nova Cond Light', 60),
                                      text_color='darkorange',
                                      height=40,
                                      fg_color='transparent')

        self.label_imagen.pack(pady=20, padx=20)
        self.after(self.showed_time, self.hide)
        self.change_direction()
        ctk.CTkFrame(self.right,
                     fg_color='transparent',
                     height=int(self.right.cget('height') * 0.25)).grid(row=0,
                                                                        column=0,
                                                                        rowspan=2,
                                                                        columnspan=2)

        self.label_msg.pack(anchor='center', fill='both')

        image_exit = ctk.CTkImage(light_image=Image.open(path.resource_path('Pictures\\exit_game.png')),
                                  dark_image=Image.open(path.resource_path('Pictures\\exit_game.png')),
                                  size=(40, 40))

        self.image_pause = ctk.CTkImage(light_image=Image.open(path.resource_path('Pictures\\pause.png')),
                                        dark_image=Image.open(path.resource_path('Pictures\\pause.png')),
                                        size=(40, 40))

        self.image_resume = ctk.CTkImage(light_image=Image.open(path.resource_path('Pictures\\resume.png')),
                                         dark_image=Image.open(path.resource_path('Pictures\\resume.png')),
                                         size=(40, 40))

        self.pause_button = ctk.CTkButton(self.right,
                                          text="",
                                          border_width=2,
                                          border_spacing=1,
                                          border_color='black',
                                          fg_color='white',
                                          hover_color='darkgray',
                                          image=self.image_pause,
                                          height=40, width=40,
                                          command=self.pause_game)

        self.label_time = ctk.CTkLabel(self.time_frame,
                                       text=milisegundos_a_minutos(self.time_to_play),
                                       font=('Courier', 75),
                                       text_color='black',
                                       fg_color='transparent')

        self.label_time.pack(anchor='center',
                             padx=20,
                             fill='both')

        self.pause_button.grid(column=0,
                               row=2,
                               sticky='e',
                               padx=5)

        self.exit_button = ctk.CTkButton(self.right,
                                         text="",
                                         border_width=2,
                                         border_spacing=1,
                                         border_color='black',
                                         fg_color='white',
                                         hover_color='darkgray',
                                         image=image_exit,
                                         height=40, width=40,
                                         command=self.exit)

        self.exit_button.grid(column=1,
                              row=2,
                              sticky='w',
                              padx=10)

    # define el nombre de la primera imagen a mostrar, dado el modo de juego
    def first_image(self):
        if self.mode == 'ABC-Random':
            new_image_name = random.choice(self.letters_option)
            self.letters_option.remove(new_image_name)
            self.showed_images.append(new_image_name)
            return new_image_name
        elif self.mode == 'ABC-Ascending' or self.mode == 'ABC-Grouping 3' or self.mode == 'ABC-Grouping 4':
            return 'A'
        elif self.mode == 'ABC-Descending':
            return 'Z'
        elif self.mode == '123-Random':
            new_image_name = str(random.randint(1, 99))
            self.numbers_option.remove(new_image_name)
            self.showed_images.append(new_image_name)
            return new_image_name
        elif self.mode == '123-Ascending':
            return '1'
        elif self.mode == '123-Descending':
            return '99'
        elif self.mode == 'Mixed-Random':
            new_image_name = random.choice(self.letters_option)
            self.letters_option.remove(new_image_name)
            self.showed_images.append(new_image_name)
            return new_image_name

    # define el nombre de la siguiente imagen a mostrar, dado el modo de juego
    def next_image(self):
        self.index_image += 1
        if self.index_image == 26 and 'ABC' in self.mode:
            self.index_image = 0

        elif self.index_image == 99 and '123' in self.mode:
            self.index_image = 0

        if self.mode == 'ABC-Random':
            if len(self.letters_option) == 0:
                self.letters_option = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', "L",
                                       "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
                self.showed_images.clear()
            new_image_name = random.choice(self.letters_option)
            self.showed_images.append(new_image_name)
            self.letters_option.remove(new_image_name)
            return new_image_name

        elif self.mode == 'ABC-Ascending':
            return self.letters_option[self.index_image]

        elif self.mode == 'ABC-Descending':
            return self.letters_option[25 - self.index_image]

        elif self.mode == 'ABC-Grouping 3':
            return self.group_of_three[self.index_image]

        elif self.mode == 'ABC-Grouping 4':
            return self.group_of_four[self.index_image]

        elif self.mode == '123-Random':
            if len(self.numbers_option) == 0:
                self.numbers_option = [str(i) for i in range(1, 100)]
                self.showed_images.clear()
            new_image_name = random.choice(self.numbers_option)
            self.showed_images.append(new_image_name)
            self.numbers_option.remove(new_image_name)
            return new_image_name

        elif self.mode == '123-Ascending':
            return self.numbers_option[self.index_image]

        elif self.mode == '123-Descending':
            return self.numbers_option[98 - self.index_image]

        elif self.mode == 'Mixed-Random':
            if len(self.letters_option) == 0:
                self.letters_option = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', "K", "L", "M", "N",
                                       "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
                self.showed_images.clear()
            if len(self.numbers_option) == 0:
                self.numbers_option = [str(i) for i in range(1, 100)]
            if self.index_image % 2 == 0:
                new_image_name = random.choice(self.letters_option)
                self.letters_option.remove(new_image_name)
                self.showed_images.append(new_image_name)
            else:
                new_image_name = random.choice(self.numbers_option)
            return new_image_name

    # muestra la imagen en pantalla.
    def change_image(self):
        self.label_imagen.pack(pady=20, padx=20)
        new_image_name = self.next_image()
        current_image_name = new_image_name
        # path de la imagen a cargar
        image_path = 'Pictures\\' + current_image_name + '.png'
        # se crea la imagen
        nueva_imagen = ctk.CTkImage(light_image=Image.open(path.resource_path(image_path)),
                                    dark_image=Image.open(path.resource_path(image_path)),
                                    size=(self.size_image, self.size_image))

        # Actualizar la etiqueta con la nueva imagen
        self.label_imagen.configure(image=nueva_imagen)
        self.label_imagen.image = nueva_imagen  # Actualizar la referencia a la imagen

    # elige la siguiente dirección de las flechas.
    def choose_new_direction(self):
        if self.current_direction == "r":
            self.current_direction = random.choice(["l", "b"])
        elif self.current_direction == "l":
            self.current_direction = random.choice(["r", "b"])
        elif self.current_direction == "b":
            self.current_direction = random.choice(["l", "r"])

    # muestra la dirección con las flechas.
    def change_direction(self):
        if self.current_direction == "r":
            # mostrar solo imagen derecha
            self.label_derecha.pack()
            self.label_izquierda.pack_forget()
        elif self.current_direction == "l":
            # mostrar solo imagen izquierda
            self.label_izquierda.pack()
            self.label_derecha.pack_forget()
        else:
            # mostrar ambas images
            self.label_derecha.pack()
            self.label_izquierda.pack()
        self.choose_new_direction()

    # oculta el mensaje.
    def hide_message(self):
        if not self.paused:
            self.label_msg.configure(text='')
            self.after(self.msg_timer, self.show_message)
        else:
            self.after(500, self.hide_message)

    # muestra en pantalla uno de los mensajes disponibles.
    def show_message(self):
        if len(self.messages_list) == 0:
            self.messages_list = modify.get_messages(path.resource_path('config-ng\\show_msg.txt'))
            self.showed_msgs.clear()
        if not self.paused and len(self.messages_list) > 0:
            msg = random.choice(self.messages_list)
            self.label_msg.configure(text=msg)
            self.showed_msgs.append(msg)
            self.messages_list.remove(msg)
            self.after(self.msg_timer, self.hide_message)
        else:
            self.after(500, self.show_message)

    # oculta las flechas y la imagen principal, estas volverán a aparecer después de 'speed' milisegundos.
    def hide(self):
        if not self.paused:
            self.label_imagen.pack_forget()
            self.label_derecha.pack_forget()
            self.label_izquierda.pack_forget()
            self.after(self.speed, self.update_screen)
        else:
            self.after(150, self.hide)

    # muestra en pantalla las flechas y la imagen principal durante 'showed_time' milisegundos.
    def update_screen(self):
        if not self.paused:
            self.change_direction()
            self.change_image()
            self.after(self.showed_time, self.hide)
        else:
            self.after(self.showed_time, self.update_screen)

    # actualiza en tiempo real de juego la cuenta regresiva, cuando esta sea '00:00' el juego habrá terminado.
    def update_clock(self):
        if not self.paused:
            self.time_to_play -= 1000
            self.label_time.configure(text=milisegundos_a_minutos(self.time_to_play))
            if self.label_time.cget('text') == '00:00':
                self.finish_game()
            elif self.label_time.cget('text') == '00:04':
                pygame.mixer.music.fadeout(4000)
                self.after(1000, self.update_clock)
            else:
                self.after(1000, self.update_clock)
        else:
            self.after(500, self.update_clock)

    # acciones a ejecutar cuando se termine el tiempo a jugar.
    def finish_game(self):
        self.label_msg.configure(text='Thanks for playing!', text_color='black')
        self.label_imagen.pack(pady=20, padx=20)
        self.label_imagen.configure(image=self.finish_image)

        self.label_derecha.pack_forget()
        self.label_izquierda.pack_forget()
        self.paused = True
        self.pause_button.grid_forget()
        self.exit_button.configure(width=120)
        pygame.mixer.music.load(path.resource_path('music\\finish_music.mp3'))
        pygame.mixer_music.set_volume(0.2)
        pygame.mixer.music.play(loops=1, start=26.0, fade_ms=7500)

    # acción del botón exit.
    def exit(self):
        self.showed_images.clear()
        self.master.deiconify()
        self.destroy()
        pygame.mixer.music.load(path.resource_path('music\\welcome_music.mp3'))
        pygame.mixer.music.play(loops=-1, start=8.5, fade_ms=5000)
        if modify.get_variable('mute') == 'Mute':
            pygame.mixer.music.set_volume(0.2)
        else:
            pygame.mixer.music.set_volume(0.0)
