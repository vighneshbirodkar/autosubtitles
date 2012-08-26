import xmlrpclib as x
import gzip
import os
import urllib as url
import threading
import gui
import wx
import time
import base64
import thread
import string
import psutil
import webbrowser as web
import sys
import httplib
import socket



ERROR = 0
NOTFOUND = None


sys.stdout = open('log.txt','w')
#To open a link
def start(x):
	if sys.platform.startswith('darwin'):
		os.system('open "' + '"' + x +'"')
	elif os.name == 'nt':
		os.startfile(x)
	elif os.name == 'posix':
		os.system('xdg-open "' + x +'"')



def log(s):
    print s



#### Get  name of open video File
def get_file():
    plist = psutil.get_process_list()

    #go through all processes
    for process in plist:
        try:
            #see which process matches gicen video-player names
            if process.name.split('.')[0] not in settings['players']:
                continue
            flist = process.get_open_files()
            for f in flist:
                #to see if file is a video file
                if((f.path.split('.')[-1] in settings['ext'])):
                    #to ensure same file isnt reported again, if more than one plyer is open simultaneously
                    if(process.name in get_file.last_file.keys() ):
                        if(get_file.last_file[process.name] == f.path):
                            continue
                    get_file.last_file[process.name] = f.path
                    return f.path.encode('ascii','ignore')
        except psutil.error.NoSuchProcess:
            pass
    
get_file.last_file = {}



###### To store chaged settings 
def write_sett(filename):
    global settings
    lines = ''
    for i in settings.keys():
        if(type(settings[i]) == type('')):
            lines += '[' + i + ']' + '=' + "'" + settings[i] + "'" + '\n'
        else:
            lines += '[' + i + ']' + '=' + str(settings[i]) + '\n'
    f = open(filename,'w')
    f.write(lines)
    f.close()
    log('Settings Written')

##### Find similarity between strings
# look up "Levenshtein distance"
def lev_dist(s1,s2):
    s1 = ' ' + s1
    s2 = ' ' + s2
    m=len(s1)
    n=len(s2)
    s1 = s1.lower()
    s2 = s2.lower()
    array =[[0]*m for i in range(n)]
    for i in range(m):
        array[0][i] = i
    for i in range(n):
        array[i][0] = i
    for i in range(1,n):
        for j in range(1,m):
            x = array[i-1][j] + 1
            y = array[i][j-1] + 1
            z = array[i-1][j-1]
            if(s1[j]!=s2[i]):
                z=z+1
            array[i][j]=min(x,y,z)
    return array[n-1][m-1]

##### To remove unwanted characters from string
def legalize(s):
    #s=str(s)
    global settings
    #s = s.lower()
    for i in settings['chars']:
        s = s.replace(i,' ')
    l = s.split()
    s = ''
    s +=' ' + l[0]

    for i in l[1:None]:
        # to remove digits from strings like Toy.Story.1996
        #while preserving sequel number like Toy.Story.2.2001
        
        if(i.isdigit() and len(i)==4):
            break
        elif(i in settings['ext']):
            break
        else:
            s += ' ' + i

    s = s[1:None]
    
    if len(s)< (settings['len']):
        return s
    else:
        return s[0:settings['len']]






##### Fetches movie info from string
##### Calculates how similar given string is to the movie name found
class infoThread(threading.Thread):
    global settings
    def __init__(self,string):
        self.error = False
        self.string = string.lower()
        threading.Thread.__init__(self)
    def run(self):
        log('\nSearching Info for :' + self.string)
        try:
            url_handle=url.urlopen('http://www.imdbapi.com/?t='+self.string)
            x={}
            self.info = eval(url_handle.read())
        except IOError:
            self.error = True
            return
        
        if(self.info['Response'] == 'False'):
            #if response is false distance is set to high value,
            #indicating movie name is very dissimilar
            self.dist = settings['max']
        else:
            self.dist = lev_dist(self.string,self.info['Title'])
        #print self.dist,self.string,self.info['Title']
        return None

##compares the dist value of two info threads to see which one has more accurate result
##fetches subtitles

class subThread(threading.Thread):
    def __init__(self,frame,full_path,name,t1,t2):
        global server,settings
        self.frame = frame
        self.thread1 = t1
        self.thread2 = t2
        self.full_path = full_path
        self.name_ = name
        threading.Thread.__init__(self)
    def run(self):
        self.thread1.join()
        self.thread2.join()
        if(self.thread1.error or self.thread2.error):
            wx.CallAfter(self.frame.set_movie,ERROR)
            wx.CallAfter(self.frame.set_sub,ERROR)
            return
        ##comparing to see which thread has fetched correct name
        if(self.thread1.dist < settings['thresh'] or self.thread2.dist < settings['thresh']):
            if(self.thread1.dist >= self.thread2.dist):
                movie = self.thread2.info
            else:
                movie = self.thread1.info
        else:
            wx.CallAfter(self.frame.set_movie,NOTFOUND)
            log('movie not found')
            wx.CallAfter(self.frame.set_sub,NOTFOUND)
            return None
        log(self.thread1.string + ':' + `self.thread1.dist`)
        log(self.thread2.string + ':' + `self.thread2.dist`)
        log('Response : ' + movie['Response'])
        log('Title : ' + movie['Title'])
        wx.CallAfter(self.frame.set_movie,movie)
        #Fetching subtitles
        #refer opensubtitles api for details
        self.query = {'sublanguageid' : settings['lang'],'imdbid':movie['imdbID'][2:None]}
        server_lock.acquire()
        try:
            response = server.SearchSubtitles(token,[self.query])
        except Exception:
            wx.CallAfter(self.frame.set_sub,ERROR)
            server_lock.release()
            return
        server_lock.release()

        if(response['data']==False):
            log('Subtitles not found')
            wx.CallAfter(self.frame.set_sub,NOTFOUND)
            return None
        else:
            log('length = ' + `len(response['data'])`)

        index=0
        mini = 100
        #to determine which subtitle file has the name most similar to the original filename
        #for eg Momento-axxo.avi and Momento-axxo.srt
        for i in range(len(response['data'])):

            k = lev_dist(response['data'][i]['SubFileName'],self.name_)

            if(k < mini):
                mini = k
                index = i

        log('Match Index : ' + `i`)
        subid = response['data'][index]['IDSubtitleFile']
        log('Downloading Subs')
        server_lock.acquire()
        try:
            string = server.DownloadSubtitles(token,[subid])['data'][0]['data']
        except Exception:
            wx.CallAfter(self.frame.set_sub,ERROR)
            server_lock.release()
            return
        server_lock.release()
        log('Decoding Subs')
        string = base64.b64decode(string)

        log('Unzipping Subs')
        self.full_path = self.full_path[0:self.full_path.rfind('.')] + '.srt'
        zipfile = open('tmp.tmp','wb')
        zipfile.write(string)
        zipfile.close()

        zipfile = gzip.open('tmp.tmp','rb')
        subs = zipfile.read()
        zipfile.close()
        
        log('Subtitles Set')
        wx.CallAfter(self.frame.set_sub,subs)
        wx.CallAfter(self.frame.set_sub_details,response,self.full_path)



###### Load Settings File
log('Loading Settings...........')
settings = {}
set_file = file('settings.ini','r')
lines = set_file.readlines()

for line in lines:
    part = line.split('=')
    settings[part[0].strip().rstrip(']').lstrip('[')]=eval(part[1].strip())

set_file.close()


socket.setdefaulttimeout(settings['timeout'])
server = x.ServerProxy(settings['sub_add'])
server_lock = threading.Lock()
slide_lock =  thread.allocate_lock()

while(True):
    try:
        token = server.LogIn('vighneshbirodkar','skepticism','en',settings['user_agent'])['token']
        pass
        break
    except Exception:
        pass
log('Logged into opensubtitles')




IN =0
OUT = 1

##### Main  Information Window

lock =  thread.allocate_lock()
class MyFrame(gui.Frame):
    
    global settings,IN,OUT
    def __init__(self,parent):
        self.time =0
        self.first = True
        self.last = IN
        self.current = IN
        self.closing = False
        self.sctive = False
        self.sliding = False
        log('Initializing GUI') 
        gui.Frame.__init__(self,parent)
        self.movie_dict = None
        self.movie_found = False
        self.sub_found = False
        self.ext = ''
        #self.sub = None
        self.rect =  wx.GetClientDisplayRect()
        self.right = self.rect[0] + self.rect[2]
        self.bottom = self.rect[1] + self.rect[3]

        self.reset()

        self.active = False
        self.color()
        ##### Timer for monitoring open media files
        self.monitor_timer = monitorTimer(self)
        self.monitor_timer.Start(settings['monitor_time'],False)

        self.Show(False)
        ##### Timer to pulse status bars
        self.load_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.pulse, self.load_timer)
        self.load_timer.Start(settings['load_time'],False)

        self.dock()
        self.c = 0
        self.close(None)
        self.tb = TaskBar(None)



    def pulse(self,evt):
        
        self.movie_load.Pulse()
        self.sub_load.Pulse()
        #to see if pointer has gone from in to out, or vice versa
        self.last = self.current
        rect = wx.Rect(self.GetPosition()[0],self.GetPosition()[1],self.GetSize()[0],self.GetSize()[1])
        ms = wx.GetMouseState()
        pos = ms.GetX(),ms.GetY()
        #ignore if pointer goes out of display area
        if(not wx.GetClientDisplayRect().Contains(pos)):
            return
        #compare pointers last known position and current position
        if(rect.Contains(pos)):
            self.current = IN

        else:
            self.current = OUT
        #ignore show or hide when first started
        if(self.first):
                self.first = False
                return
        if(self.last == OUT and self.current == IN):
            log('show')
            self.show()


            
        if(self.last == IN and self.current == OUT):
            log('hide')
            self.hide()



        

    #to adjust size of app to display whatever is visible
    
    def slide(self):

        if(not self.active):
            return
        xi,yi = self.GetSize()
        xf,yf = self.GetBestSize()
        x = xf-xi+4
        y=yf-yi+4
        t=time.time()
        self.sub_load.SetMinSize((250,20))
        self.sub_load.SetSize((-1,20))
        self.sub_apply.SetSize((25,25))
        self.sub_apply.SetMinSize((25,25))
        self.Show(True)
        #so that app cant be expanded
        self.SetMaxSize((max(xi,xf),max(yi,yf)))
        while((time.time() - t) < settings['time']):
            k = (time.time() - t)/settings['time']
            self.SetSize((xi+k*x,yi+k*y))
            
            
            self.Update()
            self.SetPosition((self.right-k*x-xi,self.bottom - k*y-yi))
        self.Refresh()
        self.Update()
        if(self.closing):
            self.Show(False)
            self.closing = False
            self.active = False

    #the list self.items contains all the windows that need to be displayed
    #when the pointer hovers on the app

    #shows all the windows in self.items
    def show(self):
        for item in self.items:
            if( not item.IsShown()):
                item.Show(True)
                item.SetLabel(item.GetLabel())
                item.SetMinSize(item.GetBestSize())
        self.slide()

    #hides all the windows in self.items
    def hide(self):
        for item in self.items:
            if(item.IsShown()):
                item.Show(False)
        self.slide()


    #hides all windows and sets size of app to (0,0)
    def close(self,e):
        self.closing = True
        for child in self.GetChildren():
            child.Show(False)
        self.SetMinSize((0,0))
        self.slide()

    #positions app on bottom right
    
    def dock(self):
        self.SetSize((25,25))
        self.SetPosition((self.right ,self.bottom))
        
        
    #sets the movie details for the app to display
    def set_movie(self,dic):
        #return
        self.first = False
        self.movie_load.Show(False)
        self.movie_found = True
        if(dic == NOTFOUND):
            string = 'Movie not Found'
            self.movie_head.SetLabel(string)
        elif(dic == ERROR):
            string = 'Could not Fetch Info'
            self.movie_head.SetLabel(string)
        else:
            #to display movie page when movie  is found
            self.movie_head.SetURL('www.imdb.com/title/' + dic['imdbID'])
            string = ''
            string += 'Rating : ' + dic['imdbRating'] + '\n'
            string += dic['Plot']
            self.movie_head.SetLabel(dic['Title'] + ' (' + dic['Year'] + ')')
            

            
        self.movie.SetLabel(string)
        self.movie.Wrap(settings['width'])
        self.movie_dict = dic

        self.movie_head.Show(True)
        self.movie_head.SetMinSize(self.movie_head.GetBestSize())
        self.movie.SetMinSize(self.movie.GetBestSize())
        
        self.slide()

        
        return
    
    #sets the subtitle details for the movie to display
    def set_sub(self,sub):
     
        self.sub_found = True
        
        if(sub == NOTFOUND):
            self.sub.SetLabel('Subtitle Not Found')
            #self.sub_load.Show(False)
            if(self.sub_load in self.items):
                self.items.remove(self.sub_load)
        elif(sub == ERROR):
            self.sub_load.Show(False)
            self.sub.SetLabel('Could Not Fetch Subtitles')
            self.sub.SetSize(self.sub.GetBestSize())
            self.sub.SetMinSize(self.sub.GetBestSize())
            self.Update()
            if(self.sub_load in self.items):
                self.items.remove(self.sub_load)
        
        else:
            self.sub_buffer = sub
            #to display subtitle page when subtitle is found
            self.sub.SetURL('http://www.opensubtitles.org/search/sublanguageid-' +settings['lang'] + '/' + 'imdbid-' + self.movie_dict['imdbID'][2:None])
            self.sub.SetLabel('Subtitles Found')
            self.sub.SetSize(self.sub.GetBestSize())
            self.sub.SetMinSize(self.sub.GetBestSize())
            self.Update()
            self.items+=[self.sub_apply]
            if(self.sub_load in self.items):
                self.items.remove(self.sub_load)
            
            self.sub_load.Show(False)



            if(self.current == IN):
                self.sub_apply.SetSize((25,25))
                self.sub_apply.SetMinSize((25,25))
                self.sub_apply.Show(True)

            self.Refresh()
            self.Update()
            

            
        self.slide()

            

    # to set the unzipped decoded subs to write to a file
    #when sub_apply is clicked
    def set_sub_details(self,dic,path):
        self.sub_path = path
        self.sub_dic = dic
        
    #restart the movie with subtitles
    def sub_restart(self,e):
        f = open(self.sub_path,'w')
        f.write(self.sub_buffer)

        f.close()
        start(self.movie_path)
        self.Update()
        
    #rests variables
    #donw whenever a new media is detected
    def reset(self):
        
        
        self.items =[self.movie,self.sub_load,self.sub,self.line]
        
        self.closing = False
        
        self.active = True
        self.movie_head.SetURL('www.imdb.com')
        self.sub.SetURL('www.opensubtitles.org')
        self.movie.SetLabel('Searching Movie')
        self.sub.SetLabel('Searching Subtitles')
        self.movie_found = False
        self.sub_found = False
        self.entering  = False
        
        self.movie.Show(False)
        #hide all children
        for child in self.GetChildren():
            child.SetMinSize((0,0))
            child.SetSize((0,0))
            child.Show(False)
        #show required children
        self.movie_load.SetMinSize((250,20))
        self.movie_load.SetSize((250,20))
        self.movie_load.Show(True)
        
        self.button.SetMinSize((25,25))
        self.button.SetSize((25,25))
        self.button.Show(True)

        

       
        
        self.Show(False)
        self.SetPosition((self.bottom,self.right))
        log('Reset Done')
        return

    # set path of the movie
    def set_path(self,s):
        self.movie_path = s
        self.ext = self.movie_path.split('.')[-1].lower()
    

    def color(self):
        self.SetTransparent(settings['alpha'])



        

        
    
        
class MyAboutFrame(gui.AboutFrame):
    def __init__(self,parent):
        gui.AboutFrame.__init__(self,parent)
                

            
    def close(self,e):
        self.Destroy()
    def paint(self,evt):
        pass



        
    

class TaskBar(wx.TaskBarIcon):
    
    TB_ABOUT = wx.NewId()
    TB_CLOSE = wx.NewId()
    TB_SETTINGS = wx.NewId()
    def __init__(self,parent):
        
                
        wx.TaskBarIcon.__init__(self)
        icon = wx.EmptyIcon()
        b = wx.Bitmap('graphics/icon.png')
        icon.CopyFromBitmap(b)
        self.SetIcon(icon,settings['name'])
        self.Bind(wx.EVT_MENU, self.About, id=self.TB_ABOUT)
        self.Bind(wx.EVT_MENU, self.ShutDown, id=self.TB_CLOSE)
        self.Bind(wx.EVT_MENU, self.Setting, id=self.TB_SETTINGS)
    def CreatePopupMenu(self, evt=None):
        menu = wx.Menu()
        menu.Append(self.TB_ABOUT, "About")
        menu.Append(self.TB_SETTINGS, "Settings")
        menu.Append(self.TB_CLOSE, "Quit")
        return menu
    def About(self,e):
        abt_frame = MyAboutFrame(None)
        abt_frame.Show(True)
    def ShutDown(self,e):
        log('Shutting Down')
        os._exit(0)
    def Setting(self,e):
        sett_frame = MySettingsFrame(None)
        sett_frame.Show(True)
        
        
                
class MySettingsFrame(gui.SettingsFrame):

    def __init__(self,parent):
        gui.SettingsFrame.__init__(self,parent)
        self.Bind(wx.EVT_CLOSE, self.close)
        wx.CallAfter(f.slide)

    def close(self,evt):
        write_sett('settings.ini')
        self.Destroy()
    #to change transperency of app
    def alpha(self,evt):
        settings['alpha'] = evt.GetPosition()
        f.color()
    
class monitorTimer(wx.Timer):
    def __init__(self,frame):


        self.frame = frame

        wx.Timer.__init__(self,None)
        self.subtitle_thread = None

    def Notify(self):
##        if(self.subtitle_thread!=None):
##            if(self.subtitle_thread.isAlive()):
##                return None
        sub_thread = None
        
        moive_found = False

        if(sub_thread!=None and sun_thread.IsAlive()):
            return
############################
        path = get_file()
        
        if(path==None):
            return
        name = path.split(os.sep)[-1]
        location = path[0:len(path)-len(name)-1]
        folder = location.split(os.sep)[-1]
        log('Media Detected : '  + path)
        wx.CallAfter(self.frame.set_path,path)
        wx.CallAfter(self.frame.reset)
        #start searching with filename and folder name
        name_thread = infoThread(legalize(name))
        name_thread.start()

        folder_thread = infoThread(legalize(folder))
        folder_thread.start()




        wx.CallAfter(self.frame.slide)



        
        self.subtitle_thread = subThread(self.frame,path,name,name_thread,folder_thread)
        self.subtitle_thread.start()



app = wx.App(False)
f = MyFrame(None)

app.MainLoop()






