# Đánh giá ứng viên Archery

**Cập nhật nghiên cứu sâu 2026-10-04:** đọc [source trace mới](../../research-round-2/coordinator/oracle-governance-source.md), [license/release](../../research-round-2/licensing/licensing-review.md) và [shortlist hiện tại](../../shortlist.md). Phần dưới giữ snapshot T03 đầu; kết luận mới được ghi riêng, runtime mới vẫn NOT_RUN.

Trạng thái: ứng viên đáng xem xét cho governance SQL và vận hành DB; chưa đủ bằng chứng để xem là nền tảng migration Oracle thay Bytebase. Commit `ccc7134f48d0e261f9e3ffa0d445dcec48adb790` khớp remote HEAD ngày 2026-10-04.

Archery kết hợp inventory instance, query access, SQL review ticket, approval, execution và công cụ vận hành. README công bố Oracle query/review/execute cùng một số chức năng quản trị, nhưng không có account management và parameter management cho Oracle. Repository Apache-2.0; Oracle client, driver, image và dependency khác cần rà license riêng.

Source cho thấy connector Oracle và controller approval/execution thực sự tồn tại. Tuy nhiên, Oracle executor commit từng câu sau khi tách script. Với PLSQL object có tên, mã kiểm tra trạng thái `INVALID` và có thể đánh dấu execution lỗi. Điều này chưa chứng minh diagnostics đầy đủ hoặc parser đúng với procedure/package. `sqlparse` và delimiter tùy chỉnh cũng chưa xác nhận SQLPlus, slash delimiter và các trường hợp PL/SQL phức tạp.

Permission/resource group của Archery kiểm soát thao tác trên ứng dụng. Chúng không chứng minh ánh xạ Oracle grants/roles hay ngăn truy cập chéo schema. Execution result được lưu ở metadata trung tâm, nhưng source đã rà không cho thấy target-side Oracle migration ledger, checksum version history hoặc environment promotion ladder. Đây là khoảng trống đáng kể với migration release có thể replay.

Đề xuất task kế tiếp: nếu SQL ticket và vận hành Oracle còn hữu ích, làm POC hẹp cho PL/SQL splitting/INVALID handling, tách người duyệt, ràng buộc đúng SQL đã review, Oracle privilege boundary và kết quả sau partial execution. Chưa chấm Archery là migration platform cho tới khi giải quyết được ledger/promotion. Benchmark cần điều kiện chung và tách thời gian queue/review khỏi thời gian SQL thực thi.

Runtime: `NOT_RUN`. Không test, deploy, start service, chạy SQL hoặc thao tác DB. Chi tiết và link bằng chứng tại [source-review.md](source-review.md).
