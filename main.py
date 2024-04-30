import pygame
import sys
import math
import pygame_gui

pygame.init()

# Definições de cores
fundo = (0, 0, 0)
linha_branca = (255, 255, 255)

# Configurações da tela
altura_tela, largura_tela = 1280, 720                           # Altura e largura do display no monitor
screen = pygame.display.set_mode((altura_tela, largura_tela))   # Seta o os valores de altura e largura com base nas informações acima
pygame.display.set_icon(pygame.image.load("planetas/sol.png"))  # Icone do usuário
pygame.display.set_caption("Sistema Solar")                     # Seta o nome da aplicação
fps_visor = pygame.time.Clock()                                 # Seta a velocidade dos planetas com base no FPS da aplicação

class Planeta:
    #Código orientado a objetos para setar informações para printar o planeta
    def __init__(self, name, diretorio_imagem, raio_planeta, distancia_planetas, velocidade_planeta):
        self.name = name
        self.image = pygame.image.load(diretorio_imagem)
        self.image = pygame.transform.scale(self.image, (2 * raio_planeta, 2 * raio_planeta)) 
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
        screen.blit(self.image, (posicao_planetas[0] - self.raio_planeta, posicao_planetas[1] - self.raio_planeta))

# Desenhar as órbitas dos planetas
def desenhar_orbitas(planeta, posicao_sol):                                                 # A função se resume a pegar um angulo de -1º e adicionar no array pontos_orbita
    pontos_orbita = []                                                                      # os valores para plotar no pygame.
    for angulo in range(-1, 360):
        x = posicao_sol[0] + planeta.distancia_planetas * math.cos(math.radians(angulo))
        y = posicao_sol[1] + planeta.distancia_planetas * math.sin(math.radians(angulo))
        pontos_orbita.append((int(x), int(y)))
    pygame.draw.lines(screen, linha_branca, False, pontos_orbita, 1)

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

    # Função principal do pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.process_events(event)

        screen.fill(fundo)

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

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()