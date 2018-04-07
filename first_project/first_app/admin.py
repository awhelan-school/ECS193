from django.contrib import admin
from first_app.models import AccessRecord, Topic, Query

# Username: admin
# Email: awhelan@ucdavis.edu
# Password: alexseth

admin.site.register(AccessRecord)
admin.site.register(Topic)
admin.site.register(Query)


# Register your models here.
