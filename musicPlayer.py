import tkinter
from tkinter.ttk import Progressbar
import customtkinter
import pygame
from PIL import Image, ImageTk
from threading import *
import time
import math

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

##### Tkinter stuff ######
root = customtkinter.CTk()
root.title('Music Player')
root.geometry('400x480')
pygame.mixer.init()
##########################

list_of_songs = ['music/Out of Touch (Avangart Tabldot Remix).wav'] # Add more songs into this list, make sure they are .wav and put into the music Directory.
list_of_covers = ['img/Out of Touch (Avangart Tabldot Remix).jpg'] 
n = 0

def get_album_cover(song_name, n):
    image1 = Image.open(list_of_covers[n])
    image2=image1.resize((250, 250))
    load = ImageTk.PhotoImage(image2)
    
    label1 = tkinter.Label(root, image=load)
    label1.image = load
    label1.place(relx=.19, rely=.06)

    stripped_string = song_name[6:-4] #This is to exlude the other characters
                                                # 6       :      -4
                                    # Example: 'music/ | City | .wav'
                                    # This works because the music will always be between those 2 values
    
    song_name_label = tkinter.Label(text = stripped_string,fg='black')
    song_name_label.place(relx=.4, rely=.6)


def progress():
    a = pygame.mixer.Sound(f'{list_of_songs[n]}')
    song_len = a.get_length() * 3
    for i in range(0, math.ceil(song_len)):
        time.sleep(.4)
        progressbar.set(pygame.mixer.music.get_pos() / 1000000)

def threading():
    t1 = Thread(target=progress)
    t1.start()

def play_music():
    threading()
    global n 
    current_song = n
    if n > 2:
        n = 0
    song_name = list_of_songs[n]
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.set_volume(.5)
    get_album_cover(song_name, n)

    # print('PLAY')
    n += 1

def skip_forward():
    play_music()

def skip_back():
    global n
    n -= 2
    play_music()

def volume(value):
    pygame.mixer.music.set_volume(value)

# Create a frame to contain your widgets
frame = tkinter.Frame(root, bg='white')
frame.pack(fill=tkinter.BOTH, expand=True)

# All Buttons
play_button = customtkinter.CTkButton(master=root, text='Play', command=play_music)
play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

skip_f = customtkinter.CTkButton(master=root, text='>', command=skip_forward, width=2)
skip_f.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

skip_b = customtkinter.CTkButton(master=root, text='<', command=skip_back, width=2)
skip_b.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root, from_= 0, to=1, command=volume, width=210)
slider.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)

progressbar = customtkinter.CTkProgressBar(master=root, progress_color='#32a85a', width=250)
progressbar.place(relx=.5, rely=.85, anchor=tkinter.CENTER)

elapsed_time_label = tkinter.Label(text="Elapsed Time: 00:00",fg='Black')
elapsed_time_label.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

# Function to update the elapsed time
def update_elapsed_time():
    while True:
        if pygame.mixer.music.get_busy():
            elapsed_time = pygame.mixer.music.get_pos() // 1000  # Get elapsed time in seconds
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            elapsed_time_label.config(text=f"Elapsed Time: {minutes:02}:{seconds:02}")
        time.sleep(1)  # Update every second

elapsed_time_thread = Thread(target=update_elapsed_time)
elapsed_time_thread.daemon = True  
elapsed_time_thread.start()

# Autoplay the music when the program starts
play_music()

root.mainloop()