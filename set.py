import os
import path

# archivo que guarda configuraciones del juego.
file_variables = path.resource_path('config-ng/game_config.txt')

# archivo que guarda los mensajes del juego.
file_messages = path.resource_path('config-ng/messages.txt')

file_show_msg = path.resource_path('customtkinter/show_msg.txt')


# escribe unos ajustes por defecto en caso haber errores con el archivo de variables.
def write_variables():
    with open(file_variables, 'w') as f:
        f.write('45\n')
        f.write('3\n')
        f.write('ABC-Random\n')
        f.write('7\n')


# retorna las variables-ajustes o mensajes.
def get_lines(file):
    try:
        with open(file, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        create_txt(file)
        if file == file_variables:
            write_variables()
        with open(file, 'r') as f:
            return f.readlines()


# crea el archivo en caso de errores.
def create_txt(name):
    if not os.path.exists(name):
        with open(name, 'w') as f:
            f.write('')


# facilita el acceso a alguna de las variables.
def index_of_variable(variable):
    if variable == 'time':
        return 0
    elif variable == 'speed':
        return 1
    elif variable == 'mode':
        return 2
    elif variable == 'msg_timer':
        return 3
    elif variable == 'mute':
        return 4
    else:
        print('Error: variable not found')


# obtiene el valor de alguna de las variables.
def get_variable(variable):
    index = index_of_variable(variable)
    lines = get_lines(file_variables)
    variable = lines[index]
    variable = variable.split('\n')
    return variable[0]


# usada para modificar el valor de una variable.
def set_variable(variable, valor):
    index = index_of_variable(variable)
    lines = get_lines(file_variables)
    lines[index] = valor + '\n'
    with open(file_variables, 'w') as f:
        f.writelines(lines)


# agrega un nuevo mensaje.
def add_message(message, file):
    lines = get_lines(file)
    if message + '\n' not in lines:
        with open(file, 'a') as f:
            f.write(message + '\n')


def show_message(message):
    lines = get_lines(file_show_msg)
    if message + '\n' not in lines:
        with open(file_messages, 'a') as f:
            f.write(message + '\n')


def delete_show(msg):
    lines = get_lines(path.resource_path('customtkinter/show_msg.txt'))
    lines.remove(msg + '\n')
    delete_all_messages(file_show_msg)
    with open(path.resource_path('customtkinter/show_msg.txt'), 'w') as file:
        file.writelines(lines)


# elimina los mensajes seleccionados.
def delete_message(index, file):
    lines = get_lines(file)
    if index < len(lines):
        try:
            lines.pop(index)
        except ValueError:
            print('Message not found')
        with open(file, 'w') as f:
            f.writelines(lines)
    else:
        print('Error: Index out of range')


# obtener los mensajes disponibles.
def get_messages(file):
    lines = get_lines(file)
    lines = [line.split('\n')[0] for line in lines]
    lines = [line for line in lines if line != '']
    return lines


# limpia la lista de mensajes.
def delete_all_messages(file):
    with open(file, 'w') as f:
        f.write('')
