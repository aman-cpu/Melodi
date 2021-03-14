"""musicvideo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from musicvideo.category import ActionDisplayJSON
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .import category, subcategory, song, Admin, User
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categoryinterface/', category.Actioncategoryinterface),
    path('categorysubmit', category.Actioncategorysubmit),
    path('categorydisplayall/', category.ActioncategoryDisplayAll),
    path('categorydisplaybyid/', category.ActioncategoryDisplaybyid),
    path('categoryeditdeletesubmit', category.ActionCategoryEditDeleteSubmit),
    path('editcategorypicture', category.ActionEditCategoryPicture),

    path('subcategoryinterface/', subcategory.Actionsubcategoryinterface),
    path('subcategorysubmit', subcategory.Actionsubcategorysubmit),
    path('subcategorydisplayall/', subcategory.ActionsubcategoryDisplayAll),
    path('subcategorydisplaybyid/', subcategory.ActionsubcategoryDisplaybyid),
    path('subcategoryeditdeletesubmit',subcategory.ActionsubCategoryEditDeleteSubmit),
    path('editsubcategorypicture', subcategory.ActionEditsubCategoryPicture),

    path('songinterface/', song.Actionsonginterface),
    path('songsubmit', song.Actionsongsubmit),
    path('songdisplayall/', song.ActionsongDisplayAll),
    path('songdisplaybyid/', song.ActionsongDisplaybyid),
    path('songeditdeletesubmit', song.ActionSongEditDeleteSubmit),
    path('editsongpicture', song.ActionEditSongPicture),

    path('adminlogin/', Admin.ActionAdminLogin),
    path('checkadminlogin', Admin.ActionCheckLogin),
    path('logout/', Admin.ActionLogout),

    path('categorydisplayalljson/', category.ActionDisplayJSON),
    path('displaysubcategoryjson/', song.ActionDisplaySubCategoryJSON),


    path('', User.ActionMainPage),
    path('categorypage/', User.ActionCategoryPage),
    path('subcategorypage/', User.ActionSubcategoryPage),
    path('artistpage/', User.ActionArtistPage),
    path('playlistpage/', User.ActionPlayListPage),
    path('searchsong/', User.ActionSearchSongPage),
    path('searchsongjson/', User.ActionSearchSongJson),
    path('playsong/', User.ActionPlaySong),

    url(r'^media/(?P<path>.*)$', serve,{'document_root':  settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
urlpatterns += staticfiles_urlpatterns()
