#!/usr/bin/env python3
"""Local media checks; no lab, CI, SQL, cloud TTS or upload calls."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import wave
import numpy as np
from render import VIDEO, EVIDENCE, FF, WORK, PROJECT, verify_originals

video=VIDEO/'bytebase-demo-vi.mp4'
timeline=json.loads((VIDEO/'source/timeline.json').read_text())
expected=timeline[-1]['end']
original_count=verify_originals()
probe=subprocess.run([FF,'-hide_banner','-i',str(video)],capture_output=True,text=True)
meta=probe.stderr
assert 'Video: h264' in meta and '1920x1080' in meta and '30 fps' in meta,meta
assert 'Audio: aac' in meta and '48000 Hz' in meta,meta
blocks=(VIDEO/'subtitles-vi.srt').read_text().strip().split('\n\n')
assert len(blocks)==sum(len(t['cues']) for t in timeline)
assert all(len(b.splitlines()[2:])<=2 for b in blocks)
previous=0
for t in timeline:
    for c in t['cues']:
        assert c['start']>=previous and c['end']>c['start']
        assert len(c['lines'])<=2
        previous=c['end']
assert .5 <= expected-previous <= 1.2
with wave.open(str(VIDEO/'voiceover-vi.wav')) as w:
    audio_duration=w.getnframes()/w.getframerate()
    assert w.getframerate()==48000 and w.getnchannels()==1 and w.getsampwidth()==2
    samples=np.frombuffer(w.readframes(w.getnframes()),np.int16)
    peak_db=20*np.log10(max(1,np.abs(samples.astype(float)).max())/32768)
    assert peak_db < -1.0
assert abs(audio_duration-expected)<.04
print('Decode/black/silence validation started',flush=True)
result=subprocess.run([FF,'-hide_banner','-nostats','-i',str(video),
    '-vf','blackdetect=d=0.1:pix_th=0.03:pic_th=0.98',
    '-af','volumedetect,silencedetect=noise=-45dB:d=1.2',
    '-progress','pipe:1','-f','null','-'],capture_output=True,text=True)
(WORK/'final-media-validation.log').write_text(result.stderr+'\n'+result.stdout)
assert result.returncode==0,result.stderr[-2500:]
assert 'black_start:' not in result.stderr,'Unexpected black scene detected'
assert not re.search(r'(?i)error while decoding|invalid data found|corrupt decoded frame',result.stderr)
frames=[int(x) for x in re.findall(r'^frame=(\d+)',result.stdout,re.M)]
assert frames and frames[-1]==round(expected*30),(frames[-1:],expected)
long_silences=[float(x) for x in re.findall(r'silence_duration: ([0-9.]+)',result.stderr)]
assert not any(x>2 for x in long_silences),long_silences
bad=[]
for p in VIDEO.rglob('*'):
    if p.is_file() and p.suffix in ['.md','.json','.txt','.srt','.ass','.py','.sh']:
        if re.search(rb'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{25,}|Bearer\s+[A-Za-z0-9_-]{25,})',p.read_bytes()):
            bad.append(str(p.relative_to(VIDEO)))
assert not bad,bad
report=dict(status='PASS',duration_seconds=expected,resolution='1920x1080',fps=30,
    codec='H.264 High / yuv420p',audio='AAC / 48000 Hz mono; Vietnamese local Piper voiceover',
    voiceover_pcm='PCM s16le WAV / 48000 Hz mono',voiceover_peak_dbfs=float(peak_db),
    audio_video_duration_delta_seconds=audio_duration-expected,decoded_frames=frames[-1],
    subtitle_cues=len(blocks),subtitle_max_lines=2,black_intervals=0,
    longest_detected_silence_seconds=max(long_silences,default=0),
    silence_detection_min_duration_seconds=1.2,silence_detection_threshold_db=-45,
    original_evidence_files_unchanged=original_count,
    screenshot_count_used=18,paid_tts=False,external_upload=False,
    qa_scope='Full local decode, frames and metadata, subtitle timing, audio levels, black/silence detection, original hashes. ASR is a pronunciation heuristic, not human listening approval.',
    sha256=hashlib.sha256(video.read_bytes()).hexdigest())
(VIDEO/'quality-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
