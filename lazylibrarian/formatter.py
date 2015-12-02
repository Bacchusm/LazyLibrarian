import datetime
import re
import lazylibrarian


def now():
    dtnow = datetime.datetime.now()
    return dtnow.strftime("%Y-%m-%d %H:%M:%S")


def today():
    dttoday = datetime.date.today()
    yyyymmdd = datetime.date.isoformat(dttoday)
    return yyyymmdd


def age(histdate):
    nowdate = datetime.date.today()
    m1, d1, y1 = (int(x) for x in nowdate.split('-'))
    m2, d2, y2 = (int(x) for x in histdate.split('-'))
    date1 = datetime.date(y1, m1, d1)
    date2 = datetime.date(y2, m2, d2)
    dtage = date1 - date2
    return dtage.days


def nzbdate2format(nzbdate):
    mmname = nzbdate.split()[2].zfill(2)
    day = nzbdate.split()[1]
    # nzbdates are mostly english short month names, but not always
    # month = str(strptime(mmname, '%b').tm_mon).zfill(2)
    month = month2num(mmname)
    if month == "Invalid":
        month = "01"  # hopefully won't hit this, but return a default value rather than error
    year = nzbdate.split()[3]
    return year + '-' + month + '-' + day


def month2num(month):
# return month number given month name (long or short) in requested locales
# or season name (only in English currently)

    month = month.lower()
    for f in range(1, 13):
        if month in lazylibrarian.MONTHNAMES[f]:
            return str(f).zfill(2)

    if month == "winter":
        return "01"
    elif month == "spring":
        return "04"
    elif month == "summer":
        return "07"
    elif month == "fall":
        return "10"
    elif month == "autumn":
        return "10"
    else:
        return "Invalid"


def datecompare(nzbdate, control_date):
    y1 = int(nzbdate.split('-')[0])
    m1 = int(nzbdate.split('-')[1])
    d1 = int(nzbdate.split('-')[2])
    y2 = int(control_date.split('-')[0])
    m2 = int(control_date.split('-')[1])
    d2 = int(control_date.split('-')[2])
    date1 = datetime.date(y1, m1, d1)
    date2 = datetime.date(y2, m2, d2)
    dtage = date1 - date2
    return dtage.days


def checked(variable):
    if variable:
        return 'Checked'
    else:
        return ''


def is_valid_isbn(isbn):
    isbn = re.sub('[- ]', '', isbn)
    if len(isbn) == 13:
        if isbn.isdigit():
            return 1
        elif len(isbn) == 10:
            if isbn[:9].isdigit():
                return 1
            else:
                if isbn[9] in ["Xx"] and isbn[:8].isdigit():
                    return 1
    return 0

def is_valid_booktype(filename):
    booktype_list = formatter.getlist(lazylibrarian.EBOOK_TYPE)
    if '.' in filename:
        words = filename.split('.')
        extn = words[len(words) - 1]
        if extn in booktype_list:
            return True
    return False 

def getList(st):
    # split a string into a list
    my_splitter = shlex.shlex(st, posix=True)
    my_splitter.whitespace += ','
    my_splitter.whitespace_split = True
    return list(my_splitter)


def latinToAscii(unicrap):
    """
    From couch potato
    """
    xlate = {0xc0: 'A', 0xc1: 'A', 0xc2: 'A', 0xc3: 'A', 0xc4: 'A', 0xc5: 'A',
             0xc6: 'Ae', 0xc7: 'C',
             0xc8: 'E', 0xc9: 'E', 0xca: 'E', 0xcb: 'E', 0x86: 'e',
             0xcc: 'I', 0xcd: 'I', 0xce: 'I', 0xcf: 'I',
             0xd0: 'Th', 0xd1: 'N',
             0xd2: 'O', 0xd3: 'O', 0xd4: 'O', 0xd5: 'O', 0xd6: 'O', 0xd8: 'O',
             0xd9: 'U', 0xda: 'U', 0xdb: 'U', 0xdc: 'U',
             0xdd: 'Y', 0xde: 'th', 0xdf: 'ss',
             0xe0: 'a', 0xe1: 'a', 0xe2: 'a', 0xe3: 'a', 0xe4: 'a', 0xe5: 'a',
             0xe6: 'ae', 0xe7: 'c',
             0xe8: 'e', 0xe9: 'e', 0xea: 'e', 0xeb: 'e', 0x0259: 'e',
             0xec: 'i', 0xed: 'i', 0xee: 'i', 0xef: 'i',
             0xf0: 'th', 0xf1: 'n',
             0xf2: 'o', 0xf3: 'o', 0xf4: 'o', 0xf5: 'o', 0xf6: 'o', 0xf8: 'o',
             0xf9: 'u', 0xfa: 'u', 0xfb: 'u', 0xfc: 'u',
             0xfd: 'y', 0xfe: 'th', 0xff: 'y',
             0xa1: '!', 0xa2: '{cent}', 0xa3: '{pound}', 0xa4: '{currency}',
             0xa5: '{yen}', 0xa6: '|', 0xa7: '{section}', 0xa8: '{umlaut}',
             0xa9: '{C}', 0xaa: '{^a}', 0xab: '<<', 0xac: '{not}',
             0xad: '-', 0xae: '{R}', 0xaf: '_', 0xb0: '{degrees}',
             0xb1: '{+/-}', 0xb2: '{^2}', 0xb3: '{^3}', 0xb4: "'",
             0xb5: '{micro}', 0xb6: '{paragraph}', 0xb7: '*', 0xb8: '{cedilla}',
             0xb9: '{^1}', 0xba: '{^o}', 0xbb: '>>',
             0xbc: '{1/4}', 0xbd: '{1/2}', 0xbe: '{3/4}', 0xbf: '?',
             0xd7: '*', 0xf7: '/'}

    r = ''
    for i in unicrap:
        if ord(i) in xlate:
            r += xlate[ord(i)]
        elif ord(i) >= 0x80:
            pass
        else:
            r += str(i)
    return r


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text
