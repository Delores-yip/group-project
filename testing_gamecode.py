import pygame
import sys
import os
from pathlib import Path
from datetime import timedelta
import threading

# Audio recording and speech recognition libraries
# You'll need to install these: pip install pygame sounddevice soundfile SpeechRecognition
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

# Try to import PIL for GIF support
try:
    from PIL import Image, ImageSequence
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("⚠ PIL (Pillow) not found. Animated GIFs will be static.")
    

# ============================================================================
# CONFIGURATION - EDIT THESE FILE PATHS TO USE YOUR OWN ASSETS
# ============================================================================

# Start Screen Assets - NEW!
START_SCREEN_BACKGROUND = "temp png file/start_screen.png"  # Start screen background image
START_BUTTON_IMAGE = "temp png file/start_button.png"       # Start button image (will be clickable)

# Image Assets - Replace with your file paths
CANTEEN_BACKGROUND = "temp png file/background.png"  # e.g., "assets/canteen.png"
NPC_SPRITE = None # Deprecated, using NPC_FULL_BODY and directional GIFs instead
# NPC Directional GIFs
NPC_GIF_RIGHT = "temp png file/npc_right.gif"
NPC_GIF_LEFT = "temp png file/npc_left.gif"
NPC_GIF_UP = "temp png file/npc_up.gif"
NPC_GIF_DOWN = "temp png file/npc_down.gif"

PLAYER_SPRITE = "temp png file/player.png"       # e.g., "assets/player.png"
                    # e.g., "assets/table.png"

# Audio Assets - Replace with your file paths
DIALOGUE_AUDIO = "audio file/1.mp3"      # e.g., "assets/dialogue.mp3"
WELCOME_AUDIO = "audio file/2.mp3"       # e.g., "assets/welcome.mp3" - NPC greeting before sitting

# Tea response audio files - NPC responses for each tea type
TEA_AUDIO_TIEGUANYIN = "audio file/tea_tieguanyin.mp3"  # "Okay, one Tieguanyin"
TEA_AUDIO_XIANGPIAN = "audio file/tea_xiangpian.mp3"    # "Okay, one jasmine tea"
TEA_AUDIO_PUER = "audio file/tea_puer.mp3"              # "Okay, one Pu-erh"
TEA_AUDIO_HONGCHA = "audio file/tea_hongcha.mp3"        # "Okay, one black tea"

# NPC ordering assets
NPC_FULL_BODY = "temp png file/npc full body.png"       # NPC standing portrait for ordering
NPC_FULL_BODY_ORDERING = "temp png file/npc_full_body_ordering.png" # NPC portrait when ordering
NPC_ORDER_AUDIO = "audio file/npc_order.mp3"            # "有咩帮到你?" audio

# Dialogue Box Assets
NPC_DIALOGUE_IMAGE = "temp png file/npc_dialogue.png"
PLAYER_DIALOGUE_IMAGE = "temp png file/player_dialogue.png"

# Ordering Interface Assets
ORDER_BUTTON_IMAGE = "temp png file/order_button.png"
CHECK_BUTTON_IMAGE = "temp png file/check_button.png"
MICROPHONE_DEFAULT = "temp png file/microphone_default.png"
MICROPHONE_HOVER = "temp png file/microphone_hover.png"
MICROPHONE_RECORDING = "temp png file/microphone_recording.png"

# Bill and Checkout Assets
BILL_IMAGE = "temp png file/bill.png"
BACK_TO_HOME_IMAGE = "temp png file/back_to_home.png"

# Menu and UI Assets
MENU_ICON = "temp png file/menu.png"                     # Menu icon on table (94x136) - clickable
MENU_FULL = "temp png file/4a.png"                       # Full menu interface when opened
MENU_CLOSE_BUTTON = "temp png file/4g.png"               # Close button for menu
SHOPPING_CART = "temp png file/5a.png"                   # Shopping cart UI

# Menu category buttons (left side of menu)
MENU_BTN_STEAMED = "temp png file/4c.png"       # 经典蒸点 button
MENU_BTN_FRIED = "temp png file/4d.png"           # 香煎炸点 button
MENU_BTN_CONGEE = "temp png file/4e.png"         # 粥粉时蔬 button

# Dish images and audio - 经典蒸点 (Steamed Dim Sum)
DISH_SHRIMP_DUMPLING = {"img": "temp png file/dish_shrimp_dumpling.png", "audio": "audio file/dish_shrimp_dumpling.mp3"}  # 虾饺
DISH_SHUMAI = {"img": "temp png file/dish_shumai.png", "audio": "audio file/dish_shumai.mp3"}  # 烧卖
DISH_BBQ_PORK_BUN = {"img": "temp png file/dish_bbq_pork_bun.png", "audio": "audio file/dish_bbq_pork_bun.mp3"}  # 叉烧包
DISH_CUSTARD_BUN = {"img": "temp png file/dish_custard_bun.png", "audio": "audio file/dish_custard_bun.mp3"}  # 奶黄包
DISH_CHICKEN_FEET = {"img": "temp png file/dish_chicken_feet.png", "audio": "audio file/dish_chicken_feet.mp3"}  # 凤爪
DISH_SPARE_RIBS = {"img": "temp png file/dish_spare_ribs.png", "audio": "audio file/dish_spare_ribs.mp3"}  # 豉汁排骨
DISH_BEEF_BALLS = {"img": "temp png file/dish_beef_balls.png", "audio": "audio file/dish_beef_balls.mp3"}  # 牛肉丸
DISH_STICKY_RICE = {"img": "temp png file/dish_sticky_rice.png", "audio": "audio file/dish_sticky_rice.mp3"}  # 糯米鸡

# Dish images and audio - 香煎炸点 (Fried Dim Sum)
DISH_SPRING_ROLL = {"img": "temp png file/dish_spring_roll.png", "audio": "audio file/dish_spring_roll.mp3"}  # 春卷
DISH_DUMPLING_FRIED = {"img": "temp png file/dish_dumpling_fried.png", "audio": "audio file/dish_dumpling_fried.mp3"}  # 咸水角
DISH_TARO_CAKE = {"img": "temp png file/dish_taro_cake.png", "audio": "audio file/dish_taro_cake.mp3"}  # 芋头糕
DISH_WATER_CHESTNUT = {"img": "temp png file/dish_water_chestnut.png", "audio": "audio file/dish_water_chestnut.mp3"}  # 马蹄糕

# Dish images and audio - 粥粉时蔬 (Congee & Noodles)
DISH_BEEF_NOODLE = {"img": "temp png file/dish_beef_noodle.png", "audio": "audio file/dish_beef_noodle.mp3"}  # 牛肉肠粉
DISH_SHRIMP_NOODLE = {"img": "temp png file/dish_shrimp_noodle.png", "audio": "audio file/dish_shrimp_noodle.mp3"}  # 鲜虾肠粉
DISH_CENTURY_EGG_CONGEE = {"img": "temp png file/dish_century_egg_congee.png", "audio": "audio file/dish_century_egg_congee.mp3"}  # 皮蛋瘦肉粥
DISH_CHINESE_KALE = {"img": "temp png file/dish_chinese_kale.png", "audio": "audio file/dish_chinese_kale.mp3"}  # 菜心

# Example with actual paths:
# CANTEEN_BACKGROUND = "C:/Users/User/Documents/images/canteen.png"
# NPC_SPRITE = "C:/Users/User/Documents/images/waiter.png"
# PLAYER_SPRITE = "C:/Users/User/Documents/images/customer.png"
# DIALOGUE_AUDIO = "C:/Users/User/Documents/audio/greeting.mp3"

# ============================================================================

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
GAME_WIDTH = 1536   # Base game resolution width
GAME_HEIGHT = 864   # Base game resolution height
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (100, 149, 237)

# Timer settings
GAME_TIME = 15  # 15 seconds for player response

# Tea keywords for recognition
TEA_KEYWORDS = {
    "tieguanyin": "tieguanyin",
    "鐵觀音": "tieguanyin",
    "铁观音": "tieguanyin",
    "jasmine": "xiangpian",
    "jasmine tea": "xiangpian",
    "香片": "xiangpian",
    "pu-erh": "puer",
    "puer": "puer",
    "普洱": "puer",
    "普利": "puer",
    "black tea": "hongcha",
    "紅茶": "hongcha",
    "红茶": "hongcha"
}

# Dish keywords for recognition (Cantonese/English to dish ID)
DISH_KEYWORDS = {
    # 经典蒸点 (Steamed)
    "虾饺": "shrimp_dumpling",
    "蝦餃": "shrimp_dumpling",
    "shrimp dumpling": "shrimp_dumpling",
    "har gow": "shrimp_dumpling",
    "烧卖": "shumai",
    "燒賣": "shumai",
    "shumai": "shumai",
    "siu mai": "shumai",
    "叉烧包": "bbq_pork_bun",
    "叉燒包": "bbq_pork_bun",
    "char siu bao": "bbq_pork_bun",
    "bbq pork bun": "bbq_pork_bun",
    "奶黄包": "custard_bun",
    "奶黃包": "custard_bun",
    "custard bun": "custard_bun",
    "凤爪": "chicken_feet",
    "鳳爪": "chicken_feet",
    "chicken feet": "chicken_feet",
    "排骨": "spare_ribs",
    "spare ribs": "spare_ribs",
    "牛肉丸": "beef_balls",
    "beef balls": "beef_balls",
    "糯米鸡": "sticky_rice",
    "糯米雞": "sticky_rice",
    "sticky rice": "sticky_rice",
    "lo mai gai": "sticky_rice",
    
    # 香煎炸点 (Fried)
    "春卷": "spring_roll",
    "春捲": "spring_roll",
    "spring roll": "spring_roll",
    "咸水角": "dumpling_fried",
    "鹹水角": "dumpling_fried",
    "ham sui gok": "dumpling_fried",
    "芋头糕": "taro_cake",
    "芋頭糕": "taro_cake",
    "taro cake": "taro_cake",
    "马蹄糕": "water_chestnut",
    "馬蹄糕": "water_chestnut",
    "water chestnut cake": "water_chestnut",
    
    # 粥粉时蔬 (Congee & Noodles)
    "牛肉肠粉": "beef_noodle",
    "牛肉腸粉": "beef_noodle",
    "beef rice noodle": "beef_noodle",
    "鲜虾肠粉": "shrimp_noodle",
    "鮮蝦腸粉": "shrimp_noodle",
    "shrimp rice noodle": "shrimp_noodle",
    "皮蛋瘦肉粥": "century_egg_congee",
    "century egg congee": "century_egg_congee",
    "菜心": "chinese_kale",
    "chinese kale": "chinese_kale",
}

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.recording = []
        self.sample_rate = 44100
        self.temp_file = "temp_recording.wav"
        
    def start_recording(self):
        self.is_recording = True
        self.recording = []
        
        def record():
            with sd.InputStream(samplerate=self.sample_rate, channels=1, callback=self.audio_callback):
                while self.is_recording:
                    sd.sleep(100)
        
        self.record_thread = threading.Thread(target=record)
        self.record_thread.start()
        
    def audio_callback(self, indata, frames, time, status):
        if self.is_recording:
            self.recording.append(indata.copy())
            
    def stop_recording(self):
        self.is_recording = False
        if hasattr(self, 'record_thread'):
            self.record_thread.join()
        
        if self.recording:
            import numpy as np
            recording_array = np.concatenate(self.recording, axis=0)
            sf.write(self.temp_file, recording_array, self.sample_rate)
            return self.temp_file
        return None
    
    def transcribe_audio(self, audio_file):
        """
        Transcribe Cantonese audio to text using Google Speech Recognition
        Note: This requires internet connection and supports Cantonese (yue-Hant-HK)
        Returns tuple: (english_display_text, original_chinese_text)
        """
        recognizer = sr.Recognizer()
        
        try:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                
            # Using Google Speech Recognition with Cantonese language code
            # Language code: yue-Hant-HK (Cantonese, Traditional Chinese, Hong Kong)
            original_text = recognizer.recognize_google(audio, language="yue-Hant-HK")
            
            print(f"[DEBUG] Original transcription: '{original_text}'")
            
            # Convert Chinese characters to English-safe representation for display
            english_text = self.convert_to_english_display(original_text)
            
            print(f"[DEBUG] English display: '{english_text}'")
            
            # Return both versions: display text and original text for keyword detection
            return (english_text, original_text)
            
        except sr.UnknownValueError:
            return ("Could not understand audio", "")
        except sr.RequestError as e:
            return (f"Service error: {e}", "")
        except Exception as e:
            return (f"Error: {e}", "")
    
    def convert_to_english_display(self, chinese_text):
        """
        Convert Chinese text to English-safe display format
        Maps common tea-related terms to English
        """
        # Common Cantonese dim sum phrases mapping
        translation_map = {
            "鐵觀音": "Tieguanyin",
            "铁观音": "Tieguanyin",
            "香片": "Jasmine tea",
            "普洱": "Pu-erh",
            "普利": "Pu-erh",
            "紅茶": "Black tea",
            "红茶": "Black tea",
        }
        
        # Try to translate common phrases
        result = chinese_text
        for chinese, english in translation_map.items():
            result = result.replace(chinese, english)
        
        # If still contains Chinese characters, provide a fallback
        # Check if any Chinese characters remain
        if any('\u4e00' <= char <= '\u9fff' for char in result):
            # Still has Chinese characters
            return f"Please try again."
        
        return result

class Game(AudioRecorder):
    def __init__(self):
        super().__init__()
        # Setup display with aspect ratio preservation
        self.game_width = GAME_WIDTH
        self.game_height = GAME_HEIGHT
        self.aspect_ratio = GAME_WIDTH / GAME_HEIGHT
        
        # Get display info for fullscreen
        display_info = pygame.display.Info()
        self.display_width = display_info.current_w
        self.display_height = display_info.current_h
        
        # Start in windowed mode with a reasonable initial size
        self.fullscreen = False
        initial_width = 1280  # Start with 1280x720 window (more comfortable size)
        initial_height = 720
        self.screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
        
        # Create game surface that maintains aspect ratio
        self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        
        pygame.display.set_caption("Cantonese Learning Game - Dim Sum Ordering")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"  # start, game, end
        
        # Timer
        self.time_remaining = GAME_TIME
        self.start_time = None
        self.timer_active = False  # Timer only starts after player sits
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.dialogue_font = pygame.font.Font(None, 32)
        self.timer_font = pygame.font.Font(None, 48)
        
        # Buttons
        self.start_button = Button(
            GAME_WIDTH // 2 - 150, GAME_HEIGHT // 2 - 50,
            300, 100, "Start Learning", GREEN, BLACK
        )
        
        # Start screen assets
        self.start_screen_bg = None
        self.start_button_image = None
        self.start_button_rect = None  # Will be set when image is loaded
        self.start_button_base_rect = None  # Base position/size for hover effect
        self.start_button_hovered = False  # Whether mouse is over button
        self.start_button_clicked = False  # Whether button is being clicked
        self.start_button_click_time = 0  # Time when button was clicked
        
        # Initialize menu assets BEFORE loading
        
        self.category_btn_images = {}      # Category button images
        self.dish_images = {}              # All dish images
        self.dish_audio_paths = {}         # All dish audio paths
        self.npc_full_body_image = None    # NPC full body standing portrait
        self.npc_full_body_original = None # NPC full body image (original size)
        self.npc_full_body_ordering = None # NPC full body image (ordering state)
        
        self.npc_dialogue_image = None     # NPC dialogue box image
        self.player_dialogue_image = None  # Player dialogue box image
        
        self.order_button_image = None     # Place Order button image
        self.check_button_image = None     # Check Out button image
        self.microphone_images = {}        # Microphone icons (default, hover, recording)
        
        self.bill_image = None             # Bill image
        self.back_to_home_image = None     # Back to home button image
        self.show_bill = False             # Flag to show bill
        self.bill_scroll_y = 0             # Scroll offset for bill
        self.bill_scroll_area = None       # Rect for bill scroll area
        self.back_to_home_rect = None      # Rect for back to home button
        
        self.npc_images = {}               # NPC directional images (static fallback)
        self.npc_frames = {}               # NPC directional frames (for animation)
        self.npc_direction = "down"        # Current NPC direction
        self.npc_frame_index = 0           # Current frame index
        self.npc_last_frame_time = 0       # Last frame update time
        self.npc_frame_duration = 100      # Duration per frame in ms
        
        # Load game images from file paths
        self.canteen_bg = None
        self.npc_image = None
        self.player_image = None
        self.table_image = None
        self.menu_icon = None         # Small menu icon on table
        self.menu_full = None         # Full menu interface
        self.close_button_image = None
        self.shopping_cart_image = None  # Shopping cart UI
        self.load_assets()
        
        # Player state
        self.player_seated = False  # Player not seated initially
        
        # Table position (bottom-right corner, moved more to bottom-right)
        self.table_rect = pygame.Rect(GAME_WIDTH - 441, GAME_HEIGHT - 376, 228, 190)
        
        # Menu state
        self.show_menu = False        # Whether menu icon appears on table
        self.menu_open = False        # Whether full menu interface is open
        self.menu_icon_rect = None    # Clickable area for menu icon on table
        self.menu_full_rect = None    # Full menu interface rect
        self.close_button_rect = None
        
        # Menu category system
        self.current_category = "steamed"  # Default category: steamed, fried, congee
        self.menu_scroll_offset = 0        # Scroll position for dish display
        self.menu_category_buttons = {}    # Rects for category buttons
        self.menu_boundary_rect = None     # Boundary area for dishes
        self.dish_display_rects = []       # Rects for each displayed dish
        
        # Shopping cart state
        self.show_shopping_cart = False  # Show shopping cart after timer ends
        self.shopping_cart_rect = None
        self.cart_items = []  # List of dish IDs in cart
        self.cart_scroll_offset = 0  # Scroll offset for cart items
        
        # NPC movement system
        self.npc_path_points = [
            (GAME_WIDTH - 550, GAME_HEIGHT - 480),  # Starting point (current NPC position)
            (GAME_WIDTH - 700, GAME_HEIGHT - 480),  # Move left
            (GAME_WIDTH - 700, GAME_HEIGHT - 150),  # Move down
            (150, GAME_HEIGHT - 150),               # Move far left
            (GAME_WIDTH - 700, GAME_HEIGHT - 150),  # Move back to right area
            (GAME_WIDTH - 700, GAME_HEIGHT - 800),               # Move up
            (GAME_WIDTH - 700, GAME_HEIGHT - 480),               # Move down
            (GAME_WIDTH - 700, GAME_HEIGHT - 480),  # Back to right area
        ]
        self.npc_current_path_index = 0
        self.npc_position = list(self.npc_path_points[0])  # Current NPC position [x, y]
        self.npc_speed = 5.0  # Pixels per frame
        self.npc_at_player = False
        self.npc_wait_time = 0
        self.npc_wait_duration = 3000  # 3 seconds in milliseconds
        self.npc_moving = False  # Only start moving after timer ends
        self.npc_clickable = False  # Whether NPC can be clicked (when near player)
        self.npc_rect = None  # NPC click detection rect
        
        # NPC ordering state
        self.ordering_mode = False  # Whether player is placing order with NPC
        self.order_recording = False  # Whether recording order
        self.order_transcribed_text = ""  # Transcribed order text
        self.place_order_button = None  # Place order button
        self.checkout_button = None  # Checkout button
        self.order_record_button = None  # Recording button for orders
        
        # Audio
        self.current_dialogue_audio = None
        self.dialogue_audio_path = DIALOGUE_AUDIO
        self.welcome_audio_path = WELCOME_AUDIO
        
        # Tea audio paths
        self.tea_audio_paths = {
            "tieguanyin": TEA_AUDIO_TIEGUANYIN,
            "xiangpian": TEA_AUDIO_XIANGPIAN,
            "puer": TEA_AUDIO_PUER,
            "hongcha": TEA_AUDIO_HONGCHA
        }
        
        # Recording
        self.recorder = AudioRecorder()
        self.record_button = Button(
            GAME_WIDTH - 380, 345,
            240, 64, "Record Answer", RED, WHITE
        )
        self.is_recording = False
        self.transcribed_text = ""
        
        # Tea selection tracking
        self.tea_selected = None
        self.waiting_for_tea_choice = False
        
        # Dialogue
        self.current_dialogue = ""
        self.dialogue_lines = []
        
    def load_assets(self):
        """Load all assets from the file paths specified at the top of the script"""
        # Load start screen background
        if START_SCREEN_BACKGROUND and os.path.exists(START_SCREEN_BACKGROUND):
            try:
                self.start_screen_bg = pygame.image.load(START_SCREEN_BACKGROUND)
                print(f"✓ Loaded start screen background: {START_SCREEN_BACKGROUND}")
            except Exception as e:
                print(f"✗ Failed to load start screen background: {e}")
        else:
            print("⚠ No start screen background specified or file not found")
        
        # Load start button image
        if START_BUTTON_IMAGE and os.path.exists(START_BUTTON_IMAGE):
            try:
                # Load the image and store it
                self.start_button_image = pygame.image.load(START_BUTTON_IMAGE)
                btn_width = self.start_button_image.get_width()
                btn_height = self.start_button_image.get_height()
                # Position at middle-left (1/4 from left, vertically centered)
                self.start_button_base_rect = pygame.Rect(
                    GAME_WIDTH // 4 - btn_width // 2,
                    GAME_HEIGHT // 2 - btn_height // 2,
                    btn_width,
                    btn_height
                )
                self.start_button_rect = self.start_button_base_rect.copy()
                print(f"✓ Loaded start button image: {START_BUTTON_IMAGE}")
            except Exception as e:
                print(f"✗ Failed to load start button image: {e}")
        else:
            print("⚠ No start button image specified or file not found")
        
        # Load canteen background
        if CANTEEN_BACKGROUND and os.path.exists(CANTEEN_BACKGROUND):
            try:
                self.canteen_bg = pygame.image.load(CANTEEN_BACKGROUND)
                print(f"✓ Loaded canteen background: {CANTEEN_BACKGROUND}")
            except Exception as e:
                print(f"✗ Failed to load canteen background: {e}")
        else:
            print("⚠ No canteen background specified or file not found")
            
        # Load NPC full body image
        if NPC_FULL_BODY and os.path.exists(NPC_FULL_BODY):
            try:
                img = pygame.image.load(NPC_FULL_BODY).convert_alpha()
                # Resize to 30% as requested
                width = int(img.get_width() * 0.3)
                height = int(img.get_height() * 0.3)
                self.npc_full_body_image = pygame.transform.smoothscale(img, (width, height))
                # Set as default NPC image
                self.npc_image = self.npc_full_body_image
                print(f"✓ Loaded NPC full body: {NPC_FULL_BODY}")
            except Exception as e:
                print(f"✗ Failed to load NPC full body: {e}")
        else:
            print("⚠ No NPC full body specified or file not found")
            
        # Load NPC sprite (Deprecated - kept for fallback if needed but not used if full body exists)
        if NPC_SPRITE and os.path.exists(NPC_SPRITE) and not self.npc_image:
            try:
                self.npc_image = pygame.image.load(NPC_SPRITE)
                print(f"✓ Loaded NPC sprite: {NPC_SPRITE}")
            except Exception as e:
                print(f"✗ Failed to load NPC sprite: {e}")

        # Load NPC directional images
        npc_directions = {
            "right": NPC_GIF_RIGHT,
            "left": NPC_GIF_LEFT,
            "up": NPC_GIF_UP,
            "down": NPC_GIF_DOWN
        }
        
        for direction, path in npc_directions.items():
            if path and os.path.exists(path):
                try:
                    # Try to load as animated GIF using PIL
                    if HAS_PIL:
                        pil_img = Image.open(path)
                        frames = []
                        for frame in ImageSequence.Iterator(pil_img):
                            frame_rgba = frame.convert("RGBA")
                            pygame_img = pygame.image.fromstring(
                                frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
                            ).convert_alpha()
                            # Resize based on direction
                            
                            scale_factor = 0.12 if direction in ["up", "down"] else 0.105
                            
                            width = int(pygame_img.get_width() * scale_factor)
                            height = int(pygame_img.get_height() * scale_factor)
                            pygame_img = pygame.transform.smoothscale(pygame_img, (width, height))
                            frames.append(pygame_img)
                        
                        self.npc_frames[direction] = frames
                        if frames:
                            self.npc_images[direction] = frames[0] # Set first frame as static fallback
                        print(f"✓ Loaded NPC {direction} GIF with {len(frames)} frames: {path}")
                    else:
                        # Fallback to static load
                        img = pygame.image.load(path).convert_alpha()
                        
                        scale_factor = 0.12 if direction in ["up", "down"] else 0.105
                        
                        width = int(img.get_width() * scale_factor)
                        height = int(img.get_height() * scale_factor)
                        img = pygame.transform.smoothscale(img, (width, height))
                        self.npc_images[direction] = img
                        print(f"✓ Loaded NPC {direction} image (static): {path}")
                except Exception as e:
                    print(f"✗ Failed to load NPC {direction} image: {e}")
            
        # Load player sprite
        if PLAYER_SPRITE and os.path.exists(PLAYER_SPRITE):
            try:
                self.player_image = pygame.image.load(PLAYER_SPRITE)
                print(f"✓ Loaded player sprite: {PLAYER_SPRITE}")
            except Exception as e:
                print(f"✗ Failed to load player sprite: {e}")
        else:
            print("⚠ No player sprite specified or file not found")
            
        
        # Load menu icon (small icon on table)
        if MENU_ICON and os.path.exists(MENU_ICON):
            try:
                self.menu_icon = pygame.image.load(MENU_ICON)
                print(f"✓ Loaded menu icon: {MENU_ICON}")
            except Exception as e:
                print(f"✗ Failed to load menu icon: {e}")
        else:
            print("⚠ No menu icon specified or file not found")
        
        # Load full menu interface
        if MENU_FULL and os.path.exists(MENU_FULL):
            try:
                self.menu_full = pygame.image.load(MENU_FULL)
                print(f"✓ Loaded full menu: {MENU_FULL}")
            except Exception as e:
                print(f"✗ Failed to load full menu: {e}")
        else:
            print("⚠ No full menu specified or file not found")
        
        # Load close button
        if MENU_CLOSE_BUTTON and os.path.exists(MENU_CLOSE_BUTTON):
            try:
                self.close_button_image = pygame.image.load(MENU_CLOSE_BUTTON)
                print(f"✓ Loaded close button: {MENU_CLOSE_BUTTON}")
            except Exception as e:
                print(f"✗ Failed to load close button: {e}")
        else:
            print("⚠ No close button specified or file not found")
        
        # Load shopping cart
        if SHOPPING_CART and os.path.exists(SHOPPING_CART):
            try:
                self.shopping_cart_image = pygame.image.load(SHOPPING_CART)
                print(f"✓ Loaded shopping cart: {SHOPPING_CART}")
            except Exception as e:
                print(f"✗ Failed to load shopping cart: {e}")
        else:
            print("⚠ No shopping cart specified or file not found")
        
        
        
        # Load NPC full body image
        if NPC_FULL_BODY and os.path.exists(NPC_FULL_BODY):
            try:
                img = pygame.image.load(NPC_FULL_BODY).convert_alpha()
                
                # Store original for ordering interface
                self.npc_full_body_original = img
                
                # Resize to 30% for game screen (waiting at player)
                width = int(img.get_width() * 0.3)
                height = int(img.get_height() * 0.3)
                self.npc_full_body_image = pygame.transform.smoothscale(img, (width, height))
                
                # Set as default NPC image if not already set
                if not self.npc_image:
                     self.npc_image = self.npc_full_body_image
                print(f"✓ Loaded NPC full body: {NPC_FULL_BODY}")
            except Exception as e:
                print(f"✗ Failed to load NPC full body: {e}")
        else:
            print("⚠ No NPC full body specified or file not found")
            
        # Load dialogue box images
        if NPC_DIALOGUE_IMAGE and os.path.exists(NPC_DIALOGUE_IMAGE):
            try:
                self.npc_dialogue_image = pygame.image.load(NPC_DIALOGUE_IMAGE).convert_alpha()
                print(f"✓ Loaded NPC dialogue image: {NPC_DIALOGUE_IMAGE}")
            except Exception as e:
                print(f"✗ Failed to load NPC dialogue image: {e}")
        
        if PLAYER_DIALOGUE_IMAGE and os.path.exists(PLAYER_DIALOGUE_IMAGE):
            try:
                self.player_dialogue_image = pygame.image.load(PLAYER_DIALOGUE_IMAGE).convert_alpha()
                print(f"✓ Loaded player dialogue image: {PLAYER_DIALOGUE_IMAGE}")
            except Exception as e:
                print(f"✗ Failed to load player dialogue image: {e}")
        
        # Load ordering interface buttons
        if ORDER_BUTTON_IMAGE and os.path.exists(ORDER_BUTTON_IMAGE):
            try:
                self.order_button_image = pygame.image.load(ORDER_BUTTON_IMAGE).convert_alpha()
                print(f"✓ Loaded order button image: {ORDER_BUTTON_IMAGE}")
            except Exception as e:
                print(f"✗ Failed to load order button image: {e}")
                
        if CHECK_BUTTON_IMAGE and os.path.exists(CHECK_BUTTON_IMAGE):
            try:
                self.check_button_image = pygame.image.load(CHECK_BUTTON_IMAGE).convert_alpha()
                print(f"✓ Loaded check button image: {CHECK_BUTTON_IMAGE}")
            except Exception as e:
                print(f"✗ Failed to load check button image: {e}")
                
        # Load microphone icons
        mic_assets = {
            "default": MICROPHONE_DEFAULT,
            "hover": MICROPHONE_HOVER,
            "recording": MICROPHONE_RECORDING
        }
        
        for state, path in mic_assets.items():
            if path and os.path.exists(path):
                try:
                    self.microphone_images[state] = pygame.image.load(path).convert_alpha()
                    print(f"✓ Loaded microphone {state} icon: {path}")
                except Exception as e:
                    print(f"✗ Failed to load microphone {state} icon: {e}")
        
        # Load category buttons
        category_buttons = {
            "steamed": MENU_BTN_STEAMED,
            "fried": MENU_BTN_FRIED,
            "congee": MENU_BTN_CONGEE
        }
        
        for category, path in category_buttons.items():
            if path and os.path.exists(path):
                try:
                    self.category_btn_images[category] = pygame.image.load(path)
                    print(f"✓ Loaded {category} button: {path}")
                except Exception as e:
                    print(f"✗ Failed to load {category} button: {e}")
            else:
                print(f"⚠ No {category} button specified or file not found")
        
        # Load all dish images and audio paths
        dishes = {
            # 经典蒸点
            "shrimp_dumpling": {"data": DISH_SHRIMP_DUMPLING, "price": 28},
            "shumai": {"data": DISH_SHUMAI, "price": 20},
            "bbq_pork_bun": {"data": DISH_BBQ_PORK_BUN, "price": 20},
            "custard_bun": {"data": DISH_CUSTARD_BUN, "price": 20},
            "chicken_feet": {"data": DISH_CHICKEN_FEET, "price": 28},
            "spare_ribs": {"data": DISH_SPARE_RIBS, "price": 28},
            "beef_balls": {"data": DISH_BEEF_BALLS, "price": 20},
            "sticky_rice": {"data": DISH_STICKY_RICE, "price": 28},
            # 香煎炸点
            "spring_roll": {"data": DISH_SPRING_ROLL, "price": 16},
            "dumpling_fried": {"data": DISH_DUMPLING_FRIED, "price": 20},
            "taro_cake": {"data": DISH_TARO_CAKE, "price": 18},
            "water_chestnut": {"data": DISH_WATER_CHESTNUT, "price": 16},
            # 粥粉时蔬
            "beef_noodle": {"data": DISH_BEEF_NOODLE, "price": 36},
            "shrimp_noodle": {"data": DISH_SHRIMP_NOODLE, "price": 36},
            "century_egg_congee": {"data": DISH_CENTURY_EGG_CONGEE, "price": 32},
            "chinese_kale": {"data": DISH_CHINESE_KALE, "price": 20}
        }
        
        self.dish_prices = {} # Store prices
        
        for dish_id, info in dishes.items():
            dish_data = info["data"]
            price = info["price"]
            self.dish_prices[dish_id] = price
            
            img_path = dish_data["img"]
            audio_path = dish_data["audio"]
            
            # Load image
            if img_path and os.path.exists(img_path):
                try:
                    self.dish_images[dish_id] = pygame.image.load(img_path)
                    print(f"✓ Loaded dish image: {dish_id}")
                except Exception as e:
                    print(f"✗ Failed to load dish image {dish_id}: {e}")
            
            # Store audio path
            if audio_path and os.path.exists(audio_path):
                self.dish_audio_paths[dish_id] = audio_path
                print(f"✓ Found audio for: {dish_id}")
            else:
                print(f"⚠ No audio found for: {dish_id}")
                
        # Load NPC ordering full body
        if NPC_FULL_BODY_ORDERING and os.path.exists(NPC_FULL_BODY_ORDERING):
            try:
                self.npc_full_body_ordering = pygame.image.load(NPC_FULL_BODY_ORDERING).convert_alpha()
                print(f"✓ Loaded NPC ordering full body: {NPC_FULL_BODY_ORDERING}")
            except Exception as e:
                print(f"✗ Failed to load NPC ordering full body: {e}")
                
        # Load Bill and Back to Home
        if BILL_IMAGE and os.path.exists(BILL_IMAGE):
            try:
                self.bill_image = pygame.image.load(BILL_IMAGE).convert_alpha()
                print(f"✓ Loaded bill image: {BILL_IMAGE}")
            except Exception as e:
                print(f"✗ Failed to load bill image: {e}")
                
        if BACK_TO_HOME_IMAGE and os.path.exists(BACK_TO_HOME_IMAGE):
            try:
                self.back_to_home_image = pygame.image.load(BACK_TO_HOME_IMAGE).convert_alpha()
                print(f"✓ Loaded back to home image: {BACK_TO_HOME_IMAGE}")
            except Exception as e:
                print(f"✗ Failed to load back to home image: {e}")
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode while maintaining aspect ratio"""
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.display_width, self.display_height), 
                                                   pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)
    
    def get_scaled_rect(self):
        """Calculate the rect for the game surface to maintain aspect ratio"""
        screen_width, screen_height = self.screen.get_size()
        screen_aspect = screen_width / screen_height
        
        if screen_aspect > self.aspect_ratio:
            # Screen is wider than game - letterbox on sides
            scaled_height = screen_height
            scaled_width = int(scaled_height * self.aspect_ratio)
            x_offset = (screen_width - scaled_width) // 2
            y_offset = 0
        else:
            # Screen is taller than game - letterbox on top/bottom
            scaled_width = screen_width
            scaled_height = int(scaled_width / self.aspect_ratio)
            x_offset = 0
            y_offset = (screen_height - scaled_height) // 2
            
        return pygame.Rect(x_offset, y_offset, scaled_width, scaled_height)
    
    def scale_mouse_pos(self, mouse_pos):
        """Convert screen mouse position to game surface coordinates"""
        scaled_rect = self.get_scaled_rect()
        
        # Check if mouse is within the game area
        if not scaled_rect.collidepoint(mouse_pos):
            return None
            
        # Convert to game coordinates
        x = (mouse_pos[0] - scaled_rect.x) * GAME_WIDTH / scaled_rect.width
        y = (mouse_pos[1] - scaled_rect.y) * GAME_HEIGHT / scaled_rect.height
        x = (mouse_pos[0] - scaled_rect.x) * GAME_WIDTH / scaled_rect.width
        return (int(x), int(y))
        
    def load_dialogue_audio(self, audio_path):
        """Load and play dialogue audio"""
        try:
            self.dialogue_audio_path = audio_path
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Failed to load audio: {e}")
    
    def set_dialogue(self, text, audio_path=None):
        """Set the dialogue text and optional audio"""
        self.current_dialogue = text
        # Wrap text for display - use smaller width for 80% sized box
        # Box width is 384, minus padding on both sides (10*2) = 364
        self.dialogue_lines = self.wrap_text(text, pygame.font.Font(None, 28), 360)
        
        if audio_path:
            self.load_dialogue_audio(audio_path)
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def get_dishes_for_category(self, category):
        """Get list of dish IDs for a given category"""
        dishes = {
            "steamed": ["shrimp_dumpling", "shumai", "bbq_pork_bun", "custard_bun", 
                       "chicken_feet", "spare_ribs", "beef_balls", "sticky_rice"],
            "fried": ["spring_roll", "dumpling_fried", "taro_cake", "water_chestnut"],
            "congee": ["beef_noodle", "shrimp_noodle", "century_egg_congee", "chinese_kale"]
        }
        return dishes.get(category, [])
    
    def draw_start_screen(self):
        """Draw the start screen"""
        # Background - use custom image if available
        if self.start_screen_bg:
            # Scale background to cover the game surface while maintaining aspect ratio
            bg_rect = self.start_screen_bg.get_rect()
            scale_x = GAME_WIDTH / bg_rect.width
            scale_y = GAME_HEIGHT / bg_rect.height
            scale = max(scale_x, scale_y)  # Use max to cover entire surface
            
            new_width = int(bg_rect.width * scale)
            new_height = int(bg_rect.height * scale)
            scaled_bg = pygame.transform.scale(self.start_screen_bg, (new_width, new_height))
            
            # Center the background
            x_offset = (GAME_WIDTH - new_width) // 2
            y_offset = (GAME_HEIGHT - new_height) // 2
            
            self.game_surface.blit(scaled_bg, (x_offset, y_offset))
        else:
            # Default white background
            self.game_surface.fill(WHITE)
            
            # Default title (only show if no custom background)
            title = self.title_font.render("Cantonese Dim Sum", True, BLACK)
            subtitle = self.dialogue_font.render("Learn to Order in Cantonese!", True, DARK_GRAY)
            
            title_rect = title.get_rect(center=(GAME_WIDTH // 2, 200))
            subtitle_rect = subtitle.get_rect(center=(GAME_WIDTH // 2, 280))
            
            self.game_surface.blit(title, title_rect)
            self.game_surface.blit(subtitle, subtitle_rect)
        
        # Start button - use custom image if available (ALWAYS draw, not inside else block)
        if self.start_button_image and self.start_button_rect:
            # Apply hover/click effects
            current_time = pygame.time.get_ticks()
            
            # Calculate scale based on state
            if self.start_button_clicked and current_time - self.start_button_click_time < 150:
                # Clicked effect: shrink to 90% for 150ms
                scale_factor = 0.90
            elif self.start_button_hovered:
                # Hover effect: grow to 110%
                scale_factor = 1.10
            else:
                # Normal size
                scale_factor = 1.0
            
            # Scale the button image
            if scale_factor != 1.0:
                new_width = int(self.start_button_base_rect.width * scale_factor)
                new_height = int(self.start_button_base_rect.height * scale_factor)
                scaled_button = pygame.transform.scale(self.start_button_image, (new_width, new_height))
                
                # Center the scaled button on the base position
                scaled_rect = scaled_button.get_rect(
                    center=self.start_button_base_rect.center
                )
                self.game_surface.blit(scaled_button, scaled_rect)
                
                # Update hitbox for click detection
                self.start_button_rect = scaled_rect
            else:
                # Draw at normal size
                self.game_surface.blit(self.start_button_image, self.start_button_base_rect)
                self.start_button_rect = self.start_button_base_rect.copy()
        else:
            # Default button (if no custom image)
            self.start_button.draw(self.game_surface)
        
        # Instruction for fullscreen (always show)
        instruction = pygame.font.Font(None, 24).render("Press F11 for fullscreen", True, DARK_GRAY)
        instruction_rect = instruction.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT - 50))
        self.game_surface.blit(instruction, instruction_rect)
        
    def draw_game_screen(self):
        """Draw the main game screen"""
        # Background (canteen) - maintain aspect ratio
        if self.canteen_bg:
            # Scale background to cover the game surface while maintaining aspect ratio
            bg_rect = self.canteen_bg.get_rect()
            scale_x = GAME_WIDTH / bg_rect.width
            scale_y = GAME_HEIGHT / bg_rect.height
            scale = max(scale_x, scale_y)  # Use max to cover entire surface
            
            new_width = int(bg_rect.width * scale)
            new_height = int(bg_rect.height * scale)
            scaled_bg = pygame.transform.scale(self.canteen_bg, (new_width, new_height))
            
            # Center the background
            x_offset = (GAME_WIDTH - new_width) // 2
            y_offset = (GAME_HEIGHT - new_height) // 2
            
            self.game_surface.blit(scaled_bg, (x_offset, y_offset))
        else:
            self.game_surface.fill((245, 222, 179))  # Wheat color as default
        
        # Draw NPC at current position (maintain aspect ratio) - same size as player, 120 height
        npc_x, npc_y = int(self.npc_position[0]), int(self.npc_position[1])
        
        # Determine which image to show
        current_npc_img = None
        
        if self.npc_at_player and self.npc_full_body_image:
            # Use full body image when waiting at player
            current_npc_img = self.npc_full_body_image
        elif self.npc_moving:
             # Use directional animation when moving
            if self.npc_frames.get(self.npc_direction):
                # Update animation frame
                current_time = pygame.time.get_ticks()
                if current_time - self.npc_last_frame_time > self.npc_frame_duration:
                    self.npc_frame_index = (self.npc_frame_index + 1) % len(self.npc_frames[self.npc_direction])
                    self.npc_last_frame_time = current_time
                
                frames = self.npc_frames[self.npc_direction]
                if frames:
                    current_npc_img = frames[self.npc_frame_index]
            else:
                # Fallback to static directional image
                current_npc_img = self.npc_images.get(self.npc_direction)
        
        # If no specific image found (not moving or no directional image), use default
        if not current_npc_img:
            current_npc_img = self.npc_image
        
        if current_npc_img:
            # Use the image as-is (it is already resized in load_assets)
            npc_width = current_npc_img.get_width()
            npc_height = current_npc_img.get_height()
            
            # Adjust Y position so feet are at the same level as the original 120px sprite
            # Original sprite was drawn at npc_y with height 120. Bottom was npc_y + 120.
            # New sprite bottom should be at same position.
            # New top = (npc_y + 120) - npc_height
            
            draw_y = npc_y + 120 - npc_height
            
            self.game_surface.blit(current_npc_img, (npc_x, draw_y))
            self.npc_rect = pygame.Rect(npc_x, draw_y, npc_width, npc_height)
        else:
            npc_width, npc_height = 96, 120
            pygame.draw.rect(self.game_surface, BLUE, (npc_x, npc_y, npc_width, npc_height))
            npc_label = self.dialogue_font.render("NPC", True, WHITE)
            self.game_surface.blit(npc_label, (npc_x + 30, npc_y + 50))
            self.npc_rect = pygame.Rect(npc_x, npc_y, npc_width, npc_height)
        
        # Draw clickable indicator if NPC is near player
        if self.npc_clickable and not self.ordering_mode:
            # Draw subtle highlight or indicator
            pygame.draw.rect(self.game_surface, (255, 255, 0), self.npc_rect, 3)
        
        # Draw Table (bottom-right corner)
        if self.table_image:
            # Scale table while maintaining aspect ratio
            table_rect_img = self.table_image.get_rect()
            scale_factor = min(self.table_rect.width / table_rect_img.width, 
                             self.table_rect.height / table_rect_img.height)
            table_width = int(table_rect_img.width * scale_factor)
            table_height = int(table_rect_img.height * scale_factor)
            table_scaled = pygame.transform.scale(self.table_image, (table_width, table_height))
            self.game_surface.blit(table_scaled, (self.table_rect.x, self.table_rect.y))
        else:
            # Draw placeholder table (only when player is NOT seated)
            if not self.player_seated:
                pygame.draw.rect(self.game_surface, (255,247,225), self.table_rect)
                # Show "Click to sit" message
                sit_text = pygame.font.Font(None, 28).render("Click to sit", True, (207,118,44))
                sit_rect = sit_text.get_rect(center=self.table_rect.center)
                self.game_surface.blit(sit_text, sit_rect)
            
        # Draw Player (only if seated, maintain aspect ratio, 80% size)
        if self.player_seated:
            if self.player_image:
                player_rect = self.player_image.get_rect()
                # Scale to height of 140, maintain aspect ratio
                scale_factor = 140 / player_rect.height
                player_width = int(player_rect.width * scale_factor)
                player_scaled = pygame.transform.scale(self.player_image, (player_width, 140))
                # Position player at the top center side of the table (sitting position)
                player_x = self.table_rect.centerx - (player_width // 2)
                player_y = self.table_rect.top - 140  # Slightly overlap table 
                self.game_surface.blit(player_scaled, (player_x, player_y))
            else:
                # Draw placeholder player - 80% size and positioned at left of table
                player_rect = pygame.Rect(self.table_rect.left - 112, self.table_rect.centery - 60, 96, 120)
                pygame.draw.rect(self.game_surface, GREEN, player_rect)
                player_label = self.dialogue_font.render("Player", True, WHITE)
                self.game_surface.blit(player_label, (player_rect.x + 12, player_rect.y + 48))
        
        # Draw menu icon on table (if timer has ended)
        if self.show_menu and self.player_seated:
            icon_x = self.table_rect.centerx
            icon_y = self.table_rect.centery - 100 
            
            if self.menu_icon:
                # Draw menu icon (157x157)
                self.game_surface.blit(pygame.transform.scale(self.menu_icon, (int(157 * 0.7), int(157 * 0.7))), (icon_x, icon_y))
                self.menu_icon_rect = pygame.Rect(icon_x, icon_y, int(157 * 0.7), int(157 * 0.7))
            else:
                # Fallback: draw placeholder icon
                self.menu_icon_rect = pygame.Rect(icon_x, icon_y, 94, 136)
                pygame.draw.rect(self.game_surface, WHITE, self.menu_icon_rect)
                pygame.draw.rect(self.game_surface, BLACK, self.menu_icon_rect, 2)
                menu_label = pygame.font.Font(None, 20).render("Menu", True, BLACK)
                self.game_surface.blit(menu_label, (icon_x + 25, icon_y + 60))
        
        # Timer (top right corner) - only show if active
        if self.timer_active:
            self.draw_timer()
        
        # Dialogue box - show if game has started (always visible during game, even before timer)
        if self.state == "game":
            self.draw_dialogue_box()
        
        # Recording box - only show if timer is active
        if self.timer_active:
            self.draw_recording_box()
        
        # Shopping cart - only show after timer ends
        if self.show_shopping_cart and self.player_seated:
            self.draw_shopping_cart()
        
        # Draw full menu interface (if menu is open) - LAST so it appears on top of everything
        if self.menu_open and self.player_seated:
            # Draw semi-transparent overlay (dark background)
            overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.game_surface.blit(overlay, (0, 0))
            
            if self.menu_full:
                # Scale menu to 70% of original size
                original_width = self.menu_full.get_width()
                original_height = self.menu_full.get_height()
                menu_full_width = int(original_width * 0.7)
                menu_full_height = int(original_height * 0.7)
                
                # Scale the menu image
                scaled_menu = pygame.transform.scale(self.menu_full, (menu_full_width, menu_full_height))
                
                # Center the scaled menu on screen
                menu_x = (GAME_WIDTH - menu_full_width) // 2
                menu_y = (GAME_HEIGHT - menu_full_height) // 2
                
                # Draw scaled menu background
                self.game_surface.blit(scaled_menu, (menu_x, menu_y))
                self.menu_full_rect = pygame.Rect(menu_x, menu_y, menu_full_width, menu_full_height)
                
                # Draw category buttons on the LEFT side of menu (scaled to 70%)
                button_x = menu_x + int(40) # Scaled distance from menu
                button_y_start = menu_y + int(125)  # Scaled start position
                button_spacing = int(120)  # Scaled vertical spacing
                
                self.menu_category_buttons = {}
                categories = ["steamed", "fried", "congee"]
                
                for i, category in enumerate(categories):
                    btn_y = button_y_start + (i * button_spacing)
                    
                    if category in self.category_btn_images:
                        btn_img = self.category_btn_images[category]
                        # Scale button image to 70%
                        original_btn_width = btn_img.get_width()
                        original_btn_height = btn_img.get_height()
                        btn_width = int(original_btn_width * 0.7)
                        btn_height = int(original_btn_height * 0.7)
                        btn_img = pygame.transform.scale(btn_img, (btn_width, btn_height))
                        
                        # Highlight if this is current category
                        if category == self.current_category:
                            # Draw highlight background
                            highlight_rect = pygame.Rect(button_x - 5, btn_y - 5, btn_width + 10, btn_height + 10)
                            pygame.draw.rect(self.game_surface, (255, 255, 0), highlight_rect, 3)
                        
                        self.game_surface.blit(btn_img, (button_x, btn_y))
                        self.menu_category_buttons[category] = pygame.Rect(button_x, btn_y, btn_width, btn_height)
                    else:
                        # Fallback: draw placeholder buttons (scaled to 70%)
                        btn_width, btn_height = int(120 * 0.7), int(80 * 0.7)
                        btn_rect = pygame.Rect(button_x, btn_y, btn_width, btn_height)
                        
                        # Highlight if current category
                        color = (255, 200, 0) if category == self.current_category else GRAY
                        pygame.draw.rect(self.game_surface, color, btn_rect)
                        pygame.draw.rect(self.game_surface, BLACK, btn_rect, 2)
                        
                        # Category labels (scaled font size)
                        labels = {"steamed": "蒸点", "fried": "炸点", "congee": "粥粉"}
                        label = pygame.font.Font(None, int(32 * 0.7)).render(labels[category], True, BLACK)
                        label_rect = label.get_rect(center=btn_rect.center)
                        self.game_surface.blit(label, label_rect)
                        
                        self.menu_category_buttons[category] = btn_rect
                
                # Define menu boundary rect (dish display area) - no visible border
                boundary_width, boundary_height = menu_full_width - int(100 * 0.7), menu_full_height - int(160 * 0.7)
                boundary_x = menu_x + int(50 * 0.7)
                boundary_y = menu_y + int(80 * 0.7)
                self.menu_boundary_rect = pygame.Rect(boundary_x, boundary_y, boundary_width, boundary_height)
                
                # Draw dishes in a 3-column grid within boundary
                self.draw_menu_dishes()
                
                # Draw close button on top-right corner of menu
                if self.close_button_image:
                    close_btn_x = menu_x + menu_full_width - self.close_button_image.get_width() - 10
                    close_btn_y = menu_y + 10
                    self.game_surface.blit(self.close_button_image, (close_btn_x, close_btn_y))
                    self.close_button_rect = pygame.Rect(close_btn_x, close_btn_y, 
                                                         self.close_button_image.get_width(), 
                                                         self.close_button_image.get_height())
                else:
                    # Fallback: draw X button
                    close_btn_size = 30
                    close_btn_x = menu_x + menu_full_width - close_btn_size - 10
                    close_btn_y = menu_y + 10
                    self.close_button_rect = pygame.Rect(close_btn_x, close_btn_y, close_btn_size, close_btn_size)
                    pygame.draw.rect(self.game_surface, RED, self.close_button_rect)
                    pygame.draw.rect(self.game_surface, WHITE, self.close_button_rect, 2)
                    close_text = pygame.font.Font(None, 24).render("X", True, WHITE)
                    self.game_surface.blit(close_text, (close_btn_x + 8, close_btn_y + 3))
            else:
                # Fallback: draw placeholder menu
                menu_width, menu_height = 800, 600
                menu_x = (GAME_WIDTH - menu_width) // 2
                menu_y = (GAME_HEIGHT - menu_height) // 2
                
                # Draw overlay
                overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
                overlay.set_alpha(180)
                overlay.fill(BLACK)
                self.game_surface.blit(overlay, (0, 0))
                
                # Draw placeholder menu
                self.menu_full_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
                pygame.draw.rect(self.game_surface, WHITE, self.menu_full_rect)
                pygame.draw.rect(self.game_surface, BLACK, self.menu_full_rect, 3)
                
                menu_title = pygame.font.Font(None, 48).render("Menu", True, BLACK)
                self.game_surface.blit(menu_title, (menu_x + 340, menu_y + 30))
                
                # Close button
                close_btn_size = 30
                close_btn_x = menu_x + menu_width - close_btn_size - 10
                close_btn_y = menu_y + 10
                self.close_button_rect = pygame.Rect(close_btn_x, close_btn_y, close_btn_size, close_btn_size)
                pygame.draw.rect(self.game_surface, RED, self.close_button_rect)
                pygame.draw.rect(self.game_surface, WHITE, self.close_button_rect, 2)
                close_text = pygame.font.Font(None, 24).render("X", True, WHITE)
                self.game_surface.blit(close_text, (close_btn_x + 8, close_btn_y + 3))
        
        # Draw NPC ordering interface (if player clicked NPC) - LAST so it appears on top
        if self.ordering_mode and self.player_seated:
            self.draw_ordering_interface()
            
        # Draw Bill (if checkout clicked)
        if self.show_bill:
            self.draw_bill()
        
    def draw_ordering_interface(self):
        """Draw the NPC ordering interface when player clicks NPC"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.game_surface.blit(overlay, (0, 0))
        
        # Draw NPC full body on lower-left (about 1/4 from left)
        # Use original full body image if available, otherwise use the resized one
        # Switch to ordering image if recording or transcribed text is present
        if (self.order_recording or self.order_transcribed_text) and self.npc_full_body_ordering:
            npc_img_to_use = self.npc_full_body_ordering
        else:
            npc_img_to_use = getattr(self, 'npc_full_body_original', self.npc_full_body_image)
        
        if npc_img_to_use:
            npc_img = npc_img_to_use
            npc_width = npc_img.get_width()
            npc_height = npc_img.get_height()
            
            # Position at lower-left (scale if too large)
            max_height = GAME_HEIGHT - 100
            if npc_height > max_height:
                scale_factor = max_height / npc_height
                npc_width = int(npc_width * scale_factor)
                npc_height = max_height
                npc_img = pygame.transform.scale(npc_img_to_use, (npc_width, npc_height))
            
            npc_x = GAME_WIDTH // 4 - npc_width // 2
            npc_y = GAME_HEIGHT - npc_height - 20
            self.game_surface.blit(npc_img, (npc_x, npc_y))
        else:
            # Fallback: draw placeholder
            npc_x = GAME_WIDTH // 4 - 75
            npc_y = GAME_HEIGHT - 320
            pygame.draw.rect(self.game_surface, BLUE, (npc_x, npc_y, 150, 300))
            pygame.draw.rect(self.game_surface, WHITE, (npc_x, npc_y, 150, 300), 3)
            npc_label = pygame.font.Font(None, 36).render("NPC", True, WHITE)
            self.game_surface.blit(npc_label, (npc_x + 45, npc_y + 140))
        
        # Update dialogue to show NPC question (audio already played when entering ordering mode)
        temp_dialogue = self.current_dialogue
        temp_lines = self.dialogue_lines
        self.set_dialogue("What can I help you with?", None)  # Don't play audio here - already played on click
        
        # Draw dialogue box (will show NPC question)
        self.draw_dialogue_box()
        
        # Restore original dialogue
        self.current_dialogue = temp_dialogue
        self.dialogue_lines = temp_lines
        
        # Draw two buttons in center-lower area
        button_width = 303
        button_height = 158
        button_spacing = 40
        total_width = button_width * 2 + button_spacing
        start_x = (GAME_WIDTH - total_width) // 2
        button_y = GAME_HEIGHT - 200
        
        # Place Order button (left)
        self.place_order_button = pygame.Rect(start_x, button_y, button_width, button_height)
        
        if self.order_button_image:
            # Scale image to fit button rect
            scaled_order_btn = pygame.transform.smoothscale(self.order_button_image, (button_width, button_height))
            self.game_surface.blit(scaled_order_btn, (start_x, button_y))
            
            # Draw microphone icon
            # Determine state
            mic_state = "default"
            if self.order_recording:
                mic_state = "recording"
            elif self.place_order_button.collidepoint(self.scale_mouse_pos(pygame.mouse.get_pos()) or (0,0)):
                mic_state = "hover"
            
            mic_img = self.microphone_images.get(mic_state)
            if mic_img:
                # Position: right side, middle height
                # Button width is 303. Right side middle.
                # Mic size is 48x48.
                
                mic_target_width = 48
                mic_target_height = 48
                scaled_mic = pygame.transform.smoothscale(mic_img, (mic_target_width, mic_target_height))
                
                # Position at right middle with some padding
                # Let's place it at 15% of width from right
                # x = start_x + button_width - padding - mic_width
                mic_x = start_x + button_width - 45 - mic_target_width
                mic_y = button_y + (button_height - mic_target_height) // 2
                
                self.game_surface.blit(scaled_mic, (mic_x, mic_y))
        else:
            # Fallback
            pygame.draw.rect(self.game_surface, GREEN, self.place_order_button)
            pygame.draw.rect(self.game_surface, BLACK, self.place_order_button, 3)
            order_text = pygame.font.Font(None, 42).render("Place Order", True, BLACK)
            order_rect = order_text.get_rect(center=self.place_order_button.center)
            self.game_surface.blit(order_text, order_rect)
        
        # Check Out button (right)
        self.checkout_button = pygame.Rect(start_x + button_width + button_spacing, button_y, button_width, button_height)
        
        if self.check_button_image:
            # Scale image to fit button rect
            scaled_check_btn = pygame.transform.smoothscale(self.check_button_image, (button_width, button_height))
            self.game_surface.blit(scaled_check_btn, (self.checkout_button.x, self.checkout_button.y))
        else:
            # Fallback
            pygame.draw.rect(self.game_surface, BLUE, self.checkout_button)
            pygame.draw.rect(self.game_surface, BLACK, self.checkout_button, 3)
            checkout_text = pygame.font.Font(None, 42).render("Check Out", True, WHITE)
            checkout_rect = checkout_text.get_rect(center=self.checkout_button.center)
            self.game_surface.blit(checkout_text, checkout_rect)
        
        # If Place Order was clicked, show recording interface
        if self.order_recording or self.order_transcribed_text:
            # Recording area below buttons
            record_y = button_y - 120
            record_width = 400
            record_height = 100
            record_x = (GAME_WIDTH - record_width) // 2
            
            record_rect = pygame.Rect(record_x, record_y, record_width, record_height)
            
            # Draw recording box with custom colors and rounded corners
            # Outer color: RGB 133,63,31
            # Inner color: RGB 255, 242, 223
            # Corner radius: 15
            
            # Draw filled inner box
            pygame.draw.rect(self.game_surface, (255, 242, 223), record_rect, border_radius=15)
            # Draw border
            pygame.draw.rect(self.game_surface, (133, 63, 31), record_rect, 3, border_radius=15)
            
            # Recording button
            self.order_record_button = pygame.Rect(record_x + 10, record_y + 10, 180, 50)
            # Start Recording: RGB 170, 167, 165
            # Recording (Stop): RGB 253, 152, 73
            btn_color = (253, 152, 73) if self.order_recording else (170, 167, 165)
            btn_text = "Stop Recording" if self.order_recording else "Start Recording"
            pygame.draw.rect(self.game_surface, btn_color, self.order_record_button)
            pygame.draw.rect(self.game_surface, BLACK, self.order_record_button, 2)
            rec_text = pygame.font.Font(None, 28).render(btn_text, True, WHITE)
            rec_text_rect = rec_text.get_rect(center=self.order_record_button.center)
            self.game_surface.blit(rec_text, rec_text_rect)
            
            # Show transcribed text
            if self.order_transcribed_text:
                text_lines = self.wrap_text(self.order_transcribed_text, pygame.font.Font(None, 24), record_width - 20)
                y_offset = record_y + 65
                for line in text_lines[:2]:  # Max 2 lines
                    text_surf = pygame.font.Font(None, 24).render(line, True, BLACK)
                    self.game_surface.blit(text_surf, (record_x + 10, y_offset))
                    y_offset += 26
    
    def draw_timer(self):
        """Draw the countdown timer"""
        # Only show timer if it's active (after player sits)
        if not self.timer_active:
            return
            
        if self.start_time:
            elapsed = pygame.time.get_ticks() - self.start_time
            self.time_remaining = max(0, GAME_TIME - elapsed // 1000)
            
            # Check if time is up
            if self.time_remaining == 0:
                self.timer_active = False  # Hide timer
                self.show_menu = True  # Show menu on table
                self.show_shopping_cart = True  # Show shopping cart
                self.npc_moving = True  # Start NPC movement
                
                # Handle tea timeout if no tea selected
                if self.waiting_for_tea_choice and not self.tea_selected:
                    self.handle_tea_timeout()
        
        seconds = self.time_remaining
        timer_text = f"{seconds:02d}s"
        
        # Timer background - positioned at top right (more to the right)
        timer_rect = pygame.Rect(GAME_WIDTH - 220, 20, 180, 80)
        pygame.draw.rect(self.game_surface, WHITE, timer_rect)
        pygame.draw.rect(self.game_surface, BLACK, timer_rect, 3)
        
        # Timer text - red when less than 6 seconds
        timer_surface = self.timer_font.render(timer_text, True, BLACK if self.time_remaining > 5 else RED)
        timer_text_rect = timer_surface.get_rect(center=timer_rect.center)
        self.game_surface.blit(timer_surface, timer_text_rect)
        
    def draw_dialogue_box(self):
        """Draw the dialogue display box"""
        # Position below timer in top-right area
        # Original box was 384x160. New image is approx 800x309.
        # We should scale it down to fit the UI better, maybe 50%? -> 400x155
        
        target_width = 400
        target_height = 155
        box_x = GAME_WIDTH - 420
        box_y = 120
        
        if self.npc_dialogue_image:
            # Use image
            scaled_img = pygame.transform.smoothscale(self.npc_dialogue_image, (target_width, target_height))
            self.game_surface.blit(scaled_img, (box_x, box_y))
            
            # Text area: Right 3/4 of the box, with padding
            # Box width 400. 3/4 is 300. Start x = box_x + 100.
            # Padding: let's say 20px from right edge, 10px from top/bottom
            text_area_width = (target_width * 0.75) - 30 # 300 - 30 = 270
            text_start_x = box_x + (target_width * 0.25) + 10 # 100 + 10 = 110 offset
            text_start_y = box_y + 20
            
            # Re-wrap text for new width
            wrapped_lines = self.wrap_text(self.current_dialogue, pygame.font.Font(None, 26), text_area_width)
            
            y_offset = text_start_y
            dialogue_font = pygame.font.Font(None, 26)
            
            for line in wrapped_lines[:4]: # Show up to 4 lines
                text_surface = dialogue_font.render(line, True, BLACK)
                self.game_surface.blit(text_surface, (text_start_x, y_offset))
                y_offset += 24
                
            # Play audio button removed as requested
                
        else:
            # Fallback to rectangle
            box_rect = pygame.Rect(box_x, box_y, 384, 160)
            pygame.draw.rect(self.game_surface, WHITE, box_rect)
            pygame.draw.rect(self.game_surface, BLACK, box_rect, 3)
            
            title_font = pygame.font.Font(None, 28)
            title = title_font.render("Dialogue:", True, BLACK)
            self.game_surface.blit(title, (GAME_WIDTH - 410, 130))
            
            # Dialogue text - ensure it stays within box boundaries
            y_offset = 160
            dialogue_font = pygame.font.Font(None, 26)  # Slightly smaller font
            max_lines = 3  # Limit number of lines to fit in box
            for i, line in enumerate(self.dialogue_lines[:max_lines]):
                if y_offset + 26 > box_rect.bottom - 10:  # Check if text exceeds box
                    break
                text_surface = dialogue_font.render(line, True, BLACK)
                self.game_surface.blit(text_surface, (GAME_WIDTH - 410, y_offset))
                y_offset += 28
            
            # Play audio button (if audio is loaded)
            if self.dialogue_audio_path:
                play_button = Button(GAME_WIDTH - 130, 130, 90, 35, "Play", BLUE, WHITE)
                play_button.draw(self.game_surface)
            
    def draw_recording_box(self):
        """Draw the recording box"""
        # Position below dialogue box
        target_width = 400
        target_height = 155
        box_x = GAME_WIDTH - 420
        box_y = 300
        
        if self.player_dialogue_image:
            # Use image
            scaled_img = pygame.transform.smoothscale(self.player_dialogue_image, (target_width, target_height))
            self.game_surface.blit(scaled_img, (box_x, box_y))
            
            # Text area: Left 3/4 of the box, with padding
            # Box width 400. 3/4 is 300.
            # Padding: 20px from left edge, 10px from top
            text_area_width = (target_width * 0.75) - 30 # 270
            text_start_x = box_x + 20
            text_start_y = box_y + 20
            
            # Title
            title = pygame.font.Font(None, 28).render("Your Answer:", True, BLACK)
            self.game_surface.blit(title, (text_start_x, text_start_y))
            
            # Record button - position left middle with padding, moved down slightly
            btn_width = 120
            btn_height = 40
            btn_x = text_start_x
            btn_y = box_y + (target_height // 2) - (btn_height // 2) + 20 # Added 20px offset
            
            # Colors: Default (170, 167, 165), Recording (253, 152, 73)
            btn_color = (253, 152, 73) if self.is_recording else (170, 167, 165)
            
            record_button_small = Button(btn_x, btn_y, btn_width, btn_height, 
                                        "Stop" if self.is_recording else "Record", 
                                        btn_color, WHITE)
            record_button_small.draw(self.game_surface)
            
            # Update main record button position for click detection
            self.record_button.rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
            
            # Show transcribed text
            if self.transcribed_text:
                # Wrap transcribed text
                wrapped_transcription = self.wrap_text(self.transcribed_text, 
                                                    pygame.font.Font(None, 22), text_area_width)
                y_offset = text_start_y + 30
                for line in wrapped_transcription[:2]:
                    text_surface = pygame.font.Font(None, 22).render(line, True, BLACK)
                    self.game_surface.blit(text_surface, (text_start_x, y_offset))
                    y_offset += 20
        else:
            # Fallback to rectangle
            box_rect = pygame.Rect(box_x, box_y, 384, 160)
            pygame.draw.rect(self.game_surface, WHITE, box_rect)
            pygame.draw.rect(self.game_surface, BLACK, box_rect, 3)
            
            # Title
            title = pygame.font.Font(None, 28).render("Your Answer:", True, BLACK)  # Smaller font
            self.game_surface.blit(title, (GAME_WIDTH - 410, 310))
            
            # Record button (80% size)
            record_button_small = Button(GAME_WIDTH - 380, 345, 240, 64, 
                                        "Stop" if self.is_recording else "Record", 
                                        GREEN if self.is_recording else RED, WHITE)
            record_button_small.draw(self.game_surface)
            
            # Update main record button position for click detection
            self.record_button.rect = pygame.Rect(GAME_WIDTH - 380, 345, 240, 64)
            
            # Show transcribed text
            if self.transcribed_text:
                # Wrap transcribed text
                wrapped_transcription = self.wrap_text(self.transcribed_text, 
                                                    pygame.font.Font(None, 22), 350)
                y_offset = 420
                for line in wrapped_transcription[:2]:  # Show max 2 lines
                    text_surface = pygame.font.Font(None, 22).render(line, True, DARK_GRAY)
                    self.game_surface.blit(text_surface, (GAME_WIDTH - 410, y_offset))
                    y_offset += 25
    
    def draw_shopping_cart(self):
        """Draw the shopping cart with scrolling support for items"""
        
        cart_x = GAME_WIDTH - 410
        cart_y = 650
        
        if self.shopping_cart_image:
            # Scale shopping cart image to 70% of original size
            original_width = self.shopping_cart_image.get_width()
            original_height = self.shopping_cart_image.get_height()
            scaled_width = int(original_width * 0.7)
            scaled_height = int(original_height * 0.7)
            
            # Scale the image
            scaled_cart = pygame.transform.scale(self.shopping_cart_image, (scaled_width, scaled_height))
            
            # Draw scaled shopping cart image as background
            self.game_surface.blit(scaled_cart, (cart_x, cart_y))
            self.shopping_cart_rect = pygame.Rect(cart_x, cart_y, scaled_width, scaled_height)
            
            # Draw cart items horizontally with left-right scrolling
            if self.cart_items:
                # Create clipping region for items with side margins
                side_margin = 40  # Leave 40px margin on each side
                items_x = cart_x + side_margin
                items_y = cart_y + 70  # Lower position
                items_width = scaled_width - (side_margin * 2)  # Subtract margins from both sides
                items_height = scaled_height - 100  # Larger scroll area
                items_rect = pygame.Rect(items_x, items_y, items_width, items_height)
                
                self.game_surface.set_clip(items_rect)
                
                # Draw each item horizontally (left to right)
                item_size = 80  # User adjusted size
                padding = 5
                
                for i, dish_id in enumerate(self.cart_items):
                    # Calculate x position for each item
                    x_offset = items_x + i * (item_size + padding) - self.cart_scroll_offset
                    
                    if dish_id in self.dish_images:
                        dish_img = self.dish_images[dish_id]
                        scaled_dish = pygame.transform.scale(dish_img, (item_size, item_size))
                        
                        # Only draw if visible (horizontal check)
                        if x_offset + item_size >= items_x and x_offset <= items_x + items_width:
                            self.game_surface.blit(scaled_dish, (x_offset, items_y))
                
                self.game_surface.set_clip(None)
        else:
            # Fallback: draw placeholder shopping cart with items
            cart_width, cart_height = int(384 * 0.7), int(280 * 0.7)  # Taller for items
            self.shopping_cart_rect = pygame.Rect(cart_x, cart_y, cart_width, cart_height)
            pygame.draw.rect(self.game_surface, WHITE, self.shopping_cart_rect)
            pygame.draw.rect(self.game_surface, BLACK, self.shopping_cart_rect, 3)
            
            # Title
            title = pygame.font.Font(None, 28).render("Shopping Cart:", True, BLACK)
            self.game_surface.blit(title, (cart_x + 10, cart_y + 10))
            
            # Draw items horizontally (left to right)
            if self.cart_items:
                side_margin = 40  # Leave 40px margin on each side
                items_x = cart_x + side_margin
                items_y = cart_y + 90  # Lower position (center-bottom area)
                item_size = 80  # User adjusted size
                padding = 5
                
                for i, dish_id in enumerate(self.cart_items):
                    x_pos = items_x + i * (item_size + padding) - self.cart_scroll_offset
                    
                    # Only draw if visible (horizontal check)
                    if x_pos + item_size >= items_x and x_pos <= cart_x + cart_width - 10:
                        if dish_id in self.dish_images:
                            dish_img = self.dish_images[dish_id]
                            scaled_dish = pygame.transform.scale(dish_img, (item_size, item_size))
                            self.game_surface.blit(scaled_dish, (x_pos, items_y))
            else:
                # Empty cart message
                placeholder = pygame.font.Font(None, 24).render("(Empty)", True, DARK_GRAY)
                self.game_surface.blit(placeholder, (cart_x + 80, cart_y + 100))
    
    def draw_menu_dishes(self):
        """Draw dishes in a 3-column grid with scrolling support"""
        if not self.menu_boundary_rect:
            return
        
        # Get dishes for current category
        dish_ids = self.get_dishes_for_category(self.current_category)
        
        # Grid configuration
        cols = 3
        dish_width = 150  # Width of each dish image
        dish_height = 150  # Height of each dish image
        padding = 20  # Padding between dishes
        
        # Calculate grid layout
        grid_width = (dish_width + padding) * cols - padding - 200  # Extra padding on sides
        start_x = self.menu_boundary_rect.x + (self.menu_boundary_rect.width - grid_width) // 2
        start_y = self.menu_boundary_rect.y + 20  # Top padding
        
        # Clear dish display rects
        self.dish_display_rects = []
        
        # Create a clipping region for the boundary (for scrolling)
        clip_rect = self.menu_boundary_rect.copy()
        self.game_surface.set_clip(clip_rect)
        
        # Draw dishes in grid
        for i, dish_id in enumerate(dish_ids):
            row = i // cols
            col = i % cols
            
            dish_x = start_x + col * (dish_width + padding)
            dish_y = start_y + row * (dish_height + padding) - self.menu_scroll_offset
            
            # Only draw if within visible boundary
            if dish_y + dish_height >= self.menu_boundary_rect.y and dish_y <= self.menu_boundary_rect.bottom:
                dish_rect = pygame.Rect(dish_x, dish_y, dish_width, dish_height)
                
                if dish_id in self.dish_images:
                    # Scale dish image to fit
                    dish_img = self.dish_images[dish_id]
                    scaled_dish = pygame.transform.scale(dish_img, (dish_width, dish_height))
                    self.game_surface.blit(scaled_dish, (dish_x, dish_y))
                else:
                    # Fallback: draw placeholder
                    pygame.draw.rect(self.game_surface, (200, 200, 200), dish_rect)
                    pygame.draw.rect(self.game_surface, BLACK, dish_rect, 2)
                    
                    # Dish label
                    label = pygame.font.Font(None, 20).render(dish_id[:10], True, BLACK)
                    label_rect = label.get_rect(center=dish_rect.center)
                    self.game_surface.blit(label, label_rect)
                
                # Store rect for click detection
                self.dish_display_rects.append((dish_id, dish_rect))
        
        # Remove clipping
        self.game_surface.set_clip(None)
    
    def draw_bill(self):
        """Draw the bill screen"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.game_surface.blit(overlay, (0, 0))
        
        if self.bill_image:
            # Center the bill
            bill_x = (GAME_WIDTH - self.bill_image.get_width()) // 2
            bill_y = (GAME_HEIGHT - self.bill_image.get_height()) // 2
            self.game_surface.blit(self.bill_image, (bill_x, bill_y))
            
            # Scrollable area definition (253x368)
            # Position needs to be determined relative to bill image
            # Assuming it's in the "middle" as requested. 
            # Let's estimate or use fixed offset if user didn't specify exact coordinates.
            # User said "middle position". Let's center it horizontally in the bill, and vertically somewhat centered.
            # Bill size: 654x866. Area size: 253x368.
            
            area_width = 253
            area_height = 368
            area_x = bill_x + (self.bill_image.get_width() - area_width) // 2
            area_y = bill_y + 200 # Estimate Y position, maybe adjust later
            
            self.bill_scroll_area = pygame.Rect(area_x, area_y, area_width, area_height)
            
            # Create clipping rect for scroll area
            self.game_surface.set_clip(self.bill_scroll_area)
            
            # Draw items in 2 columns
            col_count = 2
            item_width = 80 # Same as cart
            item_height = 80
            padding_x = (area_width - (col_count * item_width)) // 3
            padding_y = 20
            
            total_price = 0
            
            for i, dish_id in enumerate(self.cart_items):
                # Calculate price
                price = self.dish_prices.get(dish_id, 0)
                total_price += price
                
                row = i // col_count
                col = i % col_count
                
                item_x = area_x + padding_x + col * (item_width + padding_x)
                item_y = area_y + padding_y + row * (item_height + padding_y) - self.bill_scroll_y
                
                # Draw item if visible
                if item_y + item_height >= area_y and item_y <= area_y + area_height:
                    if dish_id in self.dish_images:
                        dish_img = self.dish_images[dish_id]
                        scaled_dish = pygame.transform.scale(dish_img, (item_width, item_height))
                        self.game_surface.blit(scaled_dish, (item_x, item_y))
                        
                        # Draw price tag
                        price_tag = pygame.font.Font(None, 20).render(f"${price}", True, BLACK)
                        tag_rect = price_tag.get_rect(center=(item_x + item_width//2, item_y + item_height + 10))
                        self.game_surface.blit(price_tag, tag_rect)
            
            self.game_surface.set_clip(None)
            
            # Draw Total Price at bottom right of the area
            total_text = pygame.font.Font(None, 36).render(f"${total_price}", True, BLACK)
            # Position at bottom right of scroll area
            self.game_surface.blit(total_text, (area_x + area_width - 80, area_y + area_height + 50))
            
            # Draw Back to Home button at bottom
            if self.back_to_home_image:
                btn_x = (GAME_WIDTH - self.back_to_home_image.get_width()) // 2
                btn_y = bill_y + self.bill_image.get_height() - 100 # Near bottom of bill or screen?
                # User said "bottom position of bill".
                # Let's put it slightly overlapping or just below the bill content area
                btn_y = bill_y + 650 # Adjust based on bill design
                
                self.back_to_home_rect = pygame.Rect(btn_x, btn_y, self.back_to_home_image.get_width(), self.back_to_home_image.get_height())
                self.game_surface.blit(self.back_to_home_image, (btn_x, btn_y))
        else:
            # Fallback bill
            bill_rect = pygame.Rect((GAME_WIDTH - 600)//2, (GAME_HEIGHT - 800)//2, 600, 800)
            pygame.draw.rect(self.game_surface, WHITE, bill_rect)
            pygame.draw.rect(self.game_surface, BLACK, bill_rect, 3)
            
            title = pygame.font.Font(None, 48).render("Bill", True, BLACK)
            self.game_surface.blit(title, (bill_rect.centerx - 30, bill_rect.y + 30))
            
            # Back button fallback
            self.back_to_home_rect = pygame.Rect(bill_rect.centerx - 100, bill_rect.bottom - 80, 200, 60)
            pygame.draw.rect(self.game_surface, BLUE, self.back_to_home_rect)
            text = pygame.font.Font(None, 32).render("Back to Home", True, WHITE)
            self.game_surface.blit(text, (self.back_to_home_rect.x + 20, self.back_to_home_rect.y + 20))

    def detect_tea_keyword(self, text):
        """Detect tea keywords in transcribed text"""
        if not text:
            return None
        
        text_lower = text.lower()
        print(f"[DEBUG] Checking text for tea keywords: '{text}'")
        print(f"[DEBUG] Lowercase version: '{text_lower}'")
        # Get audio path for the tea type
        # Check each keyword (both original case and lowercase)
        for keyword, tea_type in TEA_KEYWORDS.items():
            keyword_lower = keyword.lower()
            # Check both original text and lowercase text
            if keyword in text or keyword_lower in text_lower:
                print(f"[DEBUG] FOUND tea keyword: '{keyword}' -> {tea_type}")
                return tea_type
        
        print(f"[DEBUG] No tea keyword found in: '{text}'")
        return None
    
    def handle_tea_selection(self, tea_type):
        """Handle tea selection and play corresponding NPC response"""
        self.tea_selected = tea_type
        self.waiting_for_tea_choice = False
        
        # Get tea name in English
        tea_names = {
            "tieguanyin": "Tieguanyin",
            "xiangpian": "jasmine tea",
            "puer": "Pu-erh",
            "hongcha": "black tea"
        }
        tea_name = tea_names.get(tea_type, "jasmine tea")
        
        # All tea types use the same format: "Okay, one [tea name]"
        dialogue_text = f"Okay, one {tea_name}"
        
        # Get audio path for the tea type
        audio_path = self.tea_audio_paths.get(tea_type)
        
        self.set_dialogue(dialogue_text, audio_path)
    
    def handle_tea_timeout(self):
        """Handle timeout - default to jasmine tea"""
        if not self.tea_selected:
            print("Timeout - defaulting to jasmine tea")
            self.handle_tea_selection("xiangpian")
    
    def start_order_recording(self):
        """Start recording for order"""
        self.order_recording = True
        self.order_recording_data = []
        
        def record():
            with sd.InputStream(samplerate=self.sample_rate, channels=1, callback=self.order_audio_callback):
                while self.order_recording:
                    sd.sleep(100)
        
        self.order_record_thread = threading.Thread(target=record)
        self.order_record_thread.start()
        print("[INFO] Started order recording...")

    def order_audio_callback(self, indata, frames, time, status):
        """Callback for order recording"""
        if self.order_recording:
            self.order_recording_data.append(indata.copy())

    def stop_order_recording(self):
        """Stop recording for order and transcribe"""
        print("[INFO] Stopping order recording...")
        self.order_recording = False
        if hasattr(self, 'order_record_thread'):
            self.order_record_thread.join()
        
        if self.order_recording_data:
            import numpy as np
            recording_array = np.concatenate(self.order_recording_data, axis=0)
            temp_file = "temp_order_recording.wav"
            sf.write(temp_file, recording_array, self.sample_rate)
            
            # Transcribe
            print("[INFO] Transcribing order...")
            self.order_transcribed_text = "Transcribing..."
            
            # Run transcription in separate thread to avoid blocking UI
            def transcribe_thread():
                display_text, original_text = self.transcribe_audio(temp_file)
                self.order_transcribed_text = display_text
                print(f"[INFO] Order transcribed: {display_text} ({original_text})")
                
                # Use original text for detection if it contains Chinese characters
                text_to_analyze = original_text if original_text else display_text
                self.handle_order_transcription(text_to_analyze)
                
            threading.Thread(target=transcribe_thread).start()

    def detect_dish_keywords(self, text):
        """Detect dish keywords in transcribed text and return list of dish IDs"""
        if not text:
            return []
        
        detected_dishes = []
        text_lower = text.lower()
        print(f"[DEBUG] Checking text for dish keywords: '{text}'")
        
        # Check each keyword
        for keyword, dish_id in DISH_KEYWORDS.items():
            keyword_lower = keyword.lower()
            # Check both original text and lowercase text
            if keyword in text or keyword_lower in text_lower:
                if dish_id not in detected_dishes:  # Avoid duplicates
                    detected_dishes.append(dish_id)
                    print(f"[DEBUG] FOUND dish keyword: '{keyword}' -> {dish_id}")
        
        print(f"[DEBUG] Total dishes found: {len(detected_dishes)}")
        return detected_dishes
    
    def handle_order_transcription(self, text):
        """Handle order transcription and add detected dishes to cart"""
        # Detect dishes from transcription
        detected_dishes = self.detect_dish_keywords(text)
        
        if detected_dishes:
            # Add dishes to cart
            for dish_id in detected_dishes:
                self.cart_items.append(dish_id)
                print(f"[INFO] Added {dish_id} to cart")
            
            # Close ordering interface
            self.ordering_mode = False
            self.order_recording = False
            self.order_transcribed_text = ""
            
            # Resume NPC movement
            self.npc_moving = True
            
            # Show confirmation message
            dish_count = len(detected_dishes)
            self.set_dialogue(f"Added {dish_count} dish(es) to your cart!", None)
        else:
            # No dishes detected
            self.order_transcribed_text = "Sorry, I didn't catch that. Please try again."
            print("[WARNING] No dishes detected in order")
    
    def update_npc_movement(self):
        """Update NPC position along the path"""
        if not self.npc_moving or self.ordering_mode:
            return
        
        # Check if NPC is waiting at player
        if self.npc_at_player:
            # Make NPC clickable when near player
            self.npc_clickable = True
            
            current_time = pygame.time.get_ticks()
            if current_time - self.npc_wait_time >= self.npc_wait_duration:
                # Finish waiting, continue moving
                self.npc_at_player = False
                self.npc_clickable = False
                self.npc_current_path_index = (self.npc_current_path_index + 1) % len(self.npc_path_points)
            return
        else:
            self.npc_clickable = False
        
        # Get target position
        target = self.npc_path_points[self.npc_current_path_index]
        
        # Calculate direction
        dx = target[0] - self.npc_position[0]
        dy = target[1] - self.npc_position[1]
        
        # Determine direction for sprite
        if abs(dx) > abs(dy):
            self.npc_direction = "right" if dx > 0 else "left"
        else:
            self.npc_direction = "down" if dy > 0 else "up"
            
        distance = (dx**2 + dy**2) ** 0.5
        
        # Check if reached target
        if distance < self.npc_speed:
            self.npc_position = list(target)
            
            # Check if this is the player position (index 0)
            if self.npc_current_path_index == 0:
                self.npc_at_player = True
                self.npc_wait_time = pygame.time.get_ticks()
            else:
                # Move to next waypoint
                self.npc_current_path_index = (self.npc_current_path_index + 1) % len(self.npc_path_points)
        else:
            # Move towards target
            self.npc_position[0] += (dx / distance) * self.npc_speed
            self.npc_position[1] += (dy / distance) * self.npc_speed
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle window resize
            if event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            
            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE and self.fullscreen:
                    self.toggle_fullscreen()
            
            # Handle mouse wheel for scrolling in menu
            if event.type == pygame.MOUSEWHEEL:
                game_pos = self.scale_mouse_pos(pygame.mouse.get_pos())
                if game_pos:
                    # Scroll in menu
                    if self.menu_open and self.menu_boundary_rect:
                        if self.menu_boundary_rect.collidepoint(game_pos):
                            # Scroll dishes
                            scroll_speed = 30
                            self.menu_scroll_offset -= event.y * scroll_speed
                            
                            # Calculate max scroll (prevent scrolling past content)
                            dish_ids = self.get_dishes_for_category(self.current_category)
                            rows = (len(dish_ids) + 2) // 3  # Round up division
                            max_scroll = max(0, rows * 170 - self.menu_boundary_rect.height + 40)
                            
                            # Clamp scroll offset
                            self.menu_scroll_offset = max(0, min(self.menu_scroll_offset, max_scroll))
                            print(f"[DEBUG] Scroll offset: {self.menu_scroll_offset}/{max_scroll}")
                    
                    # Scroll in shopping cart (horizontal scrolling)
                    elif self.shopping_cart_rect and self.shopping_cart_rect.collidepoint(game_pos):
                        if self.cart_items:
                            scroll_speed = 30
                            # Use event.y for horizontal scroll (positive y = scroll right, negative y = scroll left)
                            self.cart_scroll_offset -= event.y * scroll_speed
                            
                            # Calculate max scroll (horizontal)
                            item_size = 80  # User adjusted size
                            padding = 5
                            side_margin = 40  # Margin on each side
                            cart_display_width = int(self.shopping_cart_image.get_width() * 0.7 - side_margin * 2) if self.shopping_cart_image else 350
                            max_scroll = max(0, len(self.cart_items) * (item_size + padding) - cart_display_width)
                            
                            # Clamp scroll offset
                            self.cart_scroll_offset = max(0, min(self.cart_scroll_offset, max_scroll))
                            print(f"[DEBUG] Cart scroll: {self.cart_scroll_offset}/{max_scroll}")
                            
                    # Scroll in Bill
                    elif self.show_bill and self.bill_scroll_area and self.bill_scroll_area.collidepoint(game_pos):
                        scroll_speed = 30
                        self.bill_scroll_y -= event.y * scroll_speed
                        
                        # Calculate max scroll
                        col_count = 2
                        item_height = 80
                        padding_y = 20
                        rows = (len(self.cart_items) + col_count - 1) // col_count
                        content_height = rows * (item_height + padding_y) + padding_y
                        max_scroll = max(0, content_height - self.bill_scroll_area.height)
                        
                        self.bill_scroll_y = max(0, min(self.bill_scroll_y, max_scroll))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Scale mouse position to game coordinates
                game_pos = self.scale_mouse_pos(pygame.mouse.get_pos())
                
                if game_pos is None:
                    continue  # Click was outside game area
                
                if self.state == "start":
                    # Check if start button is clicked (image or default button)
                    if self.start_button_image and self.start_button_rect:
                        # Use custom image button rect
                        if self.start_button_rect.collidepoint(game_pos):
                            self.start_button_clicked = True
                            self.start_button_click_time = pygame.time.get_ticks()
                            self.state = "game"
                            # Don't start timer yet - wait until player sits
                            # Show welcome dialogue before sitting
                            self.set_dialogue("Find any empty seat", WELCOME_AUDIO)
                    else:
                        # Use default button
                        if self.start_button.is_clicked(game_pos):
                            self.state = "game"
                            # Don't start timer yet - wait until player sits
                            # Show welcome dialogue before sitting
                            self.set_dialogue("Find any empty seat", WELCOME_AUDIO)
                        
                elif self.state == "game":
                    # Check if player clicks on table to sit
                    if not self.player_seated and self.table_rect.collidepoint(game_pos):
                        self.player_seated = True
                        # Start timer when player sits
                        self.start_time = pygame.time.get_ticks()
                        self.timer_active = True
                        self.waiting_for_tea_choice = True
                        # Set initial dialogue after sitting
                        self.set_dialogue("How many people? What tea would you like? We have Tieguanyin, jasmine tea, Pu-erh, and black tea.", 
                                        DIALOGUE_AUDIO)
                    
                    # Only allow other interactions if player is seated
                    if self.player_seated:
                        # Handle ordering mode interactions
                        if self.ordering_mode:
                            # Check Place Order button
                            if self.place_order_button and self.place_order_button.collidepoint(game_pos):
                                # Show recording interface (toggle recording state in next section)
                                if not self.order_recording and not self.order_transcribed_text:
                                    # Just show the recording interface, actual recording starts with record button
                                    self.order_transcribed_text = " "  # Placeholder to show interface
                                print("[INFO] Place Order clicked")
                                continue
                            
                            # Check Check Out button
                            if self.checkout_button and self.checkout_button.collidepoint(game_pos):
                                # Show bill
                                print("[INFO] Check Out clicked - Showing Bill")
                                self.show_bill = True
                                self.ordering_mode = False # Hide ordering interface
                                continue
                        
                        # Handle Bill interactions
                        if self.show_bill:
                            if self.back_to_home_rect and self.back_to_home_rect.collidepoint(game_pos):
                                # Reset game
                                print("[INFO] Back to Home clicked - Resetting Game")
                                self.state = "start"
                                self.player_seated = False
                                self.ordering_mode = False
                                self.show_bill = False
                                self.cart_items = []
                                self.tea_selected = None
                                self.waiting_for_tea_choice = False
                                self.timer_active = False
                                self.show_menu = False
                                self.show_shopping_cart = False
                                self.npc_moving = True
                                self.npc_at_player = False
                                self.npc_current_path_index = 0
                                self.npc_position = list(self.npc_path_points[0])
                                continue
                            
                            # Handle scrolling in bill (if clicked inside area? usually wheel is better)
                            pass

                        # Handle recording button click (only if ordering mode is active)
                        if self.ordering_mode and (self.order_recording or self.order_transcribed_text):
                            if self.order_record_button and self.order_record_button.collidepoint(game_pos):
                                # Toggle recording
                                if self.order_recording:
                                    self.stop_order_recording()
                                else:
                                    self.start_order_recording()
                                continue
                                continue
                            
                            # Check recording button (if visible)
                            if self.order_record_button and self.order_record_button.collidepoint(game_pos):
                                if not self.order_recording:
                                    # Start recording
                                    self.order_recording = True
                                    self.recorder.start_recording()
                                    self.order_transcribed_text = "Recording..."
                                    print("[INFO] Started order recording")
                                else:
                                    # Stop recording and transcribe
                                    self.order_recording = False
                                    audio_file = self.recorder.stop_recording()
                                    if audio_file:
                                        def transcribe_order():
                                            self.order_transcribed_text = "Transcribing..."
                                            result = self.recorder.transcribe_audio(audio_file)
                                            
                                            # Handle tuple return (display_text, original_text)
                                            if isinstance(result, tuple):
                                                display_text, original_text = result
                                                self.order_transcribed_text = display_text
                                                # Use original text for dish detection
                                                self.handle_order_transcription(original_text)
                                            else:
                                                self.order_transcribed_text = result
                                        
                                        threading.Thread(target=transcribe_order).start()
                                    print("[INFO] Stopped order recording")
                                continue
                            
                            # Click outside closes ordering mode
                            if not (self.place_order_button.collidepoint(game_pos) or 
                                   self.checkout_button.collidepoint(game_pos) or
                                   (self.order_record_button and self.order_record_button.collidepoint(game_pos))):
                                # Click outside - close ordering interface
                                self.ordering_mode = False
                                self.order_recording = False
                                self.order_transcribed_text = ""
                                self.npc_moving = True  # Resume NPC movement
                                print("[INFO] Ordering mode closed")
                                continue
                        
                        # Check if NPC is clicked (when clickable and not in ordering mode)
                        if self.npc_clickable and not self.ordering_mode and self.npc_rect:
                            if self.npc_rect.collidepoint(game_pos):
                                # Enter ordering mode
                                self.ordering_mode = True
                                self.npc_moving = False  # Stop NPC movement
                                self.order_recording = False
                                self.order_transcribed_text = ""
                                print("[INFO] NPC clicked - entering ordering mode")
                                
                                # Play NPC greeting audio if exists
                                if NPC_ORDER_AUDIO and os.path.exists(NPC_ORDER_AUDIO):
                                    try:
                                        pygame.mixer.music.load(NPC_ORDER_AUDIO)
                                        pygame.mixer.music.play()
                                    except Exception as e:
                                        print(f"[ERROR] Failed to play NPC order audio: {e}")
                                continue
                        
                        # Check if close button is clicked (when full menu is open)
                        if self.menu_open and self.close_button_rect:
                            if self.close_button_rect.collidepoint(game_pos):
                                self.menu_open = False
                                self.menu_scroll_offset = 0  # Reset scroll when closing
                                print("[INFO] Menu closed")
                                continue  # Don't process other clicks
                        
                        # Check category button clicks (when menu is open)
                        if self.menu_open:
                            for category, btn_rect in self.menu_category_buttons.items():
                                if btn_rect.collidepoint(game_pos):
                                    self.current_category = category
                                    self.menu_scroll_offset = 0  # Reset scroll when changing category
                                    print(f"[INFO] Switched to category: {category}")
                                    continue
                            
                            # Check dish clicks (when menu is open)
                            for dish_id, dish_rect in self.dish_display_rects:
                                if dish_rect.collidepoint(game_pos):
                                    # Play dish audio
                                    if dish_id in self.dish_audio_paths:
                                        audio_path = self.dish_audio_paths[dish_id]
                                        try:
                                            pygame.mixer.music.load(audio_path)
                                            pygame.mixer.music.play()
                                            print(f"[INFO] Playing audio for dish: {dish_id}")
                                        except Exception as e:
                                            print(f"[ERROR] Failed to play audio for {dish_id}: {e}")
                                    continue
                        
                        # Check if menu icon is clicked (open full menu)
                        if self.show_menu and not self.menu_open and self.menu_icon_rect:
                            if self.menu_icon_rect.collidepoint(game_pos):
                                self.menu_open = True
                                self.current_category = "steamed"  # Default to steamed category
                                self.menu_scroll_offset = 0
                                print("[INFO] Menu opened! Player can view dishes.")
                                continue  # Don't process other clicks
                        
                        # Check play audio button (updated position)
                        play_button_rect = pygame.Rect(GAME_WIDTH - 130, 130, 90, 35)
                        if play_button_rect.collidepoint(game_pos) and self.dialogue_audio_path:
                            pygame.mixer.music.load(self.dialogue_audio_path)
                            pygame.mixer.music.play()
                        
                        # Check record button
                        if self.record_button.is_clicked(game_pos):
                            if not self.is_recording:
                                self.is_recording = True
                                self.recorder.start_recording()
                                self.transcribed_text = "Recording..."
                            else:
                                self.is_recording = False
                                audio_file = self.recorder.stop_recording()
                                if audio_file:
                                    # Transcribe in a separate thread to avoid blocking
                                    def transcribe():
                                        self.transcribed_text = "Transcribing..."
                                        # Get both display text and original text
                                        result = self.recorder.transcribe_audio(audio_file)
                                        
                                        # Handle tuple return (display_text, original_text)
                                        if isinstance(result, tuple):
                                            display_text, original_text = result
                                            self.transcribed_text = display_text
                                            
                                            # Use original Chinese text for keyword detection
                                            if self.waiting_for_tea_choice and not self.tea_selected:
                                                detected_tea = self.detect_tea_keyword(original_text)
                                                if detected_tea:
                                                    print(f"[SUCCESS] Detected tea: {detected_tea}")
                                                    self.handle_tea_selection(detected_tea)
                                                else:
                                                    print(f"[INFO] No tea keyword detected in: '{original_text}'")
                                        else:
                                            # Fallback for error messages (single string)
                                            self.transcribed_text = result
                                    
                                    threading.Thread(target=transcribe).start()
    
    def update(self):
        """Update game state"""
        # Update NPC movement
        self.update_npc_movement()
        
        # Update start button hover state (only on start screen)
        if self.state == "start" and self.start_button_image and self.start_button_rect:
            mouse_pos = pygame.mouse.get_pos()
            game_pos = self.scale_mouse_pos(mouse_pos)
            
            if game_pos:
                # Check if mouse is over the button
                self.start_button_hovered = self.start_button_rect.collidepoint(game_pos)
            else:
                self.start_button_hovered = False
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw to game surface
            if self.state == "start":
                self.draw_start_screen()
            elif self.state == "game":
                self.draw_game_screen()
            
            # Scale and draw game surface to screen with letterboxing
            self.screen.fill(BLACK)  # Black bars for letterboxing
            scaled_rect = self.get_scaled_rect()
            scaled_surface = pygame.transform.scale(self.game_surface, 
                                                    (scaled_rect.width, scaled_rect.height))
            self.screen.blit(scaled_surface, scaled_rect)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":

    game = Game()



    game.run() 