# Mẫu video "bản 6" (Mr Di • Phân Tích Đất Nền)

Bố cục theo video đang chạy tốt nhất (8.390 lượt xem): ảnh vệ tinh thật ở nửa trên, nền đỏ gradient bên dưới,
tiêu đề cố định 2 dòng, chữ vàng đầu mỗi cảnh, các thẻ thông tin hiện dần và xếp chồng.

Tệp:
- gen.py: sinh vid/index.html cho HyperFrames. Sửa mảng `heads` (chữ vàng từng cảnh), `rows` (thẻ), `hook` (tiêu đề cố định), `B` (mốc cảnh), `sc` (zoom/di chuyển ảnh vệ tinh).
- tts.py: giọng KorvaTTS hoang_nam.
- sc.example.json, tm.example.json: ví dụ lời đọc từng cảnh và mốc thời gian câu.

Cần trong vid/assets: sat.jpg (ảnh vệ tinh anh Di gửi, cắt dọc), mix.mp3 (giọng + nhạc nền nhẹ 0.13), fonts/Inter-ExtraBold.otf, Inter-Bold.otf.
Render: `pkill -f chrome; npx -y hyperframes render --fps 24 --quality looks --output ../ep.mp4` (chạy foreground, khoảng 8 phút cho 59 giây).
Nén: `ffmpeg -i ep.mp4 -c:v libx264 -crf 24 -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart out.mp4`.
