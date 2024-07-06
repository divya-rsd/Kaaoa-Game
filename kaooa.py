import pygame
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kaooa Game")

WHITE =(0, 0, 0)    # crow
BLACK =    (255, 255, 255) # board
RED =  (201, 94, 94)   # normal (219, 93, 131) 
GREEN = (100, 149, 237) # vulture
WIN = (255, 0, 0)

points = []
inner_points = []    
crow_circles = set()  # Keep track of clicked circles
vulture_point = None  # the previous point of vulture
vulture_number = 0    # number to the point in which vulture there
circle_numbers = {}   # dictionary for numbers(value) and points(key)
number_colors = {}    # dictionary for numbers(key) and colours(value)
index = 1         
death=0               # number of deaths to make vulture win
crow_turn = True      
vulture_turn = False
crow_count = 0          #number of crows placed on board(doesnt include deaths)
selected_crow = False   # after all crows have been placed, variable for moving a crow
selected_crow_num = 0
game_over = False   
running = True
clicked_circle = None  # Define clicked_circle outside the event loop

font = pygame.font.Font(None, 36)

def winning_condition():
    global death,running
    if death >= 4:
        invalid_text = font.render("Vulture Wins", True, WIN)
        invalid_rect = invalid_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(invalid_text, invalid_rect)
        pygame.display.flip() 
        pygame.time.wait(2000)
        running = False
    return


def draw_star_with_circles(size):                       # Function to draw a star
    
    for i in range(5):
        angle = math.radians(i * 72 - 90)
        x = size * math.cos(angle) + WIDTH / 2
        y = size * math.sin(angle) + HEIGHT / 2
        points.append((x, y))
        inner_angle = math.radians((i * 72 - 90) + 36)  # Adjust angle for inner vertices
        x = (size / 2) * math.cos(inner_angle) + WIDTH / 2
        y = (size / 2) * math.sin(inner_angle) + HEIGHT / 2
        points.append((x, y))
        inner_points.append((x, y))
        
    pygame.draw.lines(screen, WHITE, True, points, 2)         # Join the dots with lines
    pygame.draw.lines(screen, WHITE, True, inner_points, 2)   # Connect inner circles to form a pentagon

    for point in points:     # Draw circles after drawing the lines
        if point in crow_circles: 
            color = WHITE
        elif point == vulture_point:
            color = GREEN
        else :
            color = RED
        pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), 20)
        
    for point in inner_points:
        if point in crow_circles: 
            color = WHITE
        elif point == vulture_point:
            color = GREEN
        else :
            color = RED
        pygame.draw.circle(screen, color, (int(point[0]), int(point[1])), 20)
    
    font = pygame.font.Font(None, 24)
    for point, number in circle_numbers.items():
        text = font.render(str(number), True, BLACK)
        text_rect = text.get_rect(center=(int(point[0]), int(point[1])))
        screen.blit(text, text_rect)

    circle_radius = 20
    circle_spacing = 5
    circle_x = WIDTH // 2 + 250 
    circle_y = HEIGHT // 2  - 150

    if not vulture_point:
        pygame.draw.circle(screen, GREEN, (circle_x, circle_y), circle_radius)    # representing vulture before making 1st move
        circle_y += (circle_radius * 2) + circle_spacing
        
    for _ in range(7-crow_count):
        pygame.draw.circle(screen, WHITE, (circle_x, circle_y), circle_radius)    # represetn crow coins left to use
        circle_y += (circle_radius * 2) + circle_spacing

    death_font = pygame.font.Font(None, 24)
    circle_x = circle_radius * 2 
    circle_y = HEIGHT // 2 - 100 
    for i in range(death):                                         # represent killed crows
        pygame.draw.circle(screen, WHITE, (circle_x, circle_y), circle_radius)
        death_text = death_font.render(str(i + 1), True, GREEN)   # i + 1 because the numbering starts from 1
        text_rect = death_text.get_rect(center=(circle_x, circle_y))
        screen.blit(death_text, text_rect)
        circle_y += (circle_radius * 2) + circle_spacing
                
def assign_numbers():           # unique numbers to token positions
    index = 1
    for point in points:
        if point not in circle_numbers:
         circle_numbers[point] = index
         number_colors[index] = "R"
         index = index+1
    
    for point in inner_points:
        if point not in circle_numbers:
         circle_numbers[point] = index
         number_colors[index] = "R"
         index = index+1
         
    return
  
draw_star_with_circles(150)
assign_numbers()  

def print_errormove():
    invalid_text = font.render("Invalid move", True, WIN)
    invalid_rect = invalid_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(invalid_text, invalid_rect)
    pygame.display.flip() 
    pygame.time.wait(1000)
    return 

def kill_n_move_vulture(point,num):
    global number_colors,crow_circles,vulture_number,vulture_turn,vulture_point,crow_turn,death
    remove_point = get_key_from_value(circle_numbers,num)
    number_colors[num] = 'R'
    number_colors[vulture_number] = 'R'
    crow_circles.remove(remove_point)
    number_colors[circle_numbers[point]] = "G"  
    vulture_point = point 
    vulture_number = circle_numbers[point]
    vulture_turn = False
    crow_turn = True
    death+=1
    return

player_font = pygame.font.Font(None, 36)

def draw_players():
    player1_text = player_font.render("Player 1", True, WHITE)
    player2_text = player_font.render("Player 2", True, WHITE)

    player1_rect = player1_text.get_rect(midbottom=(WIDTH // 4, HEIGHT - 10))
    player2_rect = player2_text.get_rect(midbottom=(WIDTH * 3 // 4, HEIGHT - 10))

    if crow_turn:
        player1_text = player_font.render("Player 1", True, WIN)
    elif vulture_turn:
        player2_text = player_font.render("Player 2", True, WIN)

    screen.blit(player1_text, player1_rect)
    screen.blit(player2_text, player2_rect)


def get_key_from_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None 

def crow_winning_print():
    global running
    invalid_text = font.render("Crow Wins! GAME OVER", True, WIN)
    invalid_rect = invalid_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(invalid_text, invalid_rect)
    pygame.display.flip() 
    pygame.time.wait(1000)
    running = False
    return

def select_crow_to_move():
    invalid_text = font.render("Choose a crow to move", True, WIN)
    invalid_rect = invalid_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(invalid_text, invalid_rect)
    pygame.display.flip() 
    pygame.time.wait(1000)
    return
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_circle = None
            for point in points + inner_points:
                winning_condition()   # Check if mouse click is inside any of the circles
                if math.hypot(mouse_x - point[0], mouse_y - point[1]) < 20 and vulture_turn:
                    if vulture_number == 1:
                        if number_colors[2] != "R" and number_colors[10] != "R" and number_colors[4] != "R" and number_colors[8] != "R":
                            crow_winning_print()
                            break
                        if circle_numbers[point] == 8 and number_colors[10] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,10)
                            break
                        if circle_numbers[point] == 4 and number_colors[2] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,2)
                            break
                        
                    elif vulture_number == 3:
                        if number_colors[2] != "R" and number_colors[10] != "R" and number_colors[4] != "R" and number_colors[6] != "R":
                            crow_winning_print()
                            break
                        if circle_numbers[point] == 10 and number_colors[2] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,2)
                            break
                        if circle_numbers[point] == 6 and number_colors[4] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,4)
                            break
                     
                    elif vulture_number == 5:
                        if number_colors[2] != "R" and number_colors[6] != "R" and number_colors[4] != "R" and number_colors[8] != "R":
                            crow_winning_print()
                            break
                        if circle_numbers[point] == 2 and number_colors[4] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,4)
                            break
                        if circle_numbers[point] == 8 and number_colors[6] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,6)
                            break
                        
                    elif vulture_number == 7:
                        if number_colors[6] != "R" and number_colors[10] != "R" and number_colors[4] != "R" and number_colors[8] != "R":
                            crow_winning_print()
                            break
                        if  circle_numbers[point]== 10 and number_colors[8] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,8)
                            break
                        if circle_numbers[point]== 4 and number_colors[6] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,6)
                            break
                        
                    elif vulture_number == 9:
                        if number_colors[2] != "R" and number_colors[10] != "R" and number_colors[6] != "R" and number_colors[8] != "R":
                            crow_winning_print()
                            break
                        if circle_numbers[point] == 2 and number_colors[10] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,10)
                            break
                        if circle_numbers[point] == 6 and number_colors[8] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,8)
                            break
                        
                    elif vulture_number == 2:
                        if number_colors[1] != "R" and number_colors[3] != "R" and number_colors[4] != "R" and number_colors[10] != "R" and number_colors[9] != "R" and number_colors[5] != "R":
                            crow_winning_print()
                            break
                        if circle_numbers[point] == 9 and number_colors[10] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,10)
                            break
                        if circle_numbers[point] == 5 and number_colors[4] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,4)
                            break
                           
                    elif vulture_number == 4:
                        if number_colors[2] != "R" and number_colors[3] != "R" and number_colors[5] != "R" and number_colors[6] != "R" and number_colors[7] != "R" and number_colors[1] != "R":
                            crow_winning_print()
                            break
                        if circle_numbers[point] == 1 and  number_colors[2] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,2)
                            break
                        if circle_numbers[point] == 7 and number_colors[6] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,6)
                            break
                           
                    elif vulture_number == 6:
                        if number_colors[4] != "R" and number_colors[5] != "R" and number_colors[7] != "R" and number_colors[8] != "R" and number_colors[9] != "R" and number_colors[3] != "R":
                            crow_winning_print()
                            break
                        if circle_numbers[point] == 3 and number_colors[4] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,4)
                            break
                        if circle_numbers[point] == 9 and number_colors[8] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,8)
                            break
                           
                    elif vulture_number == 8:
                        if number_colors[6] != "R" and number_colors[7] != "R" and number_colors[9] != "R" and number_colors[10] != "R" and number_colors[1] != "R" and number_colors[5] != "R":
                            crow_winning_print()
                            break
                        if circle_numbers[point] == 5 and number_colors[6] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,6)
                            break
                        if circle_numbers[point] == 1 and number_colors[10] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,10)
                            break
                           
                    elif vulture_number == 10:
                        if number_colors[1] != "R" and number_colors[2] != "R" and number_colors[8] != "R" and number_colors[9] != "R" and number_colors[3] != "R" and number_colors[7] != "R":
                            crow_winning_print()
                            break
                        if circle_numbers[point] == 3 and number_colors[2] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,2)
                            break
                        if circle_numbers[point] == 7 and number_colors[8] == 'W' and number_colors[circle_numbers[point]] == 'R':
                            kill_n_move_vulture(point,8)
                            break
                        
                    if vulture_number!=0 :
                        if vulture_number%2!=0 and (circle_numbers[point]%10!= (vulture_number+1)%10 and circle_numbers[point]%10!= (vulture_number-1)%10):
                         print_errormove()
                         break
                     
                        if vulture_number%2==0 and (circle_numbers[point]%10!= (vulture_number+1)%10 and circle_numbers[point]%10!= (vulture_number-1)%10 and circle_numbers[point]%10!= (vulture_number+2)%10 and circle_numbers[point]%10!= (vulture_number-2)%10):
                         print_errormove()
                         break
                    
                    if number_colors[circle_numbers[point]] != "R":
                        print_errormove()
                        break
                    number_colors[circle_numbers[point]] = "G"  
                    if vulture_number:
                        number_colors[vulture_number] = "R"
                    vulture_point = point 
                    vulture_number = circle_numbers[point]
                    vulture_turn = False
                    crow_turn = True
                    break
                
                elif math.hypot(mouse_x - point[0], mouse_y - point[1]) < 20 and crow_turn and crow_count < 7:
                    if number_colors[circle_numbers[point]]!="R":
                        print_errormove()
                        break
                    number_colors[circle_numbers[point]] = "W"
                    crow_circles.add(point)
                    crow_turn = False
                    crow_count +=1
                    vulture_turn = True
                    break
                
                elif math.hypot(mouse_x - point[0], mouse_y - point[1]) < 20 and crow_turn and crow_count == 7 and not selected_crow : 
                    if number_colors[circle_numbers[point]]!="W":
                        select_crow_to_move()
                        break
                    selected_crow = point
                    selected_crow_num = circle_numbers[point]
                    
                elif math.hypot(mouse_x - point[0], mouse_y - point[1]) < 20 and crow_turn and crow_count == 7 and selected_crow :
                   if number_colors[circle_numbers[point]] == "R":
                    if selected_crow_num!=0 :
                        if selected_crow_num%2!=0 and (circle_numbers[point]%10!= (selected_crow_num+1)%10 and circle_numbers[point]%10!= (selected_crow_num-1)%10):
                         print_errormove()
                         selected_crow = False
                         break

                    if selected_crow_num!=0 :
                        if selected_crow_num%2==0 and (circle_numbers[point]%10!= (selected_crow_num+1)%10 and circle_numbers[point]%10!= (selected_crow_num-1)%10 and circle_numbers[point]%10!= (selected_crow_num+2)%10 and circle_numbers[point]%10!= (selected_crow_num-2)%10):
                         selected_crow=False
                         print_errormove()
                         break
                     
                    number_colors[selected_crow_num] = "R"
                    number_colors[circle_numbers[point]] = "W"
                    crow_circles.remove(selected_crow)
                    selected_crow = False
                    selected_crow_num = 0
                    crow_circles.add(point)
                    crow_turn = False
                    vulture_turn = True
                    break
                
    screen.fill(BLACK) 
    draw_star_with_circles(150) 
    draw_players()
    pygame.display.flip()  

pygame.quit()
