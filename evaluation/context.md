# Context T00–T04

Ngày: 2026-10-04. Coordinator: /root.

## Phạm vi và quyền

User cho phép đọc nguồn, tìm trên mạng, ghi tài liệu và dùng agent song song.
Lượt này thực hiện T00–T04. Không triển khai, chạy test, SQL, benchmark hoặc khởi động dịch vụ.
Không đọc credential. Không kiểm kết nối hoặc quyền target bằng runtime.
Resource ceiling cho tải và deployment lượt này: 0.
Oracle 26ai 23.26.4.1.0 là đối chứng lịch sử. Oracle 19c/21c chưa được kiểm.
Bốn schema trên một instance không chứng minh cách ly môi trường vật lý.

## Checklist nghiệm thu

1. Giữ nguyên expected của 45 ca gốc, thêm F01–F12 và ghi mapping.
2. Tìm rộng ít nhất hai vòng, ghi truy vấn, thời điểm, phạm vi và giới hạn.
3. Tách A/B/C/D, native/adapter, source license/image/plugin/driver và miễn phí/trial.
4. Ghi source theo commit và dòng. Không coi DOC/SOURCE là runtime PASS.
5. Review chéo trước khi chốt tối đa năm ứng viên OSS để nghiên cứu tiếp.
6. Chốt workload, cách đo, điều kiện dừng và các điều kiện T05/T09 còn thiếu.
7. Giữ hash bằng chứng Bytebase/ODC, cập nhật index và báo công việc chưa chạy.

## Tiêu chí đóng băng

`criteria.csv` chứa 45 expected nguyên văn và 12 nhóm bổ sung.
`poc/ORACLE-POC.md` là nguồn authoritative cho 45 ca.
`poc/PLATFORM-EVALUATION-PLAN.md` là nguồn authoritative cho F01–F12.
P0 không được hạ để tạo người thắng. Thiếu ledger giảm migration fit, vẫn giữ nghiên cứu platform fit.
Shortlist nghiên cứu không đồng nghĩa shortlist đạt toàn bộ hard requirements.
Trọng số giữ 25/30/15/10/5/10/5 theo kế hoạch. Chưa tính điểm vì coverage khác nhau và chưa có SLA.
MODEL-07/GOV-04 có trùng bằng chứng promotion. Không đếm hai lần.
P04 SQL Review enforcement là lỗi bổ sung, ngoài 45 ca. Giữ P03/P04 lịch sử.

## Ownership và dependency

Coordinator giữ context, criteria, register chung, shortlist, benchmark và index.
Worker search ghi `candidates/discovery/`, không sửa register chung.
Worker CloudDM ghi `candidates/clouddm/`.
Worker AccessFlow/Archery ghi các thư mục riêng cho hai tool.
T02 dựa T01. T03 bắt đầu với ứng viên seed đã đăng ký, bổ sung theo kết quả T02.
Worker CloudDM và AccessFlow/Archery review chéo khi hoàn thành.
Coordinator kiểm nguồn quan trọng và quyết định cuối.

## Gap tài liệu và môi trường

DB-Research không phải Git repository. Không có AGENTS.md cục bộ được tìm thấy.
Áp dụng hướng dẫn AGENTS.md user cung cấp. `README.md` là documentation index hiện có.
Chưa có architecture/schema chung. Dùng guide và source từng tool, không tạo schema giả.
Tập đọc mở rộng khỏi mục tiêu 5.000 token để lấy expected nguyên văn và nguồn license mâu thuẫn.
Không xác minh trực tiếp target, quota host, credential, image digest hoặc giấy phép driver.
`preserved-evidence.json` lưu SHA-256 tài liệu và JSON lịch sử để so sánh cuối lượt.
