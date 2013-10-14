from pygoogle import pygoogle
import subprocess
import time
import sys
import os.path
import unicodedata
import glob
import shutil
from couchpotato.core.providers.trailer.base import VFTrailerProvider
from couchpotato.core.helpers.variable import mergeDicts, getTitle
from couchpotato.core.logger import CPLog
log = CPLog(__name__)
rootDir = os.path.dirname(os.path.abspath(__file__))
try:
    _DEV_NULL = subprocess.DEVNULL
except AttributeError:
    _DEV_NULL = open(os.devnull, 'wb')
class vftrailers(VFTrailerProvider):
    def search(self, group, filename, destination):
        movie_name = getTitle(group['library'])
        movienorm = unicodedata.normalize('NFKD', movie_name).encode('ascii','ignore')
        movie_year = group['library']['year']
        searchstring=movienorm+' '+ str(movie_year) +' bande annonce vf HD'
        time.sleep(3)
        log.info('Searching google for: %s', searchstring)
        g = pygoogle(str(searchstring))
        diclist = g.search()
        urllist = g.get_urls()
        cleanlist=[]
        for x in urllist:
            if 'youtube' in x or 'dailymotion' in x:
                cleanlist.append(x)
        if cleanlist:
            bocount=0
            for bo in cleanlist:
                if bocount==0:
                    tempdest=unicodedata.normalize('NFKD', os.path.join(rootDir,filename)).encode('ascii','ignore')+u'.%(ext)s'
                    dest=destination+u'.%(ext)s'
                    log.info('Trying to download : %s to %s ', (bo, tempdest))
                    subprocess.check_call([sys.executable, 'youtube_dl/__main__.py', '-o',tempdest,'--newline', bo],cwd=rootDir, shell=False, stdout=_DEV_NULL,stderr=subprocess.STDOUT)
                    listetemp=glob.glob(os.path.join(rootDir,'*'))
                    filecount=0
                    for listfile in listetemp:
                        if unicodedata.normalize('NFKD', filename).encode('ascii','ignore') in listfile:
                            ext=listfile[-4:]
                            finaldest=destination+ext
                            shutil.move(listfile, finaldest)
                            bocount=1
                            filecount=1
                            log.info('Downloaded trailer for : %s', movienorm)
                            return True
                    if filecount==0:
                        continue
        else:
            return False
    
