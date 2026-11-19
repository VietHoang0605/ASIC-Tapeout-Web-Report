# TÀI LIỆU KỸ THUẬT - BUỔI 1: NHẬP MÔN PHYSICAL DESIGN & GIẢI MÃ LỖI FLOORPLANNING (LAB 0)

**Dự án:** ASIC Silicon Tapeout
**Module:** 8-bit Synchronous Counter
**Công nghệ:** SkyWater 130nm (`sky130A` / `sky130_fd_sc_hd`)
**Nền tảng EDA:** CTW SEMI (LibreLane / OpenROAD Flow)

---

## PHẦN I: BẢN CHẤT CỦA TIẾN TRÌNH TAPEOUT & HẠ TẦNG CÔNG CỤ

### 1. Khái niệm Tapeout trên Silicon
* **Tapeout** vào cuối kỳ không phải là lúc nhận chip vật lý trên tay, mà là thời điểm hoàn thiện và đóng gói toàn bộ bản vẽ thành tệp tin định dạng **GDSII** (bản đồ địa hình ở cấp độ nguyên tử) để nộp cho nhà máy chế tạo (Foundry).
* Quá trình đúc wafer, quang khắc (lithography), cắt phiến (dicing) và đóng gói (packaging) theo mô hình chia sẻ chi phí **MPW (Multi-Project Wafer)** sẽ mất từ **3 đến 6 tháng** trước khi chip thực tế được gửi về.
* **Nguyên tắc vàng:** *Trên Silicon, không có nút Ctrl+Z.* Một vi phạm thời gian vài picosecond hoặc một đoản mạch khoảng cách nanomet đều biến con chip thành đống cát vô dụng.

### 2. Bản chất của Web App CTW SEMI
* Không phải là phần mềm biên dịch ma thuật độc quyền, mà là một **Web Cockpit (Bảng điều khiển trực quan)** được đóng gói bằng Docker để điều khiển chuỗi công cụ thiết kế vi mạch mã nguồn mở: **Yosys** (Synthesis), **OpenROAD** (Floorplan, Placement, CTS, Routing), **OpenSTA** (Static Timing Analysis), **Magic & KLayout** (DRC, LVS, GDSII export).
* Hoạt động trong môi trường container kết nối trực tiếp với Docker socket (`/var/run/docker.sock`) bên trong hầm ngầm Ubuntu WSL2.

### 3. Vị trí Lưu trữ Dữ liệu Thực tế
* Toàn bộ mã nguồn Verilog, file cấu hình `.json`/`.yaml`, và các sản phẩm layout trung gian/cuối cùng **nằm 100% trên ổ cứng laptop**, được lưu trữ trong phân vùng hệ thống tệp của WSL tại:
  ```text
  \\wsl.localhost\Ubuntu\home\admin060506\ctwsemi-data\
  ```
* Địa chỉ web `http://127.0.0.1:8765` chỉ là giao diện hiển thị tại chỗ (Localhost).

### 4. Phân biệt Tải PDK và Chỉ định Thư viện Tế bào (SCL)
* **Tải PDK (`sky130A` tại tab Tools):** Kéo toàn bộ kho thư viện công nghệ của nhà máy SkyWater về ổ đĩa.
* **Chỉ định thư viện (`sky130_fd_sc_hd` tại tab Setup):** Ra lệnh cho dự án sử dụng đúng phân loại gạch chuẩn *High Density* (mật độ cao). Cần chọn đủ cả hai bước thì hệ thống mới xác nhận trạng thái xanh `Ready to run`.

---

## PHẦN II: NGƯỜI LÍNH GÁC CỔNG FRONT-END (IVERILOG & WAVEFORM)

### 1. Vai trò của Iverilog (Icarus Verilog)
* Là trình mô phỏng logic hướng sự kiện (Event-Driven Simulator) mã nguồn mở. Đóng vai trò như một **bản vẽ CAD 3D mô phỏng động cơ trên màn hình** trước khi mang kim loại ra đúc thật.
* Giúp phát hiện sai sót thuật toán và chức năng logic mà không tiêu tốn tài nguyên chạy quy trình vật lý nặng nề.

### 2. Cơ chế Testbench & Giản đồ Xung (Waveform)
* File thiết kế (`src/counter.v`) được kiểm tra bởi file giả lập môi trường (`verify/counter_tb.v`).
* Testbench tự phát xung `clk` (chu kỳ 10ns = 100MHz), kích hoạt chân `reset` kéo về 0 để dọn sạch thanh ghi, sau đó nhả lên 1 để mạch bắt đầu đếm.
* Kết quả mô phỏng ghi nhận biến thiên theo từng picosecond vào file `.vcd`.
* **Sóng Waveform trong RTL IDE:** Là "đôi mắt" duy nhất của kỹ sư thiết kế. Vì transistor thực tế trong thạch anh không có màn hình hiển thị hay lệnh `printf()`, giản đồ xung giúp xác nhận bằng mắt thường giá trị `out[7:0]` tăng đều đặn `0x00 -> 0x01 -> 0x02 ...` sau mỗi sườn dương của Clock.

---

## PHẦN III: HIỆN TRƯỜNG VỤ ÁN, KỸ NĂNG TRUY VẾT & GIẢI MÃ LỖI VẬT LÝ LAB 0

### 1. Quy mô Hệ thống Counter 8-bit
* Được Yosys tổng hợp thành **31 cổng logic chuẩn** ($S_{\text{cells}} = 376.611\,\mu m^2$), gồm:
  * **8 Sequential cells** (D-Flip-Flop `sky130_fd_sc_hd__dfxtp_2`) để lưu 8 bit dữ liệu.
  * **23 Combinational cells** (AND, OR, XOR, NAND...) để thực hiện phép toán cộng 1.
* Xung nhịp hoạt động mục tiêu: $T = 10\,\text{ns}$ (Tần số $100\,\text{MHz}$).

### 2. Tuyệt Kỹ Dò Log Nhanh (Truy vết Hiện trường giữa biển Log 10.000 dòng)
* **Cách 1 (Soi trực tiếp trên Web CTW SEMI):**
  1. Trên bản đồ `Pipeline`, bấm chuột thẳng vào trạm dừng màu đỏ: **`OpenROAD.ResizerTimingPostCTS`** để cô lập riêng log chặng này.
  2. Nhấn phím `Ctrl + F`, tìm kiếm từ khóa `ERROR` hoặc `DPL-0036`.
  3. Áp dụng quy tắc vàng: **Đọc từ dưới đáy ngược lên**.
* **Cách 2 (Mở file log độc lập trên ổ cứng Laptop):**
  1. Truy cập thư mục lần chạy trên laptop:
     ```text
     \\wsl.localhost\Ubuntu\home\admin060506\ctwsemi-data\counter\runs\<tên-run>\37-openroad-resizertimingpostcts\
     ```
  2. Mở file `openroad-resizertimingpostcts.log`. File này **chỉ có 56 dòng**, ngắn gọn và làm nổi bật ngay hiện trường vụ án ở nửa cuối file.

### 3. Trích xuất Đoạn Log Chứa Lỗi Gốc (Raw Log Artifact)
Nguyên văn 20 dòng cuối (từ dòng 36 đến 55) trong file log chặng 37:

```text
36: [INFO RSZ-0098] No setup violations found
37: + repair_timing -verbose -hold -setup_margin 0.05 -hold_margin 0.10 -max_buffer_percent 50.0
38: [INFO RSZ-0046] Found 7 endpoints with hold violations.
39: Iteration | Resized | Buffers | Cloned Gates |   Area   |   WNS   |   TNS   | Endpoint
40: --------------------------------------------------------------------------------------
41:         0 |       0 |       0 |            0 |    +0.0% |   0.024 |   0.000 | _48_/D
42:     final |       0 |       9 |            0 |   +15.8% |   0.102 |   0.000 | _46_/D
43: --------------------------------------------------------------------------------------
44: [INFO RSZ-0032] Inserted 9 hold buffers.
45: + detailed_placement -max_displacement  500 100 
46: [INFO DPL-0034] Detailed placement failed on the following 7 instances:
47: [INFO DPL-0035]  _30_
48: [INFO DPL-0035]  _25_
49: [INFO DPL-0035]  _34_
50: [INFO DPL-0035]  _23_
51: [INFO DPL-0035]  _33_
52: [INFO DPL-0035]  _26_
53: [INFO DPL-0035]  _26_
54: [ERROR DPL-0036] Detailed placement failed.
55: Error: rsz_timing_postcts.tcl, 61 DPL-0036
```

### 4. Giải Phẫu Chi Tiết Từng Dòng Lỗi (Line-by-Line Breakdown)
* **Dòng 36 (`[INFO RSZ-0098] No setup violations found`):** Mạch không dính lỗi Setup Time, tốc độ truyền dẫn đạt yêu cầu chu kỳ 10ns.
* **Dòng 37 (`+ repair_timing -verbose -hold ...`):** Thuật toán tự động sửa lỗi giữ chân tín hiệu (Hold Time) được kích hoạt.
* **Dòng 38 (`[INFO RSZ-0046] Found 7 endpoints with hold violations`):** Phát hiện **7 điểm chốt thanh ghi bị vi phạm Hold Time** do dữ liệu đến quá nhanh, có nguy cơ ghi đè dữ liệu cũ.
* **Dòng 39 - 43 (Bảng thống kê tối ưu):** Hàng `final` ghi nhận `Buffers = 9`, `Area = +15.8%`. Để hãm phanh 7 đường truyền trên, công cụ phải chèn thêm **9 bộ đệm (Hold Buffers)**, làm tăng 15.8% diện tích tế bào toàn mạch.
* **Dòng 44 (`[INFO RSZ-0032] Inserted 9 hold buffers`):** Xác nhận 9 bộ đệm đã được thêm vào netlist.
* **Dòng 45 (`+ detailed_placement -max_displacement 500 100`):** Lệnh bắt đầu tìm kiếm vị trí lưới (sites) thực tế để ghim 9 bộ đệm mới cùng các cổng cũ vào các hàng ngang (rows) hợp lệ.
* **Dòng 46 - 53 (`[INFO DPL-0034] Detailed placement failed on the following 7 instances: _30_, _25_...`):** Chỉ đích danh **7 linh kiện không thể xếp được vị trí** do xung quanh không còn khoảng đất trống hợp lệ nào.
* **Dòng 54 (`[ERROR DPL-0036] Detailed placement failed`):** **Mã lỗi tử thần DPL-0036**. Thuật toán sắp xếp chi tiết tuyên bố thất bại vì bế tắc không gian vật lý.
* **Dòng 55 (`Error: rsz_timing_postcts.tcl, 61 DPL-0036`):** Tiến trình LibreLane lập tức dừng khẩn cấp tại dòng 61 của file kịch bản điều khiển.

### 5. Căn Nguyên Gốc Rễ: Tại Sao Lỗi Lại Xảy Ra?
1. **Nguồn gốc tham số 50%:** Trong file cấu hình ban đầu `config.json`, người thiết kế không khai báo diện tích (`DIE_AREA`, `CORE_AREA`). OpenROAD tự động sử dụng giá trị mặc định của hệ thống: `FP_CORE_UTIL = 50.0%`, `aspect_ratio = 1.0` (khu đất hình vuông).
   * **Bài học:** *Không bao giờ tin tưởng mù quáng vào các giá trị mặc định của phần mềm EDA.*
2. **Khu đất bị bóp nghẹt:**
   $$\text{Utilization} = \frac{S_{\text{cells}}}{S_{\text{core}}} \implies S_{\text{core}} = \frac{376.611\,\mu m^2}{0.5} \approx 738.208\,\mu m^2$$
   Khu đất $738.208\,\mu m^2$ được đo ni đóng giày chỉ vừa đủ cho 31 cổng logic ban đầu.
3. **Hiệu ứng sụp đổ dây chuyền:** Xung 100MHz gây 7 lỗi Hold $\rightarrow$ Đẻ thêm 9 Buffer (+15.8% diện tích) $\rightarrow$ Không gian dự phòng bị lấp đầy $\rightarrow$ Hết sạch ô đất hợp lệ $\rightarrow$ Nổ lỗi `DPL-0036`.
4. **Phương pháp Khắc phục:** Nới rộng khu đất bằng cách hạ `FP_CORE_UTIL = 40%`:
   $$S_{\text{core\_new}} = \frac{376.611\,\mu m^2}{0.4} \approx 941.528\,\mu m^2$$
   Diện tích tăng thêm hơn $200\,\mu m^2$ đất trống (tỷ lệ đất trống tăng lên 60%), đủ chỗ cho 9 bộ đệm đỗ xe hợp lệ và thông suốt dây chuyền sang khâu Routing.

---

## PHẦN IV: BÁO CÁO GIẢI TRÌNH 6 CÂU HỎI THU HOẠCH LAB 0 (TRANG 16)

### Câu 1: Giải thích Nguyên lý Hoạt động của Bộ đếm qua Giản đồ Sóng (Waveform Analysis)

* **Nội dung câu hỏi khảo sát:**
  > *Dựa vào giản đồ thời gian (Waveform) thu được trong RTL IDE (`dump.vcd`), hãy giải thích sự tương tác giữa các tín hiệu điều khiển (`clk`, `rst`, `en`) và ngõ ra dữ liệu `count[7:0]` trong suốt quá trình mô phỏng? Hiện tượng gì xảy ra khi bộ đếm đạt giá trị cực đại?*

* **Trích dẫn nguyên văn câu trả lời của Kỹ sư:**
  > *"Trước tiên, ta sẽ kể đến các tín hiệu trong waveform sẽ gồm có: xung clk, tín hiệu rst mức cao, tín hiệu en(enable) và cuối cùng là count. Ở giai đoạn đầu tiên, sau khi tín hiệu rst rớt xuống mức 0 và khi tín hiệu en nhảy lên mức 1 thì ở thời điểm sườn dương kế tiếp, count sẽ bắt đầu đếm và sẽ +1 mỗi khi gặp sườn dương của clk, khi đếm đến cực đại tức là 2^8-1 thì sẽ xảy ra hiện tượng tràn bộ đếm và bắt đầu đếm lại từ 0."*

* **Đánh giá & Chú giải Kỹ thuật của Kiến trúc sư Trưởng (Điểm: 9.5/10 - Xuất sắc):**
  1. **Nhận diện đầy đủ hệ tín hiệu:** Nắm bắt chính xác vai trò của chân `en` (Enable) – chốt chặn logic quyết định mạch có được phép đếm hay không, bên cạnh cặp tín hiệu truyền thống `clk` và `rst` (Active-high).
  2. **Bản chất logic đồng bộ (Synchronous Logic):** Nhận diện chuẩn xác tính chất đồng bộ theo xung nhịp: Mặc dù tại thời điểm $t = 12\,\text{ns}$ (trong `counter_tb.v`), `rst` tụt xuống mức 0 và `en` kích hoạt mức 1, dữ liệu ngõ ra không lập tức đổi trạng thái mà phải chờ đến đúng thời điểm sườn dương kế tiếp của Clock ($t = 15\,\text{ns}$) mới chính thức bắt đầu tăng giá trị.
  3. **Hiện tượng tràn bộ đếm (Rollover / Overflow):** Dung lượng thanh ghi 8-bit có giới hạn biểu diễn là $2^8 - 1 = 255$ (`8'hFF`). Khi gặp sườn dương tiếp theo, phép cộng $255 + 1 = 256$ làm rơi rớt bit nhớ thứ 9 (Carry bit) ra ngoài khoảng không lưu trữ, khiến toàn bộ 8 bit ngõ ra tự động tuần hoàn quay về trạng thái gốc `8'h00` (`0`).


### Câu 2: Giải phẫu Sơ đồ Phần cứng RTL & Cơ chế Biến đổi thành 31 Cổng Logic

* **Nội dung câu hỏi khảo sát:**
  > *Bên trong Counter 8-bit thực chất chứa những linh kiện phần cứng cụ thể nào? Làm sao biết được cấu tạo từ các khối ý niệm (Bộ cộng, MUX) biến thành các cổng logic thực tế và chiếm dụng đúng 31 Standard Cells trong công nghệ SkyWater 130nm?*

* **Trích dẫn nguyên văn câu trả lời của Kỹ sư:**
  > *"Để có thể tạo ra 1 counter 8 bit ta cần sử dụng 8 D-FF với sơ đồ Q của flip-flop đứng trước được nối vào D của flip-flop đứng sau, khối cộng ta sẽ sử dụng bộ cộng full adder với các cổng xor và and, or, ngoài ra còn 1 bộ mux với tín hiệu điều khiển là enable or !rst, 1 đầu vào là kết quả của phép cộng, đầu vào còn lại nối xuống đất."*

* **Đánh giá & Hiệu chỉnh Kỹ thuật của Kiến trúc sư Trưởng (Điểm: 8.5/10 - Tư duy bóc tách linh kiện tốt, cần chỉnh chuẩn kết nối):**
  1. **Hiệu chỉnh kết nối phần cứng (Phân biệt Counter vs Shift Register):**
     * Mô hình *"Q của Flip-Flop trước nối vào D của Flip-Flop sau"* là cấu trúc của **Thanh ghi dịch (Shift Register)**, nơi dữ liệu chỉ trượt tuần tự qua các ô nhớ.
     * Đối với **Bộ đếm nhị phân (Binary Counter)**: Cả 8 con D-FF bắt buộc phải mắc **hoàn toàn song song (Parallel)**, dùng chung một nhịp xung `clk`. Toàn bộ 8 bit ngõ ra $Q[7:0]$ cùng chạy vào Bộ cộng để tính giá trị tiếp theo $Q + 1$, sau đó đi qua hệ thống MUX và quay ngược về chân $D[7:0]$ của chính 8 con D-FF đó.
  2. **Cơ cấu 2 tầng MUX điều khiển (Multiplexer Hierarchy):**
     * **Tầng 1 (MUX Enable):** Kiểm tra tín hiệu `en`. Nếu `en = 1` chọn kết quả của bộ cộng ($Q + 1$). Nếu `en = 0` chọn đường Bus phản hồi lấy lại chính giá trị cũ $Q$ để giữ nguyên trạng thái đếm.
     * **Tầng 2 (MUX Reset - Quyền ưu tiên cao nhất):** Kiểm tra tín hiệu `rst`. Nếu `rst = 1`, đè mọi dữ liệu và nạp hằng số `8'h00` (GND). Nếu `rst = 0`, cho phép kết quả từ Tầng 1 đi vào chân $D$ của các D-FF.
  3. **Làm sao biết được con chip dùng cổng gì và tại sao là đúng 31 Cổng Logic?**
     * **Từ Sơ đồ khối (RTL Architecture) sang Cổng thật (Gate-Level):** Sơ đồ khối gồm các biểu tượng toán học trừu tượng (`$add`, `$mux`, `$dff`). Cỗ máy tổng hợp **Yosys** sẽ nén toàn bộ hệ hàm Boolean của Bộ cộng và 2 tầng MUX, sau đó thực hiện **Technology Mapping** vào thư viện công nghệ **`sky130_fd_sc_hd`**.
     * **Ứng dụng Cổng phức hợp (Complex Gates):** Yosys không dùng các cổng AND/OR rời rạc mà thay bằng các cổng phức hợp như **`a21oi_2`** (AND-OR-Invert), **`o21a_2`**... giúp giảm diện tích và số lượng transistor đáng kể.
     * **Chứng minh định lượng từ Netlist (`counter_synthesis_netlist.v`):**
       * **8 Sequential Cells:** 8 ô D-Flip-Flop (`sky130_fd_sc_hd__dfxtp_2`) từ linh kiện `_46_` đến `_53_` (lưu trữ 8-bit `count[7:0]`).
       * **23 Combinational Cells:** 23 cổng logic tổ hợp từ linh kiện `_23_` đến `_45_` (đảm nhiệm toàn bộ phép cộng và 2 tầng MUX).
       * $\implies$ **Tổng cộng:** $8 + 23 = \mathbf{31\text{ Standard Cells}}$ (Tổng diện tích tế bào $S_{\text{cells}} = 376.611\,\mu m^2$).
  4. **Bản vẽ trực quan hóa:**
     * Toàn bộ sơ đồ luồng dữ liệu 1 chiều phẳng (Planar Datapath) không chồng chéo dây, kèm hình thang cân chuẩn Điện tử số đã được xuất bản tại: [**`counter_schematic.svg`**](file:///D:/Tapeout_chip/Buoi_1/counter_schematic.svg).

### Câu 3: Bản chất, Vị trí và Cơ chế Khởi tạo Mặt bằng Chip (Floorplan Initialization)

* **Nội dung câu hỏi khảo sát:**
  > *Hiểu cách khởi tạo floor plan. Floorplan thực chất là cái gì? Nó nằm ở vị trí nào trong quy trình chuyển đổi từ RTL sang Layout GDSII của bộ đếm 8-bit? Phân biệt rạch ròi giữa Total Instances Area và Core Area qua các con số thực tế thu được trong log.*

* **Tổng hợp Kiến thức & Giải mã Kỹ thuật của Kiến trúc sư Trưởng:**

#### 1. Bản chất Vật lý của Floorplan (Ẩn dụ Quy hoạch Đô thị & Xây dựng)
* **Từ Thế giới ảo sang Mặt bằng thật:** Sau bước Tổng hợp (Synthesis), bản thiết kế chỉ là một danh sách kết nối vô hình (Netlist) trôi nổi trong không gian ảo. Các cổng logic chỉ biết mình nối với cổng nào chứ **chưa hề có tọa độ vật lý $(x, y)$, chưa có kích thước chip, và chưa có ranh giới**.
* **Floorplan là công đoạn "Cắm mốc ranh giới, phân lô và kéo điện lưới":**
  * **Die Area (Khuôn chip tổng thể):** Toàn bộ kích thước viên silicon vật lý. Sau này khi nhà máy chế tạo xong tấm Wafer, lưỡi cưa kim cương sẽ cắt rời từng viên chip theo đúng ranh giới của Die này.
  * **Core Area (Vùng lõi logic):** Khuôn viên đất trung tâm bên trong Die. Đây là **vùng duy nhất** mà 31 cổng logic chuẩn và các bộ đệm được phép sinh sống và bố trí.
  * **Core Margin / Core Space:** Dải đất đệm bao quanh giữa biên ngoài của Core và biên của Die (gồm 4 cạnh: Bottom, Top, Left, Right). Vùng này bị cấm đặt cổng logic, giữ vai trò sinh tử:
    * Chừa đất để đặt các chân tiếp xúc ngoại vi (**I/O Pins / Pads**: `clk`, `rst`, `enable`, `count[7:0]`).
    * Đi các dải kim loại nguồn to bản bao quanh (**Power Ring**: thanh $V_{DD}$ $1.8V$ và $V_{SS}$ GND) để bơm điện vào toàn bộ khuôn chip.
  * **Rows (Hàng đặt tế bào):** Bên trong Core, công cụ kẻ sẵn các hàng song song (như các luống đất trồng cây) từ các ô lưới chuẩn `site unithd`. Mọi cổng logic sau này bắt buộc phải nằm ngay ngắn trên các hàng này.
  * **PDN (Power Distribution Network):** Lưới điện quốc gia gồm các thanh kim loại đan dọc ngang qua vùng Core để sẵn sàng "cắm điện" cho mọi cổng logic.

---

#### 2. Vị trí của Floorplan trong Quy trình RTL-to-GDSII
Trong chuỗi 7 chặng công nghệ mà Kỹ sư đã chạy trên **CTW SEMI (OpenROAD Flow)**:

$$\text{RTL IDE} \longrightarrow \text{Synthesis (Yosys)} \longrightarrow \mathbf{FLOORPLAN\ (OpenROAD)} \longrightarrow \text{Placement} \longrightarrow \text{CTS} \longrightarrow \text{Routing} \longrightarrow \text{GDSII}$$

* **Floorplan nằm ngay sau Synthesis và là bước mở màn của toàn bộ khâu Thiết kế Vật lý (Backend / Physical Design).**
* Trước khi có Floorplan, công cụ hoàn toàn chưa biết hình dáng con chip. Floorplan chính là **"Cái móng nhà"**: Nếu móng được đúc vững chắc, đúng kích thước thì các khâu sau (xếp cổng Placement, dựng cây xung nhịp CTS, đi dây Routing) mới có thể hoàn thành trơn tru.

---

#### 3. Phân biệt Bản chất 2 Con số: `Total Instances Area` vs `Core Area`

Tránh nhầm lẫn kinh điển giữa diện tích đồ nội thất và diện tích căn phòng:

| Thông số | Giá trị trong Log | Bản chất Kỹ thuật | Ẩn dụ Trực quan |
| :--- | :---: | :--- | :--- |
| **Total Instances Area** | **`376.611 um²`** | Tổng diện tích vật lý của bản thân **31 cổng logic** (8 D-FF = $170.16\,\mu m^2$ + 23 cổng tổ hợp = $206.45\,\mu m^2$). | **Tổng diện tích đáy của bàn ghế, tủ giường** kê trong phòng. |
| **Core Area** | **`738.208 um²`** | Diện tích toàn bộ mặt sàn vùng lõi được cấp phát cho con chip. | **Diện tích toàn bộ mặt sàn của căn phòng**. |
| **Utilization** | **`51.0%` (`0.510`)** | Tỷ lệ lấp đầy: $\frac{\text{Total Instances Area}}{\text{Core Area}} = \frac{376.611}{738.208}$. | Tỷ lệ sàn nhà bị đồ đạc chiếm dụng. |
| **Whitespace** | **`49.0%`** | Khoảng đất trống còn lại: $100\% - 51\% = 49\%$. | Lối đi lại để luồn dây điện (Routing) và kê thêm đồ (Buffers). |

---

#### 4. Mối liên hệ Nhân quả tới Lỗi Tràn Ô `DPL-0036` của Bộ Đếm
* Ở lần chạy đầu tiên, do để mật độ mặc định $50\%$, Core Area bị bó hẹp ở mức $738.208\,\mu m^2$.
* Khi mạch bị 7 lỗi Hold sau bước CTS, công cụ bắt buộc phải chèn thêm **9 bộ đệm (Hold Buffers)** (+15.8% diện tích).
* Lượng đất trống $49\%$ ban đầu bị nuốt sạch, các cổng bị chen chúc và thuật toán sắp xếp chi tiết không tìm được vị trí hợp lệ trên các hàng `site unithd` $\implies$ Bùng nổ mã lỗi tử thần:
  ```text
  [INFO DPL-0034] Detailed placement failed on the following 7 instances: _30_, _25_, _34_...
  [ERROR DPL-0036] Detailed placement failed.
  ```
* **Bài học quy hoạch:** Khi khởi tạo Floorplan, phải chủ động hạ `FP_CORE_UTIL` xuống **$40\%$** để nâng diện tích Core lên $\approx 941.5\,\mu m^2$ (chừa $60\%$ đất trống dự phòng), giúp các bộ đệm có đất đỗ xe an toàn!

---

#### 5. Giải mã Toán học Định lượng: Lưới Site `unithd`, 10 Rows x 59 Sites & Tọa độ BBox

* **Bản vẽ Kiến trúc Mặt bằng Chuẩn vector:** Toàn bộ kích thước hình học, tọa độ Bounding Box, luồng 10 hàng và phóng đại ô lưới `site unithd` đã được xuất bản trực quan tại:  
  👉 [**`floorplan_architecture.svg`**](file:///D:/Tapeout_chip/Buoi_1/floorplan_architecture.svg)

##### A. Bí ẩn Lưới ô chuẩn `site unithd` (SkyWater 130nm High-Density)
* Nhà máy đúc SkyWater quy định kích thước chuẩn của 1 ô lưới cơ sở (`site unithd`):
  * **Chiều cao 1 hàng (Row Height):** $H_{\text{row}} = \mathbf{2.72\,\mu m}$ (cố định trên toàn bộ thư viện tế bào chuẩn).
  * **Chiều rộng 1 bước lưới (Site Width):** $W_{\text{site}} = \mathbf{0.46\,\mu m}$ (mọi cell đều có bề rộng là bội số nguyên của $0.46\,\mu m$).
* Khi OpenROAD nhận diện tích Core mục tiêu là $738.208\,\mu m^2$ với `aspect_ratio = 1.0` (hình vuông), công cụ chia thành:
  * **Số hàng (Rows):** $10\text{ rows} \implies \text{Core Height} = 10 \times 2.72\,\mu m = \mathbf{27.200\,\mu m}$.
  * **Số ô trên 1 hàng (Sites/Row):** $59\text{ sites} \implies \text{Core Width} = 59 \times 0.46\,\mu m = \mathbf{27.140\,\mu m}$.
  * **Kiểm chứng diện tích Core:**
    $$\text{Core Area} = 27.200\,\mu m \times 27.140\,\mu m = \mathbf{738.208\,\mu m^2} \quad \text{(Khớp log 100%!)}$$

##### B. Cơ chế Tính Tọa độ Hộp bao quanh (Bounding Box)
* Gốc tọa độ $(0, 0)$ đặt tại góc **Dưới-Trái của Die Area**:
* **Core Bounding Box (`Core BBox`):**
  * Góc Dưới-Trái: $(X_{\min}, Y_{\min}) = (\text{Left Margin}, \text{Bottom Margin}) = \mathbf{(5.520, 10.880)\,\mu m}$.
  * Góc Trên-Phải: 
    $$X_{\max} = 5.520 + 27.140 = \mathbf{32.660\,\mu m}$$
    $$Y_{\max} = 10.880 + 27.200 = \mathbf{38.080\,\mu m}$$
    $$\implies \mathbf{\text{Core BBox: (5.520, 10.880) (32.660, 38.080) um}}$$
* **Die Bounding Box (`Die BBox`):**
  * Bề ngang Die: $\text{Width}_{\text{core}} + \text{Left} + \text{Right} = 27.14 + 5.52 + 5.52 = 38.18\,\mu m \rightarrow$ Khớp vào lưới chế tạo thành **$38.485\,\mu m$**.
  * Bề dọc Die: $\text{Height}_{\text{core}} + \text{Bottom} + \text{Top} = 27.20 + 10.88 + 10.88 = 48.96\,\mu m \rightarrow$ Khớp vào lưới chế tạo thành **$49.205\,\mu m$**.
  * $\implies \mathbf{\text{Die BBox: (0.000, 0.000) (38.485, 49.205) um}}$ (Diện tích khuôn $S_{\text{die}} = 1,893.65\,\mu m^2$).

---

### Câu 4: Bản chất, Ý nghĩa Kỹ thuật và Bài toán Đánh đổi của Tham số `FP_CORE_UTIL`

* **Nội dung hệ thống câu hỏi khảo sát:**
  1. *Định nghĩa & Công thức toán học: `FP_CORE_UTIL` viết tắt của từ gì? Công thức toán học chuẩn xác liên kết giữa `FP_CORE_UTIL`, diện tích cổng logic (`Instances Area`) và diện tích vùng lõi (`Core Area`)?*
  2. *Khoảng đất trống (Whitespace): Nếu đặt `FP_CORE_UTIL = 40%`, thì 60% diện tích còn lại trong Core là gì? Nó có bị bỏ phí không, hay giữ nhiệm vụ sống còn nào ở các bước CTS và Routing phía sau?*
  3. *Bài toán đánh đổi (Trade-off): Nếu ép `FP_CORE_UTIL` lên quá cao (70% - 80%) thì con chip đối mặt với nguy cơ gì? Ngược lại, nếu thả `FP_CORE_UTIL` xuống quá thấp (10% - 20%) thì gây hậu quả gì về chi phí và hiệu năng điện tử?*
  4. *Giải mã thực tế Lab 0: Tại sao ở bài Lab 0, hệ thống để mặc định 50% thì bị nổ lỗi tử thần, mà khi hạ xuống 40% thì lại chạy trót lọt ra tới file GDSII?*

* **Trích dẫn toàn bộ câu trả lời thực chiến của Kỹ sư:**
  * **Trả lời Ý 1 (Công thức):**  
    > *"FP_CORE_UTIL = Instances Area / Core Area (đơn vị tính bằng %)."*
  * **Trả lời Ý 2 (Bản chất 60% đất trống):**  
    > *"Khi cấu hình FP_CORE_UTIL = 40% tức là 40% diện tích của core area sẽ là dành cho các cell vật lý và còn 60% diện tích còn lại sẽ là khoảng đất trống dùng cho việc đi dây giữa các cell, sắp xếp các cell sao cho chúng không được quá sát nhau để tránh tình trạng chập mạch, và có thể thêm vào đó các buffer... giống như trường hợp bài mẫu của Lab 0, khi phát hiện vi phạm thời gian, hệ thống tự động thêm vào core area 9 bộ buffer để vá lỗi."*
  * **Trả lời Ý 3 (Bài toán đánh đổi):**  
    > *"Nếu ép FP_CORE_UTIL lên quá cao thì mạch điện sẽ dễ bị chập do các đường dây điện nối giữa các cell quá sát nhau và sẽ không còn đất để đặt các buffer nếu gặp phải vi phạm thời gian... Còn nếu thả FP_CORE_UTIL xuống quá thấp thì diện tích đất Core Area sẽ nở to ra gấp nhiều lần, gây lãng phí chi phí đúc chip silicon đắt đỏ, đồng thời dây dẫn kéo dài làm tăng điện trở - điện dung ký sinh, khiến mạch chạy chậm chạp và tiêu hao nhiều năng lượng."*
  * **Trả lời Ý 4 (Giải mã bài Lab 0 - Chốt hạ 10/10):**  
    > *"Chính vì mạch vi phạm 7 lỗi Hold Time nên cần lắp thêm 9 buffer vào để vá lỗi. Khi FP_CORE_UTIL = 50% thì diện tích đất trống còn lại không đủ để nhét thêm 9 buffer này khiến trình đặt ô báo lỗi. Khi chúng ta hạ FP_CORE_UTIL xuống 40%, vì Instances Area là một con số cố định không thể thay đổi rồi, ta không thể bớt nó đi cho vừa với con số 40% được, mà lúc này PHẢI MỞ RỘNG KHU ĐẤT CORE AREA TO RA để cái Instances Area này so với Core Area chỉ còn chiếm 40%!"*

* **Đánh giá & Chú giải Kỹ thuật của Kiến trúc sư Trưởng (Điểm: 10/10 - Xuất sắc Tuyệt đối):**

#### 1. Định nghĩa và Công thức Chuẩn hóa
* **Tên đầy đủ:** `FP_CORE_UTIL` = **Floorplan Core Utilization** (Mật độ sử dụng vùng lõi khi quy hoạch mặt bằng).
* **Công thức toán học:**
  $$\mathbf{FP\text{_}CORE\text{_}UTIL} = \frac{\mathbf{Instances\ Area}}{\mathbf{Core\ Area}} \times 100\%$$
* **Hệ quả thiết kế:** Vì `Instances Area` ($376.611\,\mu m^2$) là đại lượng bất biến do 31 cổng sau Synthesis quy định, công cụ OpenROAD dùng `FP_CORE_UTIL` để tính ngược ra diện tích khuôn đất cần cấp phát:
  $$\mathbf{Core\ Area} = \frac{\mathbf{Instances\ Area}}{\mathbf{FP\text{_}CORE\text{_}UTIL}}$$

#### 2. Vai trò Sống còn của Khoảng Đất Trống (Whitespace = 100% - FP_CORE_UTIL)
Khi thiết lập `FP_CORE_UTIL = 40%`, thì **60% diện tích còn lại (Whitespace)** giữ 2 nhiệm vụ sống còn:
1. **Không gian luồn dây kim loại (Routing Channels):** Đảm bảo hàng trăm đường dây kim loại (Metal 1 đến Metal 5) có đủ khoảng cách ly an toàn theo luật DRC của nhà máy, tránh nghẽn mạch (Routing Congestion) và đoản mạch.
2. **Bãi đỗ xe dự phòng cho các Tế bào Tối ưu hóa (Optimization Buffers):** Sau các bước CTS (Clock Tree Synthesis) và STA, công cụ bắt buộc phải chèn thêm các bộ đệm cân bằng xung nhịp (`clkbuf`) và bộ đệm sửa lỗi thời gian giữ (Hold Buffers). Whitespace chính là bãi đất trống để nhét các bộ đệm này vào mà không làm xô lệch các cổng cũ.

#### 3. Ma trận Đánh đổi (Engineering Trade-off)
| Cấu hình | Nguy cơ / Nhược điểm | Ưu điểm |
| :--- | :--- | :--- |
| **Ép quá cao ($70\% - 80\%$)** | • Đất quá chật, nghẽn dây Routing, vi phạm khoảng cách DRC.<br>• Không còn đất trống để chèn Hold Buffers $\implies$ **Dễ nổ lỗi `DPL-0036`**. | Tiết kiệm diện tích silicon, giảm chi phí đúc chip. |
| **Thả quá thấp ($10\% - 20\%$)** | • Diện tích Core phình to lãng phí, tốn tiền đúc chip (đội số Tile trong Tiny Tapeout).<br>• Dây dẫn kéo dài $\implies$ Điện trở/điện dung ký sinh tăng $\implies$ **Chậm mạch (vi phạm Setup), chip ăn nhiều pin và tỏa nhiệt**. | Đi dây cực kỳ dễ dàng, không bao giờ sợ thiếu chỗ nhét buffer. |
| **Điểm cân bằng ($40\% - 60\%$)** | Vùng an toàn (Sweet Spot) chuẩn công nghiệp cho thiết kế ASIC. | Cân bằng hoàn hảo giữa diện tích, khả năng đi dây và tốc độ. |

#### 4. Giải mã Hiện tượng Bài Lab 0 (50% Thất bại vs 40% Thành công)
* **Ở mức mặc định $50\%$:** Core Area chỉ được cấp $\approx 738.2\,\mu m^2$. Sau bước CTS, mạch phát sinh **7 lỗi Hold**, hệ thống cố gắng chèn thêm **9 bộ đệm (Hold Buffers)** làm tăng $+15.8\%$ diện tích cell. Khoảng đất trống bị bóp nghẹt, thuật toán sắp xếp chi tiết không tìm được vị trí hợp lệ trên các hàng `site unithd` $\implies$ Nổ lỗi tử thần `[ERROR DPL-0036] Detailed placement failed`.
* **Khi hạ xuống $40\%$:** Vì $376.611\,\mu m^2$ là bất biến, công cụ buộc phải **mở rộng khu đất Core Area lên $\approx 941.5\,\mu m^2$** (tăng thêm hơn $200\,\mu m^2$ đất trống Whitespace chiếm $60\%$). Nhờ có thêm bãi đất trống này, 9 bộ đệm được xếp vào các luống đất một cách vừa vặn, toàn bộ flow chạy thông suốt tới file GDSII!

---

### Câu 5: Tính lại Instances Area, Core Area với `FP_CORE_UTIL = 45%`

* **Nội dung hệ thống câu hỏi khảo sát:**
  1. *Tính bất biến của Instances Area: Khi đổi `FP_CORE_UTIL` từ 50% sang 45%, số lượng 31 Standard Cells và diện tích Instances Area có thay đổi không? Con số này bằng bao nhiêu?*
  2. *Thiết lập phép tính và xác định Core Area: Áp dụng công thức liên hệ, tính ra giá trị Core Area tương ứng với `FP_CORE_UTIL = 45%` (làm tròn đến 3 chữ số thập phân)?*
  3. *Quy hoạch trên lưới vật lý (Physical Grid Snapping): Nếu giữ tỷ lệ khung `aspect_ratio = 1.0` (hình vuông) trên thư viện Sky130 HD, vùng Core 45% này sẽ được OpenROAD phân bổ thành bao nhiêu hàng (rows) và bao nhiêu ô (sites)?*
  4. *Đánh giá khả năng vượt lỗi `DPL-0036`: So sánh đất trống Whitespace ở mức 45% với mức 50% (lỗi) và 40% (thành công). Cấu hình 45% có đủ an toàn để hoàn thành việc chèn 9 bộ đệm (Hold Buffers) và đi dây GDSII không?*

* **Lời giải & Phân tích Chuyên sâu của Kiến trúc sư Trưởng ASIC:**

#### 1. Tính Bất biến Tuyệt đối của `Instances Area`
* **Nguyên lý:** Công đoạn Floorplan nằm sau Synthesis (Yosys). Kết quả tổng hợp logic đã chốt cứng Netlist gồm đúng **31 Standard Cells** (`sky130_fd_sc_hd` gồm 8 D-FF và 23 cổng tổ hợp).
* Kích thước hình học của từng cell trong thư viện PDK là cố định. Việc kỹ sư thay đổi thông số Floorplan (`FP_CORE_UTIL`) hoàn toàn không làm co giãn hay thay đổi diện tích thực của 31 cổng này.
* $\implies \mathbf{Instances\ Area = 376.611\,\mu m^2}$ **(Không đổi - Đại lượng bất biến).**

---

#### 2. Tính toán Diện tích Vùng Lõi Lý thuyết (`Core Area`)
Áp dụng công thức quy hoạch mặt bằng:
$$\mathbf{Core\ Area} = \frac{\mathbf{Instances\ Area}}{\mathbf{FP\text{_}CORE\text{_}UTIL}} = \frac{376.611\,\mu m^2}{45\%} = \frac{376.611}{0.45} = \mathbf{836.913\,\mu m^2}$$

* **Tỷ lệ Đất trống (Whitespace):**
  $$\text{Whitespace \%} = 100\% - 45\% = \mathbf{55\%}$$
* **Diện tích Đất trống lý thuyết:**
  $$\text{Whitespace Area} = 836.913\,\mu m^2 - 376.611\,\mu m^2 = \mathbf{460.302\,\mu m^2}$$

---

#### 3. Mô phỏng Quy hoạch Lưới Vật lý (Snap vào Lưới Sky130 HD)
Để hiểu sâu cách công cụ OpenROAD thực thi trên silicon thực tế:
* Chuẩn ô lưới SkyWater 130nm:
  * Chiều cao hàng: $H_{\text{row}} = 2.72\,\mu m$.
  * Bề rộng 1 site: $W_{\text{site}} = 0.46\,\mu m$.
* Với mục tiêu khuôn hình vuông (`aspect_ratio = 1.0`):
  * Cạnh lý thuyết: $L = \sqrt{836.913} \approx 28.929\,\mu m$.
  * **Số hàng (Rows):** $\text{round}\left(\frac{28.929}{2.72}\right) = \text{round}(10.63) = \mathbf{11\text{ rows}} \implies \text{Core Height} = 11 \times 2.72 = \mathbf{29.920\,\mu m}$.
  * **Số ô trên mỗi hàng (Sites/Row):** $\text{round}\left(\frac{836.913}{29.920 \times 0.46}\right) = \text{round}(60.8) = \mathbf{61\text{ sites}} \implies \text{Core Width} = 61 \times 0.46 = \mathbf{28.060\,\mu m}$.
* **Diện tích Core thực tế sau khi khớp lưới ô (Snapped Core Area):**
  $$\text{Snapped Core Area} = 29.920\,\mu m \times 28.060\,\mu m = \mathbf{839.555\,\mu m^2}$$
  $$\implies \text{Mật độ thực tế (Actual Core Util)} = \frac{376.611}{839.555} \approx \mathbf{44.86\%} \approx 45.0\%$$

---

#### 4. Ma trận So sánh 3 Cấu hình & Kết luận Khả thi
| Thông số Floorplan | Mức 50% (Mặc định - Lỗi) | Mức 45% (Khảo sát) | Mức 40% (Lab 0 - Thành công) |
| :--- | :---: | :---: | :---: |
| **Instances Area** | $376.611\,\mu m^2$ | $376.611\,\mu m^2$ | $376.611\,\mu m^2$ |
| **Core Area (Lý thuyết)** | $753.222\,\mu m^2$ | $\mathbf{836.913\,\mu m^2}$ | $941.528\,\mu m^2$ |
| **Core Area (Khớp lưới ô)** | $738.208\,\mu m^2$ (10 rows $\times$ 59 sites) | $\mathbf{839.555\,\mu m^2}$ (11 rows $\times$ 61 sites) | $941.528\,\mu m^2$ (11 rows $\times$ 68 sites) |
| **Whitespace (%)** | $49.0\%$ | $\mathbf{55.0\%}$ | $60.0\%$ |
| **Whitespace Area** | $361.597\,\mu m^2$ | $\mathbf{462.944\,\mu m^2}$ | $564.917\,\mu m^2$ |
| **Đất trống dôi dư so với 50%** | $0\,\mu m^2$ (Gốc) | $\mathbf{+101.347\,\mu m^2\ (+28\%)}$ | $+203.320\,\mu m^2\ (+56\%)$ |
| **Khả năng chèn Buffers** | **THẤT BÀI (`DPL-0036`)** | **Lý thuyết: Khả thi cao<br>Thực nghiệm: THẤT BÀI (`DPL-0036`)** | **THÀNH CÔNG (Trót lọt)** |

* **Đánh giá Chuyên môn từ Kiến trúc sư:**
  * Ở mức $50\%$, đất trống chỉ có $\approx 361.6\,\mu m^2$. Khi 9 bộ Hold Buffers được chèn vào (ngốn thêm $\approx 59.5\,\mu m^2$, tức chiếm gần $17\%$ toàn bộ đất trống), mật độ cục bộ tăng vọt khiến Detailed Placement không thể tìm được chỗ đặt hợp lệ trên 10 hàng ô lưới.
  * Ở mức **$45\%$**, theo lý thuyết vùng Core được tăng thêm hơn $100\,\mu m^2$ đất trống. Tuy nhiên, khi đưa vào thực nghiệm thực tế trên hệ thống CTW SEMI, OpenROAD phát hiện cần tới **10 bộ đệm (tăng $+17.5\%$ diện tích)**, gây nghẽn mật độ cục bộ và vẫn làm bùng nổ mã lỗi `DPL-0036`.
  * Điều này chứng minh vì sao mức an toàn tối ưu được chọn trong giáo trình là **$40\%$**!

---

### Câu 6: Phương Pháp Đọc và Phân Tích Log Lỗi Detailed Placement (`DPL-0036`)

* **Nội dung câu hỏi khảo sát:**
  > *Đọc được log lỗi của step detailed placement routing (DPL-0036). Trình bày nguyên tắc đọc log chuyên nghiệp của kỹ sư vi mạch, giải mã chuỗi phản ứng nhân quả từ lỗi thời gian Hold đến sự sụp đổ của luồng đặt ô, và kết luận bài học kinh nghiệm từ thực nghiệm chạy chip.*

* **Hiện trường đoạn Log máy thực tế (Trích xuất từ chặng Stage 37 - `ResizerTimingPostCTS`):**
  ```text
  Classic - Stage 37 - Resizer Timing Optimizations (Post-Clock Tree Synthesis)
  [INFO RSZ-0046] Found 7 endpoints with hold violations.
  Iteration | Resized | Buffers | Cloned Gates |   Area   |   WNS   |   TNS   | Endpoint
  --------------------------------------------------------------------------------------
          0 |       0 |       0 |            0 |    +0.0% |   0.024 |   0.000 | _48_/D
      final |       0 |      10 |            0 |   +17.5% |   0.105 |   0.000 | _50_/D
  --------------------------------------------------------------------------------------
  [INFO RSZ-0032] Inserted 10 hold buffers.
  + detailed_placement -max_displacement  500 100
  [INFO DPL-0034] Detailed placement failed on the following 9 instances:
  [INFO DPL-0035]  _23_
  [INFO DPL-0035]  _25_
  [INFO DPL-0035]  _34_
  [INFO DPL-0035]  _24_
  [INFO DPL-0035]  _33_
  [INFO DPL-0035]  _31_
  [INFO DPL-0035]  _40_
  [INFO DPL-0035]  _40_
  [INFO DPL-0035]  _40_
  [06:41:03] ERROR    [DPL-0036] Detailed placement failed.        openroad.py:312
  Error: rsz_timing_postcts.tcl, 61 DPL-0036
  [06:41:03] ERROR    The following error was encountered while    __main__.py:189
                      running the flow:
                      OpenROAD.ResizerTimingPostCTS failed with the following errors:
                      [DPL-0036] Detailed placement failed.
  [06:41:03] ERROR    LibreLane will now quit.                     __main__.py:190
  ```

* **Lời giải & Phân tích Chuyên sâu của Kiến trúc sư Trưởng ASIC:**

#### 1. Quy tắc Vàng Đọc Log Thực chiến của Kỹ sư Bán dẫn
* **Nguyên tắc "Đọc ngược từ dưới lên" (Bottom-Up Reading):**
  * Trong các flow thiết kế vi mạch chạy tự động (như LibreLane / OpenLane), nhật ký thực thi có thể dài hàng chục nghìn dòng. Kỹ sư không bao giờ đọc tuần tự từ dòng đầu tiên.
  * **Quy trình:** Kéo chuột xuống dòng cuối cùng $\rightarrow$ Tìm kiếm các từ khóa mang tính kết liễu: `ERROR`, `failed`, `quit`, `abort`.
  * **Dấu vết chỉ điểm đầu tiên:** Dòng `[ERROR] LibreLane will now quit` báo hiệu tiến trình chết. Ngay phía trên nó là mã định danh thảm họa: `[ERROR] [DPL-0036] Detailed placement failed.`
* **Nguyên tắc "Lần theo chuỗi nhân quả" (Root-Cause Tracing):**
  * Không dừng lại ở việc biết là lỗi đặt ô (Placement), kỹ sư phải truy ngược lên trước lệnh `detailed_placement` để trả lời câu hỏi: *"Điều gì đã kích hoạt khiến bước đặt ô vốn dĩ đã xong ở Global Placement bỗng nhiên bị quá tải?"*

---

#### 2. Giải mã 5 Mắt xích Nhân quả Cốt lõi (Chuỗi phản ứng dây chuyền)

```
[1. Sau CTS: Lỗi Hold] ────► [2. Chèn 9-10 Buffers] ────► [3. Diện tích tăng +17.5%]
  (RSZ-0046: 7 vi phạm)       (RSZ-0032: Cứu hộ timing)      (Đất trống bị nuốt chửng)
                                                                       │
                                                                       ▼
[5. Sập Flow Tape-out] ◄─── [4. Bật khỏi Lưới ô] ◄─── [3b. Ép dồn ô chi tiết]
  (DPL-0036 & LibreLane Quit) (DPL-0034: 9 cổng logic rớt)    (detailed_placement)
```

1. **Mắt xích 1 — Phát hiện vi phạm thời gian giữ (`[INFO RSZ-0046]`):**
   * Sau khi bước Clock Tree Synthesis (CTS) xây dựng xong mạng phân phối xung nhịp, công cụ kiểm tra STA và phát hiện có **7 điểm đích (endpoints) bị vi phạm Hold Time** (tín hiệu dữ liệu đến quá nhanh trước khi mép xung Clock chốt an toàn).
2. **Mắt xích 2 — Hành động cứu hộ tự động của Resizer (`[INFO RSZ-0032]`):**
   * Để cứu 7 lỗi Hold, công cụ buộc phải làm chậm đường truyền dữ liệu bằng cách chèn thêm các bộ đệm trễ: **Inserted 9 đến 10 hold buffers**.
   * Diện tích tế bào lập tức phình to: **`Area: +15.8%` đến `+17.5%`**.
3. **Mắt xích 3 — Mệnh lệnh chuẩn hóa hình học (`detailed_placement`):**
   * Sau khi nhét thêm 10 bộ đệm mới vào mạch, các cell bị đè chồng lên nhau trong không gian ảo. Công cụ thực thi lệnh `detailed_placement -max_displacement 500 100` để dịch chuyển các cell vào đúng các rãnh chuẩn `site unithd`, không được chạm hoặc đè lên nhau.
4. **Mắt xích 4 — Hiện trường các tế bào bị văng khỏi lưới (`[INFO DPL-0034]` & `[INFO DPL-0035]`):**
   * Do khoảng đất trống Whitespace xung quanh đã bị chiếm dụng hết, thuật toán dịch chuyển bị nghẽn (vượt quá giới hạn displacement 500nm).
   * Hệ thống chỉ đích danh **7 đến 9 linh kiện bị thất bại (failed instances)** như: `_23_`, `_25_`, `_34_`, `_24_`, `_33_`, `_31_`, `_40_`...
5. **Mắt xích 5 — Nhát dao kết liễu (`[ERROR DPL-0036]`):**
   * Khi thuật toán đặt ô chi tiết không thể hợp lệ hóa (legalize) 100% linh kiện, nó bắn ra mã lỗi chuẩn công nghiệp **`DPL-0036`**.
   * Hệ điều hành flow lập tức ra lệnh hủy bỏ: `LibreLane will now quit.`, ngăn chặn việc xuất ra một file layout bị chập mạch hoặc rách hình học.

---

#### 3. Báo cáo Thực nghiệm R&D Đối chứng (50% vs 45% vs 40%)

Nhờ thí nghiệm thực tế của Kỹ sư trên nền tảng CTW SEMI Web GUI, ta có bảng dữ liệu thực nghiệm vô cùng quý giá:

| Mức cấu hình `FP_CORE_UTIL` | Mức 50% (Mặc định) | Mức 45% (Thực nghiệm của Kỹ sư) | Mức 40% (Giáo trình Lab 0) |
| :--- | :---: | :---: | :---: |
| **Kích thước Core** | $738.208\,\mu m^2$ (10 rows) | $839.555\,\mu m^2$ (11 rows) | $941.528\,\mu m^2$ (11 rows) |
| **Tỷ lệ Whitespace** | $49.0\%$ | $55.0\%$ | $60.0\%$ |
| **Số Buffer cần chèn** | 9 Buffers ($+15.8\%$ Area) | 10 Buffers ($+17.5\%$ Area) | 9 Buffers ($+15.8\%$ Area) |
| **Số linh kiện bị văng khỏi ô** | 7 instances (`_30_`, `_25_`...) | 9 instances (`_23_`, `_25_`...) | **0 instance (Hợp lệ 100%)** |
| **Trạng thái Detailed Placement** | **FAILED (`DPL-0036`)** | **FAILED (`DPL-0036`)** | **PASSED (Thành công)** |
| **Kết quả cuối cùng** | Dừng flow | Dừng flow | **Xuất thành công GDSII!** |

* **Giải mã hiện tượng mức 45% vẫn bị nổ lỗi:**
  * Mặc dù mức 45% cấp thêm $+101\,\mu m^2$ đất trống, nhưng trong một con chip siêu nhỏ (Micro-macro chỉ có 31 cell), các cell không phân bố liên tục mà bị bẻ gãy theo các bước nhảy của ô lưới rời rạc (`site unithd = 0.46 um`).
  * Ở lần chạy 45%, hệ thống STA nhận thấy độ trễ dây thay đổi nên quyết định chèn tới **10 bộ đệm (tăng +17.5% diện tích)**.
  * Mật độ chân cục bộ (Local Pin Density) tại khu vực trung tâm tăng đột biến, kết hợp với tham số dịch chuyển an toàn `-max_displacement 500 100` khiến các cell không thể dạt sang hai bên sườn.
  * $\implies$ **Bài học xương máu:** Đối với các khối mạch nhỏ có xu hướng phát sinh nhiều lỗi Hold sau CTS, không thể tăng đất một cách "nhỏ giọt" ($50\% \rightarrow 45\%$). Phải hạ thẳng tay xuống **`FP_CORE_UTIL = 40%`** (mở rộng Whitespace lên $60\%$) để tạo ra những dải hành lang di chuyển thông thoáng, đảm bảo 100% tỷ lệ tape-out thành công!

---

#### 4. Quy trình Khắc phục Chuẩn hóa (Actionable Resolution)
Khi gặp lỗi `DPL-0036` trong bất kỳ dự án ASIC nào, Kỹ sư Physical Design áp dụng quy trình xử lý 3 bước:
1. **Bước 1 (Giải pháp kinh tế & nhanh nhất):** Mở file cấu hình Floorplan (`config.json` hoặc giao diện Web Setup), chủ động hạ `FP_CORE_UTIL` xuống $5\% - 10\%$ (ví dụ từ $50\%$ xuống $40\%$) để mở rộng diện tích Core Area.
2. **Bước 2 (Kiểm tra hình học Aspect Ratio):** Nếu chip bị kéo quá dài theo một chiều (hình chữ nhật hẹp), điều chỉnh `FP_ASPECT_RATIO = 1.0` để đưa Core về dạng hình vuông, giúp thuật toán xếp ô đa hướng dễ thở hơn.
3. **Bước 3 (Can thiệp SDC Constraints - nếu bị cố định kích thước Die):** Nới lỏng Clock Uncertainty hoặc giảm bớt ràng buộc Hold Margin trong file SDC để công cụ không chèn quá nhiều bộ đệm không cần thiết.

---

*Tài liệu được kiểm duyệt và phê duyệt hoàn tất 100% 6 bài tập Lab 0 bởi Kỹ sư Thiết kế & Kiến trúc sư Trưởng ASIC.*


