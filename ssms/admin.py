from django.contrib import admin
from ssms.models import Grub,Grub_Coord,Grub_Student,Grub_Member,Veg,NonVeg,Both,Student,DateMailStatus,Batch,Feedback, Meal,Grub_Invalid_Students
admin.site.register(Veg)
admin.site.register(NonVeg)
admin.site.register(Both)
admin.site.register(DateMailStatus)
class GrubStudentAdmin(admin.ModelAdmin):
    search_fields = ('student_id','name','user_id')
admin.site.register(Grub_Student,GrubStudentAdmin)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ('bits_id','name','user_id')
admin.site.register(Student,StudentAdmin)
class Grub_CoordAdmin(admin.ModelAdmin):
    search_fields = ('assoc_name','cg_bitsid','cg_name')
admin.site.register(Grub_Coord,Grub_CoordAdmin)
class GrubAdmin(admin.ModelAdmin):
    search_fields = ('name','date')
admin.site.register(Grub,GrubAdmin)
admin.site.register(Batch)
admin.site.register(Feedback)
class MealAdmin(admin.ModelAdmin):
    search_fields = ('meal_type','date','day')
admin.site.register(Meal,MealAdmin)
class Grub_Invalid_StudentsAdmin(admin.ModelAdmin):
    search_fields = ('student_id',)
admin.site.register(Grub_Invalid_Students,Grub_Invalid_StudentsAdmin)
admin.site.register(Grub_Member)

