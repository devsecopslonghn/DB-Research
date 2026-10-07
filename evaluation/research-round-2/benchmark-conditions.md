# Điều kiện benchmark bổ sung từ source/license review

**Chưa đủ điều kiện xếp hạng hiệu năng.** Không có runtime hoặc raw sample mới.
[Spec](../benchmark-spec.md), [config](../benchmark-config.json) và [workload](../workloads/manifest.json) giữ nguyên hash.
Tài liệu này ghi dependency và capability gates. Nó không đổi tiêu chí hoặc SQL bytes.

| Điều kiện | Quyết định cho T09 |
| --- | --- |
| CloudDM indexed pricing nêu 10 instances/5 accounts, nhưng direct GET trả trang khác | Giữ DOC và disagreement. Pin current entitlement trên artifact. Onboarding là 50 target logic. Ghi mapping target→datasource/instance được license đếm. Cell 50 BLOCKED nếu cap thực tế chặn mapping native đó. Không tự coi 50 schema là 50 physical instances. Không chia estate hoặc gộp target nhân tạo để lách cap. Không thay workload 50 thành 10 rồi gọi đạt. |
| AccessFlow release gate từ chối DML/BEGIN/internal semicolon | PERF-03 native common release không eligible theo source reviewed. Ghi capability gap; runtime NOT_RUN cho đến confirm. Không dùng raw query làm substitute. |
| Archery INVALID check lấy một hàng owner/name, không OBJECT_TYPE | Đạt SQL-11 bằng hậu kiểm spec/body và ALL_ERRORS trước throughput migration. SOURCE check không là runtime correctness PASS. |
| CloudDM optional compile mode, ODC warning mode, Bytebase central record | Compile validation, replay/hash và partial/uncertain P0 phải qua T07/T08. Download MD5, delivery receipt hoặc central state không tự chứng minh target correctness. |
| Oracle Instant Client nằm trong selected path/image | Pin exact terms và Thin/Thick mode. Điều khoản [Instant Client](https://www.oracle.com/downloads/licenses/instant-client-lic.html) yêu cầu prior consent cho disclosure kết quả benchmark của chương trình. Kiểm phạm vi áp dụng trước chia sẻ ngoài nhóm. Không mở rộng kết luận sang mọi platform benchmark. |
| Release archive SHA khác OCI digest | Thu cả hai nếu có. Manifest/config metadata không chứng nhận SBOM, driver contents hoặc source-image reproducibility. |
| Approval không được cấp entitlement | Full-workflow time = null/BLOCKED, không bằng 0. Ghi executor-only path riêng. |
| Chưa xác nhận quota/SLA/Oracle version | Không dùng proposed 4 vCPU/8 GiB/20 GiB/16 sessions làm quota thực tế. Không tính performance score khi SLA null. |

Chạy từng tool tuần tự trên shared Oracle. Tính tài nguyên metadata DB, worker, proxy và executor trong total budget.
Chỉ throughput có hậu kiểm đúng được tính successful throughput. Fixed attempts giữ mọi lỗi, không chạy bù đến đủ success.
Pin release ID/version, route, pool global/per-target, observer, retry/timeouts, clock, reset và snapshot trước lượt đầu.
Unknown/partial target phải được reconcile trước reset hoặc retry. Không xóa evidence để làm lượt kế tiếp sạch.
API p95 chỉ dùng đúng sample cell/round. UI/migration có ít sample thì báo raw/median/min/max và error count.
Không gộp native/adapter/direct-client thành một ranking. Lỗi P0 chặn kết luận production-ready.
