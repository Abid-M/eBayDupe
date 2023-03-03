from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Item, Bid, Question, Answer
# from .forms import  CustomUserChangeForm


class CustomUserAdmin(UserAdmin):

    model = Account
    list_display = ('email', 'profileImage', 'username', 'first_name', 'last_name', 'dOB',
                    'phoneNumber', 'addressLine1', 'addressLine2', 'city', 'postcode', 'country')
    fieldsets = (
        ('Personal Information', {
         'fields': ('profileImage', 'first_name', 'last_name', 'dOB')}),
        ('Contact Information', {
         'fields': ('email', 'phoneNumber', 'username')}),
        ('Location Information', {
         'fields': ('city', 'postcode', 'country', 'addressLine1', 'addressLine2')}),

    )


# Register your models here.
admin.site.register(Account, CustomUserAdmin)
# admin.site.register(Userr)
admin.site.register(Item)
admin.site.register(Question)
admin.site.register(Bid)
admin.site.register(Answer)
