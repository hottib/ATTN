import pygame

# initialize pygame
pygame.init()

# set the size of the window
window_size = (400, 400)

# create the window surface
window = pygame.display.set_mode(window_size)

# set the initial position of the point
point_pos = (window_size[0] // 2, window_size[1] // 2)

# set the color of the point
point_color = (255, 255, 255)

# set the radius of the point
point_radius = 5

# main game loop
while True:

    # handle events
    for event in pygame.event.get():

        # if the user closes the window, exit the program
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # if the user moves the mouse, update the point position
        elif event.type == pygame.MOUSEMOTION:
            point_pos = event.pos

    # clear the window
    window.fill((0, 0, 0))

    # draw the point
    pygame.draw.circle(window, point_color, point_pos, point_radius)

    # update the display
    pygame.display.update()

    # print mouse position
    print(point_pos)
    
