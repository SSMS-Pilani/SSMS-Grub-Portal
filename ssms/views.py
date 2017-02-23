from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from ssms.models import Grub,Grub_Coord,Grub_Student,Veg,NonVeg,Both,Student,DateMailStatus
from ssms.forms import GrubForm,Grub_CoordUserForm,Grub_CoordUserProfileForm,ExcelUpload,VegForm,NonVegForm,BothForm,CoordStudentRegForm, GrubFormEdit , UploadFileForm
from django.conf import settings
#addddddd
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.template import RequestContext
import django_excel as excel
from datetime import datetime,date,timedelta
from django.core.mail import send_mail,send_mass_mail
from django.views.decorators.cache import cache_control
import xlsxwriter
####
#from django_cron import CronJobBase, Schedule


def datechecker(gmid):
	grub = Grub.objects.get(gm_id=gmid)
	c=date.today()
	d=0
	if (grub.deadline2>c):     # coord reg open
		return 2
	elif (grub.deadline >=c and grub.deadline2<= c):   #student register/cancel  , coord reg closed
		return 1	
	elif (grub.deadline <c and grub.date>=c):   #student reg/cancel closed
		return 3
	elif (grub.date<c):    # coord spot signing upload
		return 4



def home(request):
	return render(request, 'ssms/home.html')
def about(request):
	return render(request, 'ssms/about.html')
def contact(request):
	return render(request, 'ssms/contact.html')

#To be triggered
from django.core.mail import EmailMultiAlternatives


def send(request):
	if request.user.is_superuser:
		grub=Grub.objects.filter(status="Active",mails="Not Sent")
		c=date.today()
		d=timedelta(days=1)
		f=c+d
		b=[]
		for i in grub:
		
			d = datetime.strptime(str(i.date), '%Y-%m-%d')
			e = date.strftime(d, "%d %B %Y")
			v = datetime.strptime(str(i.deadline), '%Y-%m-%d')
			h = date.strftime(v, "%d %B %Y")
			if (c==i.deadline2 or f==i.deadline2):
				abcd=Grub_Student.objects.filter(gm_id=i.gm_id,status="Signed Up")
				#return HttpResponse(abcd)
				k=len(abcd)//99
				#return HttpResponse(i.name,k)
				for q in range(k+1):
					a=[]
					students=abcd[q*99:(q+1)*99] 
					for j in students:
						a.append(str(j.user_id)+"@pilani.bits-pilani.ac.in")
						j.mail = "Sent"
						j.save()
					print a
				
					subject, from_email = str(i.name), 'ssms.pilani@gmail.com'
					text_content = 'This is an important message.'
					html_content = "<body><p>This is to inform you that you have been signed up for the <strong> "+str(i.name)+"</strong> that is to take place on <strong>"+ e +"</strong> </p> <p>In case you wish to cancel your signing, please visit <a href=http://grub.ssms-pilani.org/ssms/student/grub/"+str(i.gm_id)+"/ >SSMS Grub Portal</a>, before 12 midnight,<strong>" + h +"</strong>. Any requests made after the deadline will not be entertained. </p><p>If you receive your stub even after cancellation, do not give it to anybody else; please return it to the SSMS office in FD II with your name and ID number written on the back. Else, your cancellation will be treated as invalid. </p><p>Thank you.</p><p>Grub Committee, SSMS</p></body>"
					msg = EmailMultiAlternatives(subject, text_content, from_email, cc = a, bcc=["f2014623@pilani.bits-pilani.ac.in", "f2015040@pilani.bits-pilani.ac.in"])
					msg.attach_alternative(html_content, "text/html")
					msg.send(fail_silently=False)
					b.append("Sent mail for " + str(i.name) + " to " + str(len(a)) +str(a))
				i.mails="Sent"
				i.save()
			
		return HttpResponse("Sent python mail" + str(b) )
		#return HttpResponseRedirect("/ssms")
	else :
		return HttpResponseRedirect("/ssms")

def send2(request):
	if request.user.is_superuser:
		grub=Grub.objects.filter(status="Active",mails="Sent")
		c=date.today()
		d=timedelta(days=1)
		f=c+d
		b=[]
		for i in grub :
			if (i.meal=="Veg"):
				veg = Veg.objects.get(gm_id=i.gm_id)
				meal = str(veg.v_venue)
			elif (i.meal=="Non Veg"):
				veg = NonVeg.objects.get(gm_id=i.gm_id)
				meal = str(veg.n_venue)
			else :
				veg = Veg.objects.get(gm_id=i.gm_id)
				veg2 = NonVeg.objects.get(gm_id=i.gm_id)
				meal = str(veg.v_venue) + " and "  +str(veg2.n_venue)
			d = datetime.strptime(str(i.date), '%Y-%m-%d')
			e = date.strftime(d, "%d %B %Y")
			if (c==i.date or f==i.date):
				abcd=Grub_Student.objects.filter(gm_id=i.gm_id,status="Signed Up")
				k=len(abcd)//99
				#return HttpResponse(len(abcd))
				#return HttpResponse(i.name,k)
				for q in range(k+1):
					a=[]
					students=abcd[q*99:(q+1)*99] 
					for j in students:
						a.append(str(j.user_id)+"@pilani.bits-pilani.ac.in")
						j.mail = "Sent"
						j.save()
					print a
					subject, from_email = str(i.name) + " (Reminder)", 'ssms.pilani@gmail.com'
					text_content = 'This is an important message.'
					html_content = "<body><p>This is to remind you that you that you have been signed up for <strong> "+str(i.name)+"</strong> which will take place on <strong>"+ e +"</strong> at the <strong>"+meal+"</strong> Mess. </p> <p>Wristbands for the same are available at your mess counter, and you are requested to collect the same if you haven't already.</p><strong><p>Entry into the grub shall not be allowed if you are not wearing the wristband.</p></strong><p>Limited on spot signings will be available. Please carry your ID cards for the same. </p><p>Thank you.</p><p>Grub Committee, SSMS</p></body>"
					msg = EmailMultiAlternatives(subject, text_content, from_email, cc = a, bcc=["f2014623@pilani.bits-pilani.ac.in", "f2015040@pilani.bits-pilani.ac.in"])
					msg.attach_alternative(html_content, "text/html")
					msg.send(fail_silently=False)
					b.append("Sent mail for " + str(i.name) + " to " + str(len(a)) +str(a))
				i.mails="Sent2"
				i.save()
			
		return HttpResponse("Sent python mail" + str(b) )
	else :
		return HttpResponseRedirect("/ssms")
	
	    
def ssms_grub_sendmail1(request,gmid):
	grubid = request.GET.get('grubid')
	datemail = DateMailStatus.objects.get(date=datetime.now())
	print(gmid)
	try:
		grub = Grub.objects.get(name=str(grubid))
		print(gmid)
		d = datetime.strptime(str(grub.date), '%Y-%m-%d')
		e = date.strftime(d, "%d %B %Y")
		v = datetime.strptime(str(grub.deadline), '%Y-%m-%d')
		h = date.strftime(v, "%d %B %Y")
		abcd=Grub_Student.objects.filter(gm_id=grub.gm_id,status="Signed Up",mail="Not Sent")
		print e
		print h
		k=len(abcd)//99
		count=0
		for q in range(k+1):
			a=[]
			students=abcd[q*99:(q+1)*99] 
			for j in students:
				a.append(str(j.user_id)+"@pilani.bits-pilani.ac.in")
				j.mail = "Sent"
				j.save()
			print a
			subject, from_email = str(grub.name), 'ssms.pilani@gmail.com'
			text_content = 'This is an important message.'
			html_content = "<body><p>This is to inform you that you have been signed up for the <strong> "+str(grub.name)+"</strong> that is to take place on <strong>"+ e +"</strong> </p> <p>In case you wish to cancel your signing, please visit <a href=http://grub.ssms-pilani.org/ssms/student/grub/"+str(grub.gm_id)+"/ >SSMS Grub Portal</a>, before 12 midnight,<strong>" + h +"</strong>. Any requests made after the deadline will not be entertained. </p><p>If you receive your stub even after cancellation, do not give it to anybody else; please return it to the SSMS office in FD II with your name and ID number written on the back. Else, your cancellation will be treated as invalid. </p><p>Thank you.</p><p>Grub Committee, SSMS</p></body>"
			msg = EmailMultiAlternatives(subject, text_content, from_email, cc = a, bcc=["f2014623@pilani.bits-pilani.ac.in", "f2015040@pilani.bits-pilani.ac.in"])
			msg.attach_alternative(html_content, "text/html")
			print a
			try :
				msg.send(fail_silently=False)
				count=count + len(a)
				datemail.mails = datemail.mails+len(a)
				datemail.save()
			except :
				for j in students:
					j.mail = "Not Sent"
					j.save()
				left = len(abcd)-count
				data ={'is_taken': "Only "+str(count)+" mails were sent succesfully. " + str(left) +" mails are left to be send." }
				return JsonResponse(data)
		grub.mails="Sent"
		grub.save()
		print(gmid)
		data = {'is_taken': "All the mails ("+ str(len(abcd)) +") were sent succesfully"}
		return JsonResponse(data)
	except :
		print("here")
		data = {'is_taken': "Internal Error"}
		return JsonResponse(data)

def ssms_grub_sendmail2(request,gmid):
	grubid = request.GET.get('grubid')
	datemail = DateMailStatus.objects.get(date=datetime.now())
	print(gmid)
	try:
		grub = Grub.objects.get(name=str(grubid))
		print(gmid)
		if (grub.meal=="Veg"):
			veg = Veg.objects.get(gm_id=grub.gm_id)
			meal = str(veg.v_venue)
		elif (grub.meal=="Non Veg"):
			veg = NonVeg.objects.get(gm_id=grub.gm_id)
			meal = str(veg.n_venue)
		else :
			veg = Veg.objects.get(gm_id=grub.gm_id)
			veg2 = NonVeg.objects.get(gm_id=grub.gm_id)
			meal = str(veg.v_venue) + " and " + str(veg2.n_venue)
		d = datetime.strptime(str(grub.date), '%Y-%m-%d')
		e = date.strftime(d, "%d %B %Y")
		abcd=Grub_Student.objects.filter(gm_id=grub.gm_id,status="Signed Up")
		print e
		k=len(abcd)//99
		count=0
		for q in range(k+1):
			a=[]
			students=abcd[q*99:(q+1)*99] 
			for j in students:
				a.append(str(j.user_id)+"@pilani.bits-pilani.ac.in")
				j.mail = "Sent2"
				j.save()
			print a
			subject, from_email = str(grub.name) + " (Reminder)", 'ssms.pilani@gmail.com'
			text_content = 'This is an important message.'
			html_content = "<body><p>This is to remind you that you that you have been signed up for <strong> "+str(grub.name)+"</strong> which will take place on <strong>"+ e +"</strong> at the <strong>"+meal+"</strong> Mess. </p> <p>Wristbands for the same are available at your mess counter, and you are requested to collect the same if you haven't already.</p><strong><p>Entry into the grub shall not be allowed if you are not wearing the wristband.</p></strong><p>Limited on spot signings will be available. Please carry your ID cards for the same. </p><p>Thank you.</p><p>Grub Committee, SSMS</p></body>"
			print a
			msg = EmailMultiAlternatives(subject, text_content, from_email, cc = a, bcc=["f2014623@pilani.bits-pilani.ac.in", "f2015040@pilani.bits-pilani.ac.in"])
			msg.attach_alternative(html_content, "text/html")
			try :
				msg.send(fail_silently=False)
				count = count + len(a)
				datemail.mails = datemail.mails+len(a)
				datemail.save()
			except :
				for j in students:
					j.mail = "Sent"
					j.save()
				left = len(abcd)-count
				data ={'is_taken': "Only "+str(count)+" mails were sent succesfully. " + str(left) +" mails are left to be send." }
				return JsonResponse(data)
		grub.mails="Sent"
		grub.save()
		print(gmid)
		data = {'is_taken': "All the mails ("+ str(len(abcd)) +") were sent succesfully"}
		return JsonResponse(data)
	except :
		print("here")
		data = {'is_taken': "Internal Error"}
		return JsonResponse(data)
	
	    
def ssms_grub_sendmail(request,gmid):
	context_dict={}
	try:
		grub = Grub.objects.get(gm_id=gmid)
		context_dict["grub"]=grub
		stud = Grub_Student.objects.filter(gm_id=gmid,status="Signed Up")
		registered=len(stud)
		context_dict["registered"]=registered
		if(DateMailStatus.objects.filter(date=datetime.now()).exists()):
			datemail = DateMailStatus.objects.get(date=datetime.now())
			context_dict["datemail"]=datemail
		else :
			datemail = DateMailStatus.objects.create(date=datetime.now(),mails=0)
			context_dict["datemail"]=datemail
		mailsleft = 1000 - datemail.mails
		context_dict["mailsleft"]=mailsleft
	except:
		pass	
		return HttpResponseRedirect('/ssms/')
	return render(request,'ssms/ssms_grub_sendmail.html',context_dict)
		
def index(request):
	if not request.user.is_authenticated():
		return render(request, 'ssms/index.html')
	else:
	
		try:
			coord=Grub_Coord.objects.get(user=request.user)
			grub=Grub.objects.filter(cg_id=coord.cg_id).order_by('-date')
			context_dict={'grub':grub,'coord':coord}
			return render(request, 'ssms/index.html',context_dict)
		except Grub_Coord.DoesNotExist:
			context_dict={}
			pass
		try:
			stud= Student.objects.get(user_id=str(request.user))
			context_dict={'student':stud}
			return render(request, 'ssms/index.html',context_dict)
		except Student.DoesNotExist:
			context_dict={}
			pass
		return render(request, 'ssms/index.html',context_dict)

def ssms_login(request):
	context_dict={}
    	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user and user.is_superuser:
		    	if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/ssms/')
		    	else:
				return HttpResponse("Your ssms account is disabled.")
		else:
			
			context_dict['invalid']="Invalid login details supplied."
		    	return render(request, 'ssms/ssms_login.html',context_dict)

    	else:
		
		return render(request, 'ssms/ssms_login.html')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ssms_register(request):
	if request.user.is_superuser:
		registered = False
		if request.method == 'POST':
			user_form = Grub_CoordUserForm(data=request.POST)
			profile_form = Grub_CoordUserProfileForm(data=request.POST)
			if user_form.is_valid() and profile_form.is_valid():
				user = user_form.save(commit=False)
				user.set_password(user.password)
				user.is_staff=True
			
				profile = profile_form.save(commit=False)
			
				profile.status="Active"
				profile.date=datetime.now()
				profile.reg_by=str(request.user)
				user.save()
				profile.user = user
				profile.save()
				registered = True


			else:
				print user_form.errors
				print profile_form.errors

		else:
			user_form = Grub_CoordUserForm()
			profile_form = Grub_CoordUserProfileForm()
		return render(request,'ssms/ssms_register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
	else :
		return HttpResponseRedirect('/ssms/ssms/login/')
	
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ssms_grubinfo(request,gmid):
	if request.user.is_superuser:
		e=datechecker(gmid)
		context_dict = {}
	    	try:
			grub = Grub.objects.get(gm_id=gmid)
			if (grub.meal=='Veg'):
				b=Veg.objects.get(gm_id=gmid)
				i=0
			elif (grub.meal=='Non Veg'):
				b=NonVeg.objects.get(gm_id=gmid)
				i=1
			elif (grub.meal=='Both'):
				b=Both.objects.get(gm_id=gmid)
				i=2
			context_dict['grub'] = grub
			context_dict['meal'] = b
			context_dict['i'] = i
			context_dict['e'] = e
	    	except Grub.DoesNotExist:
			pass
    		return render(request, 'ssms/ssms_grubinfo.html', context_dict)
	else :
		return HttpResponseRedirect('/ssms/ssms/login/')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ssms_grub_list(request):
	if request.user.is_superuser:
		grub_list=Grub.objects.order_by('-date')[:]
		coord_list=Grub_Coord.objects.all()
		context_dict={"grub":grub_list,"coord":coord_list}
		return render(request, 'ssms/ssms_grublist.html',context_dict)
	else :
		return HttpResponseRedirect('/ssms/ssms/login/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ssms_student_table(request,gmid):
	if request.user.is_superuser:
		grub=Grub.objects.get(gm_id=gmid)
		stud = Grub_Student.objects.filter(gm_id=gmid)
		registered=len(stud.filter(status="Signed Up"))
		out=len(stud.filter(status="Opted Out"))
		context_dict={"stud":stud,"reg":registered,"out":out,"gmid":gmid,"grub":grub}
		return render(request, 'ssms/dynamic_table.html',context_dict)
	elif request.user.is_staff :
		try :
			grub =Grub.objects.get(gm_id=gmid)
			form = ExcelUpload(instance=grub)
			e=datechecker(gmid)
			coord = Grub_Coord.objects.get(cg_name=grub.cg_id)
			if request.user == coord.user:
				grub=Grub.objects.get(gm_id=gmid)
				stud = Grub_Student.objects.filter(gm_id=gmid)
				registered=len(stud.filter(status="Signed Up"))
				out=len(stud.filter(status="Opted Out"))
				context_dict={"stud":stud,"reg":registered,"out":out,"gmid":gmid,"grub":grub}
				return render(request, 'ssms/dynamic_table.html',context_dict)
			else :
				return HttpResponseRedirect("/ssms")
		except Grub.DoesNotExist:
			pass
			return HttpResponseRedirect("/ssms")
	else:
		return HttpResponseRedirect('/ssms/ssms/login/')



from django.contrib.auth.models import User



def ssms_coord_active(request,cgid):
	if request.user.is_superuser:
		a=Grub_Coord.objects.get(cg_id=cgid)
		b=User.objects.get(username=a.user)
		c=Grub.objects.filter(cg_id=cgid)
		for i in c:
			i.status="Active"
			i.save()
		b.is_staff=True
		b.is_active=True
		a.status="Active"
		a.save()
		b.save()
		return HttpResponseRedirect("/ssms/ssms/grublist/")
	else :
		return HttpResponseRedirect('/ssms/ssms/login/')



def ssms_coord_inactive(request,cgid):
	if request.user.is_superuser:
		a=Grub_Coord.objects.get(cg_id=cgid)
		b=User.objects.get(username=a.user)
		c=Grub.objects.filter(cg_id=cgid)
		for i in c:
			i.status="Inactive"
			i.save()
		b.is_staff=False
		b.is_active=False
		a.status="Inactive"
		a.save()
		b.save()
		return HttpResponseRedirect("/ssms/ssms/grublist/")
	else :
		return HttpResponseRedirect('/ssms/ssms/login/')

import os

def export_data(request, gmid):
	if request.user.is_staff:
		if request.method == "POST":
			try :
				grub =Grub.objects.get(gm_id=gmid)
				bh = request.POST.get('bhawan')
				if bh=="All":
					c = Grub_Student.objects.filter(gm_id=gmid,status="Signed Up")
				else :
					c = Grub_Student.objects.filter(gm_id=gmid,status="Signed Up",bhawan=bh)
				a= Grub.objects.get(gm_id=gmid)
		
				b=[]		
				for stu in c:
					b.append([stu.user_id,stu.name, stu.student_id, stu.meal,stu.bhawan,stu.room])
				print(b)
				workbook = xlsxwriter.Workbook('media/'+a.name+'_'+bh+'_grublist.xlsx')
				worksheet = workbook.add_worksheet()
				worksheet.set_column('A:A', 15)
				worksheet.set_column('B:B', 25)
				worksheet.set_column('C:C', 20)
				worksheet.set_column('D:D', 15)
				worksheet.set_column('E:E', 15)
				worksheet.set_column('F:F', 15)
				bold = workbook.add_format({'bold': 1})
				worksheet.write('A1', 'User ID', bold)
				worksheet.write('B1', 'Name', bold)
				worksheet.write('C1', 'BITS ID', bold)
				worksheet.write('D1', 'Meal Type', bold)
				worksheet.write('E1', 'Bhawan', bold)
				worksheet.write('F1', 'Room No.', bold)
				row = 1
				col = 0
				for i in b:
					worksheet.write_string  (row, col,i[0] )
					worksheet.write_string(row, col + 1, i[1] )
					worksheet.write_string  (row, col + 2,i[2] )
					worksheet.write_string  (row, col+3,i[3] )
					worksheet.write_string(row, col + 4, i[4] )
					worksheet.write_string  (row, col + 5,i[5] )
					row += 1
				workbook.close()
				return HttpResponseRedirect('media/'+a.name+'_'+bh+'_grublist.xlsx')
			except Grub.DoesNotExist:
				pass
				return HttpResponseRedirect("/ssms")
		else:
			return HttpResponseRedirect("/ssms")

	else :
		return HttpResponseRedirect('/ssms/')





def coord_login(request):
	context_dict={}
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

        	user = authenticate(username=username, password=password)

		if user and user.is_staff:
		    	if user.is_active:                                                 #add status  choice here
		        	login(request, user)
		        	return HttpResponseRedirect('/ssms/')
		    	else:
		        	return HttpResponse("Your ssms account is disabled.")	
		else:
			context_dict['invalid']="Invalid login details supplied."
		    	print "Invalid login details: {0}, {1}".format(username, password)
		    	return render(request,'ssms/coord_login.html', context_dict)

    	else:

       		return render(request, 'ssms/coord_login.html', {})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def coord_grub_register(request):
	if request.user.is_staff and not request.user.is_superuser:
		done=0
		if request.method == 'POST':
			form = GrubForm(request.POST,request.FILES)
			form1= VegForm(request.POST,request.FILES)
			form2= NonVegForm(request.POST,request.FILES)
			form3= BothForm(request.POST,request.FILES)
			if form.is_valid() and  form1.is_valid():
				a=form.save(commit=False)
				a.meal=request.POST.get('mealtype')
				a.date=request.POST.get('grubdate')
				a.reg_date=datetime.now()
				d=Grub_Coord.objects.get(user=request.user)
				a.cg_id=d
				a.save()
				qw=Grub.objects.get(gm_id = a.gm_id)
				b=qw.date
				c=timedelta(days=2)
				e=timedelta(days=4)
				a.deadline=b-c
				a.deadline2=b-e
				a.save()
		   		photo=form1.save(commit=False)
				photo.name=request.POST.get('name')
				photo.veg_price=request.POST.get('v_price')
				photo.veg_venue=request.POST.get('v_venue')
				d=Grub.objects.get(gm_id = a.gm_id)
				photo.gm_id=d
				if 'v_images' in request.FILES :
					photo.v_images = request.FILES['v_images']
			    		photo.save()
					done=1			
					
			
			elif form.is_valid() and  form2.is_valid():
				a=form.save(commit=False)
				a.meal=request.POST.get('mealtype')
				a.date=request.POST.get('grubdate')
				a.reg_date=datetime.now()
				d=Grub_Coord.objects.get(user=request.user)
				a.cg_id=d
				a.save()
				qw=Grub.objects.get(gm_id = a.gm_id)
				b=qw.date
				c=timedelta(days=2)
				e=timedelta(days=4)
				a.deadline=b-c
				a.deadline2=b-e
				a.save()
				photo=form2.save(commit=False)
				photo.veg_venue=request.POST.get('n_venue')
				photo.non_veg_venue=request.POST.get('n_venue')
				d=Grub.objects.get(gm_id = a.gm_id)
				photo.gm_id=d
				if 'n_images' in request.FILES :
					photo.n_images = request.FILES['n_images']
			    		photo.save()
					done=1
			
			elif form.is_valid() and  form3.is_valid():
				a=form.save(commit=False)
				a.meal=request.POST.get('mealtype')
				a.date=request.POST.get('grubdate')
				a.reg_date=datetime.now()
				d=Grub_Coord.objects.get(user=request.user)
				a.cg_id=d
				a.save()
				qw=Grub.objects.get(gm_id = a.gm_id)
				b=qw.date
				c=timedelta(days=2)
				e=timedelta(days=4)
				a.deadline=b-c
				a.deadline2=b-e
				a.save()
		   		photo=form3.save(commit=False)
				photo.veg_price=request.POST.get('veg_price')
				photo.non_veg_price=request.POST.get('non_veg_price')
				photo.veg_venue=request.POST.get('veg_venue')
				photo.non_veg_venue=request.POST.get('non_veg_venue')
				d=Grub.objects.get(gm_id = a.gm_id)
				photo.gm_id=d
				if 'veg_images' in request.FILES and 'non_veg_images' in request.FILES:
					photo.veg_images = request.FILES['veg_images']
					photo.non_veg_images = request.FILES['non_veg_images']
			    		photo.save()
					done=1
			
		   	else:
				print form.errors

		else:
			form = GrubForm()
			form1= VegForm()
			form2= NonVegForm()
			form3= BothForm()		
		return render(request, 'ssms/coord_grub_register.html', {'form': form,'form1':form1,'form2':form2,'form3':form3,'done':done})
	else :
		return HttpResponseRedirect('/ssms/coord/login/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def coord_upload(request,gmid):
	if request.user.is_staff and not request.user.is_superuser:
		try :
			grub =Grub.objects.get(gm_id=gmid)
			form = ExcelUpload(instance=grub)
			e=datechecker(gmid)
			coord = Grub_Coord.objects.get(cg_name=grub.cg_id)
			if request.user == coord.user:
				if (e==2 or e==4):
					if request.method == 'POST' and request.FILES:
						b=request.FILES['excel']
						filename=str(b.name)
						if filename.endswith('.xls') or filename.endswith('.xlsx') or filename.endswith('.csv'):
							a = Grub.objects.get(gm_id=gmid)
							d=Grub.objects.filter(gm_id=gmid)[0]
			
							form = ExcelUpload(request.POST,request.FILES,instance=grub)
							if form.is_valid():
						   		photo=form.save(commit=False)
								if 'excel' in request.FILES :
									def choice_func(row):
										a=row[0]
										a=str(a).upper()[:11]
										try :
											b=Student.objects.get(bits_id=str(a))
											smailid=b.user_id
											sname=b.name
											sbhawan=b.bhawan
											sroom=b.room_no
											row.append(smailid)
											row.append(sname)
											row.append(sbhawan)
											row.append(sroom)
										except :
											if a[4]=="H" or a[4]=="P":
												smailid=a[4]+a[0:4]+a[8:11]
												sname="User"
												sbhawan="Not Specified"
												sroom="Not Specified"
												row.append(smailid)
												row.append(sname)
												row.append(sbhawan)
												row.append(sroom)
											else :
												smailid="f"+a[0:4]+a[8:11]
												sname="User"
												sbhawan="Not Specified"
												sroom="Not Specified"
												row.append(smailid)
												row.append(sname)
												row.append(sbhawan)
												row.append(sroom)
										if str(row[1]).lower()=="veg":
											row[1]="Veg"
										elif str(row[1]).lower()=="non veg":
											row[1]="Non Veg"
										row.append("Signed Up")
										row.append(d)
									    	return row
									files=request.FILES['excel']
									files.save_to_database(
									model=Grub_Student,
									initializer=choice_func,
									mapdict=[ 'student_id','meal','user_id','name','bhawan', 'room','status','gm_id']
								    	)
							    		photo.excel = files
									photo.save()
									return HttpResponseRedirect("/ssms/stats/"+gmid)
							else:
								print form.errors
						else :
					
							invalid="Unsupported File type."
							return render(request, 'ssms/coord_upload.html', {'form': form,'grub':grub,"e":e,"invalid":invalid})
		
					else:
				
						form = ExcelUpload(instance=grub)
			
					return render(request, 'ssms/coord_upload.html', {'form': form,'grub':grub,"e":e})
				else:
					return render(request, 'ssms/coord_upload.html', {"e":e})
			else:
				return HttpResponseRedirect("/ssms")
		except Grub.DoesNotExist:
			pass
			return HttpResponseRedirect("/ssms")
	else :
			return HttpResponseRedirect('/ssms/coord/login/')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def coord_student_register(request,gmid):
	if request.user.is_staff and not request.user.is_superuser:
		try :
			grub =Grub.objects.get(gm_id=gmid)
			form = ExcelUpload(instance=grub)
			e=datechecker(gmid)
			coord = Grub_Coord.objects.get(cg_name=grub.cg_id)
			if request.user == coord.user:
				done=0
				if e==2:
					if request.method == 'POST': 
						form = CoordStudentRegForm(request.POST)    
						if form.is_valid():
							photo=form.save(commit=False)
							photo.student_id=photo.student_id.upper()
							try :
								gs=Grub_Student.objects.get(student_id=photo.student_id,gm_id=gmid)
								invalid="Student already registered."
								return render(request, 'ssms/coord_student_register.html',{'form': form,'done':done,'grub':grub,'e':e,"invalid":invalid})
							except Grub_Student.DoesNotExist:
								pass
							photo.status="Signed Up"
							photo.meal=request.POST.get('mealtype')
							a = photo.student_id
							photo.user_id="f"+a[0:4]+a[8:11]
							try :
								d=Student.objects.get(bits_id=a)
								photo.room=d.room_no
								photo.bhawan=d.bhawan
								photo.name=d.name
								b=Grub.objects.filter(gm_id=gmid)[0]
								photo.gm_id=b			
								photo.save()
								done=1
							except Student.DoesNotExist:
								pass
								invalid="Invalid ID"
								return render(request, 'ssms/coord_student_register.html',{'form': form,'done':done,'grub':grub,'e':e,"invalid":invalid})
							
						else:
							print form.errors
					else:
						form = CoordStudentRegForm()
						grub = Grub.objects.get(gm_id=gmid)
			
					return render(request, 'ssms/coord_student_register.html', {'form': form,'done':done,'grub':grub,'e':e})
				else:
					return render(request, 'ssms/coord_student_register.html', {'grub':grub,'e':e})
			else:
				return HttpResponseRedirect("/ssms")
		except Grub.DoesNotExist:
			pass
			return HttpResponseRedirect("/ssms")
	else :
		return HttpResponseRedirect('/ssms/coord/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def coord_view_grub(request,gmid):
	if request.user.is_staff and not request.user.is_superuser:
		try :
			grub =Grub.objects.get(gm_id=gmid)
			form = ExcelUpload(instance=grub)
			e=datechecker(gmid)
			coord = Grub_Coord.objects.get(cg_name=grub.cg_id)
			if request.user == coord.user:
				context_dict = {}
			    	try:
					grub = Grub.objects.get(gm_id=gmid)
					if (grub.meal=='Veg'):
						b=Veg.objects.get(gm_id=gmid)
						i=0
					elif (grub.meal=='Non Veg'):
						b=NonVeg.objects.get(gm_id=gmid)
						i=1
					elif (grub.meal=='Both'):
						b=Both.objects.get(gm_id=gmid)
						i=2
					context_dict['grub'] = grub
					context_dict['meal'] = b
					context_dict['i'] = i
					context_dict['e']=e
			    	except Grub.DoesNotExist:
					pass
			    	return render(request, 'ssms/coord_grubinfo.html', context_dict)
			else:
				return HttpResponseRedirect("/ssms")
		except Grub.DoesNotExist:
			pass
			return HttpResponseRedirect("/ssms")
	else :
		return HttpResponseRedirect('/ssms/coord/login/')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def coord_grub_edit(request,gmid):
	if request.user.is_staff and not request.user.is_superuser:
		try :
			grub =Grub.objects.get(gm_id=gmid)
			form = ExcelUpload(instance=grub)
			e=datechecker(gmid)
			coord = Grub_Coord.objects.get(cg_name=grub.cg_id)
			if request.user == coord.user:
				done=0
				inst = Grub.objects.get(gm_id=gmid)
				grub=Grub.objects.get(gm_id=gmid)
				if request.method == 'POST':
					form = GrubFormEdit(request.POST, instance=inst)		
					if form.is_valid():
						grub=form.save(commit=False)
						grub.save()
						done=1		
				   	else:
						print form.errors
				else:
					form = GrubFormEdit(instance=inst)		
				return render(request, 'ssms/coord_grub_edit.html', {'form': form,'done':done,'grub':grub})
			else:
				return HttpResponseRedirect("/ssms")
		except Grub.DoesNotExist:
			pass
			return HttpResponseRedirect("/ssms")
	else :
		return HttpResponseRedirect('/ssms/coord/login/')
	
# Coord do not have permission to cancel/activate grubs

def ssms_grub_inactive(request,gmid):
	if request.user.is_superuser:
		a=Grub.objects.get(gm_id=gmid)
		a.status="Inactive"
		a.save()
		return HttpResponseRedirect("/ssms/ssms/grub/"+gmid)
	else :
		return HttpResponseRedirect('/ssms/ssms/login/')


def ssms_grub_active(request,gmid):
	if request.user.is_superuser:
		a=Grub.objects.get(gm_id=gmid)
		a.status="Active"
		a.save()
		return HttpResponseRedirect("/ssms/ssms/grub/"+gmid)
	else :
		return HttpResponseRedirect('/ssms/ssms/login/')

"""
def student_login(request):
	return HttpResponse("working")

"""
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def student_upcoming_grubs(request):
	if request.user.is_authenticated() and not request.user.is_staff:
		c = date.today()
		grub_list=Grub.objects.filter(status="Active").order_by('-date')[:]
		context_dict={"grub":grub_list}
		return render(request, 'ssms/student_grublist.html',context_dict)
	else :
		return HttpResponseRedirect("/ssms/")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def student_grub_register(request, gmid):
	context_dict={}
	context_dict['gmid'] = gmid
	if request.user.is_authenticated() and not request.user.is_staff:
	    	try:
			grub = Grub.objects.get(gm_id=gmid,status="Active")
			if (grub.meal=='Veg'):
				b=Veg.objects.get(gm_id=gmid)
				i=0
			elif (grub.meal=='Non Veg'):
				b=NonVeg.objects.get(gm_id=gmid)
				i=1
			elif (grub.meal=='Both'):
				b=Both.objects.get(gm_id=gmid)
				i=2
			try :
				a = Grub_Student.objects.get(gm_id=gmid,user_id=str(request.user))
				context_dict['student']= a
			except Grub_Student.DoesNotExist:
				pass
			e=datechecker(gmid)
			context_dict['grub'] = grub
			context_dict['meal'] = b
			context_dict['i'] = i
			context_dict['e']=e
	    	except Grub.DoesNotExist:
			pass
	    	return render(request, 'ssms/student_grubinfo.html', context_dict)
	else :
		return render(request, 'ssms/student_grubinfo.html', context_dict)
		return HttpResponseRedirect("/soc/login/google-oauth2/?next=/ssms/student/grub/"+gmid)

def student_grub_register2(request, gmid):           #register for veg
	if request.user.is_authenticated() and not request.user.is_staff:
		try:
			grub = Grub.objects.get(gm_id=gmid,status="Active")
			d=datechecker(gmid)
			if (d==1 or d==2) :
				a = Grub.objects.filter(gm_id=gmid)[0]
				d= Student.objects.get(user_id=str(request.user))
				try :
					b=Grub_Student.objects.get(gm_id=gmid,user_id=str(request.user))
					b.meal="Veg"
					b.status="Signed Up"
					b.save()
				except Grub_Student.DoesNotExist:
					Grub_Student.objects.create(gm_id=a,user_id=str(request.user),student_id=str(d.bits_id)+"P",meal="Veg",status="Signed Up",room=d.room_no,bhawan=d.bhawan,name=d.name)
				return HttpResponseRedirect("/ssms/student/grub/"+gmid+"/")
			else :
				return HttpResponseRedirect("/ssms/student/grub/"+gmid+"/")
		except Grub.DoesNotExist:
			pass
			return HttpResponseRedirect("/ssms/")
	else :
		return HttpResponseRedirect("/ssms/")
def student_grub_register3(request, gmid):                 #register for non veg
	if request.user.is_authenticated() and not request.user.is_staff:
		try:
			grub = Grub.objects.get(gm_id=gmid,status="Active")
			d=datechecker(gmid)
			if (d==1 or d==2) :
				a = Grub.objects.filter(gm_id=gmid)[0]
				d= Student.objects.get(user_id=str(request.user))
				try :
					b=Grub_Student.objects.get(gm_id=gmid,user_id=str(request.user))
					b.meal="Non Veg"
					b.status="Signed Up"
					b.save()
				except Grub_Student.DoesNotExist:
					Grub_Student.objects.create(gm_id=a,user_id=str(request.user),student_id=str(d.bits_id)+"P",meal="Non Veg",status="Signed Up", room=d.room_no ,bhawan=d.bhawan,name=d.name)
	
				return HttpResponseRedirect("/ssms/student/grub/"+gmid+"/")
			else :
				return HttpResponseRedirect("/ssms/student/grub/"+gmid+"/")
		except Grub.DoesNotExist:
			pass
			return HttpResponseRedirect("/ssms/")
	else :
		return HttpResponseRedirect("/ssms/")



def student_grub_cancel(request, gmid):
	if request.user.is_authenticated() and not request.user.is_staff:
		try:
			grub = Grub.objects.get(gm_id=gmid,status="Active")
			d=datechecker(gmid)
			if d==1 :
				try :
					a=Grub_Student.objects.get(gm_id=gmid,user_id=str(request.user))
					a.status="Opted Out"
					a.save()
				except Grub_Student.DoesNotExist:
					pass
				return HttpResponseRedirect("/ssms/student/grub/"+gmid+"/")
			else :
				return HttpResponseRedirect("/ssms/student/grub/"+gmid+"/")
		except Grub.DoesNotExist:
			pass
			return HttpResponseRedirect("/ssms/")
	else :
		return HttpResponseRedirect("/ssms/")
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/ssms/')	





def import_data(request):
	if request.user.is_superuser:
		done=0
		
		
	    	if request.method == "POST":
			form = UploadFileForm(request.POST,request.FILES)
			if form.is_valid():
				def choice_func(row):
					a=row[0]
					if a[4]=="H" or a[4]=="P":
						b=a[4]+a[0:4]+a[8:]
					else :
						b="f"+a[0:4]+a[8:]
					row.append(b.lower())
					
				    	return row
				request.FILES['file'].save_to_database(
				model=Student,
				initializer=choice_func,
				mapdict=['bits_id','name','bhawan','room_no','user_id',]
			   	)
				done=1
				
		else:
			form = UploadFileForm()
	    	return render(request,'ssms/upload_form.html',{'form': form,'d':done})
	else :
		return HttpResponseRedirect("/ssms/ssms/login/")
		
		
def export(request):
	student = Student.objects.all()
	b=[]
	for i in student:
		b.append(i.name)
	workbook = xlsxwriter.Workbook('media/'+'uploaded_student_list.xlsx')
	worksheet = workbook.add_worksheet()
	worksheet.set_column('A:A', 20)	
	bold = workbook.add_format({'bold': 1})
	worksheet.write('A1', 'User ID', bold)
	row = 1
	col = 0
	for i in b:
		worksheet.write_string  (row, col,i )
		row += 1
	workbook.close()
	return (b)
	return HttpResponseRedirect('media/'+'uploaded_student_list.xlsx')
	
#def invalid(request,inv):
#	return HttpResponse("done")





