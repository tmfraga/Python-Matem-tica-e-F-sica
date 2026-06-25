import tkinter as tk
from tkinter import messagebox
import math

def calcular_lei_cossenos():
    try:
        # b e c são os lados conhecidos, angulo_graus é o ângulo entre eles
        b = float(entry_b.get())
        c = float(entry_c.get())
        angulo_graus = float(entry_ang.get())

        # O Python calcula seno e cosseno em RADIANOS. 
        # Precisamos converter o que o usuário digita (Graus) para Radianos.
        angulo_rad = math.radians(angulo_graus)

        # Fórmula: a² = b² + c² - 2bc * cos(alpha)
        a_quadrado = (b**2) + (c**2) - (2 * b * c * math.cos(angulo_rad))
        
        # O lado 'a' é a raiz quadrada do resultado
        a = math.sqrt(a_quadrado)

        lbl_res_val.config(text=f"Lado a = {a:.4f}", fg="blue")
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira apenas valores numéricos válidos.")

# Configuração da Janela
janela = tk.Tk()
janela.title("Calculadora: Lei dos Cossenos")
janela.geometry("350x400")

# Título e Fórmula
tk.Label(janela, text="Lei dos Cossenos", font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(janela, text="a² = b² + c² - 2bc · cos(α)", font=("Arial", 10, "italic")).pack()

# Entradas
frame_in = tk.Frame(janela)
frame_in.pack(pady=20)

tk.Label(frame_in, text="Lado b:").grid(row=0, column=0, pady=5)
entry_b = tk.Entry(frame_in, width=10)
entry_b.grid(row=0, column=1)

tk.Label(frame_in, text="Lado c:").grid(row=1, column=0, pady=5)
entry_c = tk.Entry(frame_in, width=10)
entry_c.grid(row=1, column=1)

tk.Label(frame_in, text="Ângulo α (°):").grid(row=2, column=0, pady=5)
entry_ang = tk.Entry(frame_in, width=10)
entry_ang.grid(row=2, column=1)

# Botão
btn = tk.Button(janela, text="Calcular Lado Oposto (a)", command=calcular_lei_cossenos, 
                bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
btn.pack(pady=10)

# Resultado
tk.Label(janela, text="Resultado:").pack(pady=(10,0))
lbl_res_val = tk.Label(janela, text="-", font=("Arial", 14, "bold"))
lbl_res_val.pack()

janela.mainloop()
