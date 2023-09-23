from tkinter import Toplevel
import tkinter as tk
import customtkinter as ctk

import set  # cargar y guardar configuraciones del juego.
import path  # contiene la funcion resource_path, la cual devuelve la ruta global de un archivo.
path_show_msg = path.resource_path('customtkinter/show_msg.txt')


# crea la ventana top level.
def show_msg_top(root: ctk.CTk, pos_x: int, pos_y: int):
    icon_path = path.resource_path('Pictures\\message.ico')
    window = Toplevel(root)
    window.configure(bg='#2C3958')
    window.iconbitmap(icon_path)
    window.title('Messages to be displayed')
    # w_messages.geometry(f"623x360+{pos_x - 200}+{pos_y - 200}")
    window.geometry(f"+{pos_y}+{pos_x -500}")
    window.resizable(False, False)
    window.transient(root)
    window.focus_set()

    # frames primarios
    f_messages = tk.Frame(window, height=240, width=623, bg='#2C3958')
    f_messages.grid(row=0, column=0, rowspan=4)
    f_bottom = tk.Frame(window, height=60, width=623, bg='#2C3958')
    f_bottom.grid(row=4, column=0)

    # eliminar los mensajes seleccionados.
    def selected():
        seleccionados = listbox.curselection()
        for msg_index in seleccionados[::-1]:
            try:
                listbox.delete(msg_index)
                set.delete_message(msg_index, path_show_msg)
            except IndexError:
                print('Error: INDEX ERROR - delete_selected')

    canvas = tk.Canvas(f_messages, bg='darkgray')
    canvas.grid(row=0, column=0, pady=5, padx=5)
    listbox = tk.Listbox(canvas, selectmode=tk.MULTIPLE, background='#343638', fg='white', font=('Candara', 13), justify='left', highlightbackground='White', selectbackground='#394970', width=40, height=8)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipadx=5)
    for item in set.get_messages(path_show_msg):
        listbox.insert(tk.END, ' ' + item)
    ctk.CTkButton(f_bottom, text='Hide', width=60, command=lambda: selected(), fg_color='darkred', hover_color='red', border_color="White", border_width=1, text_color='White').pack(anchor='center', pady=6)

    # cerrar la ventana de mensajes.
    def on_close():
        window.destroy()
        try:
            root.buttons_enabled()
        except AttributeError:
            pass

    window.protocol("WM_DELETE_WINDOW", on_close)
