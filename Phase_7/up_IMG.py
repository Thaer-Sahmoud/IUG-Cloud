


from flask import Flask, render_template, request, redirect, flash, url_for,g
import os
import psycopg2
import time
from datetime import datetime, timezone
import pandas as pd


database = "Photos"
user = "postgres"
pwd = "root"
host = "localhost"
port = '5432'
cur = None
conn = None

def CreateKeyValueTable ():
    global cur
    global conn
    try:
        conn = psycopg2.connect(database=database,
                                user=user,
                                password=pwd,
                                host=host,
                                port=port)

        print("Connection successfully")
        cur = conn.cursor()
        create_script = ''' create table if  not exists key_value(             
                        key_id varchar(200),
                        value   varchar(200))'''
        cur.execute(create_script)
        conn.commit()

        cur.close()
        conn.close()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def CreateMemCacheStatusTable ():
    global cur
    global conn
    try:
        conn = psycopg2.connect(database=database,
                                user=user,
                                password=pwd,
                                host=host,
                                port=port)

        print("Connection successfully")
        cur = conn.cursor()
        create_script = ''' create table if  not exists memcache_status(             
                        id SERIAL,
                        key_id varchar(200),
                        value   varchar(200),
                        arrive  time,
                        hit_or_miss boolean)'''
        cur.execute(create_script)
        conn.commit()

        cur.close()
        conn.close()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

CreateKeyValueTable()

def insertIMGtoDB (img_key, imgName):
    global conn
    global cur
    try:
        conn = psycopg2.connect(database=database,
                                user=user,
                                password=pwd,
                                host=host,
                                port=port)

        print("Connection successfully")
        cur = conn.cursor()

        create_script = ''' create table if  not exists key_value(             
                        key_id varchar(200),
                        value   varchar(200))'''
        cur.execute(create_script)
        conn.commit()

        sql = """INSERT INTO key_value (key_id, value)
                 VALUES(%s, %s);"""
        cur.execute(sql, (img_key,imgName))
        conn.commit()

        cur.close()
        conn.close()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def insertMemHit (k, val, hitBool):
    global conn
    global cur
    try:
        conn = psycopg2.connect(database=database,
                                user=user,
                                password=pwd,
                                host=host,
                                port=port)


        cur = conn.cursor()
        sql = """INSERT INTO memcache_status (key_id,value,arrive, hit_or_miss)
                 VALUES(%s, %s, %s,%s );"""
        dt = datetime.now(timezone.utc)
        cur.execute(sql, (k,val,time.time(),hitBool))
        print("Mem Cache Inserted")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


memcache = {}


hits = misses =0


memCacheStatus = pd.DataFrame()

CreateMemCacheStatusTable ()
def hit_sql (key, val,HitBool):
    global memCacheStatus
    if HitBool == True:
        new_row = {'key':key, 'value':val, 'hit':True, 'time':time.time()}
        memCacheStatus= memCacheStatus.append(new_row, ignore_index=True)
    else:
        new_row = {'key':key, 'value':val, 'hit':False, 'time':time.time()}
        memCacheStatus= memCacheStatus.append(new_row, ignore_index=True)
    print(memCacheStatus)
# def memcache_status(key):
#     global memcache, hits, misses
#     if key in memcache:
#         hits += 1
#         hit_sql(key, memcache[key], True)
#         return memcache[key]
#     else:
#         misses += 1
#         hit_sql(key, memcache[key],False)
#         return None



def memcache_status(key):
    global memcache, hits, misses
    if key in memcache:
        hits += 1
        hit_sql(key, memcache[key], True)
        return memcache[key]
    else:
        misses += 1
        hit_sql(key, memcache[key],False)
        return None


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

# Set the allowed file extensions for uploads
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    # Check if a file has an allowed extension
    print(f"The extenction is {filename.rsplit('.', 1)[1]}")
    if (filename.rsplit('.', 1)[1]).lower() in app.config['ALLOWED_EXTENSIONS']:
        validation = True
    else:
        validation = False
    print(f"Validation is {validation}")
    return validation

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')
def home():
    return render_template('index.html')
def view():
    return render_template('view.html')
def KEYs():
    return render_template('keys.html')
def Statistics():
    return render_template('statistics.html')
def Images():
    return render_template('images.html')

@app.route('/view', methods=['GET', 'POST'])
def view():
    image_folder = os.path.join('static', 'uploads')
    images = []
    for filename in os.listdir(image_folder):
        if filename.endswith(('.jpeg', '.png', '.PNG','.jpg', '.gif')):
            images.append(filename)
    return render_template('view.html', images=images)
    # return render_template('view.html')

@app.route('/statistics', methods=['GET', 'POST'])
def Statistics():
    return render_template('statistics.html')

@app.route('/keys', methods=['GET', 'POST'])
def KEYs():
    global memcache
    return render_template('keys.html',result=memcache)

@app.route('/images', methods=['GET', 'POST'])
def Images():
    return render_template('images.html')

@app.route('/get_file', methods=['GET', 'POST'])
def get_file():
    global memcache
    file = request.files['file']
    if allowed_file(file.filename):
        filename = file.filename
        file_ext = os.path.splitext(filename)[1]

        IMG_Key = request.form['text']
        new_file_key_name =IMG_Key+ file_ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_file_key_name))
        insertIMGtoDB(IMG_Key, new_file_key_name)
        msg_to_disp = 'File Uploaded Sucessfully'
        memcache[IMG_Key]=new_file_key_name
        memcache_status(IMG_Key)
        for key,value in memcache.items():
            print(key, "\t",value)
        return render_template('upload_S.html', error=msg_to_disp)
    else:

        return render_template('upload_Invalid.html')



if __name__ == '__main__':
    app.run(debug=True)
