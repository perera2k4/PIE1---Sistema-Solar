import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Definindo as dimensões da janela
altura = 800
largura = 600

# Configurando a tela
screen = pygame.display.set_mode((altura, largura))
pygame.display.set_caption('Botão de Saída Estilizado')

# Definindo as cores
preto = (0 ,0 ,0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
vermelho_escuro = (200, 0, 0)

# Função para desenhar um retângulo com cantos arvermelhoondados
def desenhar_quadrado(surface, rect, color, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

# Função para desenhar o botão
def desenhar_botao(screen, x, y, width, height, bg_color, text, text_color):
    desenhar_quadrado(screen, (x, y, width, height), bg_color, 10)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Coordenadas e dimensões do botão
botao_x = 10
botao_y = 10
altura_botao = 50
largura_botao = 30

# Loop principal
running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_hover = botao_x <= mouse_x <= botao_x + altura_botao and botao_y <= mouse_y <= botao_y + largura_botao

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Verificando se o botão foi clicado
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_hover:
            running = False

    # Preenchendo a tela com branco
    screen.fill(preto)

    # Desenhando o botão com cores invertidas se o mouse estiver sobre ele
    if mouse_hover:
        button_color = branco
        text_color = vermelho
    else:
        button_color = vermelho
        text_color = branco
        
    desenhar_botao(screen, botao_x, botao_y, altura_botao, largura_botao, button_color, 'x', text_color)

    # Atualizando a tela
    pygame.display.flip()

# Finalizando o Pygame
pygame.quit()
sys.exit()
