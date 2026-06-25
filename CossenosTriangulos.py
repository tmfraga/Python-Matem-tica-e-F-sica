import tkinter as tk
from tkinter import messagebox
import math

def calcular_angulo():
    try:
        # Lado oposto ao ângulo que queremos (a) e lados adjacentes (b, c)
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())

        # Validação geométrica: a soma de dois lados deve ser maior que o terceiro
        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            messagebox.showerror("Erro", "Estes lados não formam um triângulo válido.")
            return

        # Cálculo do Cosseno de Alfa: cos(α) = (b² + c² - a²) / (2bc)
        cos_alfa = (b**2 + c**2 - a**2) / (2 * b * c)
        
        # Obter o ângulo em radianos e converter para graus
        angulo_rad = math.acos(cos_alfa)
        angulo_graus = math.degrees(angulo_rad)

        lbl_cos_val.config(text=f"cos(α) = {cos_alfa:.4f}", fg="blue")
        lbl_ang_val.config(text=f"α = {angulo_graus:.2f}°", fg="green")
        
    except ValueError:
        messagebox.showerror("Erro", "Insira valores numéricos válidos.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro no cálculo: {e}")

# Configuração da Janela
janela = tk.Tk()
janela.title("Engenharia: Cosseno de Alfa")
janela.geometry("400x450")

# Interface e Equação
tk.Label(janela, text="Obter Cosseno de α", font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(janela, text="Fórmula: cos(α) = (b² + c² - a²) / 2bc", font=("Arial", 11, "italic"), fg="red").pack()

# Entradas de Dados
frame_in = tk.Frame(janela)
frame_in.pack(pady=20)

tk.Label(frame_in, text="Lado a (oposto a α):").grid(row=0, column=0, pady=5, sticky="e")
entry_a = tk.Entry(frame_in, width=10)
entry_a.grid(row=0, column=1)

tk.Label(frame_in, text="Lado b (adjacente):").grid(row=1, column=0, pady=5, sticky="e")
entry_b = tk.Entry(frame_in, width=10)
entry_b.grid(row=1, column=1)

tk.Label(frame_in, text="Lado c (adjacente):").grid(row=2, column=0, pady=5, sticky="e")
entry_c = tk.Entry(frame_in, width=10)
entry_c.grid(row=2, column=1)

# Botão de Processamento
btn = tk.Button(janela, text="Calcular Cosseno e Ângulo", command=calcular_angulo, 
                bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn.pack(pady=10)

# Resultados
tk.Label(janela, text="Resultados:", font=("Arial", 10, "bold")).pack(pady=(10,0))
lbl_cos_val = tk.Label(janela, text="cos(α) = -", font=("Arial", 12))
lbl_cos_val.pack()

lbl_ang_val = tk.Label(janela, text="α = -", font=("Arial", 12, "bold"))
lbl_ang_val.pack()

janela.mainloop()
