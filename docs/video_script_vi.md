# Kịch bản video demo VietLearn Agent

Thời lượng mục tiêu: 90–120 giây. Quay màn hình, thuyết minh tiếng Việt; có thể bật phụ đề tự động tiếng Anh trên YouTube.

## Cảnh 1 — Vấn đề (0:00–0:15)

Hiển thị thumbnail và tiêu đề.

> Nhiều người Việt muốn học các khóa công nghệ quốc tế nhưng gặp hai rào cản: tiếng Anh và kiến thức nền tảng. VietLearn Agent không chỉ dịch, mà còn chẩn đoán, dạy, kiểm tra và điều chỉnh bài học.

## Cảnh 2 — Kiến trúc ADK (0:15–0:40)

Hiển thị ADK graph hoặc sơ đồ trong README.

> Learning Coach điều phối ba agent chuyên trách. Diagnostic Agent xác định năng lực người học. Tutor Agent lấy tài liệu qua MCP và dùng Agent Skill để giảng bằng tiếng Việt. Evaluator Agent phát hiện hiểu lầm và đề xuất bài tiếp theo. Các agent trao đổi qua shared session state.

## Cảnh 3 — MCP, Skill và bảo mật (0:40–1:00)

Hiển thị cây thư mục hoặc các file `course_server.py`, `SKILL.md`, `security.md`.

> MCP chỉ có hai tool đọc là search materials và get lesson. Agent Skill chứa quy trình, tài liệu tham chiếu, mẫu bài học và script kiểm tra. Nội dung lấy về được coi là dữ liệu không đáng tin cậy; prompt injection bị chặn và secret không được ghi vào trace.

## Cảnh 4 — Demo (1:00–1:25)

Chạy `python scripts/demo_learning_flow.py`.

> Demo tạo learner profile, kiểm tra lộ trình đúng năm ngày, đánh giá tính an toàn, bám nguồn và cá nhân hóa. Khi phát hiện người học nhầm API với Tool, hệ thống đề xuất dạy lại bằng một ví dụ đơn giản hơn.

## Cảnh 5 — Kiểm thử và kết thúc (1:25–1:45)

Chạy `python -m pytest` và dừng ở dòng `39 passed`.

> Ba mươi chín test kiểm tra kiến trúc multi-agent, MCP read-only, guardrail, prompt injection, eval và observability. Mã nguồn đầy đủ được công khai trên GitHub. VietLearn hướng tới việc giúp người Việt tiếp cận kiến thức công nghệ toàn cầu một cách an toàn và phù hợp với năng lực cá nhân.
