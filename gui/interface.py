import tkinter as tk
from tkinter import filedialog
import os

class TestCaseGeneratorApp:
    """
    Clase principal que construye la interfaz gráfica y gestiona los eventos de usuario
    para ingresar datos, seleccionar archivos y generar los casos de prueba.
    """

    def __init__(self, root):
        """
        Constructor de la clase que inicializa la ventana y sus componentes.

        Args:
            root (tk.Tk): Ventana raíz de Tkinter.
        """
        self.root = root
        self.root.title("TEST AI")
        self.root.geometry("500x550")
        self.root.config(bg="#FFF")

        self.center_window()
        self.selected_files = []

        self.create_widgets()

    def center_window(self):
        """Centrar la ventana principal en la pantalla."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 500
        window_height = 550

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    def create_widgets(self):
        """Crear y configurar todos los widgets de la interfaz."""
        frame = tk.Frame(self.root, bg="black", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=440, height=500)

        # Botones tipo ventana estilo Mac
        tk.Canvas(frame, bg="#FF5F57", height=10, width=10, highlightthickness=0).place(x=10, y=10)
        tk.Canvas(frame, bg="#FFBD2E", height=10, width=10, highlightthickness=0).place(x=25, y=10)
        tk.Canvas(frame, bg="#28C840", height=10, width=10, highlightthickness=0).place(x=40, y=10)

        # Título
        tk.Label(frame, text="bSide", font=("Helvetica", 18, "bold"),
                 fg="#FFD700", bg="black").pack(pady=(30, 10))

        # Selector de modo: Standard o Custom
        self.mode = tk.StringVar(value="standard")
        mode_frame = tk.Frame(frame, bg="black")
        mode_frame.pack(pady=(0, 10))

        tk.Label(mode_frame, text="Mode:", font=("Arial", 10, "bold"),
                 fg="white", bg="#000").pack(side="left", padx=(0, 15))
        tk.Radiobutton(mode_frame, text="Standard", variable=self.mode, value="standard",
                       command=self.update_mode, bg="#000", fg="white", selectcolor="#1B1036").pack(side="left")
        tk.Radiobutton(mode_frame, text="Custom", variable=self.mode, value="custom",
                       command=self.update_mode, bg="#000", fg="white", selectcolor="#1B1036").pack(side="left")

        # Prompt
        tk.Label(frame, text="Prompt:", font=("Helvetica", 10, "bold"),
                 fg="white", bg="#000").pack(anchor="w", padx=20)
        self.prompt_entry = tk.Text(frame, height=10, bg="#000000", fg="#FFD700", insertbackground="black")
        self.prompt_entry.pack(padx=20, fill="x")

        # Área personalizada (solo visible en modo Custom)
        self.custom_frame = tk.Frame(frame, bg="#000")
        self.custom_field = tk.Entry(self.custom_frame, bg="#000", fg="#FFD700")
        tk.Label(self.custom_frame, text="Campo personalizado:", bg="#000", fg="white").pack(anchor="w")
        self.custom_field.pack(fill="x")

        # Botón para seleccionar archivos
        tk.Button(frame, text="Seleccionar archivos", command=self.select_files,
                  bg="#FFF", fg="black", font=("Arial", 11, "bold"),
                  relief="flat", width=20).pack(pady=(15, 5))

        # Etiqueta con los archivos seleccionados
        self.file_label = tk.Label(frame, text="Archivo", fg="#FFF", bg="#000")
        self.file_label.pack()

        # Botón para generar los casos de prueba
        tk.Button(frame, text="    Generar Casos    ", command=self.generate,
                  bg="#FFF", fg="black", font=("Arial", 11, "bold"),
                  relief="flat", width=20).pack(pady=(15, 10))

        # Pie de página
        tk.Label(frame, text="Quality Assurance",
                 fg="#FFD700", bg="#000", font=("Arial", 10)).pack(side="bottom", pady=10)

        # Mostrar u ocultar campos personalizados según modo
        self.update_mode()

    def update_mode(self):
        """Mostrar u ocultar campos personalizados según el modo seleccionado."""
        if self.mode.get() == "custom":
            self.custom_frame.pack(padx=20, pady=(5, 5), fill="x")
        else:
            self.custom_frame.pack_forget()

    def select_files(self):
        """Abrir un diálogo para seleccionar archivos y mostrar los nombres seleccionados."""
        files = filedialog.askopenfilenames(title="Seleccionar archivos")
        self.selected_files = files
        file_names = ', '.join([f.split(os.sep)[-1] for f in files])
        self.file_label.config(text=file_names or "Archivo")

    def generate(self):
        """
        Obtener datos del usuario y lanzar el procesamiento para generar la respuesta de Claude
        y el archivo Excel.
        """
        prompt = self.prompt_entry.get("1.0", "end").strip()  # Obtener el prompt del usuario
        custom_text = self.custom_field.get().strip() if self.mode.get() == "custom" else ""  # Campo personalizado

        # Mostrar los valores para depuración
        print("Modo:", self.mode.get())
        print("Prompt:", prompt)
        print("Campo personalizado:", custom_text)
        print("Archivos seleccionados:", self.selected_files)

        # Llamar a la función para generar la matriz con base en el prompt y la plantilla seleccionada
        template_type = self.mode.get()  # Obtener el tipo de plantilla seleccionado (standard o custom)
        try:
            # Simulación de procesamiento para mostrar en consola
            print(f"Procesando con plantilla {template_type}...")

        except Exception as e:
            print(f"Error al generar la matriz: {str(e)}")


def iniciar_interfaz():
    """Inicializa la interfaz gráfica principal."""
    root = tk.Tk()
    app = TestCaseGeneratorApp(root)
    root.mainloop()


# Permite ejecutar la app directamente si se corre este archivo como script
if __name__ == "__main__":
    iniciar_interfaz()

