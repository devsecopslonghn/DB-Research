# Bytebase và ODC: đối chiếu POC Oracle

**Bytebase mạnh hơn ODC ở native version/revision, replay và tách quyền thực thi. Cả hai build đã thử đều chưa đạt yêu cầu production.**

Ngày quan sát: 04/10/2026. ODC 4.4.1 và Bytebase 3.22.1/FREE dùng bộ 45 tiêu chí gốc.
Cả hai dùng schema riêng trên cùng Oracle 26ai. Không dùng kết quả này cho Oracle 19c/21c hoặc mọi edition.

| Kết quả 45 tiêu chí | ODC | Bytebase FREE |
|---|---|---|
| PASS | 12 | 17 |
| PARTIAL | 20 | 14 |
| FAIL | 5 | 4 |
| BLOCKED | 0 | 3 |
| NOT_RUN | 8 | 7 |

Số PASS không phải điểm nghiệm thu tổng thể. MODEL-07/GOV-04 cùng ghi nhận một lỗi promotion của Bytebase.
P04 SQL Review enforcement là ca bổ sung FAIL, ngoài 45 tiêu chí gốc. MODEL-05 chỉ yêu cầu review đúng SQL/target.

| Chức năng | ODC đã thử | Bytebase FREE đã thử | Đánh giá |
|---|---|---|---|
| Project/inventory/environment | Project, datasource, permission grant và environment | Project, project-owned instance/database, environment, IAM | Cả hai có mô hình nền tảng. |
| Kết nối Oracle | Wrapper JDBC TCPS; schema owner giới hạn | TCPS SSL và certificate verification bật; schema owner giới hạn | Có hậu kiểm độc lập. |
| Native release/version | Ticket SQL; chưa có applied-state theo migration version | VERSIONED release, file.version, sheet SHA và central revision | Bytebase rõ hơn cho migration version. |
| Replay thành công | Ticket mới chạy lại SQL; có lỗi hoặc thêm effect | Native version đã áp dụng được skip; target không đổi | Bytebase đạt REC-02. |
| Checksum đổi nội dung | Không có checksum gate; SQL gặp object đã tồn tại | Có WARNING với applied/release SHA; task DONE/skip | Bytebase có detection. Cả hai chưa đạt strict validation-failure criterion. |
| Duplicate execution | Request lặp tạo effect lặp | Cùng task hai request chỉ một taskRun/effect | Bytebase dedup tiểu ca tốt hơn; FREE không có approved execution đầy đủ. |
| Concurrent version | Chưa có lock proof | Hai plan cùng version DONE/DONE, một effect | Bytebase có applied-state; chưa nghiệm thu lock/fencing. |
| Oracle INVALID | Ticket success nhưng procedure INVALID | Task DONE/Deployed nhưng procedure INVALID | Cả hai FAIL SQL-11. |
| SQL Review enforcement | Chưa tái hiện cùng P04 trên ODC | Fresh check ERROR trước issue, executor vẫn chạy DONE | Bytebase P04 FAIL hiện tại, không chỉ lịch sử. |
| Approval | OWNER→DBA trên mockPROD được chạy API/UI | FREE SKIPPED, không có approval template | ODC có workflow approval đã chạy. Bytebase FREE BLOCKED. |
| Requester execute | Được execute sau khi duyệt | Rollout requester/CI bị 403. sqlEditorUser ban đầu vẫn cho UPDATE. Sau thu hẹp sang sqlEditorReadUser, query UPDATE cũng bị chặn. | Bytebase tách rollout role; phải hạn chế quyền SQL console riêng. |
| Environment promotion | Cùng artifact bốn ticket; runner giữ thứ tự; native batch chưa nghiệm thu | Native stage đủ bốn môi trường; server nhận staging trước SIT/UAT | Bytebase GOV-04 FAIL. Không suy ra ODC native batch PASS. |
| Audit | API có audit record; retention/export chưa đủ | Search/export 403 TEAM gate; UI ghi Pro | FREE Bytebase không đủ audit theo yêu cầu. |
| Expiry/read-only | Grant/revoke chạy; expiry boundary chưa kiểm | Conditional grant hết hạn thật; native observer SELECT được, UPDATE bị Oracle từ chối | Bytebase có expiry evidence. READ_ONLY datasource riêng bị TEAM gate. |
| CI/CD | API/CLI cục bộ; thiếu named runner thật | Named service principal, native CLI/API cục bộ | Chưa có job GitLab/Jenkins thật ở cả hai. |
| Recovery/failover/restore | Chưa có controlled fault proof | Chưa có controlled fault proof | Không coi DDL/DML thành công là recovery PASS. |

## Quyết định theo nhu cầu

Nếu ưu tiên migration theo version, tôi chọn Bytebase để đánh giá tiếp. Native release/revision và replay đã có bằng chứng tốt hơn.
Build FREE hiện tại cần xử lý compile gate, SQL Review enforcement và promotion trước khi dùng cho thay đổi quan trọng.
Cần license phù hợp cho approval và audit. POC chưa đánh giá Enterprise nên không kết luận mua license sẽ sửa các lỗi này.

Nếu yêu cầu nền tảng mã nguồn mở miễn phí có approval, ODC là ứng viên tiếp tục POC.
ODC hiện thiếu migration-state và dedup theo yêu cầu, đồng thời chưa chặn requester execute sau duyệt.
Không xem việc dùng ODC API thay CLI là cách tự động giải quyết các thiếu hụt này.

Bước tiếp theo là tái hiện ca FAIL trên build dự kiến dùng, có chính sách và license chính thức.
Sau đó mới nghiệm thu crash giữa commit/revision, fencing và restore. Các ca đó vẫn NOT_RUN.

## Tài liệu và bằng chứng

- [Bytebase: 45 kết quả và phạm vi](BYTEBASE-ORACLE-POC-RESULTS.md).
- [ODC: 45 kết quả và phạm vi](ODC-ORACLE-POC-RESULTS.md).
- [Bộ tiêu chí gốc](poc/ORACLE-POC.md).
- [Ảnh, JSON và task commands](https://db-poc.apps.drgdevlab.com/).
- [License audit theo snapshot](LICENSE-AUDIT.md). Bản miễn phí, quyền sử dụng source và tính năng trả phí là các vấn đề riêng.

Không đổi P03/P04 lịch sử thành PASS. Hai lỗi đã tái hiện lại trên runtime hiện tại.
