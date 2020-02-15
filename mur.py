#!/usr/bin/env python3
# Sorrow446

import os
import re
import sys
import json
import shutil
import zipfile
import argparse
import platform

import api
import img2pdf
from tqdm import tqdm
from requests.exceptions import HTTPError
from api.exceptions import IneligibleError

client = api.Client()

def print_title():
	print("""
 _____ _____ _____ 
|     |  |  | __  |
| | | |  |  |    -|
|_|_|_|_____|__|__|
   """)

def get_os():
	if platform.system() == 'Windows':
		return True
	return False
   
def set_con_title():
	if get_os():
		os.system('title MUR R1 (by Sorrow446)')
	else:
		sys.stdout.write('\x1b]2;MUR R1 (by Sorrow446)\x07')

def sanitize(fn):
	if get_os():
		return re.sub(r'[\/:*?"><|]', '_', fn)
	else:
		return re.sub('/', '_', fn)
		
def parse_args():
	parser = argparse.ArgumentParser(
		description='Sorrow446.'
	)	
	parser.add_argument(
		'-u', '--url',
		help="URL - marvel.com/comics/issue/ or read.marvel.com/#/book/.",
		nargs='*',
		required=True
	)
	parser.add_argument(
		'-f', '--format',
		help="Export format.",
		choices=['cbz', 'pdf'],
		required=True
	)
	parser.add_argument(
		'-m', '--meta',
		help="Write comic's metadata to JSON file.",
		action='store_true'
	)
	return parser.parse_args()

def parse_cookies(cd, out_cookies={}):
	with open(os.path.join(cd, 'cookies.txt')) as f:
		for line in f.readlines():
			if not line.startswith('#'):
				field = line.strip().split('\t')
				out_cookies[field[5]] = field[6]
	client.set_cookies(out_cookies)
	
def exist_check(f):
	if os.path.isfile(f): 
		return True
	return False

def dir_setup(tmp_dir, dl_dir):
	if os.path.isdir(tmp_dir): 
		shutil.rmtree(tmp_dir)
	if not os.path.isdir(dl_dir): 
		os.makedirs(dl_dir)
	os.makedirs(tmp_dir)
	
def check_url(url):
	regexes=[
		r'http[s]://(read).marvel.com/#/book/([0-9]{5}$)',
		r'http[s]://(www).marvel.com/comics/issue/([0-9]+)/.+'
	]
	for regex in regexes:
		match = re.match(regex, url)
		if match:
			return match.group(1), match.group(2)

def download(urls, tmp_dir, cur=0):
	total = len(urls)
	for url in urls:
		cur += 1
		print('Downloading image {} of {}...'.format(cur, total))
		r = client.session.get(url, stream=True)
		r.raise_for_status()
		size = int(r.headers.get('content-length', 0))
		abs = os.path.join(tmp_dir, str(cur) + '.jpg')
		with open(abs, 'wb') as f:
			with tqdm(total=size, unit='B',
				unit_scale=True, unit_divisor=1024,
				initial=0, miniters=1) as bar:		
					for chunk in r.iter_content(32*1024):
						if chunk:
							f.write(chunk)
							bar.update(len(chunk))

def make_pdf(abs, images, title):
	with open(abs, 'wb') as f:
		f.write(img2pdf.convert(images, title=title))

def make_cbz(abs, images):
	with zipfile.ZipFile(abs, 'w', zipfile.ZIP_STORED) as f:
		for i in images:
			f.write(i)
	
def write_meta(meta_abs, meta):
	with open(meta_abs, 'w') as f: 
		json.dump(meta, f, indent=4)

def err(e, cur, tot):
	print(e)
	if cur == tot:
		sys.exit(1)
		
def main():		
	if hasattr(sys, 'frozen'):
		cd = os.path.dirname(sys.executable)
	else:
		cd = os.path.dirname(__file__)
	tmp_dir = os.path.join(cd, 'mur_tmp')
	dl_dir = os.path.join(cd, 'MUR downloads')
	dir_setup(tmp_dir, dl_dir)
	parse_cookies(cd)
	args = parse_args()
	tot = len(args.url)
	cur = 0
	for url in args.url:
		cur += 1	
		try:
			print("Comic {} of {}:".format(cur, tot))
			try:
				type, id = check_url(url)
			except TypeError:
				err('Invalid URL: '+str(url), cur, tot)
				continue
			if type == "www":
				id = client.get_id(url)
			fmt = args.format
			meta = client.get_comic_meta(id)
			title = meta['title']
			title_s = sanitize(title)
			print(str(title) + "\n")
			abs = os.path.join(dl_dir, '{}.{}'.format(title_s, fmt))
			if exist_check(abs):
				err('Comic already exists locally.', cur, tot)
				continue
			try:
				download(client.get_comic(id), tmp_dir)
			except IneligibleError as e:
				print(e)
				sys.exit(1)
			images = [os.path.join(tmp_dir, i) for i in os.listdir(tmp_dir)]
			print('Converting to {}...'.format(fmt.upper()))
			if fmt == 'pdf':
				make_pdf(abs, images, title)
			else:
				make_cbz(abs, images)
			if args.meta:
				print("Writing metadata to JSON file...")
				meta_abs = os.path.join(dl_dir, '{}_meta.json'.format(title_s))
				write_meta(meta_abs, meta)
			for i in images:
				os.remove(i)
		except HTTPError as e:
			err(e, cur, tot)
		except Exception as e:
			err(e, cur, tot)

if __name__ == '__main__':
	print_title()
	set_con_title()
	main()
