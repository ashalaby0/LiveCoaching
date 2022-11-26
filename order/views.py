import hashlib
import hmac

from django.shortcuts import HttpResponse, HttpResponseRedirect, render

from . import models
