import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
import math

class GeradorPapelMonolog:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Gerador de Papel Monolog (Log-Linear)")
        self.raiz.geometry("850x520")
        self.raiz.resizable(False, False)
        
        # Cores padrão iniciais
        self.cor_grade_hex = "D3D3D3"  # Cinza claro para linhas secundárias
        self.cor_ciclo_hex = "000000"  # Preto para as linhas dos ciclos principais
        
        # Estilização
        self.estilo = ttk.Style()
        self.estilo.configure("TLabel", font=("Arial", 10))
        self.estilo.configure("TButton", font=("Arial", 10, "bold"))

        # --- CONTAINER PRINCIPAL ---
        self.frame_esquerdo = ttk.Frame(raiz, padding="20")
        self.frame_esquerdo.pack(side="left", fill="y")

        self.frame_direito = ttk.Frame(raiz, padding="20")
        self.frame_direito.pack(side="right", fill="both", expand=True)

        # --- ESQUERDA: ENTRADAS DE DADOS ---
        # 1. Dimensões da Imagem (Pixels)
        ttk.Label(self.frame_esquerdo, text="Largura da Imagem (px):").grid(row=0, column=0, sticky="w", pady=5)
        self.spin_largura_img = ttk.Spinbox(self.frame_esquerdo, from_=100, to=5000, width=12, command=self.atualizar_preview)
        self.spin_largura_img.set(800)
        self.spin_largura_img.grid(row=0, column=1, sticky="w", padx=10)
        self.spin_largura_img.bind("<KeyRelease>", lambda e: self.atualizar_preview())

        ttk.Label(self.frame_esquerdo, text="Altura da Imagem (px):").grid(row=1, column=0, sticky="w", pady=5)
        self.spin_altura_img = ttk.Spinbox(self.frame_esquerdo, from_=100, to=5000, width=12, command=self.atualizar_preview)
        self.spin_altura_img.set(1000)
        self.spin_altura_img.grid(row=1, column=1, sticky="w", padx=10)
        self.spin_altura_img.bind("<KeyRelease>", lambda e: self.atualizar_preview())

        # 2. Configuração do Eixo Logarítmico (Vertical)
        ttk.Label(self.frame_esquerdo, text="Número de Ciclos (Décadas):").grid(row=2, column=0, sticky="w", pady=5)
        self.spin_ciclos = ttk.Spinbox(self.frame_esquerdo, from_=1, to=10, width=12, command=self.atualizar_preview)
        self.spin_ciclos.set(3)
        self.spin_ciclos.grid(row=2, column=1, sticky="w", padx=10)
        self.spin_ciclos.bind("<KeyRelease>", lambda e: self.atualizar_preview())

        # 3. Configuração do Eixo Linear (Horizontal)
        ttk.Label(self.frame_esquerdo, text="Divisões Lineares (X):").grid(row=3, column=0, sticky="w", pady=5)
        self.spin_div_x = ttk.Spinbox(self.frame_esquerdo, from_=5, to=200, width=12, command=self.atualizar_preview)
        self.spin_div_x.set(20)
        self.spin_div_x.grid(row=3, column=1, sticky="w", padx=10)
        self.spin_div_x.bind("<KeyRelease>", lambda e: self.atualizar_preview())

        # 4. Seleção de Cores
        ttk.Label(self.frame_esquerdo, text="Cor das Subdivisões:").grid(row=4, column=0, sticky="w", pady=5)
        self.frame_cor_grade = tk.Frame(self.frame_esquerdo, width=35, height=22, bg=f"#{self.cor_grade_hex}", relief="groove", bd=2)
        self.frame_cor_grade.grid(row=4, column=1, sticky="w", padx=10)
        self.btn_cor_grade = ttk.Button(self.frame_esquerdo, text="Escolher...", command=self.escolher_cor_grade)
        self.btn_cor_grade.grid(row=4, column=1, sticky="w", padx=55)

        ttk.Label(self.frame_esquerdo, text="Cor dos Ciclos (Forte):").grid(row=5, column=0, sticky="w", pady=10)
        self.frame_cor_ciclo = tk.Frame(self.frame_esquerdo, width=35, height=22, bg=f"#{self.cor_ciclo_hex}", relief="groove", bd=2)
        self.frame_cor_ciclo.grid(row=5, column=1, sticky="w", padx=10)
        self.btn_cor_ciclo = ttk.Button(self.frame_esquerdo, text="Escolher...", command=self.escolher_cor_ciclo)
        self.btn_cor_ciclo.grid(row=5, column=1, sticky="w", padx=55)

        # 5. Botão Salvar
        self.btn_salvar = tk.Button(
            self.frame_esquerdo, text="💾 SALVAR IMAGEM MONOLOG...", 
            command=self.salvar_imagem,
            bg="#0056b3", fg="white", font=("Arial", 11, "bold"),
            relief="raised", bd=3, cursor="hand2"
        )
        self.btn_salvar.grid(row=6, column=0, columnspan=2, pady=35, sticky="ew")

        # --- DIREITA: PREVIEW EM TEMPO REAL ---
        ttk.Label(self.frame_direito, text="Visualização Prévia (Escala Monolog):", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        
        self.canvas_w = 380
        self.canvas_h = 440
        self.canvas = tk.Canvas(self.frame_direito, width=self.canvas_w, height=self.canvas_h, bg="#EAEAEA", relief="solid", bd=1)
        self.canvas.pack(pady=5, fill="both", expand=True)

        self.atualizar_preview()

    def hex_para_rgb(self, hex_str):
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return (r, g, b)

    def escolher_cor_grade(self):
        cor = colorchooser.askcolor(title="Cor das subdivisões")
        if cor[1]:
            self.cor_grade_hex = cor[1].replace("#", "").upper()
            self.frame_cor_grade.config(bg=cor[1])
            self.atualizar_preview()

    def escolher_cor_ciclo(self):
        cor = colorchooser.askcolor(title="Cor dos ciclos principais")
        if cor[1]:
            self.cor_ciclo_hex = cor[1].replace("#", "").upper()
            self.frame_cor_ciclo.config(bg=cor[1])
            self.atualizar_preview()

    def criar_imagem_base(self, larg, alt, num_ciclos, div_x, rgb_grade, rgb_ciclo):
        """Gera a malha logarítmica no eixo Y e linear no eixo X"""
        img = Image.new("RGB", (larg, alt), "white")
        draw = ImageDraw.Draw(img)

        # 1. Desenha as linhas horizontais (Escala Logarítmica no eixo Y de baixo para cima)
        altura_ciclo = alt / num_ciclos
        
        for ciclo in range(num_ciclos + 1):
            y_base = alt - (ciclo * altura_ciclo)
            
            # Linha principal do Ciclo (Ex: 1, 10, 100...)
            if ciclo < num_ciclos:
                draw.line([(0, y_base), (larg, y_base)], fill=rgb_ciclo, width=3)
                
                # Subdivisões internas do ciclo logarítmico (valores de 2 a 9)
                for i in range(2, 10):
                    # Distância proporcional logarítmica
                    deslocamento_log = math.log10(i) * altura_ciclo
                    y_sub = y_base - deslocamento_log
                    draw.line([(0, y_sub), (larg, y_sub)], fill=rgb_grade, width=1)
            else:
                # Topo da imagem (última linha)
                draw.line([(0, 0), (larg, 0)], fill=rgb_ciclo, width=3)

        # 2. Desenha as linhas verticais (Escala Linear tradicional no eixo X)
        passo_x = larg / div_x
        for i in range(div_x + 1):
            x = i * passo_x
            espessura = 2 if i == 0 or i == div_x else 1
            cor = rgb_ciclo if (i == 0 or i == div_x) else rgb_grade
            draw.line([(x, 0), (x, alt)], fill=cor, width=espessura)

        return img

    def atualizar_preview(self):
        try:
            larg = int(self.spin_largura_img.get())
            alt = int(self.spin_altura_img.get())
            num_ciclos = int(self.spin_ciclos.get())
            div_x = int(self.spin_div_x.get())
        except ValueError:
            return 

        if larg <= 0 or alt <= 0 or num_ciclos <= 0 or div_x <= 0:
            return

        rgb_grade = self.hex_para_rgb(self.cor_grade_hex)
        rgb_ciclo = self.hex_para_rgb(self.cor_ciclo_hex)

        img_real = self.criar_imagem_base(larg, alt, num_ciclos, div_x, rgb_grade, rgb_ciclo)
        img_real.thumbnail((self.canvas_w - 10, self.canvas_h - 10), Image.Resampling.LANCZOS)
        
        self.img_tk = ImageTk.PhotoImage(img_real)
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas_w // 2, self.canvas_h // 2, image=self.img_tk, anchor="center")

    def salvar_imagem(self):
        try:
            larg = int(self.spin_largura_img.get())
            alt = int(self.spin_altura_img.get())
            num_ciclos = int(self.spin_ciclos.get())
            div_x = int(self.spin_div_x.get())
            
            caminho_arquivo = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("Imagem PNG", "*.png"), ("Imagem JPEG", "*.jpg")],
                title="Salvar Imagem Monolog"
            )
            
            if not caminho_arquivo:
                return

            rgb_grade = self.hex_para_rgb(self.cor_grade_hex)
            rgb_ciclo = self.hex_para_rgb(self.cor_ciclo_hex)

            img_final = self.criar_imagem_base(larg, alt, num_ciclos, div_x, rgb_grade, rgb_ciclo)
            img_final.save(caminho_arquivo)
            
            messagebox.showinfo("Sucesso!", f"Papel Monolog salvo com sucesso em:\n{caminho_arquivo}")

        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar a imagem:\n{e}")

if __name__ == "__main__":
    raiz = tk.Tk()
    app = GeradorPapelMonolog(raiz)
    raiz.mainloop()
