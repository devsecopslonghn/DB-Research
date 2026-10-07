# Search log T02

## Mở rộng sau T00–T04 đầu

[Log vòng4–6](research-round-2/discovery/search-log.md) bổ sung forge/topic/catalog, tiếng Trung, client/engine và package source.
Register hiện có 47 mục: 36 mục kế thừa, 10 lead product/component mới và một composition sample. Có fork/components nên không gọi đây là 47 platform độc lập.
Không tìm được A OSS mới đủ evidence. Runtime mới NOT_RUN. GitHub API rate limit, private source và search indexes giới hạn coverage.
DBGit npm archive được đọc tĩnh để khép source/license gap. Không install/execute. Dsync LICENSE404 vẫn có distribution gap.
Các vòng1–3 phía dưới là log ban đầu, không là kết luận chưa làm vòng sâu.

Ngày: 2026-10-04. Scope: nền tảng gần Bytebase, Oracle, governance và quản lý DB.
[Log worker](candidates/discovery/search-log.md) ghi exact queries, primary URLs, các lead và giới hạn.
Không tuyên bố đã tìm mọi sản phẩm hoặc fork.

## Các vòng và phần kế thừa

| Vòng | Phạm vi đã tìm | Kết quả chính |
| --- | --- | --- |
| Seed registration sau T01 | CloudDM, ODC, Bytebase, AccessFlow và Archery từ index/handoff | Giữ nguồn cũ, giao câu hỏi native workflow/Oracle/license độc lập cho worker |
| 1 | Repo/topics, Oracle platform, deployment/change/release và open-source alternatives | Tái phát hiện D-Band DRM/dbward và các engine cũ; commercial leads |
| 2 | Official product/license docs, DBmaestro/DataStar và Oracle lifecycle management | Ba đối chứng thương mại; không có A OSS mới đủ căn cứ |
| 3 | GitLab, CNCF/catalogue, awesome fork, dependency reuse, Bytebase forks và Chinese SQL governance | advisorTool B/component, AdminerEvo D/client; SQLE là mục trùng; không có A OSS mới đủ căn cứ |

Dừng sau vòng 2 và 3 liên tiếp không có A OSS mới đủ căn cứ theo kế hoạch.
D-Band DRM chính là `dband-drm/drm-cli`. Không đếm đó là phát hiện mới.
CloudDM là lead đã tìm trước T00, không gọi đó là discovery mới của worker T02.

[Register](candidates.csv) kế thừa toàn bộ 21 mục trong ma trận cũ, thêm SQLE/DMS, NineData, CloudDM và bảy fork đã kiểm.
Register tách các lead mới DataStar, DBmaestro, OEM, advisorTool và AdminerEvo.
Các mục kế thừa có `review_scope` và source snapshot riêng. Không nói đã re-audit toàn bộ current HEAD.
Tham khảo [old search log](../evidence/product-model/SEARCH.md), [fork sample](../FORK-SEARCH.md), [license audit](../LICENSE-AUDIT.md).

## Source/edition recheck ở T03

CloudDM source pin a9f16e7 trùng official main tại lần worker đọc API.
AccessFlow 55c209a và Archery ccc7134 trùng HEAD qua read-only git ls-remote.
Bytebase license/plan đọc theo runtime commit a85f6cb, không thay bằng current HEAD khác.
ODC source/backend/frontend dùng snapshot trong manifest cũ; build lịch sử ghi riêng.
Worker chỉ đọc source có chọn lọc. Coordinator kiểm lại license, connector/batch và source admission gate liên quan.

Coordinator web query bổ sung:

- `site.bytebase.com pricing free approval audit 2026`
- `site.oceanbase.github.io/odc Oracle database support batch change`

[Bytebase pricing](https://www.bytebase.com/pricing/) hỗ trợ phân biệt Community/Pro/Enterprise với TEAM label trong runtime.
[ODC official repo](https://github.com/oceanbase/odc) và pinned batch docs được dùng cho product support.
ODC quick-start cũ chỉ liệt kê OceanBase Oracle mode, nên không dùng nó phủ định native Oracle đã có source/runtime.

## Giới hạn

Web/topic/catalogue indexing không đầy đủ. GitLab không có authenticated private group search.
Catalogue entry không chứng minh license, Oracle compatibility hoặc production use.
Đã tìm fork/dependency leads nhưng không kiểm toàn bộ fork graph.
Không tải commercial binary hoặc truy cập private source. Vendor DOC chưa được xác nhận runtime.
Không tìm thêm bằng cách đọc toàn evidence/source. Source lookup theo claim/path cụ thể.
Không đọc credential, kết nối target, deployment, service, test, SQL hoặc benchmark.
