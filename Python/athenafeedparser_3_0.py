##This program extract feed text and other information from RSS feeds.
##It inserts the extracted information into database table
##
##created by: Dipen Vadodaria
##created date: 19-mar-2013
##updated for enclosures on 09-may-2013
##updated to get content and image from the content on 14-may-2013

import feedparser
import re
import MySQLdb
import traceback
from BeautifulSoup import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys
from datetime import datetime
from datetime import timedelta
import DBuser

db = MySQLdb.connect(user=DBuser.user,db=DBuser.database,host=DBuser.host,passwd=DBuser.password,charset='utf8',use_unicode=True)
#db = MySQLdb.connect(user='root',passwd='root',db='athena',charset='utf8',use_unicode=True)

#prepare cursors for read and write
cursor_r = db.cursor()
cursor_w = db.cursor()
cursor_u = db.cursor()

#prepare SQL query to select feed_url
#print sys.argv[1]
frequency = sys.argv[1]
myread = [{"frequency" : frequency}]
sql_read="select feed_catalogue_id, feed_url, feed_etag, feed_last_modified, updated_time, upper(scrap_page) from salt_feed_catalogue where upper(is_active='YES') and frequency = %(frequency)s" 

try:
        #execute SQL commond
        cursor_r.executemany(sql_read,myread)
        #fetch all rows
        results = cursor_r.fetchall()
        for row in results:
                feed_id = row[0]
                feed_url = row[1]
                e_tag = row[2]
                last_modified = row[3]
                last_updated_time = row[4]
                scrap_flag = row[5]
                new_url = feed_url
                #print result
                print "id=%d,url=%s" % (feed_id, feed_url)
                last_updated_time =  last_updated_time.strftime('%Y-%m-%d %H:%M:%S')
                #feedparser.USER_AGENT = "Feeds/1.0 +http://iookii.com/"
                
                d=feedparser.parse(feed_url,etag=e_tag,modified=last_modified)
                
                ##following two lines were used for testing
                #d=feedparser.parse("http://feeds.abcnews.com/abcnews/topstories")
                #feed_id=227 
                
                if 'status' in d.feed:
                        if d.status == 304:
                                # skip if feed has not changed
                                continue

                        if d.status == 301 :
                                #url has permenently changed update database with the new one
                                new_url = d.href
                        else :
                                new_url = feed_url
                        
                #get the last modified and e-tags to see if the feed has been modified when accesssed next time
                        
                last_modified = d.feed.get('modified','no modified')
                e_tag = d.feed.get('etag','no etag')

                date_last_modified = None #use this if individual feeds do not have dates
                
                if 'modified_parsed' in d.feed and d.feed.modified_parsed <> None:
                        print 'modified time'
                        feed_year=d.feed.modified_parsed.tm_year
                        feed_month=d.feed.modified_parsed.tm_mon
                        feed_day=d.feed.modified_parsed.tm_mday
                        feed_hour=d.feed.modified_parsed.tm_hour
                        feed_minute=d.feed.modified_parsed.tm_min
                        feed_second=d.feed.modified_parsed.tm_sec

                        date_last_modified = str(feed_year)+"-"+str(feed_month).zfill(2)+"-"+ str(feed_day).zfill(2)+" "+ str(feed_hour).zfill(2)+":"+str(feed_minute).zfill(2)+":"+str(feed_second).zfill(2)

                updated_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                sql_update="update salt_feed_catalogue \
                                set feed_url = '%s', \
                                feed_etag= '%s', \
                                feed_last_modified = '%s',\
                                updated_time = '%s' \
                                where feed_catalogue_id = '%d'" %\
                                (new_url,e_tag,last_modified,updated_time, feed_id)
                try:
                        cursor_u.execute(sql_update)
                        db.commit()
                except Exception:
                        print sql_update
                        traceback.print_exc()
                        db.rollback()
                        break
                
                for e in d.entries :
                        try:
                                                       
                                image_url = None
                                
                                s=e.summary

                                soup=bs(s)

                                try:
                                        if 'published_parsed' in e:
                                                print 'in pub date'
                                                feed_date_published=e.published
                                                feed_year=e.published_parsed.tm_year
                                                feed_month=e.published_parsed.tm_mon
                                                feed_day=e.published_parsed.tm_mday
                                                feed_hour=e.published_parsed.tm_hour
                                                feed_minute=e.published_parsed.tm_min
                                                feed_second=e.published_parsed.tm_sec
                                        else:
                                                print 'in date'
                                                feed_date_published=e.date
                                                feed_year=e.date_parsed.tm_year
                                                feed_month=e.date_parsed.tm_mon
                                                feed_day=e.date_parsed.tm_mday
                                                feed_hour=e.date_parsed.tm_hour
                                                feed_minute=e.date_parsed.tm_min
                                                feed_second=e.date_parsed.tm_sec
                                        date_published = str(feed_year)+"-"+str(feed_month).zfill(2)+"-"+ str(feed_day).zfill(2)+" "+ str(feed_hour).zfill(2)+":"+str(feed_minute).zfill(2)+":"+str(feed_second).zfill(2)
                                        print date_published
                                        print last_updated_time
                                except Exception:
                                        print 'in date exception'
                                        if date_last_modified <> None:
                                                #if last modified is available in feeds at the top use it
                                                print "modified date in the header"
                                                date_published = date_last_modified
                                        else:
                                                if (feed_id >= 1436 and feed_id <= 1449):
                                                        print 'sandesh'
                                                        print feed_date_published
                                                        dt =  datetime.strptime(feed_date_published.replace(' ', '')[:-3],'%m/%d/%Y%I:%M:%S%p') #remove IST with replace
                                                        t=timedelta(minutes=330)
                                                        date_published = dt-t
                                                        date_published = date_published.strftime('%Y-%m-%d %H:%M:%S')
                                                        print date_published
                                                else:
                                                        if (feed_id >= 1123 and feed_id <= 1141):
                                                                print 'sakal'
                                                                print feed_date_published
                                                                dt =  datetime.strptime(feed_date_published[:-6],'%a,%d %b %Y %H:%M:%S') #remove +0550 with [-5]
                                                                t=timedelta(minutes=330)
                                                                date_published = dt-t
                                                                date_published = date_published.strftime('%Y-%m-%d %H:%M:%S')
                                                                print date_published                                
                                                        else:
                                                                date_published = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


                                
                                if (date_published > last_updated_time) and (date_published <= datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')):
                                        
                                        try:
                                                #get image embeded in description..ignore if width is given and is less than 90
                                                for image in soup.findAll("img"):
                                                        if image.has_key("width") :
                                                                if int(image["width"].replace("px","")) > 75:  #accept this image only if width is large enough
                                                                        image_url = image["src"]
                                                                        break;
                                                        else:
                                                                filename = image["src"].split("/")[-1]
                                                                file_ext=filename.split(".")[-1]
                                                                if (file_ext == "jpg" or file_ext == "jpeg") or (feed_id > 1176 and feed_id < 1239 and file_ext == "cms") or (feed_id > 1397 and feed_id < 1407 and file_ext == "cms"):
                                                                        image_url = image["src"]
                                                                        #print "got the image 1"
                                                                        break;
                                        except Exception:
                                                traceback.print_exc()
                                        
                                        feed_text=re.compile(r'<[^>]+>').sub('',s)
                                        #feed_text=re.compile(r"'").sub("\\'",feed_text)
                                        feed_text=re.compile(r"&nbsp;").sub(' ',feed_text) #ignore &nbsp
                                        feed_text=bs(feed_text,convertEntities=bs.HTML_ENTITIES)
                                        #feed_text=feed_text.encode('utf-8','ignore')

                                        feed_title=re.compile(r'<[^>]+>').sub('',e.title)
                                        #feed_title=re.compile(r"'").sub("\\'",feed_title)
                                        feed_title=re.compile(r"&nbsp;").sub(' ',feed_title) #ignore &nbsp
                                        feed_title=bs(feed_title,convertEntities=bs.HTML_ENTITIES)
                                        #feed_title=feed_title.encode('utf-8','ignore')
                                        
                                        #feed_text_url=re.compile(r"'").sub("\\'",e.link)
                                        feed_text_url=e.link
                                        
                                        #if e.published.find("GMT") > -1:
        ##                                try:
        ##                                        feed_date_published=e.published
        ##                                        feed_year=e.published_parsed.tm_year
        ##                                        feed_month=e.published_parsed.tm_mon
        ##                                        feed_day=e.published_parsed.tm_mday
        ##                                        feed_hour=e.published_parsed.tm_hour
        ##                                        feed_minute=e.published_parsed.tm_min
        ##                                        feed_second=e.published_parsed.tm_sec
        ##                                        date_published = str(feed_year)+"-"+str(feed_month)+"-"+str(feed_day)+" "+str(feed_hour)+":"+str(feed_minute)+":"+str(feed_second)
        ##                                except Exception:
        ##                                        date_published = created_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

                                        feed_content=" "
                                        #image_url = None


                                        #if media content tag is specified get url as it most likely is an image
                                        if 'media_content' in e:
                                                for content in e.media_content:
                                                        if 'url' in content:
                                                                file_ext = content['url'].split(".")[-1]
                                                                if (file_ext == "jpg" or file_ext == "jpeg" or file_ext == "gif"):
                                                                        image_url = content['url']
                                                                        #print "got the image 2"
                                                                        break;
                                                      
                                        try:
                                                #if content is present get the content and image embedded in it
                                                if 'content' in e:
                                                        for c in e.content :
                                                                #print "in content"
                                                                try:
                                                                        #content=re.compile(r'<[^>]+>').sub('',c.value)
                                                                        #follwing one line commented on 08 sept 2013
                                                                        #content=re.compile(r"'").sub("\\'",c.value)
                                                                        #content = unicode(content,"utf-8")
                                                                        content=content.encode("utf-8","ignore")
                                                                        #content=c.value
                                                                        feed_content=feed_content+content
                                                                        #print c.value
                                                                except Exception:
                                                                        traceback.print_exc()
                                                        
                                                                #image_url = None
                                                                soup=bs(feed_content)
                                        
                                                                for image in soup.findAll("img"):
                                                                        if image.has_key("width") :
                                                                                if int(image["width"].replace("px","")) > 75:  #accept this image only if width is large enough
                                                                                        image_url = image["src"]
                                                                                        print "got the image 3"
                                                                                        #print image_url
                                                                                        break;
                                                                        else:
                                                                                image_url = image["src"]
                                                                                print "got the image 3a"
                                                                                break
                                        except Exception:
                                                traceback.print_exc()
                                                
                                        if image_url == None:
                                                #check the enclosure tag for image
                                                if 'enclosures' in e:
                                                        for encl in e.enclosures :
                                                                if encl.type == "image/jpeg" or encl.type == "image/jpg":
                                                                        image_url = encl.href
                                                                        print "image in enclosure"
                                                                        break

                                        if scrap_flag == "YES":
                                                if image_url == None:
                                                        soup = bs(urlopen(feed_text_url))
                                                        parsed = list(urlparse.urlparse(feed_text_url))
                                                        image_url=None

                                                        for ptag in soup.findAll("p"):
                                                        
                                                                try:
                                                                        #go thru all ptags to find an image and stop once found
                                                                        for image in ptag.findAll("img"):
                                                                                if image.has_key("width") :
                                                                                        #print image["width"]
                                                                                        if feed_id > 1035 and feed_id < 1057:
                                                                                                #for the hindu 
                                                                                                w_size=325
                                                                                        else:
                                                                                                w_size=150
                                                                                        if int(image["width"].replace("px","")) > w_size:
                                                                                                #print image
                                                                                                filename = image["src"].split("/")[-1]
                                                                                                file_ext=filename.split(".")[-1]
                                                                                                if (file_ext == "jpg" or file_ext == "jpeg" or file_ext == "gif") and filename.find("-rss") < 0 and filename.find("logo") < 0 and (feed_id < 1036 or feed_id > 1056 or image["src"].find("archive") < 0):
                                                                                                        parsed[2] = image["src"]
                                                                                                        #outpath = os.path.join(out_folder, filename)
                                                                                                        if image["src"].lower().startswith("http"):
                                                                                                                image_url=image["src"]
                                                                                                                #print "got the image 4"
                                                                                                        else:
                                                                                                                image_url=urlparse.urlunparse(parsed)
                                                                                                                #print image_url
                                                                                                                #print "got the image 4a"
                                                                                                        break
                                                                                else:
                                                                                        #print image
                                                                                        filename = image["src"].split("/")[-1]
                                                                                        file_ext=filename.split(".")[-1]
                                                                                        if (file_ext == "jpg" or file_ext == "jpeg" or file_ext == "gif") and filename.find("subscribe-facebook") < 0 and filename.find("subscribe-twitter") < 0 and filename.find("-rss") < 0 and filename.find("logo") < 0 and filename.find("-icon") < 0 and (feed_id < 1036 or feed_id > 1056 or image["src"].find("archive") < 0):
                                                                                                parsed[2] = image["src"]
                                                                                                #outpath = os.path.join(out_folder, filename)
                                                                                                if image["src"].lower().startswith("http"):
                                                                                                        image_url=image["src"]
                                                                                                        print "got the image 4b"
                                                                                                else:
                                                                                                        image_url=urlparse.urlunparse(parsed)
                                                                                                        print image_url
                                                                                                        print "got the image 4c"
                                                                                                break
                                                                except Exception:
                                                                        traceback.print_exc()
                                                                        break
                                                        
                                                                if image_url <> None:
                                                                        break
                                                        
                                                        if image_url == None:
                                                                #print "no url making last effort"
                                                                #if nothing works make the last effort scrap the page take first six and see if they are gif or jpg
                                                        
                                                                bodytag = soup.find("body");

                                                                for image in bodytag.findAll("img",limit=12):
                                                                        if image.has_key("width") :
                                                                                if feed_id > 1035 and feed_id < 1057:
                                                                                        #for the hindu
                                                                                        w_size=325
                                                                                else:
                                                                                        w_size=150
                                                                                if int(image["width"].replace("px","")) > w_size:
                                                                                        #print "Image: %(src)s" % image
                                                                                        filename = image["src"].split("/")[-1]
                                                                                        file_ext=filename.split(".")[-1]
                                                                                        if (file_ext == "jpg" or file_ext == "jpeg") and filename.find("logo") < 0 and filename.find("-icon") < 0 and (feed_id < 1036 or feed_id > 1056 or image["src"].find("archive") < 0):
                                                                                                parsed[2] = image["src"]
                                                                                                #outpath = os.path.join(out_folder, filename)
                                                                                                if image["src"].lower().startswith("http"):
                                                                                                        image_url=image["src"]
                                                                                                else:
                                                                                                        image_url=urlparse.urlunparse(parsed)
                                                                                                #print image_url
                                                                                                #print "got the image 5"
                                                                                                break
                                                                        else:
                                                                                #print "Image: %(src)s" % image
                                                                                filename = image["src"].split("/")[-1]
                                                                                file_ext=filename.split(".")[-1]
                                                                                if (file_ext == "jpg" or file_ext == "jpeg") and filename.find("subscribe-facebook") < 0 and filename.find("subscribe-twitter") < 0 and filename.find("logo") < 0 and filename.find("-rss") < 0 and filename.find("-icon") < 0 and (feed_id < 1036 or feed_id > 1056 or image["src"].find("archive") < 0):
                                                                                        parsed[2] = image["src"]
                                                                                        #outpath = os.path.join(out_folder, filename)
                                                                                        if image["src"].lower().startswith("http"):
                                                                                                image_url=image["src"]
                                                                                        else:
                                                                                                image_url=urlparse.urlunparse(parsed)
                                                                                        #print "got the image 5b"
                                                                                        #print image_url
                                                                                        break
                        
                                        #print feed_text

                                        #if len(e.enclosures) > 0:
                                        #        print e.enclosures[0]

                                        #prepare SQL query to insert feed_text
                                        try:
                                                created_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                                                myinsert = [{"id" : feed_id, "url": feed_text_url, "text": feed_text, "title": feed_title, "content": feed_content, "image": image_url, "published": date_published, "created": created_time }]
                                                
                                                sql_write="insert into salt_feeds(feed_catalogue_id, feed_text_url, \
                                                feed_text, feed_title, feed_content, feed_image_file_path,feed_date_published,created_time) \
                                                values (%(id)s, %(url)s, %(text)s,%(title)s,%(content)s, %(image)s,%(published)s,%(created)s)"
                                                
                                                
                                        except Exception:
                                                traceback.print_exc()
                                        try:
                                                cursor_w.execute("set names utf8;") 
                                                cursor_w.executemany(sql_write,myinsert)
                                                db.commit()
                                        except Exception:
                                                print sql_write
                                                db.rollback()
                                                traceback.print_exc()
                        except Exception:
                                traceback.print_exc()
                                pass
                #break
except Exception, e:
        #ignore exception and go forward
        #pass
        print "Error: Unable to extract feed data"
        traceback.print_exc()
#disconnect
db.close()
