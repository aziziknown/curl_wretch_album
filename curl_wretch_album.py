#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import os
import urllib2
from lxml import etree
import glob
import os
import sqlite3
import codecs

def get_album_list(url,outfile,htmldir):
	if not os.path.exists(htmldir):
		os.mkdir(htmldir)
	if not os.path.exists(htmldir+'/images'):
		os.mkdir(htmldir+'/images')
	fout = codecs.open(outfile,"w",encoding="utf-8")
	parser = etree.HTMLParser()
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	stream = urllib2.urlopen(req)
	tree = etree.parse(stream,parser)
	links = tree.xpath("//td/b/font[@class='small-c']/a")
	i=1
	for ll in links:
		fout.write("%02d,%s,%s\n"%(i,ll.get('href').replace('./','http://www.wretch.cc/album/'),ll.text))
		ll.set('href','album%02d/index.htm'%i)
		i=i+1
	links = tree.xpath("//td[@class='side']/a")
	i=1
	for ll in links:
		ll.set('href','album%02d/index.htm'%i)
		img=ll.getchildren()
		img=img[0]
		url=img.get('src')
		os.system("wget -O %s/images/thumb%02d.jpg %s"%(htmldir,i,url))
		img.set('src','images/thumb%02d.jpg'%i)
		i=i+1

	styles = tree.xpath("//link[@rel='stylesheet']")
	for st in styles:
		url=st.get('href')
		fn = url.split('/')[-1].split('?')[0]
		if not os.path.exists(htmldir+'/css/'+fn):
			if not os.path.exists(htmldir+'/css'):
				os.mkdir(htmldir+'/css')
			os.system("wget -O %s/css/%s %s"%(htmldir,fn,url))
		st.set('href','css/%s'%fn)

	scripts= tree.xpath("//script[@src]")
	for sc in scripts:
		url=sc.get('src')
		fn = url.split('/')[-1].split('?')[0]
		if not os.path.exists(htmldir+'/js/'+fn):
			if not os.path.exists(htmldir+'/js'):
				os.mkdir(htmldir+'/js')
			os.system("wget -O %s/js/%s %s"%(htmldir,fn,url))
		sc.set('src','js/%s'%fn)
		
	tree.write(htmldir+'/index.htm')

	

def album_list2page_list(infile,outdir):
#read infiles of urls
# output full list with pages in category
	if not os.path.exists(outdir):
		os.mkdir(outdir)
	fin = codecs.open(infile,encoding="utf-8")
	parser = etree.HTMLParser()
	for line in fin:
		line = line.strip()
		if len(line)>0: 
			#print line
			tok=line.split(',')
			print tok[1]
			fout = codecs.open("%s/%s.txt"%(outdir,tok[0].strip()),'w',encoding="utf-8")
			fout.write("%s\n"%tok[1])
			req = urllib2.Request(tok[1], headers={'User-Agent' : "Magic Browser"})
			stream = urllib2.urlopen(req)
			tree = etree.parse(stream,parser)
			links = tree.xpath("//td/center/font[@class='small-c']/a")
			l = len(links)/2-1
			for i in range(l):
				url=links[i].get("href")
				fout.write("%s\n"%url.replace('./','http://www.wretch.cc/album/'))	
		fout.close()
	fin.close()

def page_list2photo_list(infile,outfile,htmldir):
	if not os.path.exists(htmldir):
		os.mkdir(htmldir)
	if not os.path.exists(htmldir+'/images'):
		os.mkdir(htmldir+'/images')
	fin = open(infile)
	fout = codecs.open(outfile,'w',encoding='utf-8')
	parser = etree.HTMLParser()
	page=1
	for line in fin:
		line = line.strip()
		if len(line)>0:
			print line
			req = urllib2.Request(line, headers={'User-Agent' : "Magic Browser"})
			stream = urllib2.urlopen(req)
			tree = etree.parse(stream,parser)
			links = tree.xpath("//td/b/font[@class='small-e']/a")
			for ll in links:
				url = ll.get("href")
				fout.write("%s,%s\n"%(url.replace('./','http://www.wretch.cc/album/'),ll.text))
				photoNo=url.split('&')[2].split('=')[1]
				ll.set('href','photo%s.htm'%photoNo)
			links = tree.xpath("//td/center/font[@class='small-c']/a")
			for ll in links:
				url = ll.get("href")
				ll.set('href','page'+url.split('=')[-1]+'.htm')

			links = tree.xpath("//td[@class='side']/a")
			for ll in links:
				url=ll.get("href")
				photoNo=url.split('&')[2].split('=')[1]
				ll.set('href','photo%s.htm'%photoNo)
				img=ll.getchildren()
				img=img[0]
				url=img.get('src')
				os.system("wget -O %s/images/thumb%s.jpg %s"%(htmldir,photoNo,url))
				img.set('src','images/thumb%s.jpg'%photoNo)

			styles = tree.xpath("//link[@rel='stylesheet']")
			for st in styles:
				url=st.get('href')
				fn = url.split('/')[-1].split('?')[0]
				if not os.path.exists(htmldir+'/../css/'+fn):
					if not os.path.exists(htmldir+'/../css'):
						os.mkdir(htmldir+'/../css')
					os.system("wget -O %s/../css/%s %s"%(htmldir,fn,url))
				st.set('href','../css/%s'%fn)

			scripts= tree.xpath("//script[@src]")
			for sc in scripts:
				url=sc.get('src')
				fn = url.split('/')[-1].split('?')[0]
				if not os.path.exists(htmldir+'/../js/'+fn):
					if not os.path.exists(htmldir+'/../js'):
						os.mkdir(htmldir+'/../js')
					os.system("wget -O %s/../js/%s %s"%(htmldir,fn,url))
				sc.set('src','../js/%s'%fn)

			tree.write(htmldir+'/page%d.htm'%page)
			if page==1:
				tree.write(htmldir+'/index.htm')
			page=page+1
	fin.close()
	fout.close()

def curl_photo(url,htmldir):
	parser = etree.HTMLParser()
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	stream = urllib2.urlopen(req)
	tree = etree.parse(stream,parser)

	out = dict()
	
	tmp=tree.xpath("//span[@id='DisplayTitle']")
	out['photo_title']=tmp[0].text.strip()
	tmp=tree.xpath("//span[@id='DisplayDesc']")
	out['photo_desc']=tmp[0].text.strip()
	photoNo=url.split('&')[2].split('=')[1]
	out['photo_id']=photoNo

	img=tree.xpath("//img[@id='DisplayImage']")
	if len(img)>0:
		img=img[0]
		out['photo_url']=img.get('src')
		url=out['photo_url']
		#photoNo=url.split('/')[5].split('.')[0]
		os.system("wget -O %s/images/photo%s.jpg %s"%(htmldir,photoNo,url))
		img.set('src','images/photo%s.jpg'%photoNo)
	else:
		out['photo_url']='none'

	links=tree.xpath("//a[@id='DisplayLink']")
	if len(links)>0:
		links=links[0]
		pn=links.get('href').split('&')[-2].split('=')[1]
		links.set('href','photo%s.htm'%pn)

	links=tree.xpath("//font[@class='small-e']/a")
	for ll in links:
		url=ll.get('href')
		pn=url.split('&')[-2].split('=')[1]
		ll.set('href','photo%s.htm'%pn)

	links=tree.xpath("//td[@class='side']/a")
	for ll in links:
		url=ll.get('href')
		pn=url.split('&')[-2].split('=')[1]
		ll.set('href','photo%s.htm'%pn)
		img=ll.getchildren()[0]	
		img.set('src','images/thumb%s.jpg'%pn)

	styles = tree.xpath("//link[@rel='stylesheet']")
	for st in styles:
		url=st.get('href')
		fn = url.split('/')[-1].split('?')[0]
		if not os.path.exists(htmldir+'/../css/'+fn):
			if not os.path.exists(htmldir+'/../css'):
				os.mkdir(htmldir+'/../css')
			os.system("wget -O %s/../css/%s %s"%(htmldir,fn,url))
		st.set('href','../css/%s'%fn)

	scripts= tree.xpath("//script[@src]")
	for sc in scripts:
		url=sc.get('src')
		fn = url.split('/')[-1].split('?')[0]
		if not os.path.exists(htmldir+'/../js/'+fn):
			if not os.path.exists(htmldir+'/../js'):
				os.mkdir(htmldir+'/../js')
			os.system("wget -O %s/../js/%s %s"%(htmldir,fn,url))
		sc.set('src','../js/%s'%fn)

	tree.write('%s/photo%s.htm'%(htmldir,photoNo))
	return out

if __name__ == '__main__':
	
	if len(sys.argv)<2:
		print 'usage: python curl_wretch_album.py your_wretch_id [path_to_put_your_backup]'
	elif len(sys.argv)<3:
		htmlroot = 'wretch'
	else:
		wretch_url = 'http://www.wretch.cc/album/'+sys.argv[1].strip()
		htmlroot=sys.argv[2]

	get_album_list(wretch_url,'wretch_album_list.txt',htmlroot)
	album_list2page_list('wretch_album_list.txt','wretch_page_list')
	
	if not os.path.exists('wretch_photo_list'):
		os.mkdir('wretch_photo_list')
	if not os.path.exists('wretch_photo_data'):
		os.mkdir('wretch_photo_data')
	
	files = glob.glob('wretch_page_list/*.txt')	
	ii=0
	for fn in files:
		albumNo=fn.split('/')[1].split('.')[0]
		photo_list="wretch_photo_list/%s"%fn.split('/')[1]
		page_list2photo_list(fn,photo_list,'%s/album%s'%(htmlroot,albumNo))
		fout = codecs.open("wretch_photo_data/%s"%fn.split('/')[1],'w',encoding="utf-8")
		for line in open(photo_list):
			line = line.strip()
			if len(line)>0:
				print line
				out=curl_photo(line.split(',')[0],'%s/album%s'%(htmlroot,albumNo))
				fout.write("%s,%s,%s,%s\n"%(out['photo_id'],out['photo_url'],out['photo_title'],out['photo_desc']))
				time.sleep(1)
		fout.close()

