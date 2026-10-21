"""Acquire/normalize captions and verify exact quotations. Python 3.10+."""
import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def whitespace(text):
    return ' '.join(text.split())


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def seconds(value):
    parts = value.replace(',', '.').split(':')
    return sum(float(p) * 60**i for i, p in enumerate(reversed(parts)))


def timestamp(value):
    if value is None:
        return '无时间'
    n = int(value)
    return f'{n//3600:02d}:{n%3600//60:02d}:{n%60:02d}'


def parse(path):
    raw = path.read_text(encoding='utf-8-sig')
    ext = path.suffix.lower()
    rows = []
    if ext in ('.json', '.json3'):
        data = json.loads(raw)
        if 'events' in data:
            for event in data['events']:
                text = ''.join(s.get('utf8', '') for s in event.get('segs', []))
                if not text.strip():
                    continue
                start = event.get('tStartMs', 0) / 1000
                duration = event.get('dDurationMs')
                rows.append({'start': start, 'end': start + duration / 1000 if duration is not None else None, 'text': text})
        elif 'segments' in data:
            rows = [{'start': s.get('start'), 'end': s.get('end'), 'text': s['text']} for s in data['segments']]
        else:
            raise ValueError('Unsupported JSON: expected events or segments')
    elif ext in ('.vtt', '.srt'):
        for block in re.split(r'\n\s*\n', raw):
            lines = block.splitlines()
            for i, line in enumerate(lines):
                if '-->' not in line:
                    continue
                a, b = line.split('-->', 1)
                text = '\n'.join(lines[i+1:])
                text = html.unescape(re.sub(r'<[^>]+>', '', text))
                rows.append({'start': seconds(a.strip()), 'end': seconds(b.strip().split()[0]), 'text': text})
                break
    elif ext in ('.txt', '.md'):
        rows = [{'start': None, 'end': None, 'text': p} for p in re.split(r'\n\s*\n', raw) if p.strip()]
    else:
        raise ValueError('Supported files: txt, md, srt, vtt, json3, Whisper JSON')

    normalized = []
    previous = None
    for i, row in enumerate(rows):
        text = whitespace(row['text'])
        # Only remove rolling repeats when the caption time windows overlap.
        if previous and row['start'] is not None and previous['end'] is not None and row['start'] < previous['end']:
            old, new = whitespace(previous['text']).split(), text.split()
            for k in range(min(len(old), len(new)), 0, -1):
                if old[-k:] == new[:k]:
                    text = ' '.join(new[k:])
                    break
        previous = row
        if text:
            normalized.append({'id': f's{i+1:05d}', 'raw_index': i, 'start': row['start'], 'end': row['end'], 'text': text})
    if not normalized:
        raise ValueError('No caption text found')
    return normalized


def normalize(path, output, url=None):
    output.mkdir(parents=True, exist_ok=True)
    result = output / 'source.json'
    if result.exists():
        raise FileExistsError(f'Refusing to overwrite {result}; choose a new run directory')
    source = path.resolve()
    rawcopy = output / ('original' + path.suffix.lower())
    if source != rawcopy.resolve():
        if rawcopy.exists():
            raise FileExistsError(rawcopy)
        shutil.copy2(source, rawcopy)
    rows = parse(source)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    dump(result, {'source_path': str(source), 'sha256': digest, 'url': url, 'segments': rows})
    # Whole segment chunks. A very long plain paragraph remains intact rather
    # than being cut arbitrarily; users can supply SRT/Whisper for finer chunks.
    groups, group, length = [], [], 0
    for row in rows:
        if group and length + len(row['text']) > 18000:
            groups.append(group)
            group, length = [], 0
        group.append(row)
        length += len(row['text'])
    if group:
        groups.append(group)
    chunkdir = output / 'chunks'
    chunkdir.mkdir(exist_ok=True)
    manifest = []
    for n, group in enumerate(groups, 1):
        target = chunkdir / f'chunk-{n:02d}.txt'
        target.write_text('\n'.join(f'[{s["id"]} {timestamp(s["start"])}] {s["text"]}' for s in group)+'\n', encoding='utf-8')
        manifest.append({'file': target.name, 'segment_ids': [s['id'] for s in group]})
    dump(output / 'chunks.json', manifest)
    print(json.dumps({'segments': len(rows), 'chunks': len(groups), 'source': str(result)}, ensure_ascii=False))


def acquire(args):
    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    command = [sys.executable, '-m', 'yt_dlp', '--no-playlist', '--skip-download', '--write-info-json', '--write-subs', '--write-auto-subs', '--sub-langs', 'en.*,en', '--sub-format', 'json3/vtt', '--retries', '2', '--socket-timeout', '25', '-o', str(output/'%(id)s.%(ext)s'), args.url]
    result = subprocess.run(command, capture_output=True, text=True)
    (output/'acquire.log').write_text(result.stdout+'\n'+result.stderr, encoding='utf-8')
    candidates = sorted(output.glob('*.json3')) or sorted(output.glob('*.vtt'))
    if not candidates:
        raise RuntimeError(f'No English captions obtained. See {output / "acquire.log"}')
    # Prefer original English track over translated variants.
    candidates.sort(key=lambda p: (not (p.name.endswith('.en.json3') or p.name.endswith('.en.vtt')), len(p.name)))
    normalize(candidates[0], output/'normalized', args.url)


def check_quotes(args):
    source = json.loads(args.source.read_text(encoding='utf-8'))
    rows = source['segments']
    by_id = {s['id']: (i, s) for i, s in enumerate(rows)}
    quotes = json.loads(args.quotes.read_text(encoding='utf-8'))
    errors, checked = [], []
    if len(quotes) != args.count:
        errors.append(f'Expected {args.count} quotes, found {len(quotes)}')
    seen = set()
    for i, quote in enumerate(quotes, 1):
        problems = []
        text = whitespace(quote.get('text', ''))
        ids = quote.get('segment_ids', [])
        if not text:
            problems.append('Empty quote')
        if text in seen:
            problems.append('Duplicate quote')
        seen.add(text)
        if not quote.get('speaker') or not quote.get('translation'):
            problems.append('Missing speaker or Chinese translation')
        valid = bool(ids) and all(s in by_id for s in ids)
        if not valid:
            problems.append('Missing or unknown segment IDs')
        else:
            indexes = [by_id[s][0] for s in ids]
            if indexes != list(range(indexes[0], indexes[0]+len(indexes))):
                problems.append('Segments must be contiguous and ordered')
            haystack = ' '.join(whitespace(by_id[s][1]['text']) for s in ids)
            if text not in haystack:
                problems.append('Quote is not an exact substring (whitespace normalization only)')
        item = {'index': i, 'matches_transcript': not problems, 'errors': problems, 'speaker': quote.get('speaker'), 'segment_ids': ids, 'audio_verified': False}
        if valid:
            item['start'] = by_id[ids[0]][1]['start']
            if item['start'] is not None and source.get('url'):
                item['jump_url'] = source['url'].split('&t=')[0] + ('&' if '?' in source['url'] else '?') + f't={int(item["start"])}s'
        checked.append(item)
    success = not errors and all(q['matches_transcript'] for q in checked)
    report = {'passed': success, 'source_sha256': source['sha256'], 'errors': errors, 'quotes': checked, 'note': 'Text matching does not verify audio or speaker attribution.'}
    dump(args.output, report)
    print(json.dumps({'passed': success, 'checked': len(checked), 'report': str(args.output)}))
    return 0 if success else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('acquire')
    p.add_argument('--url', required=True)
    p.add_argument('--output', required=True, type=Path)
    p = sub.add_parser('normalize')
    p.add_argument('--input', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--url')
    p = sub.add_parser('check-quotes')
    p.add_argument('--source', required=True, type=Path)
    p.add_argument('--quotes', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--count', type=int, default=10)
    args = parser.parse_args()
    try:
        if args.command == 'acquire':
            acquire(args)
        elif args.command == 'normalize':
            normalize(args.input, args.output, args.url)
        else:
            return check_quotes(args)
    except (ValueError, OSError, RuntimeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
