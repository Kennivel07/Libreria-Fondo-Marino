import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import os

# Obtenemos la carpeta donde está guardado el archivo .py actual (dentro de TP)
carpeta = os.path.dirname(os.path.abspath(__file__))

pygame.mixer.init()
##Lista principal de libros
libros = [
    {"título": "El Aleph", "autor": "Jorge Luis Borges", "género": "Novela", "año": "1949"},
    {"título": "Cien años de soledad", "autor": "Gabriel García Márquez", "género": "Novela", "año": "1967"},
    {"título": "El resplandor", "autor": "Stephen King", "género": "Terror", "año": "1977"},
    {"título": "Fundación", "autor": "Isaac Asimov", "género": "Ciencia ficción", "año": "1951"}
]
##Los libros q se ven actualmente en la lista.
libros_mostrados = []
##Lista de géneros 
géneros = ["Novela", "Fantasía", "Ciencia ficción", "Terror", "Romance",
           "Misterio", "Historia", "Aventura", "Comedia"]


##Muestra los libros en pantalla, ya sea todos o la lista que reciba.
def mostrar_libros(lista=None):
    ##Indica que se va a actualizar la variable creada fuera de esta función.
    global libros_mostrados
    if lista is None:
        libros_mostrados = libros
    else:
        libros_mostrados = lista
    ##Limpia la lista visual antes de cargar los libros actualizados.
    lista_libros.delete(0, tk.END)
    ##Recorre los libros y prepara el texto que se verá para cada uno.
    for libro in libros_mostrados:
        texto = libro["título"] + " - " + libro["autor"] + " - " + libro["año"] + " (" + libro["género"] + ")"
        lista_libros.insert(tk.END, texto)

def validar(título, autor, género, año):
    ##Valida que el título o autor estén completos.
    if título == "" or autor == "":
        messagebox.showwarning("Advertencia", "El título y el autor son obligatorios.")
        return False
    ##Valida que el género exista entre las opciones.
    if género not in géneros:
        messagebox.showwarning("Advertencia", "Ingrese un género de la lista disponible.")
        return False
    ##Valida que el campo de año sea sólo números.
    if not año.isdigit():
        messagebox.showwarning("Advertencia", "El año debe ser numérico.")
        return False
    ##Convierte el año a número y comprueba que esté entre 1500 y 2026.
    if int(año) < 1500 or int(año) > 2026:
        messagebox.showwarning("Advertencia", "El año debe estar entre 1500 y 2026.")
        return False
    return True


##Formulario para agregar o editar un libro.
def formulario(libro=None):
    ##Ventana secundaria proveniente de la principal.
    ventana = tk.Toplevel(ventana_principal)
    if libro is None:
        ventana.title("Agregar libro")
    else:
        ventana.title("Editar libro")
    ventana.geometry("400x350")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Título:").pack(pady=5)
    entrada_título = tk.Entry(ventana, width=40)
    entrada_título.pack()

    tk.Label(ventana, text="Autor:").pack(pady=5)
    entrada_autor = tk.Entry(ventana, width=40)
    entrada_autor.pack()

    tk.Label(ventana, text="Género:").pack(pady=5)
    tk.Label(ventana, text="Novela, Fantasía, Ciencia ficción, Terror, Romance,").pack()
    tk.Label(ventana, text="Misterio, Historia, Aventura o Comedia").pack()
    entrada_género = tk.Entry(ventana, width=40)
    entrada_género.pack()

    tk.Label(ventana, text="Año:").pack(pady=5)
    entrada_año = tk.Entry(ventana, width=40)
    entrada_año.pack()

    ##Si se está editando, completa los datos con los ingresados anteriormente.
    if libro is not None:
        entrada_título.insert(0, libro["título"])
        entrada_autor.insert(0, libro["autor"])
        entrada_género.insert(0, libro["género"])
        entrada_año.insert(0, libro["año"])

    ##Valida los datos y agrega un libro o modifica uno ya creado.
    def guardar():
        título = entrada_título.get()
        autor = entrada_autor.get()
        género = entrada_género.get()
        año = entrada_año.get()

        ##Valida que todo sea correcto para guardar el libro
        if validar(título, autor, género, año):
            if libro is None:
                nuevo_libro = {"título": título, "autor": autor,
                               "género": género, "año": año}
                libros.append(nuevo_libro)
                mensaje = "El libro fue agregado correctamente."
            else:
                libro["título"] = título
                libro["autor"] = autor
                libro["género"] = género
                libro["año"] = año
                mensaje = "El libro fue modificado correctamente."

            ##Actualiza la lista
            mostrar_libros()
            messagebox.showinfo("Éxito", mensaje)
            ventana.destroy()
            tk.Button(ventana, text="Guardar", command=con_sonido(guardar), width=20).pack(pady=20)
    tk.Button(ventana, text="Guardar", command=guardar, width=20).pack(pady=20)


##Agregar libro
def agregar_libro():
    formulario()


##Editar libro
def editar_libro():
    seleccion = lista_libros.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Debe seleccionar un libro.")
    else:
        posicion = seleccion[0]
        libro = libros_mostrados[posicion]
        formulario(libro)


##Eliminar libro
def eliminar_libro():
    seleccion = lista_libros.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Debe seleccionar un libro.")
    else:
        posicion = seleccion[0]
        libro = libros_mostrados[posicion]
        confirmar = messagebox.askyesno("Eliminar libro", "¿Está seguro de que desea eliminar este libro?")
        if confirmar:
            libros.remove(libro)
            mostrar_libros()
            messagebox.showinfo("Éxito", "El libro fue eliminado correctamente.")


##Filtrar libros dependiendo lo ingresado
def buscar_libro():
    ##Pasa a minúsculas para no perder resultados
    texto = entrada_busqueda.get().lower()
    resultados = []
    ##Revisa los libros y muestra coincidencias con la búsqueda
    for libro in libros:
        if (texto in libro["título"].lower() or texto in libro["autor"].lower()
                or texto in libro["género"].lower()):
            resultados.append(libro)
    mostrar_libros(resultados)


##Deja de mostrar lo seleccionado y vuelve a mostrar todo
def mostrar_todos():
    entrada_busqueda.delete(0, tk.END)
    mostrar_libros()

import pygame  # <--- 1. Importas pygame

##Ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Fondo Marino")
ventana_principal.geometry("750x550")
ventana_principal.resizable(False, False)
ventana_principal.config(bg="#e0f7fa")

try:
    # 1. Música de fondo en bucle
    ruta_musica = os.path.join(carpeta, "MUSICA.mp3")
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.play(loops=-1)  # loops=-1 hace que se repita infinitamente
except Exception as e:
    print(f"No se pudo cargar la música: {e}")
    
# 2. Cargar el sonido del botón
try:
    ruta_sonido = os.path.join(carpeta, "SONIDO.wav")
    sonido_clic = pygame.mixer.Sound(ruta_sonido)
except Exception as e:
    print(f"No se pudo cargar el sonido de los botones: {e}")

##Imagen de fondo
imagen_fondo = Image.open(os.path.join(carpeta, "FONDO.jfif"))
imagen_fondo = imagen_fondo.resize((750, 550))
fondo = ImageTk.PhotoImage(imagen_fondo)

label_fondo = tk.Label(ventana_principal, image=fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
label_fondo.lower()

def con_sonido(accion):
    def wrapper():
        try:
            sonido_clic.play() # Reproduce el efecto de sonido
        except:
            pass
        accion() # Ejecuta la función original del botón
    return wrapper

tk.Label(ventana_principal, text="Fondo Marino", font=("Times New Roman", 22, "bold"), bg="#e0f7fa").pack(pady=20)

##Buscador
frame_busqueda = tk.Frame(ventana_principal, bg="#e0f7fa")
frame_busqueda.pack(pady=10)
tk.Label(frame_busqueda, text="Buscar:", bg="#e0f7fa").pack(side=tk.LEFT, padx=5)
entrada_busqueda = tk.Entry(frame_busqueda, width=40)
entrada_busqueda.pack(side=tk.LEFT, padx=5)

tk.Button(frame_busqueda, text="Buscar", command=con_sonido(buscar_libro)).pack(side=tk.LEFT, padx=5)
tk.Button(frame_busqueda, text="Mostrar todos", command=con_sonido(mostrar_todos)).pack(side=tk.LEFT, padx=5)

#tk.Button(frame_busqueda, text="Buscar", command=buscar_libro).pack(side=tk.LEFT, padx=5)
#tk.Button(frame_busqueda, text="Mostrar todos", command=mostrar_todos).pack(side=tk.LEFT, padx=5)

##Lista de libros
lista_libros = tk.Listbox(ventana_principal, width=85, height=15)
lista_libros.pack(pady=15)

##Botones de la biblioteca
frame_botones = tk.Frame(ventana_principal , bg="#e0f7fa" )
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Agregar libro", command=con_sonido(agregar_libro), width=18).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Editar libro", command=con_sonido(editar_libro), width=18).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Eliminar libro", command=con_sonido(eliminar_libro), width=18).grid(row=0, column=2, padx=5)

#tk.Button(frame_botones, text="Agregar libro", command=agregar_libro, width=18).grid(row=0, column=0, padx=5)
#tk.Button(frame_botones, text="Editar libro", command=editar_libro, width=18).grid(row=0, column=1, padx=5)
#tk.Button(frame_botones, text="Eliminar libro", command=eliminar_libro, width=18).grid(row=0, column=2, padx=5)

mostrar_libros() 

ventana_principal.mainloop()
