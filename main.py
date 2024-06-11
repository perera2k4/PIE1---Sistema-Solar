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
altura_tela, largura_tela = info_Tela.current_w, info_Tela.current_h    # Altura e largura do display no monitor
screen = pygame.display.set_mode((altura_tela, largura_tela))           # Seta o os valores de altura e largura com base nas informações acima
pygame.display.set_icon(pygame.image.load("planetas/sol.png"))          # Icone do usuário
pygame.display.set_caption("Sistema Solar")                             # Seta o nome da aplicação
fps_visor = pygame.time.Clock()                                         # Seta a velocidade dos planetas com base no FPS da aplicação

# Definindo a fonte
fonte = pygame.font.SysFont(None, 30)

# Lista do Sol e dos planetas
sistema_solar = ["Sol", "Mercúrio", "Vênus", "Terra", "Marte", "Júpiter", "Saturno", "Urano", "Netuno"]

# Dicionário de caminhos para as imagens dos planetas
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

# Carregar imagens dos planetas
carregar_imagens = {}
for planet, image_path in lista_planetas.items():
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (50, 50))  # Redimensionar a imagem para 50x50 pixels
    carregar_imagens[planet] = image

def plotar_texto(text, fonte, color, tela, x, y):
    textobj = fonte.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    tela.blit(textobj, textrect)

def plotar_quadrado(tela, color, rect, canto_arredondado):
    pygame.draw.rect(tela, color, rect, border_radius=canto_arredondado)

# Função para criar botões
def criar_botao(tela, text, x, y, w, h, cor_inativa, cor_ativa, canto_arredondado):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        plotar_quadrado(tela, cor_ativa, (x, y, w, h), canto_arredondado)
        
        if clique[0] == 1:
            print(f"O usuário clicou em: {text}")
    else:
        plotar_quadrado(tela, cor_inativa, (x, y, w, h), canto_arredondado)

    imagem = carregar_imagens.get(text)
    if imagem:
        tela.blit(imagem, (x + 10, y + (h - imagem.get_height()) // 2))
        plotar_texto(text, fonte, branco, tela, x + w // 2 + 30, y + h // 2)
    else:
        plotar_texto(text, fonte, preto, tela, x + w // 2, y + h // 2)

class Planeta:
    #Código orientado a objetos para setar informações para printar o planeta
    def __init__(self, name, diretorio_imagem, raio_planeta, distancia_planetas, velocidade_planeta):
        self.name = name
        self.imagem = pygame.image.load(diretorio_imagem)
        self.imagem = pygame.transform.scale(self.imagem, (2 * raio_planeta, 2 * raio_planeta)) 
        self.raio_planeta = raio_planeta
        self.distancia_planetas = distancia_planetas
        self.angulo = 0
        self.velocidade_planeta = velocidade_planeta

    # Cria o ângulo de 360º em volta do sol para formas os circulos
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
def desenhar_orbitas(planeta, posicao_sol):                                                 # A função se resume a pegar um angulo de -1º e adicionar no array pontos_orbita
    pontos_orbita = []                                                                      # os valores para plotar no pygame.
    for angulo in range(-1, 360):
        x = posicao_sol[0] + planeta.distancia_planetas * math.cos(math.radians(angulo))
        y = posicao_sol[1] + planeta.distancia_planetas * math.sin(math.radians(angulo))
        pontos_orbita.append((int(x), int(y)))
    pygame.draw.lines(screen, branco, False, pontos_orbita, 1)

# Função principal
def main():
    # Configurações do Sol
    posicao_sol = (altura_tela // 2, largura_tela // 2)                                                 # Posição da estrela (sol)
    imagem_sol = pygame.image.load("planetas/sol.png")                                                  # Carrega a imagem do sol
    circunferencia_sol = 40                                                                             # Define o raio do sol
    imagem_sol = pygame.transform.scale(imagem_sol, (2 * circunferencia_sol, 2 * circunferencia_sol))   # Redimensiona a imagem do sol para o dobro do raio

    # Array de planetas Planeta(["nome","diretório","raio","distancia","velocidade"]
    planetas = [
        Planeta("Mercurio", "planetas/mercurio.png", 8, 80, 1.607),
        Planeta("Venus", "planetas/venus.png", 12, 120, 1.174),
        Planeta("Terra", "planetas/terra.png", 14, 160, 1.0),
        Planeta("Marte", "planetas/marte.png", 10, 200, 0.802),
        Planeta("Jupiter", "planetas/jupiter.png", 25, 280, 0.434),
        Planeta("Saturno", "planetas/saturno.png", 22, 360, 0.323),
        Planeta("Urano", "planetas/urano.png", 18, 440, 0.228),
        Planeta("Netuno", "planetas/netuno.png", 16, 520, 0.182)
    ]

    # Barra da mudança de velocidade
    manager = pygame_gui.UIManager((altura_tela, largura_tela))
    alterar_fps = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((1050, 20), (200, 20)), start_value=30, value_range=(15, 240), manager=manager)

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

    # Função principal do pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.process_events(event)

        screen.fill(preto)
    
        # Exibir botões para o Sol e os planetas
        button_width = int(altura_tela * 0.125)
        button_height = int(largura_tela * 0.05)
        margin = int(largura_tela * 0.02)
        canto_arredondado = 10

        for index, body in enumerate(sistema_solar):
            y_position = 100 + index * (button_height + margin)
            criar_botao(screen, body, 20, y_position, button_width, button_height, cinza_claro, cinza_escuro, canto_arredondado)
    

        # Desenha a imagem do sol
        screen.blit(imagem_sol, (posicao_sol[0] - circunferencia_sol, posicao_sol[1] - circunferencia_sol))

        # Desenha as órbitas tracejadas dos planetas
        for planeta in planetas:
            desenhar_orbitas(planeta, posicao_sol)

        # Desenha os planetas
        for planeta in planetas:
            planeta.plotar_imagens(screen, posicao_sol)
            planeta.atualizar_posicao()

        # Atualiza a velocidade
        manager.update(fps_visor.tick_busy_loop(int(alterar_fps.get_current_value())) / 1000.0)
        manager.draw_ui(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_hover = 10 <= mouse_x <= 10 + 50 and 10 <= mouse_y <= 10 + 30

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

        desenhar_botao_sair(screen, 10, 10, 50, 30, button_color, 'x', text_color)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()