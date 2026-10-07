# Review và quyết định của coordinator

Ngày: 2026-10-04. Scope: T02/T03 sâu và chuẩn bị thông tin T04/T05. Không deployment hoặc runtime.
Chỉ coordinator sửa common files. Ba worker có thư mục riêng và review chéo.

| Nội dung review | Điều chỉnh hoặc quyết định |
| --- | --- |
| AccessFlow BEGIN/internal semicolon | Coordinator đọc scanner/gate; CloudDM worker review lại. Giữ SOURCE incompatibility của native change set, không runtime FAIL. |
| AccessFlow continueOnError/self-approval | Native promotion dùng continueOnError=false. Self-approval guard chạy trước reviewer override. Không gán generic group behavior cho native path. |
| Source pin khác release | Đối chiếu bốn AccessFlow file với v2.7.0 và 11 CloudDM file với v4.3.0. Byte-identical trong selected files. Không suy toàn repo/image giống nhau. |
| Archery release driver | Source v1.14.0 dùng cx-Oracle 7.3.0, HEAD dùng oracledb 4.0.1. Parser/setup và execute_workflow byte-identical; package-body inference vẫn có, Thin mode không gán cho release. |
| Archery PACKAGE BODY | Coordinator thấy owner/name + fetchone không OBJECT_TYPE. Cross-review giữ inference có điều kiện, không nói đã tái hiện. |
| CloudDM receipt uniqueness/splitter | Worker trace DDL unique delivery/commit và datasource SPI. Coordinator đọc selected release files. Đóng SOURCE gaps đã đủ bằng chứng; runtime race/parser vẫn NOT_RUN. |
| CloudDM compile/checksum/lock | ALL_ERRORS helper phụ thuộc compile flag. MD5 transport, webhook dedup và flow row lock không thay target ledger/checksum/fencing. |
| CloudDM requester/primary account | Primary account có quyền override trong inspected source. GOV-03 yêu cầu unauthorized requester separation và administrator powers riêng. Không tự ghi runtime FAIL từ admin path. |
| CloudDM pricing | Indexed official page 10/5, direct GET homepage khác nội dung. Đã lưu cả provenance. Sửa claim current-live verified thành published DOC gate, enforcement UNKNOWN. |
| Oracle client terms | Điều khoản Instant Client gắn đúng Programs/path; không tổng quát hóa sang mọi JDBC/platform benchmark. Tách use/distribution/disclosure. |
| ODC MetaDB | OceanBase source tag v4.3.5_CE pin MulanPubL-2.0. ODC Apache không bao phủ component này. Historical image source mapping chưa chốt. |
| Register CSV | Coordinator phát hiện worker CSV sai field count. Worker chuyển sang DictWriter và kiểm 24 fields trước merge. |
| DBGit source availability | Repo404 không là đủ lý do source gate khi npm tarball công khai. Worker inspect archive tĩnh, không install/execute. Pin source/license bằng archive hash riêng với Git SHA. |
| Discovery category | Oracle connection/UI/CDC/lineage/docs-only không là A native release. Liquibase demo là sample có Pro/Flow gate, không tool độc lập. |
| Benchmark | Giữ criteria/spec/config/workload hash. Thêm gate/dependencies riêng, không chỉnh workload 50 hoặc bỏ DML để đạt tool. |
| Registry | Worker GET 9 refs thành công và một mirror timeout. Coordinator GET độc lập ODC 4.4.1 và CloudDM 4.3.0, header digest khớp bodySHA và worker. No layer pulls. Labels/source mapping còn gap, Bytebase revision khác release SHA. |
| Historical evidence | 15 file source/evidence hashes giữ nguyên. New source/runtime version không ghi đè old FAIL/P03/P04. |

Review chéo:

- [CloudDM worker review AccessFlow/Archery](clouddm/cross-review.md).
- [License worker review source/license/provenance](licensing/cross-review.md).
- [Discovery worker review shortlist/criteria/benchmark](discovery/cross-review.md).

Review độc lập agy của benchmark ở [vòng đầu](../reviews/coordinator-review.md) vẫn được giữ. Vòng này không cần chạy lại cùng review.
Đã kiểm `agy models` và `/usage` cho công việc có thể giao. Ba native worker và review chéo đáp ứng câu hỏi độc lập của vòng này. Không mở thêm worker vượt ba slot.

[Artifact checks](artifact-checks.json) sẽ ghi hash/CSV/local-link checks và scope chưa chạy. Đây là inspection, không product tests.
Remaining: exact image inventory/source mapping/driver/license enforcement, Oracle runtime correctness, real CI, recovery và performance.
Contributor API rate limit và public indexing không đủ để khẳng định tìm hết dự án hoặc xác nhận support SLA.
