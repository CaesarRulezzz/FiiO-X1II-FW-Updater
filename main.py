import urllib.request
from bs4 import BeautifulSoup
import re
from tkinter import messagebox
import sys
import subprocess
import os

# read version from file
try:
    config = open('version.txt', 'r')
    version = config.read()
    config.close()
    print('Last checked version:', version)
except:
    print('Could not open version file!')
    version = '0.0.0'

# open forum page with FW posts
update_page = urllib.request.urlopen('http://www.fiio.me/forum.php?mod=viewthread&tid=39932')

str_var = ''
new_str = ''
version_latest = ''

# parsing with BeautifulSoup4
soup = BeautifulSoup(update_page.read().decode(), "html.parser")
first_font_tag = soup.find('font', string=re.compile(r'FiiO X1'))

# find download link in the nearest element to the search above
for element in first_font_tag.next_elements:
    str_var = str(element)
    str_pos = str_var.find('http://x1pack.fiio.net')
    if str_pos > 0:
        new_str = str_var[str_pos:]
        break;

# extract version and link from html
if len(new_str) > 1:
    str_parts = new_str.split('/')
    version_latest = str_parts[3]
    link = new_str.split('"')[0]

# check version
if version_latest != version:
    print('FOUND NEW FW VERSION!!!', version_latest)
    messagebox.showinfo(message="Обнаружена новая версия прошивки плеера FiiO X1II!", icon='info', title='Внимание!')
    if messagebox.askyesno(message='Скачать новую версию прошивки сейчас?', icon='question', title='Обновление FiiO X1II') is False:
        sys.exit(0)
else:
    print('NO NEW VERSION!')
    sys.exit(0)

# Download firmware from server
try:
    fw = urllib.request.urlopen(link)
    # trying to save fw file
    try:
        print('Downloading data...')
        data = fw.read()
        print('Saving FW to file...')
        config = open('X1II.fw', 'wb')
        config.write(data)
        config.close()
        print('FW saved to X1II.fw')
        messagebox.showinfo(message="Прошивка успешно сохранена", icon='info',
                            title='Обновление FiiO X1II')

        if messagebox.askyesno(message='Открыть папку с файлом прошивки (X1II.fw)?', icon='question',
                               title='Обновление FiiO X1II') is True:
            fw_path = os.getcwd() + '\X1II.fw'
            print(fw_path)
            subprocess.Popen(r'explorer /select, ' + fw_path)
        if messagebox.askyesno(message='Открыть инструкцию по прошивке плеера?', icon='question',
                               title='Обновление FiiO X1II') is True:
            os.startfile('http://fiio.me/forum.php?mod=viewthread&tid=41621&extra=')
    except:
        print('Could not write FW file!')
        messagebox.showinfo(message="Ошибка при сохранении прошивки!", icon='error',
                            title='Обновление FiiO X1II')
    # trying to save version to file
    try:
        config = open('version.txt', 'w')
        config.write(version_latest)
        config.close()
        print('Latest version saved')
    except:
        print('Could not open version file!')
        messagebox.showinfo(message="Ошибка при запоминании прошивки!", icon='error',
                            title='Обновление FiiO X1II')
except urllib.error.HTTPError:
    print('No FW found :(')
    pass
