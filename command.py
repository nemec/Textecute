import subprocess as sp

# Each function in this script is a command that you can send.
# The function will be called by sending a text/email starting
# with the function name, followed by a space and any arguments.
# The function should process the arguments and return a string.
# The string will be sent back to the device that requested data.
# If no data needs to be sent back, return an empty string ('')

# Executes the supplied command on the host computer

def help(arg = ''):
    return "Prepend @ to disable lowercase"

def exe(arg = ''):
    if arg == '':
        return ''
    p = sp.Popen(arg, stdout = sp.PIPE, stderr = sp.PIPE, shell = True)
    out, err = p.communicate()
    if len(out) == 0:
        return err
    return out

# Shuts down the host computer in the specified number of seconds
def shutdown(arg = 'now'):
    try:
        int(arg)
    except ValueError:  # arg is not int
        try:
            if arg.find(':') > 0: # Possibly in hh:mm format
                int(arg.split(':')[0])+int(arg.split(':')[1])
            elif not arg == 'now': # Otherwise must be 'now'
                return ''
        except ValueError:
            return ''        
        
    p = sp.Popen('shutdown -P ' + arg, stdout = sp.PIPE, shell = True)
    return p.communicate()[0]


def google(arg = ''):
    # Requires simplejson module for AJAX search
    # from:http://pypi.python.org/pypi/simplejson
    # Example code found at: http://dcortesi.com/
    import urllib
    import simplejson
    import re
    import unicodedata
    if arg == '':
        return 'Error: No search string.'
    query = urllib.urlencode({'q' : arg})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
    search_results = urllib.urlopen(url)
    json = simplejson.loads(search_results.read())
    results = json['responseData']['results']
    try:
      ret = re.sub(r'<[^>]*?>', '', results[0]['content']) # Strips HTML formatting
    except:
      return "There was an error parsing data. Please try again."
    ret = re.sub(r'&[^ ]*?;', '', ret) # Strips HTML special characters (ie. &quot; )
    return unicodedata.normalize('NFKD', unicode(ret, "utf-8")).encode('ascii','ignore')
    #return unicodedata.normalize('NFKD', ret).encode('ascii','ignore')

#Inserts your specified text into a "memo" textfile
def memo(arg = ''):
    f = open("/home/dan/doc/memo" , "a")
    if arg != '':
        f.write(arg+"\n")
    f.close()
    return "Inserted into memo file."

def translate(arg = ''):
    from urllib2 import urlopen
    from urllib import urlencode
    import unicodedata

    # The google translate API can be found here: 
    # http://code.google.com/apis/ajaxlanguage/documentation/#Examples
    if arg == '' or arg.count(' ') < 2:
      return ''
    lang1=arg[0:2]
    lang2 = arg[3:5]
    langpair='%s|%s'%(lang1,lang2)
    text=arg[5:]
    base_url='http://ajax.googleapis.com/ajax/services/language/translate?'
    params=urlencode( (('v',1.0),
                       ('q',text),
                       ('langpair',langpair),) )
    url=base_url+params
    content=urlopen(url).read()
    start_idx=content.find('"translatedText":"')+18
    translation=content[start_idx:]
    end_idx=translation.find('"}, "')
    translation=translation[:end_idx]
    return unicodedata.normalize('NFKD', unicode(translation, "utf-8")).encode('ascii','ignore')

def wiki(arg = ''):
    if arg == '':
      return ''
    p = sp.Popen("dig +short txt \""+arg+".wp.dg.cx\"", stdout = sp.PIPE, stderr = sp.PIPE, shell = True)
    out, err = p.communicate()
    if len(out) == 0:
        return err
    return out

# Requires the program curl to be installed
def mail(arg = ''):
    if arg == '':
        return ''
    user, space, pas = arg.partition(" ")
    cmd ="curl -u "+user+":"+pas+" --silent \"https://mail.google.com/mail/feed/atom\" | tr -d '\n' | awk -F '<entry>' '{for (i=2; i<=NF; i++) {print $i}}' | sed -n \"s/<title>\\(.*\)<\\/title.*name>\\(.*\\)<\\/name>.*/\\2 - \\1/p\""
    p = sp.Popen(cmd, stdout = sp.PIPE, stderr = sp.PIPE, shell = True)
    out, err = p.communicate()
    if out == "":
      out="No mail."
    if len(out) == 0:
        return err
    return out





