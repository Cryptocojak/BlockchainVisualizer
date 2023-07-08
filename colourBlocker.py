## uncomment this to bypass the support prompt ##
#import os
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
from dataclasses import dataclass, field
import pygame
import pygame.font
import random
import webbrowser
from web3 import Web3

print ("\nloading.")

@dataclass
class Circle_square:
    cir_color: pygame.Color
    squ_color: pygame.Color
    posi: tuple = field(repr=True, default=(0,0))
    diam: int = field(repr=True, default=0)
    squ_size: int = field(repr=True, default=0)
    squ_pos: tuple = field(repr=True, default=(0,0))

#global variables
fps = 120
gas_price = 0
gas_price_gwei = 0
bg_color = pygame.Color(54, 74, 84)
bg_color2 = pygame.Color(14, 39, 20)


circle_color = bg_color2
historic_colours1 = bg_color
historic_colours2 = bg_color
historic_colours3 = bg_color
youngest = Circle_square(circle_color, bg_color)
last_mints = None 
mint_pack = "mint      "
b_and_w_mod = False
b_and_w_mod1 = False
button_message =    f" colour_mod [ ]"
button_message_bw = f"     B&W    [ ]"
url_opened = False  
running = True
fullscreen = True
previous_latest_block = 0
time_since_last_query = 0
query_interval = 7500
CONTRACT_ADDRESS = '0xEEd41d06AE195CA8f5CaCACE4cd691EE75F0683f' #cigawrettes contract
minting_site = f"https://mint.fun/ethereum/{CONTRACT_ADDRESS}"

print (" .     .")

# Connect to Infura  ( replace with your own key:) )
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/187ad0d7f5384a718cb62e07425df2e8'))
latest_block = w3.eth.get_block('latest')
tx_count = len(latest_block['transactions'])

print ("  .    .")

# Create the contract object with the function signature for totalSupply
nft_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=[{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}])
next_mint = (nft_contract.functions.totalSupply().call())
current_mint = next_mint - 1

print ("   .   .")

# Initialize Pygame
pygame.init()
pygame.font.init()
icon = pygame.image.load('nusainq.png')
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 16)
pygame.display.set_caption("Blockchain Visualizer")
pygame.display.set_icon(icon)
screen_info = pygame.display.Info()
size = (screen_info.current_w, screen_info.current_h)
small_window_size = (screen_info.current_w, screen_info.current_h // 2)
size_mod = size

#GET GAS PRICE and tx count
def get_gas_price():
    global gas_price
    global gas_price_gwei
    global latest_block
    global tx_count
    latest_block = w3.eth.get_block('latest')
    gas_price =  w3.eth.gas_price
    gas_price_gwei = gas_price / 1e9
    tx_count = len(latest_block['transactions'])
    return w3.eth.gas_price

# Function to generate random colors
def random_color():
    global bg_color
    global bg_color2
    global circle_color
    global b_and_w_mod
    global b_and_w_mod1
    global historic_colours1
    global historic_colours2
    global historic_colours3

    new_color_dark = pygame.Color(random.randint(min(round(gas_price_gwei), 255), 255), random.randint(min (round(gas_price_gwei), 255), 255), random.randint(min(round(gas_price_gwei), 255), 255))
    new_color_light = pygame.Color(random.randint(min(tx_count, 255), 255), random.randint(min (tx_count, 255), 255), random.randint(min(tx_count, 255), 255))
    if b_and_w_mod:
        new_color = new_color_dark
    else:
        new_color = new_color_light

    if b_and_w_mod1:
        new_color = pygame.Color.grayscale(new_color)

    historic_colours1 = historic_colours2
    historic_colours2 = historic_colours3
    historic_colours3 = bg_color2
    
    bg_color2 = bg_color
    bg_color = circle_color
    circle_color = new_color

    return new_color

def random_c1():
    tx_count_color = min(tx_count, 255)
    return pygame.Color(tx_count_color, tx_count_color, tx_count_color)

#function to get current number of mints
def get_current_number_of_mints(contract):
    global current_mint
    global next_mint

    try:
        next_mint = contract.functions.totalSupply().call()
        current_mint = next_mint - 1
        return current_mint
    except Exception as e:
        print(f"Error getting total supply: {e}")
        return None
    
def open_a_pack(which_pack):
    url = "https://opensea.io/assets/ethereum/0xeed41d06ae195ca8f5cacace4cd691ee75f0683f/{}".format(which_pack)
    webbrowser.open(url)

# function to display block number
def display_block_number_and_mints(block_number, mints):
    global text
    global text_rect
    global text1
    global text_rect1
    global text2
    global text_rect2
    global pack_text
    global pack_text_rect
    global button_message_text
    global button_message_text_rect
    global button_message_text_bw
    global button_message_text_rect_bw
    
    text = font.render(f'  -------->    [ x ]    <------------    click    to    close   [or press esc]         :)    Gas Price: {gas_price_gwei:.2f} Gwei              ^^{tx_count}^^         tx   in    the    Latest Block   ---------->  {block_number}          Current Ciggy Pack ---------->  {mints}            ', True, (0, 0, 0), bg_color)
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    window.blit(text, text_rect)

    text2 = font.render(f'  -------->    [ x ]    <------------    click    to   toggle  fullscreen   [or press 1]           ', True, (0, 0, 0), bg_color2)
    text_rect2 = text2.get_rect()
    text_rect2.topleft = (10, 30)
    window.blit(text2, text_rect2)

    text1 = font.render(f'  -------->    [ x ]    <------------    click    to    see  latest  mint             ', True, (0, 0, 0), circle_color)
    text_rect1 = text1.get_rect()
    text_rect1.topleft = (10, 50)
    window.blit(text1, text_rect1)
    
    pack_text = font.render(f"  -------->    [ x ]    <------------     {mint_pack}", True, (random_c1()), historic_colours1)
    pack_text_rect = pack_text.get_rect()
    pack_text_rect.topleft = (10, 70)
    window.blit(pack_text, pack_text_rect)

    button_message_text = font.render(f"({button_message})", True, (0,0,0), historic_colours3)
    button_message_text_rect = button_message_text.get_rect()
    button_message_text_rect.topleft = (10, 90)
    window.blit(button_message_text, button_message_text_rect)

    button_message_text_bw = font.render(f"({button_message_bw})", True, (0,0,0), historic_colours2)
    button_message_text_rect_bw = button_message_text_bw.get_rect()
    button_message_text_rect_bw.topleft = (10, 110)
    window.blit(button_message_text_bw, button_message_text_rect_bw)

def drawing_shapes():
    global old_pos
    global old_diam
    
    diameter = random.randint(100, min(size_mod))
    position = (random.randint(diameter // 2, size_mod[0] - diameter // 2), random.randint(diameter // 2, size_mod[1] - diameter // 2))
    old_pos=position
    old_diam=diameter
    pygame.draw.circle(window, circle_color, position, diameter // 2)
    square_size = int(diameter * 0.7)
    square_pos = (position[0] - square_size // 2, position[1] - square_size // 2)
    pygame.draw.rect(window, bg_color2, (square_pos[0], square_pos[1], square_size, square_size))

def drawing_shapes2():

    shapes2 = window
    shapes2.set_alpha(50)

    seethru2v= historic_colours2
    seethru2v = pygame.Color(historic_colours2[0], historic_colours2[1], historic_colours2[2], 10)

    seethru3v= historic_colours3
    seethru3v = pygame.Color(historic_colours3[0], historic_colours3[1], historic_colours3[2], 0, )
    
    diameter = random.randint(100, old_diam)  # Choose a random diameter fitting within the window
    position2 = (random.randint((old_pos[0]-(old_diam)),size_mod[0] - diameter // 2) , random.randint((old_pos[1]-old_diam), size_mod[1]- diameter //2 ))
    #pygame.draw.arc(shapes2, historic_colours1, (position2, ((size_mod[0]), (size_mod[1]))), diameter // 2, size_mod[1], 3)
    square_size = int(diameter * 0.7)
    square_pos = (position2[0] - square_size // 2, position2[1] - square_size // 2)
    pygame.draw.ellipse(shapes2, seethru3v, [(square_pos), (square_size, square_size)], 3)
    pygame.draw.polygon(shapes2, seethru2v, [(diameter, old_diam), (square_size, square_size), position2])

def colour_bool():
    global b_and_w_mod
    global button_message
    b_and_w_mod = not b_and_w_mod
    if b_and_w_mod:
        button_message=f" colour_mod [x]"
    else:
        button_message=f" colour_mod [ ]"

def greyscale_bool():
    global b_and_w_mod1
    global button_message_bw
    b_and_w_mod1 = not b_and_w_mod1
    if b_and_w_mod1:
        button_message_bw=f" B&W [x]"
    else:
        button_message_bw=f" B&W [ ]"
    
print ("    .  .\n     . .")
# Callback function for new block
def on_new_block():
    get_gas_price()
    get_current_number_of_mints(nft_contract)
    random_color()
    window.fill(bg_color)
    drawing_shapes()
    drawing_shapes2()
    display_block_number_and_mints(latest_block['number'], current_mint)
    pygame.display.update()

def fullscreen_func():
    global size_mod
    pygame.display.set_mode(size, pygame.FULLSCREEN)
    size_mod = size
    on_new_block()

def minimized():
    global size_mod
    pygame.display.set_mode(small_window_size)
    size_mod = small_window_size
    on_new_block()

print("      🦐loaded :)")
window = pygame.display.set_mode(size, pygame.FULLSCREEN)
on_new_block()

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

            if text_rect1.collidepoint(mouse_pos):
                open_a_pack(current_mint)

            if text_rect2.collidepoint(mouse_pos):
                fullscreen = not fullscreen
                if fullscreen:
                    fullscreen_func()
                else:
                    minimized()

            if pack_text_rect.collidepoint(mouse_pos):
                    webbrowser.open(minting_site)

            if button_message_text_rect.collidepoint(mouse_pos):
                colour_bool()
                i=0
                while i < 5:
                    random_color()
                    i+=1
                on_new_block()

            if button_message_text_rect_bw.collidepoint(mouse_pos):
                greyscale_bool()
                i=0
                while i < 5:
                    random_color()
                    i+=1
                on_new_block()
        #Key events           
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_1:
                fullscreen = not fullscreen
                if fullscreen:
                    fullscreen_func()
                else:
                    minimized()

            if event.key == pygame.K_BACKQUOTE:
                on_new_block()

    # Get the current time in milliseconds
    current_time = pygame.time.get_ticks()

    # Check if it's time to query the blockchain
    if current_time - time_since_last_query > query_interval:
        # Get the number of transactions in the latest block
        latest_block = w3.eth.get_block('latest')
        
        # Check if the number of transactions has increased since the last check
        if latest_block['number'] > previous_latest_block:
            on_new_block()  # Trigger the new block function
             
        previous_latest_block = latest_block['number']
        time_since_last_query = current_time

    # Control the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
