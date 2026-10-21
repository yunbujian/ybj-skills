#!/usr/bin/env python3
"""Search bundled course titles; open returned URLs to verify the actual lesson."""
import argparse
import json
import re
from pathlib import Path

def search(query, limit=8):
    terms=[s.casefold() for s in re.split(r'[\s，,、]+',query.strip()) if s]
    if not terms:
        raise ValueError('请输入至少一个关键词')
    if not 1<=limit<=30:
        raise ValueError('limit 必须为 1–30')
    catalog=Path(__file__).resolve().parents[1]/'references/catalog.json'
    rows=json.loads(catalog.read_text(encoding='utf-8'))
    hits=[]
    for row in rows:
        title=row['title'].casefold()
        headings=' '.join(row['headings']).casefold()
        score=sum(8*title.count(term)+headings.count(term) for term in terms)
        if score:
            hits.append({**row,'score':score})
    return {'scope':'仅搜索课程标题与章节线索，不含课文和 Notion 文章；候选必须联网读取正文后才能引用',
            'hits':sorted(hits,key=lambda r:(-r['score'],r['skill'],r['id']))[:limit]}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',help='以空格分隔关键词和同义词')
    p.add_argument('--limit',type=int,default=8)
    args=p.parse_args()
    try:
        print(json.dumps(search(args.query,args.limit),ensure_ascii=False,indent=2))
    except (ValueError,OSError) as e:
        p.error(str(e))
