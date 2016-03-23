from django.db import models


# Create your models here.
Role = (
	(1, 'Student'),
(2, 'Faculty')

)

class User(models.Model):
	userid = models.CharField(max_length=10, blank= False, null = False, primary_key=True)
	password = models.CharField(max_length=30, blank= False, null= False)
	name = models.CharField(max_length=20, blank= False, null= False)
	email = models.EmailField()
	contactno = models.IntegerField()
	Role =  models.IntegerField(choices=Role, default=1) 

	def __str__(self):
		retstr = str(self.name) + ","
		if self.Role == 1:
			retstr += 'Student'
		else:
			retstr += 'Faculty'
		return retstr
	

Type = (
	(1, 'Projector'),
	(2, 'Video Conferencing')
	)

class Room(models.Model):
	RoomNo = models.IntegerField()
	Occupancy = models.IntegerField()
	Type = models.IntegerField(choices=Type, default=1)
	
	def __str__(self):
		retstr = str(self.RoomNo) + "," + str(self.Occupancy) + ","
		if self.Type == 1:
			retstr += 'Projector'
		else:
			retstr += 'Video Conferencing'
		return retstr


class Booking(models.Model):
	room = models.ForeignKey('Room', on_delete = models.CASCADE)
	time = models.CharField(max_length=11, default='')
	date = models.DateField()
	CourseNo = models.CharField(max_length=11, default='')
	bookedBy = models.ForeignKey('User', on_delete = models.CASCADE)
	

	def __str__(self):
		return str(self.room.RoomNo) + "------" + str(self.date)  + "------" + " (" + self.time + ")------" +  self.CourseNo + "------" + self.bookedBy.name 




class Booking_sem(models.Model):
	room = models.ForeignKey('Room', on_delete = models.CASCADE)
	time = models.CharField(max_length=11, default='')
	day = models.IntegerField()
	CourseNo = models.CharField(max_length=11, default='')
	bookedBy = models.ForeignKey('User', on_delete = models.CASCADE)

	def __str__(self):
		return str(self.room.RoomNo) + "------" + str(self.day)  + "------" + " (" + self.time + ")------" +  self.CourseNo + "------" + self.bookedBy.name 
	