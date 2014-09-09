#python 2.7
from sys import platform as _platform
import os
import string
import random
import shutil
from random import randint
import time
import sys, getopt
import argparse

files = []
showerrors = 0
rebuild = 10
speed = 5.01
root = "./root"
filesperdir = 20
wipe=0

optcreate = 1
optreplace = 1
optrename = 1
optappend = 1
optremove = 1


#########################################################
# Functions for creating random files & directories
#########################################################

wordbank = []

def initwordbank():
    
   wordbank = []
   
   if _platform != "win32":

      word_file = "/usr/share/dict/words"
      wordbank = open(word_file).read().splitlines()

   else:
      wordbank = [''.join(random.choice(string.ascii_uppercase) for _ in range(random.randint(1, 15))) for i in range(50000)]

   return wordbank

def ranname():
    
   return wordbank[random.randint(0, len(wordbank)-1)]

def createroot():

   if os.path.exists(root) and wipe:
      shutil.rmtree(root)
      
   if not os.path.exists(root):
      os.makedirs(root)

   return root

def ranfile(path):

   filename = "{0}/{1}".format(path, ranname())
   with open(filename, 'wb') as fout:
      fout.write(os.urandom(1024))

   return filename

def randir(path):

   dirname = "{0}/{1}".format(path, ranname())
   os.mkdir(dirname)
   return dirname

def ranconent(path):

   for i in range(filesperdir):
      ranfile(path)
   
def getallfiles(path):

   files = []
   for root, dirnames, filenames in os.walk(path):
      for filename in filenames:
         files.append("{0}/{1}".format(root, filename))

   return files

def getalldirs(path):

   dirs = []
   for root, dirnames, filenames in os.walk(path):
      for dirname in dirnames:
         dirs.append("{0}/{1}".format(root, dirname))

   return dirs

def getranitem():

   if len(files):
      return files[randint(0, len(files)-1)]

   return ""

#########################################################
# Functions for performing fs crud actions
#########################################################


def ranaction(path):

   action = randint(0, 5)
   try:

      if action == 0 and optcreate:

         create(path)

      elif action == 1 and optreplace:

         replace(path)

      elif action == 2 and optrename:

         rename(path)

      elif action == 3 and optappend:

         append(path)

      elif action == 4 and optremove:

         remove(path)
         
   except Exception as e:
      error(e)
   
def create(path):

   if randint(0, 5):
      newpath = ranfile(os.path.dirname(path))
      print "Created file:\n\t{0}".format(newpath)
      files.append(newpath)
   else:
      newpath = randir(os.path.dirname(path))
      print "Created dir:\n\t{0}".format(newpath)
      files.append(newpath)
      #create folder

def replace(path):

   newpath = getranitem()
   shutil.move(path, newpath)
   print "Replaced:\n\t{0} \n\t{1}".format(path, newpath)
   files.remove(path)
   files.append(newpath)


def rename(path):

   newpath = "{0}/{1}".format(os.path.dirname(path), ranname())
   os.rename(path, newpath)

   print "Renamed:\n\t{0} \n\t{1}".format(path, newpath)
   files.remove(path)
   files.append(newpath)


def append(path):
  
   with open(path, "a") as fout:
      fout.write(os.urandom(1024))

   print "Appended:\n\t{0}".format(path)

def remove(path):

   if os.path.isdir(path):
      shutil.rmtree(path)
      print "Removed tree: \n\t{0}".format(path)
      files.remove(path)
   else:
      os.remove(path)
      print "Removed: \n\t{0}".format(path)
      files.remove(path)

def error(e):

   global rebuild, files, dirs, showerrors
   if showerrors:
      print "#"*50
      print e

   if str(e).find("[Errno 2] No such file or directory") != -1:
      rebuild -= 1
      if showerrors:
         print "Too much monkeing is killing the file index."
         print "Will rebuilt index after another {0} errors.".format(rebuild)

   if rebuild == 0:
      rebuild = 50
      files = getallfiles(root) + getalldirs(root)
      
      if showerrors:
         print "Rebuilt index"

   if showerrors:
      print "#"*50
   
#########################################################
#########################################################

def monkey():

   while(1):
      ranaction(getranitem())
      time.sleep(speed)

      if len(files) <= 2:
         ranconent(createroot())



#########################################################
#########################################################

def parseargs():

   global speed, rebuild, showerrors, optcreate, optreplace, optrename, optappend, optremove, filesperdir, root, wipe
   
   parser = argparse.ArgumentParser()
   parser.add_argument("-i", "--input", help="Folder to monkey", type=str, default=root)
   parser.add_argument("-s", "--speed", help="Set time between each monkey action", type=float, default=1.0)
   parser.add_argument("-v", "--verbosity", help="Show erros and other stuff", type=int, default=0)
   parser.add_argument("-r", "--rebuild", help="Number of errors before rebuild file index", type=int, default=30)
   parser.add_argument("-f", "--filesperdir", help="Number of files to create in each folder", type=int, default=30)
   parser.add_argument("-w", "--wipe", help="Wipe monkied folder before starting", action="store_true")
   parser.add_argument("--nocreate", help="Don't create files", action="store_true")
   parser.add_argument("--noreplace", help="Don't replace files", action="store_true")
   parser.add_argument("--norename", help="Don't rename files", action="store_true")
   parser.add_argument("--noappend", help="Don't append to files", action="store_true")
   parser.add_argument("--noremove", help="Don't remove files", action="store_true")
   args = parser.parse_args()

   root = args.input
   speed = args.speed
   showerrors = args.verbosity
   rebuild = args.rebuild
   filesperdir = args.filesperdir
   wipe = args.wipe
   optcreate = not args.nocreate
   optreplace = not args.noreplace
   optrename = not args.norename
   optappend = not args.noappend
   optremove = not args.noremove

   return 1

if __name__ == "__main__":

   if parseargs():
      
      wordbank = initwordbank()
      ranconent(createroot())

      files = getallfiles(root) + getalldirs(root)

      monkey()
