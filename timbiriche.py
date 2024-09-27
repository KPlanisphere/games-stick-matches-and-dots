import tkinter as tk
from tkinter import simpledialog
import random
import time

class Timbiriche:
    def __init__(self, root, player_choice, size=5):
        """
        Constructor de la clase Timbiriche. Inicializa el tablero y sus propiedades.
        
        Parámetros:
        - root: la ventana principal de tkinter.
        - player_choice: determina si el usuario es el jugador 1 o 2.
        - size: tamaño del tablero (mínimo de 5x5).
        """
        self.root = root
        self.size = max(5, size)        # Asegura que el tamaño mínimo sea 5x5
        self.grid_size = self.size - 1  # Tamaño de la cuadrícula interna donde se trazan las líneas
        self.cell_size = 50             # Tamaño en píxeles de cada celda
        self.canvas_size = self.size * self.cell_size   # Tamaño del área de dibujo del canvas
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size)  # Área de dibujo
        self.canvas.pack()
        self.lines = set()              # Conjunto que almacena las líneas ya trazadas
        self.squares = {}               # Diccionario para almacenar los cuadros completados
        self.player_choice = player_choice  # Elección del jugador por el usuario (1 o 2)
        self.current_player = 1         # Jugador actual, empieza en 1
        self.player_colors = {1: 'red', 2: 'blue'}  # Colores de los jugadores
        self.score = {1: 0, 2: 0}       # Puntaje de ambos jugadores
        self.first_click = None         # Primer clic de la línea (punto inicial)

        self.draw_grid()                # Dibuja la cuadrícula de puntos
        self.canvas.bind("<Button-1>", self.click_event)  # Vincula el evento de clic del ratón

        # Si el turno inicial no es del usuario, ejecuta el turno de la computadora tras 1 segundo
        if self.current_player != self.player_choice:
            self.root.after(1000, self.computer_turn)

    def draw_grid(self):
        """Dibuja la cuadrícula de puntos en el canvas"""
        for i in range(self.size):
            for j in range(self.size):
                x = (i + 0.5) * self.cell_size  # Coordenada x del punto
                y = (j + 0.5) * self.cell_size  # Coordenada y del punto
                self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")  # Crea un punto circular en la cuadrícula

    def click_event(self, event):
        """Maneja los eventos de clic del usuario para crear una línea entre dos puntos"""
        if self.current_player == self.player_choice:       # Solo permite interacción si es el turno del jugador
            x, y = event.x, event.y                         # Obtiene las coordenadas del clic
            clicked_point = self.get_closest_point(x, y)    # Obtiene el punto más cercano a las coordenadas clicadas

            if clicked_point:

                if self.first_click is None:
                    # Si no hay primer clic registrado, lo almacena
                    self.first_click = clicked_point
                else:
                    # Si ya hay un primer clic, intenta trazar la línea
                    second_click = clicked_point

                    if self.is_valid_line(self.first_click, second_click):  # Verifica si la línea es válida (adyacente)
                        line = (self.first_click, second_click)
                        
                        # Verifica si la línea no ha sido trazada antes (en ambos sentidos)
                        if line not in self.lines and self.reverse_line(line) not in self.lines:
                            self.lines.add(line)  # Agrega la línea al conjunto de líneas trazadas
                            self.animate_line(line)  # Anima la creación de la línea
                            completed_squares = self.check_square(line)  # Verifica si se ha completado un cuadro

                            if not completed_squares:
                                # Si no se completa un cuadro, cambia de jugador
                                self.current_player = 3 - self.current_player
                            else:
                                self.update_score()  # Si se completó un cuadro, actualiza el puntaje

                            self.first_click = None  # Reinicia el primer clic para el próximo turno

                            # Si ahora es turno de la computadora, inicia su turno tras 1 segundo
                            if self.current_player != self.player_choice:
                                self.root.after(1000, self.computer_turn)
                    else:
                        # Si la línea no es válida, reinicia el primer clic
                        self.first_click = None

    def is_valid_line(self, point1, point2):
        """Verifica si una línea entre dos puntos es válida (adyacente horizontal o verticalmente)"""
        x1, y1 = point1
        x2, y2 = point2

        # Verifica que la línea sea horizontal o vertical (adyacente) pero no diagonal
        if (x1 == x2 and abs(y1 - y2) == self.cell_size) or (y1 == y2 and abs(x1 - x2) == self.cell_size):
            return True
        return False

    def get_closest_point(self, x, y):
        """Obtiene el punto más cercano en la cuadrícula a las coordenadas dadas"""
        for i in range(self.size):
            for j in range(self.size):
                px, py = (i + 0.5) * self.cell_size, (j + 0.5) * self.cell_size
                if abs(x - px) < 10 and abs(y - py) < 10:  # Si está cerca de un punto, lo devuelve
                    return (px, py)
        return None

    def reverse_line(self, line):
        """Retorna la línea en orden inverso (punto2, punto1)"""
        return (line[1], line[0])

    def animate_line(self, line):
        """Anima la creación de una línea entre dos puntos"""
        (x1, y1), (x2, y2) = line
        steps = 10  # Número de pasos para la animación
        for i in range(steps + 1):
            x = x1 + (x2 - x1) * i / steps  # Interpola la posición x
            y = y1 + (y2 - y1) * i / steps  # Interpola la posición y
            # Dibuja la línea en la posición interpolada con el color del jugador actual
            self.canvas.create_line(x1, y1, x, y, fill=self.player_colors[self.current_player], width=2)
            self.root.update()  # Actualiza el canvas
            time.sleep(0.02)  # Pausa breve para la animación

    def computer_turn(self):
        """Simula el turno de la computadora, elige una línea basada en completar cuadros cuando sea posible."""
        
        available_lines = self.get_available_lines()
        if not available_lines:
            print("No hay más líneas disponibles. El juego ha terminado.")
            return  # Termina el turno de la computadora si no hay líneas disponibles

        lines_to_complete_square = []
        safe_lines = []
        dangerous_lines = []
        
        # 1. Clasifica las líneas según si completan cuadros, son seguras, o peligrosas
        for line in available_lines:
            squares_for_line = self.possible_squares(line)
            is_dangerous = False
            completes_square = False
            
            for square in squares_for_line:
                filled_lines = sum(1 for l in square if l in self.lines or self.reverse_line(l) in self.lines)
                
                # Si el cuadro ya tiene 3 líneas, completar esta línea cerrará el cuadro
                if filled_lines == 3:
                    completes_square = True
                    break
                elif filled_lines == 2:
                    is_dangerous = True

            if completes_square:
                lines_to_complete_square.append(line)
            elif is_dangerous:
                dangerous_lines.append(line)
            else:
                safe_lines.append(line)
        
        # 2. Estrategia: Priorizar completar cuadros cuando sea posible
        if lines_to_complete_square:
            # Elige una línea que complete un cuadro
            line = random.choice(lines_to_complete_square)
        elif safe_lines:
            # Si no hay cuadros para completar, elige una línea segura
            line = random.choice(safe_lines)
        elif dangerous_lines:
            # Como último recurso, elige de las líneas peligrosas
            line = random.choice(dangerous_lines)
        else:
            print("No hay más líneas disponibles para la computadora.")
            return  # Termina el turno si no hay líneas para trazar

        # 3. Realiza la jugada
        self.lines.add(line)
        self.animate_line(line)
        
        completed_squares = self.check_square(line)
        
        if not completed_squares:
            # Cambia de jugador si no completó un cuadro
            self.current_player = 3 - self.current_player
        else:
            self.update_score()  # Si completó un cuadro, actualiza el puntaje

        # Si sigue siendo el turno de la computadora, vuelve a jugar tras 1 segundo
        if self.current_player != self.player_choice:
            self.root.after(1000, self.computer_turn)



    def get_available_lines(self):
        """Obtiene todas las líneas disponibles para ser trazadas en el tablero"""
        available_lines = []

        for i in range(self.grid_size):  # Recorre la cuadrícula interna para líneas horizontales y verticales
            for j in range(self.grid_size):
                # Línea horizontal: Se dibuja desde (i, j) hasta (i+1, j)
                line_horizontal = (
                    ((i + 0.5) * self.cell_size, (j + 0.5) * self.cell_size), 
                    ((i + 1.5) * self.cell_size, (j + 0.5) * self.cell_size)
                )
                if line_horizontal not in self.lines and self.reverse_line(line_horizontal) not in self.lines:
                    available_lines.append(line_horizontal)

                # Línea vertical: Se dibuja desde (i, j) hasta (i, j+1)
                line_vertical = (
                    ((i + 0.5) * self.cell_size, (j + 0.5) * self.cell_size), 
                    ((i + 0.5) * self.cell_size, (j + 1.5) * self.cell_size)
                )
                if line_vertical not in self.lines and self.reverse_line(line_vertical) not in self.lines:
                    available_lines.append(line_vertical)

        # Añadir las líneas del borde derecho e inferior
        # Líneas horizontales de la última fila
        for i in range(self.grid_size):
            line = (
                ((i + 0.5) * self.cell_size, (self.grid_size + 0.5) * self.cell_size), 
                ((i + 1.5) * self.cell_size, (self.grid_size + 0.5) * self.cell_size)
            )
            if line not in self.lines and self.reverse_line(line) not in self.lines:
                available_lines.append(line)

        # Líneas verticales de la última columna
        for j in range(self.grid_size):
            line = (
                ((self.grid_size + 0.5) * self.cell_size, (j + 0.5) * self.cell_size), 
                ((self.grid_size + 0.5) * self.cell_size, (j + 1.5) * self.cell_size)
            )
            if line not in self.lines and self.reverse_line(line) not in self.lines:
                available_lines.append(line)

        return available_lines



    def check_square(self, line):
        """Verifica si la línea actual completa un cuadro y lo registra"""
        completed_squares = []
        for square in self.possible_squares(line):  # Revisa los cuadros asociados a la línea actual
            # Verifica si todas las líneas de un cuadro están trazadas
            if all(l in self.lines or self.reverse_line(l) in self.lines for l in square):
                self.squares[square] = self.current_player  # Asigna el cuadro al jugador actual
                self.fill_square(square)  # Rellena el cuadro con el color del jugador
                completed_squares.append(square)

        return completed_squares

    def possible_squares(self, line):
        """Obtiene los posibles cuadros que podrían completarse con la línea actual"""
        squares = []
        (x1, y1), (x2, y2) = line

        # Cuadro a la izquierda o derecha de una línea vertical
        if x1 == x2 and abs(y1 - y2) == self.cell_size:
            # Cuadro a la izquierda
            left_square = (
                ((x1 - self.cell_size, y1), (x1, y1)),
                ((x1 - self.cell_size, y2), (x1, y2)),
                ((x1 - self.cell_size, y1), (x1 - self.cell_size, y2)),
                ((x1, y1), (x1, y2))
            )
            squares.append(left_square)

            # Cuadro a la derecha
            right_square = (
                ((x1, y1), (x1 + self.cell_size, y1)),
                ((x1, y2), (x1 + self.cell_size, y2)),
                ((x1, y1), (x1, y2)),
                ((x1 + self.cell_size, y1), (x1 + self.cell_size, y2))
            )
            squares.append(right_square)

        # Cuadro arriba o abajo de una línea horizontal
        if y1 == y2 and abs(x1 - x2) == self.cell_size:
            # Cuadro arriba
            upper_square = (
                ((x1, y1 - self.cell_size), (x1, y1)),
                ((x2, y2 - self.cell_size), (x2, y2)),
                ((x1, y1 - self.cell_size), (x2, y2 - self.cell_size)),
                ((x1, y1), (x2, y2))
            )
            squares.append(upper_square)

            # Cuadro abajo
            lower_square = (
                ((x1, y1), (x1, y1 + self.cell_size)),
                ((x2, y2), (x2, y2 + self.cell_size)),
                ((x1, y1 + self.cell_size), (x2, y2 + self.cell_size)),
                ((x1, y1), (x2, y2))
            )
            squares.append(lower_square)

        return squares

    def fill_square(self, square):
        """Rellena el cuadro completado con el color del jugador"""
        x1, y1 = square[0][0]
        x2, y2 = square[1][1]
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.player_colors[self.current_player])

    def update_score(self):
        """Actualiza el marcador de los jugadores"""
        # Suma los cuadros completados por el jugador actual
        self.score[self.current_player] = sum(1 for s in self.squares.values() if s == self.current_player)
        print(f"Jugador 1 (rojo): {self.score[1]} | Jugador 2 (azul): {self.score[2]}")
        self.check_winner()  # Verifica si el juego ha terminado

    def check_winner(self):
        """Verifica si ya se han completado todos los cuadros para determinar un ganador"""
        total_squares = self.grid_size * self.grid_size  # Número total de cuadros posibles
        if len(self.squares) == total_squares:
            if self.score[1] == self.score[2]:
                print("¡El juego ha terminado en empate!")  # Imprime empate si ambos puntajes son iguales
            else:
                winner = max(self.score, key=self.score.get)  # Determina el ganador según el puntaje
                print(f"¡El jugador {winner} ha ganado!")  # Imprime el ganador en la consola


if __name__ == "__main__":
    root = tk.Tk()

    # Solicita al usuario el tamaño del tablero
    size = simpledialog.askinteger("Tamaño del Tablero", "Introduce el tamaño del tablero (mínimo 5):", minvalue=5)
    
    # Solicita al usuario que elija ser el jugador 1 o 2
    player_choice = simpledialog.askinteger("Jugador", "¿Quieres ser el jugador 1 o 2?", minvalue=1, maxvalue=2)

    # Crea una instancia del juego y arranca la interfaz gráfica
    game = Timbiriche(root, player_choice, size)
    root.mainloop()