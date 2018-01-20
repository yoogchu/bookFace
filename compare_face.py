import numpy as np
import cv2
import face_recognition
from os import listdir

def manageFaces(persons, face, encoding):
	people, numPeople = persons[0], persons[1]
	print 'cf'

	print ([person.getNumFrames() for person in people], numPeople)

	if not people:
		numPeople+=1
		p1 = Person(str(numPeople))
		p1.addFaces((face, encoding))
		people.append(p1)
		return (people,numPeople)

	# print people[numPeople].getFaces()[0][1][0]
	# if face_recognition.compare_faces(people[numPeople].getFaces()[0][1][0], encoding, tolerance=.4):
	a = face_recognition.face_distance(people[numPeople-1].getFaces()[0][1][0], encoding)
	print a
	if a < .5:
			people[numPeople-1].addFaces((face, encoding))
	else:
		print 'adding new person'
		numPeople+=1
		p2 = Person(str(numPeople))
		p2.addFaces((face, encoding))
		people.append(p2)

	return (people, numPeople)

class Person():
	def __init__(self, name):
		self.name = name
		self.faces = []
		self.numFrames = 0
	def addFaces(self, filename):
		self.faces.append(filename)
		self.numFrames+=1
	def getName(self):
		return self.name
	def getFaces(self):
		return self.faces
	def getNumFrames(self):
		return self.numFrames