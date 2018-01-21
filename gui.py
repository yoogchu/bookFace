import Tkinter as tk
import cv2
from PIL import Image, ImageTk
import facial
import compare_face
import threading

# class videoStream(threading.Thread):
	# def __init__(self):

# Layout setup
width, height = 400, 400
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
	# root.after(2000, facial.save_faces(people,folder=folder,webcam=webcam))
	root.after(5, update)

def show_frame():
	global people

	(frame, people) = facial.recog(people, cap)
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
root.geometry('800x800')
lmain = tk.Label(root)
lmain2 = tk.Label(root)
lmain3 = tk.Label(root)





lmain.pack(side=tk.LEFT)
lmain2.pack(side=tk.RIGHT)
lmain3.pack(side=tk.RIGHT)


lmain.config(width=400, height=400)
lmain2.config(width=600, height=600)
lmain3.config(width=600, height=600)

labels = []
labels.append(lmain2)
labels.append(lmain3)

def refreshPeople(people):
	print [person.getName() for person in people]
	# for r in range(2):
		# for c in range(2):
	try:
		if people:
			for i in range(len(people)):
				img = Image.fromarray(people[i].getFaces()[0][0][:,:,::-1])
				imgtk = ImageTk.PhotoImage(image=img)
				labels[i].imgtk = imgtk
				labels[i].configure(image=imgtk)
			# exit()

			# if people[r+c].getName() == 'p0':
			# 	tk.Label(lmain2, bg='red', width=10, height=10).grid(column=c,row=r)
			# elif people[r+c].getName() == 'p1':
			# 	tk.Label(lmain2, bg='blue', width=10, height=10).grid(column=c,row=r)
			# elif people[r+c].getName() == 'p2':
			# 	tk.Label(lmain2, bg='green', width=10, height=10).grid(column=c,row=r)
			# tk.Label(lmain2, width=10, height=10, bg="red").grid(column=c,row=r)

	except Exception as e:
		pass


root.after(10, update)
root.mainloop()
