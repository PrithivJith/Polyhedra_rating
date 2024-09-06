import tkinter as tk
import random
import threading
import time
from PIL import Image, ImageTk
import os


class Polyhedron():
    def __init__(self,name):
        self.name = name
        self.rating = 1000
        self.get_rating()

    def get_rating(self):
        f = open("ratings.txt",'r')
        content = f.readlines()
        for line in content:
            rating_pair = line.split(':')
            if rating_pair[0] == self.name:
                self.rating = int(rating_pair[1])
        f.close()

    def __gt__(self, other):
        if self.rating>other.rating:
            return True
        else:
            return False
    def __le__(self, other):
        if self.rating<other.rating:
            return True
        else:
            return False



vote = None
polyhedra_lib = []

def save_rating(lib=polyhedra_lib):
    f = open("ratings.txt","r")
    content_ratings = {}
    content = f.readlines()
    for f_shape in content:
        split_content = f_shape[:-1].split(':')
        name = split_content[0]
        rating = int(split_content[1])
        content_ratings[name] = rating
    for l_shape in lib:
        content_ratings[l_shape.name] = l_shape.rating
    f.close()
    f = open("ratings.txt","w")
    for shape,rating in content_ratings.items():
        f.write(f"{shape}:{rating}\n")

    f.close()

def reset_rating(lib=polyhedra_lib):
    f = open("ratings.txt","r")
    content_ratings = {}
    content = f.readlines()
    for f_shape in content:
        split_content = f_shape[:-1].split(':')
        name = split_content[0]
        rating = int(split_content[1])
        content_ratings[name] = rating

    for l_shape in lib:
        content_ratings[l_shape.name] = 1000

    f.close()
    f = open("ratings.txt", "w")
    for shape, rating in content_ratings.items():
        f.write(f"{shape}:{rating}\n")

    f.close()


def add_platonic_solids():
    global polyhedra_lib
    for i in [Polyhedron("tetrahedron"), Polyhedron("cube"), Polyhedron("octahedron"), Polyhedron("dodecahedron"),Polyhedron("icosahedron")]:
        polyhedra_lib.append(i)

def add_archimedean_solids():
    for i in [Polyhedron("truncated tetrahedron"),Polyhedron("cuboctahedron"),Polyhedron("truncated cube"),Polyhedron("truncated octahedron"),Polyhedron("rhombicuboctahedron"),Polyhedron("truncated cuboctahedron"),Polyhedron("snub cube"),Polyhedron("icosidodecahedron"),Polyhedron("truncated dodecahedron"),Polyhedron("truncated icosahedron"),Polyhedron("rhombicosidodecahedron"),Polyhedron("truncated icosidodecahedron"),Polyhedron("snub dodecahedron")]:
        polyhedra_lib.append(i)



def vote_1():
    global vote
    vote = 1
def vote_2():
    global vote
    vote = 2

def vote_tie():
    global vote
    vote = 0.5

shape1_name = None
shape2_name = None

def update_image1():
    global shape1_name
    global shape1_img

    if shape1_name != None:
        dirname = os.path.dirname(__file__)
        file_path_1 = dirname + fr'\images\{shape1_name}.png'
        shape1_img = Image.open(file_path_1)
        shape1_img = shape1_img.resize((300, 300))
        shape1_img = ImageTk.PhotoImage(shape1_img)
        shape1_img_label.config(image=shape1_img)


def update_image2(name):
    global shape2_name
    global shape2_img

    if name != None:
        dirname = os.path.dirname(__file__)
        file_path_2 = dirname + fr'\images\{name}.png'
        shape2_img = Image.open(file_path_2)
        shape2_img = shape2_img.resize((300, 300))
        shape2_img = ImageTk.PhotoImage(shape2_img)
        shape2_img_label.config(image=shape2_img)
def normal_round(num):
    if num > 0:
        return int(num+0.5)
    else:
        return int(num-0.5)
def expectedRating(you,opponent):
    expected_rating = 1/(1+10**((opponent.rating-you.rating)/400))
    return expected_rating

def newRating(you,opponent,you_s,opponent_s):
    k=34
    new_rating_you = you.rating+k*(you_s-expectedRating(you,opponent))
    new_rating_opponent = opponent.rating+k*(opponent_s-expectedRating(opponent,you))
    ratings = (new_rating_you,new_rating_opponent)
    return map(lambda num: normal_round(num),ratings)
def handle_vote(rnd):
    player1 = rnd[0]
    player2 = rnd[1]
    player1_s,player2_s = (0,0)

    if vote == 1:
        player1_s = 1
    elif vote == 2:
        player2_s =1
    elif vote == 0.5:
        player1_s = 0.5
        player2_s = 0.5
    player1_rating,player2_rating = newRating(player1,player2,player1_s,player2_s)
    rnd[0].rating = player1_rating
    rnd[1].rating = player2_rating

sorted_shapes = sorted(polyhedra_lib,reverse=True)
polyhedra_lib_added = False
def main():
    global vote
    global update_images
    global shape1_name
    global sorted_shapes
    global polyhedra_lib_added

    all_possible_comb = []

    while not polyhedra_lib_added:
        time.sleep(1)
    for index,shape in enumerate(polyhedra_lib):
        for next_index in range(index+1,len(polyhedra_lib)):
            all_possible_comb.append((shape,polyhedra_lib[next_index]))
    remaining_comb = all_possible_comb.copy()

    while remaining_comb:
        rnd_comb = remaining_comb[random.randint(0,len(remaining_comb)-1)]
        shape1.config(text=rnd_comb[0].name)
        shape2.config(text=rnd_comb[1].name)

        shape2_name = rnd_comb[1].name
        update_image2(shape2_name)
        shape1_name = rnd_comb[0].name
        update_image1()


        while vote == None:
            time.sleep(0.05)
            continue
        handle_vote(rnd_comb)
        vote = None
        remaining_comb.remove(rnd_comb)
    rank_window()





root = tk.Tk()

root.title("Polyhedra ranks")
root.geometry("1000x1000")
root.resizable(False,False)
FONT = font=("Cascadia Code SemiLight", 23)

def num_of_windows(root:tk.Tk):
    children = root.winfo_children()
    return sum(1 for child in children if isinstance(child,tk.Toplevel))

def update_list(list:tk.Listbox):
    global sorted_shapes
    sorted_shapes = sorted(polyhedra_lib, reverse=True)
    list.delete(0,tk.END)
    for i in range(0,len(sorted_shapes)):
        list.insert(i,f"{sorted_shapes[i].name.capitalize()} -> {sorted_shapes[i].rating}")

def rank_window():
    global root
    if num_of_windows(root) == 0:
        global sorted_shapes
        BACKGROUND = r'#70a9c2'
        window = tk.Toplevel()
        window.title("Ranking")
        window.geometry("700x700")
        window.config(background=BACKGROUND)
        window.resizable(False, False)
        window.attributes('-topmost',True)


        scrollbar = tk.Scrollbar(window,orient="vertical")
        rank_list = tk.Listbox(window,width=500,height=12,font=(FONT[0],30),selectbackground=BACKGROUND,selectforeground="black",background=BACKGROUND)
        update_list(rank_list)
        update_button = tk.Button(window,text="Update",font=(FONT[0],19),background="grey",width=15,height=1,activebackground="gray64",command=lambda : update_list(rank_list))

        rank_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=rank_list.yview)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        update_button.lift()
        rank_list.pack()
        update_button.place(relx=0.5,rely=0.955,anchor="center")

def handle_selection(platonic_solid,archimedean_solid,win):
    global polyhedra_lib_added
    if platonic_solid:
        add_platonic_solids()
    if archimedean_solid:
        add_archimedean_solids()
    polyhedra_lib_added = True
    win.destroy()
    win.update()

def selection_screen():
    global sorted_shapes
    global roote


    BACKGROUND = r'white'
    window_sel = tk.Toplevel()
    window_sel.title("Selection")
    window_sel.geometry("500x600")
    window_sel.config(background=BACKGROUND)
    window_sel.resizable(False, False)
    window_sel.attributes('-topmost', True)


    select_button = tk.Button(window_sel,text="Select",font=(FONT[0],15),background="grey",width=15,activebackground="gray64",command=lambda : handle_selection(platonic_variable.get(),archimedean_variable.get(),window_sel))

    platonic_variable = tk.IntVar()
    platonic_button = tk.Checkbutton(window_sel,text="Platonic solids",variable=platonic_variable,onvalue=1,offvalue=0,height=5,width=20,font=FONT,background="white",activebackground="white")

    archimedean_variable = tk.IntVar()
    archimedean_button = tk.Checkbutton(window_sel, text="Archimedean solids", variable=archimedean_variable, onvalue=1,offvalue=0, height=5, width=20, font=FONT, background="white",activebackground="white")

    platonic_button.place(relx=0.5,rely=0.20,anchor="center")
    archimedean_button.place(relx=0.5, rely=0.50, anchor="center")
    select_button.place(relx=0.5,rely=0.85,anchor="center")


root.focus_force()

rank_button = tk.Button(text="Show Ratings",font=FONT,width=15,background='#70a9c2',activebackground='#385561',command=rank_window)

shape1 = tk.Label(text="shape1",font=FONT)
shape2 = tk.Label(text="shape2",font=FONT)

shape1_img_label = tk.Label()
shape2_img_label = tk.Label()

reset_rating_button = tk.Button(text="Reset Ratings",font=(FONT[0],14),height=2,width=17,background="#70a9c2",activebackground="#385561",command=reset_rating)
shape1_button = tk.Button(text="1",font=FONT,width=15,background="#70a9c2",activebackground="#385561",command=vote_1)
shape2_button = tk.Button(text="2",font=FONT,width=15,background="#70a9c2",activebackground="#385561",command=vote_2)
tie_button = tk.Button(text="tie",font=FONT,width=10,background="#70a9c2",activebackground="#385561",command=vote_tie)
save_rating_button = tk.Button(text="Save Ratings",font=FONT,width=15,background="#70a9c2",activebackground="#385561",command=save_rating)

shape1.place(relx=0.25, y=20, anchor="center")
shape2.place(relx=0.75, y=20, anchor="center")

save_rating_button.place(rely=0.95,relx=0.75,anchor="center")
tie_button.place(relx=0.5,y=850,anchor="center")
shape1_button.place(relx=0.25, y=850, anchor="center")
shape2_button.place(relx=0.75, y=850, anchor="center")
reset_rating_button.place(rely=0.95,relx=0.5,anchor="center")

shape1_img_label.place(relx=0.25, y=400, anchor="center")
shape2_img_label.place(relx=0.75, y=400, anchor="center")

rank_button.place(relx=0.25,rely=0.95,anchor="center")

threading.Thread(target=main,daemon=True).start()
selection_screen()
root.mainloop()






