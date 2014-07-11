from dssetup.models import Group,Authority

g1 = Group(groupName="administrator",groupDes="It has all authorities to control the backend")
g1.save()
g1.authority.add(Authority.objects.get(authName="auth_user"))
g1.authority.add(Authority.objects.get(authName="auth_group"))
g1.authority.add(Authority.objects.get(authName="auth_authority"))
 
g1.authority.add(Authority.objects.get(authName="apply_form"))
g1.save()

g2 = Group(groupName="applicant",groupDes="It can apply the form")
g2.save()
g2.authority.add(Authority.objects.get(authName="apply_form"))
g2.save()

g3 = Group(groupName="verifier",groupDes="It can verify the form")
g3.save()
g3.authority.add(Authority.objects.get(authName="apply_form"))

g3.authority.add(Authority.objects.get(authName="verify_form"))
g3.save()


g4 = Group(groupName="impler",groupDes="It can implement the form")
g4.save()
g4.authority.add(Authority.objects.get(authName="apply_form"))

g4.authority.add(Authority.objects.get(authName="imple_form"))
g4.save()


g5 = Group(groupName="checker",groupDes="It can check the form")
g5.save()
g5.authority.add(Authority.objects.get(authName="apply_form"))

g5.authority.add(Authority.objects.get(authName="check_form"))
g5.save()