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

	# print ([person.getPersonEncoding()[0] for person in people],len([person.getPersonEncoding() for person in people]))

	compareList = []
	for i in range(0,len(people)):
		a = face_recognition.face_distance([person.getPersonEncoding()[0] for person in people][i], encoding)
		print a
		for x in a:
			compareList.append(a)
		# cv2.waitKey(0)

	b = sorted(enumerate(compareList),key=lambda x:x[1])
	print b

	if b[0][1] < .62:
			people[b[0][0]].addFaces((face, encoding))
	else:
		print 'adding new person...'
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
	def getPersonEncoding(self):
		return self.faces[0][1]