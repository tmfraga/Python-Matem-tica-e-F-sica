
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def calcular_rpm():
    try:
        frequencia = float(entry_frequencia.get())
        polos = int(entry_polos.get())
        if polos <= 0:
            raise ValueError("Número de polos deve ser maior que zero.")
        rpm = (120 * frequencia) / polos
        label_resultado.config(text=f"Velocidade: {rpm:.2f} RPM")
        salvar_resultado(rpm, frequencia, polos)
    except ValueError as e:
        messagebox.showerror("Erro", f"Entrada inválida: {e}")

def limpar_campos():
    entry_frequencia.delete(0, tk.END)
    entry_polos.delete(0, tk.END)
    label_resultado.config(text="Velocidade: --- RPM")

def salvar_resultado(rpm, frequencia, polos):
    try:
        with open("resultado_motor.txt", "a", encoding="utf-8") as arquivo:
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            arquivo.write(f"{data_hora} | Frequência: {frequencia} Hz | Polos: {polos} | RPM: {rpm:.2f}\n")
    except Exception as e:
        messagebox.showerror("Erro ao salvar", f"Não foi possível salvar o arquivo: {e}")

# Criando janela principal
janela = tk.Tk()
janela.title("Cálculo de RPM - Motor Síncrono")
janela.geometry("320x250")

# Labels e entradas
tk.Label(janela, text="Frequência (Hz):").pack(pady=5)
entry_frequencia = tk.Entry(janela)
entry_frequencia.pack(pady=5)

tk.Label(janela, text="Número de Polos:").pack(pady=5)
entry_polos = tk.Entry(janela)
entry_polos.pack(pady=5)

# Botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn_calcular = tk.Button(frame_botoes, text="Calcular RPM", command=calcular_rpm)
btn_calcular.grid(row=0, column=0, padx=5)

btn_limpar = tk.Button(frame_botoes, text="Limpar Campos", command=limpar_campos)
btn_limpar.grid(row=0, column=1, padx=5)

# Resultado
label_resultado = tk.Label(janela, text="Velocidade: --- RPM", font=("Arial", 12))
label_resultado.pack(pady=10)

janela.mainloop()
