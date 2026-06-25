import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Dicionário de funções matemáticas permitidas para o eval
DICI_SEGURO = {
    'x': None,
    'sin': np.sin,
    'cos': np.cos,
    'tan': np.tan,
    'sqrt': np.sqrt,
    'exp': np.exp,
    'log': np.log,
    'pi': np.pi
}

def plotar():
    equacao_texto = entry_eq.get()
    
    try:
        # 1. Geração dos pontos do gráfico
        x = np.linspace(-10, 10, 1000)
        valores_y = []
        
        for val_x in x:
            DICI_SEGURO['x'] = val_x
            y_res = eval(equacao_texto, {"__builtins__": None}, DICI_SEGURO)
            valores_y.append(y_res)
        
        y = np.array(valores_y)

        # 2. Reset e reconstrução do gráfico
        ax.clear()
        ax.plot(x, y, label=f"f(x) = {equacao_texto}", color="blue", linewidth=2)
        ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
        ax.axvline(0, color='black', linestyle='--', linewidth=0.8)
        
        # 3. Varredura numérica de raízes reais
        raizes_x = []
        for i in range(len(y) - 1):
            if y[i] * y[i+1] <= 0:
                x_raiz = x[i] - y[i] * (x[i+1] - x[i]) / (y[i+1] - y[i])
                raizes_x.append(x_raiz)
        
        # Filtragem de duplicatas próximas
        raizes_reais = []
        for r in raizes_x:
            if not any(abs(r - ja_encontrada) < 0.05 for ja_encontrada in raizes_reais):
                raizes_reais.append(r)

        # 4. Atualização visual e dos rótulos de texto
        if len(raizes_reais) > 0:
            valores_raiz_y = [0] * len(raizes_reais)
            ax.scatter(raizes_reais, valores_raiz_y, color='red', s=50, zorder=5, label="Raízes")
            texto_final = ", ".join([f"{r:.2f}" for r in raizes_reais])
            lbl_raizes_val.config(text=texto_final, fg="green")
        else:
            lbl_raizes_val.config(text="Sem raízes reais no intervalo de [-10, 10]", fg="red")

        # 5. Configurações de eixos e legenda
        ax.set_title("Análise Gráfica de f(x)", fontname="Arial", fontsize=12, fontweight="bold")
        ax.set_xlabel("Eixo X")
        ax.set_ylabel("Eixo Y")
        ax.grid(True, which='both', linestyle=':', alpha=0.6)
        ax.legend()
        ax.set_xlim([-10, 10])
        
        # Ajuste inteligente dos limites do eixo Y
        y_filtrado = y[np.isfinite(y)]
        if len(y_filtrado) > 0:
            margin = (y_filtrado.max() - y_filtrado.min()) * 0.1 if y_filtrado.max() != y_filtrado.min() else 1
            ax.set_ylim([max(y_filtrado.min() - margin, -20), min(y_filtrado.max() + margin, 20)])

        canvas.draw()

    except Exception as e:
        messagebox.showerror("Erro de Processamento", "Verifique a sintaxe da sua equação.\nExemplos válidos:\nx**2 - 4*x + 3\nsin(x) * 2")

# --- Estrutura da Janela Tkinter ---
janela = tk.Tk()
janela.title("Gerador de Gráficos e Raízes Acadêmicas")
janela.geometry("700x650")

# Painel Superior: Entrada
frame_topo = tk.Frame(janela)
frame_topo.pack(pady=15, fill="x", padx=20)

tk.Label(frame_topo, text="Digite f(x):", font=("Arial", 11, "bold")).pack(side="left", padx=5)
entry_eq = tk.Entry(frame_topo, font=("Consolas", 12), width=35)
entry_eq.pack(side="left", padx=5)
entry_eq.insert(0, "x**2 - 4*x + 3")

btn_plotar = tk.Button(frame_topo, text="Gerar Gráfico", command=plotar, bg="#007ACC", fg="white", font=("Arial", 10, "bold"))
btn_plotar.pack(side="left", padx=10)

# Painel Central: Gráfico integrado
fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=janela)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=5)

# Painel Inferior: Resultado Numérico
frame_rodape = tk.Frame(janela, bd=1, relief="sunken")
frame_rodape.pack(fill="x", padx=20, pady=15)

tk.Label(frame_rodape, text="Aproximação das Raízes Reais:", font=("Arial", 11, "bold")).pack(side="left", padx=10, pady=10)
lbl_raizes_val = tk.Label(frame_rodape, text="-", font=("Consolas", 12, "bold"))
lbl_raizes_val.pack(side="left", padx=5)

# Executa a primeira renderização automática
plotar()

janela.mainloop()
