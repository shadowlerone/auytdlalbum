'''
Usage: autoytdlalbum.py {outputfoldername} {querymetadata} {coverartfilepath}
'''

import sys
import eyed3
import os
from genericpath import isfile, isdir
import shutil
from eyed3.core import Date
import subprocess

import colorama
from colorama import Fore, Style

eyed3.log.setLevel("ERROR")

args = sys.argv
currdir = os.path.dirname(os.path.realpath(__file__))



outputdir = "output"
artistInput = "Various Artists"
albumArtistInput = "Various Artists"
albumInput = "Extra Sounds"
discNumInput = 1
yearInput = 2022
genreInput = ""

def assignValuesArgs():
    global outputdir
    global artistInput
    global albumArtistInput
    global albumInput
    global discNumInput
    global yearInput
    global genreInput
    
    if(len(args) >= 3):
        strr = args[2]
        strrspl = strr.split('|')
        
        for s in strrspl:
            
            if('=' not in s):
                print(Fore.RED + 'The provided argument could not be processed.')
                print('Formal: {tag} = {tag to set}|...' + Style.RESET_ALL)
                return False
            
            else:
                trr = s.split('=')
                prefix = trr[0].strip()
                suffix = trr[1].strip()
                
                if('alb' in prefix and 'art' in prefix):
                    albumArtistInput = suffix
                    
                elif('alb' in prefix):
                    albumInput = suffix
                    
                elif('art' in prefix):
                    artistInput = suffix
                    
                elif('dis' in prefix):
                    discNumInput = int(suffix)
                    
                elif('year' in prefix):
                    yearInput = int(suffix)
                    
                elif('gen' in prefix):
                    genreInput = suffix
              
        print("Metadata set: Album artist: " + albumArtistInput + ", " + "Album: " + albumInput + ", " + "Artist: " + artistInput + ", " + "Disc Number: " + str(discNumInput) + ", " + "Release Year: " + str(yearInput) + ", " + "Genre: " + genreInput)  
        return True

#URL = "https://www.youtube.com/watch?v=0z2ziPX7Y34"
#someFilename = os.system('yt-dlp -x --audio-format mp3 --yes-playlist --audio-quality 0 ' + URL)

def processtree(dir):
    print("Copying...")
    dirlist = os.listdir(dir)
    for x in dirlist:
        if(isdir(dir + '\\' + x) and not x == outputdir):
            processtree(dir + "\\" + x)
            
        elif(isfile(dir + '\\' + x) and ('dir' + '\\' + x).lower().endswith('.mp3')):
            copytodir(dir + '\\' + x)
            

def copytodir(filepath):
    if(not os.path.exists(outputdir + '\\' + str(os.path.basename(filepath)))):
        shutil.copy2(filepath, outputdir)
    
def setAttributes(dir):
    dirlist = os.listdir(dir + '\\' + outputdir)
    for x in dirlist:
        print("Adding tag to " + x)
        mp3file = eyed3.load(dir + '\\' + outputdir + '\\' + x)
        
        if(mp3file.tag._getArtist() is None):
            mp3file.tag.artist = artistInput
            
        if(mp3file.tag._getAlbum() is None):
            mp3file.tag.album = albumInput
            
        if(mp3file.tag._getAlbumArtist() is None):
            mp3file.tag.album_artist = albumArtistInput
         
        if(mp3file.tag.disc_num.count is None):
            mp3file.tag.disc_num = discNumInput
        
        if(mp3file.tag.recording_date is None):
            mp3file.tag.recording_date = Date(yearInput)
            
        if(mp3file.tag.genre is None):
            mp3file.tag.genre = genreInput
        
        if(mp3file.tag._getTitle() is None):
            index = x.rfind('[')
            
            if(index == -1):
                index = x.rfind('.mp3')
                if(index == -1):
                    continue
                
            name = x[:index].strip()
        
            mp3file.tag.title = name
        
        mp3file.tag.save()
        print("Added tag to " + x)

def setTrackNum(dir):
    dirlist = os.listdir(dir + '\\' + outputdir)
    
    i = 0
    found = True
    
    print('Calculating index...')
    while(i < 1000 and found):
        found = False
        i += 1
        
        for x in dirlist:
            mp3file = eyed3.load(dir + '\\' + outputdir + '\\' + x)
            if(mp3file.tag._getTrackNum().count == i):
                
                found = True
                break
            
    for x in dirlist:
        mp3file = eyed3.load(dir + '\\' + outputdir + '\\' + x)
        
        if(mp3file.tag._getTrackNum().count is None):
            print("Adding track number to " + x)
            mp3file.tag.track_num = i
            mp3file.tag.save()
            i += 1
            
def setCover(dir, image_path):
    dirlist = os.listdir(dir + '\\' + outputdir)
    for x in dirlist:
        mp3file = eyed3.load(dir + '\\' + outputdir + '\\' + x)
        with open(image_path, "rb") as cover_art:
            print("Adding cover art to " + x)
            mp3file.tag.images.set(3, cover_art.read(), "image/jpeg")
            
        mp3file.tag.save()        

#Main

if(assignValuesArgs()):
    if(len(args) >= 2):
        outputdir = args[1]
    
    if not os.path.exists(outputdir): os.mkdir(outputdir)
        
    processtree(os.getcwd())
    setAttributes(os.getcwd())
    setTrackNum(os.getcwd())
    
    if(len(args) >= 4):    setCover(os.getcwd(), args[3])
    
    print(Fore.GREEN + "Finished" + Style.RESET_ALL)

