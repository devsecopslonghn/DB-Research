# Trước và sau: release thủ công có kiểm soát

| Khả năng | Trước: DBeaver và thao tác thủ công | Demo |
| --- | --- | --- |
| Source | File SQL trao đổi rời rạc | Git commit, PR, manifest và hash |
| Review | Email/chat, đọc file thủ công | PR validation và OWNER/DBA review trong ODC |
| Target | Chọn connection/database trong DBeaver | Inventory ODC và bốn target allowlist |
| Approval | Phối hợp email/chat | Approval native ODC |
| Execution | Chạy SQL thủ công trong DBeaver | ODC thực thi artifact đã review |
| Rollout | Tự phối hợp thứ tự môi trường | Batch native MANUAL, singleton theo thứ tự |
| Audit | Screenshot và log copy rời rạc | ODC history/audit và evidence GitHub |
| Report | Tổng hợp thủ công | Markdown và JSON được sinh từ evidence |

| Trước khi áp dụng quy trình | Sau khi áp dụng quy trình demo |
| --- | --- |
| SQL và cấu hình đích có thể được trao đổi rời rạc; khó chứng minh bytes nào đã review. | PR review và exact release envelope ghi commit, cấu hình, manifest, policy và SHA-256. |
| Kiểm tra trước chạy phụ thuộc vào người đọc từng file. | GitHub Actions chạy kiểm tra tĩnh, báo policy finding và chặn contract sai; vẫn cần OWNER/DBA review. |
| Trạng thái giữa các stage khó so với kết quả DB. | ODC giữ native status theo stage; operator lưu receipt và verifier đọc Oracle bằng `SELECT`. |
| Lỗi có thể khiến người vận hành không chắc có nên chạy tiếp hay hoàn tác. | Batch `ABORT`, retry 0 dừng tại lỗi; con người xem xét trạng thái một phần và phát hành correction riêng. |
| Bản ghi thành công có thể bị hiểu nhầm từ trạng thái job đơn lẻ. | Report phân biệt native status, kết quả Oracle và source `LIVE`/`FIXTURE`/`NOT_AVAILABLE`. |

ODC có thể tập trung execution thủ công kiểu DBeaver, target selection, approval, rollout và logs. ODC không thay Git, Oracle DBA, backup, thiết kế schema, Flyway version ledger hay quy trình recovery. Có hai mode: ODC-led và version-disciplined Git + ODC với reviewed applied-release references; mode sau không có Flyway executor/bridge.

Demo không tự rollback, promote hay replay. Các schema là POC cô lập trên cùng database; `MOCKPROD` không phải production. PR fixture smoke và report fixtures không chứng minh runtime. Live workflow cần ở `refs/heads/main` và protected `odc-demo` environment đã cấu hình deployment branches/reviewers; trước pilot cần áp dụng và xác minh GitOps retention recommendation vì lab hiện ở baseline.
