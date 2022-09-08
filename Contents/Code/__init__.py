# AEBN
import re, os, urllib, cgi, inspect, unicodedata
from KunbaiLib import *

PLUGIN_LOG_TITLE='P Meta Agent'    # Log Title

VERSION_NO = '0.0.1'

# Delay used when requesting HTML, may be good to have to prevent being
# banned from the site
REQUEST_DELAY = 0

def Start():

  pass

class PMetaMaker(Agent.Movies):
    name = 'p-meta-agent'
    languages = [Locale.Language.NoLanguage, Locale.Language.English]
    fallback_agent = False
    primary_provider = True
    accepts_from = ['com.plexapp.agents.localmedia']
    

    def search(self, results, media, lang, manual):
        Log.Debug('========================================= Start of SEARCH')
        Log.Debug('SEARCH CALLED v.%s', VERSION_NO)
        Log.Debug("SEARCH - media.title -  %s", media.title)
        Log.Debug('SEARCH - media.items[0].parts[0].file -  %s', media.items[0].parts[0].file)
        if media.primary_metadata is not None:
            Log.Debug('SEARCH - media.primary_metadata.title -  %s', media.primary_metadata.title)
        Log.Debug('SEARCH - media.items -  %s', media.items)
        Log.Debug('SEARCH - media.filename -  %s', media.filename)
        Log.Debug('SEARCH - lang -  %s', lang)
        Log.Debug('SEARCH - manual -  %s', manual)

        # Log.Debug('SEARCH - inspect media start -----')
        # metainspmem = inspect.getmembers(media)
        # for mem in metainspmem:
        #     print(mem)
        # Log.Debug('SEARCH - inspect media end -----')


        title = media.title




        if not media.items[0].parts[0].file:
            return


        path_and_file = media.items[0].parts[0].file


        # if media.primary_metadata is not None and media.primary_metadata.title is not None and media.primary_metadata.title is not 'None':
        #     Log.Debug('SEARCH - There is primary metadata pass: %s', media.primary_metadata.title)
        #     title = media.primary_metadata.title
        #     ids = 'primary'


        Log.Debug('SEARCH - File Path: ' + path_and_file)

        #path_and_file = os.path.splitext(path_and_file)[0]
        ids = path_and_file

        results.Append(MetadataSearchResult(id = ids, name = title, score = 99, lang = lang))




    def update(self, metadata, media, lang, force=False):
        Log.Debug('========================================= Start of UPDATE')

        # Log.Debug('UPDATE - inspect media start -----')
        # metainspmem = inspect.getmembers(media)
        # for mem in metainspmem:
        #     print(mem)
        # Log.Debug('UPDATE - inspect media end -----')



        # Log.Debug('UPDATE - inspect metadata attrs start -----')
        # metainspmem = metadata.attrs
        # for mem in metainspmem:
        #     print(mem)
        # Log.Debug('UPDATE - inspect metadata attrs end -----')
        metadata.collections.clear()

        path_and_file = media.items[0].parts[0].file
        Log.Debug('UPDATE - File Path: %s' % path_and_file)

        ret = FileNameParser(path_and_file)

        title = None
        sortTitle = None

        title = ret.title

        if ret is not None and ret.title is not None:
            Log.Debug('UPDATE - lib title: '+  ret.title)
        Log.Debug('UPDATE - So title is : '+  title)

        sortTitle = title

        if ret.studio is not None:
            metadata.studio = ret.studio
            metadata.collections.add(ret.studio.strip())
            title = ret.studio + ' - '  + title
            sortTitle = ret.studio + ' - '  + title
            Log.Debug('UPDATE - Studio: ' + metadata.studio)


        if ret.collection is not None:
            metadata.collections.add(ret.collection.strip())
            sortTitle = ret.collection + ' - ' + sortTitle
            title = ret.collection + ' - ' + title
            Log.Debug('UPDATE - Collection: ' + metadata.collections[0])

        if ret.titlePrefix is not None:
            sortTitle = ret.titlePrefix + ' - ' + sortTitle
            title = ret.titlePrefix + ' - ' + title

        metadata.title_sort = sortTitle
        metadata.original_title = title
        metadata.title = title

        #Log.Debug('UPDATE - title_sort: ' + metadata.title_sort)
        #Log.Debug('UPDATE - original_title: ' + metadata.original_title)
        #Log.Debug('UPDATE - Title: ' + metadata.title)

        if len(ret.tags) > 0:
            metadata.genres.clear()
            metadata.tags.clear()
            for tag in ret.tags:
                metadata.genres.add(tag)
                metadata.tags.add(tag)
                metadata.collections.add(tag.strip())

        for genre in metadata.genres:
            Log.Debug('UPDATE - Genere: ' + genre)

        if len(ret.actors) > 0:
            metadata.roles.clear()
            for cast in ret.actors:
                if len(cast) > 0:
                    role = metadata.roles.new()
                    role.name = cast
                    metadata.collections.add(cast.strip())

        for role in metadata.roles:
            Log.Debug('UPDATE - Role: ' + role.name)

        metadata.content_rating = 'X'
        Log.Debug('UPDATE - Content Rating: ' + metadata.content_rating)

        return metadata
