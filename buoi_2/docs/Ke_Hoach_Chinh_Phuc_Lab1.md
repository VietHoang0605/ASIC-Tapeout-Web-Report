# KẾ HOẠCH HÀNH ĐỘNG CHI TIẾT (MASTER PLAN)
# TỪ LÀM CHỦ KIẾN THỨC BUỔI 2 ĐẾN HOÀN THÀNH XUẤT SẮC LAB 1
*(Đề tài: Logic Synthesis, ABC Technology Mapping & Khảo sát Ripple Carry Adder trên Sky130 PDK)*

---

## 🎯 MỤC TIÊU TỐI THƯỢNG
1. **Làm chủ bản chất:** Hiểu thấu đáo cách cỗ máy **ABC Engine** đọc file **Liberty (`.lib`)** để đưa ra quyết định chọn cell; phân biệt giữa việc định hướng mapper (`SYNTH_STRATEGY`) với việc ép cứng cell (`Manual Instantiation`).
2. **Khai thác triệt để tài nguyên:** Sử dụng kho mã nguồn mẫu `sky130Examples.zip` để làm giàu tư duy phần cứng và nâng cấp môi trường thực hành.
3. **Thực thi hoàn hảo Lab 1:** Hoàn thành 2 thí nghiệm thực nghiệm trên khối **8-bit Ripple Carry Adder (RCA)**, lập ma trận so sánh các chiến lược tổng hợp (`AREA`, `DELAY`, `HIERARCHY`), và đúc kết thành báo cáo chuyên nghiệp.

---

## 🧭 LỘ TRÌNH THỰC THI 5 CHẶNG (5 PHASES)

```mermaid
flowchart LR
    P1["CHẶNG 1<br>Hệ thống hóa Lý thuyết"] --> P2["CHẶNG 2<br>Môi trường & Setup Lab1"]
    P2 --> P3["CHẶNG 3<br>Thí nghiệm 1: Strategies"]
    P3 --> P4["CHẶNG 4<br>Thí nghiệm 2: Ép Cell Thủ công"]
    P4 --> P5["CHẶNG 5<br>Báo cáo & Niêm phong"]

    style P1 fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#fff
    style P2 fill:#1e293b,stroke:#8b5cf6,stroke-width:2px,color:#fff
    style P3 fill:#1e293b,stroke:#f59e0b,stroke-width:2px,color:#fff
    style P4 fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#fff
    style P5 fill:#450a0a,stroke:#ef4444,stroke-width:2px,color:#fff
```

---

### 📍 CHẶNG 1: HỆ THỐNG HÓA LÝ THUYẾT & NẮM VỮNG BẢN CHẤT ABC (Lý thuyết cốt lõi)
* **Thời lượng dự kiến:** 1 phiên thảo luận định hướng.
* **Mục tiêu kỹ thuật:**
  1. Trả lời câu hỏi: *ABC thực sự nhìn thấy gì bên trong file Liberty `.lib`?*
     * Hàm Boolean (Boolean functions).
     * Diện tích ô chuẩn (Area cost).
     * Cung trễ tín hiệu (Timing arcs theo bảng tra cứu Slew/Load).
     * Điện dung các chân (Pin capacitance).
     * Ràng buộc tế bào cấm dùng (`dont_use`).
  2. Hiểu bản chất 3 tham số cấu hình synthesis trong `config.json`:
     * `SYNTH_STRATEGY`: Các thuật ngữ cân bằng Area vs Delay (`AREA 0`, `AREA 3`, `DELAY 0`...).
     * `SYNTH_HIERARCHY_MODE`: Cơ chế `flatten` (xóa ranh giới module) vs `keep` (giữ nguyên cấu trúc phân cấp).
     * `SYNTH_SHARE_RESOURCE`: Cơ chế gộp tài nguyên logic dùng chung.

---

### 📍 CHẶNG 2: THIẾT LẬP MÔI TRƯỜNG & KHỞI TẠO DỰ ÁN LAB 1
* **Thời lượng dự kiến:** Thao tác máy tính.
* **Các bước triển khai:**
  1. **Giải nén kho tài nguyên `sky130Examples.zip`:**
     * Bung nén trực tiếp vào thư mục `ctwsemi-data` (trên WSL: `/home/admin060506/ctwsemi-data/` và Windows host: `D:\Tapeout_chip\buoi_2\sky130Examples`).
  2. **Kiểm tra nâng cấp CTW SEMI Cockpit:**
     * Chạy script `capnhatctwsemi.txt` để cập nhật container lên phiên bản `huyatieo/ctwsemi:1.0.1`, kích hoạt tính năng **Schematic Viewer** ngay trên Web GUI.
  3. **Khởi tạo thư mục dự án `Lab1`:**
     * Cấu trúc thư mục chuẩn: `ctwsemi-data/Lab1/` chứa 2 file Verilog:
       * `rca.v`: Mã nguồn mô-đun cấp cao Bộ cộng lan truyền 8-bit.
       * `fa.v`: Mã nguồn mô-đun con Bộ cộng toàn phần 1-bit.
  4. **Cấu hình trên Web GUI:**
     * Truy cập `http://127.0.0.1:8765/`, trỏ tới dự án `Lab1`.
     * Chọn `Auto-generate config` $\rightarrow$ Đặt tham số móng: `FP_CORE_UTIL = 40` (bài học sống còn từ Lab 0!).

---

### 📍 CHẶNG 3: THỰC THI THÍ NGHIỆM 1 — MA TRẬN CHIẾN LƯỢC TỔNG HỢP (SYNTHESIS STRATEGIES)
* **Khảo sát cấu trúc mạch:**
  * Mở RTL IDE, bật Schematic Viewer để quan sát chuỗi 8 khối Full Adder (`fa`) lan truyền bit nhớ $C_{\text{in}} \rightarrow C_{\text{out}}$.
* **Lần chạy 1 (Baseline - `rca-run-base`):**
  * Cấu hình: `SYNTH_STRATEGY = AREA 0`, `SYNTH_HIERARCHY_MODE = flatten`.
  * Phân tích Netlist `rca.nl.v`: Giải mã vì sao biến mất các khối `fa` (do chế độ flatten xóa nhòa ranh giới).
  * Phân tích Log `yosys-synthesis.log`: Giải mã mâu thuẫn số liệu (ABC báo 37 cell logic $\rightarrow$ Yosys tối ưu chốt 32 cell logic + 9 output buffers = 41 cell).
* **Các lần chạy đối chứng (Parametric Exploration):**
  * *Lần chạy 2:* Đổi `SYNTH_STRATEGY = AREA 3` (Tối ưu diện tích sâu hơn).
  * *Lần chạy 3:* Đổi `SYNTH_STRATEGY = DELAY 0` (Tối ưu tốc độ, ép giảm trễ đường truyền).
  * *Lần chạy 4:* Đổi `SYNTH_HIERARCHY_MODE = keep` (Giữ nguyên phân cấp các khối `fa`).
* **Sản phẩm đầu ra:** Hoàn thiện bảng ma trận so sánh định lượng:
  | Cấu hình Run | Số lượng Cell | Tổng Diện tích ($um^2$) | Trễ ABC Delay (ps) | Diện tích ABC Area | Nhận xét Chuyên môn |
  | :--- | :---: | :---: | :---: | :---: | :--- |
  | **Run 1: Base (AREA 0, Flatten)** | | | | | |
  | **Run 2: AREA 3 (Deep Area Opt)** | | | | | |
  | **Run 3: DELAY 0 (Timing Opt)** | | | | | |
  | **Run 4: HIERARCHY = keep** | | | | | |

---

### 📍 CHẶNG 4: THỰC THI THÍ NGHIỆM 2 — KỸ THUẬT ÉP CELL THỦ CÔNG (MANUAL INSTANTIATION)
* **Ý tưởng kỹ thuật:** Thay vì để cỗ máy ABC tự do lựa chọn cell, kỹ sư chủ động gọi đích danh ô chuẩn trong thư viện Sky130 (`sky130_fd_sc_hd__fa_1`).
* **Thực hành sửa code:**
  * Tạo biến thể `rca_manual.v` gọi trực tiếp cổng `sky130_fd_sc_hd__fa_1`.
  * Chạy tổng hợp qua Yosys.
* **Biện luận bài toán đánh đổi (Trade-off Analysis):**
  * *Ưu điểm:* Kiểm soát 100% phần cứng vật lý, biết chính xác cell nào nằm ở đâu.
  * *Nhược điểm chí tử:* Thiết kế bị "trói chết" vào một nhà máy đúc (mất tính Portable sang TSMC/GlobalFoundries), tước mất quyền tối ưu logic toàn cục của ABC.

---

### 📍 CHẶNG 5: TỔNG HỢP, PHẢN BIỆN VÀ NIÊM PHONG BÁO CÁO LAB 1
* **Trả lời dứt điểm Câu hỏi trung tâm của Lab 1:**
  > *"ABC chọn cell dựa vào đâu và người thiết kế có thể tự chọn cell hay không?"*
* **Soạn thảo và đồng bộ tài liệu:**
  * Khởi tạo file `Lab1_Ghi_Chep_Kien_Thuc.md` tại cả 2 thư mục `D:\Tapeout_chip\buoi_2\docs\` và `D:\Tapeout_chip\buoi_2\`.
  * Chụp ảnh sơ đồ Schematic mạch RCA và lưu vào tài liệu.
  * Đánh giá và chấm điểm mức độ hoàn thành bài Lab.
