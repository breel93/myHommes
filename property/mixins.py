from django.http import Http404

from real.mixins import LoginRequiredMixin
from realtor.mixins import RealtorAccountMixin

class PropertyManagerMixin(RealtorAccountMixin, object):
	def get_object(self, *args, **kwargs):
		realtor = self.get_account()
		obj = super(PropertyManagerMixin, self).get_object(*args, **kwargs)
		try:
			obj.realtor  == realtor
		except:
			raise Http404

		# try:
		# 	user in obj.managers.all()
		# except:
		# 	raise Http404

		if obj.realtor == realtor:
			return obj
		else:
			raise Http404