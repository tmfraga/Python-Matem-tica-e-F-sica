import tkinter as tk
from tkinter import messagebox
import math

class CalculadoraRichter:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Magnitude - Escala Richter")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f9")

        # --- CONSTANTES ---
        # E0 dado no quadro = 7 * 10^-3 KWh
        # Convertendo para Joules: (7 * 10^-3) * (3.6 * 10^6) = 25200 J
        self.E0 = 25200 

        # --- INTERFACE GRÁFICA ---
        
        # Título principal
        lbl_titulo = tk.Label(
            root, text="Análise de Magnitude Sísmica", 
            font=("Arial", 14, "bold"), bg="#f4f4f9", fg="#2c3e50"
        )
        lbl_titulo.pack(pady=15)

        # Container para a fórmula
        frame_formula = tk.Frame(root, bg="#eef2f3", bd=1, relief=tk.SOLID)
        frame_formula.pack(pady=5, padx=20, fill=tk.X)
        
        lbl_formula = tk.Label(
            frame_formula, text="Fórmula Utilizada:\nM = (2/3) * log10( E / E₀ )", 
            font=("Courier New", 11, "bold"), bg="#eef2f3", fg="#34495e", justify=tk.CENTER
        )
        lbl_formula.pack(pady=8)
        
        lbl_constante = tk.Label(
            frame_formula, text="Onde E₀ = 25.200 J (7×10⁻³ KWh)", 
            font=("Arial", 9, "italic"), bg="#eef2f3", fg="#7f8c8d"
        )
        lbl_constante.pack(pady=2)

        # Campo de entrada para a Energia E
        lbl_instrucao = tk.Label(
            root, text="Digite a Energia liberada E (em Joules):", 
            font=("Arial", 10, "bold"), bg="#f4f4f9", fg="#2c3e50"
        )
        lbl_instrucao.pack(pady=(20, 5))

        # Aceita notação científica, ex: 2.52e7 ou 25200000
        self.entry_energia = tk.Entry(root, font=("Arial", 11), justify=tk.CENTER, width=25)
        self.entry_energia.pack(pady=5)
        self.entry_energia.insert(0, "2.52e7") # Valor padrão exemplo (Magnitude 2)

        # Botão para calcular (Corrigido: trocado padding por padx e pady)
        btn_calcular = tk.Button(
            root, text="Calcular Magnitude", font=("Arial", 11, "bold"),
            bg="#2ecc71", fg="white", activebackground="#27ae60", activeforeground="white",
            command=self.calcular_magnitude, bd=0, padx=10, pady=6, cursor="hand2"
        )
        btn_calcular.pack(pady=15)

        # Quadro de resultados
        self.lbl_resultado = tk.Label(
            root, text="Magnitude (M): --", 
            font=("Arial", 13, "bold"), bg="#f4f4f9", fg="#c0392b"
        )
        self.lbl_resultado.pack(pady=5)

        self.lbl_classificacao = tk.Label(
            root, text="Classificação: --", 
            font=("Arial", 10, "italic"), bg="#f4f4f9", fg="#7f8c8d"
        )
        self.lbl_classificacao.pack(pady=5)

    def calcular_magnitude(self):
        try:
            # Captura o texto do input
            entrada_texto = self.entry_energia.get().replace(",", ".").strip()
            
            # Converte para float (suporta formatos normais e notação científica como 2.52e13)
            E = float(entrada_texto)
            
            if E <= 0:
                raise ValueError("A energia precisa ser maior que zero.")

            # Aplicação exata da fórmula matemática
            razao = E / self.E0
            magnitude = (2 / 3) * math.log10(razao)

            if magnitude < 0:
                magnitude = 0.0

            # Atualiza os textos na tela
            self.lbl_resultado.config(text=f"Magnitude (M): {magnitude:.2f}")
            
            classificacao = self.get_classificacao_texto(magnitude)
            self.lbl_classificacao.config(text=f"Classificação: {classificacao}")

        except ValueError:
            messagebox.showerror(
                "Erro de Entrada", 
                "Por favor, insira um valor numérico válido para a Energia.\n"
                "Exemplos aceitos: 25200000 ou 2.52e7"
            )

    def get_classificacao_texto(self, m):
        if m < 2.0: return "Microssismo (Imperceptível)"
        elif m < 4.0: return "Pequeno (Sentido, mas raramente causa estragos)"
        elif m < 6.0: return "Moderado (Pode causar danos em prédios frágeis)"
        elif m < 7.0: return "Forte (Destrutivo em um raio de até 100km)"
        elif m < 8.0: return "Grande Terremoto (Provoca danos sérios em vastas regiões)"
        else: return "Extremo (Devastação total em centenas de quilômetros)"

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraRichter(root)
    root.mainloop()
