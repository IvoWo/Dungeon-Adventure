import pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 200

# Slider dimensions
SLIDER_WIDTH = 200
SLIDER_HEIGHT = 20
HANDLE_RADIUS = 15

# Initialize Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Slider Demo")

# Slider variables
slider_pos = SLIDER_WIDTH // 2  # Initial position
dragging = False  # Variable to track if dragging is in progress

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if slider_pos - HANDLE_RADIUS <= mouse_pos[0] <= slider_pos + HANDLE_RADIUS:
                    # Slider handle is clicked, start dragging
                    dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False

    if dragging:
        # Update slider position based on mouse x-coordinate
        mouse_x = pygame.mouse.get_pos()[0]
        slider_pos = max(HANDLE_RADIUS, min(SLIDER_WIDTH - HANDLE_RADIUS, mouse_x))

    # Clear the screen
    screen.fill(BLACK)

    # Draw the slider track
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT // 2 - SLIDER_HEIGHT // 2, SLIDER_WIDTH, SLIDER_HEIGHT))

    # Draw the slider handle
    pygame.draw.circle(screen, BLUE, (slider_pos, SCREEN_HEIGHT // 2), HANDLE_RADIUS)

    # Update the display
    pygame.display.flip()

pygame.quit()