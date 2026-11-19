# GIÁO TRÌNH LÝ THUYẾT & KINH NGHIỆM THỰC CHIẾN BUỔI 2
# CHỦ ĐỀ: RTL CODING & SYNTHESIS (TỔNG HỢP LOGIC NỀN TẢNG CHO ASIC)

---

## MỤC LỤC HỆ THỐNG
1. [Lời Mở Đầu: Định Hướng Nghề Nghiệp & Triết Lý Thực Hành Từ Giảng Viên](#1-lời-mở-đầu-định-hướng-nghề-nghiệp--triết-lý-thực-hành-từ-giảng-viên)
2. [Cấp Độ Trừu Tượng RTL & Bộ Quy Tắc Code Khả Tổng Hợp (Synthesizable RTL)](#2-cấp-độ-trừu-tượng-rtl--bộ-quy-tắc-code-khả-tổng-hợp-synthesizable-rtl)
3. [Bản Chất Phần Cứng: So Sánh Toàn Diện FPGA vs. ASIC](#3-bản-chất-phần-cứng-so-sánh-toàn-diện-fpga-vs-asic)
4. [Kiến Trúc Bộ Cỗ Máy Tổng Hợp: Yosys & ABC Engine](#4-kiến-trúc-bộ-cỗ-máy-tổng-hợp-yosys--abc-engine)
5. [Thư Viện Tế Bào Chuẩn (Standard Cell Library) & Bài Toán Đánh Đổi Lái Dòng (Drive Strength)](#5-thư-viện-tế-bào-chuẩn-standard-cell-library--bài-toán-đánh-đổi-lái-dòng-drive-strength)
6. [Chiến Lược Tổng Hợp: Hierarchical vs. Flat Synthesis](#6-chiến-lược-tổng-hợp-hierarchical-vs-flat-synthesis)
7. [Vật Lý Của Nhiễu Kim (Glitch) & Nghệ Thuật Chặn Đầu Chặn Đuôi Bằng Flip-Flop](#7-vật-lý-của-nhiễu-kim-glitch--nghệ-thuật-chặn-đầu-chặn-đuôi-bằng-flip-flop)
8. [Chiến Lược Reset Trên ASIC: Synchronous vs. Asynchronous Reset](#8-chiến-lược-reset-trên-asic-synchronous-vs-asynchronous-reset)
9. [Các Thuật Toán Tối Ưu Hóa Logic (Logic Optimization)](#9-các-thuật-toán-tối-ưu-hóa-logic-logic-optimization)
10. [Kiểm Tra Tương Đương & 3 Cạm Bẫy Gây Lệch Giữa RTL và Netlist (Simulation Mismatch)](#10-kiểm-tra-tương-đương--3-cạm-bẫy-gây-lệch-giữa-rtl-và-netlist-simulation-mismatch)
11. [Cẩm Nang Thực Hành Lab 1: Khảo Sát Khối Mạch & Synthesis Strategies](#11-cẩm-nang-thực-hành-lab-1-khảo-sát-khối-mạch--synthesis-strategies)

---

## 1. LỜI MỞ ĐẦU: ĐỊNH HƯỚNG NGHỀ NGHIỆP & TRIẾT LÝ THỰC HÀNH TỪ GIẢNG VIÊN

### 1.1 Giá Trị Thực Tế & Định Hướng Xây Dựng Cộng Đồng
* **Tài nguyên tri thức quý hiếm:** Các kiến thức chuyên sâu về **Physical Design (BD/PD)**, quy trình **RTL Synthesis**, cùng các bài toán công nghệ bán dẫn (PDK) ở mức chuyên nghiệp cực kỳ khó tiếp cận miễn phí bên ngoài. Các khóa đào tạo tương đương tại các viện hoặc trung tâm thương mại đòi hỏi chi phí đầu tư rất lớn.
* **Mục tiêu khóa học:** Giáo trình được đúc kết từ hệ thống bài giảng vốn dùng để đào tạo giảng viên đại học chuyên ngành vi mạch, với tôn chỉ xây dựng một thế hệ kỹ sư thiết kế phần cứng Việt Nam có tư duy silicon thực chiến, nắm vững bản chất vật lý chứ không dừng lại ở mức mô phỏng phần mềm.

### 1.2 Cơ Hội Tham Gia Dự Án Silicon Thực Tế
* **Kênh tuyển chọn nhân tài:** Giảng viên thiết lập kho chứa mã nguồn (GitHub Repository) riêng cho lớp.
* **Tiêu chí đánh giá của Kiến trúc sư Trưởng:**
  * Nộp bài sớm, tinh thần học tập chủ động và kỷ luật.
  * Báo cáo kỹ thuật trình bày mạch lạc, tường minh, có hình ảnh và dẫn chứng số liệu định lượng (Waveform, Schematic, Area, Timing).
  * Hiểu sâu bản chất vấn đề thay vì chỉ "chạy lệnh theo vẹt".
* Những học viên xuất sắc nhất sẽ được giảng viên mời tham gia trực tiếp vào các **dự án chip thực tế (Real Tape-out Projects)**.

### 1.3 Triết Lý Thực Hành: "Không Làm Lab Là Vô Nghĩa"
> *Nghe giảng lý thuyết chỉ giúp tích lũy 10% nhận thức. 90% tư duy của một kỹ sư vi mạch được tôi luyện khi đối mặt với lỗi công cụ (EDA Errors), nhìn trực diện vào sơ đồ nguyên lý (Schematic), phân tích biểu đồ sóng (Waveform), và đọc hiểu ma trận thời gian (Timing Reports).*

Thiết kế vi mạch đòi hỏi **khả năng ước lượng phần cứng (Hardware Intuition)**: Khi gõ một dòng lệnh Verilog, trong đầu kỹ sư phải lập tức hiện ra cấu trúc cổng logic, số transistor tương ứng và đường trễ vật lý trên silicon.

---

## 2. CẤP ĐỘ TRỪU TƯỢNG RTL & BỘ QUY TẮC CODE KHẢ TỔNG HỢP (SYNTHESIZABLE RTL)

### 2.1 Cấp Độ Trừu Tượng RTL (Register-Transfer Level)
* **Khái niệm:** RTL là mức mô tả hành vi của hệ thống số thông qua sự dịch chuyển của dữ liệu giữa các thanh ghi (Registers / Flip-Flops) và các phép toán biến đổi trên khối logic tổ hợp (Combinational Logic).
* **Đặc tính:** Ở cấp độ này, môi trường mô phỏng hoạt động trong điều kiện **lý tưởng tuyệt đối**:
  * Chưa có khái niệm độ trễ lan truyền của dây dẫn kim loại (Wire Delay = 0).
  * Chưa có thời gian đóng ngắt của transistor (Gate Delay = 0).
  * Mục tiêu chính: Kiểm tra tính đúng đắn về thuật toán và chức năng số (Functional Verification).

```
   [ Ý tưởng / Thuật toán ]
              │
              ▼
    [ Mô tả RTL (.v) ]       <--- Cấp độ trừu tượng lý tưởng (Mô phỏng chức năng)
              │
      (Logic Synthesis)
              ▼
   [ Gate Netlist (.v) ]     <--- Cấp độ vật lý cụ thể (Map vào Standard Cells)
```

### 2.2 Định Nghĩa Code Khả Tổng Hợp (Synthesizable RTL)
* Một đoạn mã Verilog được coi là **Khả tổng hợp (Synthesizable)** khi và chỉ khi trình biên dịch (Yosys) có thể ánh xạ 1-1 các cú pháp ngôn ngữ thành các phần tử phần cứng có thật (Cổng logic, DFF, MUX, Tristate Buffer).
* Những cú pháp dùng cho môi trường Testbench mô phỏng như `#delay`, `initial`, `$display`, `$finish`, `real`, `time`... là **bất khả tổng hợp (Non-synthesizable)** và sẽ bị trình tổng hợp từ chối hoặc bỏ qua.

### 2.3 Ba Khối Phần Tử Cơ Sở Của Thế Giới Số

#### A. Bộ Chọn Kênh (Multiplexer - MUX)
* **Bản chất:** Mạch tổ hợp cho phép chọn 1 trong $N$ ngõ vào dữ liệu để đưa ra ngõ ra duy nhất dựa vào tín hiệu điều khiển chọn kênh ($Sel$).
* **Cú pháp Verilog chuẩn công nghiệp:**
  * *Dạng toán tử điều kiện (Continuous Assignment):*
    ```verilog
    assign Y = Sel ? I1 : I0; // MUX 2:1
    ```
  * *Dạng khối Procedural (`always`):*
    ```verilog
    always @(*) begin
        if (Sel)
            Y = I1;
        else
            Y = I0;
    end
    ```

#### B. Phần Tử Nhớ (D-Flip-Flop - DFF)
* **Bản chất:** Khối tuần tự lưu trữ 1-bit dữ liệu, bắt nhịp theo cạnh xung nhịp (Clock Edge).
* **Quy tắc sinh tử về Tín hiệu Khởi tạo (Reset/Set):**
  * Trên mạch thật, khi vừa bật nguồn ($V_{DD}$), các nút mạch trôi nổi ở trạng thái điện thế bất định.
  * Nếu Flip-Flop không có chân Reset/Set, ngõ ra sẽ mang giá trị không xác định (**trạng thái $X$** trong mô phỏng). Trạng thái $X$ này sẽ lan truyền qua toàn bộ hệ thống logic tổ hợp, làm sụp đổ toàn bộ chức năng của con chip.
  * $\implies$ **Mọi Flip-Flop trên ASIC bắt buộc phải có cơ chế Reset** để ép mạch về trạng thái ban đầu xác định (`0` hoặc `1`).

#### C. Bộ Đếm (Counter) & Kỹ Thuật Tham Số Hóa (Parameterization)
* **Cấu trúc:** Sự kết hợp hoàn mỹ của 3 thành phần:
  $$\text{Counter} = \text{Bộ cộng (Adder)} + \text{Bộ chọn kênh (MUX)} + \text{Dàn thanh ghi (DFFs)}$$
* **Khuyên dùng `parameter` để IP hóa:**
  * Tuyệt đối tránh việc gán cứng kích thước bit (Hardcoding: `[7:0]`).
  * Khai báo bằng `parameter WIDTH = 8;` giúp mô-đun trở thành một khối sở hữu trí tuệ (IP Core) linh hoạt, có thể tái sử dụng ở bất kỳ dự án nào chỉ bằng cách gán lại tham số khi đóng gói (Instantiation).

---

## 3. BẢN CHẤT PHẦN CỨNG: SO SÁNH TOÀN DIỆN FPGA VS. ASIC

Mặc dù cùng viết bằng ngôn ngữ Verilog, con đường vật lý đi tới phần cứng của FPGA và ASIC là hai thế giới hoàn toàn khác biệt:

| Tiêu Chí Kỹ Thuật | Nền Tảng FPGA | Thiết Kế ASIC / Silicon |
| :--- | :--- | :--- |
| **Bản chất phần cứng** | Tài nguyên định hình sẵn (LUTs, DSP, BRAM) chế tạo bằng bộ nhớ SRAM. | Tấm bán dẫn trống. Toàn bộ cổng logic và dây nối được khắc chết vĩnh viễn trên silicon. |
| **Cơ chế hiện thực** | Nạp chuỗi bitstream để đóng/ngắt các công tắc liên kết các khối LUT có sẵn. | Ánh xạ vào Thư viện Tế bào chuẩn (**Standard Cell Library**) của nhà máy đúc (Foundry). |
| **Sửa lỗi vi phạm Timing** | Tối ưu bằng thuật toán phần mềm định tuyến lại (Place & Route) trên fabric có sẵn. | Trình tổng hợp tự động **chèn các cổng Buffer vật lý** để cân bằng trễ hoặc tăng diện tích die. |
| **Chi phí & Độ linh hoạt** | Không mất phí làm khuôn; sửa code nạp lại trong vài giây; chip giá thành cao theo đơn vị. | Chi phí mặt nạ quang khắc (Mask) hàng trăm nghìn USD; **Trên silicon không có nút Ctrl+Z**. |
| **Độ tin cậy thiết kế** | Cho phép chấp nhận các cú pháp lỏng lẻo, Reset bất đồng bộ bừa bãi. | Kỷ luật thiết kế cực kỳ khắt khe; kiểm tra Signoff (DRC, LVS, STA) tuyệt đối. |

> ⭐ **Quy Tắc Vàng:**  
> **"Một mạch thiết kế chuẩn chạy đúng trên ASIC thì hầu như 100% sẽ chạy được trên FPGA. Nhưng một đoạn code chạy thành công trên FPGA thì CHƯA CHẮC đã tổng hợp hoặc hoạt động được trên ASIC!"**

---

## 4. KIẾN TRÚC BỘ CỖ MÁY TỔNG HỢP: YOSYS & ABC ENGINE

Trong luồng thiết kế mã nguồn mở (LibreLane / OpenLane), quá trình Tổng hợp Logic (Logic Synthesis) được vận hành bởi sự phối hợp nhịp nhàng giữa hai cỗ máy cốt lõi:

```
  [ RTL Verilog (.v) ] ──► [ YOSYS: Phân tích cú pháp & Dịch Generic Logic ]
                                      │
  [ Thư viện (.lib)  ] ──► [ ABC: Tối ưu Boolean & Technology Mapping      ]
                                      │
                                      ▼
                        [ Gate-Level Netlist (.v) ]
```

### 4.1 Vai Trò của Yosys
* **Frontend Parser:** Đọc mã nguồn Verilog, kiểm tra tính hợp lệ về mặt ngữ pháp phần cứng.
* **Elaboration:** Phân giải các tham số `parameter`, unroll các vòng lặp `generate`.
* **Generic Synthesis:** Chuyển đổi các cấu trúc trừu tượng (phép `+`, `-`, `*`, `always`, `case`) thành một sơ đồ mạch logic tổng quát (Generic Gates: các cổng logic lý tưởng `$_AND_`, `$_NOT_`, `$_MUX_`, `$_DFF_`).

### 4.2 Vai Trò của ABC (UC Berkeley ABC Engine)
* **Logic Optimization:** Biến đổi mạng logic tổng quát thành các đồ thị Boolean tối giản (AIG - And-Inverter Graph), triệt tiêu các cổng dư thừa.
* **Technology Mapping (Ánh xạ công nghệ):** Đọc tệp thư viện công nghệ (`.lib`), lựa chọn chính xác các tế bào chuẩn có sẵn trong thư viện (NAND, NOR, DFF, MUX của SkyWater 130nm) sao cho thỏa mãn mục tiêu diện tích (Area) hoặc tốc độ (Speed).

### 4.3 Cấu Trúc Đặt Tên Chuẩn Của Standard Cell (Ví Dụ Sky130 HD)
Tên gọi của một ô chuẩn phản ánh toàn bộ lý lịch kỹ thuật của nó:
$$\mathbf{sky130\text{_}fd\text{_}sc\text{_}hd\text{__}nand2\text{_}2}$$
* `sky130`: Tiến trình công nghệ bán dẫn $130\,\text{nm}$ của SkyWater.
* `fd`: Foundry Direct (Do chính nhà máy cung cấp).
* `sc`: Standard Cell (Tế bào chuẩn).
* `hd`: High Density (Dòng thư viện mật độ cao, tiết kiệm diện tích).
* `nand2`: Cổng logic NAND có 2 ngõ vào.
* `_2`: **Drive Strength = 2** (Hệ số lái dòng cấp 2).

> 📌 **Quy ước ngõ ra:** Các ngõ vào của Standard Cell có thể mang nhiều tên (`A`, `B`, `C`, `A0`, `A1`, `S`...), nhưng **chân ngõ ra của ô chuẩn luôn luôn được định danh là `X` hoặc `Y`**.

---

## 5. THƯ VIỆN TẾ BÀO CHUẨN (STANDARD CELL LIBRARY) & BÀI TOÁN ĐÁNH ĐỔI LÁI DÒNG (DRIVE STRENGTH)

### 5.1 Bốn Phân Nhánh Thư Viện Ô Chuẩn Trong Công Nghiệp
Nhà máy bán dẫn cung cấp nhiều biến thể thư viện `.lib` cho cùng một tiến trình để kỹ sư lựa chọn tùy theo mục tiêu sản phẩm:
1. **High Density (`hd`):** Chiều cao hàng nhỏ ($2.72\,\mu m$), tối ưu hóa diện tích tối đa. Thích hợp cho chip IoT, chip điều khiển logic quy mô lớn.
2. **Low Leakage / Low Power (`lp`):** Sử dụng các transistor có điện áp ngưỡng ($V_{th}$) cao để triệt tiêu dòng rò rỉ khi mạch ở trạng thái tĩnh. Dành cho các thiết bị chạy pin.
3. **High Speed (`hs`) / Low Voltage:** Tối ưu hóa thời gian chuyển mạch nhanh nhất, dòng lái lớn. Dành cho các khối vi xử lý tính toán hiệu năng cao.
4. **High Voltage (`hv`):** Chịu được điện áp $3.3V$ hoặc $5.0V$, đường cấp nguồn rộng (4–5 grid lines), kích thước tế bào lớn. Dành cho mạch giao tiếp ngoại vi (IO/Pads) hoặc quản lý năng lượng.

### 5.2 Khái Niệm Drive Strength & Ma Trận Đánh Đổi
Drive Strength (con số đuôi của cell: `_0`, `_1`, `_2`, `_4`...) thể hiện kích thước vật lý của các transistor PMOS/NMOS bên trong tầng đệm ngõ ra của ô chuẩn:

| Cấp Độ Drive Strength | Ưu Điểm Kỹ Thuật | Nhược Điểm / Đánh Đổi | Vùng Ứng Dụng |
| :--- | :--- | :--- | :--- |
| **Drive Nhỏ (`_0`, `_1`)** | • Diện tích tế bào siêu nhỏ.<br>• Công suất tiêu thụ rò rỉ (Leakage) cực thấp. | • Dòng ra yếu, khả năng kéo tải kém.<br>• Nếu kéo nhiều cell (High Fanout), sườn xung bị lài (slew lớn) gây trễ mạch. | Mạch nội bộ cục bộ, ngõ ra chỉ kéo 1–2 cổng kế bên (Low Fanout). |
| **Drive Lớn (`_2`, `_4`)** | • Bơm dòng điện lớn, khả năng nạp/xả tụ tải nhanh.<br>• Kéo được nhiều cổng phía sau mà không bị sụt áp. | • Kích thước silicon to, ngốn diện tích.<br>• Công suất tiêu hao tĩnh và động rất lớn. | Chân phát tín hiệu phân nhánh lớn, đường dây tín hiệu kéo dài xuyên chip. |

### 5.3 Điều Kiện Vận Hành PVT (Process, Voltage, Temperature)
Một file `.lib` không đại diện cho con chip chung chung, mà đặc tả hành vi điện tử tại một góc điều kiện môi trường xác định:
* **Góc điển hình (Typical - `tt_025C_1v80`):** Quy trình chế tạo bình thường, điện áp danh định $1.8V$, nhiệt độ phòng $25^\circ C$.
* **Góc tồi tệ (Worst/Slow - `ss_100C_1v60`):** Transistor chậm, nhiệt độ cao $100^\circ C$, điện áp sụt giảm $1.6V$ (Dùng để kiểm tra vi phạm Setup Time).
* **Góc nhanh (Fast - `ff_n40C_1v95`):** Transistor nhanh, nhiệt độ âm $-40^\circ C$, điện áp dâng cao $1.95V$ (Dùng để kiểm tra vi phạm Hold Time).

---

## 6. CHIẾN LƯỢC TỔNG HỢP: HIERARCHICAL VS. FLAT SYNTHESIS

Khi thiết kế một hệ thống vi mạch gồm Top-module chứa nhiều Sub-modules con, kỹ sư phải quyết định chiến lược tổng hợp:

```
[ Top Module ]                     [ Top Module ]
  ├── [ Sub A ]                      └── (Xóa bỏ ranh giới)
  └── [ Sub B ]                            Cell_1, Cell_2, Cell_3...
(Hierarchical Synthesis)                 (Flat Synthesis)
```

### 6.1 Tổng Hợp Phân Cấp (Hierarchical Synthesis)
* **Cơ chế:** Duy trì nguyên vẹn cấu trúc ranh giới hình học giữa Top module và các module con. Các cổng logic của module nào sẽ nằm nguyên trong phạm vi module đó.
* **Ưu điểm:** Sơ đồ Netlist cực kỳ trong sáng, dễ đọc; khi có lỗi logic dễ dàng khoanh vùng chính xác module nào gây ra.
* **Nhược điểm:** Trình tổng hợp bị "trói tay", **không thể tối ưu hóa xuyên ranh giới (Cross-boundary Optimization)**. Nếu ngõ ra Module A có một Inverter và ngõ vào Module B có một Inverter khác nối tiếp, công cụ không thể tự triệt tiêu 2 Inverter này.

### 6.2 Tổng Hợp Trải Phẳng (Flat Synthesis)
* **Cơ chế:** Xóa sạch mọi ranh giới phân cấp, đổ toàn bộ hệ hàm Boolean của tất cả module con ra một mặt phẳng duy nhất.
* **Ưu điểm:** Đạt hiệu quả tối ưu hóa logic toàn cục cao nhất; triệt tiêu tối đa các cổng trung gian thừa, giảm diện tích chip và làm ngắn đường truyền dữ liệu.
* **Nhược điểm:** Tên các dây và các cổng logic bị đổi tên và xáo trộn hoàn toàn; cực kỳ khó khăn cho kỹ sư nếu phải can thiệp sửa lỗi Netlist bằng tay (Engineering Change Order - ECO).

---

## 7. VẬT LÝ CỦA NHIỄU KIM (GLITCH) & NGHỆ THUẬT CHẶN ĐẦU CHẶN ĐUÔI BẰNG FLIP-FLOP

### 7.1 Bản Chất Vật Lý Của Nhiễu Kim (Glitch)
* Trong mạch logic tổ hợp, tín hiệu từ ngõ vào truyền tới ngõ ra theo nhiều nhánh đường dẫn khác nhau.
* Mỗi cổng logic trên đường đi đều đóng góp một thời gian trễ lan truyền ($t_{pd}$). 
* Nếu nhánh A mất $1.0\,\text{ns}$ để chuyển mức, trong khi nhánh B mất $2.5\,\text{ns}$, tại nút hội tụ ngõ ra sẽ xuất hiện một khoảng thời gian chênh lệch $1.5\,\text{ns}$.
* Trong $1.5\,\text{ns}$ chênh lệch này, ngõ ra sẽ bị giật lên mức cao rồi sụt xuống mức thấp một cách đột ngột. Xung nhọn bất thường này gọi là **Nhiễu kim (Glitch / Hazard)**.

```
Nhánh A (Trễ 1.0ns): ────┐
                         ├──► [ Cổng Logic ] ──► Ngõ ra: ──┐   ┌─── (GLITCH!)
Nhánh B (Trễ 2.5ns): ────┘                                 └───┘
```

### 7.2 Phương Pháp Triệt Tiêu: Chặn Hai Đầu Bằng Flip-Flop
* **Nguyên lý:** Mạch tổ hợp tuyệt đối không được phép chạy tự do vô tận. Kỹ sư bắt buộc phải **chặn hai đầu của khối mạch tổ hợp bằng hai dàn Flip-Flop đồng bộ theo chu kỳ xung nhịp Clock**.
* **Điều kiện an toàn thời gian:** Chu kỳ xung nhịp ($T_{\text{clk}}$) phải luôn lớn hơn độ trễ của đường dẫn dài nhất (**Critical Path Delay**):
  $$T_{\text{clk}} > t_{\text{cq}} + t_{\text{comb\_max}} + t_{\text{setup}}$$
* **Kết quả:** Mọi xung nhiễu kim (Glitch) phát sinh bên trong khối tổ hợp sẽ dao động và tự triệt tiêu trong suốt nửa đầu chu kỳ. Đến khi cạnh xung nhịp kế tiếp ập đến, tín hiệu đã lắng đọng hoàn toàn ở trạng thái ổn định và được Flip-Flop chốt một cách an toàn tuyệt đối.

---

## 8. CHIẾN LƯỢC RESET TRÊN ASIC: SYNCHRONOUS VS. ASYNCHRONOUS RESET

Một trong những quyết định kiến trúc quan trọng nhất của kỹ sư RTL khi thiết kế chip là lựa chọn cơ chế Reset:

```verilog
// 1. Asynchronous Reset (Reset Bất đồng bộ)
always @(posedge clk or posedge rst) begin
    if (rst) Q <= 1'b0;
    else     Q <= D;
end

// 2. Synchronous Reset (Reset Đồng bộ)
always @(posedge clk) begin
    if (rst) Q <= 1'b0;
    else     Q <= D;
end
```

### Bảng So Sánh Chiến Lược Reset Cho Thiết Kế ASIC:

| Tiêu Chí Kỹ Thuật | Reset Bất Đồng Bộ (Asynchronous) | Reset Đồng Bộ (Synchronous) |
| :--- | :--- | :--- |
| **Thời điểm tác động** | Ngay lập tức khi chân `rst` lên mức 1, không cần Clock. | Chỉ có tác dụng tại cạnh lên của xung Clock. |
| **Phần cứng tổng hợp ra** | Sử dụng Flip-Flop chuyên dụng có chân Clear (`dfxtp_...`). | Sử dụng Flip-Flop thường + một bộ **MUX ở ngõ vào D**. |
| **Độ nhạy với nhiễu** | Cực kỳ nguy hiểm: Một tia nhiễu kim lọt vào chân `rst` sẽ reset toàn bộ chip ngay lập tức. | Rất an toàn: Mọi nhiễu trên đường `rst` đều bị lọc sạch nếu không rơi đúng mép Clock. |
| **Độ phức tạp STA** | Rất phức tạp: Dễ vi phạm Reset Recovery/Removal Time; phải đặt ngoại lệ `set_false_path`. | Cực kỳ đơn giản: Coi tín hiệu Reset như một đường dữ liệu (Data) thông thường. |
| **Khuyến nghị trên ASIC** | Chỉ dùng cho mạch Reset cấp hệ thống (POR - Power-On Reset). | **Được khuyến nghị tối đa cho 95% logic tuần tự trên ASIC.** |

---

## 9. CÁC THUẬT TOÁN TỐI ƯU HÓA LOGIC (LOGIC OPTIMIZATION)

Khi nhận Netlist thô từ RTL, công cụ ABC thực hiện hàng loạt thuật toán biến đổi đại số Boolean để nén mạch:

### 9.1 Kỹ Thuật Truyền Hằng Số (Constant Propagation)
* Nếu một ngõ vào của một hàm logic bị nối cứng xuống $0$ ($V_{SS}$) hoặc nối lên $1$ ($V_{DD}$), công cụ sẽ đơn giản hóa toàn bộ chuỗi cổng phía sau:
  * Ví dụ: Một cổng AND có 1 chân nối đất $0 \implies$ Ngõ ra luôn bằng $0 \implies$ Vứt bỏ toàn bộ cổng AND, thay bằng một đường nối GND.
* ⚠️ **Cảnh báo viết Testbench:** Khi viết kiểm thử (Verification), nếu kỹ sư quên không kích hoạt lật trạng thái (Toggle) một tín hiệu điều khiển, công cụ tổng hợp có thể lầm tưởng đó là hằng số và "xóa sổ" toàn bộ khối mạch logic mà kỹ sư đã cất công thiết kế!

### 9.2 Rút Gọn Đại Số Boolean & Bìa Karnaugh (K-Map Optimization)
* Các chuỗi câu lệnh `if-else` hoặc `case` lồng nhau phức tạp ở mức RTL thường tạo ra hàng loạt MUX mắc nối tiếp (Cascaded MUXes).
* Bộ tối ưu hóa logic sẽ gom toàn bộ bảng chân trị (Truth Table), phân tích logic đa mức (Multi-level logic synthesis), và nén các tầng MUX này thành các **cổng phức hợp siêu nhỏ** như `a21oi` (AND-OR-Invert) hay `o21a` (OR-AND), giúp làm ngắn đường trễ Critical Path đáng kể.

---

## 10. KIỂM TRA TƯƠNG ĐƯƠNG & 3 CẠM BẪY GÂY LỆCH GIỮA RTL VÀ NETLIST (SIMULATION MISMATCH)

### 10.1 Khái Niệm Gate-Level Simulation (GOS)
* Sau khi Yosys và ABC hoàn tất xuất ra file Netlist gồm các Standard Cells, kỹ sư **bắt buộc phải lấy lại chính file Testbench ban đầu của RTL để chạy mô phỏng lại với Netlist**.
* Nếu kết quả dạng sóng của Netlist lệch dù chỉ 1 chu kỳ xung nhịp so với RTL, bản thiết kế bị coi là phế phẩm. Toàn bộ khâu Backend phía sau đều vô giá trị.

### 10.2 Ba Cạm Bẫy Kinh Điển Khiến "Mô Phỏng Một Đằng, Tổng Hợp Một Nẻo"

```
┌────────────────────────────────────────────────────────────────────────┐
│              3 CẠM BẪY TỬ THẦN TRONG RTL VERILOG                       │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Thiếu Sensitive List ──► RTL hiểu là Latch, Synth ra Cổng Tổ hợp    │
│ 2. Nhầm Gán = và <=     ──► Gây Đua tín hiệu (Race Condition) & Glitch │
│ 3. Thiếu else / default ──► Tự động sinh Chốt Latch ngoài ý muốn       │
└────────────────────────────────────────────────────────────────────────┘
```

#### Bẫy 1: Khai Báo Thiếu Danh Sách Nhạy Cảm (Incomplete Sensitivity List)
* **Code sai lầm:**
  ```verilog
  always @(A) begin   // Quên không khai báo B!
      Y = A & B;
  end
  ```
* **Hậu quả tai hại:**
  * *Trong mô phỏng RTL:* Khi `B` thay đổi giá trị, khối `always` không chạy! Ngõ ra `Y` giữ nguyên giá trị cũ (Trình mô phỏng hành xử như một phần tử nhớ Latch).
  * *Trong tổng hợp Logic:* Trình tổng hợp Yosys hiểu bản chất đây là hàm AND, nên tổng hợp ra một cổng AND chuẩn mà không có Latch nào cả!
  * $\implies$ **Dạng sóng mô phỏng RTL và mạch thật Netlist hoàn toàn đá nhau!**
* **Khắc phục:** Luôn luôn sử dụng cú pháp tự động nhận diện: `always @(*)` hoặc chuẩn SystemVerilog `always_comb`.

#### Bẫy 2: Dùng Lẫn Lộn Phép Gán Blocking (`=`) và Non-blocking (`<=`)
* **Quy tắc bất di bất dịch:**
  * **Mạch tổ hợp (Combinational):** Bắt buộc dùng phép gán **Blocking (`=`)**.
  * **Mạch tuần tự (Flip-Flops):** Bắt buộc dùng phép gán **Non-blocking (`<=`)**.
* **Hậu quả nếu dùng gán `=` trong Flip-Flop:**
  Các phép gán bị ép thực thi tuần tự từng dòng từ trên xuống dưới, tạo ra hiện tượng **Đua tranh tín hiệu (Race Condition)**. Dữ liệu từ Flip-Flop tầng 1 trượt thẳng qua Flip-Flop tầng 2 trong cùng 1 chu kỳ xung nhịp, phá hỏng nguyên lý thanh ghi dịch.

#### Bẫy 3: Thiếu Nhánh `else` Hoặc `default` (Inferred Latch Generation)
* **Code sai lầm:**
  ```verilog
  always @(*) begin
      if (en)
          out = data_in; // Quên không viết nhánh else!
  end
  ```
* **Hậu quả phần cứng:** Khi `en = 0`, mạch phải giữ lại giá trị cũ của `out`. Để "nhớ" được giá trị này mà không có xung Clock, trình tổng hợp buộc phải tự động tạo ra một **Chốt dữ liệu (Transparent Latch)**.
* **Tác hại trên ASIC:** Latch là kẻ thù số 1 của thiết kế vi mạch đồng bộ. Nó làm công cụ phân tích thời gian tĩnh (STA) bị mù đường dẫn trễ, cực kỳ dễ gây trôi timing và nghẽn Placement.

---

## 11. CẨM NANG THỰC HÀNH LAB 1: KHẢO SÁT KHỐI MẠCH & SYNTHESIS STRATEGIES

### 11.1 Hệ Sinh Thái Công Cụ Thực Hành
* **`iverilog` (Icarus Verilog):** Trình biên dịch mã nguồn RTL và Testbench để kiểm tra chức năng.
* **`GTKWave`:** Trình hiển thị và đo đạc dạng sóng tín hiệu số từ file dump `.vcd`.
* **`Yosys` & `ABC`:** Động cơ tổng hợp logic và công nghệ mapping.
* **`CTW SEMI Web GUI`:** Cockpit đồ họa hiển thị trực quan sơ đồ cổng logic (Schematic Viewer) và phân tích các tệp log.

### 11.2 Nhiệm Vụ Trọng Tâm Của Bài Lab 1
1. **Thiết kế & Tổng hợp 4 Khối Mạch Nền Tảng:**
   * Bộ dồn kênh (Multiplexer - MUX).
   * Bộ cộng lan truyền chuỗi (Ripple Carry Adder - RCA).
   * Bộ nhân nhị phân 8-bit (Multiplier).
   * Bộ đếm gợn sóng (Ripple Counter).
2. **Khảo Sát Các Chiến Lược Tổng Hợp (Synthesis Strategies):**
   * Trong ABC/Yosys, thay đổi các cờ cấu hình chiến lược (Strategies: Tối ưu diện tích `AREA`, Tối ưu tốc độ `DELAY`, hoặc Cân bằng `BALANCED`).
   * Điền và đối chiếu bảng chỉ số định lượng:
     $$\mathbf{Total\ Cell\ Count} \quad \longleftrightarrow \quad \mathbf{Total\ Area\ (\mu m^2)} \quad \longleftrightarrow \quad \mathbf{Dynamic\ \&\ Leakage\ Power\ (mW)}$$

---

---

## 12. KẾ HOẠCH HÀNH ĐỘNG 5 CHẶNG (MASTER PLAN) & VAI TRÒ CỦA KHO MẪU sky130Examples.zip

### 12.1 Vai Trò Sống Còn của Kho Tài Nguyên `sky130Examples.zip`
File nén `sky130Examples.zip` (dung lượng $\approx 28.8\,\text{MB}$, chứa 1.809 tệp tin) là kho tài nguyên thực chiến đồng hành xuyên suốt từ Buổi 2 tới các bài Lab nâng cao, mang 4 giá trị kỹ thuật cốt lõi:
1. **Chìa khóa nâng cấp công cụ CTW SEMI (`capnhatctwsemi.txt`):** Script tự động kéo bản Docker `huyatieo/ctwsemi:1.0.1` tích hợp tính năng **Schematic Viewer** ngay trên Web GUI (xem sơ đồ cổng logic trực quan).
2. **Cung cấp mã nguồn chuẩn cho Lab 1:** Chứa sẵn 2 file thiết kế nền tảng: `rca.v` (Ripple Carry Adder 8-bit) và `fa.v` (Full Adder 1-bit), cùng file testbench `tb_rca.v`.
3. **Thư viện ô chuẩn gốc của Nhà máy SkyWater (`.lib` & `.db`):** File `sky130_fd_sc_hd__tt_025C_1v80.lib` chứa toàn bộ dữ liệu tế bào chuẩn của SkyWater 130nm, là "thước đo chân lý" để ABC tính toán Area, Timing arcs, Pin capacitance.
4. **Kho tàng 1.500+ bài thực nghiệm đối chứng (Benchmark Suite):** Chứa các cặp bài trùng giải thích bằng thực nghiệm toàn bộ lý thuyết Buổi 2:
   * `good_mux.v` vs `bad_mux.v` / `good_counter.v` vs `bad_counter.v`.
   * `blocking_caveat.v` (Bẫy lỗi dùng nhầm dấu `=` trong DFF).
   * `incomp_if.v`, `incomp_case.v` (Bẫy lỗi tự sinh chốt Latch ngoài ý muốn).
   * `dff_const1.v` đến `dff_const5.v` (Thực nghiệm Constant Propagation).
   * `dff_asyncres.v` vs `dff_syncres.v` (So sánh phần cứng Reset).

### 12.2 Kế Hoạch 5 Chặng Chinh Phục Lab 1 (Master Plan)

```mermaid
flowchart LR
    P1["CHẶNG 1<br>Lý thuyết ABC & .lib"] --> P2["CHẶNG 2<br>Môi trường & Setup Lab1"]
    P2 --> P3["CHẶNG 3<br>Thí nghiệm 1: Strategies"]
    P3 --> P4["CHẶNG 4<br>Thí nghiệm 2: Ép Cell Thủ công"]
    P4 --> P5["CHẶNG 5<br>Báo cáo & Niêm phong"]

    style P1 fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#fff
    style P2 fill:#1e293b,stroke:#8b5cf6,stroke-width:2px,color:#fff
    style P3 fill:#1e293b,stroke:#f59e0b,stroke-width:2px,color:#fff
    style P4 fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#fff
    style P5 fill:#450a0a,stroke:#ef4444,stroke-width:2px,color:#fff
```

* **Chặng 1: Nắm vững Nền tảng Lý thuyết ABC & File Liberty `.lib`:**
  * Giải mã 7 thông tin ABC nhìn thấy trong `.lib`: Boolean function, Area, Timing arcs, Pin capacitance, Driving cell, Output load, Allowed cell set.
  * Hiểu rõ 3 biến cấu hình synthesis: `SYNTH_STRATEGY` (Area vs Delay), `SYNTH_HIERARCHY_MODE` (Flatten vs Keep), và `SYNTH_SHARE_RESOURCE`.
* **Chặng 2: Chuẩn Bị Môi Trường & Triển Khai Dữ Liệu:**
  * Giải nén `sky130Examples.zip` vào `ctwsemi-data` (trên WSL và Windows).
  * Khởi tạo dự án `Lab1` gồm 2 file cốt lõi: `rca.v` và `fa.v`.
  * Khởi động web CTW SEMI (`http://127.0.0.1:8765/`), trỏ tới `Lab1`, bật `Auto-generate config` và đặt tham số móng: `FP_CORE_UTIL = 40%`.
* **Chặng 3: Thí Nghiệm 1 — Ma Trận Chiến Lược Tổng Hợp (Synthesis Strategies):**
  * Bật Schematic Viewer soi mạch cộng 8-bit RCA (chuỗi 8 khối FA lan truyền bit nhớ $C_{\text{in}} \rightarrow C_{\text{out}}$).
  * Chạy Baseline (`rca-run-base`): Cấu hình `AREA 0`, `flatten`. Phân tích netlist `rca.nl.v` và log `yosys-synthesis.log` (Giải thích tại sao mất khối `fa`, giải mã con số 37 cell vs 32 cell logic vs 41 cell tổng).
  * Chạy đối chứng 3 kịch bản: `AREA 3` (Tối ưu diện tích sâu), `DELAY 0` (Tối ưu tốc độ), `HIERARCHY = keep` (Giữ nguyên phân cấp).
  * Hoàn thành bảng ma trận: Số Cell — Diện tích (Area) — Trễ (Delay ABC) — Diện tích ABC.
* **Chặng 4: Thí Nghiệm 2 — Kỹ Thuật Ép Cell Thủ Công (Manual Instantiation):**
  * Sửa code gọi đích danh ô chuẩn Sky130: `sky130_fd_sc_hd__fa_1`.
  * Biện luận bài toán đánh đổi: Kiểm soát 100% phần cứng $\leftrightarrow$ Mất tính Portable sang các nhà máy đúc khác và làm mất quyền tối ưu toàn cục của ABC.
* **Chặng 5: Đúc Kết Báo Cáo & Khảo Sát Câu Hỏi Trung Tâm:**
  * Trả lời dứt điểm câu hỏi lớn của Lab 1: *"ABC chọn cell dựa vào đâu và người thiết kế có thể tự chọn cell hay không?"*
  * Khởi tạo và niêm phong báo cáo hoàn chỉnh `Lab1_Ghi_Chep_Kien_Thuc.md`.

---

### 12.3 Bản Chất & Vai Trò Của Tệp Lệnh `config.json` Trong Toàn Bộ Luồng Physical Design
* **Bản chất "Hồ sơ thiết kế thi công":** `config.json` không phải là file cấu hình riêng của Yosys hay ABC, mà là **Tập lệnh Tổng chỉ huy (Master Configuration)** đứng ở tầng cao nhất bao trùm toàn bộ quy trình từ RTL đến GDSII.
* **Vai trò điều khiển các khâu Backend tiếp theo (sau Synthesis):**
  * **Floorplan:** Cấp diện tích vùng lõi qua `FP_CORE_UTIL`, tỷ lệ khung `FP_ASPECT_RATIO`, khoảng đệm biên `CORE_MARGIN` (bảo vệ chân IO và vòng đai nguồn).
  * **Placement:** Kiểm soát mật độ dồn ô mục tiêu qua `PL_TARGET_DENSITY`.
  * **CTS:** Chỉ định danh sách ô đệm xung nhịp chuyên dụng qua `CTS_CLK_BUFFER_LIST` và giới hạn lệch pha `CTS_TARGET_SKEW`.
  * **Routing:** Giới hạn tầng kim loại cho phép đi dây qua `RT_MIN_LAYER` và `RT_MAX_LAYER`.
  * **Signoff:** Kích hoạt bộ luật kiểm tra hình học DRC và LVS chuẩn xưởng qua `PDK = sky130A`.
* **Mối liên hệ nhân quả:** Quyết định tại 3 biến `SYNTH_STRATEGY`, `SYNTH_HIERARCHY_MODE`, `SYNTH_SHARE_RESOURCE` ở bước Synthesis sẽ quyết định kích thước, số lượng cổng và độ dài đường trễ tới hạn (Critical Path), từ đó tác động trực tiếp lên khả năng đi dây, mức độ nghẽn mạch và nguy cơ vi phạm thời gian Setup/Hold ở tất cả các bước phía sau.

---

*Tài liệu được biên soạn và lưu trữ chuẩn mực theo hệ thống giáo trình Đào tạo Kỹ sư Thiết kế Vi mạch chuyên nghiệp (RTL-to-GDSII ASIC Flow).*
