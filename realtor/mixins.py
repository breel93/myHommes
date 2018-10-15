import datetime

from django.db.models import Count, Min, Sum, Avg, Max

from real.mixins import LoginRequiredMixin
from property.models import Property

from .models import Realtor



class RealtorAccountMixin(LoginRequiredMixin, object):
	account = None
	property = []
	

	def get_account(self):
		user = self.request.user
		accounts = Realtor.objects.filter(user=user)
		if accounts.exists() and accounts.count() == 1:
			self.account = accounts.first()
			return accounts.first()
		return None

	def get_property(self):
		account = self.get_account()
		property = Property.objects.filter(realtor=account)
		self.property = property
		return property
