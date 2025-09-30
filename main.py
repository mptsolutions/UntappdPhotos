import os
import threading
from config import logger, SCREEN_WIDTH, SCREEN_HEIGHT, MEDIA_DIR, PHOTOS_DIR, BACKGROUND_COLOR, DISPLAY_DURATION
from time import sleep
from nicegui import ui, app
from nicegui.events import UploadEventArguments

# Hide the default pygame support prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from pygame import (
    FULLSCREEN, DOUBLEBUF, NOFRAME, HWSURFACE, QUIT, KEYDOWN, K_ESCAPE, 
    image, time, display, event, mouse, init, quit, error, transform
)

slideshow_running = False
slideshow_thread = None
stop_event = threading.Event()

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
    
    logo = image.load(os.path.join(MEDIA_DIR, "logo.jpg")).convert()
    logo_rect = logo.get_rect()
    logo_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.blit(logo, logo_rect)
    display.update()

    logger.debug("INITIALIZED PYGAME AND SCREEN")
    return screen

def load_images_from_directory(directory=PHOTOS_DIR):
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
                cur_image = transform.scale(cur_image, (720, 720))
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

    Args:
        screen (pygame.Surface): The main display surface.
        images (list): List of loaded images.
        current_image_index (int): Index of the currently displayed image.
        next_image_index (int): Index of the next image to display.
        duration (int): Duration of the fade effect in milliseconds.
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

def slide_show(screen):
    """
    Main loop for the Untappd Photos display application.
    Initializes pygame, loads images, and cycles through them at intervals.

    Args:
        screen (pygame.Surface): The main display surface.
    """

    logger.info("STARTING PHOTO DISPLAY")
    
    # Load images from the media directory
    images = load_images_from_directory()
    if not images:
        logger.error("NO IMAGES FOUND")
        return

    # Set the first image
    current_image_index = 0
    display_image(screen, images, current_image_index)

    running = True
    image_time = time.get_ticks()  # Track time for image switching

    logger.info("STARTING MAIN LOOP")
    stop_event.clear()  # Clear stop signal before starting
    while running and not stop_event.is_set():
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
    
    logo = image.load(os.path.join(MEDIA_DIR, "logo.jpg")).convert()
    logo_rect = logo.get_rect()
    logo_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.blit(logo, logo_rect)
    display.update()
    logger.info("STOPPED SLIDESHOW LOOP")

def toggle_slideshow(screen):
    """
    Function to start/stop the slideshow.

    Args:
        screen (pygame.Surface): The main display surface.
    """
    global slideshow_thread, slideshow_running
    if not slideshow_running:
        if slideshow_thread is None or not slideshow_thread.is_alive():
            slideshow_thread = threading.Thread(target=slide_show, args=(screen,), daemon=True)
            slideshow_thread.start()
            slideshow_running = True
            ui.notify("Slideshow started.")
        toggle_button.text = "Stop Slideshow"
    else:
        stop_event.set()
        slideshow_thread = None
        slideshow_running = False
        ui.notify("Slideshow stopped.")
        toggle_button.text = "Start Slideshow"

def reboot_click():
    """
    Function to reboot the system.
    Not yet implemented
    """
    ui.notify("Rebooting now...")

def quit_system():
    """
    Function to quit the application.
    Not yet implemented
    """
    ui.notify("Quitting now...")
    app.shutdown()

def get_image_thumbnails():
    """
    Returns a list of NiceGUI image elements for all images in PHOTOS_DIR.
    """
    thumbnails = []
    for filename in os.listdir(PHOTOS_DIR):
        if filename.lower().endswith('.jpg'):
            img_path = os.path.join(PHOTOS_DIR, filename)
            img = ui.image(img_path).classes('w-32 h-32 object-cover m-2 cursor-pointer')
            img.on('click', lambda e, fn=filename: handle_thumbnail_click(fn))
    return thumbnails

def refresh_thumbnails():
    """
    Refresh the thumbnails displayed in the UI.
    """
    global thumb_row
    if thumb_row:
        thumb_row.clear()
        with thumb_row:
            for thumb in get_image_thumbnails():
                thumb.classes('hover:scale-105 transition-transform duration-200')

def handle_upload(e: UploadEventArguments):
    """
    Handle file upload, save the file to PHOTOS_DIR, and refresh thumbnails.
    Args:
        e (UploadEventArguments): The upload event arguments.
    """
    b = e.content.read()
    with open(os.path.join(PHOTOS_DIR, e.name), "wb") as file:
        file.write(b)
    refresh_thumbnails()

async def handle_thumbnail_click(filename):
    """
    Handle click on a thumbnail image, prompt for deletion confirmation.
    Args:
        filename (str): The filename of the clicked image.
    """
    with ui.dialog() as dialog, ui.card():
        ui.label('Delete image?')
        with ui.row():
            ui.button('Yes', on_click=lambda: dialog.submit(True))
            ui.button('No', on_click=lambda: dialog.submit(False))

    result = await dialog
    if result is True:
        ui.notify('Action confirmed!')
        os.remove(os.path.join(PHOTOS_DIR, filename))
        refresh_thumbnails()

if __name__ in {"__main__", "__mp_main__"}:
    logger.info("STARTING NICEGUI")
    screen = init_pygame()
    
    # Build the NiceGUI interface
    title_style = "w-full bg-blue-500 p-1 text-center shadow-lg rounded-lg text-white text-2xl italic font-extrabold;"
    ui.add_head_html('<style type="text/tailwindcss"> @layer components { .title-box { @apply ' + title_style + '} } </style>')
    ui.label('Untappd Photos: Control Panel').classes('title-box mb-4')
    with ui.row().classes('w-full h-screen flex-row flex-nowrap items-start'):
        with ui.column().classes('w-1/5 h-screen items-start p-4'):
            ui.label('Controls').classes('text-xl font-bold mb-2')
            toggle_button = ui.button("Start Slideshow", on_click=lambda: toggle_slideshow(screen)).classes('mb-2 w-full')
            ui.button("Quit", on_click=quit_system).classes('mb-2 w-full')
            ui.button("Reboot System", on_click=reboot_click).classes('mb-2 w-full')
            with ui.dialog().props('full-width') as dialog:
                with ui.card():
                    content = ui.image().classes('w-full h-auto')
            ui.upload(on_upload=handle_upload).props('accept=.jpg').classes('max-w-full')
        with ui.column().classes('w-4/5 h-screen p-4'):
            ui.label('Loaded Images').classes('text-xl font-bold mb-2')
            global thumb_row 
            thumb_row = ui.row().classes('flex-wrap')
            with thumb_row:
                for thumb in get_image_thumbnails():
                    thumb.classes('hover:scale-105 transition-transform duration-200')
    
    # Start the slideshow by default
    toggle_slideshow(screen)

    # Start the NiceGUI UI
    ui.page_title('Untappd Photos: Control Panel')
    ui.run(native=False, show=False, dark=True)
