# Lời thuyết minh tiếng Việt

Giọng tổng hợp cục bộ: Piper / vi_VN-vais1000-medium. Mỗi đoạn phụ đề gắn với đúng WAV đã tổng hợp; không gửi lời dẫn hay ảnh tới TTS bên ngoài. Chính tả sản phẩm và ID giữ trong phụ đề; đầu vào đọc dùng bảng phát âm trong render.py.

## 01 · 00:00 · Một thay đổi mới, một chuỗi bằng chứng

Ảnh gốc: [screenshots/07-current-community-edition.png](../screenshots/07-current-community-edition.png).

Đây là demo lab, trình bày từ ảnh chụp thực nghiệm.

Chúng ta theo dõi một thay đổi SQL mới, từ GitHub qua Jenkins và Bytebase đến Oracle.

Lab đang dùng bản Community, phiên bản ba chấm hai mươi hai chấm một.

## 02 · 00:11 · PR #9: SQL và recovery cùng nằm trong Git

Ảnh gốc: [screenshots/11-pr9-reviewed-sql-diff.png](../screenshots/11-pr9-reviewed-sql-diff.png).

Điểm bắt đầu là PR số chín, với một thay đổi cơ sở dữ liệu mới và ghi chú khôi phục đi kèm.

SQL tạo riêng một bảng POC, có khóa chính trên cột ID; không sửa bảng ứng dụng.

Phiên bản một chấm không chấm không chấm mười được chọn sau khi kiểm tra lịch sử của database.

## 03 · 00:26 · PR-9 #2 nhận đúng source SHA

Ảnh gốc: [screenshots/13b-ci-pr9-reviewed-build.png](../screenshots/13b-ci-pr9-reviewed-build.png).

Jenkins tiếp nhận bản sửa cuối của PR trong bản dựng số hai.

Bản dựng thành công và lưu kết quả kiểm tra vào tệp kết quả kiểm tra SQL.

Mã băm tại mục Revision trùng với commit nguồn đã được kiểm tra.

## 04 · 00:38 · Review cuối: vẫn còn 3 WARNING

Ảnh gốc: [screenshots/14b-pr9-reviewed-findings.png](../screenshots/14b-pr9-reviewed-findings.png).

Kết quả kiểm tra của PR số chín có không lỗi và ba cảnh báo, không phải hoàn toàn không có phát hiện từ kiểm tra.

Một cảnh báo cho biết file phiên bản không đã khác bản áp dụng từ trước.

Hai cảnh báo còn lại liên quan tên bảng và cách quy tắc nhận diện giá trị mặc định của cột ID.

Cấu hình hiện có chỉ thất bại khi có lỗi. Không có việc đổi chính sách hoặc bỏ kiểm tra để chạy qua.

## 05 · 00:57 · Kết quả đã được công bố lên PR

Ảnh gốc: [screenshots/15b-pr9-bytebase-native-summary.png](../screenshots/15b-pr9-bytebase-native-summary.png).

Kết quả từ Bytebase được action công bố thành comment tổng hợp trên PR.

Jenkinsfile còn tạo một bảng chi tiết riêng, có liên kết tới đúng bản dựng Jenkins.

Ảnh này được chụp lại sau khi gộp mã. Comment CI không phải là phê duyệt trên giao diện Bytebase.

## 06 · 01:10 · Kiểm tra đúng head trước khi merge

Ảnh gốc: [screenshots/16b-git-reviewed-head-success.png](../screenshots/16b-git-reviewed-head-success.png).

Trước khi gộp mã, đúng commit cuối có cả hai trạng thái kiểm tra thành công.

Cần phân biệt kiểm tra của PR với bản dựng nhánh; một bản dựng nhánh xanh riêng lẻ không thay thế kiểm tra SQL.

Các kiểm tra xanh tự chúng chưa chứng minh Git cưỡng chế chặn gộp mã.

## 07 · 01:24 · PR #9 đã merge vào master

Ảnh gốc: [screenshots/17-pr9-merged.png](../screenshots/17-pr9-merged.png).

PR số chín được gộp vào master. Mã băm commit sau khi gộp được lưu lại.

Mã băm này là đầu mối để nối sang bản dựng triển khai tiếp theo.

Vì vậy, bộ bằng chứng này không được dùng để kết luận đã có phân tách trách nhiệm phê duyệt.

## 08 · 01:35 · master #12 nhận đúng merge commit

Ảnh gốc: [screenshots/18-master12-merge-checkout.png](../screenshots/18-master12-merge-checkout.png).

Webhook hiện có đưa thay đổi vào bản dựng master số mười hai.

Bản dựng này thành công, lấy mã nguồn đúng commit sau khi gộp mã của PR số chín.

Đây là bản dựng mới, không phải một lần thực thi cũ được ghép vào câu chuyện.

## 09 · 01:48 · Console nối build với Release và Plan

Ảnh gốc: [screenshots/19-master12-release-plan-links.png](../screenshots/19-master12-release-plan-links.png).

Console Jenkins ghi các liên kết thật tới bản phát hành mới và Plan một trăm mười bốn.

Sau khi gộp mã, quy trình hiện có tự triển khai vào môi trường develop.

Không có bước chờ người bấm triển khai hay phê duyệt độc lập nào được chứng minh trong luồng này.

## 10 · 02:00 · SQL trong Release khớp bản đã review

Ảnh gốc: [screenshots/21-bytebase-release-reviewed-sql.png](../screenshots/21-bytebase-release-reviewed-sql.png).

Trong Bytebase, chi tiết bản phát hành lưu đúng file SQL phiên bản mười và mã băm nội dung.

SQL tại commit nguồn, commit sau khi gộp mã và nội dung trong bản phát hành đã được đối chiếu giống nhau từng byte.

Không thấy liên kết commit tích hợp sẵn ở màn hình này; chuỗi nguồn được nối bằng Jenkins và mã băm thực tế.

## 11 · 02:17 · Plan 114: tác vụ mới đã hoàn tất

Ảnh gốc: [screenshots/22-bytebase-new-rollout-done.png](../screenshots/22-bytebase-new-rollout-done.png).

Plan một trăm mười bốn ghi trạng thái đã triển khai và một tác vụ hoàn tất trên đúng đích triển khai Oracle.

Danh tính thực thi là tài khoản dịch vụ của Jenkins, tại môi trường develop.

Bản phát hành có bảy file, nhưng dấu vết lần chạy này chỉ có phiên bản mười.

Tác vụ thành công vẫn cần được đối soát với trạng thái database.

## 12 · 02:34 · Đối soát đúng bảng vừa tạo

Ảnh gốc: [screenshots/25-oracle-new-object-live-query.png](../screenshots/25-oracle-new-object-live-query.png).

Một truy vấn đọc mới được chạy trên đúng bảng POC vừa tạo, trong lược đồ đã cấp.

Đường truy vấn đi qua SQL Editor của Bytebase tới Oracle.

Kết quả đếm bằng không, với thời gian truy vấn hai trăm bốn mươi ba mili giây.

Bảng rỗng đúng chủ đích vì thay đổi cơ sở dữ liệu không thêm dữ liệu. Đây là đối soát bổ sung cho trạng thái tác vụ thành công, không phải số dòng ước tính của catalog.

## 13 · 02:54 · Rời execution rồi tìm lại từ project

Ảnh gốc: [screenshots/28-find-new-plan-in-project-history.png](../screenshots/28-find-new-plan-in-project-history.png).

Sau khi bản dựng kết thúc, phiên demo rời trang thực thi và quay về danh sách kế hoạch của dự án.

Plan một trăm mười bốn vẫn được tìm thấy, cùng tên bản phát hành, người tạo và kết quả giai đoạn develop.

Dấu gạch ở cột Review không chứng minh có phê duyệt của con người.

## 14 · 03:08 · Mở lại kết quả của cùng Plan 114

Ảnh gốc: [screenshots/29-reopened-new-plan-history.png](../screenshots/29-reopened-new-plan-history.png).

Từ danh sách, mở lại đúng Plan một trăm mười bốn vẫn thấy đích triển khai, danh tính và kết quả của tác vụ.

Có thể lần sang bản phát hành để đọc lại SQL, và sang Jenkins để nối với nguồn Git.

Không đánh đồng lịch sử tác vụ với nhật ký kiểm toán đầy đủ, hoặc với toàn bộ console của hệ thống CI.

## 15 · 03:25 · PR #10: ca âm chỉ phục vụ review

Ảnh gốc: [screenshots/80-pr10-review-only-source.png](../screenshots/80-pr10-review-only-source.png).

Ca kiểm tra âm được đặt trong PR số mười, tách riêng khỏi thay đổi đã triển khai.

SQL cố ý khai báo bảng thiếu khóa chính để kiểm tra một quy tắc Oracle đang bật.

Chú thích SQL ghi rõ chỉ kiểm tra, không gộp mã và không triển khai.

File phiên bản mười một trên PR này không có nghĩa database đã áp dụng phiên bản đó.

## 16 · 03:42 · Rule trả ERROR 601 vì thiếu khóa chính

Ảnh gốc: [screenshots/82b-pr10-missing-pk-final-finding.png](../screenshots/82b-pr10-missing-pk-final-finding.png).

Tệp kết quả của bản dựng PR mười, lần hai, ghi lỗi thiếu khóa chính, mã sáu trăm linh một.

Kết quả cuối có một lỗi và hai cảnh báo.

Đây là phát hiện do Bytebase trả trong bước kiểm tra của CI, chưa phải lỗi khi chạy thay đổi cơ sở dữ liệu trên Oracle.

Không đổi chính sách và không triển khai SQL vi phạm để tạo cảnh lỗi.

## 17 · 04:00 · PR-10 #2 thực sự thất bại

Ảnh gốc: [screenshots/81-pr10-build2-failure.png](../screenshots/81-pr10-build2-failure.png).

Bản dựng PR mười, lần hai, thất bại trên đúng commit chứa SQL thiếu khóa chính.

Jenkins vẫn giữ tệp kết quả kiểm tra để tra cứu nguyên nhân.

Bản dựng của PR không đi vào các giai đoạn triển khai chỉ dành cho master.

## 18 · 04:12 · Check lỗi chưa đồng nghĩa Git cấm merge

Ảnh gốc: [screenshots/84-pr10-git-status-failure.png](../screenshots/84-pr10-git-status-failure.png).

GitHub nhận kiểm tra lỗi của PR, trong khi bản dựng nhánh vẫn xanh.

Tuy nhiên, master chưa có các kiểm tra bắt buộc cưỡng chế chặn gộp mã. Không thể kết luận Git bắt buộc cấm gộp mã chỉ từ ảnh này.

Bộ demo đã nối mã nguồn, kiểm tra, lần thực thi mới, đối soát Oracle và tra cứu kết quả.

Những phần chưa chứng minh gồm phê duyệt độc lập, phân quyền bằng tài khoản ít quyền và thực nghiệm Flyway.

Các giới hạn này được giữ nguyên khi dùng video để so sánh quy trình thay đổi cơ sở dữ liệu.

Bytebase/Jenkins/Oracle dùng bộ phát âm của Piper; GitHub dùng “Ghít Hắp”, SQL dùng “ét kiu eo”, PR dùng “pi a”. Số quan trọng được viết thành chữ trong lời đọc. Phụ đề giữ tên sản phẩm; không giả giọng người thật.
