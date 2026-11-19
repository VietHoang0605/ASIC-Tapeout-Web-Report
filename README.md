# ASIC Silicon Tapeout — Hành Trình Từ RTL Đến GDSII (SkyWater 130nm)

> *"Trên Silicon không có nút Ctrl+Z."*  
> Điều gì thực sự diễn ra khi biến những dòng code Verilog trừu tượng thành một con chip vật lý sẵn sàng gửi đi xưởng đúc (Foundry)?

> ### 🎓 Người Hướng Dẫn Khóa Học: **HUỲNH QUANG HUY** *(CTW SEMI · SILK-FPGA)*
> Toàn bộ chương trình đào tạo, tài liệu lý thuyết, bộ bài Lab thực hành và định hướng chuyên môn Physical Design được giảng dạy và dẫn dắt trực tiếp bởi **Thầy Huỳnh Quang Huy** tại lớp [**SILK-FPGA/RTL2GDS_CLASS**](https://github.com/SILK-FPGA/RTL2GDS_CLASS).

🔗 **Đọc báo cáo tương tác trực tuyến:** [**asic-tapeout-web-report.vercel.app**](https://asic-tapeout-web-report.vercel.app)  
👤 **Học viên thực hiện:** Trương Công Việt Hoàng · **Công nghệ:** SkyWater 130nm (`sky130A`) · **EDA:** OpenROAD / LibreLane (CTW SEMI)

---

## 💡 Bạn sẽ tìm thấy gì trong báo cáo này?

Không dừng ở lý thuyết sách vở hay chạy tool kiểu "hộp đen", kho tài liệu này là nhật ký thực chiến giải phẫu tận gốc bản chất vật lý bán dẫn qua từng công đoạn làm chip:

* **Khi code hóa thành phần cứng:** Trình tổng hợp (`Yosys + ABC`) dựa vào đâu trong thư viện `.lib` để chọn từng bóng bán dẫn và đánh đổi giữa **Diện tích (Area)** với **Tốc độ (Delay)**?
* **Cuộc chiến ở thang đo Picosecond:** Vì sao lỗi *Setup* chỉ làm chip chạy chậm, nhưng lỗi *Hold* lại biến chip thành "cục gạch" vĩnh viễn? Cách khóa ràng buộc **SDC** và săn lùng đường găng (**Critical Path**) qua 9 góc vận hành khắc nghiệt (**PVT Corners**).
* **Giải cứu chip trên mặt phẳng vật lý:** Chuyện gì xảy ra khi thuật toán sửa timing làm "nổ mật độ cell" gây tắc nghẽn dây kim loại, hoặc khi công cụ tối ưu vô tình xóa mất các mắt trễ chức năng của mạch?
* **Chốt chặn cuối trước giờ Tape-out:** Cách đọc cơ sở dữ liệu `.odb`, điều khiển **OpenROAD GUI/TCL**, trích xuất ký sinh dây dẫn thực tế (`SPEF/SDF`) và kiểm chứng sóng sau bố trí bằng **CVC64 & GTKWave**.

---

## 🗺️ Lộ trình 5 Buổi (Lab 0 – Lab 3)

* **Buổi 01 · [`Buoi_1/`](./Buoi_1) — Nhập môn RTL-to-GDSII & Floorplanning:** Mô phỏng kiểm thử Front-End, vận hành dây chuyền PnR và bắt bệnh tràn mật độ bố trí vật lý (`counter.v`, Lab 0).
* **Buổi 02 · [`buoi_2/`](./buoi_2) — Logic Synthesis & Standard Cells:** Giải mã cỗ máy ánh xạ công nghệ, đọc hiểu tệp Liberty (`.lib`) và thực nghiệm chiến lược tổng hợp trên mạch số (RCA 8-bit, Lab 1).
* **Buổi 03 · [`buoi_3/`](./buoi_3) — Static Timing Analysis (STA) & Timing Closure:** Thiết lập khế ước thời gian SDC, phân tích đa góc PVT và bứt phá giới hạn tần số bằng cải tiến kiến trúc RTL (`mult.v`, Lab 2).
* **Buổi 04 & 05 · [`buoi_4+5/`](./buoi_4+5) — Physical Design, ODB & Post-Layout Signoff:** Giải phẫu 72+ bước PnR trên **CPU 8-bit** (`tt_um_dvxf_dj8`) và chip đo thời gian tinh **TinyTDC** — từ xử lý nghẽn định tuyến đến mô phỏng Gate-Level sau đi dây (CVC64 + GTKWave, Lab 3).

---

## 🖥️ Trải nghiệm trên Web Report

Truy cập trực tiếp bản web tương tác tại **[https://asic-tapeout-web-report.vercel.app](https://asic-tapeout-web-report.vercel.app)**:

* **3 góc nhìn trong 1 trang:** *Giáo trình Lý thuyết* · *Hướng dẫn Thực hành Lab* · *Báo cáo Nghiệm thu*.
* **Soi chi tiết bản vẽ Silicon:** Tích hợp **Lightbox phóng đại $0.4\times - 6.0\times$** cho sơ đồ kiến trúc, bản đồ nhiệt (Heatmap), layout OpenROAD và giản đồ xung GTKWave.
* **Tra cứu kỹ thuật tức thì:** Tìm kiếm nhanh toàn văn theo hiện tượng vật lý, mã lỗi EDA hoặc kịch bản lệnh (`Verilog`, `SDC`, `TCL`).

---

## 🚀 Tải toàn bộ kho tài liệu học tập (Local)

```bash
git clone https://github.com/VietHoang0605/ASIC-Tapeout-Web-Report.git
cd ASIC-Tapeout-Web-Report
```
Kho lưu trữ bao gồm toàn bộ tài liệu Markdown, slide bài giảng (`.pptx`), đề Lab (`.pdf`), mã nguồn RTL/SDC, báo cáo timing, ảnh minh chứng thực hành từ [`Buoi_1/`](./Buoi_1) đến [`buoi_4+5/`](./buoi_4+5), cùng tài liệu hướng dẫn môi trường [`CTW_SEMI_Huong_dan_chay.docx`](./CTW_SEMI_Huong_dan_chay.docx) *(các video ghi hình dung lượng lớn được lược bỏ để tối ưu kho lưu trữ)*.
