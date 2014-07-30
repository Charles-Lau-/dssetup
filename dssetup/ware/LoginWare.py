from django.http import HttpResponseRedirect

class LoginWare():
    def process_request(self,request):
        if(not request.path.startswith("/login") and not request.path == "/"):
            if(not request.session.get("user")):
                return HttpResponseRedirect("/login")