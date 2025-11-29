# Cantonese Dim Sum Ordering Game

An interactive educational game designed to help players learn and practice ordering Dim Sum in Cantonese. Players interact with a virtual waiter, explore a menu of authentic dishes, and use voice commands to place orders, simulating a real-world "Yum Cha" experience.

## Features

*   **Interactive Environment**: Sit at a table in a virtual canteen and interact with an animated NPC waiter.
*   **Voice Recognition**: Use your microphone to order tea and dishes using Cantonese keywords.
*   **Authentic Menu**: Explore various Dim Sum categories (Steamed, Fried, Congee/Veg) with images and audio pronunciations.
*   **Ordering System**: 
    *   **Tea Selection**: Choose from popular teas like Tieguanyin, Jasmine (Xiangpian), Pu-erh, and Black tea.
    *   **Dish Ordering**: Record your voice to order multiple dishes at once.
*   **Shopping Cart & Bill**: Track your ordered items and view a detailed bill with prices upon checkout.
*   **Visual Feedback**: Animated NPC movements, dynamic dialogue boxes, and responsive UI elements.

## Prerequisites

*   Python 3.8 or higher
*   Internet connection (required for Google Speech Recognition)
*   Microphone

## Installation

1.  **Clone the repository** or download the source code.

2.  **Install the required Python libraries**:
    Open your terminal or command prompt and run:
    ```bash
    pip install pygame sounddevice soundfile SpeechRecognition numpy Pillow
    ```

    *Note: `sounddevice` requires PortAudio. On Windows, it usually comes bundled. On Linux/macOS, you might need to install it separately (e.g., `sudo apt-get install libportaudio2`).*

## How to Play

1.  **Start the Game**: Run the `yum_cha_game.py` script.
    ```bash
    python yum_cha_game.py
    ```
2.  **Enter the Canteen**: Click the **Start Learning** button on the main screen.
3.  **Find a Seat**: Click on the table to sit down.
4.  **Order Tea**: 
    *   The waiter will approach and ask for your tea preference.
    *   Use the recording interface to say the name of the tea you want (e.g., "Pu-erh", "Tieguanyin").
    *   *Tip: You have 15 seconds to make a choice!*
5.  **Browse the Menu**: 
    *   Click the **Menu** icon on the table to open the full menu.
    *   Click on dish images to hear their Cantonese pronunciation.
    *   Switch between categories (Steamed, Fried, Congee) using the tabs on the left.
6.  **Place Your Order**:
    *   Click on the **NPC** (waiter) to open the ordering interface.
    *   Click **Place Order**.
    *   Click **Start Recording** and say the names of the dishes you want to eat.
    *   Click **Stop Recording** to submit your order. The game will transcribe your speech and add detected items to your cart.
7.  **Check Out**:
    *   When you are finished, click the **NPC** and select **Check Out**.
    *   Review your bill, which lists all ordered items and the total price.
    *   Click **Back to Home** to return to the start screen.

## Controls

*   **Mouse**: Used for all interactions (clicking buttons, selecting menu items, moving the character/camera if applicable).
*   **Microphone**: Used for voice commands during the ordering phases.
*   **F11**: Toggle Fullscreen mode.
*   **Mouse Wheel**: Scroll through the menu, shopping cart, and bill.

## Project Structure

*   `testing_gamecode.py`: The main game script containing all logic.
*   `temp png file/`: Directory containing image assets (UI, sprites, backgrounds).
*   `audio file/`: Directory containing audio assets (dialogue, dish names).

## Troubleshooting

*   **Microphone issues**: Ensure your default recording device is set correctly in your OS settings.
*   **Speech Recognition errors**: Ensure you have a stable internet connection as the game uses Google's online speech recognition API.
*   **Asset errors**: If the game crashes on startup, ensure all image and audio files are present in their respective directories as defined in the configuration section of the code.

## Credits

Created for the Creative Programming Group Project.
