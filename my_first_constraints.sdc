################################################################################
# KHẾ ƯỚC THỜI GIAN THIẾT KẾ (SDC - SYNOPSYS DESIGN CONSTRAINTS)
# Cấu trúc: Giàn giáo kiểm soát không-thời gian silicon
# Quy tắc: TUYỆT ĐỐI không thay đổi giao ước vật lý nếu chưa tính toán kỹ lưỡng.
################################################################################

# ==============================================================================
# HỆ THỐNG ĐƠN VỊ VẬT LÝ MẶC ĐỊNH
# ==============================================================================
# Các công cụ tổng hợp logic và kiểm định thời gian tĩnh (STA) neo hệ quy chiếu
# theo thư viện công nghệ tế bào chuẩn (standard cell library):
#   - Thời gian (Time)        : Thường quy ước là Nanosecond (ns)
#   - Điện dung (Capacitance) : Thường quy ước là Picofarad (pF)
# Người học phải tự kiểm chứng bảng đặc tính công nghệ trước khi áp số đo.

# ==============================================================================
# 1. BƠM NHỊP ĐỒNG HỒ CHỦ (PRIMARY CLOCK GENERATION)
# ==============================================================================
# Ẩn dụ vật lý:
#   Thiết lập một con lắc điều hòa vĩ mô bơm xung năng lượng tuần hoàn qua cổng
#   nạp vật lý 'clk'. Dao động này đóng vai trò nhịp tim định chuẩn cho toàn bộ
#   mạng lưới thanh ghi nội tại.
# Mục tiêu & Kết quả mong đợi:
#   Khởi tạo một nguồn xung nhịp có tần số vật lý f = 50 MHz neo vào đúng cổng 'clk'.
#   Công cụ STA phải nhận diện được chu kỳ bước sóng cơ sở và tỉ lệ pha (duty cycle 50%)
#   để phân định ranh giới giữa các thế hệ dữ liệu.
#
# [TODO 1: Khởi tạo nguồn nhịp đập chính gắn với cổng 'clk']
# Ghi chú định hướng:
#   - Tự quy đổi tần số dao động f = 50 MHz thành chu kỳ thời gian tương ứng theo đơn vị chuẩn.
#   - Tra cứu cú pháp thiết lập nhịp đồng hồ cơ sở để khai báo chu kỳ và trỏ chính xác vào cổng thu năng lượng.
# ------------------------------------------------------------------------------

# [TODO: Viết câu lệnh thiết lập nhịp đồng hồ chính tại đây]


# ==============================================================================
# 2. KHẮC PHỤC RUNG LẮC PHA VÀ BIẾN THIÊN NHIỆT ĐỘNG (CLOCK UNCERTAINTY)
# ==============================================================================
# Ẩn dụ vật lý:
#   Không có con lắc nào gõ nhịp hoàn hảo trong thế giới vật lý thực. Mạng phân phối
#   nhịp (clock tree) phải chịu rung lắc pha (jitter) từ bộ dao động và sai lệch
#   thời gian đến (skew) do biến thiên quy trình sản xuất, sụt áp và biến thiên nhiệt độ (PVT).
# Mục tiêu & Kết quả mong đợi:
#   Khai trừ thẳng một khoản đệm an toàn vật lý chiếm đúng 10% chu kỳ bước sóng vừa tính.
#   Khoản dung sai này buộc công cụ phân tích phải siết chặt biên an toàn cả ở bờ thiết lập (setup)
#   lẫn bờ duy trì (hold), ngăn ngừa hiện tượng bất định trạng thái (metastability) tại các cổng chốt.
#
# [TODO 2: Khóa biên độ bất định nhịp chiếm 10% chu kỳ]
# Ghi chú định hướng:
#   - Tính toán lượng thời gian tương đương với 10% chu kỳ con lắc đã xác định ở Bước 1.
#   - Tra cứu câu lệnh gán biên độ bất định (uncertainty) cho nhịp đồng hồ chủ để đặt cọc biên độ dự phòng.
# ------------------------------------------------------------------------------

# [TODO: Viết câu lệnh khóa độ bất định thời gian của nhịp tại đây]


# ==============================================================================
# 3. KHOẢN NỢ THỜI GIAN NGOẠI VI (INPUT DELAY CONSTRAINT)
# ==============================================================================
# Ẩn dụ vật lý:
#   Trước khi gói điện tích chạm tới chân đế (pad) của vi mạch, nó đã phải tiêu tốn
#   thời gian di chuyển dọc theo các vết đồng trên bo mạch và vượt qua các cổng logic
#   bên ngoài. Đó là phần ngân sách bước sóng đã bị thế giới bên ngoài tiêu lạm.
# Mục tiêu & Kết quả mong đợi:
#   Khống chế ngân sách trôi dạt của các luồng tín hiệu đầu vào chiếm đúng 20% chu kỳ
#   bước sóng của nhịp đồng hồ tham chiếu. Điều này bảo đảm logic bên trong chip biết
#   chính xác nó chỉ còn lại 80% thời gian của nhịp để hoàn tất việc chuyển mạch trước kỳ gõ nhịp kế tiếp.
#
# [TODO 3: Ràng buộc độ trễ thâm nhập ngoại vi bằng 20% chu kỳ]
# Ghi chú định hướng:
#   - Tính toán lượng thời gian chiếm dụng (20% của chu kỳ ở Bước 1).
#   - Tra cứu câu lệnh ràng buộc độ trễ đầu vào liên kết với nhịp đồng hồ tương ứng lên toàn bộ các cổng nhận dữ liệu ngoại vi.
# ------------------------------------------------------------------------------

# [TODO: Viết câu lệnh khống chế độ trễ ngõ vào ngoại vi tại đây]


################################################################################
# HẾT KHUNG GIÀN GIÁO - YÊU CẦU ĐIỀN ĐỦ MÃ LÕI TRƯỚC KHI CHẠY PHÂN TÍCH STA
################################################################################
