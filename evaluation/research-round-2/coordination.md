# Điều phối nghiên cứu mở rộng

User yêu cầu coordinator tự quyết định và làm hết công việc thông tin khả thi.
Scope: tìm kiếm, source/license/release/maturity review, chuẩn bị tài liệu quyết định và POC.
Không deployment, test, service, SQL, benchmark hoặc kiểm live target.
Criteria, workload và evidence runtime cũ giữ nguyên.

## Acceptance

1. Mở rộng tìm kiếm ngoài web commercial, ghi truy vấn/kết quả/giới hạn và primary sources.
2. Trace CloudDM từ change request đến Oracle executor, parser, commit/error, ledger, approval và dedup storage.
3. Kiểm image/plugin/driver/source/edition và release metadata của ứng viên chính bằng nguồn công khai.
4. Trace AccessFlow/Archery và ODC/Bytebase cho các P0 đã biết hoặc chưa rõ, không suy runtime PASS.
5. Tách absence-of-evidence khỏi code không có feature và document/source/runtime mâu thuẫn.
6. Review chéo, cập nhật shortlist/register/source summary và task tiếp theo đủ cụ thể.
7. Giữ snapshot vòng trước và hash 45 criteria/14 workload/evidence cũ.

## Ownership

Worker cloud-deep chỉ ghi research-round-2/clouddm/.
Worker discovery-deep chỉ ghi research-round-2/discovery/.
Worker licensing chỉ ghi research-round-2/licensing/.
Coordinator giữ file chung; tự trace nguồn AccessFlow/Archery và đối chứng.
Sau worker review, làm review chéo và review quyết định độc lập có giới hạn.

## Quyết định điều phối

Chưa chuyển T05 runtime. Hoàn tất phần chuẩn bị thông tin của T05 là được phép.
Không gửi email, liên hệ vendor hoặc publish. Chỉ dùng public docs/APIs/source/registry metadata.
Không coi thiếu public SBOM hoặc quyền audit private source là lý do dừng nghiên cứu phần khác.
Những điều chỉ runtime/private entitlement mới trả lời được sẽ được ghi điều kiện rõ.
