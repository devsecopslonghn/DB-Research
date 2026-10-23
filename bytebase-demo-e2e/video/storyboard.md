# Storyboard thực nghiệm

18 ảnh gốc đã kiểm tra SHA-256 với evidence-index.csv. Dựng 1920×1080, 30 fps; khung phóng giữ tỷ lệ, luôn kèm toàn cảnh gốc và khung vàng chỉ ROI. Zoom/pan tối đa 0,8%; cắt cảnh sạch, không giả click/typing hoặc tiến độ triển khai. Phụ đề tối đa hai dòng trong dải riêng bên dưới, không che ảnh bằng chứng.

| Cảnh / thời gian | Nền tảng / ảnh | Luận điểm / vùng phóng (x,y,w,h) |
| --- | --- | --- |
| 01 · 00:00:00,000–00:00:11,633 | Bytebase · [07](../screenshots/07-current-community-edition.png) | Community • v3.22.1; ROI: [[215, 58, 440, 88]] |
| 02 · 00:00:11,633–00:00:26,467 | GitHub · [11](../screenshots/11-pr9-reviewed-sql-diff.png) | Source SHA: ecfb13f; ROI: [[448, 470, 1055, 180], [335, 840, 1220, 150]] |
| 03 · 00:00:26,467–00:00:38,033 | Jenkins · [13b](../screenshots/13b-ci-pr9-reviewed-build.png) | PR-9 / build #2 • SUCCESS; ROI: [[360, 0, 1060, 210], [365, 300, 1070, 175]] |
| 04 · 00:00:38,033–00:00:57,733 | Bytebase → Jenkins · [14b](../screenshots/14b-pr9-reviewed-findings.png) | 0 ERROR • 3 WARNING • FAIL_ON_ERROR; ROI: [[0, 90, 1090, 180], [0, 325, 1080, 405]] |
| 05 · 00:00:57,733–00:01:10,333 | GitHub • đầu ra CI · [15b](../screenshots/15b-pr9-bytebase-native-summary.png) | Comment thuộc PR-9 #2; ảnh chụp lại sau merge; ROI: [[248, 98, 816, 447], [245, 570, 830, 425]] |
| 06 · 00:01:10,333–00:01:24,067 | GitHub · [16b](../screenshots/16b-git-reviewed-head-success.png) | ecfb13f • hai status check thành công; ROI: [[478, 422, 648, 180]] |
| 07 · 00:01:24,067–00:01:35,967 | GitHub · [17](../screenshots/17-pr9-merged.png) | Merge SHA: a8267df; ROI: [[185, 195, 1000, 135]] |
| 08 · 00:01:35,967–00:01:48,100 | Jenkins · [18](../screenshots/18-master12-merge-checkout.png) | Build triển khai mới • SUCCESS; ROI: [[360, 0, 1040, 180], [365, 245, 1080, 215]] |
| 09 · 00:01:48,100–00:02:00,933 | Jenkins → Bytebase · [19](../screenshots/19-master12-release-plan-links.png) | master #12 → release_20261022-RC00 → Plan 114; ROI: [[378, 119, 1185, 225], [378, 579, 1180, 240]] |
| 10 · 00:02:00,933–00:02:17,400 | Bytebase · [21](../screenshots/21-bytebase-release-reviewed-sql.png) | V1.0.0.10 • SHA-256 bắt đầu 706ea322; ROI: [[787, 75, 787, 125], [789, 212, 785, 219]] |
| 11 · 00:02:17,400–00:02:34,300 | Bytebase · [22](../screenshots/22-bytebase-new-rollout-done.png) | Plan 114 • task 114 • task run 113; ROI: [[218, 55, 1040, 80], [295, 257, 1233, 215], [307, 685, 1215, 216]] |
| 12 · 00:02:34,300–00:02:54,300 | Oracle • qua Bytebase SQL Editor · [25](../screenshots/25-oracle-new-object-live-query.png) | Truy vấn mới • 14:28:19 GMT+7 • 243 ms; ROI: [[417, 138, 780, 95], [409, 637, 865, 158]] |
| 13 · 00:02:54,300–00:03:08,867 | Bytebase · [28](../screenshots/28-find-new-plan-in-project-history.png) | Project Plans • chọn đúng Plan 114; ROI: [[225, 176, 1170, 90]] |
| 14 · 00:03:08,867–00:03:25,533 | Bytebase · [29](../screenshots/29-reopened-new-plan-history.png) | Tra cứu sau execution • không chạy lại; ROI: [[220, 54, 1060, 77], [309, 685, 1200, 215]] |
| 15 · 00:03:25,533–00:03:42,667 | GitHub · [80](../screenshots/80-pr10-review-only-source.png) | Review-only • không merge, không deploy; ROI: [[420, 350, 975, 145]] |
| 16 · 00:03:42,667–00:04:00,433 | Bytebase → Jenkins · [82b](../screenshots/82b-pr10-missing-pk-final-finding.png) | 1 ERROR • 2 WARNING • PR-10 #2; ROI: [[0, 350, 1080, 184]] |
| 17 · 00:04:00,433–00:04:12,867 | Jenkins · [81](../screenshots/81-pr10-build2-failure.png) | FAILURE • checkout 7433020; ROI: [[360, 0, 1080, 190], [365, 300, 1080, 165]] |
| 18 · 00:04:12,867–00:04:38,133 | GitHub · [84](../screenshots/84-pr10-git-status-failure.png) | Giới hạn bằng chứng • đọc cùng results.md; ROI: [[479, 424, 647, 177]] |
