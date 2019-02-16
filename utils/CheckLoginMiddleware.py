from django.http import HttpResponse,HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

class CheckMiddleware(MiddlewareMixin):
	def process_request(self, request):
		if request.path == '/login/' or request.path == '/logout/':
			return
		if not request.session.get('status', 0):
			return HttpResponseRedirect('/login/')
		else:
			return
