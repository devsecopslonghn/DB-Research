# Demo `customer-profile`

Ứng dụng mẫu minh họa phát hành SQL Oracle qua Git PR, validation và fixture smoke trong Actions, đóng gói source đã commit, tạo batch ODC và xác minh bằng truy vấn chỉ đọc qua ODC. Tất cả đối tượng có tiền tố `DM_CP_`; bốn logical environment trỏ tới schema POC trên cùng một database. `MOCKPROD` không phải production.

| Logical stage | Native environment ID/name | Oracle schema |
| --- | --- | --- |
| DEV | `1` / `dev` | `ODC_POC_20261004_DEV` |
| SIT | `2` / `sit` | `ODC_POC_20261004_SIT` |
| UAT | `1000021` / `POCUAT` | `ODC_POC_20261004_UAT` |
| MOCKPROD | `1000022` / `POCPROD` | `ODC_POC_20261004_MOCKPROD` |

## Các release mẫu

| Release | Mục đích |
| --- | --- |
| `REL-2026.10-DEMO01` | Tạo bảng, sequence, index, function, view và ba dòng dữ liệu tổng hợp. |
| `REL-2026.10-DEMO02-FAIL` | Thành công ở DEV, sau đó cố ý phát sinh `ORA-20042` tại SIT trước lệnh tạo `DM_CP_CUSTOMER_REGION_IX`; batch phải dừng. |
| `REL-2026.10-DEMO02-FIX` | Release correction mới, khai báo sửa release thất bại; kiểm tra `USER_INDEXES` để giữ nguyên index đã tạo ở DEV và tạo index còn thiếu ở các stage sau. |

Không sửa release đã phát hành để “sửa tại chỗ”. Correction có manifest, hash, review và envelope riêng. Hệ thống không tự rollback, promote hay replay các stage.

SQL policy chặn `ALTER SYSTEM`, `ALTER USER`, `CREATE USER`, `DROP USER`, `GRANT DBA` và `GRANT ANY ...`; dynamic SQL qua `EXECUTE IMMEDIATE` hoặc `DBMS_SQL` luôn cần DBA review. Policy scan là lexical, nên review người vẫn cần thiết.

```mermaid
sequenceDiagram
  participant Dev as Developer
  participant GH as GitHub PR / Actions
  participant Rel as Release bundle
  participant ODC as ODC
  participant Ops as OWNER + DBA / operator
  participant DB as Oracle POC schemas
  Dev->>GH: Commit manifest và SQL
  GH->>GH: Static policy validation
  GH-->>Dev: Validation report
  Dev->>GH: Merge reviewed change
  GH->>Rel: Package exact committed bytes and hashes
  Rel->>ODC: Create singleton MULTIPLE_ASYNC batch (ABORT, retry 0)
  ODC-->>Ops: Native status and ticket
  Ops->>ODC: Review/approve in UI; manually continue one stage
  ODC->>DB: Execute DEV
  DB-->>ODC: Native result
  Ops->>ODC: Verify DEV with SELECT-only checks
  ODC->>DB: Objects, errors, data and function checks
  DB-->>ODC: DEV verification evidence
  Ops->>ODC: Review receipt; manually continue SIT
  ODC->>DB: Execute SIT
  DB-->>ODC: Native result
  Ops->>ODC: Verify SIT with SELECT-only checks
  ODC->>DB: Objects, errors, data and function checks
  DB-->>ODC: SIT verification evidence
  Ops->>ODC: Review receipt; manually continue UAT
  ODC->>DB: Execute UAT
  DB-->>ODC: Native result
  Ops->>ODC: Verify UAT with SELECT-only checks
  ODC->>DB: Objects, errors, data and function checks
  DB-->>ODC: UAT verification evidence
  Ops->>ODC: Review receipt; manually continue MOCKPROD
  ODC->>DB: Execute MOCKPROD
  DB-->>ODC: Native result
  Ops->>ODC: Verify MOCKPROD with SELECT-only checks
  ODC->>DB: Read-only validity, object, data and function queries
  DB-->>ODC: Query results
  ODC-->>Ops: Verification receipt
  Ops->>Rel: Collect receipts and generate evidence/report
```

## Bắt đầu cục bộ

Từ root repository, dùng Python 3.11+ và cài dependency đã pin. Workflow `db-validate` kiểm tra cả ba release và package fixture reports; PR cũng chạy `db-report` fixture smoke:

```bash
python3 -m pip install -r scripts/db_demo/requirements.txt
python3 -m unittest discover -s scripts/db_demo/tests -v
python3 -m scripts.db_demo.validate_manifest --output /tmp/db-demo-validation
```

Lệnh validation không thực thi SQL. Tạo release yêu cầu source release và cấu hình đã commit:

```bash
python3 -m scripts.db_demo.build_release --release-id REL-2026.10-DEMO01 --output /tmp/db-demo-release
```

Live workflow `db-release` cần có trên `refs/heads/main` và protected environment `odc-demo` được cấu hình deployment branches/reviewers. Fixture smoke không phải kết quả runtime. Xem [quy trình phát hành](docs/release-process.md) để biết các lệnh tích hợp, thu evidence và kiểm tra Oracle.

## Tài liệu

- [Kiến trúc](docs/architecture.md)
- [Quy trình phát hành](docs/release-process.md)
- [Hướng dẫn operator](docs/operator-guide.md)
- [Thất bại và correction](docs/failure-and-correction.md)
- [Trước và sau](docs/before-after.md)
