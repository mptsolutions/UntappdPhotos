import os
from config import logger, SCREEN_WIDTH, SCREEN_HEIGHT, MEDIA_DIR, BACKGROUND_COLOR, DISPLAY_DURATION
from time import sleep

# Hide the default pygame support prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from pygame import (
    FULLSCREEN, DOUBLEBUF, NOFRAME, HWSURFACE, QUIT, KEYDOWN, K_ESCAPE, 
    image, time, display, event, mouse, init, quit, error
)

def init_pygame():
    """
    Initialize pygame, set up the display window, and hide the mouse cursor.

    Returns:
        screen (pygame.Surface): The main display surface.
    """
    init()
    mouse.set_visible(False)
    display.init()
    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN | DOUBLEBUF | NOFRAME | HWSURFACE)
    screen.fill(BACKGROUND_COLOR)
    display.update()
    logger.debug("INITIALIZED PYGAME AND SCREEN")
    return screen

def load_images_from_directory(directory=MEDIA_DIR):
    """
    Load all .jpg images from the specified directory, center them on the screen.

    Args:
        directory (str): Path to the directory containing images.

    Returns:
        images (list): List of tuples (image_surface, image_rect, filename).
    """
    images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            try:
                cur_image = image.load(os.path.join(directory, filename)).convert()
                cur_image_rect = cur_image.get_rect()
                cur_image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                logger.debug(f"LOADED IMAGE {filename}")
            except error as e:
                logger.error(f"ERROR LOADING IMAGE {filename}: {e}")
            images.append((cur_image, cur_image_rect, filename))
    logger.info(f"LOADED {len(images)} IMAGES FROM {directory}")
    return images

def display_image(screen, images, image_index):
    """
    Display the image at the given index on the screen.

    Args:
        screen (pygame.Surface): The main display surface.
        images (list): List of loaded images.
        image_index (int): Index of the image to display.
    """
    cur_image, cur_image_rect, filename = images[image_index]
    screen.blit(cur_image, cur_image_rect)
    display.update()
    logger.debug(f"SET IMAGE {image_index}: {filename}")

def fade_transition(screen, images, current_image_index, next_image_index, duration=1000):
    """
    Fade from current to next image over the given duration (milliseconds).
    """
    current_image = images[current_image_index]
    next_image = images[next_image_index]

    clock = time.Clock()
    start_time = time.get_ticks()
    alpha_surface = current_image[0].copy()
    for alpha in range(255, -1, -10):
        screen.blit(current_image[0], current_image[1])
        alpha_surface = next_image[0].copy()
        alpha_surface.set_alpha(255 - alpha)
        screen.blit(alpha_surface, next_image[1])
        display.update()
        clock.tick(60)
        if time.get_ticks() - start_time > duration:
            break
    logger.debug(f"SET IMAGE {next_image_index}: {next_image[2]}")

def main():
    """
    Main loop for the Untappd Photos display application.
    Initializes pygame, loads images, and cycles through them at intervals.
    """

    # Initialize Pygame and get a screen object
    screen = init_pygame()

    # Load images from the media directory
    images = load_images_from_directory()
    if not images:
        logger.error("No images found in the media directory.")
        quit()

    # Set the first image
    current_image_index = 0
    display_image(screen, images, current_image_index)

    running = True
    image_time = time.get_ticks()  # Track time for image switching

    logger.info("STARTING MAIN LOOP")
    while running:
        # Handle quit and escape key events
        for cur_event in event.get():
            if cur_event.type == QUIT or cur_event.type == KEYDOWN and cur_event.key == K_ESCAPE:
                logger.info("QUIT EVENT DETECTED")
                running = False

        # Check if it's time to switch to the next image
        now = time.get_ticks()
        if now - image_time >= DISPLAY_DURATION:
            next_image_index = current_image_index + 1
            if next_image_index >= len(images):
                next_image_index = 0
            fade_transition(screen, images, current_image_index, next_image_index)
            image_time = now
            current_image_index = next_image_index

        sleep(0.1)  # Small delay to reduce CPU usage
    quit()
    logger.info("STOPPED MAIN LOOP")

if __name__ == "__main__":
    main()
