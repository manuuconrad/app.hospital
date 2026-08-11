import io
import os
import math
import random
import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ==============================================================================
# 1. BANCO DE DADOS DE CONTEÚDO (ADICIONE OU EDITE NOVAS DOENÇAS AQUI)
# ==============================================================================

CONTEUDOS = {
    "anemia_falciforme": {
        "nome_select": "Anemia Falciforme",
        "hospital": "Hospital Pequeno Príncipe",
        "titulo_diagnostico": "Anemia Falciforme",
        "tipo_ilustracao": "anemia_falciforme",
        "secoes": [
            {
                "icone": "gota",
                "titulo": "O que o(a) {nome} tem?",
                "cor": "#4A7FE0",
                "cor2": "#6FA0F5",
                "texto": (
                    "Dentro do nosso sangue existem milhões de \"carrinhos vermelhos\" "
                    "chamados glóbulos vermelhos. Eles levam oxigênio para todo o corpo, "
                    "dos pés até o cérebro.\n\n"
                    "Normalmente esses carrinhos são redondinhos e flexíveis, o que "
                    "ajuda a passar até pelos caminhos mais estreitos do corpo.\n\n"
                    "O(a) {nome} nasceu com uma característica genética que muda um "
                    "pouco esse formato: em vez de redondos, alguns ficam parecidos "
                    "com uma foice — por isso o nome \"falciforme\". Não é uma doença "
                    "que se pega de alguém, é algo que já veio desde o nascimento."
                ),
            },
            {
                "icone": "estrela",
                "titulo": "O que isso faz no corpo?",
                "cor": "#2FAE9E",
                "cor2": "#5FCBBD",
                "texto": (
                    "Os glóbulos em formato de foice são mais durinhos e podem ter "
                    "dificuldade de passar pelos vasinhos mais estreitos — como um "
                    "carrinho grande tentando passar por uma ruazinha apertada.\n\n"
                    "Isso pode causar dor (às vezes forte) em braços, pernas, barriga "
                    "ou costas, cansaço, e uma chance maior de infecções.\n\n"
                    "Esses episódios são chamados de \"crise\". Não significa que algo "
                    "deu errado — é uma característica da própria condição, e a "
                    "equipe médica sabe como agir quando ela acontece."
                ),
            },
            {
                "icone": "escudo",
                "titulo": "O caminho do cuidado",
                "cor": "#E0A233",
                "cor2": "#F0C169",
                "texto": (
                    "O acompanhamento do(a) {nome} vai incluir consultas regulares "
                    "com a equipe de hematologia, que vai acompanhar de perto e "
                    "ajustar os cuidados ao longo do tempo.\n\n"
                    "Algumas atitudes do dia a dia ajudam bastante:\n"
                    "• Manter o(a) {nome} bem hidratado(a), sempre\n"
                    "• Evitar calor ou frio excessivos\n"
                    "• Respeitar o cansaço e o descanso\n"
                    "• Não faltar às consultas e exames marcados\n\n"
                    "As orientações específicas de medicação e doses estão na "
                    "receita entregue pelo médico responsável."
                ),
            },
        ],
        "alerta_titulo": "Quando procurar o hospital com urgência",
        "alerta_itens": [
            "Qualquer febre, mesmo baixa",
            "Dor muito forte que não passa",
            "Dificuldade para respirar ou dor no peito",
            "Fraqueza súbita de um lado do corpo ou dificuldade para falar",
            "Barriga muito inchada ou dura",
            "Sonolência excessiva ou dificuldade para acordar",
            "Palidez muito forte",
        ],
        "rodape": (
            "Este material tem caráter educativo e não substitui a orientação "
            "médica individual. Qualquer dúvida sobre tratamento, medicação ou "
            "sintomas específicos, converse com a equipe médica responsável."
        ),
    },
    
    "talassemia_minor": {
        "nome_select": "Talassemia Minor",
        "hospital": "Hospital Pequeno Príncipe",
        "titulo_diagnostico": "Talassemia Minor (Traço Talassêmico)",
        "tipo_ilustracao": "talassemia_minor",
        "secoes": [
            {
                "icone": "gota",
                "titulo": "O que é a Talassemia Minor?",
                "cor": "#4A7FE0",
                "cor2": "#6FA0F5",
                "texto": (
                    "O nosso sangue possui glóbulos vermelhos (hemácias), que são "
                    "responsáveis por levar oxigênio para todo o corpo por meio de "
                    "uma proteína chamada hemoglobina.\n\n"
                    "Ter Talassemia Minor (ou Traço Talassêmico) significa apenas que o "
                    "corpo do(a) {nome} produz essas hemácias em um tamanho um pouco "
                    "menor e mais pálido do que o habitual.\n\n"
                    "É uma característica genética hereditária (passada dos pais para "
                    "os filhos) e totalmente saudável. Não é uma doença grave nem um "
                    "motivo de preocupação."
                ),
            },
            {
                "icone": "estrela",
                "titulo": "Como isso afeta o dia a dia?",
                "cor": "#2FAE9E",
                "cor2": "#5FCBBD",
                "texto": (
                    "Na prática, não afeta em nada! O(a) {nome} pode brincar, correr, "
                    "estudar e ter uma rotina completamente normal e sem limitações.\n\n"
                    "Nos exames de sangue, é comum aparecer uma 'anemia leve', mas o "
                    "próprio organismo compensa isso fabricando mais glóbulos vermelhos.\n\n"
                    "Atenção: essa condição NÃO é causada por falta de ferro! Por isso, "
                    "não adianta tomar remédios ou suplementos de ferro por conta própria."
                ),
            },
            {
                "icone": "escudo",
                "titulo": "Cuidados e Recomendações",
                "cor": "#E0A233",
                "cor2": "#F0C169",
                "texto": (
                    "O acompanhamento é bem simples e serve para garantir a saúde geral:\n\n"
                    "• Vida ativa: incentive a prática de atividades físicas e esportes\n"
                    "• Alimentação saudável: mantenha uma dieta variada e equilibrada\n"
                    "• Uso de ferro: só utilize se o médico indicar após exames específicos\n"
                    "• Rotina: mantenha as consultas com o pediatra em dia\n"
                    "• Futuro: no futuro, em idade adulta, é recomendado aconselhamento "
                    "genético para planejamento familiar."
                ),
            },
        ],
        "alerta_titulo": "Sinais para prestar atenção",
        "alerta_itens": [
            "Cansaço exagerado ou fraqueza fora do comum para a rotina da criança",
            "Palidez muito acentuada na pele, lábios ou parte interna das pálpebras",
            "Febre ou episódios de infecção acompanhados de desânimo",
            "Pele ou olhos amarelados (icterícia)",
            "Dúvidas antes de iniciar qualquer suplemento de ferro prescrito por outro profissional",
        ],
        "rodape": (
            "Este material tem caráter educativo e não substitui a orientação "
            "médica individual. Qualquer dúvida sobre o acompanhamento do(a) seu(sua) filho(a), "
            "converse com a equipe médica responsável."
        ),
    },

    # 💡 PARA ADICIONAR UMA NOVA DOENÇA NO FUTURO, BASTA DUPLICAR UM BLOCO
}

# ==============================================================================
# 2. SISTEMA DE FONTES E MOTOR GRÁFICO (NÃO PRECISA MEXER AQUI)
# ==============================================================================

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else "."
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
    caminhos = [
        os.path.join(PASTA_FONTES, nome_arquivo),
        f"/usr/share/fonts/truetype/google-fonts/{nome_arquivo}",
        f"C:\\Windows\\Fonts\\{nome_arquivo}",
        f"/System/Library/Fonts/{nome_arquivo}",
    ]
    for c in caminhos:
        if os.path.exists(c):
            return ImageFont.truetype(c, tamanho)

    destino = os.path.join(PASTA_FONTES, nome_arquivo)
    if _baixar_fonte(nome_arquivo, destino):
        return ImageFont.truetype(destino, tamanho)

    try:
        return ImageFont.load_default(size=tamanho)
    except TypeError:
        return ImageFont.load_default()

SS = 2
DPI = 150
W, H = int(8.27 * DPI) * SS, int(11.69 * DPI) * SS
COR_FUNDO = (255, 250, 240)
COR_TEXTO = (45, 40, 35)
COR_TEXTO_SUAVE = (108, 100, 90)
COR_ALERTA_BORDA = (224, 96, 79)
COR_ALERTA_FUNDO = (255, 235, 231)
MARGEM = 60 * SS

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
        draw.polygon([(cx, cy - raio * 1.25), (cx - raio * 0.78, cy - raio * 0.1), (cx + raio * 0.78, cy - raio * 0.1)], fill=cor_frente)
    elif tipo == "estrela":
        desenhar_estrela(draw, cx, cy, raio * 1.15, raio * 0.5, cor_frente, pontas=5)
    elif tipo == "escudo":
        draw.polygon([(cx, cy - raio * 1.05), (cx + raio, cy - raio * 0.5), (cx + raio, cy + raio * 0.3), (cx, cy + raio * 1.15), (cx - raio, cy + raio * 0.3), (cx - raio, cy - raio * 0.5)], fill=cor_frente)
    elif tipo == "alerta":
        draw.polygon([(cx, cy - raio * 1.1), (cx + raio * 1.05, cy + raio * 0.75), (cx - raio * 1.05, cy + raio * 0.75)], fill=cor_frente)

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

def desenhar_ilustracao_dinamica(draw, tipo, box, fontes):
    x0, y0, x1, y1 = box
    w_box, h_box = x1 - x0, y1 - y0
    rounded_rect(draw, [x0, y0, x1, y1], radius=12 * SS, fill=(248, 249, 252, 255), outline=(225, 230, 240, 255), width=int(1 * SS))
    cy = y0 + h_box * 0.42

    if tipo == "anemia_falciforme":
        cx_norm, r_norm = x0 + w_box * 0.28, 18 * SS
        draw.ellipse([cx_norm - r_norm, cy - r_norm + 2*SS, cx_norm + r_norm, cy + r_norm + 2*SS], fill=(220, 180, 180, 150))
        draw.ellipse([cx_norm - r_norm, cy - r_norm, cx_norm + r_norm, cy + r_norm], fill=(235, 60, 60))
        draw.ellipse([cx_norm - r_norm*0.5, cy - r_norm*0.5, cx_norm + r_norm*0.5, cy + r_norm*0.5], fill=(250, 130, 130))

        cx_seta = x0 + w_box * 0.52
        draw.line([(cx_seta - 8*SS, cy), (cx_seta + 6*SS, cy)], fill=(180, 190, 210), width=int(2*SS))
        draw.polygon([(cx_seta + 5*SS, cy - 4*SS), (cx_seta + 11*SS, cy), (cx_seta + 5*SS, cy + 4*SS)], fill=(180, 190, 210))

        cx_fal, r_fal = x0 + w_box * 0.76, 20 * SS
        pontos_foice = [
            (cx_fal - r_fal*0.6, cy - r_fal*0.8), (cx_fal + r_fal*0.1, cy - r_fal*0.7),
            (cx_fal + r_fal*0.6, cy - r_fal*0.2), (cx_fal + r_fal*0.7, cy + r_fal*0.4),
            (cx_fal + r_fal*0.3, cy + r_fal*0.8), (cx_fal - r_fal*0.2, cy + r_fal*0.5),
            (cx_fal + r_fal*0.2, cy + r_fal*0.2), (cx_fal + r_fal*0.1, cy - r_fal*0.3),
            (cx_fal - r_fal*0.6, cy - r_fal*0.8)
        ]
        draw.polygon(pontos_foice, fill=(210, 40, 40))

        tw1 = draw.textlength("Normal", font=fontes["legenda"])
        draw.text((cx_norm - tw1/2, y1 - 22*SS), "Normal", font=fontes["legenda"], fill=(100, 110, 125))
        tw2 = draw.textlength("Em foice", font=fontes["legenda"])
        draw.text((cx_fal - tw2/2, y1 - 22*SS), "Em foice", font=fontes["legenda"], fill=(190, 50, 50))

    elif tipo == "talassemia_minor":
        cx_norm, r_norm = x0 + w_box * 0.28, 20 * SS
        draw.ellipse([cx_norm - r_norm, cy - r_norm + 2*SS, cx_norm + r_norm, cy + r_norm + 2*SS], fill=(220, 180, 180, 150))
        draw.ellipse([cx_norm - r_norm, cy - r_norm, cx_norm + r_norm, cy + r_norm], fill=(235, 60, 60))
        draw.ellipse([cx_norm - r_norm*0.45, cy - r_norm*0.45, cx_norm + r_norm*0.45, cy + r_norm*0.45], fill=(250, 140, 140))

        cx_seta = x0 + w_box * 0.52
        draw.line([(cx_seta - 8*SS, cy), (cx_seta + 6*SS, cy)], fill=(180, 190, 210), width=int(2*SS))
        draw.polygon([(cx_seta + 5*SS, cy - 4*SS), (cx_seta + 11*SS, cy), (cx_seta + 5*SS, cy + 4*SS)], fill=(180, 190, 210))

        cx_micro, r_micro = x0 + w_box * 0.76, 13 * SS
        draw.ellipse([cx_micro - r_micro, cy - r_micro + 2*SS, cx_micro + r_micro, cy + r_micro + 2*SS], fill=(220, 180, 180, 120))
        draw.ellipse([cx_micro - r_micro, cy - r_micro, cx_micro + r_micro, cy + r_micro], fill=(220, 80, 80))
        draw.ellipse([cx_micro - r_micro*0.7, cy - r_micro*0.7, cx_micro + r_micro*0.7, cy + r_micro*0.7], fill=(248, 205, 205))

        tw1 = draw.textlength("Normal", font=fontes["legenda"])
        draw.text((cx_norm - tw1/2, y1 - 22*SS), "Normal", font=fontes["legenda"], fill=(100, 110, 125))
        tw2 = draw.textlength("Menor/Pálida", font=fontes["legenda"])
        draw.text((cx_micro - tw2/2, y1 - 22*SS), "Menor/Pálida", font=fontes["legenda"], fill=(190, 60, 60))

def gerar_imagem_panfleto(dados, nome_paciente):
    random.seed(7)
    img = Image.new("RGBA", (W, H), COR_FUNDO + (255,))
    draw = ImageDraw.Draw(img)

    fontes = {
        "titulo": carregar_fonte("Poppins-Bold.ttf", 46 * SS),
        "subtitulo": carregar_fonte("Poppins-Medium.ttf", 22 * SS),
        "secao_titulo": carregar_fonte("Poppins-Bold.ttf", 26 * SS),
        "texto": carregar_fonte("Poppins-Regular.ttf", 18 * SS),
        "texto_bold": carregar_fonte("Poppins-Medium.ttf", 18 * SS),
        "rodape": carregar_fonte("Poppins-Regular.ttf", 13 * SS),
        "hospital": carregar_fonte("Poppins-Medium.ttf", 18 * SS),
        "legenda": carregar_fonte("Poppins-Medium.ttf", 10 * SS)
    }

    desenhar_estrelas_fundo(draw, (0, 0, W, H), 60, (235, 220, 190, 255), 2, 4)

    altura_header = 210 * SS
    header_grad = gradient_vertical((W, altura_header), hex_to_rgb("#1A2550"), hex_to_rgb("#364790"))
    img.paste(header_grad, (0, 0))
    draw = ImageDraw.Draw(img)

    for _ in range(40):
        x, y = random.uniform(0, W), random.uniform(0, altura_header)
        r = random.uniform(2, 5) * SS
        desenhar_estrela(draw, x, y, r, r * 0.42, (255, 214, 130, 220), pontas=4)

    px, py, pr = W - 120 * SS, 85 * SS, 42 * SS
    draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(255, 200, 90, 230))
    draw.ellipse([px - pr * 1.6, py - pr * 0.25, px + pr * 1.6, py + pr * 0.25], outline=(255, 226, 158, 200), width=int(3 * SS))

    draw.text((MARGEM, 20 * SS), dados["hospital"].upper(), font=fontes["hospital"], fill=(210, 225, 255, 230))
    draw.text((MARGEM, 48 * SS), "Guia da Família", font=fontes["titulo"], fill=(255, 255, 255, 255))
    draw.text((MARGEM, 118 * SS), f"Paciente: {nome_paciente}", font=fontes["subtitulo"], fill=(255, 226, 158, 255))

    diag_txt = dados["titulo_diagnostico"]
    diag_w = draw.textlength(diag_txt, font=fontes["texto_bold"]) + 40 * SS
    diag_box = [MARGEM, 152 * SS, MARGEM + diag_w, 152 * SS + 36 * SS]
    rounded_rect(draw, diag_box, 18 * SS, fill=(255, 255, 255, 240))
    draw.text((MARGEM + 20 * SS, 158 * SS), diag_txt, font=fontes["texto_bold"], fill=hex_to_rgb("#1A2550"))

    y = altura_header + 24 * SS
    largura_texto = W - 2 * MARGEM - 120 * SS

    for idx, secao in enumerate(dados["secoes"]):
        titulo = secao["titulo"].format(nome=nome_paciente)
        texto = secao["texto"].format(nome=nome_paciente)
        cor, cor2 = secao["cor"], secao["cor2"]

        tem_ilustracao = (idx == 0) and ("tipo_ilustracao" in dados)
        largura_texto_secao = largura_texto - (150 * SS if tem_ilustracao else 0)

        linhas = quebrar_texto(draw, texto, fontes["texto"], largura_texto_secao)
        altura_texto = sum(10 * SS if l == '' else 26 * SS for l in linhas)
        altura_painel = 75 * SS + altura_texto + 16 * SS

        box = [MARGEM, y, W - MARGEM, y + altura_painel]
        sombra_retangulo(img, box, 22 * SS, blur=8, opacidade=30, offset=(0, 6))
        rounded_rect(draw, box, 22 * SS, fill=(255, 255, 255, 255))

        barra = [box[0], box[1] + 18 * SS, box[0] + 7 * SS, box[3] - 18 * SS]
        rounded_rect(draw, barra, 3 * SS, fill=hex_to_rgb(cor))

        cx, cy = MARGEM + 55 * SS, y + 46 * SS
        desenhar_badge(img, draw, cx, cy, 25 * SS, cor, cor2, secao["icone"])

        draw.text((MARGEM + 98 * SS, y + 24 * SS), titulo, font=fontes["secao_titulo"], fill=hex_to_rgb(cor))

        if tem_ilustracao:
            box_ilustracao = [W - MARGEM - 160 * SS, y + 60 * SS, W - MARGEM - 20 * SS, y + 180 * SS]
            desenhar_ilustracao_dinamica(draw, dados["tipo_ilustracao"], box_ilustracao, fontes)

        ty = y + 68 * SS
        for linha in linhas:
            if linha == "":
                ty += 10 * SS
                continue
            if linha.startswith("• "):
                draw.ellipse([MARGEM + 98 * SS, ty + 8 * SS, MARGEM + 105 * SS, ty + 15 * SS], fill=hex_to_rgb(cor))
                draw.text((MARGEM + 115 * SS, ty), linha[2:], font=fontes["texto"], fill=COR_TEXTO)
            else:
                draw.text((MARGEM + 98 * SS, ty), linha, font=fontes["texto"], fill=COR_TEXTO)
            ty += 26 * SS

        y += altura_painel + 20 * SS

    itens = dados["alerta_itens"]
    linhas_alerta = [quebrar_texto(draw, item, fontes["texto_bold"], largura_texto - 20 * SS) for item in itens]
    total_linhas_alerta = sum(len(l) for l in linhas_alerta)
    altura_alerta = 72 * SS + total_linhas_alerta * 26 * SS + 16 * SS

    box = [MARGEM, y, W - MARGEM, y + altura_alerta]
    sombra_retangulo(img, box, 22 * SS, blur=8, opacidade=30, offset=(0, 6))
    rounded_rect(draw, box, 22 * SS, fill=COR_ALERTA_FUNDO)
    draw.rounded_rectangle(box, radius=22 * SS, outline=COR_ALERTA_BORDA, width=int(2 * SS))

    cx, cy = MARGEM + 55 * SS, y + 44 * SS
    desenhar_badge(img, draw, cx, cy, 25 * SS, "#E0604F", "#F08A6F", "alerta")
    draw.text((MARGEM + 98 * SS, y + 22 * SS), dados["alerta_titulo"], font=fontes["secao_titulo"], fill=COR_ALERTA_BORDA)

    ty = y + 66 * SS
    for linhas_item in linhas_alerta:
        draw.ellipse([MARGEM + 98 * SS, ty + 8 * SS, MARGEM + 106 * SS, ty + 16 * SS], fill=COR_ALERTA_BORDA)
        for idx_l, linha in enumerate(linhas_item):
            indent = 118 * SS if idx_l == 0 else 122 * SS
            draw.text((MARGEM + indent, ty), linha, font=fontes["texto_bold"], fill=(122, 46, 43))
            ty += 26 * SS

    y += altura_alerta + 22 * SS

    box = [MARGEM, y, W - MARGEM, y + 145 * SS]
    sombra_retangulo(img, box, 22 * SS, blur=8, opacidade=25, offset=(0, 5))
    rounded_rect(draw, box, 22 * SS, fill=(255, 255, 255, 255))
    desenhar_estrela(draw, MARGEM + 32 * SS, y + 32 * SS, 11 * SS, 5 * SS, hex_to_rgb("#E0A233"))
    draw.text((MARGEM + 52 * SS, y + 20 * SS), "Anote aqui suas dúvidas para a próxima consulta:", font=fontes["texto_bold"], fill=COR_TEXTO_SUAVE)

    for i in range(4):
        ly = y + 62 * SS + i * 24 * SS
        draw.line([(MARGEM + 28 * SS, ly), (W - MARGEM - 28 * SS, ly)], fill=(220, 212, 196), width=int(SS * 1.2))

    linhas_rodape = quebrar_texto(draw, dados["rodape"], fontes["rodape"], W - 2 * MARGEM)
    ty = H - 30 * SS - len(linhas_rodape) * 18 * SS
    for linha in linhas_rodape:
        draw.text((MARGEM, ty), linha, font=fontes["rodape"], fill=COR_TEXTO_SUAVE)
        ty += 18 * SS

    img = img.convert("RGB")
    if SS != 1:
        img = img.resize((W // SS, H // SS), Image.LANCZOS)
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer, img

# ==============================================================================
# 3. INTERFACE STREAMLIT
# ==============================================================================

st.set_page_config(page_title="Gerador de Infográficos - Hospital", layout="centered")

st.title("🎨 Gerador de Infográficos Ilustrados (PX)")
st.caption("Ferramenta de Literacia em Saúde Infantil")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    nome_paciente = st.text_input("Nome da Criança:", value="Luís")

# Mapeia dinamicamente as opções cadastradas no topo
opcoes_mapeadas = {dados["nome_select"]: chave for chave, dados in CONTEUDOS.items()}

with col2:
    opcao_selecionada = st.selectbox(
        "Selecione o Diagnóstico:",
        list(opcoes_mapeadas.keys())
    )

if st.button("🚀 Gerar Material Visual (PNG)", type="primary"):
    chave_doenca = opcoes_mapeadas[opcao_selecionada]
    dados = CONTEUDOS[chave_doenca]
    
    buffer, img_obj = gerar_imagem_panfleto(dados, nome_paciente)
    
    st.success("Infográfico gerado com sucesso!")
    
    st.image(img_obj, caption=f"Guia Ilustrado - {nome_paciente}", use_container_width=True)
    
    st.download_button(
        label="📥 Baixar Infográfico em Alta Resolução (PNG)",
        data=buffer,
        file_name=f"Guia_Ilustrado_{chave_doenca}_{nome_paciente}.png",
        mime="image/png"
    )
