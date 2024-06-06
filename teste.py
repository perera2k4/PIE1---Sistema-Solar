import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Definindo algumas cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Definindo o tamanho da janela
WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)

# Criando a janela
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Exemplo de Pygame")

# Carregando as imagens
image1 = pygame.image.load("planetas/jupiter.png")
image2 = pygame.image.load("planetas/jupiter.png")
image3 = pygame.image.load("planetas/jupiter.png")

# Redimensionando as imagens para caberem na tela
image1 = pygame.transform.scale(image1, (100, 100))
image2 = pygame.transform.scale(image2, (100, 100))
image3 = pygame.transform.scale(image3, (100, 100))

# Lista de imagens e suas posições
images = [image1, image2, image3]
positions = [(100, 100), (300, 100), (500, 100)]

# Lista de imagens em tamanho grande
large_images = [pygame.transform.scale(image, (300, 300)) for image in images]

# Função para mostrar as imagens na tela
def show_images():
    for i in range(len(images)):
        screen.blit(images[i], positions[i])

    pygame.display.flip()

# Função para mostrar a imagem grande
def show_large_image(index):
    large_image = large_images[index]
    large_image_rect = large_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(WHITE)
        screen.blit(large_image, large_image_rect)
        pygame.display.flip()

# Loop principal
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o clique foi em uma das imagens
                for i in range(len(positions)):
                    if positions[i][0] <= event.pos[0] <= positions[i][0] + images[i].get_width() and \
                       positions[i][1] <= event.pos[1] <= positions[i][1] + images[i].get_height():
                        show_large_image(i)

        # Movimenta as imagens
        for i in range(len(positions)):
            positions[i] = (positions[i][0] + 1, positions[i][1])
            if positions[i][0] > WIDTH:
                positions[i] = (0, positions[i][1])

        # Atualiza a tela
        screen.fill(WHITE)
        show_images()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
