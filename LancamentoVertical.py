import tkinter as tk
import math

class AnimacaoLancamento:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Simulador de Física: Lançamento Parabólico")
        self.raiz.geometry("800x500")
        self.raiz.resizable(False, False)

        # ---- Parâmetros Físicos Configuráveis ----
        self.g = 9.81         # Aceleração da gravidade (m/s²)
        self.v0 = 60.0        # Velocidade inicial (m/s)
        self.angulo = 45.0    # Ângulo de lançamento (graus)
        
        # Fatores de escala para ajustar os metros reais aos pixels da tela
        self.escala_x = 4.5
        self.escala_y = 4.5
        
        # Posição inicial da bolinha no Canvas (canto inferior esquerdo)
        self.x_origem = 50
        self.y_origem = 430
        self.raio_bola = 8

        # Variáveis de controle de estado
        self.tempo = 0.0
        self.em_execucao = False
        self.trajetoria_pontos = []

        # ---- Construção da Interface Gráfica ----
        self.criar_widgets()
        
    def criar_widgets(self):
        # Painel Superior de Controles
        frame_controle = tk.Frame(self.raiz, bg="#f0f0f0", bd=2, relief="groove")
        frame_controle.pack(side="top", fill="x", padx=10, pady=10)

        # Campo: Velocidade
        tk.Label(frame_controle, text="V₀ (m/s):", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.entry_v0 = tk.Entry(frame_controle, width=6, font=("Arial", 10))
        self.entry_v0.insert(0, str(self.v0))
        self.entry_v0.grid(row=0, column=1, padx=5)

        # Campo: Ângulo
        tk.Label(frame_controle, text="Ângulo (°):", font=("Arial", 10, "bold"), bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
        self.entry_angulo = tk.Entry(frame_controle, width=6, font=("Arial", 10))
        self.entry_angulo.insert(0, str(self.angulo))
        self.entry_angulo.grid(row=0, column=3, padx=5)

        # Botão START
        self.btn_start = tk.Button(frame_controle, text="START 🚀", command=self.iniciar_lancamento, 
                                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=12)
        self.btn_start.grid(row=0, column=4, padx=20)

        # Painel do Gráfico/Animação (Canvas)
        self.canvas = tk.Canvas(self.raiz, bg="white", width=780, height=440, bd=1, relief="solid")
        self.canvas.pack(padx=10, pady=(0, 10))

        # Desenhar a linha do horizonte/solo
        self.canvas.create_line(0, self.y_origem + self.raio_bola, 800, self.y_origem + self.raio_bola, fill="#8B4513", width=2)

        # Criar a bolinha vermelha no ponto inicial
        self.bola = self.canvas.create_oval(
            self.x_origem - self.raio_bola, self.y_origem - self.raio_bola,
            self.x_origem + self.raio_bola, self.y_origem + self.raio_bola,
            fill="red", outline="black"
        )

    def iniciar_lancamento(self):
        if self.em_execucao:
            return  # Evita disparar múltiplos loops simultâneos

        try:
            # Captura e valida os dados de entrada digitados pelo usuário
            self.v0 = float(self.entry_v0.get())
            self.angulo = float(self.entry_angulo.get())
        except ValueError:
            tk.messagebox.showerror("Erro", "Insira valores numéricos válidos para V₀ e Ângulo.")
            return

        # Limpa rastros e linhas de trajetórias de simulações anteriores
        for ponto in self.trajetoria_pontos:
            self.canvas.delete(ponto)
        self.trajetoria_pontos.clear()

        # Decompõe a velocidade inicial nos eixos X e Y usando trigonometria
        angulo_rad = math.radians(self.angulo)
        self.vx = self.v0 * math.cos(angulo_rad)
        self.vy = self.v0 * math.sin(angulo_rad)

        # Reseta o cronômetro físico e muda o estado da animação
        self.tempo = 0.0
        self.em_execucao = True
        self.btn_start.config(state="disabled", bg="#9E9E9E")
        
        # Inicia o loop de animação de física
        self.atualizar_frame()

    def atualizar_frame(self):
        if not self.em_execucao:
            return

        # Passo de tempo por frame (dt = 0.03 segundos garante ~33 FPS estáveis)
        dt = 0.03
        self.tempo += dt

        # Equações de movimento cinemático
        x_real = self.vx * self.tempo
        y_real = (self.vy * self.tempo) - (0.5 * self.g * (self.tempo ** 2))

        # Conversão das coordenadas reais (metros) para o espaço do Canvas (pixels)
        # Nota: Inverte-se o eixo Y porque no Canvas o ponto (0,0) fica no canto superior esquerdo
        x_pixel = self.x_origem + (x_real * self.escala_x)
        y_pixel = self.y_origem - (y_real * self.escala_y)

        # Condição de parada: a bola tocou o solo novamente (ou passou dele)
        if y_pixel >= self.y_origem:
            # Força o posicionamento exato da bola na linha do chão
            self.canvas.coords(self.bola, 
                               self.x_origem + (x_real * self.escala_x) - self.raio_bola, self.y_origem - self.raio_bola,
                               self.x_origem + (x_real * self.escala_x) + self.raio_bola, self.y_origem + self.raio_bola)
            self.finalizar_animacao()
            return

        # Atualiza a posição da bolinha no Canvas
        self.canvas.coords(self.bola, 
                           x_pixel - self.raio_bola, y_pixel - self.raio_bola,
                           x_pixel + self.raio_bola, y_pixel + self.raio_bola)

        # Deixa uma linha pontilhada de rastro para desenhar a parábola geometricamente
        ponto_rastro = self.canvas.create_oval(x_pixel-1, y_pixel-1, x_pixel+1, y_pixel+1, fill="blue", outline="blue")
        self.trajetoria_pontos.append(ponto_rastro)

        # Agenda a execução do próximo frame em 30 milissegundos
        self.raiz.after(30, self.atualizar_frame)

    def finalizar_animacao(self):
        self.em_execucao = False
        self.btn_start.config(state="normal", bg="#4CAF50")


# Inicialização da Janela e Loop Principal
if __name__ == "__main__":
    root = tk.Tk()
    app = AnimacaoLancamento(root)
    root.mainloop()
