from django.urls import path
from .import views

urlpatterns = [
    
    path("",views.home_view, name= 'home'),
    path("about/", views.about, name= 'about'),
    path("doctors/views", views.doctors, name= 'doctors'),
    path("contact/", views.contact, name= 'contact'),

    #departments
    path("department", views.department, name= 'department'),
    path('create/', views.department_create, name='department_create'),
    path('department_list', views.department_list, name='department_list'),
    path('update/<int:pk>/', views.department_update, name='department_update'),
    path('delete/<int:pk>/', views.department_delete, name='department_delete'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('logout/', views.logout_view, name="logout"),
    path('appointments/schedule/', views.schedule_appointment, name='schedule_appointment'),
    path('appointments/reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

    #----------Health resources------------

     path('health-tips/', views.health_tips, name='health_tips'),
    path('educational-materials/', views.educational_materials, name='educational_materials'),
    path('resources/', views.resources, name='resources'),
    
    # HealthTip URLs
    path('health-tips_list/', views.HealthTipListView.as_view(), name='healthtip_list'),
    path('health-tips/create/', views.HealthTipCreateView.as_view(), name='healthtip_create'),
    path('health-tips/<int:pk>/update/', views.HealthTipUpdateView.as_view(), name='healthtip_update'),
    path('health-tips/<int:pk>/delete/', views.HealthTipDeleteView.as_view(), name='healthtip_delete'),

    # EducationalMaterial URLs
    path('educational-materials_list/', views.EducationalMaterialListView.as_view(), name='educationalmaterial_list'),
    path('educational-materials/create/', views.EducationalMaterialCreateView.as_view(), name='educationalmaterial_create'),
    path('educational-materials/<int:pk>/update/', views.EducationalMaterialUpdateView.as_view(), name='educationalmaterial_update'),
    path('educational-materials/<int:pk>/delete/', views.EducationalMaterialDeleteView.as_view(), name='educationalmaterial_delete'),

    # Resource URLs
    path('resources_list/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/create/', views.ResourceCreateView.as_view(), name='resource_create'),
    path('resources/<int:pk>/update/', views.ResourceUpdateView.as_view(), name='resource_update'),
    path('resources/<int:pk>/delete/', views.ResourceDeleteView.as_view(), name='resource_delete'), 

    path('ehrview/',views.ehrView, name="ehrView")
   
]
