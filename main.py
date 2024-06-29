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
cinza_sombra = (50, 50, 50)


# Configurações da tela
info_tela = pygame.display.Info()
altura_tela, largura_tela = info_tela.current_w, info_tela.current_h  # Altura e largura do display no monitor
screen = pygame.display.set_mode((altura_tela, largura_tela))         # Seta os valores de altura e largura com base nas informações acima
pygame.display.set_icon(pygame.image.load("planetas/sol.png"))        # Ícone do usuário
pygame.display.set_caption("Sistema Solar")                           # Seta o nome da aplicação
fps_visor = pygame.time.Clock()                                       # Seta a velocidade dos planetas com base no FPS da aplicação

# Definindo fonte e imagem inicial
fonte = pygame.font.SysFont(None, 30)

# Carrega as imagens da tela inicial
imagem_inicio = pygame.image.load('apresentacao/inicio.png')  # Certifique-se de que a imagem está no mesmo diretório do script
imagem_inicio = pygame.transform.scale(imagem_inicio, (altura_tela, largura_tela))
imagem_creditos = pygame.image.load('apresentacao/creditos.png')  # Terceira imagem para a outra tela
imagem_creditos = pygame.transform.scale(imagem_creditos, (altura_tela, largura_tela))

# Define o tamanho e posição dos botões
button1_rect = pygame.Rect((altura_tela - 200) // 2 + 425, (largura_tela - 100) // 2 - 60 + 250, 200, 100)
button2_rect = pygame.Rect((altura_tela - 200) // 2 + 425, (largura_tela - 100) // 2 + 60 + 250, 200, 100)
button_back_rect = pygame.Rect(50, 20, 50, 50)


# Função para desenhar um botão arredondado
def draw_rounded_button(surface, rect, color, border_radius):
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)



# Função para desenhar a tela
def draw_screen(image, button1_color, button2_color, buttonSkip_color, mostrar_botaoIniciar, mostrar_botaoCreditos, mostrar_botaoVoltar):
    screen.blit(image, (0, 0))
    
    # Desenha a sombra dos botões
    if mostrar_botaoIniciar:
        shadow1_rect = button1_rect.copy()
        shadow1_rect.topleft = (button1_rect.x + 5, button1_rect.y + 5)
        draw_rounded_button(screen, shadow1_rect, cinza_sombra, 20)
        
        draw_rounded_button(screen, button1_rect, button1_color, 20)
        button1_text = fonte.render('Iniciar', True, branco)
        button1_text_rect = button1_text.get_rect(center=button1_rect.center)
        screen.blit(button1_text, button1_text_rect)

    if mostrar_botaoCreditos:
        shadow2_rect = button2_rect.copy()
        shadow2_rect.topleft = (button2_rect.x + 5, button2_rect.y + 5)
        draw_rounded_button(screen, shadow2_rect, cinza_sombra, 20)
        
        draw_rounded_button(screen, button2_rect, button2_color, 20)
        button2_text = fonte.render('Créditos', True, branco)
        button2_text_rect = button2_text.get_rect(center=button2_rect.center)
        screen.blit(button2_text, button2_text_rect)

    if mostrar_botaoVoltar:
        shadow_back_rect = button_back_rect.copy()
        shadow_back_rect.topleft = (button_back_rect.x + 5, button_back_rect.y + 5)
        draw_rounded_button(screen, shadow_back_rect, cinza_sombra, 20)

        draw_rounded_button(screen, button_back_rect, buttonSkip_color, 20)
        button_back_text = fonte.render('x', True, branco)
        button_back_text_rect = button_back_text.get_rect(center=button_back_rect.center)
        screen.blit(button_back_text, button_back_text_rect)

    # Atualiza a tela
    pygame.display.flip()

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

    current_screen = 1

    # Variáveis para controlar a visibilidade dos botões
    mostrar_botaoIniciar = True
    mostrar_botaoCreditos = True
    mostrar_botaoVoltar = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if draw_presentation(screen, selected_planet, 0, 0, altura_tela, largura_tela):
                    selected_planet = None  # Desseleciona o planeta
            

            manager.process_events(event)

        # Atualiza a tela
        screen.fill(preto)
        if current_screen == 1:
            
            # Obtém a posição do mouse
            mouse_pos = pygame.mouse.get_pos()

            # Verifica se o mouse está sobre os botões
            button1_color = cinza_escuro if button1_rect.collidepoint(mouse_pos) and mostrar_botaoIniciar else cinza_claro
            button2_color = cinza_escuro if button2_rect.collidepoint(mouse_pos) and mostrar_botaoCreditos else cinza_claro
            buttonSkip_color = cinza_escuro if button_back_rect.collidepoint(mouse_pos) and mostrar_botaoVoltar else vermelho

            mostrar_botaoVoltar = False
            draw_screen(imagem_inicio, button1_color, button2_color, buttonSkip_color, mostrar_botaoIniciar, mostrar_botaoCreditos, mostrar_botaoVoltar)

            

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button1_rect.collidepoint(event.pos) and mostrar_botaoIniciar:
                        current_screen = 0
                        mostrar_botaoIniciar = False
                        mostrar_botaoCreditos = False

                        
                    elif button2_rect.collidepoint(event.pos) and mostrar_botaoCreditos:
                        current_screen = 2 if current_screen == 1 else 1
                        mostrar_botaoIniciar = False
                        mostrar_botaoCreditos = False
                        
                        
        
        elif current_screen == 2:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back_rect.collidepoint(event.pos):
                    current_screen = 1
                    mostrar_botaoIniciar = True
                    mostrar_botaoCreditos = True
                    mostrar_botaoVoltar = False
                    

            
            draw_screen(imagem_creditos, button1_color, button2_color, buttonSkip_color, mostrar_botaoIniciar, mostrar_botaoCreditos, mostrar_botaoVoltar)
            pygame.display.flip()
            mostrar_botaoVoltar = True

        else:
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
