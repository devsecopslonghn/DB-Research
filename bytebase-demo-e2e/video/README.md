# Video Bytebase bằng chứng thực nghiệm

Mở `bytebase-demo-vi.mp4` — **04:38**, 1920×1080, 30 fps, H.264/AAC; 61 đoạn phụ đề. Kiểm tra cuối: giải mã đủ 8.344 frame, không phát hiện cảnh đen, hình và WAV cùng thời lượng. Đây là phim trình bày từ 18 screenshot đã lưu, có giọng tổng hợp tiếng Việt cục bộ và phụ đề đốt trong hình. Không phải bản quay thao tác trực tiếp. Không chạy lại Git/Jenkins/Bytebase/SQL để dựng; không dùng Flow, Stitch hoặc AI sinh giao diện.

- `voiceover-vi.wav`: bản thuyết minh riêng, PCM 16-bit / 48 kHz / mono.
- `subtitles-vi.srt`: phụ đề rời; bản MP4 đã có phụ đề trên dải riêng, tối đa hai dòng.
- `narration-vi.md`, `storyboard.md`, `chapters.txt`: lời đọc, ảnh/ROI và timing thực tế.
- `source/project.json`: 18 ảnh, hash gốc, caption, ROI, lời dẫn, mô hình giọng và cấu hình.
- `source/timeline.json`: thời điểm từng câu, chữ phụ đề và đầu vào phát âm TTS tương ứng.
- `quality-check.json`: kết quả kiểm tra media cuối.
- `sample/sample-with-voiceover.mp4`: đoạn mẫu đã dùng để kiểm tra trước render toàn bộ.

## Chạy lại

Từ thư mục `video/`:

```bash
# Dựng lại bằng WAV/timeline đã bàn giao, không cần tổng hợp giọng lại.
bash source/render.sh --reuse-audio

# Hoặc dựng thử hai cảnh đầu với cùng WAV.
bash source/render.sh --sample --reuse-audio

# Tổng hợp lại tiếng Việt cục bộ rồi dựng toàn bộ.
bash source/render.sh

# Kiểm tra file cuối, dùng cùng venv ở cache.
~/.cache/bytebase-video-tools/venv/bin/python source/validate.py
```

Python 3.12; dependency pin trong `source/requirements.txt`. Lần setup cần tải wheel công cụ. Nếu tổng hợp giọng mới và cache trống, script tải mô hình ONNX cùng config theo revision đã pin, kiểm tra SHA-256 trước dùng. FFmpeg 7.0.2 đi kèm imageio-ffmpeg 0.6.0. Công cụ, model và video trung gian nằm tại `${XDG_CACHE_HOME:-~/.cache}/bytebase-video-tools/`, không nằm trong bộ ảnh gốc. Có thể đặt `FFMPEG_BINARY` để dùng binary tương thích khác.

`--reuse-audio` dùng đúng WAV và timeline bàn giao. Tổng hợp mới có thể có biến thiên nhỏ do TTS; timing và phụ đề sẽ được sinh lại từ từng đoạn WAV thực tế, không cắt câu theo thời gian ước lượng. Nếu sửa config, bỏ `--reuse-audio`. Script từ chối input gốc thay hash, phụ đề quá hai dòng hoặc thời lượng ngoài 3–5 phút.

Mọi xử lý ảnh, TTS, nhận dạng thử và render đều chạy trên máy. Network chỉ dùng tải bản lưu/công cụ/model công khai; không gửi lời dẫn hoặc screenshot tới dịch vụ ngoài, không có TTS trả phí. Không lấy credential, cookie hoặc browser auth state để làm phim.

## Giữ nguyên giới hạn bằng chứng

PR #9 có **0 ERROR, 3 WARNING**; master #12 tự rollout develop sau merge; chưa chứng minh approval độc lập. Plan/task mới là 114, task run 113; không ghép Plan 113 cũ. Query bảng POC mới trả count 0. PR #10 có ERROR thiếu PK, CI thất bại, nhưng Git master chưa có required checks cưỡng chế chặn merge. Task history không tương đương Audit Log đầy đủ; chưa thử user ít quyền hoặc Flyway. Xem [results.md](../results.md).

Giọng là Piper tổng hợp một speaker tiếng Việt, không giả giọng cá nhân. Phát âm đã thử nhiều cách đầu vào và đối chiếu bằng nhận dạng giọng nói cục bộ; ASR vẫn có thể nhầm tên riêng. Kiểm tra tự động và xem frame không thay cho duyệt nghe thủ công bởi người Việt. Không tuyên bố đã có một lượt nghe duyệt của con người.

## Nguồn và ghi công

- 57 file bằng chứng khôi phục từ [DB-Research, commit 2a6e13489d875a8547d1ee29dd4aa665f0e2ee62](https://github.com/devsecopslonghn/DB-Research/tree/2a6e13489d875a8547d1ee29dd4aa665f0e2ee62/bytebase-demo-e2e). Hash trước dựng lưu trong `source/evidence-original-sha256.json`; toàn bộ giữ nguyên.
- TTS: [OHF-Voice Piper](https://github.com/OHF-Voice/piper1-gpl), engine 1.8.0, GPL-3.0; cài ở cache, không đóng gói binary vào video source.
- Giọng: [rhasspy/piper-voices — vi_VN-vais1000-medium](https://huggingface.co/rhasspy/piper-voices/tree/0c9c5d340496a47205a799eb046aab69334a88e9/vi/vi_VN/vais1000/medium). `assets/voice-MODEL_CARD.txt` ghi một speaker / 22050 Hz, dataset [VAIS-1000](https://ieee-dataport.org/documents/vais-1000-vietnamese-speech-synthesis-corpus), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Mô hình fine-tune từ lessac medium; không sửa model, dùng để tổng hợp lời dẫn mới.
- Font: Noto Sans Variable, Google/Noto contributors, SIL Open Font License; file license kèm `assets/Noto-LICENSE.txt`.
- Render: [FFmpeg](https://ffmpeg.org/) và [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg). Không phân phối lại binary FFmpeg trong thư mục này.
