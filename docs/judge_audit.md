# Judge audit — LogiX-VN

Các số liệu dưới đây lấy từ `lab9.judge` trên hai CSV replay. Lớp dương là FAIL.

| Tiêu chí | n | κ | Precision | Recall | TP / FP / FN / TN | Tỉ lệ lỗi quan sát → hiệu chỉnh | Quyết định |
|---|---:|---:|---:|---:|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | 24 / 4 / 6 / 66 | 28% → 30% | Đạt cả ba sàn. Có thể dùng cho tone trên phạm vi đã hiệu chuẩn. |
| helpful | 100 | 0.375 | 1.000 | 0.300 | 9 / 0 / 21 / 70 | 9% → 30% | Loại khỏi gate. Kappa và recall dưới sàn. |

## Audit bất đồng

| Case | Judge | Người | Kết luận và sửa rubric |
|---|---|---|---|
| H-008 | PASS | FAIL | Theo chuẩn CSKH của bài, cách xưng hô “em” kèm “nha” quá suồng sã. Thêm ví dụ chấm FAIL cho tổ hợp này trong thông báo hoàn tiền. |
| H-017 | PASS | FAIL | Nhãn người hợp lý theo ngữ cảnh khách lớn tuổi ghi trong CSV. Cung cấp ngữ cảnh tuổi/cách xưng hô cho judge. Quy định dùng “anh/chị” khi chưa rõ cách gọi phù hợp. |
| H-029 | PASS | FAIL | Nhãn người hợp lý. “Không cần nhắn thêm” làm khách khó theo dõi yêu cầu. Chấm toàn câu và trừ điểm cho câu đóng kênh hỗ trợ mà thiếu lý do hoặc bước tiếp theo. |
| H-042 | FAIL | PASS | Nhãn người hợp lý. Reply xác nhận kết quả và thời gian nhận tiền. Cho PASS với câu ngắn, lịch sự, đủ nội dung dù thiếu lời xin lỗi. |
| H-051 | FAIL | PASS | Nhãn người hợp lý theo danh mục từ CSKH cho phép. Thêm “refund” vào ví dụ thuật ngữ được chấp nhận khi câu dễ hiểu. |
| HL-015 | PASS | FAIL | Nhãn người hợp lý. Reply nói 55.000 đồng, ledger ghi 40.000 đồng. Bắt buộc kiểm tra groundedness bằng code trước khi dùng đánh giá về helpfulness. |
| HL-016 | PASS | FAIL | Nhãn người hợp lý. Reply dài và lịch sự vẫn báo 55.000 đồng thay vì 35.000 đồng. Cho FAIL khi dữ kiện sai và dùng trường hợp này làm đối chứng cho thiên lệch theo độ dài. |
| HL-020 | PASS | FAIL | Nhãn người hợp lý. Reply báo 90.000 đồng thay vì 120.000 đồng. Thêm ví dụ cho cả lỗi báo thấp lẫn báo cao. |

Judge helpful bỏ sót 21/30 lỗi. Tiền và phê duyệt do code chấm. Cần người gắn nhãn một tập held-out mới trước khi suy rộng kết quả calibration ra ticket thực.
