from django.contrib import admin
from ssms.models import Grub,Grub_Coord,Grub_Student,Veg,NonVeg,Both,Student,DateMailStatus,Batch,Feedback, Meal, Items
admin.site.register(Veg)
admin.site.register(NonVeg)
admin.site.register(Both)
admin.site.register(DateMailStatus)
class GrubStudentAdmin(admin.ModelAdmin):
    search_fields = ('student_id',)
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
admin.site.register(Meal)
admin.site.register(Items)
