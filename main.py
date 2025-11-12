import pygame, os, sys

pygame.init()
screen = pygame.display.set_mode((1040, 800))
pygame.display.set_caption("4-bit adder")

# Load images
bg  = pygame.transform.smoothscale(
    pygame.image.load(os.path.join("assets", "FPGAB.png")), (1040, 800))
su  = pygame.image.load(os.path.join("assets", "su.png"))
sd  = pygame.image.load(os.path.join("assets", "sd.png"))
led = pygame.image.load(os.path.join("assets", "ledon.png"))

hexsurf = {}
for n in range(10):
    hexsurf[n] = pygame.image.load(os.path.join("assets", f"{n}.png"))
for let, file in ((10,"A.png"), (11,"b.png"), (12,"C.png"),
                  (13,"d.png"), (14,"E.png"), (15,"F.png")):
    hexsurf[let] = pygame.image.load(os.path.join("assets", file))

# Positions (original X-axis, -52 pixels on Y-axis)
SW_POS  = {9:(521,649), 8:(566,649), 7:(610,650), 6:(657,649),
           5:(703,649), 4:(749,650), 3:(794,649), 2:(838,649),
           1:(884,648), 0:(928,648)}
LED_POS = {9:(528,614), 8:(572,614), 7:(617,614), 6:(661,614),
           5:(705,613), 4:(750,613), 3:(795,613), 2:(839,614),
           1:(884,614), 0:(928,614)}
HEX_POS = {'HEX5':(68,618), 'HEX4':(140,619), 'HEX3':(221,619),
           'HEX2':(293,620), 'HEX1':(372,618), 'HEX0':(444,618)}

switch = {i:False for i in range(10)}

def get_value(sw_list):
    return sum(1<<(3-i) for i,sw in enumerate(sw_list) if switch[sw])

clock = pygame.time.Clock()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            for sw, (x,y) in SW_POS.items():
                if pygame.Rect(x, y, su.get_width(), su.get_height()).collidepoint(e.pos):
                    switch[sw] = not switch[sw]

    a = get_value([9,8,7,6])
    b = get_value([3,2,1,0])
    s = a + b

    screen.blit(bg, (0,0))
    for sw, pos in SW_POS.items():
        screen.blit(su if switch[sw] else sd, pos)
        if switch[sw]:
            screen.blit(led, LED_POS[sw])

    screen.blit(hexsurf[a],      HEX_POS['HEX4'])
    screen.blit(hexsurf[b],      HEX_POS['HEX2'])
    screen.blit(hexsurf[s & 0xF], HEX_POS['HEX0'])
    screen.blit(hexsurf[s >> 4],  HEX_POS['HEX1'])

    pygame.display.flip()
    clock.tick(30)