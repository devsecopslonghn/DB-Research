# Review chéo license và pin CloudDM

Ngày: 2026-10-04. Phạm vi: đối chiếu [review Oracle/governance của coordinator](../coordinator/oracle-governance-source.md), [CloudDM deep review](../clouddm/deep-source-review.md), [findings](../clouddm/findings.csv), [source manifest](../clouddm/source-manifest.json) và bằng chứng license/release/registry trong thư mục này. Không sửa criteria hoặc findings. Không kiểm runtime.

## Kết quả

1. **Các CloudDM source pin khớp trên những file đã so sánh.** Deep review pin `a9f16e78b8288c9a4158ee9df4378ee16b80021e`; release `v4.3.0` pin `3aa1238a471afca2579e76e6fbf0a922d9be5579`. Coordinator so sánh 11 file quan trọng và thấy byte-identical. Vì vậy findings trên các path này áp dụng cho cả hai source snapshot. Đây không phải so sánh toàn repository hoặc image. Xem [manifest so sánh](../coordinator/clouddm-release-comparison.json).

2. **AccessFlow cũng khớp trên các file đã so sánh.** Coordinator so sánh bốn file quan trọng giữa source review pin `55c209a4...` và release `v2.7.0` pin `2ba5d322...`; nội dung giống byte-for-byte. Kết quả này không xác nhận toàn bộ repository hoặc OCI image. Xem [manifest so sánh](../coordinator/accessflow-release-comparison.json).

3. **Bảng giá CloudDM là thông tin được index, chưa xác minh live.** Kết quả search/open index quan sát ngày 2026-10-04, ghi crawl khoảng hai tháng trước, nêu Community 10 instance/5 account và Commercial không giới hạn. GET trực tiếp đến `/en/pricing` và `/en/pricing/` đều trả homepage 55,741 byte, không có bảng giá. Cache nằm ở `coordinator/public-docs/`; SHA-256 `9bca0fb2449737ec1eba676087cb0f8b75f0b3e698d0308d8d357ccf40256ab6` không chứng minh số 10/5. Đây là gate thương mại tiềm năng. Entitlement hiện tại và enforcement của image chưa rõ. Không gọi đây là quyền live đã xác minh hoặc CloudDM miễn phí không giới hạn.

4. **Schema license không chứng minh enforcement.** Deep review nêu migration `V202605070011__dm_license_support`; file này chỉ tăng chiều dài cột trạng thái kết quả license. Source release `v4.3.0` có migration `V202605070005__add_rdp_license`, tạo bảng xác thực/version/result và trường version được mã hóa. Đây là SOURCE về schema và dữ liệu khởi tạo. Nó chưa chứng minh service validation, counter account/instance, binary gate hoặc entitlement. T05 cần lần đường validation UI/backend và kiểm đúng artifact.

5. **Apache-2.0 của CloudDM không quyết định license image.** License áp dụng cho source trong phạm vi của nó. Pricing limits là điều kiện sản phẩm riêng. Source tree release liệt kê notice/license như `Oracle-FUTC.txt` và `MySQL-UFE-1.0.txt`, nhưng tệp đó chưa được pin trong manifest source đã chọn và danh sách không xác định component nào nằm trong archive/image. Cần đối chiếu package, notice, Oracle JDBC version/hash, cách lấy driver, digest image và SBOM.

6. **Deep review không biến SOURCE thành RUNTIME.** Tài liệu giữ runtime CloudDM là NOT_RUN. Nó phân biệt webhook receipt dedup với migration idempotency; MD5 truyền gói với checksum migration; compile helper explicit mode với lời gọi compile mode chưa thấy trong AutoExec; JDBC transaction với implicit commit DDL của Oracle; trigger-flow lock với target lock. Các gap âm tính được giới hạn trong path/tập file đã đọc. Không có PASS/FAIL runtime mới.

7. **Các phát hiện source của coordinator vẫn tách khỏi kết quả runtime.** AccessFlow gate DML/PLSQL là source incompatibility đã thấy, không phải kết quả test mới. Archery có INVALID check cho object được đặt tên; nguy cơ package-body bị bỏ sót là inference cần POC. ODC phân biệt dialect OB_ORACLE với Oracle; source pin không đại diện cho toàn bộ image runtime. Bytebase source review gắn với runtime 3.22.1/FREE; các FAIL lịch sử tiếp tục thuộc build đó. Không nâng/hạ PASS/FAIL vì release hoặc source mới.

8. **MetaDB OceanBase có pin license riêng.** Coordinator xác nhận `oceanbase/oceanbase` tag source `v4.3.5_CE` tại `5d6cb5cbc3f7c1ab6eb22e40abec8e160a8764d5` khai báo MulanPubL-2.0. Đây không phải Apache-2.0 của ODC. Image lịch sử `oceanbase/oceanbase-ce:4.3.5-lts` chưa được nối provenance với source tag này. Không gán license của tag source cho toàn image hoặc giả định image là derivative/aggregation nếu chưa kiểm thành phần và build.

9. **Điều khoản Instant Client có phạm vi cụ thể.** Điều khoản OTN áp dụng cho Oracle Instant Client Programs. Hạn chế phân phối downstream và yêu cầu chấp thuận trước áp dụng trong phạm vi ghi trong agreement. Điều khoản benchmark không được suy rộng thành lệnh cấm công bố mọi benchmark platform chỉ vì platform có thể dùng Oracle driver. Với benchmark trực tiếp của Instant Client hoặc kết quả thuộc phạm vi điều khoản, xác định artifact và điều khoản rồi xin review/chấp thuận nếu cần. JDBC Thin/ojdbc có điều khoản riêng.

## Việc còn lại có thể hành động

- **T05 CloudDM:** pin `v4.3.0`, image reference/digest, package component inventory, notices và SBOM. Trace license validation/counter; xác minh định nghĩa account/instance và trang giá hiện hành. Ghi Oracle JDBC version/hash và cách phân phối.
- **T05 các ứng viên:** so release source, digest image và build runtime cụ thể. Metadata của tag không tự xác nhận provenance.
- **T09:** ghi rõ đường Oracle dùng Instant Client, SQL*Plus hay JDBC Thin. Áp dụng đúng điều khoản cho artifact đó. Giữ mọi kết luận công bố benchmark trong phạm vi terms cụ thể.
- **CVE maturity:** chỉ ODC có `SECURITY.md` đã kiểm trong lượt này. Bốn repo khác nói chưa thiết lập. Contributor total chưa lấy được vì GitHub API rate limit. Đây là khoảng trống thông tin, không phải kết luận sản phẩm có hoặc không có CVE.

## Nguồn

- [CloudDM pricing index target](https://www.cdmgr.com/en/pricing)
- [CloudDM release v4.3.0](https://github.com/ClouGence/open-cdm/releases/tag/v4.3.0)
- [CloudDM license schema migration tại release SHA](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-boot/boot-initialization/src/main/java/com/clougence/clouddm/init/component/scripts/V202605070005__add_rdp_license.java)
- [Oracle Instant Client agreement](https://www.oracle.com/downloads/licenses/instant-client-lic.html)
- [Oracle JDBC downloads và FDHUT reference](https://www.oracle.com/database/technologies/appdev/jdbc-downloads.html)
