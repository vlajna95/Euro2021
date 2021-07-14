from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

admin.site.site_header = "Euro 20/21"
admin.site.site_title = "Euro 20/21 admin"
admin.site.site_url = "http://danijela.tk"
admin.site.index_title = "Euro 20/21 administracija"
admin.empty_value_display = "** Nema unosa **"

urlpatterns = [
	path("admin/", admin.site.urls, name="admin"),
	path("", include("matches.urls"), name="matches"),
	path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
