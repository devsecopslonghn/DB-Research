# Kiểm tra registry công khai

Mốc truy vấn: 2026-10-04 khoảng 13:30 UTC. Chỉ gọi HTTP GET cho manifest/index OCI/Docker và blob config JSON nhỏ. Không gọi layer blob, không tải image, không chạy container. Giá trị chi tiết nằm trong [registry-pins.csv](registry-pins.csv).

## Kết quả theo image

- **ODC:** `docker.io/oceanbase/odc:4.4.1_bp1` trả manifest list digest `sha256:ee8ee48e...`; digest này khớp digest image đã lưu từ runtime ODC lịch sử. `latest` trả cùng digest tại thời điểm truy vấn. Có linux/amd64 và linux/arm64. Config ghi thời gian tạo và mô tả/maintainer, nhưng không ghi source revision. Đây là liên kết tốt giữa tag registry và runtime digest lịch sử; chưa phải liên kết source build.
- **CloudDM:** Tài liệu deploy chính thức công bố pattern `bladepipe/cgdm-alone:<target_version>` và ảnh Console/Sidecar. GET registry đọc tag `4.3.0` tại Docker Hub; link docs: [CloudDM deployment guide](https://github.com/ClouGence/open-cdm/blob/main/docs/guides/deployment.en.md). Tag `4.3.0` có registry index cho `cgdm-alone`, `cgdm-console`, `cgdm-sidecar`; index có linux/amd64 và linux/arm64. Config amd64 cho biết thời gian tạo và label `org.opencontainers.image.version=24.04`. Không coi `24.04` là version CloudDM. Không thấy source revision hoặc SBOM trong config. Docker Hub digest không bằng SHA-256 archive offline release vì đây là đối tượng khác. Aliyun mirror request timeout; kết quả này không chứng minh tag vắng mặt.
- **AccessFlow:** Compose tại source release `v2.7.0` dùng backend/frontend tag `latest` ([file compose](https://github.com/bablsoft/accessflow/blob/2ba5d322e7e1b4c750b5b0af85935e9ae814bd6a/docker-compose.yml)). Hai tag trả OCI index linux/amd64 và linux/arm64. Backend config không có labels. Frontend chỉ có maintainer NGINX. Không có source revision trong config; tag latest mutable và không ràng buộc digest vĩnh viễn với release source. Coordinator đã so sánh bốn file source quan trọng giữa `v2.7.0` và pin review; chúng byte-identical, nhưng điều đó không xác định layer của hai image.
- **Archery:** `ghcr.io/hhyo/archery:v1.14.0` và Docker Hub tag được [compose](https://github.com/hhyo/Archery/blob/master/src/docker-compose/docker-compose.yml) tham chiếu trả cùng manifest digest. Config linux/amd64 có `org.opencontainers.image.version=v1.14.0`, `revision=bc1f10ef...`, `licenses=Apache-2.0` và source URL. Revision khớp release commit đã kiểm. Đây là provenance label hữu ích, không phải SBOM hay xác nhận Oracle Instant Client trong image.
- **Bytebase:** `docker.io/bytebase/bytebase:3.23.0` trả OCI index cho linux/amd64 và linux/arm64. Config có version `3.23.0` nhưng revision `ab8b8a4e...`, khác GitHub release tag commit `c8188c63...`. Chưa xác định nguyên nhân hoặc quan hệ ancestry. Hai descriptor `unknown/unknown` có thể là metadata/attestation; không suy kiến trúc runnable từ chúng.

## Ranh giới kết luận

1. Registry manifest xác nhận tag trỏ tới digest tại thời điểm truy vấn. Tag có thể đổi về sau. Dùng digest cụ thể khi pin POC.
2. Config labels là metadata do builder phát ra. Labels rỗng hoặc khác SHA không chứng minh lỗi build; chúng chỉ để lại provenance gap.
3. SHA-256 của CloudDM offline archive khác OCI manifest digest và không thể dùng thay thế lẫn nhau.
4. Không có SBOM nào được truy xuất trong lượt này. Config labels, source license và tag release không xác nhận giấy phép mọi layer.
5. Registry pin không chứng minh Oracle runtime, SQL behavior, entitlement, migration correctness hoặc performance.

## MetaDB ODC

Coordinator đã pin source OceanBase `v4.3.5_CE` tại `5d6cb5cbc3f7c1ab6eb22e40abec8e160a8764d5` và xác nhận file `LICENSE` là **MulanPubL-2.0**. Đây là license của source tag đó, không phải license ODC Apache-2.0. Runtime lịch sử dùng image tag `oceanbase/oceanbase-ce:4.3.5-lts`; hiện chưa có build provenance chứng minh tag image này được tạo từ source tag `v4.3.5_CE`. Vì vậy không gán MulanPubL-2.0 cho toàn bộ image nếu chưa kiểm thành phần/layer và quan hệ build. Đánh giá license của image MetaDB phải tách khỏi ODC và giữ trạng thái chưa xác định.

## Security policy và contributor

GitHub Security Policy page được GET công khai ngày 2026-10-04 cho năm repo. ODC có `SECURITY.md` với route `security@oceanbase.com`, lời hứa liên hệ ban đầu trong 2 ngày làm việc, không nêu SLA remediation. CloudDM, AccessFlow, Archery và Bytebase cho biết chưa thiết lập `SECURITY.md`; chưa xác minh route disclosure/SLA riêng. GitHub “security and quality” counters không phải số CVE. Contributor tổng chưa lấy được do API rate limit; giữ UNKNOWN, không retry spam. Chi tiết đã cập nhật ở [maturity.csv](maturity.csv).

ODC reference image tag is in the [official README](https://github.com/oceanbase/odc/blob/main/README.md). Bytebase registry metadata came from the public [Docker Hub repository](https://hub.docker.com/r/bytebase/bytebase).
