#!/usr/bin/env python3
"""Offline evidence-film renderer. Reads original screenshots; never calls lab/CI APIs."""
import argparse
import concurrent.futures
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import subprocess
import urllib.request
import wave

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from piper import PiperVoice, SynthesisConfig

VIDEO = Path(__file__).resolve().parent.parent
EVIDENCE = VIDEO.parent
PROJECT = json.loads((VIDEO / 'source/project.json').read_text())
CACHE = Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache')) / 'bytebase-video-tools'
WORK = CACHE / 'render'
WORK.mkdir(parents=True, exist_ok=True)
FF = os.environ.get('FFMPEG_BINARY', imageio_ffmpeg.get_ffmpeg_exe())
FPS, SR = 30, 22050
FONT = VIDEO / 'assets/NotoSans-VF.ttf'


def command(args, log=None):
    result = subprocess.run([str(x) for x in args], capture_output=True, text=True)
    if log:
        Path(log).write_text(result.stderr)
    if result.returncode:
        raise RuntimeError(result.stderr[-5000:])
    return result


def verify_originals():
    manifest = json.loads((VIDEO / 'source/evidence-original-sha256.json').read_text())
    for name, expected in manifest.items():
        assert hashlib.sha256((EVIDENCE / name).read_bytes()).hexdigest() == expected, name
    assert len(PROJECT['scenes']) == 18
    for scene in PROJECT['scenes']:
        assert hashlib.sha256((EVIDENCE / scene['image']).read_bytes()).hexdigest() == scene['image_sha256']
    return len(manifest)


def voice_model():
    name = PROJECT['voice']['model'] + '.onnx'
    dest = CACHE / 'voices' / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    base = ('https://huggingface.co/rhasspy/piper-voices/resolve/'
            + PROJECT['voice']['revision'] + '/vi/vi_VN/vais1000/medium/')
    for suffix in ['', '.json']:
        path = Path(str(dest) + suffix)
        if not path.exists():
            urllib.request.urlretrieve(base + name + suffix, path)
    assert hashlib.sha256(dest.read_bytes()).hexdigest() == PROJECT['voice']['sha256']
    return dest


def spoken(text):
    # Caption keeps real product/identifier spelling. Only the TTS input is phonetic.
    replacements = {
        'GitHub': 'Ghít Hắp', 'Bytebase': 'Bytebase', 'Jenkinsfile': 'Jenkins phai', 'Jenkins': 'Jenkins',
        'Oracle': 'Oracle', 'SQL': 'ét kiu eo', 'PR': 'pi a', 'POC': 'pi ô xi',
        'CI': 'xi ai', 'API': 'ây pi ai', 'ID': 'ai đi', 'Git': 'Ghít',
        'master': 'mát tơ', 'develop': 'đê ve lốp', 'Revision': 'ri vi giần',
        'Community': 'cơ miu ni ti', 'commit': 'cơ mít', 'Plans': 'các kế hoạch',
        'Plan': 'kế hoạch', 'Flyway': 'Flyway', 'primary key': 'khóa chính',
        'Webhook': 'uép húc', 'byte': 'bai'
    }
    for a, b in replacements.items():
        text = re.sub(r'\b' + re.escape(a) + r'\b', b, text)
    return text


def font(size, bold=False):
    f = ImageFont.truetype(str(FONT), size)
    if bold:
        f.set_variation_by_name('Bold')
    return f


def wrap(text, f, width):
    words = text.split()
    lines = []
    line = ''
    for word in words:
        candidate = (line + ' ' + word).strip()
        if f.getlength(candidate) <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            # Long SHA/identifier: retain all characters, breaking only for layout.
            while f.getlength(word) > width:
                n = len(word)
                while f.getlength(word[:n]) > width:
                    n -= 1
                lines.append(word[:n])
                word = word[n:]
            line = word
    if line:
        lines.append(line)
    return lines


def stamp(seconds, ass=False):
    units = round(seconds * (100 if ass else 1000))
    denom = 100 if ass else 1000
    sec, frac = divmod(units, denom)
    minute, sec = divmod(sec, 60)
    hour, minute = divmod(minute, 60)
    return (f'{hour}:{minute:02}:{sec:02}.{frac:02}' if ass
            else f'{hour:02}:{minute:02}:{sec:02},{frac:03}')


def ass_file(path, cues, offset=0):
    header = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans,40,&H00FFFFFF,&H00FFFFFF,&H00101318,&H00101318,0,0,0,0,100,100,0,0,3,10,0,2,58,58,49,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    lines = [header]
    for cue in cues:
        a, b = cue['start'] - offset, cue['end'] - offset
        if b <= 0:
            continue
        text = '\\N'.join(cue['lines'])
        lines.append(f'Dialogue: 0,{stamp(max(0,a),True)},{stamp(b,True)},Default,,0,0,0,,{{\\q2}}{text}\n')
    path.write_text(''.join(lines))


def make_audio():
    v = None
    timeline, chunks, global_sample = [], [], 0
    for index, scene in enumerate(PROJECT['scenes'], 1):
        samples = [np.zeros(round(.38 * SR), np.int16)]
        local = len(samples[0])
        cues = []
        for ci, text in enumerate(scene['cues']):
            speech = spoken(text)
            key = hashlib.sha256((speech + json.dumps(PROJECT['voice'], sort_keys=True)).encode()).hexdigest()
            path = WORK / (key + '.wav')
            if not path.exists():
                if v is None:
                    v = PiperVoice.load(voice_model())
                with wave.open(str(path), 'wb') as wav:
                    v.synthesize_wav(speech, wav, SynthesisConfig(
                        length_scale=PROJECT['voice']['length_scale'], noise_scale=.55,
                        noise_w_scale=.7, volume=.85))
            with wave.open(str(path)) as wav:
                assert wav.getframerate() == SR and wav.getnchannels() == 1
                a = np.frombuffer(wav.readframes(wav.getnframes()), np.int16).copy()
            lines = wrap(text, font(40), 1760)
            assert len(lines) <= 2, (text, lines)
            cues.append(dict(text=text, tts_text=speech, lines=lines,
                             start=(global_sample+local)/SR,
                             end=(global_sample+local+len(a))/SR,
                             local_start=local/SR, cue_index=ci))
            samples.append(a)
            local += len(a)
            pause = np.zeros(round(.10 * SR), np.int16)
            samples.append(pause)
            local += len(pause)
        pad = np.zeros(round(.52 * SR), np.int16)
        samples.append(pad)
        local += len(pad)
        frames = math.ceil(local * FPS / SR)
        rounded_samples = round(frames * SR / FPS)
        samples.append(np.zeros(rounded_samples-local, np.int16))
        audio = np.concatenate(samples)
        item = dict(scene=scene, number=index, start=global_sample/SR,
                    end=(global_sample+len(audio))/SR, frames=frames, cues=cues)
        timeline.append(item)
        chunks.append(audio)
        global_sample += len(audio)
        print(f'AUDIO {index:02}/18 {frames/FPS:.2f}s — {scene["title"]}', flush=True)
    all_audio = np.concatenate(chunks)
    raw = WORK / 'voiceover-raw.wav'
    with wave.open(str(raw), 'wb') as wav:
        wav.setparams((1, 2, SR, 0, 'NONE', 'not compressed'))
        wav.writeframes(all_audio.tobytes())
    command([FF, '-hide_banner', '-loglevel', 'error', '-y', '-i', raw,
             '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000',
             '-c:a', 'pcm_s16le', VIDEO / 'voiceover-vi.wav'])
    (VIDEO / 'source/timeline.json').write_text(json.dumps(timeline, ensure_ascii=False, indent=2))
    total = global_sample/SR
    print(f'TIMELINE {total:.3f}s / {total/60:.2f} minutes', flush=True)
    assert 180 <= total <= 300, f'Duration {total:.2f}s outside requested 3–5 minutes; edit narration/speed.'
    return timeline


def make_canvas(scene, scene_number, view_number, roi):
    original = Image.open(EVIDENCE / scene['image']).convert('RGB')
    x, y, w, h = roi
    assert 0 <= x < x+w <= original.width and 0 <= y < y+h <= original.height
    canvas = Image.new('RGB', (1920,1080), '#0b1120')
    d = ImageDraw.Draw(canvas)
    accent = '#74dbc9' if 'Bytebase' in scene['platform'] else '#c3b0ff'
    if scene['platform'].startswith('Jenkins'):
        accent = '#ffc385'
    if scene['platform'].startswith('Oracle'):
        accent = '#ffaaa3'
    d.text((36,20), 'Demo lab — trình bày từ ảnh chụp thực nghiệm', font=font(23), fill='#b7c4d8')
    pfont = font(22,True)
    platform = scene['platform'].replace('→',' > ')
    d.text((1884-pfont.getlength(platform),22),platform,font=pfont,fill=accent)
    tf = font(43,True)
    assert tf.getlength(scene['title']) < 1848
    d.text((36,65),scene['title'],font=tf,fill='white')
    d.line((36,133,1884,133),fill='#304057',width=2)
    tag=scene['tag'].replace('→',' > ')
    d.text((38,148),f'VÙNG PHÓNG · ẢNH {scene["evidence_id"]} · {tag}',font=font(20),fill=accent)
    d.rounded_rectangle((35,185,1477,879),radius=9,fill='#edf0f4',outline=accent,width=2)
    crop = original.crop((x,y,x+w,y+h))
    scale = min(1420/w,670/h,2.1)
    crop = crop.resize((round(w*scale),round(h*scale)),Image.Resampling.LANCZOS)
    canvas.paste(crop,(46+(1420-crop.width)//2,197+(670-crop.height)//2))
    d = ImageDraw.Draw(canvas)
    d.text((1510,151),'ẢNH GỐC · TOÀN CẢNH',font=font(20,True),fill='#b7c4d8')
    ow = 374
    oh = round(ow*original.height/original.width)
    overview = original.resize((ow,oh),Image.Resampling.LANCZOS)
    canvas.paste(overview,(1510,194))
    d = ImageDraw.Draw(canvas)
    f = ow/original.width
    d.rectangle((1510+x*f,194+y*f,1510+(x+w)*f,194+(y+h)*f),outline='#ffb531',width=3)
    d.text((1510,194+oh+16),'Khung vàng = vùng đang phóng',font=font(17),fill='#ffcf7c')
    sy = max(490,194+oh+65)
    for note in scene['notes']:
        if len(note)>35 and re.fullmatch('[0-9a-f]{40}',note):
            note=note[:12]+'…'+note[-8:]
        for line in wrap(note.replace('→',' > '),font(23),370):
            d.text((1510,sy),line,font=font(23),fill='#e1e8f4')
            sy+=32
        sy+=21
    assert sy < 887,(scene['title'],sy)
    d.text((38,888),f'BẰNG CHỨNG {scene["evidence_id"]}  |  Khung {scene_number:02}/18  |  Chú thích dựng nằm ngoài ảnh sản phẩm',font=font(16),fill='#8d9db4')
    d.rounded_rectangle((35,917,1885,1055),radius=12,fill='#101318',outline='#34425a',width=1)
    path=WORK/f'scene-{scene_number:02}-view-{view_number}.png'
    canvas.save(path)
    return path


def docs(timeline):
    cues=[c for t in timeline for c in t['cues']]
    (VIDEO/'subtitles-vi.srt').write_text(''.join(
        f'{i}\n{stamp(c["start"])} --> {stamp(c["end"])}\n'+ '\n'.join(c['lines'])+'\n\n'
        for i,c in enumerate(cues,1)))
    ass_file(VIDEO/'source/subtitles-vi.ass',cues)
    narration=['# Lời thuyết minh tiếng Việt\n\nGiọng tổng hợp cục bộ: Piper / vi_VN-vais1000-medium. '
               'Mỗi đoạn phụ đề gắn với đúng WAV đã tổng hợp; không gửi lời dẫn hay ảnh tới TTS bên ngoài. '
               'Chính tả sản phẩm và ID giữ trong phụ đề; đầu vào đọc dùng bảng phát âm trong render.py.\n\n']
    storyboard=['# Storyboard thực nghiệm\n\n18 ảnh gốc đã kiểm tra SHA-256 với evidence-index.csv. '
                'Dựng 1920×1080, 30 fps; khung phóng giữ tỷ lệ, luôn kèm toàn cảnh gốc và khung vàng chỉ ROI. '
                'Zoom/pan tối đa 0,8%; cắt cảnh sạch, không giả click/typing hoặc tiến độ triển khai. '
                'Phụ đề tối đa hai dòng trong dải riêng bên dưới, không che ảnh bằng chứng.\n\n'
                '| Cảnh / thời gian | Nền tảng / ảnh | Luận điểm / vùng phóng (x,y,w,h) |\n| --- | --- | --- |\n']
    chapters=[]
    ffmeta=[';FFMETADATA1\ntitle=Bytebase demo lab — bằng chứng thực nghiệm\ncomment=Vietnamese local synthetic narration; original screenshot evidence; no live-operation simulation\n']
    for item in timeline:
        s=item['scene'];n=item['number'];start=item['start'];end=item['end']
        time=f'{int(start)//60:02}:{int(start)%60:02}'
        chapters.append(time+' '+s['title'])
        narration.append(f'## {n:02} · {time} · {s["title"]}\n\nẢnh gốc: [{s["image"]}](../{s["image"]}).\n\n'+'\n\n'.join(s['cues'])+'\n\n')
        storyboard.append(f'| {n:02} · {stamp(start)}–{stamp(end)} | {s["platform"]} · [{s["evidence_id"]}](../{s["image"]}) | {s["tag"]}; ROI: '+str([v['roi'] for v in s['views']])+' |\n')
        ffmeta.append(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(start*1000)}\nEND={round(end*1000)}\ntitle={s["title"]}\n')
    narration.append('Bytebase/Jenkins/Oracle dùng bộ phát âm của Piper; GitHub dùng “Ghít Hắp”, SQL dùng “ét kiu eo”, PR dùng “pi a”. Số quan trọng được viết thành chữ trong lời đọc. Phụ đề giữ tên sản phẩm; không giả giọng người thật.\n')
    (VIDEO/'narration-vi.md').write_text(''.join(narration))
    (VIDEO/'storyboard.md').write_text(''.join(storyboard))
    (VIDEO/'chapters.txt').write_text('\n'.join(chapters)+'\n')
    (WORK/'chapters.ffmeta').write_text(''.join(ffmeta))


def render_part(job):
    image,path,frames,ass=job
    n=max(1,frames-1)
    vf=(f"zoompan=z='1+0.008*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':"
        f"d={frames}:s=1920x1080:fps=30,ass=filename='{ass}':fontsdir='{VIDEO/'assets'}'")
    command([FF,'-hide_banner','-loglevel','error','-y','-i',image,
             '-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264',
             '-preset','medium','-crf','18','-pix_fmt','yuv420p','-profile:v','high',
             '-level','4.1','-threads','4','-filter_threads','1',path],path.with_suffix('.log'))
    print('RENDERED',path.name,f'{frames/FPS:.2f}s',flush=True)
    return path


def render(timeline,sample=False):
    selected=timeline[:2] if sample else timeline
    jobs=[]
    for item in selected:
        s=item['scene'];cues=item['cues'];views=s['views'];n=item['number']
        boundaries=[0]+[round(cues[v['at_cue']]['local_start']*FPS) for v in views[1:]]+[item['frames']]
        for vi,view in enumerate(views):
            a,b=boundaries[vi],boundaries[vi+1]
            png=make_canvas(s,n,vi,view['roi'])
            sub=WORK/f'scene-{n:02}-view-{vi}.ass'
            current=[c for c in cues if c['end']>item['start']+a/FPS and c['start']<item['start']+b/FPS]
            ass_file(sub,current,item['start']+a/FPS)
            jobs.append((png,WORK/f'part-{n:02}-{vi}.mp4',b-a,sub))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(render_part,jobs))
    concat=WORK/'parts.txt'
    concat.write_text(''.join(f"file '{p}'\n" for _,p,_,_ in jobs))
    duration=selected[-1]['end']
    dest=VIDEO/'sample/sample-with-voiceover.mp4' if sample else VIDEO/'bytebase-demo-vi.mp4'
    dest.parent.mkdir(exist_ok=True)
    command([FF,'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',concat,
             '-i',VIDEO/'voiceover-vi.wav','-f','ffmetadata','-i',WORK/'chapters.ffmeta',
             '-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','-1' if sample else '2',
             '-c:v','copy','-c:a','aac','-b:a','160k','-t',f'{duration:.6f}',
             '-movflags','+faststart',dest])
    if sample:
        command([FF,'-hide_banner','-loglevel','error','-y','-ss','4','-i',dest,
                 '-frames:v','1',VIDEO/'sample/sample-frame.png'])
    print('VIDEO_COMPLETE',dest,f'{duration:.3f}s',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample',action='store_true',help='Render two initial scenes for QA before full render')
    parser.add_argument('--reuse-audio',action='store_true',help='Use timeline and WAV already generated from this config')
    args=parser.parse_args()
    print('ORIGINAL_FILES_VERIFIED',verify_originals(),flush=True)
    timeline=json.loads((VIDEO/'source/timeline.json').read_text()) if args.reuse_audio else make_audio()
    if args.reuse_audio:
        assert [t['scene'] for t in timeline]==PROJECT['scenes'],'Config changed: regenerate audio/timeline'
    docs(timeline)
    render(timeline,sample=args.sample)
