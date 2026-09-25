import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ----------------------------------------------------------------------
# 1) CONTEÚDO — Leucemia Linfoide Aguda (LLA) em consulta de onco-pediatria
# ----------------------------------------------------------------------

CONTEUDO = {
    "hospital": "Hospital Pequeno Príncipe",
    "paciente": "Sofia",
    "titulo_diagnostico": "Leucemia Linfoide Aguda (LLA)",
    "tipo_ilustracao": "LLA",
    "secoes": [
        {
            "icone": "sangue",
            "titulo": "O que é a Leucemia Linfoide Aguda?",
            "cor": "#3A6EC8",
            "cor2": "#6090E0",
            "texto": (
                "O sangue é formado por três tipos de células: glóbulos vermelhos "
                "(que levam oxigênio), plaquetas (que ajudam a coagular) e glóbulos "
                "brancos (que defendem o corpo contra infecções).\n\n"
                "Na LLA, células jovens da medula óssea — chamadas linfoblastos — "
                "começam a se multiplicar de forma descontrolada e param de amadurecer "
                "corretamente. Com o tempo, elas ocupam o espaço das células saudáveis.\n\n"
                "É o tipo de câncer mais comum na infância. Com o tratamento adequado, "
                "a grande maioria das crianças alcança a cura completa."
            ),
        },
        {
            "icone": "relogio",
            "titulo": "Como o tratamento funciona?",
            "cor": "#2A9E72",
            "cor2": "#4CBFA0",
            "texto": (
                "O tratamento é chamado quimioterapia e acontece em fases ao longo "
                "de 2 a 3 anos. Cada fase tem um objetivo diferente:\n\n"
                "• Indução (primeiras semanas): eliminar o maior número possível de "
                "células doentes e fazer a doença entrar em remissão\n"
                "• Consolidação: reforçar os resultados e proteger o sistema nervoso\n"
                "• Manutenção: manter o organismo livre da doença com doses menores\n\n"
                "Durante o tratamento, a equipe médica fará exames regulares para "
                "acompanhar a resposta do(a) {nome} e ajustar o plano conforme necessário."
            ),
        },
        {
            "icone": "coracao",
            "titulo": "Cuidados em casa durante o tratamento",
            "cor": "#D4622A",
            "cor2": "#F08A56",
            "texto": (
                "Em casa, alguns cuidados são muito importantes:\n\n"
                "• Higiene das mãos: lave as mãos com frequência — toda a família\n"
                "• Evitar aglomerações: escolas e locais com muita gente podem ser "
                "limitados em determinadas fases do tratamento\n"
                "• Febre: qualquer febre acima de 37,8°C é sinal de ir ao hospital "
                "imediatamente — não espere e não dê antitérmico antes de ligar\n"
                "• Alimentação: priorize alimentos bem cozidos e frescos\n"
                "• Vacinas: nenhuma vacina de vírus vivo (como catapora) durante o "
                "tratamento sem orientação médica prévia"
            ),
        },
    ],
    "alerta_titulo": "Quando procurar o hospital imediatamente",
    "alerta_itens": [
        "Febre igual ou acima de 37,8°C — não espere para ver se piora",
        "Sangramentos que não param: nariz, gengiva, manchas roxas na pele",
        "Dificuldade para respirar ou chiado no peito",
        "Dor abdominal intensa ou vômitos repetidos que não melhoram",
        "Qualquer sintoma que pareça grave ou fora do habitual para o(a) seu(sua) filho(a)",
    ],
    "rodape": (
        "Este material tem caráter educativo e foi preparado como apoio à consulta "
        "com a equipe de oncologia pediátrica. Não substitui a orientação médica "
        "individualizada. Dúvidas? Fale diretamente com a equipe responsável pelo tratamento."
    ),
}

# ----------------------------------------------------------------------
# 2) CONFIGURAÇÃO VISUAL
# ----------------------------------------------------------------------

SS = 2
DPI = 150
W, H = int(8.27 * DPI) * SS, int(11.69 * DPI) * SS

COR_FUNDO = (245, 248, 255)
COR_TEXTO = (35, 35, 45)
COR_TEXTO_SUAVE = (100, 100, 115)
COR_ALERTA_BORDA = (210, 60, 60)
COR_ALERTA_FUNDO = (255, 235, 232)

MARGEM = 60 * SS
random.seed(42)

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
# 3) FUNÇÕES AUXILIARES
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


def desenhar_formas_fundo(draw, box, quantidade, cor):
    """Desenha pequenos círculos suaves como fundo decorativo (tema médico/clean)."""
    x0, y0, x1, y1 = box
    for _ in range(quantidade):
        x = random.uniform(x0, x1)
        y = random.uniform(y0, y1)
        r = random.uniform(2, 6) * SS
        draw.ellipse([x - r, y - r, x + r, y + r], fill=cor)


def sombra_retangulo(img_rgba, box, radius, blur=14, opacidade=40, offset=(0, 8)):
    ox, oy = offset[0] * SS, offset[1] * SS
    blur *= SS
    sombra = Image.new("RGBA", img_rgba.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sombra)
    box_sombra = [box[0] + ox, box[1] + oy, box[2] + ox, box[3] + oy]
    d.rounded_rectangle(box_sombra, radius=radius, fill=(30, 25, 60, opacidade))
    sombra = sombra.filter(ImageFilter.GaussianBlur(blur))
    img_rgba.alpha_composite(sombra)


def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# --- ÍCONES ---
def desenhar_icone(draw, tipo, cx, cy, raio, cor_frente="white"):
    """Ícones adaptados ao contexto de oncologia pediátrica."""
    if tipo == "sangue":
        # Gota de sangue estilizada
        draw.ellipse(
            [cx - raio, cy - raio * 0.1, cx + raio, cy + raio * 1.1],
            fill=cor_frente
        )
        draw.polygon(
            [(cx, cy - raio * 1.3), (cx - raio * 0.8, cy), (cx + raio * 0.8, cy)],
            fill=cor_frente,
        )
    elif tipo == "relogio":
        # Cruz médica / calendário simplificado
        espessura = int(raio * 0.38)
        draw.rectangle(
            [cx - espessura // 2, cy - raio, cx + espessura // 2, cy + raio],
            fill=cor_frente
        )
        draw.rectangle(
            [cx - raio, cy - espessura // 2, cx + raio, cy + espessura // 2],
            fill=cor_frente
        )
    elif tipo == "coracao":
        # Coração simplificado
        r = int(raio * 0.65)
        draw.ellipse([cx - raio, cy - raio * 0.6, cx, cy + raio * 0.2], fill=cor_frente)
        draw.ellipse([cx, cy - raio * 0.6, cx + raio, cy + raio * 0.2], fill=cor_frente)
        draw.polygon(
            [(cx - raio, cy), (cx, cy + raio * 1.1), (cx + raio, cy)],
            fill=cor_frente
        )
    elif tipo == "alerta":
        # Triângulo de atenção
        draw.polygon(
            [(cx, cy - raio * 1.1), (cx + raio * 1.05, cy + raio * 0.75),
             (cx - raio * 1.05, cy + raio * 0.75)],
            fill=cor_frente,
        )
        # ! interno
        try:
            f_alerta = carregar_fonte("Poppins-Bold.ttf", int(raio * 1.0))
            draw.text((cx - raio * 0.15, cy - raio * 0.55), "!", font=f_alerta,
                      fill=(200, 50, 50))
        except Exception:
            pass


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
    ds.ellipse([box[0] + off, box[1] + off, box[2] + off, box[3] + off],
               fill=(30, 25, 60, 60))
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


# --- ILUSTRAÇÃO VETORIAL — CÉLULAS DO SANGUE (LLA) ---
def desenhar_ilustracao_LLA(draw, box):
    """
    Infográfico didático: mostra células saudáveis vs. linfoblastos em excesso.
    Transmite de forma visual e acolhedora o conceito da doença.
    """
    x0, y0, x1, y1 = box
    w_box, h_box = x1 - x0, y1 - y0

    # Fundo do mini-card
    rounded_rect(draw, [x0, y0, x1, y1], radius=12 * SS,
                 fill=(248, 250, 255), outline=(210, 220, 240), width=int(1 * SS))

    cy = y0 + h_box * 0.42

    # --- A) Glóbulo vermelho saudável (disco bicôncavo) ---
    cx_a = x0 + w_box * 0.18
    r_a = 18 * SS
    draw.ellipse([cx_a - r_a, cy - r_a * 0.7, cx_a + r_a, cy + r_a * 0.7],
                 fill=(230, 55, 55))
    draw.ellipse([cx_a - r_a * 0.45, cy - r_a * 0.3, cx_a + r_a * 0.45, cy + r_a * 0.3],
                 fill=(245, 130, 130))

    # --- B) Linfócito maduro (pequeno, normal) ---
    cx_b = x0 + w_box * 0.42
    r_b = 14 * SS
    draw.ellipse([cx_b - r_b, cy - r_b, cx_b + r_b, cy + r_b], fill=(80, 140, 220))
    draw.ellipse([cx_b - r_b * 0.5, cy - r_b * 0.5,
                  cx_b + r_b * 0.5, cy + r_b * 0.5], fill=(140, 185, 245))

    # --- Seta indicativa ---
    cx_seta = x0 + w_box * 0.62
    draw.line([(cx_seta - 6 * SS, cy), (cx_seta + 8 * SS, cy)],
              fill=(180, 60, 60), width=int(2.5 * SS))
    draw.polygon([(cx_seta + 7 * SS, cy - 4 * SS),
                  (cx_seta + 14 * SS, cy),
                  (cx_seta + 7 * SS, cy + 4 * SS)], fill=(180, 60, 60))

    # --- C) Linfoblasto (grande, imaturo — doença) ---
    cx_c = x0 + w_box * 0.84
    r_c = 22 * SS
    # Contorno indicando anormalidade
    draw.ellipse([cx_c - r_c - 2, cy - r_c - 2, cx_c + r_c + 2, cy + r_c + 2],
                 fill=(220, 80, 80))
    draw.ellipse([cx_c - r_c, cy - r_c, cx_c + r_c, cy + r_c],
                 fill=(160, 55, 200))
    # Núcleo grande (característica do linfoblasto)
    draw.ellipse([cx_c - r_c * 0.65, cy - r_c * 0.65,
                  cx_c + r_c * 0.65, cy + r_c * 0.65], fill=(100, 20, 160))

    # --- Legendas ---
    fonte_leg = carregar_fonte("Poppins-Medium.ttf", 9 * SS)
    y_leg = y1 - 20 * SS

    for cx_l, texto, cor in [
        (cx_a, "Glóbulo", (140, 50, 50)),
        (cx_a, "vermelho", (140, 50, 50)),
        (cx_b, "Linfócito", (60, 100, 180)),
        (cx_b, "normal", (60, 100, 180)),
        (cx_c, "Linfoblasto", (140, 30, 180)),
        (cx_c, "(doente)", (140, 30, 180)),
    ]:
        pass

    # Labels de 2 linhas centralizados
    for cx_l, linhas, cor in [
        (cx_a, ["Glóbulo", "vermelho"], (140, 50, 50)),
        (cx_b, ["Linfócito", "normal"], (60, 100, 180)),
        (cx_c, ["Linfoblasto", "(doente)"], (140, 30, 180)),
    ]:
        for i, linha in enumerate(linhas):
            tw = draw.textlength(linha, font=fonte_leg)
            draw.text((cx_l - tw / 2, y_leg - (len(linhas) - 1 - i) * 14 * SS),
                      linha, font=fonte_leg, fill=cor)


# ----------------------------------------------------------------------
# 4) GERADOR PRINCIPAL
# ----------------------------------------------------------------------

def gerar_panfleto(dados, caminho_saida="panfleto_LLA.png"):
    img = Image.new("RGBA", (W, H), COR_FUNDO + (255,))
    draw = ImageDraw.Draw(img)

    # Fundo decorativo: círculos suaves (remetem a células)
    desenhar_formas_fundo(draw, (0, 0, W, H), 80, (220, 230, 248, 255))

    # Header com gradiente (azul médico profundo → azul-marinho)
    altura_header = 210 * SS
    header_grad = gradient_vertical(
        (W, altura_header),
        hex_to_rgb("#0D2550"),
        hex_to_rgb("#1A4A8A")
    )
    img.paste(header_grad, (0, 0))
    draw = ImageDraw.Draw(img)

    # Decoração do header: pequenos círculos/células flutuantes
    for _ in range(35):
        x = random.uniform(0, W)
        y = random.uniform(0, altura_header)
        r = random.uniform(3, 8) * SS
        alpha_cor = random.choice([(255, 200, 100, 160), (150, 200, 255, 120), (255, 255, 255, 80)])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=alpha_cor)

    # Círculo decorativo no canto superior direito (DNA/célula)
    px, py, pr = W - 110 * SS, 80 * SS, 45 * SS
    draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(100, 170, 255, 180))
    draw.ellipse([px - pr * 0.65, py - pr * 0.65, px + pr * 0.65, py + pr * 0.65],
                 fill=(50, 120, 220, 200))
    # Cruz médica no círculo decorativo
    e = int(pr * 0.22)
    draw.rectangle([px - e, py - int(pr * 0.6), px + e, py + int(pr * 0.6)],
                   fill=(255, 255, 255, 220))
    draw.rectangle([px - int(pr * 0.6), py - e, px + int(pr * 0.6), py + e],
                   fill=(255, 255, 255, 220))

    # Textos do header
    draw.text((MARGEM, 18 * SS), dados["hospital"].upper(),
              font=F_HOSPITAL, fill=(170, 210, 255, 230))
    draw.text((MARGEM, 46 * SS), "Guia da Família", font=F_TITULO, fill=(255, 255, 255))

    # Faixa do nome do paciente
    paciente_str = f"Paciente: {dados['paciente']}"
    draw.text((MARGEM, 116 * SS), paciente_str, font=F_SUBTITULO, fill=(255, 210, 100, 255))

    # Pílula do diagnóstico
    diag_txt = dados["titulo_diagnostico"]
    diag_w = draw.textlength(diag_txt, font=F_TEXTO_BOLD) + 44 * SS
    diag_box = [MARGEM, 150 * SS, MARGEM + diag_w, 150 * SS + 38 * SS]
    rounded_rect(draw, diag_box, 19 * SS, fill=(255, 255, 255, 245))
    draw.text((MARGEM + 22 * SS, 157 * SS), diag_txt,
              font=F_TEXTO_BOLD, fill=hex_to_rgb("#0D2550"))

    y = altura_header + 26 * SS
    largura_texto = W - 2 * MARGEM - 120 * SS

    # Seções Informativas
    for idx, secao in enumerate(dados["secoes"]):
        titulo = secao["titulo"].format(nome=dados["paciente"])
        texto = secao["texto"].format(nome=dados["paciente"])
        cor, cor2 = secao["cor"], secao["cor2"]

        tem_ilustracao = (idx == 0)
        largura_texto_secao = largura_texto - (155 * SS if tem_ilustracao else 0)

        linhas = quebrar_texto(draw, texto, F_TEXTO, largura_texto_secao)
        altura_texto = sum(10 * SS if l == "" else 26 * SS for l in linhas)
        altura_painel = 78 * SS + altura_texto + 18 * SS

        box = [MARGEM, y, W - MARGEM, y + altura_painel]
        sombra_retangulo(img, box, 22 * SS, blur=8, opacidade=28, offset=(0, 6))
        rounded_rect(draw, box, 22 * SS, fill=(255, 255, 255, 255))

        # Barra colorida lateral
        barra = [box[0], box[1] + 20 * SS, box[0] + 7 * SS, box[3] - 20 * SS]
        rounded_rect(draw, barra, 3 * SS, fill=hex_to_rgb(cor))

        # Badge com ícone
        cx, cy = MARGEM + 55 * SS, y + 46 * SS
        desenhar_badge(img, draw, cx, cy, 25 * SS, cor, cor2, secao["icone"])

        draw.text((MARGEM + 100 * SS, y + 25 * SS), titulo,
                  font=F_SECAO_TITULO, fill=hex_to_rgb(cor))

        # Ilustração na primeira seção
        if tem_ilustracao:
            box_il = [W - MARGEM - 165 * SS, y + 58 * SS,
                      W - MARGEM - 18 * SS, y + 185 * SS]
            desenhar_ilustracao_LLA(draw, box_il)

        ty = y + 70 * SS
        for linha in linhas:
            if linha == "":
                ty += 10 * SS
                continue
            if linha.startswith("• "):
                draw.ellipse([MARGEM + 100 * SS, ty + 8 * SS,
                              MARGEM + 108 * SS, ty + 16 * SS], fill=hex_to_rgb(cor))
                draw.text((MARGEM + 118 * SS, ty), linha[2:],
                          font=F_TEXTO, fill=COR_TEXTO)
            else:
                draw.text((MARGEM + 100 * SS, ty), linha,
                          font=F_TEXTO, fill=COR_TEXTO)
            ty += 26 * SS

        y += altura_painel + 22 * SS

    # Bloco de Urgência / Alerta
    itens = dados["alerta_itens"]
    linhas_alerta = [quebrar_texto(draw, item, F_TEXTO_BOLD, largura_texto - 22 * SS)
                     for item in itens]

    total_linhas_alerta = sum(len(l) for l in linhas_alerta)
    altura_alerta = 74 * SS + total_linhas_alerta * 26 * SS + 18 * SS

    box = [MARGEM, y, W - MARGEM, y + altura_alerta]
    sombra_retangulo(img, box, 22 * SS, blur=8, opacidade=30, offset=(0, 6))
    rounded_rect(draw, box, 22 * SS, fill=COR_ALERTA_FUNDO)
    draw.rounded_rectangle(box, radius=22 * SS, outline=COR_ALERTA_BORDA,
                           width=int(2 * SS))

    cx, cy = MARGEM + 55 * SS, y + 44 * SS
    desenhar_badge(img, draw, cx, cy, 25 * SS, "#CC3030", "#E86060", "alerta")
    draw.text((MARGEM + 100 * SS, y + 23 * SS), dados["alerta_titulo"],
              font=F_SECAO_TITULO, fill=COR_ALERTA_BORDA)

    ty = y + 68 * SS
    for linhas_item in linhas_alerta:
        draw.ellipse([MARGEM + 100 * SS, ty + 8 * SS,
                      MARGEM + 108 * SS, ty + 16 * SS], fill=COR_ALERTA_BORDA)
        for idx_l, linha in enumerate(linhas_item):
            indent = 120 * SS if idx_l == 0 else 124 * SS
            draw.text((MARGEM + indent, ty), linha,
                      font=F_TEXTO_BOLD, fill=(120, 30, 30))
            ty += 26 * SS

    y += altura_alerta + 24 * SS

    # Bloco de Anotações para a consulta
    altura_notas = 148 * SS
    box = [MARGEM, y, W - MARGEM, y + altura_notas]
    sombra_retangulo(img, box, 22 * SS, blur=8, opacidade=22, offset=(0, 5))
    rounded_rect(draw, box, 22 * SS, fill=(255, 255, 255, 255))

    # Ícone de lápis / estrela antes do rótulo
    desenhar_estrela(draw, MARGEM + 32 * SS, y + 32 * SS, 11 * SS, 5 * SS,
                     hex_to_rgb("#3A6EC8"), pontas=6)
    draw.text((MARGEM + 52 * SS, y + 20 * SS),
              "Anote aqui suas perguntas para a equipe médica:",
              font=F_TEXTO_BOLD, fill=COR_TEXTO_SUAVE)

    for i in range(4):
        ly = y + 64 * SS + i * 24 * SS
        draw.line([(MARGEM + 28 * SS, ly), (W - MARGEM - 28 * SS, ly)],
                  fill=(200, 210, 235), width=int(SS * 1.2))

    # Rodapé
    linhas_rodape = quebrar_texto(draw, dados["rodape"], F_RODAPE, W - 2 * MARGEM)
    ty = H - 32 * SS - len(linhas_rodape) * 18 * SS
    for linha in linhas_rodape:
        draw.text((MARGEM, ty), linha, font=F_RODAPE, fill=COR_TEXTO_SUAVE)
        ty += 18 * SS

    img = img.convert("RGB")
    if SS != 1:
        img = img.resize((W // SS, H // SS), Image.LANCZOS)
    img.save(caminho_saida, "PNG", dpi=(150, 150))
    print(f"Panfleto gerado em: {caminho_saida}")


if __name__ == "__main__":
    gerar_panfleto(CONTEUDO, "panfleto_LLA.png")
