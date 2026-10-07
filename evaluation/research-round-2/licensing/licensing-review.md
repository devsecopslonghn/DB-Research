# Rà soát release, license và tín hiệu trưởng thành

Mốc nghiên cứu: 2026-10-04. Đây là rà soát thông tin công khai. Metadata GitHub đến từ REST API chỉ đọc. Không tải image đầy đủ. Digest archive công khai chỉ là metadata. Stars, forks, issues, commit activity và lời giới thiệu sản phẩm không chứng minh độ sẵn sàng production.

## Pin release và source

[release-pins.csv](release-pins.csv) tách pin release hiện hành khỏi pin source/runtime đã dùng trước đây. Hash SHA khác nhau tự nó không chứng minh commit nào cũ hơn, mới hơn hoặc cùng ancestry.

- **ODC:** release mới nhất trong GitHub là `v4.3.4_bp2` ngày 2025-06-06. Runtime lịch sử dùng ODC `4.4.1-20260116` và digest image lưu từ lượt trước. Tài liệu sản phẩm nhắc ODC 4.5.0, nhưng GitHub Releases API không trả release tương ứng. Kết quả runtime cũ chỉ áp dụng image đã chạy.
- **CloudDM:** release công khai `v4.3.0` ngày 2026-09-30 trỏ đến `3aa1238a471afca2579e76e6fbf0a922d9be5579`. GitHub công bố SHA-256 cho archive image standalone/cluster. Chưa tải hoặc giải nén archive. Coordinator đã so sánh 11 critical files giữa `a9f16e78...` và release pin; các file đó byte-identical. Điều này xác nhận các path đã chọn, không xác nhận toàn bộ repository hoặc image.
- **AccessFlow:** release công khai `v2.7.0` trỏ đến `2ba5d322...`, không có release assets. Compose tại commit release tham chiếu GHCR tag `latest`; manifest/index và platform digests đã ghi trong [registry-pins.csv](registry-pins.csv). Coordinator đã so sánh 4 source files giữa `55c209a4...` và release pin; các file đó byte-identical. Điều này xác nhận các path đã chọn, không xác nhận toàn bộ repository hoặc ánh xạ source sang image.
- **Archery:** release công khai `v1.14.0` trỏ đến `bc1f10ef...` ngày 2026-03-07. So sánh bốn file cho thấy `sql_utils.py` và `setup.sh` trùng pin review `ccc7134f...`, còn `oracle.py` và `requirements.txt` khác. Release requirements pin `cx-Oracle==7.3.0`; OCI label revision khớp release SHA. API không trả release asset digest. Image layers và SBOM chưa kiểm.
- **Bytebase:** release công khai `3.23.0` trỏ đến `c8188c63...` ngày 2026-09-24. Review license/runtime trước dùng `3.22.1`, commit `a85f6cb...`. Cần kiểm plan của đúng build trước khi chọn POC.

Hash của release archive khác với OCI registry digest. Manifest/index và config metadata của các ref đã chọn được ghi trong [registry-pins.csv](registry-pins.csv). Không tải image layers hoặc SBOM. OCI metadata và labels không xác nhận danh sách dependency/license đầy đủ, ánh xạ source sang image hoặc provenance build runtime. Digest ODC được truy vấn lại và khớp digest lịch sử đã lưu.

## Quyền phiên bản và Oracle client

[license-components.csv](license-components.csv) ghi ranh giới source, plan và dependency. License của source sản phẩm không tự cấp quyền phân phối image hoặc quyền sử dụng mọi tính năng.

Trang giá CloudDM được search/open index hiển thị Community miễn phí với 10 datasource instance và 5 account; Commercial ghi không giới hạn hai số lượng đó. Quan sát ngày 2026-10-04 nhưng index cho biết nội dung đã được crawl khoảng hai tháng trước. Đây là DOC đã index, chưa xác minh live: urllib GET cả `/en/pricing` và `/en/pricing/` trả về trang giới thiệu sản phẩm, không có bảng giá. HTML đã tải có SHA-256 `9bca0fb2449737ec1eba676087cb0f8b75f0b3e698d0308d8d357ccf40256ab6`; nó không chứng minh số 10/5. Source công khai có migration schema xác thực license/RDP, gồm bảng chứa trường version mã hóa. Migration cho thấy cấu trúc dữ liệu, nhưng chưa chứng minh đường validation, giới hạn account/instance hoặc enforcement trong binary v4.3.0. Cần xem 10/5 là gate thương mại tiềm năng và xác minh trước khi chọn runtime. Chưa kết luận giới hạn còn hiệu lực, cách đếm hoặc CloudDM miễn phí không giới hạn.

Gate Bytebase phụ thuộc edition. Source 3.22.1 đã kiểm cấp MIT cho phần source được bao phủ, loại trừ thư mục Enterprise và enablement code, và ghi FREE có 10 instance/20 user. Approval yêu cầu Enterprise; audit yêu cầu TEAM trong source/runtime đã kiểm. Trang giá dùng nhãn plan khác ở một số chỗ. Cần đọc plan `3.23.0` trước khi mua/chọn edition. Edition trả phí không chứng minh các lỗi correctness runtime cũ đã được sửa.

Source chính ODC và AccessFlow dùng Apache-2.0. Không thấy paid gate trong các đường source đã kiểm. Điều này không xác nhận license mọi artifact, dependency hoặc image. AccessFlow khai báo Oracle `ojdbc11` là dependency connector ngoài; cần pin version/hash và cách phân phối. Runtime ODC lịch sử chứa `ojdbc8-21.1.0.0.jar`. TCPS wrapper trong lượt đánh giá là adapter cục bộ, không phải năng lực upstream ODC đã xác minh.

Archery HEAD pin `ccc7134f...` khai `python-oracledb==4.0.1`, nhưng không đại diện cho release `v1.14.0`. Release requirements pin `cx-Oracle==7.3.0`, và release setup script cài Oracle Instant Client. Tag `7.3` của dự án Oracle công bố license cx_Oracle cho phép phân phối lại theo các điều kiện về notice, disclaimer và tên. Điều đó không cấp quyền cho Instant Client. Vì vậy đường Oracle native của release cần Thick/client; không đổi sang Thin dựa trên mã HEAD. Thỏa thuận Oracle Instant Client đặt điều kiện riêng cho phân phối lại, gồm điều khoản downstream, hạn chế công bố kết quả benchmark của các Oracle Instant Client Programs và yêu cầu chấp thuận trước nêu trong thỏa thuận. Không suy rộng điều khoản này thành cấm công bố mọi benchmark platform. Image Archery được chọn chưa kiểm tra thành phần thực tế.

Trang tải Oracle JDBC ghi driver chịu FDHUT no-clickthrough terms. FAQ Oracle hướng công ty phần mềm bên thứ ba muốn phân phối JDBC driver sang FUTC, đồng thời khuyên rà pháp lý và liên hệ Oracle sales. Cần tách (1) người dùng tải/dùng driver khỏi (2) vendor đóng gói/phân phối driver. Tọa độ Maven hoặc cơ chế tự tải không chứng minh quyền tái phân phối.

SQL*Plus là công cụ/client được cài riêng. Chưa xác lập nó có trong image Archery hay ứng viên khác. Nếu lấy SQL*Plus qua gói Instant Client, cần xét điều khoản đúng gói đó. SQLcl chịu Oracle Free Use Terms and Conditions nhưng là sản phẩm khác, không chứng minh quyền SQL*Plus. Không thêm SQL*Plus vào benchmark Thin-JDBC nếu ứng viên không phụ thuộc nó.

Đây là tóm tắt gate vận hành, không phải đánh giá pháp lý toàn diện hay chứng nhận tuân thủ.

## Tín hiệu trưởng thành công khai

[maturity.csv](maturity.csv) ghi metadata theo ngày. GitHub contributor API bị rate limit trước khi lấy đủ tổng contributor. Vì vậy CSV ghi ngày hoạt động nhưng không có tổng contributor. Không suy quy mô team từ stars hoặc một số contributor đầu tiên. Chỉ ODC có SECURITY.md tại GitHub Security Policy page; tài liệu nêu email `security@oceanbase.com` và mục tiêu liên hệ trong 2 ngày làm việc, nhưng không có SLA xử lý/remediation. CloudDM, AccessFlow, Archery và Bytebase cho biết chưa thiết lập SECURITY.md; chưa xác minh disclosure route hoặc response SLA khác. GitHub security-and-quality counters không phải số CVE. Sự hiện diện/vắng mặt của policy không phải kết luận mức an toàn sản phẩm.

ODC và Archery có lịch sử dự án công khai lâu hơn. Bytebase có nhiều stars hơn các sản phẩm trong tập này. CloudDM và AccessFlow có release gần đây; AccessFlow có footprint stars/forks nhỏ hơn. Các số liệu này chỉ giúp đặt câu hỏi về hỗ trợ. Chúng không xếp hạng correctness Oracle hoặc hiệu năng runtime.

## Đối chiếu và bằng chứng được giữ lại

Rà soát bổ sung thông tin thương mại công khai, không sửa criteria hoặc kết quả runtime. Kết quả Bytebase và ODC trước đây tiếp tục gắn với đúng image/runtime đã chạy. Release mới không thừa hưởng kết quả cũ. Release hiện tại không tự thừa hưởng kết luận source từ một pin khác. Không có hành vi runtime nào được nâng thành PASS dựa trên release notes.

CloudDM source pointers cho rà license sâu: [trang giá được index](https://www.cdmgr.com/en/pricing), [migration schema license `V202605070005`](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-boot/boot-initialization/src/main/java/com/clougence/clouddm/init/component/scripts/V202605070005__add_rdp_license.java), [migration hỗ trợ license `V202605070011`](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-boot/boot-initialization/src/main/java/com/clougence/clouddm/init/component/scripts/V202605070011__dm_license_support.java). Migration sau tăng độ dài cột kết quả license. Hai migration không cho biết đầy đủ validation, ý nghĩa counter hoặc enforcement edition. Source tree release có đường dẫn `package/legal/licenses/Oracle-FUTC.txt` và `MySQL-UFE-1.0.txt`; notice không chứng minh thành phần nào nằm trong từng image. Cần đối chiếu license, notice, danh sách package và enforcement với archive/image sẽ chọn.
