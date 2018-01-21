import cv2
import face_recognition


def manageFaces(people, encoding):

	print ([person.getNumFrames() for person in people], len(people), len(encoding))

	if not people:
		print 'people is empty.. creating'
		p1 = Person(str('p'+str(len(people))))
		p1.addEncoding(encoding)
		people.append(p1)
		return (people, p1.getName())

	a = face_recognition.face_distance(list([person.getPersonEncoding() for person in people]), encoding)
	b = sorted(enumerate(a),key=lambda x:x[1])
	# print b

	if b[0][1] < .53:
		people[b[0][0]].addEncoding(encoding)
		name = people[b[0][0]].getName()
		
	else:
		print 'adding new person...'
		p2 = Person(str('p'+str(len(people))))
		p2.addEncoding(encoding)
		people.append(p2)
		name = p2.getName()
	
	return (people, name)

class Person():
	def __init__(self, name):
		self.name = name
		self.faces = []
		self.numFrames = 0
		self.encodings = []

	def addFace(self, filename):
		self.faces.append(filename)
		self.numFrames+=1
	def addEncoding(self, encoding):
		self.encodings.append(encoding)
	def getName(self):
		return self.name
	def getFaces(self):
		return self.faces
	def getNumFrames(self):
		return self.numFrames
	def getPersonEncoding(self):
		return self.encodings[0]

	@staticmethod
	def getPerson(name, people):
		if name in [person.getName() for person in people]:
			return people[[person.getName() for person in people].index(name)]