from django.contrib import admin
from user_onboarding.models import User,Roles
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class UsermodelAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("id","email", "f_name","username", "is_admin",'user_type')
    list_filter = ("is_admin",'f_name','username')
    fieldsets = (
        ('User Credential', {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("f_name",'l_name',"username",'profile_photo','user_type')}),
        ("Permissions", {"fields": ("is_admin",'is_active')}),
        ('others',{'fields':('last_login',)})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                
                "classes": ("wide",),
                "fields": ("email", 'f_name', 'username','l_name',"password1", "password2", 'user_type'),
            },
        ),
    ]
    search_fields = ("email",'f_name')
    ordering = ("email",'id')
    filter_horizontal = ()
    def has_permission(self, request):
        if request.user.is_superuser:
            return True
        return False



# Now register the new UserAdmin...
admin.site.register(User, UsermodelAdmin)
admin.site.register(Roles)