from django.contrib import admin
from .models import user, fcm_token, address

# Register your models here.
admin.site.register(user.User)
admin.site.register(user.StandardUser)
admin.site.register(user.MerchantAdministrator)
admin.site.register(user.LogisticsAdministrator)
admin.site.register(user.Driver)
admin.site.register(fcm_token.FCMToken)
admin.site.register(address.Address)
