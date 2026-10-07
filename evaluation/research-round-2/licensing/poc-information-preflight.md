# Tiền kiểm thông tin cho T05

Phần này ghi thông tin có thể chuẩn bị từ nguồn công khai. Nó không cho phép deploy, chạy test, SQL, dùng credential hoặc truy cập target.

## Thông tin công khai đã có

| Ứng viên | Release dự kiến đánh giá | Thông tin đóng gói công khai | Gate cần quyết định trước runtime |
|---|---|---|---|
| ODC | So sánh runtime 4.4.1 đã giữ với build 4.5.x công khai nếu thêm vào scope | OCI digest runtime lịch sử được truy vấn lại và khớp record cũ; registry pins có trong [registry-pins.csv](registry-pins.csv). GitHub release mới nhất `4.3.4_bp2` có archive hash; docs nhắc 4.5.0. | Làm rõ source/image build mapping, MetaDB, nguồn Oracle JDBC và quyền đối với wrapper TCPS cục bộ. Không thay runtime lịch sử bằng release notes. |
| CloudDM | `v4.3.0` / commit `3aa1238a471afca2579e76e6fbf0a922d9be5579` | SHA-256 archive image standalone/cluster; OCI refs và manifest digests của standalone/console/sidecar tại [registry-pins.csv](registry-pins.csv). Archive hash khác OCI digest. Pricing index báo 10 instance/5 account nhưng GET trực tiếp trả homepage không có bảng. | Xem 10/5 là gate tiềm năng. Xác minh trang giá hiện hành, ý nghĩa counter và enforcement của artifact. Source/image mapping, SBOM và việc image có `ojdbc` chưa rõ; pin hash driver/plugin tải riêng. |
| AccessFlow | `v2.7.0` / commit `2ba5d322e7e1b4c750b5b0af85935e9ae814bd6a` | Compose tại release tham chiếu GHCR `latest`; manifest/index và platform digests quan sát được ghi trong [registry-pins.csv](registry-pins.csv). Connector JDBC có thể tải driver. | Source/image mapping và provenance chưa xác minh. Resolve version/hash/provenance `ojdbc11`; phân biệt người dùng tự cung cấp với vendor phân phối. Kiểm tra plan của đúng build. |
| Archery | `v1.14.0` / commit `bc1f10efcc465f6a63c94b97feaba5d15546712a` | Release API không có asset digest; OCI manifest và config labels ghi trong [registry-pins.csv](registry-pins.csv). Label revision trùng release SHA; chưa lấy layers/SBOM. Release requirements pin `cx-Oracle==7.3.0`; setup script cài Instant Client. | Giữ đường Oracle Thick vốn có của release và xác minh điều khoản Instant Client. Xác minh gói client chính xác và image có chứa client không. Không đổi sang Thin dựa trên mã HEAD đã review riêng. Chưa rõ SQL*Plus có trong image không. |
| Bytebase | `3.23.0` / commit `c8188c635465321ff930c97200742a96ef653144` | GitHub API không liệt kê asset digest; OCI manifest/config metadata có trong [registry-pins.csv](registry-pins.csv). Config revision khác release tag SHA; source/image provenance chưa rõ. | Chọn FREE/TEAM/Enterprise theo quyền approval/audit cần dùng; kiểm plan `3.23.0`. Giữ kết quả runtime 3.22.1 tách riêng. |

## Dữ liệu cần ghi trước POC runtime

1. Tag source và commit SHA chính xác, image ref và immutable OCI digest, architecture, thời điểm tạo và provenance công bố. Metadata OCI đã ghi trong [registry-pins.csv](registry-pins.csv); source↔image mapping và provenance còn UNKNOWN trừ khi có bằng chứng trực tiếp.
2. SHA-256 release archive nếu có. Ghi OCI digest riêng. Không dùng archive hash làm digest manifest của image đã giải nén. OCI config labels không thay thế SBOM.
3. SBOM hoặc danh sách component chính xác, notices, license identifier, URL source, version và hash của từng Oracle driver/client, plugin và executable tùy chọn.
4. Nguồn lấy Oracle driver và điều khoản áp dụng cho đúng artifact. Ghi evaluator tự tải để dùng nội bộ hay vendor phân phối trong image. Với Instant Client, ghi mode, package variant, agreement và cách người dùng downstream truy cập.
5. Edition/plan, số account và instance đang hoạt động, hành vi license state và nguồn bằng chứng entitlement. Với CloudDM, xác minh định nghĩa counter và trang giá hiện hành.
6. Các thông tin chỉ runtime mới xác định được: Oracle compatibility, wallet/TCPS, parser/PLSQL, migration correctness, recovery, governance enforcement và giới hạn benchmark. Metadata công khai không kết luận được các điểm này.

## Ranh giới benchmark

Giữ nguyên criteria, workload bytes/hash và benchmark spec hiện tại. Chọn driver mode/version mà mọi ứng viên so sánh đều dùng được theo điều khoản tương ứng. Nếu ứng viên cần Instant Client hoặc SQL*Plus, ghi component đó thành điều kiện/chi phí riêng; không tự thêm vào đường chạy chung. Trước T09, pin pool/worker, CPU/memory/storage, digest image/driver, Oracle full version, lịch target dùng chung và trạng thái hậu kiểm. Chỉ so throughput sau khi qua correctness và governance gates. Phần này không chứng nhận hiệu năng hoặc compliance license.

## Phạm vi điều khoản benchmark của Instant Client

Thỏa thuận Instant Client có điều khoản về công bố benchmark của Oracle Instant Client Programs và các yêu cầu chấp thuận trước trong những trường hợp áp dụng. Không suy rộng thành lệnh cấm công bố mọi benchmark platform có Oracle driver. Nếu benchmark trực tiếp đánh giá Instant Client hoặc kết quả thuộc phạm vi thỏa thuận, cần xác định artifact/điều khoản chính xác và xin review pháp lý/chấp thuận cần thiết trước khi công bố. Benchmark nội bộ của platform cần được đánh giá theo đúng artifact và cách dùng, không dựa vào khẳng định blanket.
