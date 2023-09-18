import pygame

white = (255,255,255)
black = (0,0,0)
aqua = (0,255,255)

#obrazce - 1 = O, 0 = X
paw = [[0,0,0,1,0,1,0,0,0],[0,1,0,1,0,1,0,1,0],[0,1,0,0,0,0,0,1,0],[0,0,0,1,1,1,0,0,0],[0,0,1,1,1,1,1,0,0],[0,1,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,1,0],[0,0,1,1,0,1,1,0,0],[0,0,0,0,0,0,0,0,0]]
star = [[0,0,0,0,1,0,0,0,0],[0,0,0,1,1,1,0,0,0],[0,0,0,1,1,1,0,0,0],[1,1,1,1,1,1,1,1,1],[0,1,1,1,1,1,1,1,0],[0,0,1,1,1,1,1,0,0],[0,0,1,1,1,1,1,0,0],[0,1,1,1,0,1,1,1,0],[0,1,1,0,0,0,1,1,0]]
heart = [[0,0,1,1,0,1,1,0,0],[0,1,1,1,1,1,1,1,0],[1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1],[0,1,1,1,1,1,1,1,0],[0,0,1,1,1,1,1,0,0],[0,0,0,1,1,1,0,0,0],[0,0,0,0,1,0,0,0,0]]
cat = [[0,0,1,0,0,0,1,0,0],[0,1,0,1,0,1,0,1,0],[0,1,0,0,1,0,0,1,0],[1,0,1,1,0,1,1,0,1],[0,0,0,0,0,0,0,0,0],[1,1,0,1,1,1,0,1,1],[0,0,1,0,1,0,1,0,0],[1,1,0,1,0,1,0,1,1],[0,0,0,1,1,1,0,0,0]]
king = [[0,1,0,1,0,1,0,1,0],[0,1,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,1,0],[0,1,0,0,0,0,0,1,0],[0,1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1,0],[0,1,0,0,0,0,0,1,0],[0,0,1,0,0,0,1,0,0],[0,0,0,1,1,1,0,0,0]]

#kontrolni obrazec
user = []

pygame.init()
screen = pygame.display.set_mode((400,400))

font1 = pygame.font.Font(None, 36)      #menu
font2 = pygame.font.Font(None, 30)      #cisla na okrajich
font3 = pygame.font.Font(None, 75)      #prepinaci tlacitka

#herni obrazovky
menu = 0
game = 1
check = 2
solution = 3
current_state = menu

pattern = user
fill = True

def draw_menu():
    pygame.display.set_caption('NONOGRAM')
    screen.fill(white)

    #vykresli 5 tlacitek pro vyber obrazce
    for i in range(5):
        button = pygame.Rect(100, 35+i*70, 200, 50)
        pygame.draw.rect(screen, aqua, button)

    #popis tlacitek
    obrazce = ['PAW', 'STAR', 'HEART', 'CAT', 'KING']
    for i in range(len(obrazce)):
        text = font1.render(obrazce[i], True, black)
        screen.blit(text,(200 - text.get_width()/2 ,50 + i*70))

def draw_game(numbers):
    screen.fill(white)

    #tlacitka - zpet a prepinani pro vyplnene a prazdne pole
    button_back = pygame.Rect(10, 10, 110, 50)
    button_O = pygame.Rect(10, 70, 50, 50)
    button_X = pygame.Rect(70, 70, 50, 50)

    pygame.draw.rect(screen, aqua, button_back)
    pygame.draw.rect(screen, aqua, button_O)
    pygame.draw.rect(screen, aqua, button_X)

    text_back = font1.render('MENU', True, black)
    text_O = font3.render('O', True, black)
    text_X = font3.render('X', True, black)

    screen.blit(text_back, (65 - text_back.get_width()/2 , 35 - text_back.get_height()/2))
    screen.blit(text_O, (35 - text_O.get_width()/2, 97 - text_O.get_height()/2))
    screen.blit(text_X, (95 - text_X.get_width()/2, 98 - text_X.get_height()/2))

    #mrizka - 9x9, levy horni roh (125,125), rozmery bunky 30x30
    for x in range(125, 400, 30):
        pygame.draw.line(screen, aqua, (x,10), (x,395))
    for y in range(125, 400, 30):
        pygame.draw.line(screen, aqua, (10,y), (395,y))

    #tlacitko pro kontrolu
    button_check = pygame.Rect(305, 10, 90, 30)
    text_check = font2.render('CHECK', True, black)
    pygame.draw.rect(screen, aqua, button_check)
    screen.blit(text_check, (315,15))

    #cisla pro vybrany obrazec - 9 radku, 9 sloupcu
    start_y = 130
    for i in range(9):
        width = sum([font2.render(' ' + str(number), True, black).get_width() for number in numbers[i]])
        start_x = 115 - width
        for number in numbers[i]:
            text = font2.render(' ' + str(number), True, black)
            screen.blit(text, (start_x, start_y))
            start_x += text.get_width()
        start_y += 30

    start_x = 135
    for i in range(9,18):
        height = sum([font2.render(str(number), True, black).get_height() for number in numbers[i]])
        start_y = 120 - height
        for number in numbers[i]:
            text = font2.render(str(number), True, black)
            screen.blit(text, (start_x, start_y))
            start_y += text.get_height()
        start_x += 30

def draw_table(correct):
    screen.fill(white)

    #tlacitka menu a konec
    button_menu = pygame.Rect(100, 210, 200, 50)
    button_quit = pygame.Rect(100, 285, 200, 50)
    text_menu = font1.render('MENU', True, black)
    text_quit = font1.render('QUIT', True, black)
    pygame.draw.rect(screen, aqua, button_menu)
    pygame.draw.rect(screen, aqua, button_quit)
    screen.blit(text_menu, (200 - text_menu.get_width()/2, 235 - text_menu.get_height()/2))
    screen.blit(text_quit, (200 - text_quit.get_width()/2, 310 - text_quit.get_height()/2))
    
    #reseni je spravne
    if correct:
        text_correct = font1.render('CORRECT!', True, black)
        text_again = font1.render("Let's try another nonogram!", True, black)
        screen.blit(text_correct, (200 - text_correct.get_width()/2, 85 - text_correct.get_height()/2))
        screen.blit(text_again, (200 - text_again.get_width()/2, 150 - text_again.get_height()/2))

    #reseni je spatne - navic tlacitko pro zobrazeni spravneho reseni
    else:
        text_mistake = font1.render('There is a mistake!', True, black)
        text_solution = font1.render('Show correct solution', True, black)
        button_solution = pygame.Rect(50, 120, 300, 70)
        pygame.draw.rect(screen, aqua, button_solution)
        screen.blit(text_mistake, (200 - text_mistake.get_width()/2, 85 - text_mistake.get_height()/2))
        screen.blit(text_solution, (200 - text_solution.get_width()/2, 155 - text_solution.get_height()/2))

def numbers(pattern):
    numbers = []

    #radky
    for i in range(len(pattern)):
        row = pattern[i]
        row_numbers = []
        number = 0
        for j in range(len(row)):
            if row[j] == 1:
                number += 1
            if (row[j] == 0 and number > 0) or (j+1 == len(row) and number > 0):
                row_numbers.append(number)
                number = 0
        numbers.append(row_numbers)

    #sloupce
    for i in range(len(pattern)):
        col_numbers = []
        number = 0
        for j in range(len(pattern)):
            if pattern[j][i] == 1:
                number += 1
            if (pattern[j][i] == 0 and number > 0) or (j+1 == len(pattern) and number > 0):
                col_numbers.append(number)
                number = 0
        numbers.append(col_numbers)

    return numbers

def show_solution(pattern):
    screen.fill(white)

    #mrizka uprostred
    for x in range(65, 340, 30):
        pygame.draw.line(screen, aqua, (x,65), (x,335))
    for y in range(65, 340, 30):
        pygame.draw.line(screen, aqua, (65,y), (335,y))

    #vykresleni obrazce
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            if pattern[j][i] == 1:
                x = 65 + i*30
                y = 65 + j*30
                cell = pygame.Rect(x, y, 30, 30)
                pygame.draw.rect(screen, black, cell)

    #nadpis
    title = font1.render('CORRECT SOLUTION:', True, black)
    screen.blit(title, (200 - title.get_width()/2, 30))

    #tlacitka
    button_menu = pygame.Rect(90, 342, 100, 50)
    button_quit = pygame.Rect(210, 342, 100, 50)
    text_menu = font1.render('MENU', True, black)
    text_quit = font1.render('QUIT', True, black)
    pygame.draw.rect(screen, aqua, button_menu)
    pygame.draw.rect(screen, aqua, button_quit)
    screen.blit(text_menu, (140 - text_menu.get_width()/2, 367 - text_menu.get_height()/2))
    screen.blit(text_quit, (260 - text_quit.get_width()/2, 367 - text_quit.get_height()/2))

def new_game():
    new = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    return new


running = True
draw_menu()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x,y = pygame.mouse.get_pos()

            #vyber obrazce
            if current_state == menu:
                if 100 < x < 300:
                    if 35 < y < 85:
                        current_state = game
                        pattern = paw
                        user = new_game()
                        draw_game(numbers(paw))
                        pygame.display.set_caption('NONOGRAM - PAW')
                    elif 105 < y < 155:
                        current_state = game
                        pattern = star
                        user = new_game()
                        draw_game(numbers(star))
                        pygame.display.set_caption('NONOGRAM - STAR')
                    elif 175 < y < 225:
                        current_state = game
                        pattern = heart
                        user = new_game()
                        draw_game(numbers(heart))
                        pygame.display.set_caption('NONOGRAM - HEART')
                    elif 245 < y < 295:
                        current_state = game
                        pattern = cat
                        user = new_game()
                        draw_game(numbers(cat))
                        pygame.display.set_caption('NONOGRAM - CAT')
                    elif 315 < y < 365:
                        current_state = game
                        pattern = king
                        user = new_game()
                        draw_game(numbers(king))
                        pygame.display.set_caption('NONOGRAM - KING')

            elif current_state == game:
                #tlacitka
                if 10 < x < 120 and 10 < y < 60:
                    current_state = menu
                    draw_menu()
                elif 10 < x < 60 and 70 < y < 120:
                    fill = True
                elif 70 < x < 120 and 70 < y < 120:
                    fill = False
                elif 305 < x < 395 and 10 < y < 35:
                    current_state = check
                    draw_table(pattern == user)

                #mrizka
                if 125 < x < 395 and 125 < y < 395:
                    #prepocet souradnic leveho horniho rohu bunky, do ktere uzivatel kliknul
                    x = x - (x-125) % 30
                    y = y - (y-125) % 30
                    cell = pygame.Rect(x, y, 30, 30)

                    #souradnice bunky v mrizce
                    grid_y = (x-125) // 30
                    grid_x = (y-125) // 30

                    #vyplneni bunky
                    if fill:
                        pygame.draw.rect(screen, black, cell)
                        user[grid_x][grid_y] = 1

                    #oznaceni prazdne bunky
                    else:
                        pygame.draw.rect(screen, white, cell)
                        pygame.draw.line(screen, aqua, (x,y), (x+30,y+30), 2)
                        pygame.draw.line(screen, aqua, (x+30,y), (x,y+30), 2)
                        user[grid_x][grid_y] = 0

            elif current_state == check:
                #tlacitka menu a quit
                if 100 < x < 300:
                    if 210 < y < 260:
                        current_state = menu
                        draw_menu()
                    elif 285 < y < 335:
                        running = False

                #zobrazeni spravneho reseni
                if not pattern == user and 50 < x < 350 and 120 < y < 190:
                    current_state = solution
                    show_solution(pattern)

            elif current_state == solution:
                if 342 < y < 392:
                    if 90 < x < 190:
                        current_state = menu
                        draw_menu()
                    elif 210 < x < 310:
                        running = False

    pygame.display.update()

pygame.quit()
