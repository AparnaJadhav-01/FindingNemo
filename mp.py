from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector as mysql
import re
import random
#info and scores are db names
 
LARGE_FONT= ("Verdana", 12)
db=mysql.connect(
    host='localhost',
    user='root',
    password="yourpassword",
    database = "yourdatabasename",
)
def createCursor():
    return db.cursor(buffered=True)
 
global curruser
class SeaofBTCapp(Tk):
     
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        self.geometry('400x450')
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne):
            # for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
 
        
class StartPage(Frame): #main screen
    # Registered=0
    def __init__(self, parent, controller):   #starting screen 
        Frame.__init__(self,parent,bg="#044e6e")
        ("500x500")
        print("gello")
        label1 = Label(self,text = "Welcome", bg = "#044e6e",fg='white')
        label1.config(font=("Helvetica", 30))
        label1.place(x=90,y=30)
           
        label2 = Label(self,text = "Select user from given dropdown, add your password and start playing ", bg = "#044e6e",fg='white')
        label2.place(x=15, y=80)
        
        ttk.Label(self, text = "Select the User:" ,background= "#044e6e",foreground='white',font = ("Times New Roman", 14)).place(x=25,y=150)
        ttk.Label(self, text = "Password:",  background= "#044e6e",foreground='white',font = ("Times New Roman", 14)).place(x=25,y=200)
        # Combobox creation
        self.n = StringVar()
        self.p=StringVar()
        useroptns = ttk.Combobox(self, width = 27, textvariable = self.n)
        cursor=createCursor()
        cursor.execute("select username from info")
        result=cursor.fetchall()
        users=[]
        print(result)
        for i in result:
            users.append(i[0])
        useroptns['values'] = tuple(users)
        useroptns.place(x=170, y=150)
        useroptns.current()
        Entry(self,textvariable=self.p, show= '*').place(x=170,y=200)
        but4 =Button(self,text ="Login",bg="#fa8107", command=self.login_verify)
        but4.place(x=170,y=300)
       
        but3 =Button(self,text ="Add New Player",bg="#fa8107", command=lambda:controller.show_frame(PageOne))
        but3.place(x=25,y=300)
       

    def login_verify(self):  
        global curruser
        passwd=self.p.get()
        uname=self.n.get()
        if passwd=="" or uname=="":
            messagebox.showinfo("Attention!", "Enter required credentials!")
        else:
            cur=createCursor()
            cur.execute("select password from info where username=%s",(uname,))
            getpas=cur.fetchone()
            if passwd==getpas[0]:   # go to main game page  
                print("success")
                curruser=uname
                win = Toplevel()
                win.title('GAME')
                win.geometry('100x100')
                win.resizable(width = False, height = False)
                win.configure(bg='#044e6e')
                message = "Game starts now"
                Label(win, text=message).pack()
                Button(win, text='START GAME', bg="#fa8107", command=lambda:call_gm()).pack()     
            else:
                messagebox.showinfo("Oops!", "Enter correct details!")
 
class PageOne(Frame):
    Registered=0
    def  __init__(self, parent, controller): #done , redirect to first page via register_user
        Frame.__init__(self, parent,bg="#044e6e")
        self.username = StringVar()
        self.password = StringVar()
    
        Label(self, text="Please enter details below", bg = "#044e6e",fg='white').place(x=90, y= 10)
        username_lable = Label(self, text="Username * ",bg = "#044e6e",fg='white')
        username_lable.place(x=10, y= 60)
        self.username_entry = Entry(self, textvariable=self.username)
        self.username_entry.place(x=90,y=60)
        password_lable = Label(self, text="Password * ",bg = "#044e6e",fg='white')
        password_lable.place(x=10, y= 110)
        self.password_entry = Entry(self, textvariable=self.password, show='*')
        self.password_entry.place(x=90,y=110)
        Button(self, text="Done", width=10, height=1, bg="#fa8107", command = self.register_user).place(x=280,y=160)
        Button(self, text="Home", width=10, height=1, bg="#fa8107", command = lambda: controller.show_frame(StartPage)).place(x=280,y=190)

 
    
    def register_user(self):  #db+gets entry + checks using regex
        # self.destroy()
        username_info = self.username.get()
        password_info = self.password.get()
        print(username_info,password_info)
        if re.findall(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{5,8}$", password_info):
            cursor=createCursor()
            query="insert into info(username,password) values(%s,%s)"
            value=(username_info,password_info)
            print(value)
            cursor.execute(query,value)
            db.commit()
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)
            Label(self, text="Registration Success", fg="green", font=("calibri", 10)).place(x=50,y=160)
        else:
            messagebox.askretrycancel("Try Again?", "Password not acceptable.\nInclude atleast one uppercase,lowercase characters and a number.\nCheck length between 5 to 8.") 
 
 
class PageTwo:
 
    # i=StartPage()
    def FISHDown(self,event):
        self.w.move(self.FISH,0,20)
        self.FISH_Y=self.w.coords(self.FISH)[1]
 
    def FISHUp(self,event):
        if self.NOW_PAUSE == False: 
            if self.FISH_Y <= 0: self.FISH_Y = 0
            self.w.move(self.FISH,0,-20)
            self.FISH_Y=self.w.coords(self.FISH)[1]
        else:
            self.restartGame()
    
    def call_sea(self,event):
        global app
        self.master.destroy()     
        app=SeaofBTCapp()
        app.mainloop()
 
    def __init__(self,master):
        # i=SeaofBTCapp()
        self.master=master
        master.bind("<Up>",self.FISHUp)
        master.bind("<Down>",self.FISHDown)
        master.bind("<space>",self.call_sea)
        self.FRAMERATE = 18
        self.SCORE = -1
        #self.main = Tk()
        master.resizable(width = False, height = False)
        master.title("Finding Nemo")
        master.geometry('550x600')
 
        self.FISH_Y = 200
        self.PIPE_X = 550
        self.PIPE_HOLE = 0
        self.NOW_PAUSE = False
 
        self.BEST_SCORE = 0
        self.bgImg = PhotoImage(file="images/backg.png")
        self.w = Canvas(master, width = 550, height = 700, bg="#044e6e", bd=0, highlightthickness=0)
        self.w.pack()
 
        self.FISHImg = PhotoImage(file="images/fish2.png")
        self.FISH = self.w.create_image(100, self.FISH_Y, image=self.FISHImg)
 
        self.endRectangle = self.endBest = self.endScore = None
 
        self.pipeUp = self.w.create_rectangle(self.PIPE_X, 0, self.PIPE_X + 100, self.PIPE_HOLE, fill="#74BF2E", outline="#74BF2E")
        self.pipeDown = self.w.create_rectangle(self.PIPE_X, self.PIPE_HOLE + 200, self.PIPE_X + 100, 700, fill="#74BF2E", outline="#74BF2E")
        self.score_w = self.w.create_text(15, 45, text="0", font='Impact 60', fill='#ffffff', anchor=W)
        self.generatePipeHole()
        master.after(self.FRAMERATE, self.pipesMotion)
        master.after(self.FRAMERATE, self.detectCollision)
 
 
    def generatePipeHole(self):
        self.SCORE += 1
        self.w.itemconfig(self.score_w, text=str(self.SCORE))
        self.PIPE_HOLE = random.randint(50, 500)
        if self.SCORE + 1 % 4 == 0 and self.SCORE != 0: 
            self.FRAMERATE-=2
        #print("Score: " + str(SCORE))
       
    def pipesMotion(self):
        self.PIPE_X -= 5
        self.w.coords(self.pipeUp, self.PIPE_X, 0,self.PIPE_X + 100,self.PIPE_HOLE)
        self.w.coords(self.pipeDown,self.PIPE_X,self.PIPE_HOLE + 200,self.PIPE_X + 100, 700)
        
        if self.PIPE_X < -100: 
            self.PIPE_X = 550
            self.generatePipeHole()
        
        if self.NOW_PAUSE == False: 
            self.master.after(self.FRAMERATE, self.pipesMotion)
    
    def engGameScreen(self):
        cur=createCursor()
        cur.execute("select score,uname from scores order by score desc limit 3")
        h=cur.fetchall()
        self.endRectangle = self.w.create_rectangle(0, 0, 550, 700, fill='#044e6e')
        self.endScore = self.w.create_text(10, 200, text="Your score: " + str(self.SCORE), font='Impact 20', fill='#ffffff', anchor=W)
        self.endBest = self.w.create_text(15, 280, text="Top 3 scores\n" +str(h[0][0])+":"+str(h[0][1])+"\n"+str(h[1][0])+":"+str(h[1][1])+"\n"+str(h[2][0])+":"+str(h[2 ][1]), font='Arial 20', fill='#ffffff', anchor=W)
        self.spc = self.w.create_text(8, 360, text="Press the space bar to go to home page & up key to restart game ", fill='#ffffff', anchor=W)
  
    def detectCollision(self):
 
        if (self.PIPE_X < 150 and self.PIPE_X + 100 >= 55) and (self.w.coords(self.FISH)[1] < self.PIPE_HOLE + 45 or self.w.coords(self.FISH)[1] > self.PIPE_HOLE + 175):
            #print("Collision")
            self.NOW_PAUSE = True
            newscore=self.SCORE
            cur=createCursor()
            cur.execute("insert into scores(score,uname) values(%s,%s)",(int(newscore),str(curruser)))
            db.commit()
            self.engGameScreen()
        if self.NOW_PAUSE == False: self.master.after(self.FRAMERATE, self.detectCollision)
    
 
    def restartGame(self):
        self.FISH_Y = 200
        self.PIPE_X = 550
        self.SCORE = -1
        self.FRAMERATE = 18
        self.NOW_PAUSE = False
        self.w.delete(self.endScore)
        self.w.delete(self.endRectangle)
        self.w.delete(self.endBest)
        self.w.delete(self.spc)
        self.generatePipeHole()
        # self.animate()
        self.master.after(self.FRAMERATE, self.pipesMotion)
        self.master.after(self.FRAMERATE, self.detectCollision)
 
def call_gm():
    global app
    app.destroy() 
    root=Tk()
    app1=PageTwo(root)
    root.mainloop()
 
 
global app
app = SeaofBTCapp()
app.mainloop()
