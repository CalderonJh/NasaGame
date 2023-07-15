from tkinter import Toplevel
import tkinter as tk
import customtkinter as ctk

import set  # cargar y guardar configuraciones del juego.
import path  # contiene la funcion resource_path, la cual devuelve la ruta global de un archivo.

path_msgs = path.resource_path('messages.txt')


# define el tamaño máximo de caracteres de un mensaje.
def validate_text(new_text):
    if len(new_text) <= 50:
        return True
    else:
        return False


# crea la ventana top level.
def message_top(root: ctk.CTk, pos_x: int, pos_y: int):
    icon_path = path.resource_path('Pictures\\message.ico')
    w_messages = Toplevel(root)
    w_messages.configure(bg='#2C3958')
    w_messages.iconbitmap(icon_path)
    w_messages.title('Created messages')
    # w_messages.geometry(f"623x360+{pos_x - 200}+{pos_y - 200}")
    w_messages.geometry(f"+{pos_y}+{pos_x - 500}")
    w_messages.resizable(False, False)
    w_messages.transient(root)
    w_messages.focus_set()

    validation = w_messages.register(validate_text)

    # frames primarios
    f_top = tk.Frame(w_messages, height=60, width=623, bg='#2C3958')
    f_top.grid(row=0, column=0, )
    f_messages = tk.Frame(w_messages, height=240, width=623, bg='#2C3958')
    f_messages.grid(row=1, column=0, rowspan=4)
    f_bottom = tk.Frame(w_messages, height=60, width=623, bg='#2C3958')
    f_bottom.grid(row=5, column=0)

    # eliminar los mensajes seleccionados.
    def delete_selected():
        seleccionados = listbox.curselection()
        for msg_index in seleccionados[::-1]:
            try:
                listbox.delete(msg_index)
                msg = set.get_messages(path_msgs)[msg_index]
                set.delete_message(msg_index, path_msgs)
                if msg in set.get_messages(path.resource_path('show_msg.txt')):
                    set.delete_show(msg)
            except IndexError:
                print('Error: INDEX ERROR - delete_selected')

    # limpiar toda la lista.
    def delete_all():
        try:
            set.delete_all_messages(path_msgs)
            set.delete_all_messages(path.resource_path('show_msg.txt'))
            listbox.delete(0, tk.END)
        except IndexError:
            print('Error: Delete all messages')

    # agrega los mensajes seleccionados al archivo de mensajes para mostrar
    def show():
        selected = listbox.curselection()
        for i in selected:
            set.add_message(set.get_messages(path_msgs)[i], path.resource_path('show_msg.txt'))

    # widgets
    ctk.CTkButton(f_top, text='Show', width=60, fg_color='#343638', border_color="White", command=show, border_width=1,
                  text_color='White').grid(row=0, column=1, padx=10, pady=5)
    ctk.CTkButton(f_top, text='Delete', width=60, command=delete_selected, fg_color='#343638', border_color="White",
                  border_width=1, text_color='White').grid(row=0, column=2, padx=10, pady=5)
    ctk.CTkButton(f_top, text='Clear', width=60, command=delete_all, fg_color='darkred', hover_color='red',
                  border_color="White", border_width=1, text_color='White').grid(row=0, column=3, padx=10, pady=5)
    ctk.CTkLabel(f_top, text='Message every:', fg_color='transparent', text_color='White').grid(row=0, column=4, padx=1,
                                                                                                pady=5)
    msg_option_time = ctk.CTkOptionMenu(f_top, width=5, height=20, fg_color='#343638',
                                        values=['7', '5', '3', '1', '0.5'], text_color='White')
    msg_option_time.set(set.get_variable('msg_timer'))
    msg_option_time.grid(row=0, column=5, padx=3, pady=5)

    ctk.CTkLabel(f_top, text='seconds', fg_color='transparent', text_color='White').grid(row=0, column=6, padx=1,
                                                                                         pady=5)

    # lista de mensajes
    canvas = tk.Canvas(f_messages, bg='darkgray')
    canvas.grid(row=1, column=0)
    listbox = tk.Listbox(canvas, selectmode=tk.MULTIPLE, background='#343638', fg='white', font=('Candara', 13),
                         justify='left', highlightbackground='White', selectbackground='#394970', width=49, height=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipadx=5)
    for item in set.get_messages(path.resource_path('messages.txt')):
        listbox.insert(tk.END, ' ' + item)

    # crear mensajes
    entry = ctk.CTkEntry(f_bottom, validate="key", validatecommand=(validation, '%P'), border_color='White',
                         border_width=1, placeholder_text="Write a new message", font=('Calibri', 15), width=420)
    entry.pack(anchor='w', side='left', padx=5, pady=8)
    entry.bind('<Return>', lambda event: create_message())

    # agrega un nuevo mensaje.
    def create_message():
        message = entry.get().rstrip()
        if message != '' and not message.isspace():
            msgs = set.get_messages(path_msgs)
            if (message in msgs) is False:
                listbox.insert(tk.END, ' ' + message)
            set.add_message(message, path_msgs)
        entry.delete(0, tk.END)

    # cerrar la ventana de mensajes.
    def on_close():
        w_messages.destroy()
        try:
            root.buttons_enabled()
        except AttributeError:
            pass
        set.set_variable('msg_timer', msg_option_time.get())

    w_messages.protocol("WM_DELETE_WINDOW", on_close)
    ctk.CTkButton(f_bottom, command=create_message, text='Ok', fg_color='#343638', border_color="White", border_width=1,
                  width=45).pack(anchor='e', side='right', padx=10, pady=5)
