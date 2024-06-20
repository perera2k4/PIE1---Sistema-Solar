import pygame
import pygame_gui
import sys
import math

pygame.init()

# Definições de cores
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza_claro = (80, 80, 80)
cinza_escuro = (200, 200, 200)
vermelho = (255, 0, 0)
vermelho_escuro = (200, 0, 0)

# Configurações da tela
info_Tela = pygame.display.Info()
altura_tela, largura_tela = info_Tela.current_w, info_Tela.current_h  # Altura e largura do display no monitor
screen = pygame.display.set_mode((altura_tela, largura_tela))         # Seta os valores de altura e largura com base nas informações acima
pygame.display.set_icon(pygame.image.load("planetas/sol.png"))        # Ícone do usuário
pygame.display.set_caption("Sistema Solar")                           # Seta o nome da aplicação
fps_visor = pygame.time.Clock()                                       # Seta a velocidade dos planetas com base no FPS da aplicação

# Definindo a fonte
fonte = pygame.font.SysFont(None, 30)

# Lista do Sol e dos planetas
sistema_solar = ["Sol", "Mercúrio", "Vênus", "Terra", "Marte", "Júpiter", "Saturno", "Urano", "Netuno"]
# Dicionário de caminhos para as imagens dos planetas (botões)
lista_planetas = {
    "Sol": "planetas/sol.png",
    "Mercúrio": "planetas/mercurio.png",
    "Vênus": "planetas/venus.png",
    "Terra": "planetas/terra.png",
    "Marte": "planetas/marte.png",
    "Júpiter": "planetas/jupiter.png",
    "Saturno": "planetas/saturno.png",
    "Urano": "planetas/urano.png",
    "Netuno": "planetas/netuno.png"
}

# Dicionário de caminhos para as imagens de apresentação
presentation_images = {
    "Sol": "apresentacao/sol.png",
    "Mercúrio": "apresentacao/mercurio.png",
    "Vênus": "apresentacao/venus.png",
    "Terra": "apresentacao/terra.png",
    "Marte": "apresentacao/marte.png",
    "Júpiter": "apresentacao/jupiter.png",
    "Saturno": "apresentacao/saturno.png",
    "Urano": "apresentacao/urano.png",
    "Netuno": "apresentacao/netuno.png"
}

# Carregar imagens dos planetas (botões)
loaded_images = {}
for planet, image_path in lista_planetas.items():
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (50, 50))  # Redimensionar a imagem para 50x50 pixels
    loaded_images[planet] = image

# Carregar imagens de apresentação dos planetas
loaded_presentation_images = {}
for planet, image_path in presentation_images.items():
    image = pygame.image.load(image_path)
    loaded_presentation_images[planet] = image

# Variável para armazenar o planeta selecionado
selected_planet = None

# Função para desenhar texto
def draw_text(text, font, color, tela, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    tela.blit(textobj, textrect)

# Função para desenhar retângulo com cantos arredondados
def draw_rounded_rect(tela, color, rect, corner_radius):
    pygame.draw.rect(tela, color, rect, border_radius=corner_radius)

# Função para criar botões
def criar_botao(tela, text, x, y, w, h, inactive_color, active_color, corner_radius):
    global selected_planet
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        draw_rounded_rect(tela, active_color, (x, y, w, h), corner_radius)
        if click[0] == 1:
            selected_planet = text  # Atualiza o planeta selecionado
    else:
        draw_rounded_rect(tela, inactive_color, (x, y, w, h), corner_radius)

    image = loaded_images.get(text)
    if image:
        tela.blit(image, (x + 10, y + (h - image.get_height()) // 2))
        draw_text(text, fonte, branco, tela, x + w // 2 + 30, y + h // 2)
    else:
        draw_text(text, fonte, preto, tela, x + w // 2, y + h // 2)

# Função para desenhar a imagem de apresentação e o botão de fechar
def draw_presentation(tela, planet, x, y, w, h):
    if planet:
        planet_image = loaded_presentation_images.get(planet)
        if planet_image:
            planet_image = pygame.transform.scale(planet_image, (w, h))
            tela.blit(planet_image, (x, y))

            # Botão de fechar
            close_button_rect = pygame.Rect(35, y + 5, 30, 30)
            mouse = pygame.mouse.get_pos()
            if close_button_rect.collidepoint(mouse):
                close_button_color = vermelho
                if pygame.mouse.get_pressed()[0]:  # Verifica se o botão esquerdo do mouse está pressionado
                    return True  # Indica que o botão de fechar foi clicado
            else:
                close_button_color = cinza_escuro
            pygame.draw.rect(tela, close_button_color, close_button_rect, border_radius=15)
            draw_text("x", fonte, branco, tela, 50, y + 20)

    return False  # Indica que o botão de fechar não foi clicado

class planetaSistema:
    # Código orientado a objetos para setar informações para printar o planeta
    def __init__(self, name, diretorio_imagem, raio_planeta, distancia_planetas, velocidade_planeta):
        self.name = name
        self.imagem = pygame.image.load(diretorio_imagem)
        self.imagem = pygame.transform.scale(self.imagem, (2 * raio_planeta, 2 * raio_planeta)) 
        self.raio_planeta = raio_planeta
        self.distancia_planetas = distancia_planetas
        self.angulo = 0
        self.velocidade_planeta = velocidade_planeta

    # Cria o ângulo de 360º em volta do sol para formas os círculos
    def atualizar_posicao(self):                
        self.angulo += self.velocidade_planeta
        if self.angulo >= 360:
            self.angulo -= 360

    # Forma a rotação em 360º em volta do sol
    def posicao_planetas(self, posicao_sol):
        x = posicao_sol[0] + self.distancia_planetas * math.cos(math.radians(self.angulo))
        y = posicao_sol[1] + self.distancia_planetas * math.sin(math.radians(self.angulo))
        return int(x), int(y)

    # Desenha a imagem do planeta
    def plotar_imagens(self, screen, posicao_sol):
        posicao_planetas = self.posicao_planetas(posicao_sol)
        screen.blit(self.imagem, (posicao_planetas[0] - self.raio_planeta, posicao_planetas[1] - self.raio_planeta))

# Desenhar as órbitas dos planetas
def desenhar_orbitas(planeta, posicao_sol):
    pontos_orbita = []
    for angulo in range(-1, 360):
        x = posicao_sol[0] + planeta.distancia_planetas * math.cos(math.radians(angulo))
        y = posicao_sol[1] + planeta.distancia_planetas * math.sin(math.radians(angulo))
        pontos_orbita.append((int(x), int(y)))
    pygame.draw.lines(screen, branco, False, pontos_orbita, 1)

# Função principal
def main():
    global selected_planet

    # Configurações do Sol
    posicao_sol = (altura_tela // 2, largura_tela // 2)
    imagem_sol = pygame.image.load("planetas/sol.png")
    circunferencia_sol = 40
    imagem_sol = pygame.transform.scale(imagem_sol, (2 * circunferencia_sol, 2 * circunferencia_sol))

    # Array de planetas Planeta(["nome","diretório","raio","distancia","velocidade"]
    planetas = [
        planetaSistema("Mercurio", "planetas/mercurio.png", 8, 80, 1.607),
        planetaSistema("Venus", "planetas/venus.png", 12, 120, 1.174),
        planetaSistema("Terra", "planetas/terra.png", 12, 160, 1),
        planetaSistema("Marte", "planetas/marte.png", 10, 200, 0.802),
        planetaSistema("Jupiter", "planetas/jupiter.png", 25, 250, 0.434),
        planetaSistema("Saturno", "planetas/saturno.png", 22, 300, 0.323),
        planetaSistema("Urano", "planetas/urano.png", 18, 350, 0.228),
        planetaSistema("Netuno", "planetas/netuno.png", 18, 400, 0.182),
    ]

    # Barra da mudança de velocidade
    manager = pygame_gui.UIManager((altura_tela, largura_tela))
    alterar_fps = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((altura_tela-300, 20), (200, 20)), start_value=30, value_range=(15, 240), manager=manager)

    # Função para desenhar um retângulo com cantos arvermelhoondados
    def desenhar_quadrado_botao_sair(surface, rect, color, corner_radius):
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

    # Função para desenhar o botão
    def desenhar_botao_sair(screen, x, y, width, height, bg_color, text, text_color):
        desenhar_quadrado_botao_sair(screen, (x, y, width, height), bg_color, 10)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)


    running = True
    while running:
        time_delta = fps_visor.tick(60) / 1000.0  # Atualiza o relógio com base no FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if draw_presentation(screen, selected_planet, 0, 0, altura_tela, largura_tela):
                    selected_planet = None  # Desseleciona o planeta
            

            manager.process_events(event)

        # Atualiza a tela
        screen.fill(preto)

        # Desenha as órbitas e os planetas
        screen.blit(imagem_sol, (posicao_sol[0] - circunferencia_sol, posicao_sol[1] - circunferencia_sol))
        for planeta in planetas:
            desenhar_orbitas(planeta, posicao_sol)
            planeta.atualizar_posicao()
            planeta.plotar_imagens(screen, posicao_sol)

        # Desenha os botões dos planetas
        for i, planet_name in enumerate(sistema_solar):
            criar_botao(screen, planet_name, 50, 150 + i * 60, 200, 50, cinza_claro, cinza_escuro, 10)

        # Desenha a apresentação do planeta selecionado
        draw_presentation(screen, selected_planet, 0, 0, altura_tela, largura_tela)

        # Atualiza a velocidade
        manager.update(fps_visor.tick_busy_loop(int(alterar_fps.get_current_value())) / 1000.0)
        manager.draw_ui(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_hover = altura_tela-75 <= mouse_x <= altura_tela-75 + 50 and 10 <= mouse_y <= 10 + 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Verificando se o botão foi clicado
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_hover:
                running = False

        # Desenhando o botão com cores invertidas se o mouse estiver sobre ele
        if mouse_hover:
            button_color = branco
            text_color = vermelho
        else:
            button_color = vermelho
            text_color = branco

        desenhar_botao_sair(screen, altura_tela-75, 10, 60, 35, button_color, 'Sair', text_color)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
