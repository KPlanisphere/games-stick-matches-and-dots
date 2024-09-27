import random
import tkinter as tk
from tkinter import messagebox

# Función principal que controla el turno del jugador
def jugar_palillos():
    global X, N, turno, label_palillos, entry_palillos
    
    # Verificar que el jugador haya ingresado un número válido
    try:
        tomar = int(entry_palillos.get())  # Convertir la entrada a entero
        # Verificar que el número esté dentro del rango permitido
        if tomar < 1 or tomar > N or tomar > X:
            messagebox.showwarning("Movimiento inválido", f"Debes tomar entre 1 y {min(N, X)} palillos.")
            return
    except ValueError:
        messagebox.showwarning("Entrada inválida", "Debes ingresar un número.")  # Mostrar advertencia si no es un número
        return
    
    # Reducir el número de palillos restantes
    X -= tomar
    label_palillos.config(text=f"Palillos restantes: {X}")  # Actualizar el número de palillos en la pantalla
    
    # Verificar si el jugador ha ganado
    if X == 0:
        messagebox.showinfo("¡Felicidades!", "¡Has ganado!")  # Mostrar mensaje de victoria
        root.quit()  # Cerrar la ventana del juego
        return
    
    # Cambiar el turno al programa
    turno = 0  # Cambiar a turno del programa
    tomar_programa()  # Llamar a la función del turno del programa

# Función que controla el turno del programa (la computadora)
def tomar_programa():
    global X, N, turno, label_palillos

    # El programa juega de manera estratégica
    if X % (N + 1) == 0:
        # Si X es múltiplo de (N+1), toma una cantidad aleatoria de palillos
        tomar = random.randint(1, N)
    else:
        # Toma de manera estratégica X % (N + 1) palillos
        tomar = X % (N + 1)

    # Mostrar un mensaje con la cantidad de palillos que toma el programa
    messagebox.showinfo("Turno del programa", f"El programa toma {tomar} palillos.")
    
    # Reducir el número de palillos restantes
    X -= tomar
    label_palillos.config(text=f"Palillos restantes: {X}")  # Actualizar el número de palillos en la pantalla

    # Verificar si el programa ha ganado
    if X == 0:
        messagebox.showinfo("Fin del juego", "El programa gana.")  # Mostrar mensaje si el programa gana
        root.quit()  # Cerrar la ventana del juego
    else:
        # Cambiar el turno al jugador
        turno = 1  # Cambiar el turno al jugador

# Función para inicializar el juego
def iniciar_juego():
    global X, N, turno, entry_palillos, label_palillos, root
    
    # Inicializar los valores del juego
    try:
        X = int(entry_palillos_inicial.get())  # Obtener el número inicial de palillos
        N = int(entry_max_palillos.get())  # Obtener el número máximo de palillos que se pueden tomar por turno
    except ValueError:
        messagebox.showerror("Entrada inválida", "Introduce valores válidos para los palillos.")  # Mostrar error si los valores no son válidos
        return

    # Verificar que los valores sean mayores que cero
    if X <= 0 or N <= 0:
        messagebox.showerror("Entrada inválida", "Los valores deben ser mayores que cero.")
        return

    # Limpiar la pantalla para el juego
    for widget in root.winfo_children():
        widget.destroy()  # Eliminar todos los widgets anteriores
    
    # Mostrar los palillos restantes
    label_palillos = tk.Label(root, text=f"Palillos restantes: {X}", font=("Arial", 18))
    label_palillos.pack(pady=10)

    # Crear entrada para que el jugador elija cuántos palillos tomar
    tk.Label(root, text=f"¿Cuántos palillos tomas (1 a {N})?", font=("Arial", 14)).pack(pady=5)
    entry_palillos = tk.Entry(root, font=("Arial", 14))  # Caja de entrada donde el jugador ingresa su movimiento
    entry_palillos.pack(pady=5)

    # Botón para tomar los palillos
    tk.Button(root, text="Tomar palillos", command=jugar_palillos, font=("Arial", 14)).pack(pady=10)
    
    turno = 1  # Iniciar con el turno del jugador

# Configuración de la ventana principal
root = tk.Tk()
root.title("Juego de los Palillos")  # Título de la ventana
root.geometry("550x250")  # Tamaño de la ventana

# Variables globales
X = 0  # Cantidad inicial de palillos
N = 0  # Máxima cantidad de palillos por turno
turno = 1  # El jugador comienza primero

# Entrada para la cantidad inicial de palillos
tk.Label(root, text="Introduce la cantidad de palillos inicial:", font=("Arial", 14)).pack(pady=5)
entry_palillos_inicial = tk.Entry(root, font=("Arial", 14))  # Entrada para la cantidad de palillos inicial
entry_palillos_inicial.pack(pady=5)

# Entrada para la cantidad máxima de palillos por turno
tk.Label(root, text="Introduce la cantidad máxima de palillos por turno:", font=("Arial", 14)).pack(pady=5)
entry_max_palillos = tk.Entry(root, font=("Arial", 14))  # Entrada para la cantidad máxima de palillos por turno
entry_max_palillos.pack(pady=5)

# Botón para comenzar el juego
tk.Button(root, text="Iniciar juego", command=iniciar_juego, font=("Arial", 14)).pack(pady=20)

# Iniciar el bucle principal de tkinter
root.mainloop()  # Mantener la ventana activa
