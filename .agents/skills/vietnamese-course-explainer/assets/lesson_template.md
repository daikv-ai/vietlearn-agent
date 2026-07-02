# Mẫu bài học VietLearn

```yaml
day: 1-5
title: Tên bài học
objectives:
  - Kết quả quan sát được sau bài học
sections:
  - name: Giải thích
    minutes: 0
    content: Nội dung tiếng Việt
  - name: Ví dụ
    minutes: 0
    content: Ví dụ gắn với VietLearn
  - name: Thực hành
    minutes: 0
    content: Việc người học phải tự làm
  - name: Quiz
    minutes: 0
    content: Kiểm tra cuối bài
glossary:
  - term: English term
    meaning: Cách diễn giải tiếng Việt
quiz:
  - question: Câu hỏi chỉ dựa trên nội dung vừa học
    answer: Tiêu chí chấm hoặc đáp án
completion_criteria:
  - Điều kiện xác định người học đã đạt mục tiêu
```

## Quy tắc thời lượng

- Tổng `sections[].minutes` không vượt `max_minutes`.
- Không tạo Ngày 6.
- Thời gian thực hành nên bằng hoặc lớn hơn thời gian đọc thụ động nếu phù hợp.
