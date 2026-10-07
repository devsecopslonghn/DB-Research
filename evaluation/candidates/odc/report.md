# ODC: báo cáo T03

**Cập nhật nghiên cứu sâu 2026-10-04:** đọc [source trace mới](../../research-round-2/coordinator/oracle-governance-source.md), [license/release](../../research-round-2/licensing/licensing-review.md) và [shortlist hiện tại](../../shortlist.md). Phần dưới giữ snapshot T03 đầu; kết luận mới được ghi riêng, runtime mới vẫn NOT_RUN.

**Giữ ODC trong shortlist POC platform OSS. Chưa đạt migration Oracle production.**

ODC có project, inventory, environment, approval và native batch model.
Bằng chứng SOURCE/DOC nằm tại [source-review.md](source-review.md).
Bằng chứng runtime lịch sử giữ ở [45 ca gốc](../../../ODC-ORACLE-POC-RESULTS.md).
[Cases mapping](cases.json) giữ historical status riêng và new_status=NOT_RUN.

Build lịch sử 4.4.1-20260116 trên Oracle 26ai đạt 12 PASS, 20 PARTIAL, 5 FAIL, 8 NOT_RUN.
SQL-11, replay, checksum, request dedup và requester separation còn FAIL.
Ordered promotion bằng runner ngoài chưa nghiệm thu native batch.
Log/attachment sau restart còn gap, cần kiểm F09 thay vì suy ra audit bền vững.

Backend/frontend dùng Apache-2.0. MetaDB, Oracle driver, image và wrapper có phạm vi license riêng.
Không có benchmark tương đương hoặc nghiệm thu Oracle 19c/21c.
T07/T08 phải xử lý P0 trước T09. Không ghép Flyway để tự biến native gaps thành PASS.
