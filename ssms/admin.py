from django.contrib import admin
from ssms.models import Grub,Grub_Coord,Grub_Student,Veg,NonVeg,Both,Student,DateMailStatus,FB
admin.site.register(Grub)
admin.site.register(Grub_Coord)

admin.site.register(Veg)
admin.site.register(NonVeg)
admin.site.register(Both)
admin.site.register(Student)
admin.site.register(DateMailStatus)
class GrubStudentAdmin(admin.ModelAdmin):
    search_fields = ('student_id',)
admin.site.register(Grub_Student,GrubStudentAdmin)
admin.site.register(FB)
