import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CalculadoraJuros:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Simulador Financeiro: Juros Simples vs. Compostos")
        self.raiz.geometry("750x550")
        self.raiz.resizable(False, False)
        
        self.criar_widgets()

    def criar_widgets(self):
        # --- Painel Superior: Entrada de Dados ---
        frame_inputs = tk.Frame(self.raiz, bg="#f8f9fa", bd=2, relief="groove")
        frame_inputs.pack(side="top", fill="x", padx=15, pady=15)

        # Título Interno
        tk.Label(frame_inputs, text="Parâmetros Financeiros", font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#333").grid(row=0, column=0, columnspan=4, pady=5, sticky="w", padx=10)

        # 1. Capital Inicial (C)
        tk.Label(frame_inputs, text="Capital Inicial (R$):", font=("Arial", 10, "bold"), bg="#f8f9fa").grid(row=1, column=0, padx=10, pady=8, sticky="e")
        self.entry_capital = tk.Entry(frame_inputs, font=("Arial", 10), width=15)
        self.entry_capital.insert(0, "1000.00")
        self.entry_capital.grid(row=1, column=1, padx=5, pady=8, sticky="w")

        # 2. Taxa de Juros (i)
        tk.Label(frame_inputs, text="Taxa de Juros (%):", font=("Arial", 10, "bold"), bg="#f8f9fa").grid(row=2, column=0, padx=10, pady=8, sticky="e")
        self.entry_taxa = tk.Entry(frame_inputs, font=("Arial", 10), width=15)
        self.entry_taxa.insert(0, "10.0")
        self.entry_taxa.grid(row=2, column=1, padx=5, pady=8, sticky="w")

        # ComboBox para a unidade da Taxa
        self.combo_unidade_taxa = ttk.Combobox(frame_inputs, values=["a.m. (ao mês)", "a.a. (ao ano)", "a.s. (ao semestre)", "a.d. (ao dia)"], width=15, state="readonly")
        self.combo_unidade_taxa.set("a.m. (ao mês)")
        self.combo_unidade_taxa.grid(row=2, column=2, padx=5, pady=8, sticky="w")

        # 3. Tempo / Período (t)
        tk.Label(frame_inputs, text="Tempo / Período:", font=("Arial", 10, "bold"), bg="#f8f9fa").grid(row=3, column=0, padx=10, pady=8, sticky="e")
        self.entry_tempo = tk.Entry(frame_inputs, font=("Arial", 10), width=15)
        self.entry_tempo.insert(0, "12")
        self.entry_tempo.grid(row=3, column=1, padx=5, pady=8, sticky="w")

        # ComboBox para a unidade do Tempo
        self.combo_unidade_tempo = ttk.Combobox(frame_inputs, values=["meses", "anos", "semestres", "dias"], width=15, state="readonly")
        self.combo_unidade_tempo.set("meses")
        self.combo_unidade_tempo.grid(row=3, column=2, padx=5, pady=8, sticky="w")

        # Botão Calcular (Estilo similar aos anteriores)
        self.btn_calcular = tk.Button(frame_inputs, text="CALCULAR 💰", command=self.calcular_juros,
                                      bg="#008CBA", fg="white", font=("Arial", 10, "bold"), width=14, height=2)
        self.btn_calcular.grid(row=1, column=3, rowspan=3, padx=30, pady=5)


        # --- Painéis Inferiores: Resultados Comparativos ---
        frame_resultados = tk.Frame(self.raiz)
        frame_resultados.pack(fill="both", expand=True, padx=15, pady=5)

        # Coluna Juros Simples
        self.frame_simples = tk.LabelFrame(frame_resultados, text=" Regime de Juros Simples (Linear) ", font=("Arial", 10, "bold"), fg="#155724", bg="#d4edda", bd=2)
        self.frame_simples.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.lbl_juros_simples = tk.Label(self.frame_simples, text="Juros Acumulados:\nR$ 0,00", font=("Consolas", 12, "bold"), bg="#d4edda", fg="#155724")
        self.lbl_juros_simples.pack(expand=True)
        self.lbl_montante_simples = tk.Label(self.frame_simples, text="Montante Final:\nR$ 0,00", font=("Consolas", 14, "bold"), bg="#d4edda", fg="#155724")
        self.lbl_montante_simples.pack(expand=True)

        # Coluna Juros Compostos
        self.frame_compostos = tk.LabelFrame(frame_resultados, text=" Regime de Juros Compostos (Exponencial) ", font=("Arial", 10, "bold"), fg="#0c5460", bg="#d1ecf1", bd=2)
        self.frame_compostos.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.lbl_juros_compostos = tk.Label(self.frame_compostos, text="Juros Acumulados:\nR$ 0,00", font=("Consolas", 12, "bold"), bg="#d1ecf1", fg="#0c5460")
        self.lbl_juros_compostos.pack(expand=True)
        self.lbl_montante_compostos = tk.Label(self.frame_compostos, text="Montante Final:\nR$ 0,00", font=("Consolas", 14, "bold"), bg="#d1ecf1", fg="#0c5460")
        self.lbl_montante_compostos.pack(expand=True)

    def converter_tempo_para_taxa(self, tempo, u_tempo, u_taxa):
        """ Normaliza o tempo 't' para que fique na mesma unidade da taxa de juros 'i' """
        # Fatores de conversão baseados em dias comerciais (Mês = 30 dias, Ano = 360 dias, Semestre = 180 dias)
        # Primeiro, converte a entrada do usuário de qualquer unidade para DIAS
        if u_tempo == "dias":
            dias = tempo
        elif u_tempo == "meses":
            dias = tempo * 30
        elif u_tempo == "semestres":
            dias = tempo * 180
        elif u_tempo == "anos":
            dias = tempo * 360

        # Agora, converte de DIAS para a unidade correspondente da taxa escolhida
        if "ao dia" in u_taxa:
            return dias
        elif "ao mês" in u_taxa:
            return dias / 30
        elif "ao semestre" in u_taxa:
            return dias / 180
        elif "ao ano" in u_taxa:
            return dias / 360
        return tempo

    def calcular_juros(self):
        try:
            # Captura e validação das entradas
            C = float(self.entry_capital.get())
            taxa_original = float(self.entry_taxa.get())
            tempo_original = float(self.entry_tempo.get())

            if C < 0 or taxa_original < 0 or tempo_original < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, digite valores numéricos positivos válidos para os campos.")
            return

        # i em valor decimal (ex: 10% -> 0.10)
        i = taxa_original / 100

        # Obtenção das unidades selecionadas nas caixas de seleção
        unidade_taxa = self.combo_unidade_taxa.get()
        unidade_tempo = self.combo_unidade_tempo.get()

        # Alinhamento temporal (Garante que t e i combinem matematicamente)
        t = self.converter_tempo_para_taxa(tempo_original, unidade_tempo, unidade_taxa)

        # --- Cálculo 1: Juros Simples ---
        # M = C * (1 + i * t)
        montante_simples = C * (1 + (i * t))
        juros_simples = montante_simples - C

        # --- Cálculo 2: Juros Compostos ---
        # M = C * ((1 + i) ** t)
        montante_compostos = C * ((1 + i) ** t)
        juros_compostos = montante_compostos - C

        # --- Atualização Visual da Interface ---
        self.lbl_juros_simples.config(text=f"Juros Acumulados:\nR$ {juros_simples:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
        self.lbl_montante_simples.config(text=f"Montante Final:\nR$ {montante_simples:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

        self.lbl_juros_compostos.config(text=f"Juros Acumulados:\nR$ {juros_compostos:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
        self.lbl_montante_compostos.config(text=f"Montante Final:\nR$ {montante_compostos:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraJuros(root)
    root.mainloop()
