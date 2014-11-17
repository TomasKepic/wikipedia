 #!/usr/bin/python3 

import os
import unicodedata
import curses
import datetime
from collections import namedtuple
        
def check_path(value):
    svalue = value.strip()
    if not os.path.isfile(svalue):
         raise ArgumentTypeError("%s is an invalid file path" % svalue)
    return svalue

def getsel(res1, sel):
   try:
    stdscr = curses.initscr()
    stdscr.erase()
    stdscr.refresh()
    print_menu(stdscr, res1, sel)
    curses.cbreak()
    stdscr.keypad(1)
    curses.nonl()
    curses.curs_set(0)
    key = stdscr.getch()
   except Exception:
   	pass
   finally:
    curses.endwin()	   
   return key

def get_elem(iterable):
  return iterable.split(';')[1]

def print_menu(scr, res1, sel):
             res1.sort(key=get_elem)
             for i, line in enumerate(res1):
                line=line.replace('|',', ')
                line=line.split(';')
                line[0]=line[0].ljust(35)
                line[1]=line[1].rjust(11)
                line[1]+=' - '
                if i == sel:
                   scr.addstr('->>\t'+' '.join(line) + '\n', curses.A_BOLD)
                else:
                   scr.addstr('\t'+' '.join(line)+ '\n')
def getPerson(num, fi):
        res1=list()
        os.system('clear')
        while len(res1)==0:
          x = input(str(num) + '. name : ')
          fi.seek(0, 0)
          for line in fi.readlines():
            input_normalized = unicodedata.normalize('NFKD', x.strip().lower()).encode('ascii','ignore').decode('ascii')
            line_normalized = unicodedata.normalize('NFKD', line.split(';')[0].lower()).encode('ascii','ignore').decode('ascii')
            birth=line.split(';')[1]
            full_match=True
            for input_word in input_normalized.split(' '):
            	if  input_word not in line_normalized:
            		full_match= False
            if full_match and input_normalized.strip() and birth and '?' not in birth:
            	res1.append(line.strip())
          os.system('clear')   
          if len(res1)>SEARCH_LIMIT:
             res1=list()
             print('Please enter more specific keyword')
          elif len(res1)==0:
             print('No matching entry found')   
          

        sel=0
        while len(res1)>1:
           c=getsel(res1, sel)
           if c==curses.KEY_DOWN and sel<(len(res1)-1):
                  sel+=1
           elif c ==curses.KEY_UP and sel>0:
                  sel-=1
           elif c == curses.KEY_ENTER or c == 13:
           	break
        return res1[sel]
def getDates(res1):
        Range = namedtuple('Range', ['start', 'end'])
        firstB=res1.split(';')[1]
        firstB=datetime.datetime(int(firstB.split('.')[2]), int(firstB.split('.')[1]), int(firstB.split('.')[0]))
        firstD=res1.split(';')[2]
        if firstD:
           firstD=datetime.datetime(int(firstD.split('.')[2]), int(firstD.split('.')[1]), int(firstD.split('.')[0]))
        else:
           firstD=datetime.datetime.now()
        return Range(start=firstB, end=firstD)
     
SEARCH_LIMIT = 24
if __name__ == '__main__':
        from argparse import ArgumentParser,ArgumentTypeError
        import termios
        parser = ArgumentParser()
        parser.add_argument("-f", "--file", dest="input_filename", required=True,
                               help="read parsed FILE", metavar="FILE", type=check_path)
        args = parser.parse_args()
        fi = open(args.input_filename, "r")
        res1=getPerson(1, fi)
        res2=getPerson(2, fi)
        os.system('clear')
        print(res1.split(';')[0].ljust(35) +res1.split(';')[1].rjust(11)+' - '+res1.split(';')[2]+'  '+res1.split(';')[3].replace('|',', '))
        print(res2.split(';')[0].ljust(35) +res2.split(';')[1].rjust(11)+' - '+res2.split(';')[2]+'  '+res2.split(';')[3].replace('|',', '))
        r1 = getDates(res1) 
        r2 = getDates(res2) 
        latest_start = max(r1.start, r2.start)
        earliest_end = min(r1.end, r2.end)
        overlap = (earliest_end - latest_start).days + 1
        print(' ')
        if overlap > 0:
           print('Overlap:\t' + str(int(overlap/365)) + ' years')
        else:
          print('NO overlap\t(' + str(int(overlap/365)) + ' years)')
        match=False
        for place1 in res1.split(';')[3].split('|'):
           place1=unicodedata.normalize('NFKD', place1.lower()).encode('ascii','ignore').decode('ascii')
           for place2 in res2.split(';')[3].split('|'):
              place2=unicodedata.normalize('NFKD', place2.lower()).encode('ascii','ignore').decode('ascii')
              if (place1 and place1 in place2) or (place2 and place2 in place1):
                match=True
        if match:
          print("Location match")
        else:
          print('Location does not match')
        print(' ')