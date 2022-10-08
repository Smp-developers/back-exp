from django.urls import path
from . import views
from . import courseView
urlpatterns = [

    path('login/', views.logined),
    path('signup/', views.signup),
    path('getting_all_students', views.getting_all_students),
    path('delete_all_students', views.delete_all_students),
    path('getting_single_students/<int:id>', views.getting_single_students),
    path('get_all_batch1/', views.get_all_batch1),
    path('get_all_batch2/', views.get_all_batch2),
    path('get_none_batches/', views.get_none_batches),

    path('switch_batches/', views.switch_batches),
    path('update_single_total/<int:id>', views.update_single_total),
    path('update_single_referals/<int:id>', views.update_single_referals),

    path('update_single_payment/<int:id>', views.update_single_payment),
    path('update_single_payment/<int:id>', views.update_single_payment),
    path('update_student_batch/<int:id>', views.update_student_batch),


    path('delete_single_student/<int:id>', views.delete_single_student),

    path('logout/', views.logouted),


    path('course_upload/', courseView.course_upload),
    # get_all_courses
    path('get_all_courses/', courseView.get_all_courses),
    path('edit_single_course/<int:id>', courseView.edit_single_course),
    path('get_single_course/<int:id>', courseView.get_single_course),

    path('delete_all_courses/', courseView.delete_all_courses),

    path('delete_single_course/<int:id>', courseView.delete_single_course),
    path('edit_student_profile/<str:email>', views.edit_student_profile),




    path('sending_individual_mail', views.individual_mail),
    path('group_batch2_mail', views.group_batch2_mail),
    path('group_batch1_mail', views.group_batch1_mail),


    path('delete_admin_mail/<str:email>', views.delete_admin_mail),
    path('check_original_password', views.check_original_password),



    path('upload_trainee', courseView.upload_trainee),
    path('edit_single_trainee/<int:id>', courseView.edit_single_trainee),
    path('get_all_trainees', courseView.get_all_trainees),
    path('get_single_trainee/<int:id>', courseView.get_single_trainee),

    path('delete_single_trainee/<int:id>', courseView.delete_single_trainee),
    path('changePassword/<str:email>', courseView.changePassword),
    
    path('get_batch_trainer', views.get_batch_trainer),
    path('batch_request_update/<int:id>', views.batch_request_update),
    
    
path('sending_newStudents_mail', views.sending_newStudents_mail)
]
