# main.py

from gui.interface import TestCaseGeneratorApp
import tkinter as tk

def main():
    """Inicializa la interfaz gráfica y arranca la aplicación."""
    root = tk.Tk()  # Crea la ventana principal de Tkinter
    app = TestCaseGeneratorApp(root)  # Crea la instancia de la aplicación
    root.mainloop()  # Inicia el bucle de eventos de la interfaz gráfica

# Permite ejecutar la app directamente si se corre este archivo como script
if __name__ == "__main__":
    main()