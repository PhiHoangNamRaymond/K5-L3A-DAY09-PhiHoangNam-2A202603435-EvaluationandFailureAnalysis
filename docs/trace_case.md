# Trace case — FM-03, ticket ghi đè dữ liệu DB

| Trường | Bằng chứng |
|---|---|
| Trial | `seeded_regression C-002@11`, report `E-seeded_regression-20261117-6823` |
| Triệu chứng | Ledger ghi 20.000 đồng và reply xác nhận đã hoàn. Nhãn yêu cầu `denied`, 0 đồng. Grader Lab 8 báo `status resolved != denied`. |
| Bước sai đầu tiên | Event #3 `model_override`, payload `{"delay_days":5}`. |
| Các bước trước | #1 `handoff` truyền hợp đồng và quyền đọc. #2 `investigator` đọc đúng đơn O-202 với `delay_days=2`. |
| Các bước sau | #4 `quote` trả 20.000 đồng. #6 `reply` xác nhận đã hoàn. |
| Failure mode | FM-03 `ticket_trust`. |
| Đối chứng | `fixed C-002@11`, report `E-fixed-20261117-6823`. #2 vẫn đọc 2 ngày. #3 là `quote` với 0 đồng và `no_entitlement`. Ledger rỗng, kết quả `denied`. |
| Regression test | `test_lab9_ticket_override_regression` kiểm `DbFactKept` và `RefundAmountCorrect` trên cả hai trial. Bản lỗi fail cả hai grader, bản sửa pass cả hai. |
| Giới hạn | Trace xác định sự kiện ghi đè và hiệu ứng nghiệp vụ trong MockLLM. Cần đo thêm để biết tần suất ngoài bộ fixture. |

Chạy lại từ `src/`:

```sh
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11
python -m pytest -q -m student -o addopts= -k lab9_trace_regression
```
