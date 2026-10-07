# Kết luận T00–T04

**Chưa có ứng viên OSS miễn phí được chứng minh thay toàn bộ Bytebase cho migration Oracle và governance.**

[Shortlist](shortlist.md) giữ ODC, CloudDM và AccessFlow cho platform POC, cùng Archery cho SQL governance.
Bytebase là đối chứng có edition gates. Engine/UI và sản phẩm thương mại được tách trong [register](candidates.csv).
Không chọn người thắng bằng cách giảm P0 hoặc đổi acceptance.

## Coverage và giới hạn

T00/T01 tạo context và 45 expected nguyên văn, thêm F01–F12.
T02 kết hợp danh mục cũ với tìm kiếm mới có log. Không tuyên bố đã tìm mọi tool hoặc fork.
T03 review sâu ba ứng viên mới/cần kiểm và hai đối chứng, có review chéo source/license.
T04 chốt shortlist, SQL workload manifest và benchmark spec. Runtime mới toàn bộ NOT_RUN.

Bằng chứng lịch sử: ODC 12 PASS/20 PARTIAL/5 FAIL/8 NOT_RUN; Bytebase 17 PASS/14 PARTIAL/4 FAIL/3 BLOCKED/7 NOT_RUN.
Cả hai chỉ trên Oracle 26ai 23.26.4.1.0 và các schema mô phỏng cùng instance.
Không dùng source claim hoặc số PASS để xếp hạng production hoặc tốc độ.
[Hash preservation](preserved-evidence.json) giữ tài liệu/JSON gốc. Không ghi đè bằng chứng cũ.

## Khuyến nghị theo nhu cầu

Quản lý DB tập trung: kiểm CloudDM inventory/env/resource permissions và AccessFlow native schema-change ladder.
ODC có bằng chứng project/Oracle runtime, nhưng cần sửa state, dedup, compile và requester separation.

Migration Oracle: chưa có platform đạt toàn bộ P0.
Bytebase có replay/version đã kiểm tốt hơn ODC, nhưng strict checksum, compile và promotion còn FAIL.
AccessFlow release gate không phù hợp DML bắt buộc đã biết. Không thay bằng raw query để đạt release criterion.
CloudDM chưa có source trace đủ cho parser/ledger/recovery. Archery là ticket executor, chưa là versioned migration platform.

Governance miễn phí: ODC và Archery đáng kiểm theo workflow native.
AccessFlow có approval plan/promotion source. CloudDM có approval ticket/locked attachment source.
Các ca negative enforcement, artifact/target binding và role separation vẫn phải chạy.
FREE Bytebase không đáp ứng approval/audit yêu cầu hiện tại.

Hiệu năng: chỉ có [spec](benchmark-spec.md), [config](benchmark-config.json) và [SQL hashes](workloads/manifest.json).
Chưa có raw sample hoặc benchmark tương đương. Không xếp tốc độ hoặc tính điểm tổng.

## License gates và chi phí

Repo Apache/MIT không xác nhận mọi image, driver, plugin hoặc dependency.
CloudDM current image/free entitlement chưa rõ. Không dùng cache pricing cũ để kết luận cap hiện tại.
AccessFlow driver tải riêng. Archery Oracle client/external tools cần license review.
ODC frontend/backend Apache riêng với MetaDB/driver/wrapper. Bytebase Enterprise/enablement có phạm vi riêng.
Liquibase 5.x FSL, Atlas Oracle Pro, SQLE/DMS release Enterprise và NineData source gap loại khỏi đáp án OSS chính.

Chưa có dự toán tiền hoặc thời gian kỹ thuật đáng tin cậy.
T05 phải ghi hạ tầng, license hợp lệ, support, vận hành, backup và công sức adapter riêng.
Không xem chi phí license source bằng không là tổng chi phí bằng không.

## Điểm chặn và bước tiếp

P0 lịch sử ODC: false success khi INVALID; replay/checksum/dedup và requester separation FAIL.
P0 lịch sử Bytebase: INVALID, strict checksum, early promotion; P04 enforcement FAIL bổ sung.
Approval/audit trên FREE bị license gate. Enterprise chưa được POC.
Recovery/fencing/restore, real GitLab/Jenkins, Oracle 19c/21c và benchmark còn chưa kiểm.

Tiếp tục T05→T06/T07→T08 sau khi phạm vi target/quota được xác định.
T09 chỉ đo workload đúng, cùng hash/fixture/resources, tuần tự trên shared Oracle.
T10 cần target và fault checkpoint riêng. Xem task acceptance tại [shortlist](shortlist.md).
