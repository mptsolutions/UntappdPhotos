import os
from config import logger, SCREEN_WIDTH, SCREEN_HEIGHT, MEDIA_DIR, BACKGROUND_COLOR, DISPLAY_DURATION
from time import sleep

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from pygame import (
    FULLSCREEN, DOUBLEBUF, NOFRAME, HWSURFACE, QUIT, KEYDOWN, K_ESCAPE, 
    image, time, display, event, mouse, init, quit, error
)

def init_pygame():
    init()
    mouse.set_visible(False)
    display.init()
    screen = display.set_mode((720, 720), FULLSCREEN | DOUBLEBUF | NOFRAME | HWSURFACE)
    screen.fill(BACKGROUND_COLOR)
    display.update()
    return screen

def load_images_from_directory(directory=MEDIA_DIR):
    images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            try:
                cur_image = image.load(os.path.join(directory, filename)).convert()
                cur_image_rect = cur_image.get_rect()
                cur_image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            except error as e:
                logger.error(f"ERROR LOADING IMAGE {filename}: {e}")
            images.append((cur_image, cur_image_rect, filename))
    return images

def display_image(screen, images, image_index):
    cur_image, cur_image_rect, filename = images[image_index]
    screen.blit(cur_image, cur_image_rect)
    display.update()
    logger.debug(f"SET IMAGE {image_index}: {filename}")

def main():
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
    image_time = time.get_ticks()

    while running:
        for cur_event in event.get():
            if cur_event.type == QUIT or cur_event.type == KEYDOWN and cur_event.key == K_ESCAPE:
                running = False

        now = time.get_ticks()
        if now - image_time >= DISPLAY_DURATION:
            current_image_index = current_image_index + 1
            if current_image_index >= len(images):
                current_image_index = 0
            display_image(screen, images, current_image_index)
            image_time = now

        sleep(0.1)
    quit()

if __name__ == "__main__":
    main()
