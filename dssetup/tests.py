from django.test import TestCase
from dssetup.models import Account,Authority,Group
import hashlib
from django.http import  HttpResponseRedirect
from dssetup.decorator import login_required

