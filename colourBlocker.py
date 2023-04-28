import pygame
import pygame.font
import random
from web3 import Web3


# Frame rate control
clock = pygame.time.Clock()
fps = 120

# Connect to Infura (replace this with yours ;))
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/e45f1a1ddffd42c5bcd80a5319c0a711'))

# Initialize Pygame
pygame.init()
pygame.font.init()

# Get the screen resolution
screen_info = pygame.display.Info()
size = (screen_info.current_w, screen_info.current_h)
size_mod = size

# Create the window surface and set it to fullscreen
window = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("ColourBlocker")

# Set the initial background color
bg_color = (255, 255, 255)
bg_color2 = (0, 0, 0)
font_color = (175, 175, 175)
window.fill(bg_color)

# create font object
font = pygame.font.Font(None, 20)

# text box variable
text = None
text_rect = None

#cigawrettes contract
CONTRACT_ADDRESS = '0xEEd41d06AE195CA8f5CaCACE4cd691EE75F0683f'

# Create the contract object with the function signature for totalSupply
nft_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=[{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}])

#initialize mints
current_mints = 0

#function to get current number of mints
def get_current_number_of_mints(contract):
    try:
        current_mint_count = contract.functions.totalSupply().call()
        return current_mint_count
    except Exception as e:
        print(f"Error getting total supply: {e}")
        return None


# Function to get tx count from last block
def get_tx_count_in_latest_block():
    latest_block = w3.eth.get_block('latest')
    return len(latest_block['transactions'])

# function to get base gas
def get_gas_in_latest_block():
    latest_block = w3.eth.get_block('latest')
    return round(latest_block['baseFeePerGas']/1000000000)

# tx count variable
tx_count = get_tx_count_in_latest_block()
latest_block = w3.eth.get_block('latest')

# Function to generate random colors
def random_color():
    return (random.randint(min(tx_count, 255), 255), random.randint(min (tx_count, 255), 255), random.randint(min(tx_count, 255), 255))

# function to display block number
def display_block_number_and_mints(block_number, mints):
    global text
    global text_rect
    
    text = font.render(f'  -------->    [x]    <------------    click    to    close          :)                                             Latest Block   ---------->  {block_number}          Current Ciggy Pack ---------->  {mints}            ', True, (0, 0, 0), font_color)
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    window.blit(text, text_rect)
    pygame.display.update()

    
# Callback function for new block
def on_new_block():
    global bg_color
    global bg_color2
    global font_color

    # Fill the background with the previous circle's color
    window.fill(bg_color)

    # Generate a random circle with a random color
    circle_color = random_color()
    diameter = random.randint(100, min(size_mod))  # Choose a random diameter fitting within the window
    position = (random.randint(diameter // 2, size[0] - diameter // 2), random.randint(diameter // 2, size[1] - diameter // 2))
    pygame.draw.circle(window, circle_color, position, diameter // 2)

    # Draw a square inside the circle with the previous background color
    square_size = int(diameter * 0.7)
    square_pos = (position[0] - square_size // 2, position[1] - square_size // 2)
    pygame.draw.rect(window, bg_color2, (square_pos[0], square_pos[1], square_size, square_size))

    # Update the display
    pygame.display.update()

    # Set the background color to the current circle's color for the next iteration
    bg_color2 = bg_color
    bg_color = circle_color
    gas_color = get_gas_in_latest_block()
    font_color = (gas_color+gas_color, 175-gas_color+gas_color, 255-gas_color+gas_color)

# Run the main loop
running = True
previous_latest_block = 0
time_since_last_query = 0
query_interval = 5000 
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for mouse button up events
        elif event.type == pygame.MOUSEBUTTONUP:
            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()
            # Check if the mouse click was inside the block number's bounding rectangle
            if text_rect.collidepoint(mouse_pos):
                running = False

    # Get the current time in milliseconds
    current_time = pygame.time.get_ticks()

    # Check if it's time to query the blockchain
    if current_time - time_since_last_query > query_interval:
        # Get the number of transactions in the latest block
        latest_block = w3.eth.get_block('latest')
        tx_count = get_tx_count_in_latest_block()

        # Get the current number of cigawrette mints
        current_mints = get_current_number_of_mints(nft_contract) - 1

        # Check if the number of transactions has increased since the last check
        if latest_block['number'] > previous_latest_block:
            on_new_block()  # Trigger the new block function

        previous_latest_block = latest_block['number']
        time_since_last_query = current_time

    # Display the current block number and number of mints
    display_block_number_and_mints(latest_block['number'], current_mints)

    # Control the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
