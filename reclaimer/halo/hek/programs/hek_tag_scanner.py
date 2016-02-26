import os
import threading

from time import time
from traceback import format_exc

from ..handler import HaloHandler
from supyr_struct.handler import Handler

class HekTagScanner(HaloHandler):
    log_filename = "HEK_Tag_Scanner.log"
    print_to_console = False

    feedback_interval = 10
    feedback_indent   = 8
    mode = 0
    
    #initialize the class
    def __init__(self, **kwargs):
        HaloHandler.__init__(self, **kwargs)
        
        #Create and start the feedback printout thread
        self._feedback_thread = threading.Thread(target=self._feedback)
        self._feedback_thread.daemon = True
        self._feedback_thread.start()


    '''this will significantly speed up indexing tags since the default
    Handler.get_tag_id method doesnt open each file and try to read
    the 4CC Tag_Cls from the header, but just matches file extensions'''
    get_tag_id = Handler.get_tag_id

    def _feedback(self):
        start = time()
        while True:
            if self.print_to_console and time()-start >= self.feedback_interval:
                start = time()
                if self.mode in range(1, 3):
                    print(' '*self.feedback_indent +
                          self.current_tag.split(self.tagsdir)[-1])


    def load_tags(self, paths = None):        
        #local references for faster access
        directory = self.tagsdir
        tags      = self.tags
        allow     = self.allow_corrupt
        new_tag   = None
        build_tag = self.build_tag      

        #Loop over each tag_id in the tag paths to load in sorted order
        for tag_id in sorted(tags):
            tag_coll = tags.get(tag_id)

            if not isinstance(tag_coll, dict):
                tag_coll = tags[tag_id] = {}
            
            #Loop through each tagpath in Coll in sorted order
            for tagpath in sorted(tags[tag_id]):
                
                #only load the tag if it isnt already loaded
                if tag_coll.get(tagpath) is None:
                    self.current_tag = tagpath
                        
                    '''incrementing tags_loaded and decrementing tags_indexed
                    in this loop is done for reporting the loading progress'''
                    
                    try:
                        new_tag = build_tag(filepath = directory+tagpath,
                                            allow_corrupt = allow)
                        tag_coll[tagpath] = new_tag
                        self.tags_loaded += 1
                    except (OSError, MemoryError) as e:
                        print(format_exc())
                        print('Not enough accessable memory to continue '+
                              'loading tags. Ran out while opening\\reading:'+
                              ('\n    %s\n    Remaining unloaded tags will ' +
                               'be de-indexed and skipped\n') % tagpath)
                        del tag_coll[tagpath]
                        self.clear_unloaded_tags()
                        return
                    except Exception:
                        print('Error encountered while opening\\reading:'+
                              '\n    %s\n    Tag may be corrupt\n' % tagpath )
                        del tag_coll[tagpath]
                    self.tags_indexed -= 1

        #recount how many tags are loaded/indexed
        self.tally_tags()
        
        return self.tags_loaded
        

    def load_tags_and_run(self):
        self.print_to_console = True

        #make a new defs dict
        defs = {}

        #remove tags from the definitions which never have tag refs in them
        for tag_id in sorted(self.defs.keys()):
            
            #if the key exists in self.tag_ref_cache, copy the def
            if tag_id in self.tag_ref_cache:
                defs[tag_id] = self.defs[tag_id]

        #replace self.defs with the new defs and erase
        #self.tags and replace it with a fresh one
        self.defs = defs
        self.tags = {}
        self.reset_tags(defs.keys())
        
        input('This program will scan the tags directory and locate\n'
              'tags that reference other tags. A log will be created\n'+
              'in the tags directory and any tag references that\n'+
              'cannot be found in the tags directory will be logged.\n\n'+
              'This program will periodically print the path of the\n'+
              'tag it is currently indexing/loading/scanning relative\n'+
              'to the tags directory as a sort of progress update.\n\n'+
              
              'Press Enter to begin scanning in:\n'+
              '    %s\n\n' % self.tagsdir)
        
        #Stream the data from the tags to class
        #constructs so the program can work with them
        print('Indexing...')
        self.mode = 1
        if self.index_tags():
            print('\nLoading %s tags...' % self.tags_indexed)
            self.mode = 2
            self.load_tags()

            print('\nScanning %s tags...' % self.tags_loaded)
            self.mode = 3
            debuglog = self.scan_tagsdir()
            
            print('\nWriting logfile...')
            self.mode = 100
            #save the debug log to a file
            self.make_log_file(debuglog)
        else:
            #if something went wrong earlier this will notify the user
            self.mode = 100
            input('tags directory is either empty, doesnt '+
                  'exist, or cannot be accessed')
            raise SystemExit()
        
        self.mode = 100
        input('-'*80 + '\nFinished scanning tags directory.\n'+
              'Check the tags directory for the log.\n' + '-'*80 +
              '\n\nPress enter to exit.')
        raise SystemExit()
        

    def scan_tagsdir(self, **kwargs):
        #this is the string to store the entire debug log
        logstr = ("Debug log for HEK Tag Scanner\n\n\n")
        
        '''loop through both chicago and extended chicago tag types'''
        for tag_id in sorted(self.tag_ref_cache.keys()):

            tag_ref_paths = self.tag_ref_cache[tag_id]
            if self.print_to_console:
                print(" "*4+ "Scanning '%s' tags..." % tag_id)

            for tagpath in sorted(self.tags[tag_id].keys()):
                tag = self.tags[tag_id][tagpath]
                self.current_tag = tagpath
                
                try:
                    missed = self.get_blocks_by_paths(tag_ref_paths,tag.tagdata,
                                                      self.get_tag_not_exist)

                    if len(missed):
                        logstr += "\n\n%s\n" % tagpath
                        block_name = None
                        
                        for block in missed:
                            if block.NAME != block_name:
                                logstr += ' '*4 + block.NAME + '\n'
                                block_name = block.NAME
                            try:
                                ext = '.'+block.Tag_Class.data_name
                            except Exception:
                                ext = ''
                            logstr += ' '*8 + block.CHILD + ext + '\n'
                            
                except Exception:
                    print("ERROR OCCURRED WHILE ATTEMPTING TO SCAN:\n" +
                          '    ' + tag.tagpath + '\n')
                    print(format_exc())
                    continue
                        
        
        return logstr