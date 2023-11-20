# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 09:39:34 2023

@author: 54934
"""
import re
import hashlib

# with open("./js/fingerprint.js", 'r', encoding='UTF-8') as f:
#     line = f.read()
# ctx = execjs.compile(line)

class read_js:
    def __init__(self):
        print('ok')
        #self.get_js()

    # 执行本地的js
    # def get_js(self):
    #     f = open("./js/fingerprint.js", 'r', encoding='UTF-8')
    #     line = f.read()
    #     # htmlstr = ''
    #     # while line:
    #     #     htmlstr = htmlstr + line
    #     #     line = f.read()
    #     print('js文件加载成功')
    #     self.ctx = execjs.compile(line)

    def query_id(self, text):
        res = self.ctx.call('fingerprint', text, False, False)
        hash_obj = hashlib.sha256(res.encode('utf-8'))
        hash_val = hash_obj.hexdigest()
        return hash_val

    def hash_create(self, res):
        hash_obj = hashlib.sha256(res.encode('utf-8'))
        hash_val = hash_obj.hexdigest()
        return hash_val



def fingerprint(sql, matchMD5Checksum, matchEmbeddedNumbers):
    #  special cases
    pat = r'^SELECT /\*!40001 SQL_NO_CACHE \*/ \* FROM `'
    if re.search(pat, sql):
        return 'mysqldump'
    pat = r'/\*\w+\.\w+:[0-9]/[0-9]\*/'
    if re.search(pat, sql):
        return 'percona-toolkit'
    pat = r'^administrator command: '
    if re.search(pat, sql):
        return sql
    pat = r'^\s*(call\s+\S+)\('
    a = re.match(pat, sql, flags=re.I) # 忽略大小写
    if a:
        return a.group(1).lower()
    pat = r'^((?:INSERT|REPLACE)(?: IGNORE)?\s+INTO.+?VALUES\s*\(.*?\))\s*,\s*\('
    a = re.match(pat, sql, flags=re.I | re.DOTALL)
    if a:
        return a.group(1).lower()
    # multi line comment
    sql = re.sub(r'/\*[^!].*?\*/', '', sql)
    # one_line_comment
    sql = re.sub(r'(?:--|#)[^\'"\r\n]*(?=[\r\n]|$)', '', sql)
    # USE statement
    pat = r'^use \S+$'
    if re.match(pat, sql, flags=re.I):
        return 'use ?'
    # literals
    sql = re.sub(r'([^\\])(\\\')', r'\1', sql)
    sql = re.sub(r'([^\\])(\\\")', r'\1', sql)
    sql = sql.replace(r'\\\\', '')
    sql = sql.replace(r'\\\'', '')
    sql = sql.replace(r'\\"', '')
    sql = re.sub(r'([^\\])(".*?[^\\]?")', r'\1?', sql)
    sql = re.sub(r"([^\\])(\'.*?[^\\]?')", r'\1?', sql)
    sql = re.sub(r'\bfalse\b|\btrue\b', '?', sql, flags=re.I)
    if matchMD5Checksum:
        sql = re.sub(r'([._-])[a-f0-9]{32}', r'\1?', sql)
    if not matchEmbeddedNumbers:
        re_exp = r'[0-9+-][0-9a-f.xb+-]*'
        sql = re.sub(re_exp, '?', sql, flags=re.I)
    else:
        re_exp = r'[0-9+-][0-9a-f.xb+-]*'
        sql = re.sub(r'\b'+re_exp, '?', sql, flags=re.I)
    if matchMD5Checksum:
        sql = re.sub(r'[xb+-]\?', '?', sql)
    else:
        sql = re.sub(r'[xb.+-]\?', '?', sql)
    # collapse whitespace
    sql = re.sub(r'^\s+', '', sql)
    sql = re.sub(r'[\r\n]+$', '', sql)
    sql = re.sub(r'[ \n\t\r\f]+', ' ', sql)
    # to lower case
    sql = sql.lower()
    # get rid of null
    sql = re.sub(r'\bnull\b', '?', sql)
    # collapse IN and VALUES lists
    sql = re.sub(r'\b(in|values?)(?:[\s,]*\([\s?,]*\))+', r'\1(?+)', sql)
    # collapse UNION
    sql = re.sub(r'\b(select\s.*?)(?:(\sunion(?:\sall)?)\s\1)+', r'\1 /*repeat\2*/', sql)
    # limit
    sql = re.sub(r"\blimit \?\(?:, ?\?| offset \?\)?", 'limit ?', sql)
    # order by
    sql = re.sub(r"\b(.+?)\s+ASC", r'\1', sql, flags=re.I)
    if '?rom' in sql:
        sql = sql.replace(r'?rom', r'?from')
    if r'limit' in sql:
        sql = sql.replace(r'?limit ?, ?', r'?limit ?')
        sql = sql.replace(r'limit ?, ?', r'limit ?')
        sql = sql.replace(r'? limit ?,?', r'? limit ?')
    return sql

def sub_fingerprint(sql):
    pat = r'^SELECT /\*!40001 SQL_NO_CACHE \*/ \* FROM `'
    if re.search(pat, sql):
        return 'mysqldump'
    pat = r'/\*\w+\.\w+:[0-9]/[0-9]\*/'
    if re.search(pat, sql):
        return 'percona-toolkit'
    pat = r'^administrator command: '
    if re.search(pat, sql):
        return sql
    pat = r'^\s*(call\s+\S+)\('
    a = re.match(pat, sql, flags=re.I) # 忽略大小写
    if a:
        return a.group(1).lower()
    pat = r'^((?:INSERT|REPLACE)(?: IGNORE)?\s+INTO.+?VALUES\s*\(.*?\))\s*,\s*\('
    a = re.findall(pat, sql, flags=re.I | re.DOTALL)
    if a:
        try:
            sql = a[1]
        except Exception:
            sql = 'undefined'

def fingerprint1(sql, matchMD5Checksum, matchEmbeddedNumbers):
    #  special cases
    sub_fingerprint(sql)
    # multi line comment
    sql = re.sub('\/\*[^!].*?\*\/', '', sql, flags=re.M)
    # one_line_comment
    sql = re.sub('''(?:--|#)[^'"\r\n]*(?=[\r\n]|$)''', '', sql)
    # USE statement
    pat = '^use \S+$'
    if re.match(pat, sql, flags=re.I):
        return 'use ?'
    # literals
    pat = "\(\[^\\]\)\(\\'\)"
    a = re.findall(pat, sql)
    if a:
        sql = re.sub(pat, a[0], sql)
#    sql = re.sub("\(\[^\\]\)\(\\'\)", '$1', sql)  # 单行匹配
#    sql = re.sub('\(\[^\\]\)\(\\"\)', '$1', sql)
    pat = '\(\[^\\]\)\(\\"\)'
    a = re.findall(pat, sql)
    if a:
        sql = re.sub(pat, a[0], sql)
    sql = sql.replace("\\\\", '')
    sql = sql.replace("\\'", '')
    sql = sql.replace('\\"', '')
    pat = r'([^\\])(".*?[^\\]?")'
    a = re.findall(pat, sql)
    if a:
        sql = re.sub(pat, a[0], sql)
    pat = r"([^\\])('.*?[^\\]?')"
    a = re.findall(pat, sql)
    if a:
        sql = re.sub(pat, a[0], sql)
#    sql = re.sub(r'([^\\])(".*?[^\\]?")', '$1', sql)
#    sql = re.sub(r"([^\\])('.*?[^\\]?')", '$1', sql)
    sql = re.sub("\bfalse\b|\btrue\b", '?', sql, flags=re.I)
    if matchMD5Checksum:
        pat = "\([._-]\)[a-f0-9]{32}"
        a = re.findall(pat, sql)
        if a:
            sql = re.sub(pat, a[0], sql)
    if not matchEmbeddedNumbers:
        re_express = "[0-9+-][0-9a-f.xb+-]*"
        sql = re.sub(re_express, '?', sql, flags=re.I)
    else:
        re_express = "[0-9+-][0-9a-f.xb+-]*"
        sql = re.sub("\b"+re_express, '?', sql, flags=re.I)
    if matchMD5Checksum:
        sql = re.sub("[xb+-]\?", '?', sql)
    else:
        sql = re.sub("[xb.+-]\?", '?', sql)
    # collapse whitespace
    sql = re.sub('^\s+', '', sql)
    sql = re.sub('^\s+', '', sql)
    sql = re.sub('[ \n\t\r\f]+', '', sql)
    # to lower case
    sql = sql.lower()
    # get rid of null
    sql = sql.replace("\bnull\b", '?')
    # collapse IN and VALUES lists
    sql = re.sub("\b\(in|values?\)\(?:[\s,]*\([\s?,]*\)\)+", '$1(?+)', sql)
    # collapse UNION
    sql = re.sub("\b\(select\s.*?\)\(?:\(\sunion\(?:\sall\)?\)\s\1\)+", '$1 /*repeat$2*/', sql)
    # limit
    sql = re.sub("\blimit \?\(?:, ?\?| offset \?\)?", 'limit ?', sql)
    # order by
    pat = "\b\(.+?\)\s+ASC"
    a = re.findall(pat, sql)
    if a:
        sql = re.sub(pat, a[0], sql)
    return sql

def abc(x):

    res = fingerprint(x,False,False)
    return res

if __name__ == '__main__':
#    import execjs
#    with open('static/fingerprint.js','r',encoding='utf-8') as f:
#        jstext=f.read()
#    ctx=execjs.compile(jstext)
    js_read = read_js()
    text1 = """SELECT OT.OFFER_PROD_INST_REL_ID AS "offerProdInstRelId", OT.OFFER_INST_ID AS "offerInstId", OT.REGION_ID AS "regionId", OT.STATUS_CD AS "statusCd", OT.OWNER_CUST_ID AS "ownerCustId" FROM OFFER_PROD_INST_REL_B4 OT WHERE OT.EXP_DATE < '2023-03-08 22:00:30'  AND OT.EXP_DATE > '2023-10-08 22:00:30'  AND OT.STATUS_CD != '1100' LIMIT 3200; """
    a = fingerprint(text1, False, False)
    text2 = """SELECT OT.OFFER_PROD_INST_REL_ID AS "asdfferProdInstRelId", OT.OFFER_INST_ID AS "offerInstId", OT.REGION_ID AS "regionId", OT.STATUS_CD AS "statusCd", OT.OWNER_CUST_ID AS "ownerCustId" FROM OFFER_PROD_INST_REL_B4 OT WHERE OT.EXP_DATE < '2023-01-08 22:00:30'  AND OT.EXP_DATE > '2023-11-08 22:00:30'  AND OT.STATUS_CD != '3300' LIMIT 500; """
    b = fingerprint(text2, False, False)
    print('text1 MySQL指纹:',js_read.hash_create(a))
    print('text2 MySQL指纹:',js_read.hash_create(b))
    print(a)
    print(b)
    text3 = 'GET /flowplat/getImage?random=0.6334687701729151 HTTP/1.1'
    text4 = 'GET /flowplat/getImage?random=0.0 HTTP/1.1'
    c = fingerprint(text3,False,False)
    d = fingerprint(text4,False,False)
    print(c)
    print(d)
    print('text3 MySQL指纹:', js_read.hash_create(c))
    print('text4 MySQL指纹:', js_read.hash_create(d))