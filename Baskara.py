import tkinter as tk
from tkinter import messagebox
import cmath

def resolver_equacao():
    try:
        # Obtendo os valores das entradas
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())

        if a == 0:
            messagebox.showerror("Erro", "O coeficiente 'a' não pode ser zero em uma equação do 2º grau.")
            return

        # Cálculo do Discriminante (Delta)
        delta = (b**2) - (4*a*c)

        # Cálculo das raízes usando cmath para suportar números complexos
        x1 = (-b + cmath.sqrt(delta)) / (2*a)
        x2 = (-b - cmath.sqrt(delta)) / (2*a)

        # Formatação da saída
        if delta >= 0:
            tipo = "Raízes Reais"
            resultado = f"x1 = {x1.real:.2f}\nx2 = {x2.real:.2f}"
        else:
            tipo = "Raízes Imaginárias (Complexas)"
            resultado = f"x1 = {x1:.2f}\nx2 = {x2:.2f}"

        lbl_tipo_val.config(text=tipo, fg="blue" if delta >= 0 else "red")
        lbl_res_val.config(text=resultado)
        lbl_delta_val.config(text=f"{delta:.2f}")

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira apenas valores numéricos.")

# Configuração da Janela Principal
janela = tk.Tk()
janela.title("Calculadora de Equação do 2º Grau")
janela.geometry("400x450")

# Interface Estilizada
tk.Label(janela, text="Resolutor de Equação Quadrática", font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(janela, text="ax² + bx + c = 0", font=("Arial", 10, "italic")).pack()

# frames para entrada
frame_input = tk.Frame(janela)
frame_input.pack(pady=20)

tk.Label(frame_input, text="a:").grid(row=0, column=0)
entry_a = tk.Entry(frame_input, width=10)
entry_a.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="b:").grid(row=1, column=0)
entry_b = tk.Entry(frame_input, width=10)
entry_b.grid(row=1, column=1, padx=5)

tk.Label(frame_input, text="c:").grid(row=2, column=0)
entry_c = tk.Entry(frame_input, width=10)
entry_c.grid(row=2, column=1, padx=5)

# Botão de Cálculo
btn_calcular = tk.Button(janela, text="Calcular Raízes", command=resolver_equacao, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_calcular.pack(pady=10)

# Área de Resultados
tk.Label(janela, text="Delta (Δ):").pack()
lbl_delta_val = tk.Label(janela, text="-", font=("Arial", 10, "bold"))
lbl_delta_val.pack()

tk.Label(janela, text="Tipo de Raízes:").pack(pady=(10,0))
lbl_tipo_val = tk.Label(janela, text="-", font=("Arial", 10, "bold"))
lbl_tipo_val.pack()

tk.Label(janela, text="Resultado:").pack(pady=(10,0))
lbl_res_val = tk.Label(janela, text="-", font=("Arial", 12, "bold"), justify="left")
lbl_res_val.pack()

janela.mainloop()
