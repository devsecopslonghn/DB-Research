# CloudDM source preflight: account and datasource limits

Ngày: 2026-10-06. Đây là rà soát source tĩnh và metadata công khai, không chạy CloudDM, không kiểm image binary/live tenant, không có xác nhận hợp đồng từ nhà cung cấp. Source snapshot và file hashes: [manifest](clouddm-source-preflight-20261006-hashes.json), [các file được lưu](source-clouddm-20261006/).

## Kết quả hẹp về 50 datasource / 20 account

Ở `ClouGence/open-cdm@3aa1238a471afca2579e76e6fbf0a922d9be5579`, các đường được chọn không gọi counter cap tương ứng với ngưỡng 10 datasource/5 account đang được pricing index công bố:

- `RdpUserManagerController.addSubAccount` gọi service thêm tài khoản và trả success khi service thành công (`source-clouddm-20261006/RdpUserManagerController.java:142–158`). `RdpUserServiceImpl.addSubAccountCheck` có dòng `checkSubAccountCount()` đang bị comment (`:634–640`); `addSubAccountForInternal` gọi check đó rồi ghi user qua mapper (`:738–773`). Đây là bằng chứng mạnh rằng cap check không chạy trong các method đã xem.
- `DmDsController.addDs` yêu cầu quyền `RDP_DS_MANAGE`, sau đó gọi datasource service (`source-clouddm-20261006/DmDsController.java:183–195`). `DmDsWebServiceImpl.addDs/persistAddDs` dựng cấu hình và insert datasource (`:305–348`); trong hai method này không thấy instance-count check.
- `RdpAuthUtils` trong source review hiện có là quyền tài nguyên, không coi tên package là bằng chứng license enforcement. Notification hooks, interceptor/global hooks và các đường tạo qua import/API khác chưa được rà hết.

Vì vậy có thể bỏ giả thuyết rằng *các method server-side vừa rà* chủ động enforce 5 account hoặc 10 datasource. Không thể suy ra Community unlimited, xác nhận không có global/runtime cap, quyền pháp lý cho 20 account/50 datasource, hay hành vi của artifact phát hành. Source pin không được map với image digest đang phân phối.

## DOC, source và artifact đang bất đồng

Direct GET trang pricing ngày 2026-10-06 có SHA-256 trùng byte với bản direct snapshot ngày 2026-10-04; response body được lưu dưới dạng hash/provenance, không copy nguyên trang. Search index vẫn trả Community 10 datasource instance/5 account từ crawl cũ khoảng ba tháng (ngày crawl chính xác không có). README source gọi sản phẩm là free/open-source, còn [`LICENSE.txt`](source-clouddm-20261006/LICENSE.txt) cấp Apache-2.0 cho phạm vi mã thuộc license. Không tài liệu nào ở đây xác lập entitlement của mọi image/plugin, quyền thương mại ở quy mô yêu cầu, hoặc SLA/support.

Lượt kiểm tiếp theo cho CloudDM vì vậy là đối chiếu *đúng binary/image* với source/build/license/notices và xác nhận entitlement/counter bằng điều khoản hiện hành hoặc hành vi của artifact được cấp phép. Estimate 1.5–3 người-ngày ở report là expert estimate thấp độ tin cậy, không phải đã được budget hoặc đã thực hiện. Nếu trong timebox không xác định được, giữ gate UNKNOWN và không mở runtime POC rộng. Không bỏ qua điều khoản, cũng không dừng nhánh chỉ dựa trên search index cũ.

## Oracle compile path được làm rõ

Compile path cần diễn giải chính xác hơn source review trước. `OraSession` truy vấn `ALL_ERRORS` khi `QueryRequest.isUseCompile()` bật; compile diagnostic có thể phát ra `MessageLevel.Error`. `AutoExecJob` nhận Error và ném lỗi theo error policy. Tuy nhiên `QueryRequest.useCompile` mặc định `false`; trong `AutoExecServiceImpl` request mới lấy qua `DmDsUtils.createRequestCtx` rồi body/args được copy, nhưng không thấy `setUseCompile(true)` trong call site đã rà. Không thấy compile flag được truyền đến runner mặc định. Vì vậy compile support có thể fail job *nếu* được bật và request/args chính xác; source chưa chứng minh auto-execution bật nó, kiểm đủ object/body/error rows, hoặc reducer đánh toàn flow fail-closed. Tên mode/helper không đủ để gọi đây là post-DDL validity gate.

Các source execution files (`OraSession`, `AutoExecJob`, `AutoExecServiceImpl`, `ApprovalControlServiceImpl`) ở snapshot `3aa…` được đối chiếu byte-identical với source pin `a9f16e78b8288c9a4158ee9df4378ee16b80021e` trong [release comparison](clouddm-release-comparison.json). Claim về `useCompile` mặc định dựa trên [`QueryRequest.java`](source/clouddm-v4.3.0__QueryRequest.java) trong cùng coordinator source bundle. Việc này xác nhận tính liên tục của các file được so, không map source với bất kỳ distributed image nào.

`DmFlywayInit.java` trong CloudDM source quản lý nâng cấp schema ứng dụng CloudDM qua `dm_update_history` và resource scripts (`source-clouddm-20261006/DmFlywayInit.java:47–85`); không phải bằng chứng CloudDM dùng Flyway làm migration engine cho Oracle target của khách hàng.

## Quyết định lượt kiểm

Giữ CloudDM là nhánh source/build conditional. Ưu tiên xác minh binary/right/counter cho 50/20 trước. Nếu gate qua, correctness probe nhỏ nhất phải kiểm Oracle procedure/package `INVALID`: bật compile path có chủ đích, truyền owner/name và policy, xác nhận `ALL_ERRORS` đúng object type/body làm task và flow terminal-fail; sau đó cùng-ID/hash replay, cùng-ID/changed-hash block và liên kết kết quả từng target. Target migration ledger/checksum/recovery vẫn chưa được source chứng minh. Không tự nâng runtime status từ DOC/SOURCE.
