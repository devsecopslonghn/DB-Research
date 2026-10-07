# Bytebase: báo cáo đối chứng T03

**Giữ Bytebase làm đối chứng mô hình và migration version. FREE chưa đạt yêu cầu governance.**

[Source/license review](source-review.md) kiểm đúng commit runtime 3.22.1.
[45 kết quả lịch sử](../../../BYTEBASE-ORACLE-POC-RESULTS.md) giữ 17 PASS, 14 PARTIAL, 4 FAIL, 3 BLOCKED, 7 NOT_RUN.
[Cases mapping](cases.json) tách historical status và new_status=NOT_RUN.

Native version/revision/replay có bằng chứng tốt hơn ODC đã thử.
Chưa có target ledger được chứng minh. REC-08 strict checksum, SQL-11 INVALID và promotion còn FAIL.
P04 SQL Review enforcement là FAIL bổ sung ngoài 45 ca. Giữ P03/P04 lịch sử.
FREE không có approval và audit cần thiết. License repository chỉ MIT subset, Enterprise có điều kiện riêng.

T07/T08 cần tái kiểm lỗi P0 trên build/policy dự kiến dùng.
Edition có license hợp lệ chỉ giải quyết quyền dùng feature, không chứng minh correctness.
Chưa có benchmark chung hoặc kết quả Oracle 19c/21c. Không xếp tốc độ.
