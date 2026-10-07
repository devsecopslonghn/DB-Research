# CloudDM: mâu thuẫn provenance trang giá

Ngày tra cứu: 2026-10-04. Loại DOC, không runtime.

[Trang pricing chính thức](https://www.cdmgr.com/en/pricing) qua web index hiển thị Community miễn phí, giới hạn 10 datasource instance và 5 tài khoản. Commercial có số lượng không giới hạn. Bản crawl được công cụ ghi là khoảng hai tháng trước.

HTTP GET trực tiếp cả URL có và không có trailing slash trả cùng HTML homepage, không chứa pricing table. [Manifest](manifest.json) lưu URL, thời điểm và SHA-256 cho hai response này. Chúng không chứng minh số 10/5 hiện còn hiệu lực.

Giữ số 10/5 là DOC về gói công bố trong index. Điều khoản live, semantics counter và enforcement của image v4.3.0 chưa xác minh. Không tuyên bố Community unlimited hoặc xác nhận current gate chỉ từ một kênh. Không tìm đường bypass license.
