from dssetup.models import Authority 
 

a1 = Authority(authName="add_user",authDes="The authority to add new user")

a2 = Authority(authName="delete_user",authDes="The authority to delete a user")

a3 = Authority(authName="modify_user",authDes="The authority to modify a user")

a4 = Authority(authName="auth_user",authDes="The authority to control users")

a1.save()

a2.save()

a3.save()

a4.save()

a1.auth_parent = a4

a2.auth_parent = a4

a3.auth_parent = a4 

a1.save()
a2.save()
a3.save()

a5 = Authority(authName="add_group",authDes="The authority to add new group")

a6 = Authority(authName="delete_group",authDes="The authority to delete a group")

a7 = Authority(authName="modify_group",authDes="The authority to modify a group")

a8 = Authority(authName="auth_group",authDes="The authority to control group")

a5.save()

a6.save()

a7.save()

a8.save()

a5.auth_parent = a8

a6.auth_parent = a8

a7.auth_parent = a8 

a5.save()
a6.save()
a7.save()



a7 = Authority(authName="add_authority",authDes="The authority to add new authority")

a8 = Authority(authName="delete_authority",authDes="The authority to delete a authority")

a9 = Authority(authName="modify_authority",authDes="The authority to modify a authority")

a10 = Authority(authName="auth_authority",authDes="The authority to control authority")

a7.save()

a8.save()

a9.save()

a10.save()

a8.auth_parent = a10

a9.auth_parent = a10

a10.auth_parent = a10 

a8.save()
a9.save()
a10.save()

a14 = Authority(authName="verify_form",authDes="The authority to verify a form after application")
a15 = Authority(authName="imple_form",authDes="The authority to operate the requirement of the applicant")
a16 = Authority(authName="check_form",authDes="The authority to check whether it is satisfied")
a17 = Authority(authName="apply_form",authDes="The authority to confirm that the form has been implemented")
a18 = Authority(authName="auth_form",authDes="The authority to control a form")

 
a14.save()
a15.save()
a16.save()
a17.save()
a18.save()

 

a14.auth_parent=a18

a15.auth_parent=a18

a16.auth_parent=a18

a17.auth_parent=a18

 
 

 