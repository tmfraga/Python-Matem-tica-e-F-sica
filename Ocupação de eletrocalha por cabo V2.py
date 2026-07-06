
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math

# Tabela completa conforme imagem
cabos = [
    {"secao": 1.5, "diametro": 4.68, "material": "HEPR", "tensao": "0,6/1KV", "cabo": "1,5mm² - 0,6/1KV-HEPR"},
    {"secao": 2.5, "diametro": 5.33, "material": "HEPR", "tensao": "0,6/1KV", "cabo": "2,5mm² - 0,6/1KV-HEPR"},
    {"secao": 4, "diametro": 5.83, "material": "HEPR", "tensao": "0,6/1KV", "cabo": "4mm² - 0,6/1KV-HEPR"},
    {"secao": 6, "diametro": 6.38, "material": "HEPR", "tensao": "0,6/1KV", "cabo": "6mm² - 0,6/1KV-HEPR"},
    {"secao": 10, "diametro": 7.3, "material": "HEPR", "tensao": "0,6/1KV", "cabo": "10mm² - 0,6/1KV-HEPR"},
    {"secao": 1.5, "diametro": 2.9, "material": "HEPR", "tensao": "750V", "cabo": "1,5mm² - 750V-HEPR"},
    {"secao": 2.5, "diametro": 3.54, "material": "HEPR", "tensao": "750V", "cabo": "2,5mm² - 750V-HEPR"},
    {"secao": 4, "diametro": 4.05, "material": "HEPR", "tensao": "750V", "cabo": "4mm² - 750V-HEPR"},
    {"secao": 6, "diametro": 4.61, "material": "HEPR", "tensao": "750V", "cabo": "6mm² - 750V-HEPR"},
    {"secao": 1.5, "diametro": 4.9, "material": "PVC", "tensao": "0,6/1KV", "cabo": "1,5mm² - 0,6/1KV-PVC"},
    {"secao": 2.5, "diametro": 5.34, "material": "PVC", "tensao": "0,6/1KV", "cabo": "2,5mm² - 0,6/1KV-PVC"},
    {"secao": 4, "diametro": 6.45, "material": "PVC", "tensao": "0,6/1KV", "cabo": "4mm² - 0,6/1KV-PVC"},
    {"secao": 6, "diametro": 7.01, "material": "PVC", "tensao": "0,6/1KV", "cabo": "6mm² - 0,6/1KV-PVC"},
    {"secao": 10, "diametro": 8.46, "material": "PVC", "tensao": "0,6/1KV", "cabo": "10mm² - 0,6/1KV-PVC"},
    {"secao": 16, "diametro": 8.46, "material": "HEPR", "tensao": "0,6/1KV", "cabo": "16mm² - 0,6/1KV-HEPR"}
]

circuitos = []

def adicionar_circuito():
    try:
        nome = entry_nome.get().strip()
        quantidade = int(entry_quantidade.get())
        material = var_material.get()
        tensao = var_tensao.get()
        secao = float(combo_secao.get())

        if not nome:
            raise ValueError("Informe o nome do circuito.")

        cabo_encontrado = None
        for cabo in cabos:
            if cabo["material"] == material and cabo["tensao"] == tensao and cabo["secao"] == secao:
                cabo_encontrado = cabo
                break

        if cabo_encontrado is None:
            raise ValueError("Combinação não encontrada na tabela.")

        circuitos.append({"nome": nome, "quantidade": quantidade, "cabo": cabo_encontrado})
        atualizar_lista()
        entry_nome.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)
        combo_secao.set("")
    except ValueError as e:
        messagebox.showerror("Erro", f"Entrada inválida: {e}")

def atualizar_lista():
    lista_circuitos.delete(0, tk.END)
    for i, c in enumerate(circuitos, start=1):
        lista_circuitos.insert(tk.END, f"{i}. {c['nome']} | {c['quantidade']} cabos | {c['cabo']['cabo']}")

def calcular_ocupacao():
    try:
        largura = float(entry_largura.get())
        altura = float(entry_altura.get())
        area_eletrocalha = largura * altura

        area_total_cabos = 0
        for c in circuitos:
            diametro = c['cabo']['diametro']
            area_cabo = math.pi * (diametro / 2) ** 2
            area_total_cabos += area_cabo * c['quantidade']

        fator = (area_total_cabos / area_eletrocalha) * 100
        conforme = "CONFORME" if fator <= 40 else "NÃO CONFORME"

        resultado = (f"Área eletrocalha: {area_eletrocalha:.2f} mm²\n"
                     f"Área ocupada: {area_total_cabos:.2f} mm²\n"
                     f"Fator de ocupação: {fator:.2f}%\n"
                     f"Situação: {conforme}")

        label_resultado.config(text=resultado)
        salvar_resultado(largura, altura, fator, conforme)
    except ValueError as e:
        messagebox.showerror("Erro", f"Entrada inválida: {e}")

def salvar_resultado(largura, altura, fator, conforme):
    try:
        with open("resultado_eletrocalha.txt", "a", encoding="utf-8") as arquivo:
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            arquivo.write(f"{data_hora} | Largura: {largura} mm | Altura: {altura} mm | Fator: {fator:.2f}% | {conforme}\n")
            for c in circuitos:
                arquivo.write(f"   - {c['nome']} | {c['quantidade']} cabos | {c['cabo']['cabo']}\n")
    except Exception as e:
        messagebox.showerror("Erro ao salvar", f"Não foi possível salvar o arquivo: {e}")

def limpar_tudo():
    entry_largura.delete(0, tk.END)
    entry_altura.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    combo_secao.set("")
    var_material.set("HEPR")
    var_tensao.set("0,6/1KV")
    circuitos.clear()
    atualizar_lista()
    label_resultado.config(text="")

# Interface Tkinter
janela = tk.Tk()
janela.title("Cálculo de Fator de Ocupação - NBR 5410 (Múltiplos Circuitos)")
janela.geometry("600x600")

tk.Label(janela, text="Largura da eletrocalha (mm):").pack()
entry_largura = tk.Entry(janela)
entry_largura.pack()

tk.Label(janela, text="Altura da eletrocalha (mm):").pack()
entry_altura = tk.Entry(janela)
entry_altura.pack()

tk.Label(janela, text="Adicionar Circuito:").pack(pady=5)
frame_circuito = tk.Frame(janela)
frame_circuito.pack(pady=5)

tk.Label(frame_circuito, text="Nome:").grid(row=0, column=0)
entry_nome = tk.Entry(frame_circuito, width=12)
entry_nome.grid(row=0, column=1)

tk.Label(frame_circuito, text="Qtd Cabos:").grid(row=0, column=2)
entry_quantidade = tk.Entry(frame_circuito, width=5)
entry_quantidade.grid(row=0, column=3)

tk.Label(frame_circuito, text="Material:").grid(row=0, column=4)
var_material = tk.StringVar(value="HEPR")
combo_material = ttk.Combobox(frame_circuito, textvariable=var_material, values=["HEPR", "PVC"], state="readonly", width=8)
combo_material.grid(row=0, column=5)

tk.Label(frame_circuito, text="Tensão:").grid(row=0, column=6)
var_tensao = tk.StringVar(value="0,6/1KV")
combo_tensao = ttk.Combobox(frame_circuito, textvariable=var_tensao, values=["0,6/1KV", "750V"], state="readonly", width=8)
combo_tensao.grid(row=0, column=7)

tk.Label(frame_circuito, text="Seção:").grid(row=0, column=8)
combo_secao = ttk.Combobox(frame_circuito, values=["1.5", "2.5", "4", "6", "10", "16"], state="readonly", width=5)
combo_secao.grid(row=0, column=9)

tk.Label(janela, text="Circuitos adicionados:").pack()
lista_circuitos = tk.Listbox(janela, width=80, height=8)
lista_circuitos.pack(pady=5)

# Botões principais
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn_calcular = tk.Button(frame_botoes, text="Calcular", command=calcular_ocupacao, bg="red", fg="white", font=("Arial", 10, "bold"))
btn_calcular.grid(row=0, column=0, padx=5)

btn_limpar = tk.Button(frame_botoes, text="Limpar Tudo", command=limpar_tudo)
btn_limpar.grid(row=0, column=1, padx=5)

btn_adicionar = tk.Button(frame_botoes, text="Adicionar", command=adicionar_circuito, bg="blue", fg="white", font=("Arial", 10, "bold"))
btn_adicionar.grid(row=0, column=2, padx=5)

label_resultado = tk.Label(janela, text="", font=("Arial", 11), justify="left")
label_resultado.pack(pady=10)

janela.mainloop()
