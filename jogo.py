import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
import time
import random
from PIL import Image, ImageTk

class TorreHanoiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Torre de Hanoi Manual - Trabalho Acadêmico")
        self.root.geometry("1920x1080")

        # Variáveis do jogo
        self.num_discos = 3
        self.torres = {"A": [], "B": [], "C": []}
        self.origem_selecionada = None
        self.movimentos = 0
        self.tempo_inicio = None
        self.timer_id = None
        self.timer_dica_id = None
        self.modo_regressivo = tk.BooleanVar(value=False)
        self.tempo_limite = 300  # 5 minutos em segundos
        self.tempo_restante = self.tempo_limite

        self.dicas = [
            "Lembre-se: nunca coloque um disco maior sobre um menor!",
            "Tente mover o menor disco o máximo possível!",
            "O objetivo é mover todos para a torre C.",
            "Use a torre B como apoio para trocar os discos.",
            "Planeje seus movimentos antes de agir.",
            "Discos grandes devem sempre ficar embaixo."
        ]

        # Plano de fundo
        self.bg_color = "#d0f0fd"  # azul clarinho default
        self.bg_image = None
        self.bg_photoimage = None

        self.criar_interface()
        self.iniciar_jogo()

    def criar_interface(self):
        fonte_header = ("Segoe UI", 36, "bold")
        fonte_normal = ("Segoe UI", 20)
        fonte_pequena = ("Segoe UI", 16)

        # Frame principal com fundo (cor ou imagem)
        self.frame_principal = tk.Frame(self.root, bg=self.bg_color)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Cabeçalho
        header = tk.Label(self.frame_principal, text="Torre de Hanoi Manual", font=fonte_header, bg=self.bg_color, fg="#000", pady=20)
        header.pack(fill=tk.X, pady=(10,0))

        # Controle
        ctrl_frame = tk.Frame(self.frame_principal, bg=self.bg_color, pady=15)
        ctrl_frame.pack(fill=tk.X)

        tk.Label(ctrl_frame, text="Nível:", bg=self.bg_color, font=fonte_normal).pack(side=tk.LEFT, padx=20)

        self.combo_discos = ttk.Combobox(ctrl_frame, values=["3", "4", "5", "6"], width=4, font=fonte_normal, state="readonly")
        self.combo_discos.current(0)
        self.combo_discos.pack(side=tk.LEFT)
        self.combo_discos.bind("<<ComboboxSelected>>", lambda e: self.iniciar_jogo())

        self.chk_regressivo = tk.Checkbutton(ctrl_frame, text="Modo Regressivo (tempo limitado)", var=self.modo_regressivo,
                                             bg=self.bg_color, font=fonte_normal, command=self.iniciar_jogo)
        self.chk_regressivo.pack(side=tk.LEFT, padx=40)

        self.lbl_movimentos = tk.Label(ctrl_frame, text="Movimentos: 0", bg=self.bg_color, width=20, font=fonte_normal)
        self.lbl_movimentos.pack(side=tk.LEFT, padx=20)

        self.lbl_tempo = tk.Label(ctrl_frame, text="Tempo: 00:00", bg=self.bg_color, width=20, font=fonte_normal)
        self.lbl_tempo.pack(side=tk.LEFT)

        self.btn_reiniciar = tk.Button(ctrl_frame, text="Reiniciar", font=fonte_normal, command=self.iniciar_jogo)
        self.btn_reiniciar.pack(side=tk.RIGHT, padx=30)

        # Botões extras para cor e plano de fundo
        extra_frame = tk.Frame(self.frame_principal, bg=self.bg_color)
        extra_frame.pack(fill=tk.X, pady=(0, 10))

        btn_cor = tk.Button(extra_frame, text="Alterar Cor de Fundo", font=fonte_pequena, command=self.alterar_cor_fundo)
        btn_cor.pack(side=tk.LEFT, padx=20)

        btn_img = tk.Button(extra_frame, text="Selecionar Imagem de Fundo", font=fonte_pequena, command=self.selecionar_imagem_fundo)
        btn_img.pack(side=tk.LEFT, padx=20)

        btn_hist = tk.Button(extra_frame, text="Ver Histórico de Jogos", font=fonte_pequena, command=self.mostrar_historico)
        btn_hist.pack(side=tk.RIGHT, padx=20)

        # Canvas para o jogo
        self.game_frame = tk.Frame(self.frame_principal, bg=self.bg_color)
        self.game_frame.pack(fill=tk.BOTH, expand=True, pady=30)

        self.canvas_width = 1500
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.game_frame, bg="#ddd", height=self.canvas_height, width=self.canvas_width)
        self.canvas.pack(expand=True)

        margin_x = 150
        espaço_entre = (self.canvas_width - 2*margin_x) // 3
        self.torre_pos_x = {
            "A": margin_x + espaço_entre//2,
            "B": margin_x + espaço_entre + espaço_entre//2,
            "C": margin_x + 2*espaço_entre + espaço_entre//2
        }

        self.torre_width = 250
        self.torre_height = 500

        self.canvas.bind("<Button-1>", self.click_canvas)

        # Mensagem de vitória ou dica (separado do rodapé)
        self.lbl_msg = tk.Label(self.frame_principal, text="", font=("Segoe UI", 24, "bold"), fg="green", bg=self.bg_color, wraplength=self.canvas_width, justify="center")
        self.lbl_msg.pack(pady=10)

        # Rodapé com créditos FIXO na base da janela, fora do frame principal
        rodape = tk.Label(self.root,
                          text="Desenvolvido em Python por Leonardo Estevão Alves registro acadêmico 00250458-1",
                          font=("Segoe UI", 16, "bold"),
                          bg="#f2f2f7",
                          fg="#333")
        rodape.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    def alterar_cor_fundo(self):
        cor = colorchooser.askcolor(title="Escolha a cor do fundo")
        if cor[1]:
            self.bg_color = cor[1]
            self.bg_image = None
            self.bg_photoimage = None
            self.frame_principal.config(bg=self.bg_color)
            for widget in self.frame_principal.winfo_children():
                try:
                    widget.config(bg=self.bg_color)
                except:
                    pass
            self.desenhar_torres()

    def selecionar_imagem_fundo(self):
        caminho = filedialog.askopenfilename(title="Selecione a imagem de fundo",
                                             filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if caminho:
            try:
                img = Image.open(caminho)
                img = img.resize((1920, 1080), Image.ANTIALIAS)
                self.bg_photoimage = ImageTk.PhotoImage(img)
                self.bg_image = img
                # Definir imagem no canvas do jogo
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photoimage)
                self.desenhar_torres()  # desenha torres e discos sobre a imagem
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar imagem: {e}")

    def iniciar_jogo(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        if self.timer_dica_id:
            self.root.after_cancel(self.timer_dica_id)
            self.timer_dica_id = None

        self.num_discos = int(self.combo_discos.get())
        self.torres = {"A": list(range(self.num_discos, 0, -1)), "B": [], "C": []}
        self.origem_selecionada = None
        self.movimentos = 0
        self.lbl_movimentos.config(text=f"Movimentos: {self.movimentos}")
        self.lbl_msg.config(text="")
        self.tempo_restante = self.tempo_limite

        if self.modo_regressivo.get():
            self.atualizar_tempo_regressivo()
        else:
            self.tempo_inicio = time.time()
            self.atualizar_tempo()

        self.desenhar_torres()
        self.reiniciar_timer_dica()

    def atualizar_tempo(self):
        if self.lbl_msg.cget("text") == "":
            segundos = int(time.time() - self.tempo_inicio)
            self.lbl_tempo.config(text=f"Tempo: {segundos//60:02d}:{segundos%60:02d}")
            self.timer_id = self.root.after(1000, self.atualizar_tempo)

    def atualizar_tempo_regressivo(self):
        if self.tempo_restante > 0 and self.lbl_msg.cget("text") == "":
            self.lbl_tempo.config(text=f"Tempo: {self.tempo_restante//60:02d}:{self.tempo_restante%60:02d}")
            self.tempo_restante -= 1
            self.timer_id = self.root.after(1000, self.atualizar_tempo_regressivo)
        elif self.tempo_restante == 0:
            self.lbl_msg.config(text="⏰ Tempo esgotado! Tente novamente.")
            self.origem_selecionada = None
            self.salvar_historico(perdeu=True)

    def desenhar_torres(self):
        self.canvas.delete("all")

        # Se tiver imagem, desenha ela como fundo
        if self.bg_photoimage:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photoimage)
        else:
            self.canvas.config(bg=self.bg_color)

        base_y = self.canvas_height
        base_height = 20
        estaca_height = 450
        estaca_width = 20

        # Bases e estacas
        for torre, x in self.torre_pos_x.items():
            self.canvas.create_rectangle(x - self.torre_width//2, base_y,
                                         x + self.torre_width//2, base_y + base_height,
                                         fill="#bbb", outline="")
            self.canvas.create_rectangle(x - estaca_width//2, base_y - estaca_height,
                                         x + estaca_width//2, base_y,
                                         fill="#666", outline="")

        # Discos
        for torre, discos in self.torres.items():
            x = self.torre_pos_x[torre]
            y = base_y - base_height
            for disco in discos:
                largura_max = 220
                largura_min = 50
                largura = largura_min + (disco - 1) * (largura_max - largura_min) / (self.num_discos - 1 if self.num_discos > 1 else 1)
                largura = int(largura)
                cor = self.cor_disco(disco)

                self.canvas.create_rectangle(x - largura//2, y - 30, x + largura//2, y - 2,
                                            fill=cor, outline="black")
                self.canvas.create_text(x, y - 16, text=str(disco), fill="white", font=("Segoe UI", 18, "bold"))

                y -= 36

        # Destaque torre selecionada
        if self.origem_selecionada:
            x = self.torre_pos_x[self.origem_selecionada]
            self.canvas.create_rectangle(x - self.torre_width//2 - 10, base_y - estaca_height - 10,
                                         x + self.torre_width//2 + 10, base_y + base_height + 10,
                                         outline="#007aff", width=6)

    def cor_disco(self, valor):
        cores = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6', '#16a085']
        return cores[valor - 1] if valor -1 < len(cores) else "#7f8c8d"

    def click_canvas(self, event):
        for torre, x in self.torre_pos_x.items():
            if x - self.torre_width//2 <= event.x <= x + self.torre_width//2:
                self.selecionar_torre(torre)
                break

    def selecionar_torre(self, torre):
        if self.lbl_msg.cget("text") != "":
            return

        if self.origem_selecionada is None:
            if len(self.torres[torre]) == 0:
                return
            self.origem_selecionada = torre
        else:
            if self.origem_selecionada == torre:
                self.origem_selecionada = None
            else:
                if self.mover_disco(self.origem_selecionada, torre):
                    self.movimentos += 1
                    self.lbl_movimentos.config(text=f"Movimentos: {self.movimentos}")
                    self.reiniciar_timer_dica()
                self.origem_selecionada = None

        self.desenhar_torres()
        self.verificar_vitoria()

    def mover_disco(self, origem, destino):
        if len(self.torres[origem]) == 0:
            return False
        disco_origem = self.torres[origem][-1]
        disco_destino = self.torres[destino][-1] if len(self.torres[destino]) > 0 else None

        if disco_destino is None or disco_origem < disco_destino:
            self.torres[destino].append(self.torres[origem].pop())
            return True
        return False

    def verificar_vitoria(self):
        if len(self.torres["C"]) == self.num_discos:
            self.lbl_msg.config(text=f"🎉 Parabéns! Você venceu em {self.movimentos} movimentos e {self.lbl_tempo.cget('text')[7:]}!")
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            if self.timer_dica_id:
                self.root.after_cancel(self.timer_dica_id)
                self.timer_dica_id = None
            self.salvar_historico(perdeu=False)

    def reiniciar_timer_dica(self):
        if self.timer_dica_id:
            self.root.after_cancel(self.timer_dica_id)
        self.timer_dica_id = self.root.after(20000, self.mostrar_dica)

    def mostrar_dica(self):
        if self.lbl_msg.cget("text") == "":
            dica = random.choice(self.dicas)
            self.lbl_msg.config(text=f"💡 Dica: {dica}")

    def salvar_historico(self, perdeu=False):
        tempo = self.lbl_tempo.cget("text")[7:]
        status = "Perdeu" if perdeu else "Venceu"
        linha = f"{time.strftime('%d/%m/%Y %H:%M:%S')} - Nível: {self.num_discos} discos - {status} - Movimentos: {self.movimentos} - Tempo: {tempo}\n"
        try:
            with open("historico.txt", "a", encoding="utf-8") as f:
                f.write(linha)
        except Exception as e:
            print("Erro ao salvar histórico:", e)

    def mostrar_historico(self):
        try:
            with open("historico.txt", "r", encoding="utf-8") as f:
                dados = f.read()
        except:
            dados = "Nenhum histórico encontrado."

        janela_hist = tk.Toplevel(self.root)
        janela_hist.title("Histórico de Jogos")
        janela_hist.geometry("800x600")

        txt = tk.Text(janela_hist, font=("Segoe UI", 14))
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert(tk.END, dados)
        txt.config(state=tk.DISABLED)

if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
    except ImportError:
        import sys
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageTk

    root = tk.Tk()
    app = TorreHanoiApp(root)
    root.mainloop()
