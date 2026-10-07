# ODC: source review và đối chứng lịch sử

**Cập nhật nghiên cứu sâu 2026-10-04:** đọc [source trace mới](../../research-round-2/coordinator/oracle-governance-source.md), [license/release](../../research-round-2/licensing/licensing-review.md) và [shortlist hiện tại](../../shortlist.md). Phần dưới giữ snapshot T03 đầu; kết luận mới được ghi riêng, runtime mới vẫn NOT_RUN.

Ngày: 2026-10-04. Category A. Runtime mới: NOT_RUN.
Source backend pin `d517c0f27971642fb0cd7565fd61ab2309875ec3`.
Frontend pin `273fa3c4cc7d87f942ade231ce9220b98fa595e2`.
Đây là snapshot đã kiểm. Không coi source pin đó tự chứng minh build runtime tương ứng.
Runtime lịch sử dùng ODC 4.4.1-20260116, Oracle 26ai 23.26.4.1.0 và TCPS wrapper cục bộ.

| Nhận định | Loại | Bằng chứng và giới hạn |
| --- | --- | --- |
| Backend và frontend có license Apache-2.0 | SOURCE | [Backend LICENCE](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/LICENCE#L1-L202), [frontend LICENSE](https://github.com/oceanbase/odc-client/blob/273fa3c4cc7d87f942ade231ce9220b98fa595e2/LICENSE#L1-L202). Không mở rộng license đó sang MetaDB, image, JDBC driver hoặc mọi dependency. |
| Có project ownership và UI project | SOURCE | [ProjectEntity.java](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/metadb/collaboration/ProjectEntity.java#L1-L80), [Project UI](https://github.com/oceanbase/odc-client/blob/273fa3c4cc7d87f942ade231ce9220b98fa595e2/src/page/Project/index.tsx#L1-L370). Không chỉ dựa nhãn Web UI để phân loại A. |
| Có native batch model cho nhiều target theo thứ tự | SOURCE | [MultipleDatabaseChangeParameters.java](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/model/MultipleDatabaseChangeParameters.java#L36-L67), [executor](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/MultipleDatabaseChangeRuntimeFlowableTask.java#L1-L347). Model không chứng minh enforced promotion runtime. |
| Batch docs hỗ trợ serial/parallel, manual control và 2–100 target tasks | DOC | [Pinned batch guide](https://github.com/oceanbase/odc-doc/blob/40dc7c03522fef1968bd11b2b051bc216091e60d/en-US/700.database-change-management/650.multiple-database-change.md#L1-L120). Chưa nghiệm thu native batch trong 45 ca lịch sử. |
| Có Oracle JDBC connector trong sản phẩm | SOURCE | [OracleConnectionExtension.java](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/plugins/connect-plugin-oracle/src/main/java/com/oceanbase/odc/plugin/connect/oracle/OracleConnectionExtension.java#L52-L124). Plugin tích hợp khác wrapper TCPS được thêm tại deployment. |
| Oracle SQL/PLSQL và approval đã chạy một phần | RUNTIME lịch sử | [45 ca ODC](../../../ODC-ORACLE-POC-RESULTS.md), [JSON gốc](../../../evidence/oracle-poc-cases.json). 12 PASS, 20 PARTIAL, 5 FAIL, 8 NOT_RUN. Không dùng cho 19c/21c. |
| Replay/checksum/dedup và requester separation không đạt | RUNTIME lịch sử | REC-02, REC-08, REC-10 và GOV-03 FAIL. SQL-11 báo ticket success khi procedure INVALID. Không thay expected để đổi FAIL. |
| Promotion cần tách native khỏi runner ngoài | RUNTIME lịch sử | MODEL-07/GOV-04 PARTIAL: runner giữ cùng hash và thứ tự bốn ticket. Không chứng minh batch native đạt. |

## Đường thực thi và license gates

UI/API → ODC service/Flowable task → Oracle JDBC/task plugin → Oracle schema.
ODC giữ project/ticket/approval/result trong MetaDB trung tâm.
Chưa có ledger migration ID/checksum tại Oracle đích được chứng minh.
Deployment lịch sử dùng OceanBase CE 4.3.5 làm MetaDB. Đây là component license riêng.
TCPS wrapper/fallback tại deployment phải được ghi là custom adapter, không là khả năng native đã kiểm.
Không phát hiện paid user/instance gate trong các đường source đã đọc. Không chứng nhận unlimited image distribution.
[ODC-EVALUATION.md](../../../ODC-EVALUATION.md) ghi digest lịch sử và các component đã quan sát.

## Bước POC tiếp theo

T05 pin build/image/plugin/wrapper và kiểm license dependencies.
T06 kiểm DB user/role/grant, quyền kế thừa/expiry và Oracle denied thực tế.
T07 ưu tiên SQL-11, REC-02/08/10, partial DDL và central/target reconciliation.
T08 ưu tiên requester separation, immutable approval và ordered batch native.
T10 cần deployment riêng và crash checkpoints trước kiểm REC-05..07/11/12, GOV-06/07.
Không triển khai, test, SQL, service hoặc kiểm target trong source review này.
