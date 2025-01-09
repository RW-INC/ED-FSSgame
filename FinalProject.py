import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import cv2
import numpy as np
import time

class imstats:
    """handles loading aspecs of an image ie location of signals and pulling in from all images"""
    def __init__(self,imsize):
        """constructor"""
        self.imsize=imsize
        self.newim=None
        self.imsigs=[]
        self.newimsigs=[]

    def imin(self,numim):
        """import the image and get basic info"""
        impath=f'images/{numim}.png'#make not hardcoded in future
        image=Image.open(impath)
        self.imsigs=self.numsigs(impath)

        ox,oy=image.size
        nx,ny=self.imsize
        xr,yr=nx/ox,ny/oy
        self.newimsigs=[(int(x*xr),int(y*yr),int(r*xr)) for x, y, r in self.imsigs]
        self.newim=image.resize(self.imsize, Image.Resampling.LANCZOS)

    def numsigs(self,impath):
        """Detects signals location and num"""
        img=cv2.imread(impath, cv2.IMREAD_GRAYSCALE)
        thresh=cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
        circ=cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=50, param2=30, minRadius=18, maxRadius=40)
        circ=np.uint16(np.around(circ))
        acircles=[]
        for x, y, r in circ[0]:
            if self.excluded(x,y):
                acircles.append((x, y, r))
        #print(f"good circles: {acircles}")
        return acircles
        
    def excluded(self,x,y):
        """Eliminate noise created by excluded regions"""
        reg=[(250, 120, 400, 180),(260,1890,540,1990),(2540,110,2670,180),(2690,220,2890,390),(3240,240,3390,380)]
        for x1, y1, x2, y2 in reg:
            if x1<=x<=x2 and y1<=y<=y2:
                return False
        return True

class gamestate:
    """Holds the vals for the current gamestate"""
    def __init__(self, numim, imsize):
        self.numim=numim
        self.imsize=imsize
        self.imind=0
        self.totsigs=0
        self.tottime=0
        self.totscore=0
        self.sqpos=(imsize[0]//2-15,imsize[1]//2-15,30)
        self.selsq=[]
        self.t0=0

        self.aipos=(imsize[0]//2-15,imsize[1]//2-15,30)
        self.aispeed=0
        self.aisigs=[]
        self.aiselsq=[]
        self.aitime=0
        self.ptime=0
        self.aitottime=0

class scoremode:
    """Gamemode where objective is getting a large score"""
    def __init__(self,root,numim):
        """Constructor"""
        self.root=root
        self.state=gamestate(numim,(1000, 600))#want to pass dims through menu in future
        self.maximnum=15#want to make changable setting later
        self.imst=imstats(self.state.imsize)
        self.tempim=None
        self.tkref=None
        self.loadim()

    def loadim(self):
        """Loads in an image or declares end of game if max images is reached"""
        if self.state.imind<self.state.numim:
            numim = np.random.randint(1,self.maximnum)
            self.imst.imin(numim)
            self.state.sqpos=(self.state.imsize[0]//2-15,self.state.imsize[1]//2-15,30)
            self.state.selsq=[]
            self.state.t0=time.time()
            self.tkref=ImageTk.PhotoImage(self.imst.newim)
            
            if self.tempim is None:
                self.tempim=tk.Label(self.root,image=self.tkref)
                self.tempim.pack()
            else:
                self.tempim.config(image=self.tkref)
            
            self.root.focus_force()
            self.upsq()
        else:
            #print("made it to end")
            msg=(f"Score Mode Complete:\nTotal Signals Detected: {self.state.totsigs}\nTotal Time Taken: {self.state.tottime:.2f} seconds\nFinal Score: {int(self.state.totscore)}")
            messagebox.showinfo("Final Results",msg)
            self.root.destroy()

            root = tk.Tk()
            MainMenu(root)
            root.mainloop()

    def keys(self,event):
        """All key interactions movement and spacebar, space is used to check for the end of the image"""
        x,y,size=self.state.sqpos
        speed=5#want to make changable in settings later
        #print(f"Key: {event.keysym}")
        if event.keysym=='Up':
            y=y-speed    
        elif event.keysym=='Down':
            y=y+speed
        elif event.keysym=='Left':
            x=x-speed
        elif event.keysym=='Right':
            x=x+speed
        self.state.sqpos=(x,y,size)
        if event.keysym=='space':#keep seperate otherwise square doesn't reset
            self.state.selsq.append(self.state.sqpos)
            if self.chkcomp():
                t1=time.time()
                self.state.tottime=self.state.tottime+(t1-self.state.t0)
                num_signals=len(self.imst.newimsigs)
                self.state.totsigs=self.state.totsigs+num_signals
                self.state.totscore=self.state.totscore+max((num_signals*1000)-((t1-self.state.t0)*100),0)
                self.state.imind=self.state.imind+1
                self.loadim()
        self.upsq()

    def upsq(self):
        """Update the square after movement and make sure each square is drawn"""
        x,y,size=self.state.sqpos
        overlay=self.imst.newim.copy()
        draw=ImageDraw.Draw(overlay)

        for sx, sy, sr in self.imst.newimsigs:
            draw.ellipse([sx-sr,sy-sr,sx+sr,sy+sr],outline="blue",width=2)#possibly make toggleable as a setting later-very useful for debug
        for sq in self.state.selsq:
            draw.rectangle([sq[0],sq[1],sq[0]+sq[2],sq[1]+sq[2]],outline="red",width=3)
        draw.rectangle([x,y,x+size,y+size],outline="red",width=3)

        self.tkref=ImageTk.PhotoImage(overlay)
        self.tempim.config(image=self.tkref)

    def chkcomp(self):
        """Check if image is complete by testing if all signals have an overlapping square"""
        for sx, sy, sr in self.imst.newimsigs:
            sigbox=(sx-sr,sy-sr,sx+sr,sy+sr)
            if not any((sq[0]<=sigbox[2] and sq[0]+sq[2]>=sigbox[0] and sq[1]<=sigbox[3] and sq[1]+sq[2]>=sigbox[1]) for sq in self.state.selsq):
                #print(f"NOPE")
                return False
        return True

class racemode:
    """Race mode vs the AI using time"""
    def __init__(self,root,numim,diff):
        """Constructor"""
        self.root=root
        self.state=gamestate(numim,(1000, 600))#want to pass dims through menu in future
        self.imst=imstats(self.state.imsize)
        self.maximnum=15#want to make changable setting later
        self.tempim=None
        self.tkref=None
        
        if diff=="easy":
            self.state.aispeed=3
        elif diff=="medium":
            self.state.aispeed=5
        elif diff=="hard":
            self.state.aispeed=7

        self.loadim()

    def loadim(self):
        """Loads in an image or declares end of game if max images is reached"""
        if self.state.imind<self.state.numim:
            numim=np.random.randint(1,self.maximnum)
            self.imst.imin(numim)
            self.state.sqpos=(self.state.imsize[0]//2-15,self.state.imsize[1]//2-15,30)
            self.state.selsq=[]
            self.state.aipos=(self.state.imsize[0]//2-15,self.state.imsize[1]//2-15,30)
            self.state.aiselsq=[]
            self.state.aisigs=sorted(self.imst.newimsigs,key=lambda p:(p[0]**2+p[1]**2)**.5)
            self.state.aitime=0
            self.state.ptime=0
            self.state.t0=time.time()
            self.tkref=ImageTk.PhotoImage(self.imst.newim)

            if self.tempim is None:
                self.tempim=tk.Label(self.root,image=self.tkref)
                self.tempim.pack()
            else:
                self.tempim.config(image=self.tkref)

            self.root.focus_force()
            self.upsq()
            self.root.after(100, self.aimove)
        else:
            #print("made it to end")
            msg=(f"AI Race Mode Complete:\nTotal Player Time: {self.state.tottime:.2f} seconds\nTotal AI Time: {self.state.aitottime:.2f} seconds")
            if self.state.tottime<self.state.aitottime:
                msg=msg+"\nWin: You were faster than the AI!"
            elif self.state.tottime>self.state.aitottime:
                msg=msg+"\nLoss: The AI was faster than you"
            else:
                msg=msg+"\nIt's a tie: which is far more impressive than winning!"
            messagebox.showinfo("Final Results", msg)
            self.root.destroy()

            root = tk.Tk()
            MainMenu(root)
            root.mainloop()

    def keys(self,event):
        """All key interactions movement and spacebar, space is used to check for the end of the image"""
        x,y,size=self.state.sqpos
        speed=5#want to make changable in settings later
        #print(f"Key: {event.keysym}")
        if event.keysym=='Up':
            y=y-speed    
        elif event.keysym=='Down':
            y=y+speed
        elif event.keysym=='Left':
            x=x-speed
        elif event.keysym=='Right':
            x=x+speed
        self.state.sqpos=(x,y,size)
        if event.keysym=='space':
            self.state.selsq.append(self.state.sqpos)
            if self.chkpcomp():
                if self.state.ptime==0:
                    self.state.ptime=time.time()-self.state.t0
                self.chkimcomp()
        self.upsq()

    def aimove(self):
        """Moves the AI box"""
        if len(self.state.aisigs)==0:
            if self.chkaicomp():
                if self.state.aitime==0:
                    self.state.aitime=time.time()-self.state.t0
                    self.chkimcomp()
            return#needs to be return not pass............that was frustrating

        tx,ty,_=self.state.aisigs[0]
        #print(f"aipos: {self.state.aipos}")
        ax,ay,size=self.state.aipos
        dist=((tx-ax)**2+(ty-ay)**2)**0.5

        if dist<=self.state.aispeed:
            self.state.aipos=(tx,ty,size)
            self.state.aisigs.pop(0)
            self.state.aiselsq.append((tx-15,ty-15,30))
        else:
            dx=(tx-ax)/dist*self.state.aispeed
            dy=(ty-ay)/dist*self.state.aispeed
            self.state.aipos=(int(ax+dx),int(ay+dy),size)

        self.upsq()
        self.root.after(100, self.aimove)

    def upsq(self):
        """Update the square after movement and make sure each square is drawn"""
        x,y,size=self.state.sqpos
        overlay=self.imst.newim.copy()
        draw=ImageDraw.Draw(overlay)
        #would like to make an option to change colors under settings later
        for sx, sy, sr in self.imst.newimsigs:
            draw.ellipse([sx-sr,sy-sr,sx+sr,sy+sr],outline="blue",width=2)
        for sq in self.state.selsq:
            draw.rectangle([sq[0],sq[1],sq[0]+sq[2],sq[1]+sq[2]],outline="red",width=3)
        draw.rectangle([x,y,x+size,y+size],outline="red",width=3)
        
        x,y,size = self.state.aipos
        for sq in self.state.aiselsq:
            draw.rectangle([sq[0],sq[1],sq[0]+sq[2],sq[1]+sq[2]],outline="green",width=2)
        draw.rectangle([x,y,x+size,y+size],outline="green",width=2)

        self.tkref=ImageTk.PhotoImage(overlay)
        self.tempim.config(image=self.tkref)

    def chkpcomp(self):
        """Check if player signals are complete"""
        for sx, sy, sr in self.imst.newimsigs:
            sigbox=(sx-sr,sy-sr,sx+sr,sy+sr)
            if not any((sq[0]<=sigbox[2] and sq[0]+sq[2]>=sigbox[0] and sq[1]<=sigbox[3] and sq[1]+sq[2]>=sigbox[1]) for sq in self.state.selsq):
                #print("P-NOPE")
                return False
        return True

    def chkaicomp(self):
        """Check if AI signals are complete"""
        for sx, sy, sr in self.imst.newimsigs:
            sigbox=(sx-sr,sy-sr,sx+sr,sy+sr)
            if not any((sq[0]<=sigbox[2] and sq[0]+sq[2]>=sigbox[0] and sq[1]<=sigbox[3] and sq[1]+sq[2]>=sigbox[1]) for sq in self.state.aiselsq):
                #print("AI-NOPE")
                return False
        return True

    def chkimcomp(self):
        """Check if both player and AI signals are complete/update total time if so"""
        if self.state.ptime!=0 and self.state.aitime!=0:
            self.state.tottime=self.state.tottime+self.state.ptime
            #print(f"tottime: {self.state.tottime}")
            self.state.aitottime=self.state.aitottime+self.state.aitime
            #print(f"aitottime: {self.state.tottime}")
            self.state.imind=self.state.imind+1
            self.loadim()

class MainMenu:
    """Creates a main menu for the program serves as way to get params"""
    def __init__(self, root):
        self.root=root
        self.root.title("Main Menu")
        self.root.geometry("600x400")#want to make this editable in settings later

        self.l1=tk.Label(root,text="Select game mode:")
        self.l1.pack()
        self.l1v=tk.StringVar(value="score")
        self.l1o1=tk.Radiobutton(root,text="Score mode",variable=self.l1v,value="score")
        self.l1o1.pack()
        self.l1o2=tk.Radiobutton(root,text="AI race mode",variable=self.l1v,value="race")
        self.l1o2.pack()

        self.l2=tk.Label(root,text="Enter number of images:")
        self.l2.pack()
        self.l2v=tk.IntVar(value=3)#make sure no type other than int is accepted
        self.l2o1=tk.Entry(root,textvariable=self.l2v)
        self.l2o1.pack()

        self.l3=tk.Label(root,text="Select difficulty:")
        self.l3.pack()
        self.l3v=tk.StringVar(value="medium")
        self.l3o1=tk.Radiobutton(root,text="Easy",variable=self.l3v,value="easy")
        self.l3o1.pack()
        self.l3o2=tk.Radiobutton(root,text="Medium",variable=self.l3v,value="medium")
        self.l3o2.pack()
        self.l3o3=tk.Radiobutton(root,text="Hard",variable=self.l3v,value="hard")
        self.l3o3.pack()

        self.l4=tk.Button(root,text="Start Selected Mode",command=self.start)
        self.l4.pack()

        self.l5=tk.Button(root,text="Exit",command=exit)
        self.l5.pack()

    def start(self):
        """Start the selected game mode with settings from"""
        cmode=self.l1v.get()
        numim=self.l2v.get()
        diff=self.l3v.get()
        if numim<1 or numim>15:#make this reflect the changable maxnumim in the future
            messagebox.showerror("Invalid Input","Please enter a number between 1 and 15.")
            return
        
        self.root.destroy()
        tkgame=tk.Tk()
        if cmode=="score":
            mode=scoremode(tkgame,numim)
        elif cmode=="race":
            mode=racemode(tkgame,numim,diff)
        tkgame.bind('<KeyPress>', mode.keys)
        tkgame.mainloop()

    def exit(self):
        """Close window on exit button"""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()