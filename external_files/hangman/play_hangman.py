import pygame
import os
import math
import words

#set display screen
pygame.init()
white=(255,255,255)
BLACK=(0,0,0)
Width=800
Height=600
window=pygame.display.set_mode((Width,Height))
pygame.display.set_caption('Hang Man!!')

# buttons to demonstrate A-Z options
RADIUS=20
GAP=15
A=65

letters_posxy_alph_flag=[]  #stores 3 values for each button(posx,posy,alphabet to be filled in button)
startx=30   # where the first button must be located acc to x axis
starty=400  #acc to y axis
for i in range(26):  #26 alphabets
    x= startx+GAP*2+((RADIUS*2+GAP)* (i%13))  #i%13 helping to divie 13-13 alphs in 2 rows
    #GaP*2 to leave space in both edges of screen

    y= starty+((i//13)*(GAP + RADIUS *2))
    #i//13 to change row: for 0-12:0 while for 13-25:1

    letters_posxy_alph_flag.append([x,y,chr(A+i),True])

#fonts
LETTER_FONT=pygame.font.SysFont('comicsans',40)
WORD_FONT=pygame.font.SysFont('comicsans',60)
TITLE_FONT=pygame.font.SysFont('comicsans',70)
#variables for word to be guessed
word=words.random_word()
guessed=[]

HANGMAN = os.path.dirname((os.path.abspath(__file__)))
IMAGES = os.path.join(HANGMAN, 'images')

#loading hangman images
images= []
for i in range (7):
    #image=pygame.image.load(r'C:\Users\HP\OneDrive\Desktop\hangmanImages\images\hangman'+str(i)+'.png')
    image=pygame.image.load(os.path.join(IMAGES, 'hangman'+str(i)+'.png'))
    images.append(image)

#what image do we want to draw when

    hangman_status=0


#print(images):wasn confiirmation in console that images were loaded

#setup loop for game with timer
FPS=60
clock=pygame.time.Clock()

run=True


def draw_hangman():
    window.fill(white)

    #title
    text=TITLE_FONT.render("HANGMAN",1,BLACK)
    window.blit(text,(300,10))
    #display _______ word
    display_word=''
    for char in word:
        if char in guessed:
            display_word+=char+' '
        else:
            display_word+="_ "
    text=WORD_FONT.render(display_word,1,BLACK)
    window.blit(text,(400,200))

    #draw buttons for letters
    for letter in letters_posxy_alph_flag:
        x,y,ltr,visible=letter
        if(visible):
            pygame.draw.circle(window,BLACK,(x,y),RADIUS,3)
            text=LETTER_FONT.render(ltr,1,BLACK)
            window.blit(text,(x-RADIUS/2,y-RADIUS/2))
    window.blit(images[hangman_status], (150,100))
    pygame.display.update()


def display_final_result(message):
    pygame.time.delay(2000)
    window.fill(white)
    text = WORD_FONT.render(message, 1, BLACK)
    window.blit(text, (50, 60))
    pygame.display.update()
    pygame.time.delay(3000)


while run:

    clock.tick(FPS)
    draw_hangman()
    for event in pygame.event.get():    #conditions for all clicks happening in screen

        if event.type == pygame.QUIT:   #exit game
            run = False

#get pos where are we clicking
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_posx,mouse_posy=pygame.mouse.get_pos()
            #now we will be checking if the coordinate where mouse click is done is valid or not
            #it is valid if coord
            # inates lie in range of radius of button from center
            #also if valid,check which letter has been choden by player
            for letter in letters_posxy_alph_flag:
                x,y,ltr,visible=letter
                if(visible):
                    dis=math.sqrt((x-mouse_posx)**2 +(y-mouse_posy)**2)
                    if dis<RADIUS:
                        letter[3]=False
                        guessed.append(ltr)
                        #print(ltr)
                        if ltr not in word:
                            hangman_status+=1
    won=True
    for letter in word:
        if letter not in guessed:
            won=False
            break

    if won:
        display_final_result("YOU WON!")
        break

    if hangman_status == 6:
        display_final_result("YOU LOST!The word was:"+word)
        break


# completely fill the surface object
    # with white colour

pygame.quit()