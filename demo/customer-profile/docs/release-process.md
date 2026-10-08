# Quy trình phát hành

## PR và chuẩn bị release

PR chạy `db-validate`, kiểm tra cả ba release và đóng gói fixture reports; `db-report` chạy fixture smoke. Đây không phải runtime. Validation kiểm tra manifest, thứ tự migration, hash, policy SQL và contract cố định; lexical findings không phải Oracle parser và không thay thế OWNER/DBA review. Source release phải commit mới được đóng gói.

Live workflow `db-release` chỉ dispatch từ `refs/heads/main`, với input `release_id` và `operation`: `prepare`, `create_odc_change` hoặc `collect_status`. Cần protected GitHub environment `odc-demo`; authorized operator cấu hình deployment branches và reviewers. Workflow phải ở main trước khi dispatch live. `collect_status` tự tải handoff artifact mới nhất còn hạn cho đúng release và commit; workflow không nhận ticket ID. Bundle gồm SQL theo thứ tự, manifest, policy, target configs, validation report và `release-envelope.json`; thay source tạo release mới.

## Các module CLI

Chạy từ root repository với Python 3.11+ và `PyYAML==6.0.3`:

```bash
python3 -m scripts.db_demo.validate_manifest --output /tmp/db-demo-validation [--base SHA --head SHA]
python3 -m scripts.db_demo.build_release --release-id RID --output /tmp/db-demo-release
python3 -m scripts.db_demo.odc_client --operation create_odc_change --bundle /tmp/db-demo-release --output /tmp/db-demo-odc
python3 -m scripts.db_demo.odc_client --operation collect_status --bundle /tmp/db-demo-release --output /tmp/db-demo-odc --ticket-id 12345
python3 -m scripts.db_demo.collect_evidence --bundle /tmp/db-demo-release --source LIVE --output /tmp/db-demo-evidence.json [--receipt PATH] [--verification PATH]
python3 -m scripts.db_demo.generate_report --evidence /tmp/db-demo-evidence.json --output /tmp/db-demo-report
python3 -m scripts.db_demo.verify_oracle --bundle /tmp/db-demo-release --source FIXTURE --input PATH --output PATH
python3 -m scripts.db_demo.verify_oracle --bundle /tmp/db-demo-release --source LIVE --receipt PATH --output PATH
```

`RID` là release ID; SHA trong diff validation là hai commit SHA đầy đủ. Local `odc_client collect_status` cần ticket ID số có sẵn; workflow thay vào đó tải handoff artifact mới nhất còn hạn khớp chính xác release và commit. Payload bytes xác định bởi commit; run actor/ID provenance thay đổi theo run. `created_at` lấy từ timestamp commit, không đo thời gian tạo release. Output path quản lý theo lần chạy. Live cần secrets `ODC_BASE_URL`, `ODC_USERNAME`, `ODC_PASSWORD`, runner `self-hosted` với label `linux`, `odc-demo`, protected environment đã cấu hình và `openssl`. Không có password database.

Evidence dùng `FIXTURE` cho dữ liệu mẫu đã sanitize, `LIVE` cho receipt của lần chạy thực, hoặc `NOT_AVAILABLE` khi chưa có receipt. `verify_oracle` nhận input mẫu với `--source FIXTURE`; live verification tiêu thụ receipt `--source LIVE`, không kết nối DB trực tiếp. Dùng report mẫu để xem dạng trình bày: `reports/sample-migration-report.md` và `.json`.

## Approval và tiếp tục thủ công

Sau khi change được tạo, OWNER và DBA xem xét SQL, policy finding, target, hash và rollout trong ODC. Họ approve theo quy trình ODC; operator được ủy quyền tiếp tục từng stage bằng UI. Client không có approve/execute. ODC dùng `MULTIPLE_ASYNC`, singleton, `ABORT`, retry 0; operator có thể cần hủy batch còn chờ sau failure trước batch correction. Khi create trả lỗi/timeout, inspect ODC trước; không retry POST mù vì ticket có thể đã tạo. Cùng release ID không đảm bảo migration replay an toàn.

Status/audit có giới hạn: native flow `createTime` là lúc tạo flow, không phải execution start thực. Audit có thể chỉ thấy phạm vi cá nhân account hiện tại; event `create` có thể không có task ID. Không suy ra actor thực thi từ requester/node operator nếu audit chưa chứng minh.

## Điều kiện báo cáo thành công

Report ghi rõ source evidence và native status. `LIVE` chỉ được ghi khi có receipt của run thực; fixture không được nâng thành live. Verification phải xác nhận object tồn tại và hợp lệ, không có compile errors, bảng có ba dòng (hai dòng active), và function `DM_CP_LABEL('C0001')` trả `C0001:Demo Customer One`. Native status thành công riêng lẻ không đủ để kết luận migration hợp lệ.

Hai mode phù hợp là ODC-led manual execution và version-disciplined Git + ODC với reviewed applied-release references. Mode sau không thêm Flyway executor/bridge. ODC có thể gom thao tác DBeaver, target, approval, rollout và logs; vẫn cần Git, Oracle DBA, backup, schema design, version ledger và recovery. Trước pilot, áp dụng GitOps retention recommendation và xác minh ODC/MetaDB giữ result, log, ZIP, metadata và audit; lab hiện ở baseline.
