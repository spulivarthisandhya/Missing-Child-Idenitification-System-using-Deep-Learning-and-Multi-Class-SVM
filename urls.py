from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('Login.html', views.Login, name="Login"), 
	       path('Upload.html', views.Upload, name="Upload"),
	       path('OfficialLogin', views.OfficialLogin, name="OfficialLogin"),
	       path('UploadAction', views.UploadAction, name="UploadAction"),
	       path('ViewUpload', views.ViewUpload, name="ViewUpload"),
	       path('ParentRegister.html', views.ParentRegister, name="ParentRegister"), 
	       path('ParentRegisterAction', views.ParentRegisterAction, name="ParentRegisterAction"), 
	       path('ParentLogin.html', views.ParentLogin, name="ParentLogin"), 
	       path('ParentLoginAction', views.ParentLoginAction, name="ParentLoginAction"), 
	       path('ChildDetails.html', views.ChildDetails, name="ChildDetails"), 
	       path('ChildDetailsAction', views.ChildDetailsAction, name="ChildDetailsAction"), 
	       path('AdoptAction', views.AdoptAction, name="AdoptAction"),
	       path('WelfareLogin.html', views.WelfareLogin, name="WelfareLogin"), 
	       path('WelfareLoginAction', views.WelfareLoginAction, name="WelfareLoginAction"),
	       path('ViewAdoption', views.ViewAdoption, name="ViewAdoption"),
	       path('AdoptionRules.html', views.AdoptionRules, name="AdoptionRules"), 
]