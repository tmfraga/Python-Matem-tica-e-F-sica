import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

class GeradorImagemQuadriculada:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Gerador de Imagem Quadriculada")
        self.raiz.geometry("820x500")
        self.raiz.resizable(False, False)
        
        # Cor padrão inicial (Cinza claro)
        self.cor_hex = "D3D3D3"
        
        # Estilização
        self.estilo = ttk.Style()
        self.estilo.configure("TLabel", font=("Arial", 10))
        self.estilo.configure("TButton", font=("Arial", 10, "bold"))

        # --- CONTAINER PRINCIPAL (Esquerda e Direita) ---
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

        # 2. Dimensão do Quadrado (Pixels)
        ttk.Label(self.frame_esquerdo, text="Tamanho do Quadrado (px):").grid(row=2, column=0, sticky="w", pady=5)
        self.spin_quadrado = ttk.Spinbox(self.frame_esquerdo, from_=5, to=500, width=12, command=self.atualizar_preview)
        self.spin_quadrado.set(40)
        self.spin_quadrado.grid(row=2, column=1, sticky="w", padx=10)
        self.spin_quadrado.bind("<KeyRelease>", lambda e: self.atualizar_preview())

        # 3. Intervalo de Linhas Mais Grossas
        ttk.Label(self.frame_esquerdo, text="Linha grossa a cada (quadrados):").grid(row=3, column=0, sticky="w", pady=5)
        self.spin_intervalo = ttk.Spinbox(self.frame_esquerdo, from_=1, to=50, width=12, command=self.atualizar_preview)
        self.spin_intervalo.set(5)
        self.spin_intervalo.grid(row=3, column=1, sticky="w", padx=10)
        self.spin_intervalo.bind("<KeyRelease>", lambda e: self.atualizar_preview())

        # 4. Seleção da Cor
        ttk.Label(self.frame_esquerdo, text="Cor das Linhas:").grid(row=4, column=0, sticky="w", pady=10)
        self.frame_cor = tk.Frame(self.frame_esquerdo, width=35, height=22, bg=f"#{self.cor_hex}", relief="groove", bd=2)
        self.frame_cor.grid(row=4, column=1, sticky="w", padx=10)
        self.btn_cor = ttk.Button(self.frame_esquerdo, text="Escolher...", command=self.escolher_cor)
        self.btn_cor.grid(row=4, column=1, sticky="w", padx=55)

        # 5. Botão para Salvar em Local Escolhido
        self.btn_salvar = tk.Button(
            self.frame_esquerdo, text="💾 SALVAR IMAGEM EM LOCAL...", 
            command=self.salvar_imagem,
            bg="#107c41", fg="white", font=("Arial", 11, "bold"),
            relief="raised", bd=3, cursor="hand2"
        )
        # CORREÇÃO AQUI: Trocado fill="x" por sticky="ew" para corrigir o bug do TclError
        self.btn_salvar.grid(row=5, column=0, columnspan=2, pady=40, sticky="ew")

        # --- DIREITA: PREVIEW EM TEMPO REAL ---
        ttk.Label(self.frame_direito, text="Visualização Prévia (Preview Real):", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        
        # Canvas para desenhar a miniatura do preview
        self.canvas_w = 360
        self.canvas_h = 420
        self.canvas = tk.Canvas(self.frame_direito, width=self.canvas_w, height=self.canvas_h, bg="#EAEAEA", relief="solid", bd=1)
        self.canvas.pack(pady=5, fill="both", expand=True)

        # Renderiza o preview inicial
        self.atualizar_preview()

    def escolher_cor(self):
        cor_selecionada = colorchooser.askcolor(title="Selecione a cor das linhas")
        if cor_selecionada[1]:
            self.cor_hex = cor_selecionada[1].replace("#", "").upper()
            self.frame_cor.config(bg=cor_selecionada[1])
            self.atualizar_preview()

    def criar_imagem_base(self, larg, alt, tam_quadrado, intervalo, cor_rgb):
        """Gera e retorna um objeto de imagem Pillow baseado nos parâmetros fornecidos"""
        img = Image.new("RGB", (larg, alt), "white")
        draw = ImageDraw.Draw(img)

        # Desenha as linhas verticais
        idx_coluna = 0
        for x in range(0, larg, tam_quadrado):
            espessura = 3 if idx_coluna % intervalo == 0 else 1
            draw.line([(x, 0), (x, alt)], fill=cor_rgb, width=espessura)
            idx_coluna += 1

        # Desenha as linhas horizontais
        idx_linha = 0
        for y in range(0, alt, tam_quadrado):
            espessura = 3 if idx_linha % intervalo == 0 else 1
            draw.line([(0, y), (larg, y)], fill=cor_rgb, width=espessura)
            idx_linha += 1

        return img

    def atualizar_preview(self):
        """Gera uma miniatura proporcional da imagem real e coloca no Canvas"""
        try:
            larg = int(self.spin_largura_img.get())
            alt = int(self.spin_altura_img.get())
            tam_quadrado = int(self.spin_quadrado.get())
            intervalo = int(self.spin_intervalo.get())
        except ValueError:
            return 

        if larg <= 0 or alt <= 0 or tam_quadrado <= 0 or intervalo <= 0:
            return

        # Converte a cor Hex para tupla RGB
        r = int(self.cor_hex[0:2], 16)
        g = int(self.cor_hex[2:4], 16)
        b = int(self.cor_hex[4:6], 16)
        cor_rgb = (r, g, b)

        # Gera a imagem real na memória RAM
        img_real = self.criar_imagem_base(larg, alt, tam_quadrado, intervalo, cor_rgb)

        # Redimensiona a imagem para caber no Canvas (Mantendo a proporção original)
        img_real.thumbnail((self.canvas_w - 10, self.canvas_h - 10), Image.Resampling.LANCZOS)
        
        # Converte para o formato que o Tkinter aceita exibir
        self.img_tk = ImageTk.PhotoImage(img_real)
        
        # Centraliza a imagem no Canvas
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas_w // 2, self.canvas_h // 2, image=self.img_tk, anchor="center")

    def salvar_imagem(self):
        try:
            larg = int(self.spin_largura_img.get())
            alt = int(self.spin_altura_img.get())
            tam_quadrado = int(self.spin_quadrado.get())
            intervalo = int(self.spin_intervalo.get())
            
            caminho_arquivo = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("Imagem PNG", "*.png"), ("Imagem JPEG", "*.jpg")],
                title="Salvar Imagem Quadriculada"
            )
            
            if not caminho_arquivo:
                return

            r = int(self.cor_hex[0:2], 16)
            g = int(self.cor_hex[2:4], 16)
            b = int(self.cor_hex[4:6], 16)
            cor_rgb = (r, g, b)

            img_final = self.criar_imagem_base(larg, alt, tam_quadrado, intervalo, cor_rgb)
            img_final.save(caminho_arquivo)
            
            messagebox.showinfo("Sucesso!", f"Imagem salva com sucesso em:\n{caminho_arquivo}")

        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o arquivo:\n{e}")

if __name__ == "__main__":
    raiz = tk.Tk()
    app = GeradorImagemQuadriculada(raiz)
    raiz.mainloop()
