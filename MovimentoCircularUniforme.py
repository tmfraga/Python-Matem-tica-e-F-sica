import tkinter as tk
from tkinter import messagebox
import math

class SimuladorMCU:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Simulador de Física: Movimento Circular Uniforme (MCU)")
        self.raiz.geometry("800x550")
        self.raiz.resizable(False, False)

        # ---- Parâmetros Físicos Iniciais ----
        self.raio_metros = 30.0  # Raio da circunferência
        self.velocidade_m_s = 20.0 # Velocidade linear da bolinha
        
        # Centro do Canvas (onde ficará o eixo de rotação)
        self.cx = 400
        self.cy = 300
        self.raio_bola = 10

        # Variáveis de estado
        self.angulo_atual = 0.0  # Theta em radianos
        self.em_execucao = False
        self.objeto_orbita = None

        # Construção da Interface
        self.criar_widgets()
        self.desenhar_trajetoria()

    def criar_widgets(self):
        # Painel de Controle Superior
        frame_controle = tk.Frame(self.raiz, bg="#f5f5f5", bd=2, relief="groove")
        frame_controle.pack(side="top", fill="x", padx=10, pady=10)

        # Input: Raio
        tk.Label(frame_controle, text="Raio R (m):", font=("Arial", 10, "bold"), bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5)
        self.entry_raio = tk.Entry(frame_controle, width=6, font=("Arial", 10))
        self.entry_raio.insert(0, str(self.raio_metros))
        self.entry_raio.grid(row=0, column=1, padx=5)

        # Input: Velocidade Linear
        tk.Label(frame_controle, text="Velocidade v (m/s):", font=("Arial", 10, "bold"), bg="#f5f5f5").grid(row=0, column=2, padx=5, pady=5)
        self.entry_vel = tk.Entry(frame_controle, width=6, font=("Arial", 10))
        self.entry_vel.insert(0, str(self.velocidade_m_s))
        self.entry_vel.grid(row=0, column=3, padx=5)

        # Botão START / PAUSE
        self.btn_start = tk.Button(frame_controle, text="START 🔄", command=self.alternar_simulacao, 
                                  bg="#2196F3", fg="white", font=("Arial", 10, "bold"), width=12)
        self.btn_start.grid(row=0, column=4, padx=20)

        # Labels de Resultados em Tempo Real
        self.lbl_omega = tk.Label(frame_controle, text="ω = 0.00 rad/s", font=("Consolas", 10, "bold"), bg="#f5f5f5", fg="purple")
        self.lbl_omega.grid(row=0, column=5, padx=10)
        
        self.lbl_frequencia = tk.Label(frame_controle, text="f = 0.00 Hz", font=("Consolas", 10, "bold"), bg="#f5f5f5", fg="green")
        self.lbl_frequencia.grid(row=0, column=6, padx=10)

        # Canvas da Animação
        self.canvas = tk.Canvas(self.raiz, bg="white", width=780, height=460, bd=1, relief="solid")
        self.canvas.pack(padx=10, pady=(0, 10))

        # Marcador do Centro (Eixo)
        self.canvas.create_oval(self.cx-3, self.cy-3, self.cx+3, self.cy+3, fill="black")
        
        # Criar a bolinha que vai girar
        self.bola = self.canvas.create_oval(0, 0, 0, 0, fill="orangered", outline="black")

    def desenhar_trajetoria(self):
        # Remove a órbita anterior se ela existir
        if self.objeto_orbita:
            self.canvas.delete(self.objeto_orbita)
            
        # Desenha a linha pontilhada representando o raio da órbita
        # Multiplicamos por uma escala visual (ex: 4x) para o gráfico preencher a tela confortavelmente
        r_pixel = self.raio_metros * 4
        self.objeto_orbita = self.canvas.create_oval(
            self.cx - r_pixel, self.cy - r_pixel,
            self.cx + r_pixel, self.cy + r_pixel,
            outline="#BDBDBD", dash=(4, 4), width=1.5
        )
        self.atualizar_posicao_bola()

    def alternar_simulacao(self):
        if self.em_execucao:
            # Pausa o movimento
            self.em_execucao = False
            self.btn_start.config(text="START 🔄", bg="#2196F3")
        else:
            try:
                # Captura os dados técnicos fornecidos
                self.raio_metros = float(self.entry_raio.get())
                self.velocidade_m_s = float(self.entry_vel.get())
                
                if self.raio_metros <= 0:
                    raise ValueError
                    
            except ValueError:
                messagebox.showerror("Erro", "Insira valores numéricos válidos. O raio deve ser maior que zero.")
                return

            # Recalcula a física do MCU
            # ω = v / R
            self.omega = self.velocidade_m_s / self.raio_metros
            # f = ω / 2π
            frequencia = self.omega / (2 * math.pi)

            # Atualiza os painéis numéricos
            self.lbl_omega.config(text=f"ω = {self.omega:.2f} rad/s")
            self.lbl_frequencia.config(text=f"f = {frequencia:.2f} Hz")

            # Redesenha o círculo guia caso o raio tenha mudado
            self.desenhar_trajetoria()

            # Ativa o loop
            self.em_execucao = True
            self.btn_start.config(text="PAUSE ⏸️", bg="#FF9800")
            self.atualizar_frame()

    def atualizar_posicao_bola(self):
        # Converte o raio real para escala de tela
        r_pixel = self.raio_metros * 4
        
        # Trigonometria pura: mapeando coordenadas polares em cartesianas
        x_bola = self.cx + r_pixel * math.cos(self.angulo_atual)
        y_bola = self.cy - r_pixel * math.sin(self.angulo_atual)

        # Move a bolinha para a nova coordenada calculada
        self.canvas.coords(
            self.bola,
            x_bola - self.raio_bola, y_bola - self.raio_bola,
            x_bola + self.raio_bola, y_bola + self.raio_bola
        )

    def atualizar_frame(self):
        if not self.em_execucao:
            return

        # Variação do tempo por frame (dt = 0.03 segundos)
        dt = 0.03
        
        # dθ = ω * dt
        self.angulo_atual += self.omega * dt

        # Mantém o ângulo dentro do limite geométrico de 0 a 2π para evitar estouro de memória
        self.angulo_atual = self.angulo_atual % (2 * math.pi)

        # Atualiza o objeto na tela
        self.atualizar_posicao_bola()

        # Agenda o próximo frame (aproximadamente 33 FPS)
        self.raiz.after(30, self.atualizar_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorMCU(root)
    root.mainloop()
