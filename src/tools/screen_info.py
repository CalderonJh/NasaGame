import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


# obtener el tamaño de la pantalla.
def get_info():
    return ancho, alto
