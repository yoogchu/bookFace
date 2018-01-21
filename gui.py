import Tkinter as tk
import cv2
from PIL import Image, ImageTk
import facial
import compare_face
import threading

# class videoStream(threading.Thread):
	# def __init__(self):
		
# Layout setup
width, height = 600, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Important variables 
people = []
webcam=True
folder='faces'

def update():
	lmain.after(1, show_frame())
	lmain2.after(1, refreshPeople(people))
	root.after(5, update)

def show_frame():
	global people

	(frame, people) = facial.recog(people, cap)
	# frame = cv2.flip(frame, 1)
	cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	img = Image.fromarray(frame)
	imgtk = ImageTk.PhotoImage(image=img)
	
	lmain.imgtk = imgtk
	lmain.configure(image=imgtk)

def close_window(people):
	root.quit()
	print 'Exiting...'
	print 'Saving faces in: '+folder
	facial.save_faces(people,folder=folder,webcam=webcam)

# Tkinkter
root = tk.Tk()
root.bind('<Escape>', lambda e: close_window(people))
root.title('Gotcha Bitch!')
# root.geometry('1280x800')
lmain = tk.Label(root)
lmain2 = tk.Label(root)
lmain.pack(side=tk.LEFT)
lmain2.pack(side=tk.RIGHT)

def refreshPeople(people):
	person=0
	
	for r in range(4):
		for c in range(3):
			try:
				tk.Label(lmain2, text='%s'%(people[r+c].getName()), borderwidth=1).grid(row=r, column=c)
			except Exception as e:
				tk.Label(lmain2, text='%s'%('unknown'), borderwidth=1).grid(row=r, column=c)
			# img = Image.fromarray()
			# imgtk = ImageTk.PhotoImage(image=img)
			# tk.Label(lmain2, text='%s, %s'%('Person', str(person)), borderwidth=1 ).grid(row=r,column=c)
root.after(50, update)
root.mainloop()

