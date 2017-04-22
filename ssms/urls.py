from django.conf.urls import patterns, url
from ssms import views
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^send/$', views.send, name="send"), # Cancellation/Registration mail
	url(r'^send2/$', views.send2, name="send2"),  # Signed up mail 1-2 days before
	url(r'^contact/$', views.contact, name='contact'),#Contact
	url(r'^about/$', views.about, name='about'),#About
	#url(r'^index/$', views.index, name='index'),#Home
	url(r'^ssms/login/$', views.ssms_login, name='ssms_login'), #Ssms Login
	url(r'^ssms/register/$',views.ssms_register,name='register'),
	url(r'^ssms/coord-inactive/(?P<cgid>[-\w]+)/$',views.ssms_coord_inactive,name='coord inactive'), 
	url(r'^ssms/coord-active/(?P<cgid>[-\w]+)/$',views.ssms_coord_active,name='coord active'), #register coords
	url(r'^coord/login/$',views.coord_login,name='coord_login'), #coord login
	url(r'^logout/$', views.user_logout, name='logout'),  #Common logout
	url(r'^coord/register/$', views.coord_grub_register, name='grub_register'),  #coord register grubs
	url(r'^coord/upload/(?P<gmid>[-\w]+)/$', views.coord_upload, name='upload'),#upload list and all list related updates here
	url(r'^coord/view/(?P<gmid>[-\w]+)/$',views.coord_view_grub,name="view registered grub"), 
	url(r'^ssms/grub/(?P<gmid>[-\w]+)/$', views.ssms_grubinfo, name='grubs'),  #ssms view all grubs
	url(r'^ssms/grub/(?P<gmid>[-\w]+)/editdeadline/$', views.ssms_grubeditdeadline, name='grubs edit deadline'),  #ssms edit deadline
	url(r'^ssms/grublist/$', views.ssms_grub_list, name='grub_list'),  #Smms view List and all list related updates here
	url(r'^ssms/grub/(?P<gmid>[-\w]+)/inactive/' , views.ssms_grub_inactive, name="Coord Grub Inactive") ,
	url(r'^ssms/grub/(?P<gmid>[-\w]+)/active/' , views.ssms_grub_active, name="Coord Grub Active") ,
	url(r'^ssms/grub/(?P<gmid>[-\w]+)/batchallocation/$', views.ssms_grub_batchallocation, name='grubs batch'), 
	
	#url(r'^student/login$', views.student_login, name='student_login'),  #student login
	url(r'^student/upcoming_grubs/$', views.student_upcoming_grubs, name='student_upcoming_grubs'),  #view upcoming grubs
	url(r'^student/grub/(?P<gmid>[-\w]+)/$', views.student_grub_register, name='student grub register'),
	url(r'^student/grub/(?P<gmid>[-\w]+)/cancel/$', views.student_grub_cancel, name='student grub cancel'),
	url(r'^student/grub/(?P<gmid>[-\w]+)/register/veg/$', views.student_grub_register2, name='student grub register2'),
	url(r'^student/grub/(?P<gmid>[-\w]+)/register/non_veg/$', views.student_grub_register3, name='student grub register2'),  
	url(r'^student/grub/(?P<gmid>[-\w]+)/feedback/$', views.student_grub_feedback, name='student grub feedback'),  
 #Cancel and register for grubs here
	url(r'^coord/register-students/(?P<gmid>[-\w]+)/$',views.coord_student_register,name='coord student register'),
	#url(r'^grub_info/(?P<gmid>\w+)/$', views.grub_info, name='grub_info'),
	#adddddddddddddddd
	url(r'^export/(?P<gmid>[-\w]+)/$', views.export_data, name="export"),
	url(r'^stats/(?P<gmid>[-\w]+)/$', views.ssms_student_table, name="stats"),
	url(r'^import/', views.import_data, name="import"),
	url(r'^coord/edit/(?P<gmid>[-\w]+)/$', views.coord_grub_edit, name='grub_edit'), 
	url(r'^export2/',views.export,name="export2"),
	url('^ssms/grub/(?P<gmid>[-\w]+)/sendmail/' , views.ssms_grub_sendmail, name="Grub send mail1") ,
	url('^ajax/ssms/grub/(?P<gmid>[-\w]+)/sendmail1/' , views.ssms_grub_sendmail1, name="Grub send mail1") ,
	url('^ajax/ssms/grub/(?P<gmid>[-\w]+)/sendmail2/' , views.ssms_grub_sendmail2, name="Grub send mail1") ,
	#url(r'^(?P<inv>\w+)/$',views.invalid,name="invalid"),
	#url(r'^coord/upload-spot-signing/(?P<gmid>[-\w]+)/$', views.coord_upload_spot, name='upload spot signing'),
	]

