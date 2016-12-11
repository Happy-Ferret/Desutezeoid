#!/usr/bin/env python
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
import pygame
import time
import os
from pygame.locals import *
import xml.etree.ElementTree as ET
pygame.display.init()
pygame.font.init()
print "Desutezeoid arbitrary point and click engine v1.0"

conftree = ET.parse("ENGSYSTEM.xml")
confroot = conftree.getroot()
screentag=confroot.find("screen")
scrnx=int(screentag.attrib.get("x", "800"))
scrny=int(screentag.attrib.get("y", "600"))
titletag=confroot.find("title")
titlebase=titletag.attrib.get("base", "Desutezeoid: ")
class clicktab:
	def __init__(self, box, reftype, ref, keyid, takekey):
		self.box=box
		self.ref=ref
		self.keyid=keyid
		self.takekey=takekey
		self.reftype=reftype
DEBUG=1

def debugmsg(msg, printplaypos=0):
	if DEBUG==1:
		
		if printplaypos==1:
			print (msg + " x(" + str(playx) + "),y(" + str(playy) + ")")
		else:
			print msg
prevpage="NULL"
#point this to your first screen c: no menu program really needed :o
curpage="test0.xml"

screensurf=pygame.display.set_mode((scrnx, scrny))
quitflag=0
clicklist=list()
keylist=list(["0"])
keybak=list(keylist)
forksanitycheck=0
forksanity=0
while quitflag==0:
	huris=0
	clicklist=list()
	time.sleep(0.1)
	pos = pygame.mouse.get_pos()
	#print "tic"
	if curpage!=prevpage:
		print "preparsing page"
		tree = ET.parse(curpage)
		root = tree.getroot()
		prevpage=curpage
		coretag=root.find('core')
		forktag=root.find('forks')
		pageconf=root.find('pageconf')
		pagetitle=(pageconf.find('title')).text
		BGon=int(pageconf.attrib.get("BGimg", "0"))
		pygame.display.set_caption((titlebase + pagetitle), (titlebase + pagetitle))
		print ("Page title: '" + pagetitle + "'")
		if BGon==1:
			BGfile=(pageconf.find('BG')).text
			BG=pygame.image.load(BGfile)
		screensurf.fill((170, 170, 170))
		#pygame.event.get()
		#while pygame.mouse.get_pressed()[0]!=0:
		#	pygame.event.get()
		#	print "wait"
		#	print pygame.mouse.get_pressed()[0]
		#	time.sleep(0.1)
		print "done. begin mainloop"
	if BGon==1:
		screensurf.blit(BG, (0, 0))
	#print keylist
	#print keybak
	#if keylist!=keybak or forksanitycheck==1:
	if True:
		#debugmsg("keyid change detected. reparsing forks.")
		for fork in forktag.findall("batchtrig"):
			#print "batchtrig"
			masterkey=fork.attrib.get("keyid")
			complist=[1] 
			for keyif in fork.findall("k"):
				ifpol=keyif.attrib.get("if")
				subkey=keyif.attrib.get("keyid")
				if subkey in keylist:
					if ifpol=="1":
						complist.extend([1])
					else:
						complist.extend([0])
				elif not subkey in keylist:
					if ifpol=="0":
						complist.extend([1])
					else:
						complist.extend([0])
			if len(set(complist)) == 1:
				if not masterkey in keylist:
					keylist.extend([masterkey])
					print keylist
					forksanity=1
			else:
				if masterkey in keylist:
					keylist.remove(masterkey)
					print keylist
					forksanity=1
		for fork in forktag.findall("batchset"):
			#print "batch"
			#print fork
			masterkey=fork.attrib.get("keyid")
			toggpol=fork.attrib.get("set")
			if masterkey in keylist:
				keylist.remove(masterkey)
				if toggpol=="1":
					for subkey in fork.findall("k"):
						subkeyid=subkey.attrib.get("keyid")
						if not subkeyid in keylist:
							keylist.extend([subkeyid])
							print keylist
					forksanity=1
				else:
					for subkey in fork.findall("k"):
						subkeyid=subkey.attrib.get("keyid")
						if subkeyid in keylist:
							keylist.remove(subkeyid)
							print keylist
					forksanity=1
		if forksanity==1:
			forksanitycheck=1
			forksanity=0
			#skiploop=1
		else:
			forksanitycheck=0
			
	keybak=list(keylist)
	for labref in coretag.findall("label"):
		keyid=labref.attrib.get('keyid', "0")
		takekey=labref.attrib.get('takekey', "0")
		onkey=labref.attrib.get('onkey', "0")
		offkey=labref.attrib.get('offkey', "0")
		if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
			labx=int(labref.attrib.get("x"))
			laby=int(labref.attrib.get("y"))
			size=int(labref.attrib.get("size"))
			FGCOL=pygame.Color(labref.attrib.get("FGCOLOR", "#FFFFFF"))
			BGCOL=pygame.Color(labref.attrib.get("BGCOLOR", "#000000"))
			labcon=(labref.find("con")).text
			act=labref.find("act")
			acttype=act.attrib.get("type", "none")
			transp=int(labref.attrib.get("transp", "0"))
			labfnt=pygame.font.SysFont(None, size)
			if transp==0:
				labgfx=labfnt.render(labcon, True, FGCOL, BGCOL)
			else:
				labgfx=labfnt.render(labcon, True, FGCOL)
			clickref=screensurf.blit(labgfx, (labx, laby))
			if acttype!="none":
				pos = pygame.mouse.get_pos()
			if acttype=="iref":
				ref=act.attrib.get("ref")
				#for event in pygame.event.get(MOUSEBUTTONDOWN):
				#pygame.event.get()
				#if clickref.collidepoint(pos)==1 and (pygame.mouse.get_pressed()[0])==1:
				#	curpage=ref
				#	break
				datstr=clicktab(clickref, "iref", ref, keyid, takekey)
				clicklist.extend([datstr])
			if acttype=="quit":
				ref=act.attrib.get("ref")
				#for event in pygame.event.get(MOUSEBUTTONDOWN):
				#pygame.event.get()
				#if clickref.collidepoint(pos)==1 and (pygame.mouse.get_pressed()[0])==1:
				#	quitflag=1
				#	break
				datstr=clicktab(clickref, "quit", ref, keyid, takekey)
				clicklist.extend([datstr])
			if acttype=="key":
				ref=act.attrib.get("ref")
				#for event in pygame.event.get(MOUSEBUTTONDOWN):
				#pygame.event.get()
				#if clickref.collidepoint(pos)==1 and (pygame.mouse.get_pressed()[0])==1:
				#	quitflag=1
				#	break
				datstr=clicktab(clickref, "key", ref, keyid, takekey)
				clicklist.extend([datstr])
		#else:
			#time.sleep(0.04)
	for labref in coretag.findall("img"):
		keyid=labref.attrib.get('keyid', "0")
		takekey=labref.attrib.get('takekey', "0")
		onkey=labref.attrib.get('onkey', "0")
		offkey=labref.attrib.get('offkey', "0")
		if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
			imgx=int(labref.attrib.get("x"))
			imgy=int(labref.attrib.get("y"))
			imgcon=(labref.find("con")).text
			hovpic=int(labref.attrib.get("hovpic", "0"))
			act=labref.find("act")
			acttype=act.attrib.get("type", "none")
			pos = pygame.mouse.get_pos()
			imggfx=pygame.image.load(imgcon)
			clickref=screensurf.blit(imggfx, (imgx, imgy))
			if hovpic==1:
				hovcon=(labref.find("altcon")).text
				hovgfx=pygame.image.load(hovcon)
				if clickref.collidepoint(pos)==1:
					clickref=screensurf.blit(hovgfx, (imgx, imgy))
		
			if acttype!="none":
				pos = pygame.mouse.get_pos()
				if acttype=="iref":
					ref=act.attrib.get("ref")
				#for event in pygame.event.get(MOUSEBUTTONDOWN):
				#pygame.event.get()
				#if clickref.collidepoint(pos)==1 and (pygame.mouse.get_pressed()[0])==1:
				#	curpage=ref
				#	break
					datstr=clicktab(clickref, "iref", ref, keyid, takekey)
					clicklist.extend([datstr])
				if acttype=="quit":
					ref=act.attrib.get("ref")
				#for event in pygame.event.get(MOUSEBUTTONDOWN):
				#pygame.event.get()
				#if clickref.collidepoint(pos)==1 and (pygame.mouse.get_pressed()[0])==1:
				#	quitflag=1
				#	break
					datstr=clicktab(clickref, "quit", ref, keyid, takekey)
					clicklist.extend([datstr])
				if acttype=="key":
					ref=act.attrib.get("ref")
				#for event in pygame.event.get(MOUSEBUTTONDOWN):
				#pygame.event.get()
				#if clickref.collidepoint(pos)==1 and (pygame.mouse.get_pressed()[0])==1:
				#	quitflag=1
				#	break
					datstr=clicktab(clickref, "key", ref, keyid, takekey)
					clicklist.extend([datstr])
	for event in pygame.event.get():
		#print "nominal"
		if event.type==MOUSEBUTTONDOWN:
			#print "nominal2"
			for f in clicklist:
				#print "nominal3"
				if f.box.collidepoint(event.pos)==1 and event.button==1:
					if f.keyid!="0":
						if not f.keyid in keylist:
							keylist.extend([f.keyid])
							print keylist
					if f.takekey!="0":
						if takekey in keylist and f.takekey!="0":
							keylist.remove(f.takekey)
							print keylist
					if f.reftype=="iref":
						curpage=f.ref
						print ("iref: loading page '" + f.ref + "'")
						break
					if f.reftype=="quit":
						print ("quit: onclick quit")
						quitflag=1
						break
	pygame.display.update()
	pygame.event.pump()
	pygame.event.clear()
	