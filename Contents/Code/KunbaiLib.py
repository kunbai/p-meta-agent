import re, os, urllib, cgi, urllib2

class FileNameParser():

    TopTopCategories = ('GEast', 'GWest', 'GWest2', 'GWest3', 'SEast', 'SWest','SWest2','SWest3', 'Social')
    TopCategories = ('GEast', 'GWest', 'GWest2', 'GWest3', 'SEast', 'SWest','SWest2','SWest3', 'Social', 'xvideo.com', 'amatures','91porn.com','9isex.net','porn.com','mymusclevideo.com','pornhub.com','xtube.com')
    filePath = None
    fileName = None
    finalDir = None
    upperDir = None
    upperDir2 = None
    upperDir3 = None
    upperDir4 = None
    topCategory = None
    collection = None
    studio = None
    title = None
    titlePrefix = None
    actors = set()
    tags = set()
    hints = set()

    def __init__(self, filePath):
        self.Log('=================================================')

        self.hints.clear()
        self.actors.clear()
        self.tags.clear()
        self.filePath = None
        self.fileName = None
        self.finalDir = None
        self.upperDir = None
        self.upperDir2 = None
        self.upperDir3 = None
        self.upperDir4 = None
        self.topCategory = None
        self.collection = None
        self.studio = None
        self.title = None
        self.titlePrefix = None


        self.baseParse(filePath)
        self.parseDir()
        #print(self.hints)
        if 'studio' not in self.hints:
            studio = self.getStudio(self.fileName)
            if studio is not None:
                self.studio = studio

        if 'collection' not in self.hints:
            collection = self.getCollection(self.fileName)
            if collection is not None:
                self.collection = collection

        actors = self.getActors(self.fileName)
        if actors is not None and len(actors) > 0:
            for actor in actors:
                self.actors.add(actor)

        tags = self.getTags(self.fileName)
        if tags is not None and len(tags) > 0:
            for tag in tags:
                self.tags.add(tag)


        self.title = self.getTitle(self.fileName)


    def Log(self, message, *args):
        Log('FilenameParser - ' + message, *args)
        #print('FilenameParser - ' + message)
        #logging.debug(message, *args)


    def urlencode(self, s):
        return urllib2.quote(s)

    def urldecode(self, s):
        return urllib2.unquote(s).decode('utf8')


    def baseParse(self, filePath):
        #filePath = self.urldecode(filePath)
        filePath = filePath.replace('_', ' ')
        self.filePath = filePath
        self.Log('baseParse - ' + 'starts with filePath: ' + filePath)
        (fileDir, basename) = os.path.split(os.path.splitext(filePath)[0])
        finalDir = os.path.split(fileDir)[1]
        (fileDir, upperDir) = os.path.split(os.path.split(fileDir)[0])

        basename.strip()
        finalDir.strip()
        upperDir.strip()

        self.fileName = basename
        self.finalDir = finalDir
        self.upperDir = upperDir

        self.Log("baseParse - upperDir: " + upperDir)
        self.Log("baseParse - finalDir: " + finalDir)
        self.Log("baseParse - fileName: " + basename)

    def parseDir(self):
        self.Log('parseDir - starts with filePath: ' + self.filePath)

        hint = None
        hint2 = None
        hint3 = None
        hint4 = None
        hintType = None
        self.topCategory = None

        if self.finalDir in self.TopCategories and self.finalDir is not 'videos':
            self.topCategory = self.finalDir
        elif self.upperDir in self.TopCategories and self.upperDir is not 'videos':
            hint = self.finalDir
            self.topCategory = self.upperDir
        elif self.upperDir2 in self.TopCategories and self.upperDir2 is not 'videos':
            hint = self.finalDir
            hint2 = self.upperDir
            self.topCategory = self.upperDir2
        elif self.upperDir3 in self.TopCategories and self.upperDir3 is not 'videos':
            hint = self.finalDir
            hint2 = self.upperDir
            hint3 = self.upperDir2
            self.topCategory = self.upperDir3


        if self.topCategory is not None:
            self.Log('parseDir - topCategory: ' + self.topCategory)

        if hint is not None:
            self.Log('parseDir - hint: ' + hint)
        if hint2 is not None:
            self.Log('parseDir - hint2: ' + hint2)
        if hint3 is not None:
            self.Log('parseDir - hint3: ' + hint3)
        if hint4 is not None:
            self.Log('parseDir - hint4: ' + hint4)

        if hint is None:
            hintType = 'fileName'
            self.hints.add(hintType)
        else:
            col = self.getCollection(hint)
            if col is not None: # has collection
                self.Log('Collection: ' + col)
                self.collection = col
                if col.find('(actor)') is -1:
                    self.tags.add(col)
                hintType = 'collection'
                self.hints.add(hintType)

            actors = self.getActors(hint)
            if actors is not None:
                self.actors = actors
                hintType = 'actor'
                self.hints.add(hintType)

            # tags = self.getTags(hint)
            # if tags is not None:
            #     self.tags = tags
            #     hintType = 'tag'
            #     self.hints.add(hintType)

        if self.topCategory is not None:
            self.tags.add(self.topCategory)

        if hint is '#others':
            self.hints.add('studio')



        if self.topCategory not in self.TopTopCategories:
            self.studio = self.topCategory

            self.tags.add('Social')
            if hint is not None and hint.find('#') is -1:
                self.actors.add(hint)
                self.titlePrefix = hint




            hintType = 'studio'
            self.hints.add(hintType)

        else:
            if col is None and actors is None:
                if hint.find('#') is -1:
                    self.studio = self.getTitle(hint)
                    hintType = 'studio'
                    self.hints.add(hintType)

                #print('if col is None and actors is None and tags is None:')


        for h in self.hints:
            self.Log('parseDir - Hints Type: '+ h)



    def getTitle(self, input):
        self.Log('getTitle - starts with: ' + input)

        cName = input
        if cName.find('#') is 0:
            cName = cName[1:]

        type1 = re.compile("^\[[a-zA-Z\s@\.\-]+\]")
        st = type1.findall(cName)
        if len(st) > 0:
            cName = cName.replace(st[0],'')

        type2 = re.compile("^\([a-zA-Z\s@\.\-]+\)")
        st2 = type2.findall(cName)
        if len(st2) > 0:
            cName = cName.replace(st2[0],'')

        reTag = re.compile('#[a-zA-Z0-9]+')
        tt = reTag.findall(cName)
        if len(tt) > 0:
            for t in tt:
                cName = cName.replace(t, '')



        # if cName.find(' - ') > 0:
        #     cName = cName.split(' - ')[1]

        # if cName.find(' @') > 0:
        #     cName = cName.split(' @')[0]

        cName = cName.replace('#','')
        cName = cName.replace('_',' ')
        cName = cName.replace('+',' ')
        cName = cName.replace('Collection','')
        cName = cName.replace('collection','')
        cName = cName.replace('@','')



        cName = cName.replace('-',' ').strip()

        self.Log('getTitle - RESULT: ' + cName)
        return cName




    def getCollection(self, input):
        self.Log('getCollection - starts with: ' + input)
        cName = input

        if cName.find('#') is 0:
            cName = cName[1:]

        if cName.find(' Collection') > -1 or cName.find(' collection') > -1: #collection
            hasActor = False
            if cName.find('@') > -1:
                hasActor = True

            cName = cName.split('Collection')[0].strip()
            cName = cName.replace('@','')
            if hasActor is True:
                cName =  cName + ' (actor)'
            self.Log('getCollection - RESULT: ' + cName)
            return cName
        else:
            self.Log('getCollection - RESULT: None')
            return None

    def getTags(self, input):
        self.Log('getTags - starts with: ' + input)
        cName = input

        if cName.find('#') is 0:
            cName = cName[1:]

        if cName.find('#') > -1: #collection

            if cName.find('#') is 0:
                cName = cName[1:]

            cName = input.replace('@','')
            cName = cName.replace('_',' ')
            cName = cName.replace('+',' ')
            cName = cName.replace('Collection','')
            cName = cName.replace('collection','')
            cName.strip()
            tags= set()


            reTag = re.compile('#[a-zA-Z0-9]+')

            tt = reTag.findall(cName)

            if tt is not None and len(tt) == 0:
                return None

            for t in tt:
                t = t.replace('#', '').lower()
                self.Log('getTags - RESULT: ' + t)
                tags.add(t)

            #self.Log('Tags: ', len(tags))
            return tags

        else:
            return None


    def getActors(self, input):
        self.Log('getActors - starts with: ' + input)
        actorStr = input
        if actorStr.find('#') is 0:
            actorStr = actorStr[1:]
        actorStr = actorStr.replace('_',' ')
        actorStr = actorStr.replace(' Collection','')
        actorStr = actorStr.replace(' collection','')

        type1 = re.compile("^\[[a-zA-Z\s@\.\-]+\]")
        st = type1.findall(actorStr)
        if len(st) > 0:
            actorStr = actorStr.replace(st[0],'')

        type2 = re.compile("^\([a-zA-Z\s@\.\-]+\)")
        st2 = type2.findall(actorStr)
        if len(st2) > 0:
            actorStr = actorStr.replace(st2[0],'')

        reTag = re.compile('#[a-zA-Z0-9]+')
        tt = reTag.findall(actorStr)
        if len(tt) > 0:
            for t in tt:
                actorStr = actorStr.replace(t, '')

        actorStr = actorStr.replace(' - ','').strip()
        self.Log('getActors - RESULT1: ' + actorStr)

        result = list()
        actors = None

        # case 1 : explicit name
        if actorStr.find("@") > -1:

            actors = set()

            start = actorStr.find("@") + 1

            if actorStr.count('@') == 2:
                serch = actorStr[start:]
                self.Log(serch)
                end = serch.find('@')
                parsable = serch[:end]
            elif actorStr.count('@') == 1:
                parsable = actorStr[start:]

            self.Log('getActors - parsable: ' + parsable)

            actorsStr = parsable.strip()

            actorStr = actorStr.replace('#','')

            splits = (',', ' and ', ' And ', ' AND ', ' fuck ', ' fucks ', ' Fucks ', ' Fuck ', ' & ')

            for sp in splits:
                temp = actorsStr.split(sp)
                if(len(temp) > 1):
                    for ac in temp:
                        self.Log('getActors - RESULT: ' + ac)
                        actors.add(ac.strip())

            return actors
        else:
            return None

    def getStudio(self, input):
        self.Log('getStudio - starts with: ' + input)
        cName = input
        studio = None


        type1 = re.compile("^\[[a-zA-Z\s@\.\-]+\]")
        st = type1.findall(cName)

        type2 = re.compile("^\([a-zA-Z\s@\.\-]+\)")
        st2 = type2.findall(cName)

        if len(st) > 0:
            studio = st[0]
            studio = studio.replace('[','').replace(']','').strip()
        elif len(st2) > 0:
            studio = st2[0]
            studio = studio.replace('(','').replace(')','').strip()
        # elif cName.find(' - ') > 0:
        #     studio = cName.split(' - ')[0].strip()


        if studio is not None:
            self.Log('getActors - RESULT: ' + studio)
        else:
            self.Log('getActors - RESULT: None')
        return studio
