import subprocess, re, random, os, sys, pymediainfo # , tensorflow as tf

# Build ffmpeg, ffplay and ffprobe from source
# or download at https://www.gyan.dev/ffmpeg/builds/
# (MT builds, Windows builds only)
# or down;pad at https://github.com/BtbN/FFmpeg-Builds/releases
# (MD builds, cross-platform)
# or download at https://ffmpeg.org//download.html
# or download at https://mega.nz/file/TAlnSJhC#u58yn-9baEduAXW2dDXLz8YAc_72DC8E0u9J1Wmr6WI
# (MT builds, Windows builds only)
# Only 'bin' folder content needed

# All tools are suggested to be placed to script folder

vidDuraDict = {}
xfadelist = []
xfadesused = []
fadeTypes = [ 'fadetoblack', 'crossfade', 'random', 'xfadedistance', 'xfadedissolve', 'xfaderadial', 'xfadecircleopen',
              'xfadecircleclose', 'xfadepixelize', 'xfadehlslice', 'xfadehrslice',
              'xfadevuslice', 'xfadevdslice', 'xfadehblur', 'xfadefadegrays', 'xfadefadewhite', 'xfaderectcrop',
              'xfadecirclecrop', 'xfaderectcrop', 'xfadehorzclose', 'xfadehorzopen',
              'xfadevertclose', 'xfadevertopen', 'xfadewipeleft', 'xfadewiperight',
              'xfadewipeup', 'xfadewipedown', 'xfadewipetl', 'xfadewipetr', 'xfadewipebl', 'xfadewipebr',
              'xfadesqueezeh', 'xfadesqueezev', 'xfadehlwind', 'xfadehrwind', 'xfadevuwind', 'xfadevdwind',
              'xfadeslideleft', 'xfadeslideright', 'xfadeslideup', 'xfadeslidedown',
              'xfadesmoothleft', 'xfadesmoothright', 'xfadesmoothup', 'xfadesmoothdown',
              'xfadecoverleft', 'xfadecoverright', 'xfadecoverup', 'xfadecoverdown',
              'xfaderevealleft', 'xfaderevealright', 'xfaderevealup', 'xfaderevealdown',
              'xfadediagtl', 'xfadediagtr', 'xfadediagbl', 'xfadediagbr', 'xfadezoomin', 'xfaderandom',
              'xfaderandomtotal' ]
imageFolder = 'C:\\yt-dlp\\skazi\\art'
audioFolder = 'C:\\yt-dlp\\skazi'
outFolder= 'C:\\yt-dlp\\skazi\\mp4'
vidPatternTemp = r'tempvid\d+'
imagePattern = r'\d+. art'
partVideoFileName = 'tempvid'
vidListFName = 'vidlist.txt'
imageListFName = 'imglist.txt'
audioListFName = 'audlist.txt'
mdfile = 'metadata.txt'
videoExt = '.mp4'
imageExt = '.png'
audioExt = '.mp3'
xfadeOffsetMulti = 4
imgsPerBatch = 5
gpuAccelAllowed = False # True
gpuMan = 'nvidia' # 'amd'
ffmpegfname = 'ffmpeg.exe'
ffprobefname = 'ffprobe.exe'
partVideoFName = outFolder + os.path.sep + 'tempvid'
tempVideoFName = outFolder + os.path.sep + 'tempmerged.mp4'
outVideoFName = outFolder + os.path.sep + 'outmerged.mp4'
outVideoFNameMD = outFolder + os.path.sep + 'outmergedMD.mp4'
outAudioFName = audioFolder + os.path.sep + 'outaudio.mp3'
chapDescFName = audioFolder + os.path.sep + 'chapdesc.txt'

metainfo = { 'metaauthors_perimeter': 'K-D Lab [Victor Krasnokutsky]',
             'metaadd_perimeter': { 'empire primary': 'Bell Strike',
                                    'empire psychosphere': 'Phobia',
                                    'exodus military': 'Construction',
                                    'exodus primary': 'Promised Land',
                                    'exodus psychosphere': 'Delusion',
                                    'harkbackhood primary': 'DNA',
                                    'harkbackhood covered':'Scourge',
                                    'alpha expedition': 'Destination' },
             'metaauthors_tekken 5': '',
             'metaadd_tekken 5': '',
             'metaauthors_fight club': 'The Dust Brothers',
             'metaadd_fight club': '',
             'metaauthors_doom 2016': 'Mick Gordon',
             'metaadd_doom 2016': '',
             'metaauthors_doom eternal': 'Mick Gordon',
             'metaadd_doom eternal': '',
             'metaauthors_warcraft 3': '',
             'metaadd_warcraft 3': '',
             'metaauthors_wh': 'Jeremy Soule',
             'metaadd_wh': '' }

# A python class definition for printing formatted text on terminal.
# Initialize TextFormatter object like this:
# >>> cprint = TextFormatter()
#
# Configure formatting style using .cfg method:
# >>> cprint.cfg('r', 'y', 'i')
# Argument 1: foreground(text) color
# Argument 2: background color
# Argument 3: text style
#
# Print formatted text using .out method:
# >>> cprint.out("Hello, world!")
#
# Reset to default settings using .reset method:
# >>> cprint.reset()

class TextFormatter:
    COLORCODE = {
        'k': 0,  # black
        'r': 1,  # red
        'g': 2,  # green
        'y': 3,  # yellow
        'b': 4,  # blue
        'm': 5,  # magenta
        'c': 6,  # cyan
        'w': 7   # white
    }
    FORMATCODE = {
        'b': 1,  # bold
        'f': 2,  # faint
        'i': 3,  # italic
        'u': 4,  # underline
        'x': 5,  # blinking
        'y': 6,  # fast blinking
        'r': 7,  # reverse
        'h': 8,  # hide
        's': 9,  # strikethrough
    }

    # constructor
    def __init__(self):
        self.reset()


    # function to reset properties
    def reset(self):
        # properties as dictionary
        self.prop = {'st': None, 'fg': None, 'bg': None}
        return self


    # function to configure properties
    def cfg(self, fg, bg=None, st=None):
        # reset and set all properties
        return self.reset().st(st).fg(fg).bg(bg)


    # set text style
    def st(self, st):
        if st in self.FORMATCODE.keys():
            self.prop['st'] = self.FORMATCODE[st]
        return self


    # set foreground color
    def fg(self, fg):
        if fg in self.COLORCODE.keys():
            self.prop['fg'] = 30 + self.COLORCODE[fg]
        return self


    # set background color
    def bg(self, bg):
        if bg in self.COLORCODE.keys():
            self.prop['bg'] = 40 + self.COLORCODE[bg]
        return self


    # formatting function
    def format(self, string):
        w = [self.prop['st'], self.prop['fg'], self.prop['bg']]
        w = [str(x) for x in w if x is not None]
        # return formatted string
        return '\x1b[%sm%s\x1b[0m' % (';'.join(w), string) if w else string


    # output formatted string
    def out(self, string):
        print(self.format(string))


def getos():
    if 'posix' == os.name:
        retstr = os.system("uname -a")
    else:
        retstr = sys.platform
    return retstr


def isAudio(filepath: str):
    if not os.path.exists(filepath):
        return False
    fileInfo = pymediainfo.MediaInfo.parse(filepath)
    for track in fileInfo.tracks:
        if 'Audio' == track.track_type:
            return True
    return  False


def isVideo(filepath: str):
    if not os.path.exists(filepath):
        return False
    fileInfo = pymediainfo.MediaInfo.parse(filepath)
    for track in fileInfo.tracks:
        if 'Video' == track.track_type:
            return True
    return  False


def isImage(filepath: str):
    if not os.path.exists(filepath):
        return False
    fileInfo = pymediainfo.MediaInfo.parse(filepath)
    for track in fileInfo.tracks:
        if 'Image' == track.track_type:
            return True
    return False


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def prepXFShortname(xfname: str):
    if len(xfname) == 0:
        return None
    tstr = ''
    out = ''
    xfnamerev = xfname[::-1]
    for c in xfnamerev:
        if c.isdigit():
            if len(out) < 2:
                out += c
            else:
                break
    out = out[::-1]
    out = '[s' + out + ']'
    return out


def prepXFadeList():
    global xfadelist
    global fadeTypes
    for fade in fadeTypes:
        if fade.startswith('xfade'):
            xfadelist.append(fade)


def pickXFade(tryUnique: bool = True):
    global xfadelist
    global xfadesused
    if tryUnique:
        xfdiff = list(set(xfadelist) - set(xfadesused))
        xfdlen = len(xfdiff)
        if xfdlen > 0:
            pxf = xfdiff[random.randint(0, xfdlen - 1)]
            xfadesused.append(pxf)
            return pxf
        else:
            return xfadelist[random.randint(0, len(xfadelist) - 1)][5:][5:]
    else:
        return xfadelist[random.randint(0, len(xfadelist) - 1)][5:][5:]


def getrealduration(duration: int):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if duration <= 0:
        return '00:00:00'
    if duration is None:
        return None
    realdura = ''
    days = 0
    hrs = 0
    mins = 0
    secs = 0
    dura = 0
    if duration <= 10:
        return '00:00:00'
    if duration > 1000:
        dura = duration / 1000
    else:
        dura = duration
    secs = int(dura % 60)
    mins = int((dura / 60) % 60)
    hrs = int(dura / 3600)
    if hrs > 0:
        days = int(dura / 86400)
    if days > 0:
        realdura = ('{:02}'.format(days) + '{:02}'.format(hrs) + ':' + '{:02}'.format(mins) + ':' +
                    '{:02}'.format(secs))
    else:
        realdura = '{:02}'.format(hrs) + ':' + '{:02}'.format(mins) + ':' + '{:02}'.format(secs)
    return realdura


def formTitle(argstr:str, removeNums: bool = True):
    global metainfo
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if len(argstr) == 0 or argstr is None:
        return ''
    argstrlow = argstr.strip().lower()
    keylist = []
    for key in metainfo:
        if not '_' in key:
            continue
        keylowspl = key.lower().split('_')[-1]
        if keylowspl in argstrlow:
            keylist.append(key)
    title = ''
    # title = argstr
    soundname = argstr.split('\\')[-1]
    if removeNums and '. ' in soundname:
        soundname = ''.join(soundname.split('. ')[1:]).strip()
    for key in keylist:
        if 'metaauthors' in key:
            if len(metainfo[key]) > 0 and not ' - ' in argstr:
                title += metainfo[key]
        if 'metaadd' in key:
            if len(metainfo[key]) > 0 and type(metainfo[key]) is dict:
                for skey in metainfo[key]:
                    skeylow = skey.lower()
                    if skeylow in argstrlow:
                        argstrpr = argstr.split('c')[0][::-1].split('\\')[0][::-1]
                        soundname = (metainfo[key][skey]) + ' [' + argstr + ']'
                        if len(title) > 0:
                            title += ' - ' + soundname
                        else:
                            title = soundname
                        return title
                    # else:
                        # soundname = argstr
            # else:
                # soundname = argstr
    if len(title) > 0:
        if '.' in soundname:
            title += ' - ' + soundname.replace(soundname.split('.')[-1], '')[:-1]
        else:
            title += ' - ' + soundname
    else:
        if len(soundname) > 0:
            # snext = soundname.split('.')[-1]
            if '.' in soundname:
                title = soundname.replace(soundname.split('.')[-1], '')[:-1]
    return title


def videoRemoveAudio(videoPath: str, targetPath: str):
    global ffmpegfname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if not os.path.exists(videoPath):
        return False
    if len(targetPath) == 0:
        return False
    if not os.path.exists(os.path.dirname(targetPath)):
        return False
    arglist = [ ffmpegfname, '-y' ]
    arglist.append('-i')
    arglist.append(videoPath)
    arglist.append('-c')
    arglist.append('copy')
    arglist.append('-an')
    arglist.append(targetPath)
    subprocess.run(arglist)
    return os.path.exists(targetPath) and isVideo(targetPath)


def calcXFadeOffset(duration: float, prevXFadeOffset: float, xfadeDuaration: float):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if duration < 0:
        colorprint.out('calcXFadeOffset ERROR - NEGATIVE DURATION VALUE')
        return None
    if prevXFadeOffset < 0:
        colorprint.out('calcXFadeOffset ERROR - NEGATIVE PREVXFADEOFFSET VALUE')
        return None
    if xfadeDuaration < 0:
        colorprint.out('calcXFadeOffset ERROR - NEGATIVE XFADEDURATION VALUE')
        return None
    return duration + prevXFadeOffset - xfadeDuaration


def videoFromImages(targetPath: str, imgList: list, imageDuration: float, fadeDuration: int = 1,
                    keepAudio:bool = True, allowOverwrite:bool = True, fadeType: str = 'crossfade'):
    global ffmpegfname
    global fadeTypes
    global gpuAccelAllowed
    global gpuMan
    global xfadeOffsetMulti
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if fadeType is None or len(fadeType) == 0:
        return False
    fadeTypelow = fadeType.strip().lower()
    if not fadeTypelow in fadeTypes:
        return False
    listlen = len(imgList)
    if listlen == 0:
        return False
    if not isinstance(imageDuration, float) or not isinstance(fadeDuration, int):
        return False
    if imageDuration <= 0 or fadeDuration <= 0:
        return False
    if imageDuration< fadeDuration:
        return False
    if not isinstance(targetPath, str):
        return False
    if len(targetPath) == 0:
        return False
    if os.path.exists(targetPath):
        if allowOverwrite:
            os.remove(targetPath)
        else:
            return False
    mdur = 0
    ctime = 0
    isPrevVid = False
    if gpuAccelAllowed:
        if 'nvidia' == gpuMan:
            # '-hwaccel_output_format', 'cuda'
            arglist = [ ffmpegfname, '-hwaccel', 'cuda', '-y' ]
        elif 'amd' == gpuMan:
            arglist = [ ffmpegfname, '-y' ]
        else:
            return False
    else:
        arglist = [ ffmpegfname, '-y' ]
    if listlen > 1:
        for img in imgList:
            isimg = isImage(img)
            isvid = isVideo(img)
            if isimg and not isvid:
                arglist.append('-loop')
                arglist.append('1')
                arglist.append('-t')
                if isPrevVid:
                    if imageDuration > float(mdur):
                        arglist.append(str(imageDuration - float(mdur)))
                    else:
                        arglist.append(str(imageDuration))
                else:
                    arglist.append(str(imageDuration))
                arglist.append('-i')
                arglist.append(img)
                isPrevVid = False
            elif isvid:
                mdur = getmediaduration(img)
                vidDuraDict[img] = mdur
                arglist.append('-t')
                arglist.append(mdur)
                arglist.append('-i')
                arglist.append(img)
                isPrevVid = True
        arglist.append('-filter_complex')
        if 'fadetoblack' == fadeTypelow:
            trparamstr = '[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=in:st=0:d=' + \
                         str(fadeDuration) + ',fade=t=out:st=' + str(imageDuration - fadeDuration) + ':d=' + str(fadeDuration) + '[v0];'
            trparamfinstr = '[v0]'
            idx = 1
            for i in range(idx, listlen):
                trparamstr += '[' + str(i) + ':v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=in:st=0:d=' +\
                              str(fadeDuration) + ',fade=t=out:st=' + str(imageDuration - fadeDuration) + ':d=' + str(fadeDuration) + '[v' + str(i) + '];'
                trparamfinstr += '[v' + str(i) + ']'
            # trparamfinstr += 'concat=n=' + str(listlen) + ':v=1:a=0,format=yuv420p[v]'
            trparamstr += trparamfinstr
            arglist.append(trparamstr)
            arglist.append('-map')
            arglist.append('[v]')
            if keepAudio:
                arglist.append('-map')
                arglist.append(str(listlen) + ':a')
        elif 'crossfade' == fadeTypelow:
            maxidx = listlen - 3
            idx = 1
            osstr = ''
            trparamstr = ''
            trparamfinstr = '[0][f0]overlay[bg1];'
            for i in range(idx, listlen):
                addtime = i * (imageDuration - fadeDuration)
                midx = i - idx
                trparamstr += '[' + str(i) + ']scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuva444p,fade=d=' + str(fadeDuration) +\
                             ':t=in:alpha=1,setpts=PTS-STARTPTS+' + str(addtime) + '/TB[f' + str(midx) + '];'
                if i < listlen - 1:
                    if i < listlen - 2:
                        osstr += '[bg' + str(i) + '][f' +  str(i) + ']overlay[bg' + str(i + 1) + '];'
                    else:
                        osstr += '[bg' + str(i) + '][f' + str(i) + ']overlay,format=yuv420p[v]'
            trparamfinstr += osstr
            trparamstr += trparamfinstr
            arglist.append(trparamstr)
            arglist.append('-map')
            arglist.append('[v]')
            if keepAudio:
                arglist.append('-map')
                arglist.append(str(listlen) + ':a')
        else:
            if fadeTypelow.startswith('xfade'):
                if not fadeTypelow in fadeTypes:
                    return False
                prevtran = '[s0][s1]'
                pickedxf = ''
                xfstr = fadeTypelow[5:]
                if xfstr.startswith('random'):
                    pickedxf = xfadelist[random.randint(0, len(xfadelist) - 1)][5:]
                else:
                    pickedxf = xfstr
                xfoffs = 0
                prevoffs = 0
                # trparamstr = '[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[s0]'
                trparamstr = ''
                trparamxfstr = ''
                upid = listlen - 1
                for ind in range(0, listlen):
                    xfoffs = calcXFadeOffset(imageDuration, prevoffs, fadeDuration)
                    if 'randomtotal' == xfstr:
                        pickedxf = pickXFade()
                    # '[0:v]scale=1280:720:force_original_aspect_ratio=decrease:eval=frame,pad=1280:720:-1:-1:color=black[v0]; [1:v]scale=1280:720:force_original_aspect_ratio=decrease:eval=frame,pad=1280:720:-1:-1:color=black[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]'
                    trparamstr += '[' + str(ind) +  ':v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[s' +\
                                  str(ind) + '];'
                    if ind < upid:
                        ri = ind + 1
                        timeoffset = ri * (imageDuration - fadeDuration)
                        if ind < upid -1:
                            sname = prepXFShortname(prevtran)
                            trparamxfstr += prevtran + 'xfade=transition=' + pickedxf + ':duration=' + str(xfoffs) +\
                                            ':offset=' +str(round(timeoffset, 3)) + sname + ';'
                            prevtran = sname + '[s' + str(ind + 2) + ']'
                        else:
                            trparamxfstr += prevtran + 'xfade=transition=' + pickedxf + ':duration=' +\
                                            str(round(xfoffs, 3)) + ':offset=' + str(timeoffset) + ',format=yuv420p;'
                        prevoffs = xfoffs
                # trparamstr +='[1:v:0]setsar=sar=40/33,[0][1][2][3][1v0sar]concat=n=5:v=1:a=0,'
                trparamstr += trparamxfstr
                arglist.append(trparamstr)
            else:
                return False
    else:
        if 'fadetoblack' == fadeTypelow:
            arglist.append('-loop')
            arglist.append('1')
            arglist.append('-t')
            arglist.append(str(imageDuration))
            arglist.append('-i')
            arglist.append(imgList[0])
            trparamstr = '[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=in:st=0:d=' + \
                         str(round(fadeDuration, 3)) + ',fade=t=out:st=' + str(round(imageDuration - fadeDuration, 3)) + ':d=' + str(fadeDuration) + '[v0];'
            trparamfinstr = '[v0]format=yuv420p[v]'
            trparamstr += trparamfinstr
            arglist.append(trparamstr)
            arglist.append('-map')
            arglist.append('[v]')
        elif 'crossfade' == fadeTypelow:
            return False
        else:
            return False
    if gpuAccelAllowed:
        if 'nvidia' == gpuMan:
            # hevc_amf
            arglist.append('-c:v')
            arglist.append('h264_nvenc')
            arglist.append('-pix_fmt')
            arglist.append('yuv420p')
        elif 'amd' == gpuMan:
            # hevc_vaapi
            arglist.append('-vcodec')
            osinuse = getos()
            if 'win32' == osinuse:
                arglist.append('h264_amf')
            else:
                arglist.append('h264_vaapi')
    arglist.append(targetPath)
    ###
    subprocess.run(arglist)
    if os.path.exists(targetPath):
        if isVideo(targetPath):
            return True
        else:
            return False
    else:
        return False


def videoList2TextFile(filename: str, datalist: list):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if os.path.exists(filename):
        colorprint.out('REQUESTED OBJECT (' + filename + ') IS ALREADY PRESENT IN THE SYSTEM')
        return False
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('ffconcat version 1.0\n\n')
        for line in datalist:
            flieln = 'file ' + line.replace('\\', '\\\\').replace('\'', '\\\'').replace(' ', '\\ ') + '\n'
            f.write(flieln)
        f.close()
    return True


def imageList2TextFile(filename: str, avgduration:int, datalist: list):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if avgduration < 0:
        colorprint.out('INCORRECT IMAGE DURATION VALUE SPECIFIED')
        return False
    if os.path.exists(filename):
        colorprint.out('REQUESTED OBJECT (' + filename + ') IS ALREADY PRESENT IN THE SYSTEM')
        return False
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('ffconcat version 1.0\n\n')
        for line in datalist:
            flieln = 'file ' + line.replace('\\', '\\\\').replace('\'', '\\\'').replace(' ', '\\ ') + '\n'
            f.write(flieln)
            f.write('duration ' + str(avgduration) + '\n')
        f.close()
    return True


def audioList2textfile(filename: str, datalist: list):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if os.path.exists(filename):
        colorprint.out('REQUESTED OBJECT (' + filename + ') IS ALREADY PRESENT IN THE SYSTEM')
        return False
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('ffconcat version 1.0\n\n')
        for line in datalist:
            # fline = 'file "' + line.replace('\\', '\\\\').replace(' ', '\\ ') + '"\n'
            flieln = 'file ' + line.replace('\\', '\\\\').replace('\'', '\\\'').replace(' ', '\\ ') + '\n'
            f.write(flieln)
        f.close()
    return True


def getmediaduration(mp3filename: str):
    global ffprobefname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if mp3filename == '':
        colorprint.out('PATH TO MP3 FILE IS EMPTY')
        return None
    if not os.path.exists(mp3filename):
        colorprint.out('PATH TO MP3 FILE DOES NOT EXIST')
        return None
    subarglist = [ ffprobefname, '-show_entries', 'format=duration','-i',mp3filename ]
    popen  = subprocess.Popen(subarglist, stdout = subprocess.PIPE)
    popen.wait()
    output = str(popen.stdout.read())
    if len(output) > 0 and '\\r\\n' in output:
        return output.split('\\r\\n')[1][9:]
    else:
        return None


def listFilesInFolderByNameRegexExt(folderpath: str, seeknameregex: str = imagePattern,
                                    fileext: str = imageExt,
                                    fullfilenames: bool = True):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if len(folderpath) == 0:
        colorprint.out('PATH TO FOLDER IS EMPTY')
        return None
    if not os.path.exists(folderpath):
        colorprint.out('PATH TO FOLDER DOES NOT EXIST')
        return None
    filenames = []
    for root, dirs, files in os.walk(folderpath):
        for filename in files:
            foundname = os.path.splitext(filename)[0]
            foundext = os.path.splitext(filename)[1]
            if foundext == fileext and re.match(seeknameregex, foundname):
                if fullfilenames:
                    filenames.append(os.path.join(root, filename))
                else:
                    filenames.append(filename)
    return filenames


def listFilesInFolderByNameRegex(folderpath: str, seeknameregex: str = imagePattern,
                                    fullfilenames: bool = True):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if folderpath == '':
        colorprint.out('PATH TO FOLDER IS EMPTY')
        return None
    if not os.path.exists(folderpath):
        colorprint.out('PATH TO FOLDER DOES NOT EXIST')
        return None
    filenames = []
    for root, dirs, files in os.walk(folderpath):
        for filename in files:
            foundname = os.path.splitext(filename)[0]
            foundext = os.path.splitext(filename)[1]
            if re.match(seeknameregex, foundname):
                if fullfilenames:
                    filenames.append(os.path.join(root, filename))
                else:
                    filenames.append(filename)
    return filenames


def listFilesInFolderByExt(folderpath: str, fileext: str = audioExt,
                           fullfilenames: bool = True):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if folderpath == '':
        colorprint.out('PATH TO FOLDER IS EMPTY')
        return None
    if not os.path.exists(folderpath):
        colorprint.out('PATH TO FOLDER DOES NOT EXIST')
        return None
    filenames = []
    for root, dirs, files in os.walk(folderpath):
        for filename in files:
            if os.path.splitext(filename)[1] == fileext:
                if fullfilenames:
                    filenames.append(os.path.join(root, filename))
                else:
                    filenames.append(filename)
    return filenames


######### SCRIPT #########
if __name__ == "__main__":
    print(isVideo('C:\\Users\\admin\\Downloads\\test\\KR-HELL.mp3'))
    colorprint = TextFormatter()
    colorprint.cfg('r', 'k', 'b')
    sctiptdir = get_script_path()
    if len(ffmpegfname) > 0:
        ffmpegfname =sctiptdir + os.path.sep + ffmpegfname
    if len(ffprobefname) > 0:
        ffprobefname = sctiptdir + os.path.sep + ffprobefname
    if len(vidListFName) > 0:
        vidListFName = sctiptdir + os.path.sep + vidListFName
    if len(imageListFName) > 0:
        imageListFName = sctiptdir + os.path.sep + imageListFName
    if len(audioListFName) > 0:
        audioListFName = sctiptdir + os.path.sep + audioListFName
    if len(mdfile) > 0:
        mdfile = sctiptdir + os.path.sep + mdfile
    if None == imageFolder or not os.path.exists(imageFolder):
        if len(sys.argv) > 1:
            if os.path.exists(sys.argv[1]):
                imageFolder = sys.argv[1]
            else:
                colorprint.out('IMAGE FOLDER NOT SET OR INCORRECT')
                systemExitCode = 1
                sys.exit(systemExitCode)
        else:
            colorprint.out('IMAGE FOLDER NOT SET OR INCORRECT')
            systemExitCode = 2
            sys.exit(systemExitCode)
    if None == audioFolder or not os.path.exists(audioFolder):
        if len(sys.argv) > 2:
            if os.path.exists(sys.argv[2]):
                audioFolder = sys.argv[2]
            else:
                colorprint.out('AUDIO FOLDER NOT SET OR INCORRECT')
                systemExitCode = 3
                sys.exit(systemExitCode)
        else:
            colorprint.out('AUDIO FOLDER NOT SET OR INCORRECT')
            systemExitCode = 4
            sys.exit(systemExitCode)
    if None == outFolder or not os.path.exists(outFolder):
        if len(sys.argv) > 3:
            if os.path.exists(sys.argv[3]):
                outFolder = sys.argv[3]
            else:
                colorprint.out('OUTPUT FOLDER NOT SET OR INCORRECT')
                systemExitCode = 5
                sys.exit(systemExitCode)
        else:
            colorprint.out('OUTPUT FOLDER NOT SET OR INCORRECT')
            systemExitCode = 6
            sys.exit(systemExitCode)
    if None == imagePattern or len(imagePattern) == 0:
        if len(sys.argv) > 4:
            if len(sys.argv[4]) <= 8:
                imagePattern = sys.argv[4]
            else:
                colorprint.out('IMAGE PATTERN NOT SET OR INCORRECT')
                systemExitCode = 7
                sys.exit(systemExitCode)
        else:
            colorprint.out('IMAGE PATTERN NOT SET OR INCORRECT')
            systemExitCode = 8
            sys.exit(systemExitCode)
    if None == imageExt or len(imageExt) == 0:
        if len(sys.argv) > 5:
            if len(sys.argv[5]) <= 4:
                imageExt = sys.argv[5]
            else:
                colorprint.out('IMAGE EXTENSION NOT SET OR INCORRECT')
                systemExitCode = 9
                sys.exit(systemExitCode)
        else:
            colorprint.out('IMAGE EXTENSION NOT SET OR INCORRECT')
            systemExitCode = 10
            sys.exit(systemExitCode)
    if None == audioExt or len(audioExt) == 0:
        if len(sys.argv) > 6:
            if len(sys.argv[6]) <= 4:
                audioExt = sys.argv[6]
            else:
                colorprint.out('AUDIO EXTENSION NOT SET OR INCORRECT')
                systemExitCode = 11
                sys.exit(systemExitCode)
        else:
            colorprint.out('AUDIO EXTENSION NOT SET OR INCORRECT')
            systemExitCode = 12
            sys.exit(systemExitCode)
    mp3files = listFilesInFolderByExt(audioFolder)
    if not mp3files or len(mp3files) ==0:
        colorprint.out('COULD NOT GET ANY AUDIO FILES')
        systemExitCode = 13
        sys.exit(systemExitCode)
    if not audioList2textfile(audioListFName, mp3files):
        colorprint.out('COULD NOT CREATE AUDIO FILE LIST')
        systemExitCode = 14
        sys.exit(systemExitCode)
    prepXFadeList()
    # images = listFilesInFolderByNameRegexExt(imageFolder)
    images = listFilesInFolderByNameRegex(imageFolder)
    imglen = len(images)
    if not images or imglen == 0:
        colorprint.out('COULD NOT GET ANY IMAGE FILES')
        systemExitCode = 13
        sys.exit(systemExitCode)
    # create metadata
    stdur = 0
    totalLen = 0
    mdrecs = [ ';FFMETADATA1' ]
    chapdesclist = [ 'Tracklist:' ]
    for rec in mp3files:
        mdrecs.append('[CHAPTER]')
        mdrecs.append('TIMEBASE=1/1000')
        mdrecs.append('START=' + str(stdur + 1))
        mp3dur = getmediaduration(rec)
        if mp3dur is None:
            colorprint.out('COULD NOT GET MEDIA FILE (' + rec + ') DURATION')
            systemExitCode = 15
            sys.exit(systemExitCode)
        mp3dur = round(float(mp3dur)) * 1000
        mdrecs.append('END=' + str(stdur + mp3dur))
        title = formTitle(rec)
        mdrecs.append('title=' + title)
        chapdesclist.append(str(getrealduration(stdur)) + ' ' + title)
        stdur += mp3dur
    with open(mdfile, 'w', encoding='utf-8') as f:
        for rec in mdrecs:
            f.write(rec + '\n')
        f.close()
    with open(chapDescFName,'w', encoding='utf-8') as f:
        for rec in chapdesclist:
            f.write(rec + '\n')
        f.close()
    # prepare audio track
    arglist = [ ffmpegfname,
                '-y',
                '-safe',
                '0',
                '-f',
                'concat',
                '-i',
                audioListFName,
                '-codec',
                'copy',
                outAudioFName ]
    subprocess.run(arglist)
    if not os.path.exists(outAudioFName):
        colorprint.out('COULD NOT PREPARE AUDIO TRACK')
        systemExitCode = 15
        sys.exit(systemExitCode)
    # prepare soundless video
    pidur = float(float(stdur / 1000) / imglen)
    if imglen > imgsPerBatch:
        iidx = 0
        idxch = 0
        idxdiff = 0
        cnameidx = 0
        eidx = 0
        while True:
            idxdiff = imglen - eidx
            if idxdiff > imgsPerBatch:
                idxch = imgsPerBatch
            elif imgsPerBatch > idxdiff > 0:
                idxch = idxdiff
            elif idxdiff <= 0:
                break
            eidx = iidx + idxch
            cname = partVideoFName + str(cnameidx) + videoExt
            imgList = images[ iidx : eidx ]
            if not videoFromImages(targetPath=cname, imgList=imgList, imageDuration=pidur,
                                   fadeType='xfadepixelize'):
                colorprint.out('COULD NOT CREATE SOUNDLESS VIDEO CLIP')
                systemExitCode = 16
                sys.exit(systemExitCode)
            iidx = eidx
            cnameidx += 1
        shortvids = listFilesInFolderByNameRegexExt(outFolder, vidPatternTemp, videoExt, True)
        if len(shortvids) == 0:
            colorprint.out('COULD NOT GET TEMPORARY VIDEOS')
            systemExitCode = 16
            sys.exit(systemExitCode)
        if not videoList2TextFile(vidListFName, shortvids):
            colorprint.out('COULD NOT CREATE VIDEO list')
            systemExitCode = 16
            sys.exit(systemExitCode)
        # merge temporary videos
        arglist = [ ffmpegfname,
                    '-safe',
                    '0',
                    '-f',
                    'concat',
                    '-i',
                    vidListFName,
                    '-codec',
                    'copy',
                    # '-t',
                    # '00:15:45',
                    tempVideoFName ]
        subprocess.run(arglist)
        for vid in shortvids:
            os.remove(vid)
    else:
        if not videoFromImages(tempVideoFName, images, pidur):
            colorprint.out('COULD NOT CREATE SOUNDLESS VIDEO')
            systemExitCode = 16
            sys.exit(systemExitCode)
    # add audio to video
    arglist = [ ffmpegfname,
                '-y',
                '-i',
                tempVideoFName,
                '-i',
                outAudioFName,
                '-codec',
                'copy',
                '-map',
                '0:v:0',
                '-map',
                '1:a:0',
                outVideoFName ]
    subprocess.run(arglist)
    if not os.path.exists(outAudioFName):
        colorprint.out('COULD NOT CREATE RESULT VIDEO')
        systemExitCode = 17
        sys.exit(systemExitCode)
    # add metadata to video
    arglist = [ ffmpegfname,
                '-y',
                '-i',
                outVideoFName,
                '-i',
                mdfile,
                '-map_metadata',
                '1',
                '-codec',
                'copy',
                outVideoFNameMD ]
    subprocess.run(arglist)
    if not os.path.exists(outAudioFName):
        colorprint.out('COULD NOT CREATE VIDEO FILE WITH METADATA')
        systemExitCode = 18
        sys.exit(systemExitCode)
    if os.path.exists(vidListFName):
        os.remove(vidListFName)
    if os.path.exists(imageListFName):
        os.remove(imageListFName)
    if os.path.exists(audioListFName):
        os.remove(audioListFName)
    if os.path.exists(tempVideoFName):
        os.remove(tempVideoFName)
    if os.path.exists(outAudioFName):
        os.remove(outAudioFName)
    if os.path.exists(mdfile):
        os.remove(mdfile)
    print('DONE.')