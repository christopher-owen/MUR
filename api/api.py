# Sorrow446

import os
import re
from random import randint

import requests
from api.exceptions import IneligibleError

class Client:

	def __init__(self, **kwargs):
		self.session = requests.Session()
		self.session.headers.update({
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
		})
		self.base = 'https://read-api.marvel.com/'

	def set_cookies(self, cookies):
		self.session.cookies.update(cookies)
	
	def get_id(self, url):
		r = self.session.get(url)
		regex = r'digital_comic_id :  "(([0-9]{5}))"'
		return re.search(regex, r.text).group(1)
	
	def make_call(self, epoint, json=None, params=None):
		r = self.session.get(self.base+epoint, json=json, params=params)
		r.raise_for_status()
		return r

	def get_comic_meta(self, id):	
		self.session.headers.update({'Referer': 'https://read.marvel.com/'})
		r = self.make_call('issue/v1/digitalcomics/'+id+'?')
		return r.json()['data']['results'][0]['issue_meta']

	def get_comic(self, id):
		params={'rand': randint(10000, 99999)}
		r = self.make_call('asset/v1/digitalcomics/'+id+'?', params=params)
		j = r.json()['data']['results'][0]
		if not j['auth_state']['subscriber']:
			raise IneligibleError('Marvel Unlimited subscription required.')
		urls = [url['assets']['source'] for url in j['pages']]
		return urls
