# Kết nối Oracle qua ODC trong lab

Ngày kiểm tra: 04/10/2026. URL: https://oceanbase.apps.drgdevlab.com.

Datasource `oracle-cloud` đã kết nối thành công. Truy vấn chỉ đọc qua ODC trả về `ADMIN` cho người dùng và schema.

## Cấu hình đang hoạt động

| Trường | Giá trị |
|---|---|
| Type | Oracle |
| Host | `adb.ap-mumbai-1.oraclecloud.com` |
| Port | `1521` |
| Connection type | Service Name |
| Service Name | `gaf051b0a6547f3_labdb_tp.adb.oraclecloud.com` |
| Username / Default Schema | `ADMIN` / `ADMIN` |
| User Role | Normal; giá trị API `NORMAL` |
| Driver Properties | `protocol=tcps`, `ssl_server_dn_match=true` |

Mật khẩu được giữ trong ODC. Hồ sơ công bố không chứa mật khẩu.

## Thao tác trong giao diện

1. Đăng nhập. Chọn Team Workspace, rồi mở **Data Sources**.
2. Chọn `oracle-cloud`, rồi chọn **Edit**.
3. Chọn **Service Name** và đối chiếu host, port, service trong bảng.
4. Mở **Advanced Settings → Driver Properties**.
5. Đặt `protocol` thành `tcps` và `ssl_server_dn_match` thành `true`.
6. Xóa `SSL` và `SSL VERIFY` nếu còn. Các tên này thuộc cấu hình driver Go trước đó.
7. Giữ mật khẩu đã lưu. Chọn **Test Connection**, rồi lưu.
8. Mở SQL console cho datasource này. Chạy truy vấn dưới đây.

```sql
SELECT USER AS SESSION_USER,
       SYS_CONTEXT('USERENV','DB_NAME') AS DB_NAME,
       SYS_CONTEXT('USERENV','CURRENT_SCHEMA') AS CURRENT_SCHEMA
FROM DUAL;
```

Kết quả đã quan sát: `ADMIN`, `GAF051B0A6547F3_LABDB`, `ADMIN`.

## Vì sao cần bản sửa

Plugin Oracle gốc trong image đang dùng tạo URL JDBC TCP. Endpoint Oracle hiện tại cần TCPS.
Wrapper cục bộ thêm URL TCPS và hỗ trợ parser metadata. Argo CD đã triển khai wrapper từ PR #32.
Wrapper luôn bật kiểm tra tên máy chủ. Không cần tắt xác minh chứng chỉ.
Wrapper phụ thuộc đúng image ODC đang pin. Khi nâng phiên bản, phải đánh giá lại wrapper.

## Bằng chứng và giới hạn

Bằng chứng API đã chọn lọc: [odc-oracle-readonly.json](https://db-poc.apps.drgdevlab.com/evidence/odc-oracle-readonly.json).
Ảnh datasource là giao diện thật. Ảnh không thay thế kết quả SQL trong hồ sơ API.
Snapshot kết nối ban đầu chưa chạy 45 ca. Lần POC sau đã có [kết quả API/UI](ODC-ORACLE-POC-RESULTS.md).
Truy vấn POC chỉ đọc metadata. Tài khoản ADMIN có quyền ghi, nên kết quả này không chứng minh enforcement read-only.

Để đánh giá quyền, tạo tài khoản Oracle dành riêng cho POC và cấp đúng quyền schema cần thiết.
Để đánh giá migration, dùng schema thử nghiệm riêng và thực hiện từng ca trong kế hoạch Oracle đã có.

Tài liệu upstream: [Oracle Autonomous Database TLS](https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/connect-introduction.html).

## Tóm tắt lỗi và cách sửa

| Mục | Kết luận |
|---|---|
| Hiện tượng | Test Connection thất bại, kết nối bị reset. |
| Target | Oracle Autonomous Database, host `adb.ap-mumbai-1.oraclecloud.com`, port `1521`, Service Name như trên. |
| Nguyên nhân | Plugin ODC tạo URL TCP mặc định. Endpoint này cần TCPS. |
| Cấu hình chưa đúng | `SSL=true`, `SSL VERIFY=false` không chọn giao thức TCPS cho Oracle JDBC. |
| Sửa ở ứng dụng | Wrapper TCPS cho plugin Oracle và parser metadata; triển khai qua Argo CD từ PR #32. |
| Sửa ở datasource | Dùng Service Name, `protocol=tcps`, `ssl_server_dn_match=true`; bỏ `SSL` và `SSL VERIFY`. |
| Bằng chứng | Test Connection `active=true`; SELECT metadata qua ODC có `SUCCESS`. |

### Có phải chỉ Oracle Free bị lỗi?

Không có bằng chứng cho thấy lỗi này do gói Free. Thuộc tính quyết định là giao thức của listener.
Oracle Autonomous Database yêu cầu kết nối TLS hoặc mTLS. Database Oracle tự triển khai có thể dùng TCP hoặc TCPS tùy cấu hình listener.
Vì vậy, Oracle trả phí dùng endpoint TCPS cũng có thể gặp cùng giới hạn plugin ODC. Oracle Free dùng listener TCP không nhất thiết gặp lỗi này.

Host, port, Service Name và mật khẩu hiện tại đã dùng được sau khi đổi giao thức. Không cần đổi mật khẩu hoặc tắt xác minh chứng chỉ.
Có hai vấn đề kết hợp: các thuộc tính SSL chưa đúng driver và plugin ODC đang dùng chưa tạo URL TCPS.
Cấu hình `protocol=tcps` chỉ có tác dụng sau khi triển khai wrapper lab này. Đây không phải tùy chọn TCPS upstream đã được xác nhận.

Không chọn giao thức chỉ theo số cổng. Oracle có thể phục vụ TLS trên `1521` hoặc `1522` tùy cấu hình.
Lấy đúng chuỗi kết nối của database từ trang Oracle hoặc DBA. Nếu database bắt buộc mTLS, cần cấu hình wallet riêng.
POC hiện tại dùng TLS không có wallet. Kết quả này không áp dụng tự động cho mọi endpoint mTLS.

Nguồn: [Oracle Autonomous: TLS và mTLS](https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/connect-introduction.html),
[Oracle JDBC: TCP và TCPS](https://docs.oracle.com/en/database/oracle/oracle-database/26/jajdb/oracle/jdbc/OracleDriver.html).
