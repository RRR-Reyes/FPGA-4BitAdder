# IMPORTS & INITIAL SETUP
import pygame, os, sys

pygame.init()
screen = pygame.display.set_mode((1040, 800))
pygame.display.set_caption("4-bit adder")

# IMAGE LOADING - Load background and switch/LED images
bg  = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets", "FPGAB.png")), (1040, 800)) # FPGA Board
su  = pygame.image.load(os.path.join("assets", "su.png"))    # switch up
sd  = pygame.image.load(os.path.join("assets", "sd.png"))    # switch down
led = pygame.image.load(os.path.join("assets", "ledon.png")) # LED on

# HEX DIGIT IMAGES (0–F) IN DICTIONARY
hexsurf = {}

# Digits 0–9
for i in range(10):
    hexsurf[i] = pygame.image.load(os.path.join("assets", f"{i}.png"))

# Letters A–F
letters = ["A", "b", "C", "d", "E", "F"]
for i, letter in enumerate(letters, start=10):
    hexsurf[i] = pygame.image.load(os.path.join("assets", f"{letter}.png"))


# IMAGE POSITIONS ON THE BOARD
SW_POS  = {9:(521,649), 8:(566,649), 7:(610,650), 6:(657,649),
           5:(703,649), 4:(749,650), 3:(794,649), 2:(838,649),
           1:(884,648), 0:(928,648)}

LED_POS = {9:(528,614), 8:(572,614), 7:(617,614), 6:(661,614),
           5:(705,613), 4:(750,613), 3:(795,613), 2:(839,614),
           1:(884,614), 0:(928,614)}

HEX_POS = {'HEX5':(68,618), 'HEX4':(140,619), 'HEX3':(221,619),
           'HEX2':(293,620), 'HEX1':(372,618), 'HEX0':(444,618)}


# Each switch (0–9) starts OFF (False)
switch = {i: False for i in range(10)}

# Logic Function – Get Value from Switches
def get_value(sw_list):
    value = 0
    for i, sw in enumerate(sw_list):
        if switch[sw]:                # Switch ON => Calculate Bit
            bit_value = 2 ** (3 - i)  # i = index, determines bit position
            value += bit_value
    return value                      # Switch OFF => Return 0 

clock = pygame.time.Clock()

# Main Loop
while True:

    # User Input - Window Close OR Click Switch
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.MOUSEBUTTONDOWN:
            for sw, (x, y) in SW_POS.items():
                rect = pygame.Rect(x, y, su.get_width(), su.get_height())
                if rect.collidepoint(e.pos):
                    switch[sw] = not switch[sw]  # toggle switch on click

    # CALCULATIONS
    a = get_value([9, 8, 7, 6])  # Switch: 9876
    b = get_value([3, 2, 1, 0])  # Switch: 3210
    s = a + b                    # sum of 4-bit Switches

    # Image Updating
    screen.blit(bg, (0, 0))  # draw background

    # Draw switches and LEDs
    for sw, pos in SW_POS.items():
        screen.blit(su if switch[sw] else sd, pos)

        # SWITCH ON => LED ON
        #if switch[sw]:
        #    screen.blit(led, LED_POS[sw])

    # LED always ON
    #for pos in LED_POS.values():
        #screen.blit(led, pos)

    # Draw hexadecimal displays
    screen.blit(hexsurf[a],        HEX_POS['HEX4'])
    screen.blit(hexsurf[b],        HEX_POS['HEX2'])
    screen.blit(hexsurf[s & 0xF],  HEX_POS['HEX0'])  # Result - last 4 bits of the sum
    screen.blit(hexsurf[s >> 4],   HEX_POS['HEX1'])  # Carry Over - Return remaining bits after shifting 4 bits right

    pygame.display.flip()  # refresh screen
    clock.tick(30)         # 30 frames per second
