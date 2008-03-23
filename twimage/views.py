# Create your views here.
import cStringIO
import os
import time
import traceback
import twitter
import urllib2

import Image
import ImageFont
import ImageDraw

from copy import copy

from django.http import Http404
from django.views.static import serve

from app.settings import MEDIA_ROOT

def _mksect(txt, font, max_width):
    char_lens = map(lambda x: font.getsize(x)[0], [i for i in txt]) 
    _sections = []
    sec_start = 0
    cur_sect_char_cnt = 0
    last_space = -1
    for i in range(len(txt)):
        c = txt[i]
        w = char_lens[i]
        if c == ' ':
            last_space = i

        cur_section = sum(char_lens[sec_start:i+1])
        if cur_section > max_width:
            if last_space > sec_start:
                sec_end = last_space+1
            else:
                sec_end = i+1
            _sections.append(sec_end)
            sec_start = sec_end

    _sections.append(len(txt)+1)
    return _sections

def _checkuser(username):
    valid_users = ['tristanking']
    return username in valid_users

def twittertoimage(request, username):

    if not _checkuser(username):
        raise Http404
    
    try:
        status = twitter.Api().GetUserTimeline(username)[0]
    except:
        raise Http404

    print status.created_at
    print status.created_at_in_seconds
    s_time = time.strftime('%I:%m%p %B %d', time.localtime(status.created_at_in_seconds)).replace('AM','am').replace('PM','pm')
    s_text = status.text

    # base image
    base = Image.open('%s/base.jpg' % MEDIA_ROOT)
    base_width, base_height = base.size   
    font_dir = MEDIA_ROOT + '/fonts/'
    font = ImageFont.truetype(font_dir + 'Verdana.ttf',12)
    txt = '%s %s %s' % (username, s_text, s_time)
    width = base_width-40
    _w,font_height = font.getsize(txt)
    sections = _mksect(txt, font, width)
    if len(sections) == 1:
        width = _w+40
    else:
        width = base_width
    height = 40+(font_height * len(sections))

    img = base.copy()

    #img = Image.new('RGBA', (w,h), '#ffffff')
    draw = ImageDraw.Draw(img)
    draw.rectangle([(10,10),(width-10,height-10)], '#ffffff')
    draw.fontmode = "0"

    chars_left = len(txt)
    sec_start = 0
    sec_end = sections[0]-1
    section = 0

    char_lens = map(lambda x: font.getsize(x)[0], [i for i in txt]) 
    username_color = '#0000ff'
    status_color = '#333333'
    date_color = '#BBBBBB'
    color = username_color
    for i in range(len(txt)):
        if i > sec_end:
            section += 1
            sec_start = i
            sec_end = sections[section]-1
        w = 20+(sum(char_lens[sec_start:i]))
        h = 20+(font_height * section)
        if i > len(username):
            color = status_color
        if i > len(username) + len(s_text) + 1:
            color = date_color
        draw.text((w,h), txt[i], font=font, fill=color)
    
    #draw.text((10,10), '%s %s %s' % (username, s_text, s_time), font=font, fill='#0000ff')

    try:
        if request.GET.get('extra', '').lower() == 'true':
            print 'processing extra!'
            profile_pic_uri = status.GetUser().GetProfileImageUrl()
            pro_pic = Image.open(cStringIO.StringIO(urllib2.urlopen(profile_pic_uri).read()))
            pro_pic = pro_pic.resize((23,23))
            draw.polygon([(width-60, height-10), (width-50, height), (width-40, height-10)], fill='#ffffff')
            draw.rectangle([(width-62, height+4), (width-38, height+27)], outline='#999999')
            img.paste(pro_pic, (width-61, height+5))
            tw_img = Image.open('%s/small_twitter.png' % MEDIA_ROOT)
            img.paste(tw_img, (14,height+10))
            height += 4 + 25 + 10
    except:
        traceback.print_exc()
        
    img = img.crop((0,0, width, height))
        
    out_file = '%s/%s-twitter.png' % (MEDIA_ROOT, username)
    img.save(out_file, 'PNG')

    return serve(request, out_file[1:], '/')
