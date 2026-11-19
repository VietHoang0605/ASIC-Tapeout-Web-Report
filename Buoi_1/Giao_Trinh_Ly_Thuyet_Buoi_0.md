# HƯỚNG DẪN HỌC TẬP THIẾT KẾ VẬT LÝ VI MẠCH TỪ RTL ĐẾN GDSII
*(Tài liệu Cơ sở Lý thuyết Nền tảng — Buổi 0)*

---

## 1. TỔNG QUAN QUY TRÌNH THIẾT KẾ VI MẠCH (RTL TO GDSII)

Quy trình thiết kế vi mạch số (**Digital ASIC Design Flow**) là chuỗi các bước biến đổi liên tục một ý tưởng chức năng thành một sản phẩm vật lý bằng silicon. Hành trình này đi từ mức mô tả hành vi tổng quát đến các cấu trúc hình học chi tiết có thể sản xuất tại nhà máy bán dẫn (Foundry).

### 1.1 Các Cấp Độ Trừu Tượng Trong Thiết Kế Vi Mạch

Thiết kế vi mạch số bao gồm **5 cấp độ biểu diễn/trừu tượng cơ bản** theo thứ tự từ cao xuống thấp. Càng đi xuống sâu, mức độ trừu tượng càng giảm, trong khi các yêu cầu và chi tiết vật lý (điện áp, năng lượng, điện trở, điện dung ký sinh) càng tăng:

1. **Cấp độ Hành vi (Behavioral Level):** Định nghĩa chức năng, ý tưởng và thuật toán hoạt động của khối mạch ở mức cao nhất mà kỹ sư có thể dễ dàng hiểu được.
2. **Cấp độ Chuyển giao Thanh ghi (RTL - Register Transfer Level):** Sử dụng các ngôn ngữ mô tả phần cứng (HDL) như Verilog/SystemVerilog để mô tả chính xác luồng dữ liệu giữa các thanh ghi và các mạch chức năng số.
3. **Cấp độ Cổng Logic (Gate-Level Netlist):** Kết quả sau khi tổng hợp logic (Synthesis). Mạch lúc này không còn ở dạng ngôn ngữ mô tả trừu tượng mà chuyển thành sơ đồ nguyên lý gồm các cổng logic cơ bản (AND, NAND, OR, NOR, Inverter, Flip-Flop) và các mối liên kết (Nets).
4. **Cấp độ Sơ đồ Bố trí Hình học (Geometric Layout / GDSII):** Bố trí không gian thực tế của các tế bào chuẩn (Standard Cells) và hệ thống dây dẫn kim loại trên mặt phẳng chip.
5. **Cấp độ Vật lý Silicon / Bóng bán dẫn (Physical/Silicon Level):** Cấu trúc vật lý thấp nhất gồm các bóng bán dẫn (NMOS, PMOS), các vùng khuếch tán, và các kết nối điện thực tế.

> **Lưu ý cốt lõi:** Dù biểu diễn ở bất kỳ cấp độ nào, hành vi/chức năng logic của mạch phải luôn được bảo toàn (ví dụ: một bộ cộng ở mức RTL sau khi xuống cấp độ Layout vẫn phải hoạt động đúng là một bộ cộng).

```
   [ Ý tưởng / Chức năng ]
             │
             ▼
      [ Mô tả RTL ]           ────────► Front-End Flow
             │                          (Mức trừu tượng cao)
             ▼
   [ Synthesis / Netlist ]    ──┐
             │                  │
             ▼                  │
    [ Layout / Floorplan ]      ├──────► Back-End Flow
             │                  │        (Physical Design - Mức trừu tượng thấp)
             ▼                  │
  [ Signoff GDSII / Silicon ] ──┘
```

### 1.2 Sơ Đồ Phân Vùng Front-End Và Back-End

Quy trình thiết kế chip toàn diện được chia làm hai giai đoạn lớn:

* **Front-End (Tiền thiết kế):** Bao gồm việc viết mã mô tả phần cứng RTL, kiểm thử chức năng (Design Verification - DV), và mô phỏng chạy thử nghiệm trên máy tính để đảm bảo thuật toán đúng.
* **Back-End (Physical Design - Thiết kế Vật lý):** Bắt đầu từ quá trình Tổng hợp Logic (Synthesis) biến đổi RTL thành Gate Netlist, kéo dài qua các bước Floorplan, Placement, CTS, Routing và kết thúc khi hoàn tất kiểm tra Signoff để tạo file GDSII chuẩn bị đúc chip.

> **Tính chất hồi tiếp (Feedback Loop):** Quy trình thiết kế vật lý không phải là một đường thẳng một chiều khép kín. Nếu phát hiện vi phạm ở các bước sau (như nghẽn dây, vi phạm thời gian, vi phạm DRC), hệ thống bắt buộc phải hồi tiếp quay ngược lại các bước trước (điều chỉnh Floorplan, nới lỏng Ràng buộc Constraints, hoặc sửa lại mã RTL ban đầu).

---

## 2. SO SÁNH CHI TIẾT BIẾN THỂ THIẾT KẾ: ASIC VS. FPGA

Mặc dù cùng sử dụng chung ngôn ngữ mô tả phần cứng RTL để định nghĩa chức năng, việc triển khai trên cấu trúc ASIC (*Application-Specific Integrated Circuit*) và FPGA (*Field-Programmable Gate Array*) hoàn toàn khác biệt về mặt bản chất vật lý:

| Tiêu chí | FPGA | ASIC |
| :--- | :--- | :--- |
| **Bản chất tài nguyên** | Có sẵn tài nguyên cố định (FPGA Fabric, LUTs, DSP slices, khối BRAM tích hợp sẵn). | Ban đầu là khung đất trống hoàn toàn. Xây dựng từ móng bằng các Standard Cells, Macro và bộ luật (PDK Rules). |
| **Cơ chế hoạt động** | Nạp file Bitstream vào bộ nhớ tĩnh (SRAM) để cấu hình đóng/ngắt các công tắc kết nối các khối sẵn có. | Khái niệm vật lý cố định, sắp đặt và quang khắc đúc trực tiếp các lớp bóng bán dẫn và dây kim loại. |
| **Độ linh hoạt & Cấu hình** | Có thể tái cấu hình vô số lần bằng cách nạp lại file Bitstream mới trong vài giây. | Cố định vĩnh viễn sau khi sản xuất, không thể thay đổi bất kỳ cổng logic hay đường dây kim loại nào. |
| **Cây Xung nhịp (Clock & Reset)** | Đi kèm mạng lưới Clock chuyên dụng tích hợp sẵn (Dedicated Clock Trees, PLLs/MMCM, bộ chia xung). | Phải tự xây dựng, phân bổ, chèn đệm và tối ưu hóa Cây Xung nhịp (CTS) từ đầu cho mỗi thiết kế. |
| **Yếu tố ảnh hưởng Timing** | Phụ thuộc vào ma trận kết nối và kiến trúc Fabric cố định của hãng FPGA (Xilinx/Intel). | Phụ thuộc trực tiếp vào điện trở ký sinh ($R$), điện dung ký sinh ($C$) trên đường dây và các góc công nghệ (Corners: SS, TT, FF) của PDK. |
| **Khả năng sửa lỗi (Debugging/Fixes)** | Cực kỳ linh hoạt: Phát hiện lỗi chỉ cần sửa code, tổng hợp và nạp lại ngay lập tức. | **Trên Silicon không có Ctrl+Z.** Mỗi lần sửa lỗi (Respin) tốn hàng trăm nghìn đến hàng triệu USD và mất từ **3 đến 6 tháng** để xưởng đúc làm lại mặt nạ quang khắc. |

---

## 3. CÁC KHÁI NIỆM NỀN TẢNG TRONG PHYSICAL DESIGN

### 3.1 Process Design Kit (PDK) và Thư Viện Thiết Kế

**PDK (Process Design Kit)** là tập hợp các tệp dữ liệu do nhà máy sản xuất chip (Foundry) cung cấp, đóng vai trò là giao ước quy chuẩn vật lý bắt buộc kỹ sư phải tuân theo:

* **Tập luật hình học (Geometry Rules):** Quy định kích thước tối thiểu, khoảng cách an toàn giữa các lớp kim loại và bóng bán dẫn.
* **Mô hình vật lý:** Chứa các thông số đo đạc thực tế về nhiệt độ, điện áp, các lớp vật liệu. Ví dụ: Tiến trình PDK 130nm cung cấp 5 lớp kim loại (Metal Layers), trong khi tiến trình 65nm cung cấp 7 lớp kim loại.
* **Thư viện Tế bào chuẩn (Standard Cell Library):** Chứa thông tin mô hình hóa thời gian (Timing), công suất tiêu thụ (Power), và kích thước hình học của từng tế bào logic.
* **Tính chất độc quyền:** Mỗi tiến trình nhà máy có một PDK riêng biệt. Cùng một đoạn mã RTL nhưng khi tổng hợp trên hai PDK khác nhau sẽ sinh ra hai Netlist và kết quả vật lý hoàn toàn khác nhau. Nếu không có PDK từ nhà đúc chip, quy trình Physical Design không thể thực hiện được.

### 3.2 Tế Bào Chuẩn (Standard Cells) Và Các Tế Bào Chức Năng Đặc Biệt

Thư viện Standard Cells chứa các khối logic cơ bản được thiết kế sẵn theo chuẩn chiều cao đồng nhất:

* **Các cổng Logic cơ bản:** AND, NAND, OR, NOR, NOT (Inverter), D-Flip-Flop.
  * *Ưu tiên cổng đảo (NAND/NOR/NOT):* Trong thiết kế vi mạch, các cổng đảo cực kỳ được ưa chuộng do cấu trúc vật lý CMOS của cổng đảo (như NAND/NOR) dùng ít transistor hơn và tốc độ chuyển mạch nhanh hơn cổng không đảo (AND = NAND + NOT).
* **Tế bào không chứa Logic:**
  * **Buffer (Bộ đệm):** Dùng để khuếch đại tín hiệu trên các đường dây dài nhằm chống suy hao và làm chậm tín hiệu để sửa lỗi vi phạm thời gian giữ (Hold Violation).
  * **Cap Cells (End-cap Cells):** Đặt tại biên các hàng ở rìa vùng Core để chặn và bảo vệ cấu trúc tế bào logic không bị tổn hại quang khắc ở biên.
  * **Filler Cells:** Tế bào chèn lấp đầy các khoảng trống giữa các Standard Cells nhằm đảm bảo tính liên tục của các lớp khuếch tán bán dẫn (N-well, P-well).

> **Ký hiệu thư viện chuẩn SkyWater 130nm:** `sky130_fd_sc_hd`
> * `sky130`: Tiến trình công nghệ SkyWater 130nm/150nm.
> * `fd`: Foundry Direct.
> * `sc`: Standard Cell (Tế bào chuẩn).
> * `hd`: High Density (Mật độ cao).

### 3.3 Ràng Buộc Thiết Kế (Design Constraints)

Ràng buộc là hệ thống các điều kiện biên bắt buộc trình thiết kế vật lý phải tuân thủ, chia làm hai loại chính:

1. **Ràng buộc Thời gian (Timing Constraints - file SDC):**
   * Định nghĩa Tần số/Chu kỳ Xung nhịp (Clock Period). Xung nhịp đóng vai trò như tín hiệu điều phối nhịp đập toàn bộ hệ thống.
   * Yêu cầu kiểm tra phân tích thời gian tĩnh (STA) để đảm bảo tín hiệu lan truyền kịp thời trước khi mép xung nhịp kế tiếp xuất hiện.
2. **Ràng buộc Không gian (Spatial/Area Constraints):**
   * **Die Area (Diện tích Die):** Tổng diện tích toàn bộ con chip, bao gồm vùng chứa logic và vùng đặt các chân giao tiếp đầu vào/đầu ra (IO Pins/Pads).
   * **Core Area (Diện tích Core):** Vùng diện tích bên trong chip chuyên dụng để đặt các Standard Cells, Buffers và Macro logic.

> **Sự cân bằng Ràng buộc (Constraint Balancing):** Nếu xiết ràng buộc quá chặt (ép tần số quá cao, diện tích quá nhỏ), công đoạn thiết kế vật lý sẽ bị nghẽn mạch, vi phạm thời gian và không thể đi dây. Ngược lại, nếu thả ràng buộc quá lỏng, con chip sẽ hoạt động chậm và lãng phí diện tích silicon.

---

## 4. CHI TIẾT CÁC BƯỚC THỰC THI PHYSICAL DESIGN (IMPLEMENTATION)

```
[ Gate Netlist & Constraints ]
              │
              ▼
       1. Logic Synthesis
              │
              ▼
       2. Floorplanning & PDN
              │
              ▼
       3. Placement (Global & Detail)
              │
              ▼
       4. Clock Tree Synthesis (CTS)
              │
              ▼
       5. Routing (Global & Detail)
              │
              ▼
       6. Cell Insertion (Filler & Cap)
              │
              ▼
      [ Unchecked GDSII Layout ]
```

### 4.1 Logic Synthesis (Tổng Hợp Logic)
* **Khái niệm:** Bước chuyển đổi mã nguồn RTL trừu tượng thành Gate-Level Netlist cụ thể dựa trên thư viện Standard Cells.
* **Công cụ:** Yosys (mã nguồn mở trong luồng LibreLane) hoặc Design Compiler / Genus (thương mại).
* **Nhiệm vụ:**
  * Phân tích cú pháp RTL, kiểm tra tính tổng hợp được của mã code.
  * Ánh xạ các toán tử logic (bộ cộng, bộ chọn Mux, Flip-Flop) sang các tế bào tương ứng trong PDK.
  * Ước lượng độ trễ và diện tích ban đầu.

### 4.2 Floorplanning & Power Distribution Network (PDN)
Floorplan là bước quy hoạch không gian vật lý đầu tiên cho con chip, đòi hỏi nhiều kinh nghiệm thiết kế nhất:
* **Quy hoạch khung hình học:** Xác định kích thước Core, Die, tỷ lệ khung hình (*Aspect Ratio* - ví dụ: Ratio = 1 tạo hình vuông, Ratio = 1:2 tạo hình chữ nhật để nới rộng mật độ).
* **Đặt chân IO (IO Placement):** Phân bổ các chân cắm tín hiệu đầu vào/đầu ra xung quanh mép Die.
* **Xây dựng mạng phân phối nguồn (PDN):** Đan các lưới dây điện áp cao ($V_{DD}$) và dây nối đất ($V_{SS}$) chạy dọc và ngang khắp chip dưới dạng các vòng nguồn (Power Rings) và sọc nguồn (Power Stripes) để cấp năng lượng cho toàn bộ tế bào.

### 4.3 Placement (Đặt Tế Bào Logic)
Quá trình sắp xếp các tế bào chuẩn vào các hàng (Rows) đã định nghĩa trong vùng Core, chia làm 2 giai đoạn:
* **Global Placement (Đặt tế bào tổng thể):** Sắp xếp các tế bào vào các vị trí tối ưu để giảm thiểu tổng độ dài dây nối. Trong giai đoạn này, các tế bào **được phép đè lên nhau (Overlap)** nhằm tìm ra vị trí tối ưu về mặt lý thuyết.
* **Detail Placement (Đặt tế bào chi tiết):** Loại bỏ hoàn toàn sự đè chồng. Ép tất cả các tế bào gắn chặt và khớp chính xác vào từng hàng tế bào chuẩn (Standard Cell Rows), tuân thủ khoảng cách an toàn.

### 4.4 Clock Tree Synthesis (CTS - Tổng Hợp Cây Xung Nhịp)
* **Vấn đề:** Tín hiệu xung nhịp (Clock) phải phân phối tới hàng triệu Flip-Flop cùng lúc. Tải dung lớn sẽ làm suy hao và lệch xung (*Clock Skew*).
* **Giải pháp:** Bước CTS tiến hành xây dựng một mạng lưới phân nhánh cây xung nhịp cân bằng, tự động chèn thêm các bộ đệm xung nhịp (*Clock Buffers*) chuyên dụng trên đường đi để khuếch đại tín hiệu, đảm bảo thời điểm xung nhịp tới tất cả các phần tử lưu trữ là đồng đều nhất.

### 4.5 Routing (Đi Dây Kết Nối)
Quá trình tạo ra các đường dây kim loại vật lý nối các chân tín hiệu của các tế bào lại với nhau:
* **Global Routing (Đi dây tổng thể):** Phân chia mặt phẳng chip thành các lưới nhỏ, vạch ra lộ trình đường đi sơ bộ cho các nhóm dây tín hiệu.
* **Detail Routing (Đi dây chi tiết):** Thực thi đi dây chính xác trên từng lớp kim loại (Metal Layers). Bước này chịu rủi ro cao về hiện tượng nghẽn dây (*Congestion*) nếu mật độ tế bào quá dày đặc.

### 4.6 Lắp Đầy Tế Bào (Filler & Cap Cells Insertion)
Sau khi hoàn tất đi dây, trên bề mặt Core vẫn còn tồn tại các khoảng trống nhỏ giữa các tế bào:
* Trình thiết kế sẽ chèn các **Filler Cells** vào các khoảng trống này nhằm tạo sự liên tục cho các lớp vi mạch (N-well, P-well) phục vụ quá trình quang khắc.
* Các **Cap Cells** được bổ sung ở biên để ngăn chặn tổn hại biên hình học.

---

## 5. CÁC TIÊU CHUẨN KIỂM TRA SIGNOFF

Signoff là bước kiểm định chất lượng cuối cùng. Một tệp sơ đồ bố trí chip (GDSII) chỉ được phép gửi tới nhà đúc chip (Tape-out) sau khi vượt qua tất cả 5 tiêu chuẩn Signoff dưới đây:

```
                  ┌──► 1. DRC Check  (Đúng luật hình học?)
                  ├──► 2. LVS Check  (Khớp sơ đồ nguyên lý?)
[ Final Layout ] ─┼──► 3. STA Check  (Đạt tốc độ thời gian?)
                  ├──► 4. Antenna    (Không hỏng cổng cách điện?)
                  └──► 5. LEC Check  (Đúng chức năng logic?)
```

### 5.1 DRC (Design Rule Check - Kiểm Tra Luật Thiết Kế Hình Học)
* **Mục đích:** Đảm bảo bản vẽ Layout tuân thủ tuyệt đối các quy tắc sản xuất của nhà máy trong PDK.
* **Nội dung kiểm tra:** Khoảng cách tối thiểu giữa 2 đường dây kim loại, độ rộng tối thiểu của vệt kim loại, khoảng cách giữa các tế bào.
* **Công cụ:** Magic, KLayout.

### 5.2 LVS (Layout Versus Schematic - Kiểm Tra Sự Tương Đương Sơ Đồ)
* **Mục đích:** Đảm bảo sơ đồ vật lý sau khi đi dây (Layout Netlist) khớp hoàn toàn với sơ đồ nguyên lý sau tổng hợp (Verilog Gate Netlist).
* **Nội dung kiểm tra:** Phát hiện các sự cố hở mạch, ngắn mạch (nối lầm dây tín hiệu vào dây nguồn/đất), hoặc mất linh kiện trong quá trình đặt dây.
* **Công cụ:** Netgen.

### 5.3 STA (Static Timing Analysis - Phân Tích Thời Gian Tĩnh)
* **Mục đích:** Đảm bảo mạch chạy đúng ở tốc độ/tần số thiết kế trong điều kiện thực tế.
* **Cơ chế:** Trích xuất ma trận điện trở và điện dung ký sinh trên đường dây dẫn (Parasitic R-C) lưu vào các tệp chuẩn SPEF. Công cụ STA đọc các thông số ký sinh này để tính toán độ trễ đường truyền thực tế, đánh giá vi phạm thời gian thiết lập (Setup Time) và thời gian giữ (Hold Time).
* **Công cụ:** OpenSTA.

### 5.4 Antenna Effect Check & Mitigation (Kiểm Tra Hiệu Ứng Anten)
* **Mục đích:** Ngăn ngừa sự phá hủy vật lý đối với bóng bán dẫn trong quá trình chế tạo.
* **Cơ chế rủi ro:** Trong quá trình ăn mòn kim loại bằng plasma tại nhà đúc, các đoạn dây kim loại quá dài chưa nối xuống cực N/P sẽ hoạt động như những cột thu lôi tụ điện tích tĩnh. Lượng điện tích này tích tụ lớn có thể phóng qua gây đánh thủng lớp oxit cách điện mỏng tại cực Cổng (Gate Oxide) của các tế bào logic.
* **Khắc phục:** Chèn thêm các bộ đệm (Buffers) hoặc Diode xả tĩnh điện (*Antenna Diodes*) trên các đường dây dài để chuyển hướng dòng điện tích xả an toàn xuống nền chip.

### 5.5 Logic Equivalence Check (LEC / Formal Verification)
Kiểm tra tính tương đương chức năng logic ở cấp độ thấp nhất giữa bản mô tả RTL ban đầu và Netlist/Layout cuối cùng. Bước này xác nhận rằng quá trình đi dây và tổng hợp không làm biến đổi thuật toán logic gốc của thiết kế.

---

## 6. THỰC HÀNH VỚI CÔNG CỤ MÃ NGUỒN MỞ: LIBRELANE & TINY TAPEOUT

Nhằm phổ cập khả năng tự tay hiện thực hóa vi mạch số mà không phụ thuộc vào chi phí bản quyền đắt đỏ của các phần mềm thương mại, hệ sinh thái mã nguồn mở cung cấp luồng công cụ hoàn chỉnh từ RTL đến sản phẩm silicon đúc thực tế.

### 6.1 Luồng Thực Thi Tự Động LibreLane
LibreLane (dựa trên luồng OpenLane) tích hợp một chuỗi các công cụ mã nguồn mở độc lập thành một quy trình chạy tự động từng bước:
* **Tích hợp công cụ:**
  * Tổng hợp logic: **Yosys**
  * Đặt tế bào & Đi dây: **OpenROAD**
  * Kiểm tra DRC & Xem Layout: **Magic, KLayout**
  * Kiểm tra LVS: **Netgen**
  * Phân tích thời gian tĩnh: **OpenSTA**
* **Cơ chế quản lý:** Luồng chạy được thiết lập thông qua các tệp kịch bản TCL cấu hình tham số. Người dùng có thể điều khiển qua giao diện dòng lệnh (Command Line) hoặc giao diện đồ họa (CTW SEMI Web GUI).
* **Báo cáo và Phân tích:** Hệ thống tự động trích xuất kết quả trực quan bao gồm: Mật độ tế bào sử dụng, thống kê số lượng tế bào, diện tích tiêu tốn, báo cáo vi phạm thời gian Setup/Hold và nhật ký DRC.

```
[ Code RTL (.v) ] ──► [ Yosys ] ──► [ OpenROAD ] ──► [ Magic / KLayout ] ──► [ GDSII File ]
                          │               │                  │
                          ▼               ▼                  ▼
                   (Gate Netlist)  (Placement/CTS)     (DRC/LVS Signoff)
```

### 6.2 Khung Hình Học Và Mô Hình Băng Nhóm Tiny Tapeout (MPW)
Tiny Tapeout là giải pháp giúp giảm thiểu tối đa chi phí đúc chip học thuật bằng mô hình **Gom đúc nhiều dự án trên một tấm Bán dẫn (Multi-Project Wafer - MPW)**:
* **Đơn vị Tile:** Chia không gian trên đai chip thành các ô vuông đơn vị gọi là các Tiles.
* **Cơ chế Mua diện tích:** Người dùng chỉ cần chi trả chi phí cho đúng số lượng ô Tile mà thiết kế của mình chiếm dụng (1 Tile, 2 Tiles hoặc 4 Tiles) thay vì mua toàn bộ tấm bán dẫn (Wafer) đắt đỏ.
* **Chia sẻ chân Giao tiếp (Shared IO MUX):** Tất cả các dự án trên cùng một Die chip sẽ chia sẻ chung hệ thống chân IO, xung nhịp Clock, và tín hiệu Reset thông qua các bộ dồn kênh Muxes.

### 6.3 Quy Trình Kiểm Thử Và Tape-Out Thực Tế
Để gửi một dự án hoàn chỉnh lên hệ thống Tiny Tapeout, người dùng thực hiện qua các bước quy chuẩn:
1. **Tuân thủ tệp Mẫu (Template Standard):**
   * Tệp thiết kế Top-level bắt buộc đặt tên: `project.v`
   * Tệp kịch bản kiểm thử: `test.py`
   * Tệp mô tả thông tin cấu hình: `info.yaml`
2. **Kiểm tra tự động trên GitHub Action:** Khi đẩy mã nguồn lên kho lưu trữ, hệ thống server sẽ tự động chạy luồng LibreLane để kiểm định tính hợp lệ của file.
3. **Phân tích cục bộ bằng Docker:** Người dùng tải ứng dụng đóng gói dưới dạng Docker (như CTW SEMI) về máy tính cá nhân để tự thực thi, xem bản vẽ Layout GDSII và tinh chỉnh các lỗi DRC/Timing trước khi chốt nộp.
4. **Nhận chip và Kiểm thử phần cứng (Post-Fabrication Testing):**
   * Thời gian chờ đóng gói và đúc chip kéo dài từ 3 đến 6 tháng.
   * Khi hoàn tất, chip thực tế được gắn sẵn trên một mạch in thử nghiệm (PCB Demo Board). Người dùng cắm bo mạch thử nghiệm để đo đạc tín hiệu điện tử vật lý thực tế từ các chân kim loại, đối chiếu với kết quả mô phỏng ban đầu.
