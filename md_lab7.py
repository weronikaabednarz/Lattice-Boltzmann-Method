import numpy as np
from PIL import Image
import pygame
import random

class Board:
    def __init__(self, image_path="obrazek.bmp"):

        # Wczytanie obrazu
        self.image = Image.open(image_path).convert("RGB")

        # Konwersja obrazu na tablicę numpy
        self.img_array = np.array(self.image)
        self.board_height = self.img_array.shape[0]   #wysokość planszy, czyli liczbę wierszy kwadratów na planszy
        self.board_width = self.img_array.shape[1]   #szerokość planszy, czyli liczbę kolumn kwadratów na planszy

        self.size = 7    # rozmiar małego kwadratu
        #matrix= []
        self.matrix = [[[0,0,0,0] for x in range(self.board_width)] for y in range(self.board_height)]
        self.number_of_squares = 1000
        self.tick = 0

        # Inicjalizacja pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.board_width * self.size, self.board_height * self.size))
        # wyświetlenie okna gry
        pygame.display.set_caption("LGA")
        self.clock = pygame.time.Clock()        


    def initialize_matrix(self):
        for x in range(25):
            for y in range(self.board_height):
                #dla rownomiernego:
                #self.matrix[y][x] = [0.25, 0.25, 0.25, 0.25]
                #dla nierownomiernego:
                self.matrix[y][x] = [0, 0, 0, 0]
                dir = random.randint(0,3)
                self.matrix[y][x][dir] = 1


        self.new_matrix = [[[0,0,0,0] for x in range(self.board_width)] for y in range(self.board_height)]

    def rysuj(self):
        temp = np.copy(self.image)
        for x in range(self.board_width):
            for y in range(self.board_height):
                if np.all(self.img_array[x][y] == [0,0,0]):
                    color = [0,0,0]
                else:    
                    color = [255,255,255]
                    
                    suma = 0
                    for i in range(4):
                        suma += self.matrix[x][y][i]
                    if suma == 0:
                        color = [255, 255, 255]    
                    elif suma < 0.1:
                        color = [209, 231, 240]    
                    elif suma < 0.2:
                        color = [187, 223, 237]    
                    elif suma < 0.3:
                        color = [154, 192, 217]    
                    elif suma < 0.4:
                        color = [133, 182, 214]    
                    elif suma < 0.5:
                        color = [102, 164, 204]    
                    elif suma < 0.6:
                        color = [84, 157, 204]    
                    elif suma < 0.7:
                        color = [70, 153, 207]    
                    elif suma < 0.8:
                        color = [48, 146, 209]    
                    elif suma < 0.9:
                        color = [26, 122, 184]    
                    elif suma < 1:
                        color = [18, 114, 176]    
                    elif suma == 1:
                        color = [7, 86, 138]  
                    else:
                        color = [6, 58, 92]    
                                        

                pygame.draw.rect(self.screen, color, (y*self.size, x*self.size, self.size, self.size))
                temp[x,y] = color
        img_save =  Image.fromarray(temp)
        img_save.save(f"./gif{self.tick}.bmp")

    def chodzenie(self):

        Direction = {
            0:[0,-1],   #gora
            1:[1,0],    #prawo
            2:[0,1],    #dol
            3:[-1,0]    #lewo
        }

        Waga = {
            0:0.25,   #gora
            1:0.25,    #prawo
            2:0.25,    #dol
            3:0.25    #lewo
        }

        for x in range(self.board_width):
            for y in range(self.board_height):
                if np.all(self.img_array[x][y] != [0,0,0]):
                    for i in range(4):
                        if self.matrix[x][y][i] > 0:
                            #print(f"Przed ruchem: Pozycja ({x}, {y}), Kierunek: {i}")
                            if np.all(self.img_array[(x+Direction[i][1])][(y+Direction[i][0])] == [0,0,0]): 
                                self.new_matrix[(x - Direction[i][1])][(y - Direction[i][0])][(i+2)%4] += self.matrix[x][y][i]
                            else:  
                                self.new_matrix[(x + Direction[i][1])][(y + Direction[i][0])][i] += self.matrix[x][y][i]
                            self.matrix[x][y][i] = 0

        # for x in range(self.board_width):
        #     for y in range(self.board_height):
        #         self.matrix[x][y]=[0,0,0,0]
        #         if np.all(self.img_array[x][y] != [0,0,0]): 
        #             for i in [0,1]:
        #                 if self.new_matrix[x][y][i] + self.new_matrix[x][y][i+2] >= 2:
        #                     if self.new_matrix[x][y][i] == 0:
        #                         self.new_matrix[x][y][i+2] -= 2
        #                     elif self.new_matrix[x][y][i+2] == 0:
        #                         self.new_matrix[x][y][i] -= 2
        #                     else:
        #                         self.new_matrix[x][y][i] -= 1
        #                         self.new_matrix[x][y][i+2] -= 1
        #                     self.matrix[x][y][i+1] += 1
        #                     self.matrix[x][y][(i+3)%4] += 1

                    suma = 0
                    for i in range(4):
                        suma += self.new_matrix[x][y][i]
                    for i in range(4):
                        self.matrix[x][y][i] += suma*Waga[i]
                        self.new_matrix[x][y][i]= 0    

                    self.new_matrix[x][y] = [0,0,0,0] 
             

if __name__ == "__main__":
 
    board = Board()
    board.initialize_matrix()

    max_ticks = 50000  # Maksymalna liczba iteracji
    run = True
    # pętla główna

    board.rysuj()
    while run:
        if board.tick < max_ticks:
            board.clock.tick(60)

            board.chodzenie()
            board.rysuj()        
            board.tick += 1
            pygame.time.delay(1) 


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed() 


            pygame.display.flip()
