from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.db.models import Count
from operator import attrgetter

import datetime

from .models import *


def home(request):
	if "userid" in request.session:
		return HttpResponseRedirect(reverse('CRM:index'))
	if request.method == 'POST':
		userid = request.POST.get('username', '')
		password = request.POST.get('password', '')
		
		c = {}
		c.update(csrf(request))
		try:
			user = User.objects.get(userid = userid)
		except (KeyError, User.DoesNotExist):
			c.update({'err_msg' : 'Incorrect Username'})
			return render(request, 'home.html', c)
		else:
			if password != user.password:
				c.update({'err_msg' : 'Incorrect Password'})
				return render(request, 'home.html', c)
			request.session['userid'] = userid

			role = user.Role
			if role == 2 :
				return HttpResponseRedirect(reverse('CRM:index'))
			else :
				return HttpResponseRedirect(reverse('CRM:index_stu'))


	c = {}
	c.update(csrf(request))
	return render(request, 'home.html', c)
	
def index(request):
	if "userid" in request.session:
		user = User.objects.get(userid = request.session['userid'])
		return render(request, 'index.html', {'user' : user})
	else:
		return HttpResponseRedirect(reverse('CRM:home'))

def index_stu(request):
	if "userid" in request.session:
		user = User.objects.get(userid = request.session['userid'])
		return render(request, 'index_stu.html', {'user' : user})
	else:
		return HttpResponseRedirect(reverse('CRM:home'))

def logout(request):
	if "userid" in request.session:
		try:
			del request.session['userid']
		except (KeyError):
			return HttpResponseRedirect(reverse('CRM:index'))
		return HttpResponseRedirect(reverse('CRM:home'))
	else:
		return HttpResponseRedirect(reverse('CRM:home'))

def BookExtra(request):
	

	if request.method == 'POST':
		courseno = request.POST.get('courseno', '')
		occupancy = request.POST.get('occupancy', '')
		t = request.POST.get('type', '')
		date = request.POST.get('date', '')
		time = request.POST.get('time', '')
		

		day = datetime.datetime.strptime(date, '%Y-%m-%d').date().weekday()

		allRooms = Room.objects.all()
		allBookings = Booking.objects.all()

		availRooms = []

		for rm in allRooms:
			available = True
			if str(rm.Type) == str(t) and int(rm.Occupancy) >= int(occupancy):
				for b in allBookings:
					if str(rm.RoomNo) == str(b.room.RoomNo) and str(b.time) == str(time) and str(b.date) == str(date):
						available = False
				if available:
					try:
						sb = Booking_sem.objects.filter(room = rm)
					except (KeyError, Booking_sem.DoesNotExist):
						availRooms.append(rm)
					else:
						available1 = True
						for sb1 in sb:
							if str(sb1.day) == str(day) and str(sb1.time) == str(time):
								available1 = False
						if available1:
							availRooms.append(rm)

		availRooms = sorted(availRooms, key = attrgetter('RoomNo'))
		c = {}
		c = c.update(csrf(request))
		c_new = {}
		if availRooms.__len__():
			c_new = ({'availRooms' : availRooms, 'available' : '1', 'searched' : '1', 'date' : date, 'time' : time, 'CourseNo' : courseno })
		else:
			c_new = ({'available' : '0', 'searched' : '1'})

		# c.update(c_new)
		print(c_new)
		return render(request, 'BookExtra.html', c_new)

	else:
		return render(request, 'BookExtra.html', {'searched' : '0'})

def BookRoom(request):
	if "userid" in request.session:
		if request.method == 'POST':
			user = User.objects.get(userid = request.session['userid'])
			roomno = request.POST.get('roomno', '')
			time = request.POST.get('time', '')
			book_for_sem = request.POST.get('book_for_sem', '')
			if book_for_sem == '1':
				day = request.POST.get('day', '')
			else:
				date = request.POST.get('date', '')
			
			courseno = request.POST.get('courseno', '')
			if roomno != '':
				try:
					rm = Room.objects.get(RoomNo = roomno)
				except (KeyError, Room.DoesNotExist):
					return HttpResponseRedirect(reverse('CRM:index'))
				else:
					if book_for_sem == '1':
						b = Booking_sem(room = rm, time = time, day = day, CourseNo = courseno ,bookedBy = user)
					else:
						b = Booking(room = rm, time = time, date = date, CourseNo = courseno ,bookedBy = user)
					b.save()
				if book_for_sem == '1':
					return render(request, 'Booksem.html', {'bookingSuccess' : 1})
				return render(request, 'BookExtra.html', {'bookingSuccess' : 1})
			else:
				return HttpResponseRedirect(reverse('CRM:index'))	
		else:
			return HttpResponseRedirect(reverse('CRM:index'))
	else:
		return HttpResponseRedirect(reverse('CRM:home'))

def time_table(request):
	if "userid" in request.session:
		user = User.objects.get(userid = request.session['userid'])
		allSemBookings = Booking_sem.objects.all().order_by('day')
		timeTable = [[],[],[],[],[],[],[]]
		role = user.Role

		for b in allSemBookings:
			obj = {
				'roomno' : b.room.RoomNo,
				'day' : b.day,
				'time_slot1' : '',
				'time_slot2' : '',
				'time_slot3' : '',
				'time_slot4' : '',
				'time_slot5' : '',
				'time_slot6' : '',
				'time_slot7' : '',
				'time_slot8' : '',
				'time_slot9' : '',
			}
			found = False
			for o in timeTable[b.day]:
				if o['roomno'] == b.room.RoomNo and o['day'] == b.day:
					found = True
					if b.time == "8AM-9AM":
						o.update({'time_slot1' : b.CourseNo})
					elif b.time == "9AM-10AM":
						o.update({'time_slot2' : b.CourseNo})
					elif b.time == "10AM-11AM":
						o.update({'time_slot3' : b.CourseNo})
					elif b.time == "11AM-12PM":
						o.update({'time_slot4' : b.CourseNo})
					elif b.time == "12PM-1PM":
						o.update({'time_slot5' : b.CourseNo})
					elif b.time == "1PM-2PM":
						o.update({'time_slot6' : b.CourseNo})
					elif b.time == "2PM-3PM":
						o.update({'time_slot7' : b.CourseNo})
					elif b.time == "3PM-4PM":
						o.update({'time_slot8' : b.CourseNo})
					else:
						o.update({'time_slot9' : b.CourseNo})
					break
			if found == False:
				if b.time == "8AM-9AM":
					obj.update({'time_slot1' : b.CourseNo})
				elif b.time == "9AM-10AM":
					obj.update({'time_slot2' : b.CourseNo})
				elif b.time == "10AM-11AM":
					obj.update({'time_slot3' : b.CourseNo})
				elif b.time == "11AM-12PM":
					obj.update({'time_slot4' : b.CourseNo})
				elif b.time == "12PM-1PM":
					obj.update({'time_slot5' : b.CourseNo})
				elif b.time == "1PM-2PM":
					obj.update({'time_slot6' : b.CourseNo})
				elif b.time == "2PM-3PM":
					obj.update({'time_slot7' : b.CourseNo})
				elif b.time == "3PM-4PM":
					obj.update({'time_slot8' : b.CourseNo})
				else:
					obj.update({'time_slot9' : b.CourseNo})
				timeTable[b.day].append(obj)
		print("timeTable : " + str(timeTable))

		return render(request, 'time_table.html', {'user' : user,
												   'timeTable' : timeTable, 'role': role})
	else:
		return HttpResponseRedirect(reverse('CRM:home'))

def extra_table(request):
	if "userid" in request.session:
		user = User.objects.get(userid = request.session['userid'])
		role=user.Role
		# return render(request, 'extra_table.html', {'user' : user, 'role' : role})
		allbookings  = Booking.objects.all().order_by('date')

		return render(request, 'extra_table.html', {'user' : user, 'allbookings' : allbookings, 'role' : role})
	else:
		return HttpResponseRedirect(reverse('CRM:home'))


def booksem(request):
	if request.method == 'POST':
		courseno = request.POST.get('courseno', '')
		occupancy = request.POST.get('occupancy', '')
		t = request.POST.get('type', '')
		day = request.POST.get('day', '')
		time = request.POST.get('time', '')

		# try:
		# 	q1=Booking.objects.get()


		allRooms = Room.objects.all()
		allBookings = Booking_sem.objects.all()

		availRooms = []

		for rm in allRooms:
			available = True
			if str(rm.Type) == str(t) and int(rm.Occupancy) >= int(occupancy):
				for b in allBookings:
					if str(rm.RoomNo) == str(b.room.RoomNo) and str(b.time) == str(time) and str(b.day) == str(day):
						available = False
				if available:
					availRooms.append(rm)

		c = {}
		c = c.update(csrf(request))
		c_new = {}
		if availRooms.__len__():
			c_new = ({'availRooms' : availRooms, 'available' : '1', 'searched' : '1', 'day' : day, 'time' : time, 'CourseNo' : courseno })
		else:
			c_new = ({'available' : '0', 'searched' : '1'})

		# c.update(c_new)
		print(c_new)
		return render(request, 'Booksem.html', c_new)

	else:
		return render(request, 'Booksem.html', {'searched' : '0'})

def book_his(request):
	if "userid" in request.session:
		user = User.objects.get(userid = request.session['userid'])
		allbookings  = Booking.objects.filter(bookedBy=user)
		scs_msg = ""
		if request.method=="POST":
			roomno=request.POST.get('roomno','')
			time1=request.POST.get('time','')
			room1=Room.objects.get(RoomNo=roomno)
			q1=Booking.objects.get(room=room1,time=time1)
			q1.delete()
			scs_msg = "Successfully deleted"
		return render(request, 'book_his.html', {'user' : user, 'allbookings' : allbookings, 'scs_msg' : scs_msg})
	else:
		return HttpResponseRedirect(reverse('CRM:home'))


def sem_his(request):
	if "userid" in request.session:
		user = User.objects.get(userid = request.session['userid'])
		allbookings  = Booking_sem.objects.filter(bookedBy=user)
		scs_msg = ""
		if request.method=="POST":
			roomno=request.POST.get('roomno','')
			day=request.POST.get('day','')
			courseno = request.POST.get('courseno', '')
			room1=Room.objects.get(RoomNo=roomno)
			q1=Booking_sem.objects.get(room=room1,day=day,CourseNo = courseno)
			q1.delete()
			scs_msg = "Successfully deleted"
		return render(request, 'sem_his.html', {'user' : user, 'allbookings' : allbookings, 'scs_msg' : scs_msg})
	else:
		return HttpResponseRedirect(reverse('CRM:home'))


		#