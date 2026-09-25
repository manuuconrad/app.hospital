import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ----------------------------------------------------------------------
# 1) CONTEÚDO
# ----------------------------------------------------------------------

CONTEUDO = {
    "hospital": "Hospital Pequeno Príncipe",
    "paciente": "Seu filho",
    "titulo_diagnostico": "Leucemia Linfoblástica Aguda",
    "tipo_ilustracao": "leucemia_linfoblastica_aguda",
    "secoes": [
        {
            "icone": "gota",
            "titulo": "O que esse diagnóstico significa?",
            "cor": "#4A7FE0",
            "cor2": "#6FA0F5",
            "texto": (
                "A leucemia linfoblástica aguda é um câncer do sangue e da medula óssea, "
                "o tecido dentro dos ossos onde as células do sangue são produzidas.\n\n"
                "Nessa doença, células muito jovens chamadas linfoblastos passam a se multiplicar "
                "sem controle e ocupam espaço que deveria formar células sanguíneas saudáveis. "
                "Por isso podem aparecer palidez e cansaço, febre ou infecções, manchas roxas "
                "e sangramentos, além de dores nos ossos ou articulações.\n\n"
                "A doença não surgiu por algo que a família fez ou deixou de fazer e não é contagiosa. "
                "Nos primeiros dias, exames ajudam a definir as características da leucemia e o plano de tratamento."
            ),
        },
        {
            "icone": "estrela",
            "titulo": "O que acontece agora?",
            "cor": "#2FAE9E",
            "cor2": "#5FCBBD",
            "texto": (
                "O tratamento costuma começar logo após a confirmação do diagnóstico e é feito em etapas. "
                "A primeira busca reduzir rapidamente as células da leucemia e alcançar a remissão. Depois, "
                "outras fases tratam células que possam ter permanecido no organismo e reduzem o risco de a doença voltar.\n\n"
                "A quimioterapia é a base do tratamento. Alguns medicamentos podem ser dados pela veia, pela boca "
                "ou no líquido que envolve o cérebro e a medula espinhal. O esquema, a intensidade e a duração "
                "não são iguais para todas as crianças: dependem do tipo de leucemia, dos exames e da resposta ao tratamento."
            ),
        },
        {
            "icone": "escudo",
            "titulo": "O que a família precisa priorizar",
            "cor": "#E0A233",
            "cor2": "#F0C169",
            "texto": (
                "Nas próximas semanas, a equipe vai orientar cuidados para reduzir complicações e acompanhar a resposta ao tratamento.\n\n"
                "• Tenha sempre à mão o telefone da equipe e saiba qual serviço procurar fora do horário\n"
                "• Meça a temperatura quando houver mal-estar e siga exatamente a orientação recebida para febre\n"
                "• Não ofereça remédios, vitaminas, chás ou suplementos sem confirmar com a equipe\n"
                "• Administre as medicações nos horários prescritos e avise se houver vômito ou dose esquecida\n"
                "• Compareça aos exames e consultas, mesmo quando a criança parecer bem\n"
                "• Pergunte quais cuidados com alimentação, escola, visitas e contato com pessoas doentes valem para esta fase"
            ),
        },
    ],
    "alerta_titulo": "Quando entrar em contato com a equipe imediatamente",
    "alerta_itens": [
        "Febre na temperatura definida pela equipe como sinal de alerta — não espere a febre subir",
        "Dificuldade para respirar, respiração muito rápida, lábios arroxeados ou dor no peito",
        "Sangramento que não para, sangue no vômito, urina ou fezes, ou muitas manchas roxas novas",
        "Sonolência incomum, confusão, desmaio, convulsão ou dificuldade para acordar",
        "Dor intensa ou piora rápida do estado geral",
        "Vômitos repetidos, incapacidade de beber líquidos ou sinais de desidratação",
        "Qualquer sintoma que a equipe tenha orientado como urgência durante esta fase do tratamento",
    ],
    "rodape": (
        "Este material é educativo e foi pensado para os primeiros dias após o diagnóstico. "
        "Ele não substitui as orientações da equipe de oncologia pediátrica, que devem prevalecer "
        "sobre qualquer informação geral. Doses, medicamentos e limites de temperatura precisam "
        "seguir o plano individual entregue à família."
    ),
}

# ----------------------------------------------------------------------
# 2) CONFIGURAÇÃO VISUAL
# ----------------------------------------------------------------------

SS = 2
DPI = 150
W, H = int(8.27 * DPI) * SS, int(11.69 * DPI) * SS

COR_FUNDO = (255, 250, 240)
COR_TEXTO = (45, 40, 35)
COR_TEXTO_SUAVE = (108, 100, 90)
COR_ALERTA_BORDA = (224, 96, 79)
COR_ALERTA_FUNDO = (255, 235, 231)

MARGEM = 60 * SS
random.seed(7)

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_FONTES = os.path.join(PASTA_SCRIPT, "fonts")
URL_BASE_POPPINS = "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/"

def _contexto_ssl():
    import ssl
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()

def _baixar_fonte(nome_arquivo, destino):
    import urllib.request
    import ssl
    os.makedirs(PASTA_FONTES, exist_ok=True)
    url = URL_BASE_POPPINS + nome_arquivo
    try:
        ctx = _contexto_ssl()
        with urllib.request.urlopen(url, context=ctx, timeout=15) as resp:
            dados = resp.read()
        with open(destino, "wb") as f:
            f.write(dados)
        return os.path.exists(destino) and os.path.getsize(destino) > 0
    except Exception:
        try:
            ctx_inseguro = ssl._create_unverified_context()
            with urllib.request.urlopen(url, context=ctx_inseguro, timeout=15) as resp:
                dados = resp.read()
            with open(destino, "wb") as f:
                f.write(dados)
            return os.path.exists(destino) and os.path.getsize(destino) > 0
        except Exception:
            return False

def carregar_fonte(nome_arquivo, tamanho):
    caminhos_possiveis = [
        os.path.join(PASTA_FONTES, nome_arquivo),
        f"/usr/share/fonts/truetype/google-fonts/{nome_arquivo}",
        f"/usr/share/fonts/truetype/dejavu/{nome_arquivo}",
        f"C:\\Windows\\Fonts\\{nome_arquivo}",
        f"/System/Library/Fonts/{nome_arquivo}",
        os.path.expanduser(f"~/Library/Fonts/{nome_arquivo}"),
    ]
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            return ImageFont.truetype(caminho, tamanho)

    destino = os.path.join(PASTA_FONTES, nome_arquivo)
    if _baixar_fonte(nome_arquivo, destino):
        return ImageFont.truetype(destino, tamanho)

    try:
        return ImageFont.load_default(size=tamanho)
    except TypeError:
        return ImageFont.load_default()

F_TITULO = carregar_fonte("Poppins-Bold.ttf", 46 * SS)
F_SUBTITULO = carregar_fonte("Poppins-Medium.ttf", 22 * SS)
F_SECAO_TITULO = carregar_fonte("Poppins-Bold.ttf", 26 * SS)
F_TEXTO = carregar_fonte("Poppins-Regular.ttf", 18 * SS)
F_TEXTO_BOLD = carregar_fonte("Poppins-Medium.ttf", 18 * SS)
F_RODAPE = carregar_fonte("Poppins-Regular.ttf", 13 * SS)
F_HOSPITAL = carregar_fonte("Poppins-Medium.ttf", 18 * SS)

# ----------------------------------------------------------------------
# 3) FUNÇÕES AUXILIARES & DESENHOS VETORIAIS
# ----------------------------------------------------------------------

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def gradient_vertical(size, cor_topo, cor_base):
    w, h = size
    base = Image.new("RGB", (1, h), color=0)
    px = base.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = lerp_color(cor_topo, cor_base, t)
    return base.resize((w, h))

def desenhar_estrela(draw, cx, cy, r_ext, r_int, cor, pontas=5, rotacao=-90):
    pontos = []
    ang = math.radians(rotacao)
    passo = math.pi / pontas
    for i in range(pontas * 2):
        raio = r_ext if i % 2 == 0 else r_int
        a = ang + i * passo
        pontos.append((cx + raio * math.cos(a), cy + raio * math.sin(a)))
    draw.polygon(pontos, fill=cor)

def desenhar_estrelas_fundo(draw, box, quantidade, cor, r_min=2, r_max=5):
    x0, y0, x1, y1 = box
    for _ in range(quantidade):
        x = random.uniform(x0, x1)
        y = random.uniform(y0, y1)
        r = random.uniform(r_min, r_max) * SS
        desenhar_estrela(draw, x, y, r, r * 0.42, cor, pontas=4)

def sombra_retangulo(img_rgba, box, radius, blur=14, opacidade=40, offset=(0, 8)):
    ox, oy = offset[0] * SS, offset[1] * SS
    blur *= SS
    sombra = Image.new("RGBA", img_rgba.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sombra)
    box_sombra = [box[0] + ox, box[1] + oy, box[2] + ox, box[3] + oy]
    d.rounded_rectangle(box_sombra, radius=radius, fill=(30, 25, 60, opacidade))
    sombra = sombra.filter(ImageFilter.GaussianBlur(blur))
    img_rgba.alpha_composite(sombra)

def desenhar_icone(draw, tipo, cx, cy, raio, cor_frente="#FFFFFF"):
    if tipo == "gota":
        draw.ellipse([cx - raio, cy - raio * 0.15, cx + raio, cy + raio * 1.05], fill=cor_frente)
        draw.polygon(
            [(cx, cy - raio * 1.25), (cx - raio * 0.78, cy - raio * 0.1),
             (cx + raio * 0.78, cy - raio * 0.1)],
            fill=cor_frente,
        )
    elif tipo == "estrela":
        desenhar_estrela(draw, cx, cy, raio * 1.15, raio * 0.5, cor_frente, pontas=5)
    elif tipo == "escudo":
        draw.polygon(
            [
                (cx, cy - raio * 1.05),
                (cx + raio, cy - raio * 0.5),
                (cx + raio, cy + raio * 0.3),
                (cx, cy + raio * 1.15),
                (cx - raio, cy + raio * 0.3),
                (cx - raio, cy - raio * 0.5),
            ],
            fill=cor_frente,
        )
    elif tipo == "alerta":
        draw.polygon(
            [(cx, cy - raio * 1.1), (cx + raio * 1.05, cy + raio * 0.75),
             (cx - raio * 1.05, cy + raio * 0.75)],
            fill=cor_frente,
        )

def desenhar_badge(img_rgba, draw, cx, cy, raio, cor_hex, cor2_hex, icone):
    cor1, cor2 = hex_to_rgb(cor_hex), hex_to_rgb(cor2_hex)
    d = int(raio * 2)
    grad = gradient_vertical((d, d), cor1, cor2)
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, d, d], fill=255)
    box = [int(cx - raio), int(cy - raio), int(cx - raio) + d, int(cy - raio) + d]
    
    sombra = Image.new("RGBA", img_rgba.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sombra)
    off = 5 * SS
    ds.ellipse([box[0] + off, box[1] + off, box[2] + off, box[3] + off], fill=(30, 25, 60, 60))
    sombra = sombra.filter(ImageFilter.GaussianBlur(6 * SS))
    img_rgba.alpha_composite(sombra)
    
    img_rgba.paste(grad, (box[0], box[1]), mask)
    desenhar_icone(draw, icone, cx, cy, raio * 0.42)

def quebrar_texto(draw, texto, fonte, largura_max):
    linhas_finais = []
    for paragrafo in texto.split("\n"):
        if paragrafo.strip() == "":
            linhas_finais.append("")
            continue
        palavras = paragrafo.split(" ")
        linha_atual = ""
        for palavra in palavras:
            teste = (linha_atual + " " + palavra).strip()
            if draw.textlength(teste, font=fonte) <= largura_max:
                linha_atual = teste
            else:
                if linha_atual:
                    linhas_finais.append(linha_atual)
                linha_atual = palavra
        linhas_finais.append(linha_atual)
    return linhas_finais

def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

# --- GERADOR DE ILUSTRAÇÕES VETORIAIS COM CONTAINER E LEGENDA ---
def desenhar_ilustracao_dinamica(draw, tipo, box):
    """
    Desenha infográficos didáticos com container, rótulos e setas de indicação.
    """
    x0, y0, x1, y1 = box
    w_box, h_box = x1 - x0, y1 - y0
    
    # 1) Fundo tipo "mini card" para abraçar as ilustrações
    rounded_rect(draw, [x0, y0, x1, y1], radius=12 * SS, fill=(248, 249, 252, 255), outline=(225, 230, 240, 255), width=int(1 * SS))

    if tipo == "leucemia_linfoblastica_aguda":
        cy = y0 + h_box * 0.42
        
        # --- A) CÉLULAS DO SANGUE SAUDÁVEIS ---
        cx_norm = x0 + w_box * 0.28
        r_norm = 17 * SS
        draw.ellipse([cx_norm - r_norm, cy - r_norm, cx_norm + r_norm, cy + r_norm], fill=(235, 70, 70))
        draw.ellipse([cx_norm - r_norm*0.48, cy - r_norm*0.48, cx_norm + r_norm*0.48, cy + r_norm*0.48], fill=(250, 145, 145))
        draw.ellipse([cx_norm + 20*SS, cy - 12*SS, cx_norm + 32*SS, cy], fill=(245, 190, 80))
        draw.ellipse([cx_norm - 30*SS, cy + 15*SS, cx_norm - 22*SS, cy + 23*SS], fill=(245, 190, 80))

        # --- B) SETA PARA REPRESENTAR A OCUPAÇÃO DA MEDULA ---
        cx_seta = x0 + w_box * 0.52
        draw.line([(cx_seta - 8*SS, cy), (cx_seta + 6*SS, cy)], fill=(180, 190, 210), width=int(2*SS))
        draw.polygon([(cx_seta + 5*SS, cy - 4*SS), (cx_seta + 11*SS, cy), (cx_seta + 5*SS, cy + 4*SS)], fill=(180, 190, 210))

        # --- C) LINFOBLASTOS EM EXCESSO ---
        cx_leuc = x0 + w_box * 0.76
        for dx, dy, rr in [(-12, -9, 16), (10, -5, 15), (-5, 12, 14), (15, 14, 12)]:
            rr *= SS
            cx = cx_leuc + dx * SS
            yy = cy + dy * SS
            draw.ellipse([cx-rr, yy-rr, cx+rr, yy+rr], fill=(176, 145, 220), outline=(128, 100, 180), width=int(1*SS))
            draw.ellipse([cx-rr*0.45, yy-rr*0.45, cx+rr*0.45, yy+rr*0.45], fill=(115, 86, 165))

        # --- D) LEGENDA ---
        fonte_legenda = carregar_fonte("Poppins-Medium.ttf", 10 * SS)
        tw1 = draw.textlength("Células saudáveis", font=fonte_legenda)
        draw.text((cx_norm - tw1/2, y1 - 22*SS), "Células saudáveis", font=fonte_legenda, fill=(100, 110, 125))
        tw2 = draw.textlength("Linfoblastos", font=fonte_legenda)
        draw.text((cx_leuc - tw2/2, y1 - 22*SS), "Linfoblastos", font=fonte_legenda, fill=(115, 86, 165))

# ----------------------------------------------------------------------
# 4) GERADOR PRINCIPAL
# ----------------------------------------------------------------------

def gerar_panfleto(dados, caminho_saida="panfleto_v2_saida.png"):
    img = Image.new("RGBA", (W, H), COR_FUNDO + (255,))
    draw = ImageDraw.Draw(img)

    desenhar_estrelas_fundo(draw, (0, 0, W, H), 60, (235, 220, 190, 255), 2, 4)

    # Header Otimizado
    altura_header = 210 * SS
    header_grad = gradient_vertical((W, altura_header), hex_to_rgb("#1A2550"), hex_to_rgb("#364790"))
    img.paste(header_grad, (0, 0))
    draw = ImageDraw.Draw(img)

    # Estrelas do header
    for _ in range(40):
        x = random.uniform(0, W)
        y = random.uniform(0, altura_header)
        r = random.uniform(2, 5) * SS
        desenhar_estrela(draw, x, y, r, r * 0.42, (255, 214, 130, 220), pontas=4)

    # Planeta decorativo no topo direito
    px, py, pr = W - 120 * SS, 85 * SS, 42 * SS
    draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(255, 200, 90, 230))
    draw.ellipse([px - pr * 1.6, py - pr * 0.25, px + pr * 1.6, py + pr * 0.25],
                 outline=(255, 226, 158, 200), width=int(3 * SS))

    # Títulos
    draw.text((MARGEM, 20 * SS), dados["hospital"].upper(), font=F_HOSPITAL, fill=(210, 225, 255, 230))
    draw.text((MARGEM, 48 * SS), "Guia da Família", font=F_TITULO, fill=(255, 255, 255, 255))
    
    # Bloco Paciente + Diagnóstico
    paciente_str = f"Paciente: {dados['paciente']}"
    draw.text((MARGEM, 118 * SS), paciente_str, font=F_SUBTITULO, fill=(255, 226, 158, 255))

    diag_txt = dados["titulo_diagnostico"]
    diag_w = draw.textlength(diag_txt, font=F_TEXTO_BOLD) + 40 * SS
    diag_box = [MARGEM, 152 * SS, MARGEM + diag_w, 152 * SS + 36 * SS]
    rounded_rect(draw, diag_box, 18 * SS, fill=(255, 255, 255, 240))
    draw.text((MARGEM + 20 * SS, 158 * SS), diag_txt, font=F_TEXTO_BOLD, fill=hex_to_rgb("#1A2550"))

    y = altura_header + 24 * SS
    largura_texto = W - 2 * MARGEM - 120 * SS

    # Seções Informativas
    for idx, secao in enumerate(dados["secoes"]):
        titulo = secao["titulo"].format(nome=dados["paciente"])
        texto = secao["texto"].format(nome=dados["paciente"])
        cor, cor2 = secao["cor"], secao["cor2"]

        tem_ilustracao = (idx == 0) and ("tipo_ilustracao" in dados)
        largura_texto_secao = largura_texto - (150 * SS if tem_ilustracao else 0)

        linhas = quebrar_texto(draw, texto, F_TEXTO, largura_texto_secao)
        altura_texto = sum(10 * SS if l == '' else 26 * SS for l in linhas)
        altura_painel = 75 * SS + altura_texto + 16 * SS

        box = [MARGEM, y, W - MARGEM, y + altura_painel]
        sombra_retangulo(img, box, 22 * SS, blur=8, opacidade=30, offset=(0, 6))
        rounded_rect(draw, box, 22 * SS, fill=(255, 255, 255, 255))

        barra = [box[0], box[1] + 18 * SS, box[0] + 7 * SS, box[3] - 18 * SS]
        rounded_rect(draw, barra, 3 * SS, fill=hex_to_rgb(cor))

        cx, cy = MARGEM + 55 * SS, y + 46 * SS
        desenhar_badge(img, draw, cx, cy, 25 * SS, cor, cor2, secao["icone"])

        draw.text((MARGEM + 98 * SS, y + 24 * SS), titulo, font=F_SECAO_TITULO, fill=hex_to_rgb(cor))

        if tem_ilustracao:
            box_ilustracao = [W - MARGEM - 160 * SS, y + 60 * SS, W - MARGEM - 20 * SS, y + 180 * SS]
            desenhar_ilustracao_dinamica(draw, dados["tipo_ilustracao"], box_ilustracao)

        ty = y + 68 * SS
        for linha in linhas:
            if linha == "":
                ty += 10 * SS
                continue
            if linha.startswith("• "):
                draw.ellipse([MARGEM + 98 * SS, ty + 8 * SS, MARGEM + 105 * SS, ty + 15 * SS], fill=hex_to_rgb(cor))
                draw.text((MARGEM + 115 * SS, ty), linha[2:], font=F_TEXTO, fill=COR_TEXTO)
            else:
                draw.text((MARGEM + 98 * SS, ty), linha, font=F_TEXTO, fill=COR_TEXTO)
            ty += 26 * SS

        y += altura_painel + 20 * SS

    # Bloco de Urgência / Alerta
    itens = dados["alerta_itens"]
    linhas_alerta = []
    for item in itens:
        linhas_alerta.append(quebrar_texto(draw, item, F_TEXTO_BOLD, largura_texto - 20 * SS))

    total_linhas_alerta = sum(len(l) for l in linhas_alerta)
    altura_alerta = 72 * SS + total_linhas_alerta * 26 * SS + 16 * SS

    box = [MARGEM, y, W - MARGEM, y + altura_alerta]
    sombra_retangulo(img, box, 22 * SS, blur=8, opacidade=30, offset=(0, 6))
    rounded_rect(draw, box, 22 * SS, fill=COR_ALERTA_FUNDO)
    draw.rounded_rectangle(box, radius=22 * SS, outline=COR_ALERTA_BORDA, width=int(2 * SS))

    cx, cy = MARGEM + 55 * SS, y + 44 * SS
    desenhar_badge(img, draw, cx, cy, 25 * SS, "#E0604F", "#F08A6F", "alerta")
    draw.text((MARGEM + 98 * SS, y + 22 * SS), dados["alerta_titulo"], font=F_SECAO_TITULO, fill=COR_ALERTA_BORDA)

    ty = y + 66 * SS
    for linhas_item in linhas_alerta:
        draw.ellipse([MARGEM + 98 * SS, ty + 8 * SS, MARGEM + 106 * SS, ty + 16 * SS], fill=COR_ALERTA_BORDA)
        for idx_l, linha in enumerate(linhas_item):
            indent = 118 * SS if idx_l == 0 else 122 * SS
            draw.text((MARGEM + indent, ty), linha, font=F_TEXTO_BOLD, fill=(122, 46, 43))
            ty += 26 * SS

    y += altura_alerta + 22 * SS

    # Bloco de Anotações
    altura_notas = 145 * SS
    box = [MARGEM, y, W - MARGEM, y + altura_notas]
    sombra_retangulo(img, box, 22 * SS, blur=8, opacidade=25, offset=(0, 5))
    rounded_rect(draw, box, 22 * SS, fill=(255, 255, 255, 255))
    
    desenhar_estrela(draw, MARGEM + 32 * SS, y + 32 * SS, 11 * SS, 5 * SS, hex_to_rgb("#E0A233"))
    draw.text((MARGEM + 52 * SS, y + 20 * SS), "Anote aqui suas dúvidas para a próxima consulta:",
              font=F_TEXTO_BOLD, fill=COR_TEXTO_SUAVE)

    for i in range(4):
        ly = y + 62 * SS + i * 24 * SS
        draw.line([(MARGEM + 28 * SS, ly), (W - MARGEM - 28 * SS, ly)], fill=(220, 212, 196), width=int(SS * 1.2))

    # Rodapé Fixo
    linhas_rodape = quebrar_texto(draw, dados["rodape"], F_RODAPE, W - 2 * MARGEM)
    ty = H - 30 * SS - len(linhas_rodape) * 18 * SS
    for linha in linhas_rodape:
        draw.text((MARGEM, ty), linha, font=F_RODAPE, fill=COR_TEXTO_SUAVE)
        ty += 18 * SS

    img = img.convert("RGB")
    if SS != 1:
        img = img.resize((W // SS, H // SS), Image.LANCZOS)
    img.save(caminho_saida, "PNG")
    print(f"Panfleto gerado em: {caminho_saida}")


if __name__ == "__main__":
    gerar_panfleto(CONTEUDO, "panfleto_leucemia_linfoblastica_aguda.png")
