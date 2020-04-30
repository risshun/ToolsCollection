import email
import os
import html2text

os.chdir('C:/Users/Ernest/Desktop/corpus')

h2t = html2text.HTML2Text()
h2t.body_width=20000

def text_parser(path):
    with open(path) as eml:
        m = email.message_from_file(eml)

    if m.get_content_type!='mixed':
        for m in m.walk():
            if m.get_content_subtype()=='plain':
                try:
                    text = str(m.get_payload(decode=True),encoding='utf-8')
                except:
                    text = str(m.get_payload(decode=True),encoding='gbk')
                text = text.replace('--\n发自我的网易邮箱平板适配版','')
                text = text.split('----------------')[0]
                text = text.strip()
                return text
            if m.get_content_subtype()=='html':
                try:
                    text = str(m.get_payload(decode=True),encoding='utf-8')
                except:
                    text = str(m.get_payload(decode=True),encoding='gbk')
                text = h2t.handle(text)
                text = text.strip()
                text = text.replace('  ','')
                return text

for root, dirs, files in os.walk("."):
    for file_name in files:
        if file_name.endswith('.eml'):
            path = os.path.join(root,file_name)
            try:
                text = text_parser(path)
                text = text.replace(u'\u202f','')
                text = text.replace('\n ','')
                text = text.splitlines()
                text = list(filter(None, text))
                for ed in text:
                    if 'Editor:' in ed or 'Editors:' in ed:
                        text = text[:text.index(ed)+1]
                        text = '\n'.join(text)
                        with open(path.replace('.eml', '')+'.txt', 'w') as txt:
                            txt.write(text)
            except:
                print('fuck:',path)
                break
        print('\r','已完成：{:.2f}%'.format(round((files.index(file_name)+1)*100/len(files))), end='', flush=True)