import win32api
import win32con
import win32gui
from KleeClass import *
import math
# import os

# ----------------------------------------------------------------------------------------------------------------------
# os.makedirs("C:/Users/"+win32api.GetUserName()+"/Desktop/OK")
# print(win32gui.GetIconInfo(hicon))

pygame.init()
clock = pygame.time.Clock()

window_width, window_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

screen = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
# main loop state
done = False

# Transparency color
fuchsia = (255, 0, 128)

information_screen = True

# Create layered window
hwnd = pygame.display.get_wm_info()['window']
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

# taskbar size
task_bar = window_height - win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))['Work'][3]

font = pygame.font.SysFont("cambria", 30)
line1 = font.render("Press 'Space' to start", True, (0, 0, 0))
line2 = font.render("ctrl+k stops the program", True, (0, 0, 0))
line3 = font.render("feel free to drag her around", True, (0, 0, 0))
# print(pygame.font.get_fonts())
# ----------------------------------------------------------------------------------------------------------------------
# create main character and load animations

Klee = Klee(window_width + 100, window_height - 82 - task_bar)
# Klee = Klee(window_width / 2, window_height - 82 - task_bar)
klee = pygame.sprite.Group()
klee.add(Klee)
Klee.add_animation("throw", "./sprites/klee_throw.png", 1)
Klee.add_animation("walk", "./sprites/klee_walk_v3.png", 12)
Klee.add_animation("catch", "./sprites/klee_catch.png", 5)
Klee.add_animation("catch_walk", "./sprites/klee_catch_walk.png", 12)
decision_delay = 100 * 60
decision_timer = pygame.time.get_ticks() + decision_delay
decision = 15

# ----------------------------------------------------------------------------------------------------------------------
# main loop
while not done:

    # events loop
    for event in pygame.event.get():
        if win32api.GetAsyncKeyState(win32con.VK_LCONTROL) and win32api.GetAsyncKeyState(ord('K')):
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if Klee.rect.collidepoint(pygame.mouse.get_pos()) and not Klee.drag:
                Klee.drag = True
            if decision_timer < pygame.time.get_ticks():
                decision_timer += decision_delay
        if not win32api.GetAsyncKeyState(win32con.VK_LBUTTON):
            Klee.drag = False
        if win32api.GetAsyncKeyState(win32con.VK_SPACE):
            information_screen = False

    if not information_screen:

        # dragging main character
        if Klee.drag:
            Klee.directionVector = win32gui.GetCursorInfo()[2][0] - Klee.rect.x - Klee.rect.width / 2, \
                                   win32gui.GetCursorInfo()[2][1] - Klee.rect.y - Klee.rect.height / 2
            Klee.rect.x += int(Klee.directionVector[0] / 10)
            Klee.rect.y += int(Klee.directionVector[1] / 10)
            if Klee.directionVector[0] < 0:
                Klee.next_frame('right', 200, 'throw')
            if Klee.directionVector[0] > 0:
                Klee.next_frame('left', 200, 'throw')

        # dropped main character
        elif not Klee.drag and math.sqrt(
                math.pow(Klee.directionVector[0], 2) + math.pow(Klee.directionVector[1], 2)) > 0:
            Klee.directionVector = Klee.directionVector[0], Klee.directionVector[1] + 20.0
            if (Klee.rect.y + Klee.rect.height) > (window_height - task_bar):
                Klee.directionVector = Klee.directionVector[0]/5, math.floor(Klee.directionVector[1] * -0.5)
            if Klee.rect.x < 0 or Klee.rect.x > (window_width - Klee.rect.width):
                Klee.directionVector = Klee.directionVector[0] * -1, Klee.directionVector[1]
            if Klee.directionVector[0] < 0:
                Klee.next_frame('right', 200, 'throw')
            if Klee.directionVector[0] > 0:
                Klee.next_frame('left', 200, 'throw')
            if math.sqrt(math.pow(Klee.directionVector[0], 2) + math.pow(Klee.directionVector[1], 2)) < 5:
                Klee.rect.y = window_height - Klee.rect.height + 4 - task_bar
                Klee.directionVector = 0, 0
            Klee.rect.x += int(Klee.directionVector[0] / 10)
            Klee.rect.y += int(Klee.directionVector[1] / 10)

        # decisions and walking
        else:
            if decision_timer < pygame.time.get_ticks():
                decision_timer += decision_delay
                decision = Klee.action()

            if decision <= 14:
                Klee.next_frame('front', 150, 'idle')
            elif 14 < decision <= 16:
                if Klee.rect.x < -200:
                    decision = 17
                    decision_timer += decision_delay
                else:
                    Klee.next_frame('left', 20, 'walk')
            elif 16 < decision <= 18:
                if Klee.rect.x > window_width + 136:
                    decision = 15
                    decision_timer += decision_delay
                else:
                    Klee.next_frame('right', 20, 'walk')
            elif 18 < decision:
                r = Klee.distance_to_from_center(win32gui.GetCursorPos())
                if r < 100:
                    if decision < 19:
                        Klee.next_frame('left', 20, 'catch_walk')
                        win32api.SetCursorPos((Klee.rect.x + 20, Klee.rect.y + math.floor(Klee.rect.height / 2)))
                        if Klee.rect.x <= 0:
                            decision = 19.5
                        else:
                            Klee.rect.x -= 3
                    else:
                        Klee.next_frame('right', 20, 'catch_walk')
                        win32api.SetCursorPos((Klee.rect.x + math.floor(Klee.rect.width / 2),
                                               Klee.rect.y + math.floor(Klee.rect.height / 2)))
                        if Klee.rect.x + Klee.rect.width >= window_width:
                            decision = 18.5
                        else:
                            Klee.rect.x += 3
                else:
                    decision = Klee.action()

        # Transparent background
        screen.fill(fuchsia)

        klee.draw(screen)

        # window always on top
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, -1, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOREPOSITION)

    else:
        screen.fill(fuchsia)
        pygame.draw.rect(screen, (255, 204, 204), (window_width / 2 - 600, window_height / 2 - 150, 1200, 260))
        screen.blit(line1, (window_width / 2 - line1.get_width() / 2, window_height / 2 - 120))
        screen.blit(line2, (window_width / 2 - line2.get_width() / 2, window_height / 2 - 50))
        screen.blit(line3, (window_width / 2 - line3.get_width() / 2, window_height / 2 + 20))

    # print(os.listdir("C:/Users/"+win32api.GetUserName()+"/Desktop"))
    pygame.display.update()
    clock.tick(60)
