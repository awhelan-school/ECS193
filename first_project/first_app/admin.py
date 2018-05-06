from django.contrib import admin
from first_app.models import AccessRecord, Topic, Query, Article, ModelInfo

# Username: admin
# Email: awhelan@ucdavis.edu
# Password: alexseth

admin.site.register(AccessRecord)
admin.site.register(Topic)
admin.site.register(Query)
admin.site.register(Article)
admin.site.register(ModelInfo)


# Register your models here.
