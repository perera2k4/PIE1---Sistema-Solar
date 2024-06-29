import pygame
import sys

# Inicializa o pygame
pygame.init()

# Define as dimensões da tela
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen_size = (screen_width, screen_height)

# Configura a tela
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

# Carrega as imagens
imagem_inicio = pygame.image.load('apresentacao/inicio.png')  # Certifique-se de que a imagem está no mesmo diretório do script
imagem_inicio = pygame.transform.scale(imagem_inicio, screen_size)
image2 = pygame.image.load('apresentacao/venus.png')  # Segunda imagem para a outra tela
image2 = pygame.transform.scale(image2, screen_size)
imagem_creditos = pygame.image.load('apresentacao/creditos.png')  # Terceira imagem para a outra tela
imagem_creditos = pygame.transform.scale(imagem_creditos, screen_size)

# Redimensiona as imagens para preencher a tela




# Define cores
cinza_claro = (80, 80, 80)
cinza_escuro = (200, 200, 200)
text_color = (255, 255, 255)
shadow_color = (50, 50, 50)

# Define o tamanho e posição dos botões
button1_rect = pygame.Rect((screen_width - 200) // 2 + 425, (screen_height - 100) // 2 - 60 + 250, 200, 100)
button2_rect = pygame.Rect((screen_width - 200) // 2 + 425, (screen_height - 100) // 2 + 60 + 250, 200, 100)

# Define a fonte
font = pygame.font.SysFont(None, 48)

# Função para desenhar um botão arredondado
def draw_rounded_button(surface, rect, color, border_radius):
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)

# Função para desenhar a tela
def draw_screen(image, button1_color, button2_color, mostrar_botaoIniciar, mostrar_botaoCreditos):
    screen.blit(image, (0, 0))
    
    # Desenha a sombra dos botões
    if mostrar_botaoIniciar:
        shadow1_rect = button1_rect.copy()
        shadow1_rect.topleft = (button1_rect.x + 5, button1_rect.y + 5)
        draw_rounded_button(screen, shadow1_rect, shadow_color, 20)
        
        draw_rounded_button(screen, button1_rect, button1_color, 20)
        button1_text = font.render('Iniciar', True, text_color)
        button1_text_rect = button1_text.get_rect(center=button1_rect.center)
        screen.blit(button1_text, button1_text_rect)

    if mostrar_botaoCreditos:
        shadow2_rect = button2_rect.copy()
        shadow2_rect.topleft = (button2_rect.x + 5, button2_rect.y + 5)
        draw_rounded_button(screen, shadow2_rect, shadow_color, 20)
        
        draw_rounded_button(screen, button2_rect, button2_color, 20)
        button2_text = font.render('Créditos', True, text_color)
        button2_text_rect = button2_text.get_rect(center=button2_rect.center)
        screen.blit(button2_text, button2_text_rect)

    # Atualiza a tela
    pygame.display.flip()

# Variável para controlar qual tela está ativa
current_screen = 1

# Variáveis para controlar a visibilidade dos botões
mostrar_botaoIniciar = True
mostrar_botaoCreditos = True

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button1_rect.collidepoint(event.pos) and mostrar_botaoIniciar:
                    current_screen = 2 if current_screen == 1 else 1
                    mostrar_botaoIniciar = False
                    mostrar_botaoCreditos = False
                elif button2_rect.collidepoint(event.pos) and mostrar_botaoCreditos:
                    current_screen = 3 if current_screen == 1 else 1
                    mostrar_botaoIniciar = False
                    mostrar_botaoCreditos = False


    # Obtém a posição do mouse
    mouse_pos = pygame.mouse.get_pos()

    # Verifica se o mouse está sobre os botões
    button1_color = cinza_escuro if button1_rect.collidepoint(mouse_pos) and mostrar_botaoIniciar else cinza_claro
    button2_color = cinza_escuro if button2_rect.collidepoint(mouse_pos) and mostrar_botaoCreditos else cinza_claro

    # Desenha a tela atual
    if current_screen == 1:
        draw_screen(imagem_inicio, button1_color, button2_color, mostrar_botaoIniciar, mostrar_botaoCreditos)
    elif current_screen == 2:
        draw_screen(image2, button1_color, button2_color, mostrar_botaoIniciar, mostrar_botaoCreditos)
    elif current_screen == 3:
        draw_screen(imagem_creditos, button1_color, button2_color, mostrar_botaoIniciar, mostrar_botaoCreditos)

# Encerra o pygame
pygame.quit()
sys.exit()
