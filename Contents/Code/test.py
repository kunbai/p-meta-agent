from KunbaiLib import *
import inspect
import logging
logging.basicConfig(level=logging.DEBUG)
class fp(FileNameParser):
    def Log(self, message, *args):
        #logging.debug(message, *args)
        print(message)
        #print()


#parser = FileNameParser("/volume1/personal/videos/GWest/#Asian in West Collection/nathanbenhi-1468347405.wmv");
#parser = fp("/volume1/personal/videos/GWest/@Wizard Collection/[StuidoName] - title is Title @actor1 and actor2@ #raw #real.wmv");

#parser = fp("/volume1/personal/videos/Social/#others/title.aiv");
parser = fp('/volume1/personal/videos/GWest/#Wizard Collection/#hidhfi dfjdk');

#parser = FileNameParser("/volume1/personal/videos/GWest/@Keichi, Watane Collection/nathanbenhi-1468347405.wmv");

print('------------ title - ' + parser.title)
if parser.studio is not None:
    print('------------ studio - ' + parser.studio)
if parser.collection is not None:
    print('------------ collection - ' + parser.collection)
for a in parser.actors:
    print('------------ actor - ' + a)
for a in parser.tags:
    print('------------ tag - ' + a)
