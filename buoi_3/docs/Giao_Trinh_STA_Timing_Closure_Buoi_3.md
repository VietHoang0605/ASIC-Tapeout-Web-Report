# GIÁO TRÌNH CHUYÊN SÂU & BÁO CÁO KỸ THUẬT: BUỔI 3
# CHỦ ĐỀ: STATIC TIMING ANALYSIS (STA) — TỪ RÀNG BUỘC THỜI GIAN ĐẾN TIMING CLOSURE

> **Dự án:** Khóa đào tạo Thiết kế Vi mạch chuyên nghiệp: RTL-to-GDSII hướng tới Tape-out  
> **Nền tảng EDA:** LibreLane / OpenLane / CTW SEMI — Tiến trình SkyWater 130nm High-Density (`sky130_fd_sc_hd`)  
> **Lưu trữ tài liệu:** `D:\Tapeout_chip\buoi_3\docs\Giao_Trinh_STA_Timing_Closure_Buoi_3.md`  
> **Phương châm Tape-out:** *"Trên Silicon không có nút Ctrl+Z — Lỗi Setup làm chip chạy chậm, nhưng lỗi Hold sẽ biến con chip thành cục gạch vĩnh viễn."*

---

## 🗺️ TỔNG QUAN HÀNH TRÌNH BUỔI 3 (MASTER ROADMAP ARCHITECTURE)

> [!NOTE]
> **HƯỚNG DẪN XEM CHI TIẾT SƠ ĐỒ KHỐI TỔNG QUAN:**  
> Sơ đồ khối kiến trúc dưới đây tổng hợp trọn vẹn toàn bộ hành trình buổi 3 thành một khung nhìn tích hợp 2D (không cuộn dọc), kết nối chặt chẽ giữa: **1. Nền tảng vật lý** ➔ **2. Ràng buộc SDC & Bộ nhân** ➔ **3. Trung tâm STA & Ép xung 13ns (Góc tử thần max_ss)** ➔ **4. Hai con đường tối ưu (Tool DSE vs RTL Pipelining)** ➔ **5. Bàn giao Tape-out GDSII**.  
> 💡 **Cách xem chi tiết:** Hãy **nhấp trực tiếp vào hình** để mở trình chiếu toàn màn hình (Lightbox). Bạn có thể **lăn chuột để phóng to / thu nhỏ** từ $0.4\times$ đến $6.0\times$ và **kéo rê chuột để soi chi tiết** từng cổng tín hiệu, cờ báo vi phạm và giá trị Slack!

![Sơ đồ khối tổng quan hành trình Buổi 3: Lộ trình STA & Timing Closure Kiến trúc Khép Kín](images/b3_master_roadmap_architecture.svg)

---

## 💎 PHẦN I: TÂM HUYẾT NGHỀ NGHIỆP & KINH NGHIỆM THỰC CHIẾN TỪ GIẢNG VIÊN

### 1. Vị Thế & Cơ Hội Nghề Nghiệp Của Kỹ Sư STA (STA / Signoff Engineer)
* **Tính chuyên môn hóa cực cao:** Trong các tập đoàn bán dẫn hàng đầu (Marvell, Synopsys, Cadence, Qualcomm, MediaTek...), phân tích thời gian tĩnh (Static Timing Analysis - STA) không phải là một công việc phụ trợ mà là một chuyên ngành độc lập. Có những kỹ sư dành toàn bộ $100\%$ sự nghiệp chỉ để làm **Timing Closure** và **Signoff Verification** — bước quyết định ký duyệt cuối cùng trước khi gửi file GDSII sang các xưởng đúc wafer (Foundry) như TSMC, Samsung, GlobalFoundries.
* **Độ hiếm và chi phí đào tạo:** Kiến thức thực chiến về STA và Physical Design (PD) rất hiếm khi được chia sẻ công khai hay miễn phí. Các khóa đào tạo chuyên sâu về STA trên các công cụ chuẩn công nghiệp thường có chi phí lên tới hàng chục đến hàng trăm triệu đồng tại các trung tâm quốc tế.
* **Cơ hội bước vào dự án Tapeout thật:** Thái độ học tập chỉn chu, hoàn thành các bài Lab, chủ động mổ xẻ file log và lập báo cáo kỹ thuật chuẩn mực là "tấm vé vàng" để được các chuyên gia và giảng viên tuyển chọn tham gia trực tiếp vào các dự án thương mại hóa chip và các đợt Shuttle Tape-out thực tế.

---

### 2. Triết Lý Học & Phương Pháp Tích Lũy Kinh Nghiệm PD
* **Lý thuyết ít, thực hành là sống còn:** Các công thức toán học của STA ($T_{\text{clk}} \ge T_{\text{co}} + T_{\text{comb}} + T_{\text{su}}$) thực ra rất ngắn gọn và đơn giản. Nhưng cái phân biệt giữa một "kỹ sư lý thuyết" và một "Senior Tape-out Architect" nằm ở **kinh nghiệm cảm nhận phần cứng (Silicon Intuition)**:
  * Phải tự tay gõ lệnh, chỉnh sửa file ràng buộc `.sdc`.
  * Phải tự tay chạy các chiến lược tổng hợp (Synthesis Strategies) và phân bổ mặt bằng (Floorplanning).
  * Phải đọc từng dòng log cảnh báo, tra cứu bảng `summary.rpt` tại từng góc bán dẫn (Corners) để hiểu cặn kẽ tại sao công cụ lại chọn tế bào này thay vì tế bào khác.

---

### 3. Bài Học "Xương Máu" Cốt Tử: Phân Biệt Lỗi Setup vs Lỗi Hold Khi Tapeout

Đây là bài học nền tảng định hình tư duy của mọi kỹ sư thiết kế phần cứng:

| Tiêu Chí So Sánh | Vi Phạm Thời Gian Setup (Setup Violation) | Vi Phạm Thời Gian Giữ (Hold Violation) |
| :--- | :--- | :--- |
| **Bản chất vật lý** | **Dữ liệu đến QUÁ CHẬM** (Tín hiệu bò qua mạch tổ hợp quá lâu, không kịp ổn định trước nhịp chốt kế tiếp). | **Dữ liệu mới tràn đến QUÁ NHANH** (Dữ liệu mới phóng qua mạch tổ hợp đè hỏng dữ liệu cũ khi FF chưa kịp chốt xong). |
| **Tính chất chu kỳ** | Xảy ra giữa **2 chu kỳ Clock khác nhau** (từ Launch Edge $N$ đến Latch Edge $N+1$). | Xảy ra ngay trong **CÙNG MỘT chu kỳ Clock** (tại Latch Edge $N$). |
| **Hậu quả khi chip về** | **CỨU ĐƯỢC:** Nếu chip xuất xưởng bị vi phạm Setup ở $100\,\text{MHz}$, ta có thể hạ tần số xung nhịp xuống $50\,\text{MHz}$ hoặc $10\,\text{MHz}$. Cửa sổ chu kỳ dãn ra, dữ liệu kịp đến đích, **con chip vẫn sống và hoạt động hoàn hảo** (chỉ là chạy chậm hơn dự kiến). | **CHẾT VĨNH VIỄN ("CỤC GẠCH"):** Vì lỗi Hold xảy ra trong cùng một chu kỳ và hoàn toàn độc lập với chu kỳ clock $T_{\text{clk}}$, **dù có hạ tần số xuống $1\,\text{Hz}$ hay $0.1\,\text{Hz}$ thì dữ liệu mới vẫn tràn sang đè nát dữ liệu cũ**. Con chip hoàn toàn mất chức năng, không thể cứu chữa! |
| **Quy tắc ưu tiên Tapeout** | **Ưu tiên số 2:** Tối ưu hiệu năng sau khi đã an toàn về mạch. | **ƯU TIÊN SỐ 1 TUYỆT ĐỐI:** Phải quét sạch $100\%$ lỗi Hold trước khi đóng gói gửi sang nhà máy đúc wafer! |

---

### 4. CHUYÊN LUẬN ĐẶC BIỆT: BẢN CHẤT VẬT LÝ, MÔ HÌNH TOÁN HỌC VÀ CƠ CHẾ ĐÓNG TIMING CỦA THỜI GIAN THIẾT LẬP ($T_{\text{setup}}$)

> **Định đề cốt tử:** *Thời gian thiết lập là một ràng buộc vật lý nội tại của linh kiện bán dẫn, hoàn toàn độc lập với dữ liệu, xác định giới hạn tốc độ trần của mọi con chip số.*

#### A. Bản Chất Vật Lý Nội Tại Của $T_{\text{setup}}$: Hằng Số Bất Biến Của Tế Bào Chuẩn

Trong thiết kế vi mạch, **Thời gian thiết lập ($T_{\text{setup}}$)** không phải là một thông số co dãn theo chu kỳ hay tần số xung nhịp. Nó là **đặc tính vật lý nội tại (Intrinsic Cell Property)** của phần tử nhớ tuần tự (D-Flip-Flop):

* **Cơ chế nạp điện tích:** Để một phần tử nhớ chốt chính xác trạng thái logic mới, điện áp tại chân `D` cần truyền qua cổng truyền dẫn nội bộ (*Transmission Gate TG1*) và nạp đủ điện tích lên tụ điện ký sinh của các cực cổng transistor CMOS (*Gate Capacitance $C_{\text{gate}}$*) thuộc tầng Master Latch trước khi sườn clock cắt dòng dẫn.
* **Tính bất biến với tần số:** Lượng thời gian vật lý này phụ thuộc trực tiếp vào hằng số thời gian $\tau = R_{\text{on}} \times C_{\text{gate}}$, thường dao động trong khoảng từ $0.15\,\text{ns} - 0.20\,\text{ns}$ (đối với thư viện SkyWater 130nm `sky130_fd_sc_hd`).
* **Minh chứng từ thư viện Liberty (`.lib`):** Trong bảng tra cứu thời gian (LUT) do xưởng đúc cung cấp, $T_{\text{setup}}$ chỉ phụ thuộc vào độ dốc sườn tín hiệu (*Data Transition*) và độ dốc sườn clock (*Clock Transition*). Bảng tra cứu này **hoàn toàn không chứa biến số chu kỳ xung nhịp $T_{\text{clk}}$**. Dù chip vận hành ở $1\,\text{GHz}$, $100\,\text{MHz}$ hay kích tay ở $1\,\text{Hz}$, con Flip-Flop vẫn chỉ đòi hỏi đúng lượng thời gian $T_{\text{setup}}$ cố định này.

![Cấu trúc vật lý nội bộ Flip-Flop và cơ chế nạp điện cực cổng](file:///D:/Tapeout_chip/buoi_3/docs/cau_truc_flip_flop_setup_time.svg)

---

#### B. Hệ Quy Chiếu Thời Gian Và Quy Tắc Chu Kỳ Toàn Phần

Để hiểu chính xác thời điểm dữ liệu được chốt, cần xác định rõ hệ quy chiếu thời gian và phạm vi lan truyền:

1. **Gốc tọa độ của Setup là Sườn Clock đón (Latch Edge):**
   * Cửa sổ thời gian setup **không neo vào thời điểm dữ liệu chuyển mức**, mà được **tính ngược từ sườn Clock đón kế tiếp**:
     $$\text{Thời điểm bắt đầu vùng cấm} = T_{\text{Latch\_Edge}} - T_{\text{setup}}$$
   * Dữ liệu bắt buộc phải đến đích và hoàn tất việc đổi mức điện áp **TRƯỚC** thời điểm này. Một khi đã hoàn tất chuyển trạng thái, dữ liệu sẽ duy trì ổn định tại mức điện áp đó để chờ sườn clock tới chốt.
2. **Dữ liệu chuyển động trong Chu kỳ toàn phần ($100\%$ $T_{\text{clk}}$):**
   * Trong mạch số đồng bộ kích hoạt theo sườn dương (*Positive Edge-Triggered*), Flip-Flop phát phóng dữ liệu tại sườn dương thứ nhất ($t = 0$) và Flip-Flop thu bắt dữ liệu tại **sườn dương kế tiếp** ($t = T_{\text{clk}}$).
   * Khoảng cách giữa hai sườn này là **một chu kỳ hoàn chỉnh**, không phải nửa chu kỳ ($T_{\text{clk}}/2$). Tín hiệu có trọn vẹn cả chu kỳ $T_{\text{clk}}$ để vượt qua mạng cổng logic tổ hợp.

---

#### C. Cơ Chế Cứu Sống Chip Bằng Cách Hạ Tần Số Xung Nhịp (Dãn Chu Kỳ Clock)

Vi phạm Setup xảy ra khi thời gian lan truyền thực tế qua mạch logic ($T_{\text{data}}$) vượt quá ngân sách chu kỳ cho phép. Tuy nhiên, vì ngân sách chu kỳ là đại lượng điều khiển được từ bên ngoài, vi phạm Setup luôn có thể khắc phục được sau khi sản xuất:

$$\text{Data Required Time} = T_{\text{clk}} - T_{\text{setup}}$$
$$\text{Data Arrival Time} = T_{\text{cq}} + T_{\text{data}}$$
$$\text{Setup Slack} = \text{Data Required Time} - \text{Data Arrival Time}$$

##### Ma trận đối chiếu định lượng (Độ trễ logic $T_{\text{data}} = 12.0\,\text{ns}$, $T_{\text{setup}} = 0.2\,\text{ns}$):

| Thông Số Thời Gian | Vận Hành $100\,\text{MHz}$ ($T_{\text{clk}} = 10\,\text{ns}$) | Vận Hành $50\,\text{MHz}$ ($T_{\text{clk}} = 20\,\text{ns}$) |
| :--- | :--- | :--- |
| **Sườn phát (Launch Edge)** | $0.0\,\text{ns}$ | $0.0\,\text{ns}$ |
| **Thời điểm dữ liệu tới đích** | $12.0\,\text{ns}$ (Đổi trạng thái xong) | $12.0\,\text{ns}$ (Đổi trạng thái xong) |
| **Sườn đón (Latch Edge)** | $10.0\,\text{ns}$ | **$20.0\,\text{ns}$ (Được dời lùi $+10\,\text{ns}$)** |
| **Hạn chót ổn định (Required)** | $10.0 - 0.2 = \mathbf{9.8\,\text{ns}}$ | $20.0 - 0.2 = \mathbf{19.8\,\text{ns}}$ |
| **Setup Slack** | $9.8 - 12.0 = \mathbf{-2.2\,\text{ns}}$ ❌ | $19.8 - 12.0 = \mathbf{+7.8\,\text{ns}}$ ✅ |
| **Trạng thái thực tế** | Clock đập búa khi dữ liệu chưa kịp tới. | Dữ liệu tới lúc $12\,\text{ns}$, **đứng im ổn định $7.8\,\text{ns}$** chờ sườn clock. |
| **Kết luận vận hành** | **Chip lỗi logic / Không hoạt động.** | **Con chip sống và hoạt động hoàn hảo!** |

![Sơ đồ thời gian đối chiếu 100MHz vs 50MHz](file:///D:/Tapeout_chip/buoi_3/docs/so_do_thoi_gian_setup_100mhz_vs_50mhz.svg)

---

#### D. Bản Chất "Dữ Liệu Ổn Định": Dữ Liệu Mới Hợp Lệ vs Dữ Liệu Cũ & Hiểm Họa Bất Định (Metastability)

Một hiểu lầm thường gặp là cho rằng: *"Nếu tín hiệu đang ở mức logic phẳng (ví dụ mức 0) tại thời điểm $T_{\text{setup}}$, thì nó vẫn thỏa mãn điều kiện ổn định."* Trong vi mạch số, nhận định này không chính xác vì hai lý do nền tảng:

1. **Yêu cầu về "Dữ liệu mới hợp lệ" (New Valid Data):**  
   Mục đích của mạch tuần tự là ghi nhận **kết quả của phép toán vừa được kích hoạt tại sườn Launch ($t = 0$)**. Mức 0 phẳng lì tồn tại trước khi chuyển mạch chỉ là **giá trị rác (Stale Data)** của chu kỳ trước còn vương lại trên đường dây. Nếu Flip-Flop chốt giá trị cũ này, toàn bộ chức năng giải thuật của chip sẽ bị sai lệch hoàn toàn.
2. **Nhiễu chuyển mạch trung gian (Glitches / Hazards):**  
   Trên silicon thực tế, khi các bit truyền qua các tầng logic (như chuỗi truyền carry trong bộ cộng), đường dây không phẳng lì mà dao động liên tục do độ trễ không đồng đều giữa các nhánh. Quá trình dao động này chỉ chấm dứt khi bit trễ nhất hoàn tất chuyển trạng thái ($12\,\text{ns}$).
3. **Hiểm họa Metastability:**  
   Nếu sườn clock xuất hiện trong khi điện áp đang chuyển đổi dở dang, Flip-Flop sẽ bị kẹt ở vùng điện áp lơ lửng giữa 0 và 1. Trạng thái bất định này khiến ngõ ra dao động không kiểm soát, gây sập toàn bộ hệ thống xử lý phía sau.

![Hiện tượng Glitch trên Silicon và Nguy cơ Bất định trạng thái Metastability](file:///D:/Tapeout_chip/buoi_3/docs/hien_tuong_glitch_va_metastability.svg)

---

#### E. Phương Pháp Luận STA: Cơ Chế Bắt Lỗi Độc Lập Với Dữ Liệu (Pattern-Independent Analysis)

Công cụ Static Timing Analysis (như OpenSTA, Synopsys PrimeTime) không sử dụng phương pháp mô phỏng chức năng (Simulation) và **hoàn toàn không cần biết dữ liệu là 0 hay 1**. Nó phát hiện vi phạm Setup dựa trên phân tích hình học và mô hình mạch tương đương:

1. **Mô hình hóa Đồ thị thời gian (Timing Graph / DAG):**  
   Mọi cổng logic và dây dẫn kim loại được trừu tượng hóa thành các nút (Pins) và nhánh liên kết có trọng số thời gian, tính toán từ điện trở và điện dung ký sinh ($RC$).
2. **Tính toán độ trễ đường truyền dài nhất (Critical Path Delay):**  
   Công cụ cộng dồn toàn bộ độ trễ vật lý cực đại từ chân phát đến chân thu:
   $$T_{\text{arrival}} = T_{\text{clk-to-q}} + \sum T_{\text{cell\_delay}} + \sum T_{\text{wire\_delay}} = \mathbf{12.0\,\text{ns}}$$
   Giá trị $12.0\,\text{ns}$ biểu thị: **Bất kỳ sự kiện chuyển trạng thái nào xảy ra trên con đường này đều đòi hỏi tối thiểu $12.0\,\text{ns}$ để hoàn tất.**
3. **Nguyên lý bi quan cực hạn (Worst-Case Pessimism):**  
   STA không quan tâm chu kỳ hiện tại có phát sinh phép tính hay không. Theo nguyên lý kiểm định phần cứng: *Trong hàng tỷ chu kỳ vận hành thực tế, chắc chắn sẽ có lúc dữ liệu buộc phải đổi trạng thái qua con đường này*. Vì độ trễ vật lý ($12.0\,\text{ns}$) vượt quá ngân sách cho phép ($9.8\,\text{ns}$), công cụ khẳng định chắc chắn sẽ xảy ra lỗi sai chức năng và lập tức gắn cờ **Vi phạm Setup**.

![Phương pháp luận STA Timing Graph](file:///D:/Tapeout_chip/buoi_3/docs/phuong_phap_luan_sta_timing_graph.svg)

---

## ⚡ PHẦN II: KHÁI NIỆM NỀN TẢNG & BẢN CHẤT VẬT LÝ CỦA THỜI GIAN (PHYSICAL TIMING)

### 1. Dạng Sóng Lý Tưởng (RTL Simulation) vs Dạng Sóng Vật Lý Thật (Silicon Reality)

Trong tư duy của kỹ sư viết RTL, tín hiệu số được biểu diễn dưới dạng các xung vuông hình học hoàn mỹ:

```
[ Mô Phỏng RTL - Xung Vuông Lý Tưởng ]
1 ┌─────┐     ┌─────┐
  │     │     │     │
0 ┘     └─────┘     └─────
  Chuyển trạng thái tức thời (dt = 0 ps, dòng vô hạn)
```

Nhưng trên tấm bán dẫn Silicon thật:
* Cổng logic được cấu tạo từ các transistor MOSFET có **điện trở kênh dẫn ($R_{\text{on}}$)**.
* Các đường dây kim loại (Metal Layers) có **điện trở ký sinh ($R_{\text{wire}}$)** và **điện dung ký sinh ($C_{\text{wire}}$)** đối với chất nền và các dây lân cận.
* Ngõ vào của các cổng phía sau luôn có **điện dung cực cổng ($C_{\text{gate}}$)**.

$$\implies \text{Quá trình đổi trạng thái thực chất là nạp/xả tụ điện qua điện trở: } \tau = R \times C$$

```
[ Silicon Thật - Sườn Xung Bị Thoái Hóa Do RC ]
       VDD ───────────╭─────────╮
                      │         │
       VSS ───────────╯         ╰─────────
                  ◄───►         ◄───►
                  T_rise        T_fall
```

Tín hiệu chuyển mức không bao giờ là một đường thẳng đứng mà luôn là một **đường cong tích phân/vi phân mượt mà**.

---

### 2. Slew Rate & Thời Gian Chuyển Mạch (Transition Time - $T_{\text{slew}}$)
* **Khái niệm:** Là khoảng thời gian để mức điện áp biến thiên giữa hai ngưỡng logic quy chuẩn (thường đo từ $10\% \rightarrow 90\%$ hoặc $30\% \rightarrow 70\%$ của điện áp nguồn $V_{DD}$).
  * **$T_{\text{rise}}$ (Thời gian sườn lên):** Khoảng thời gian điện áp leo từ mức thấp lên mức cao ($0 \rightarrow 1$).
  * **$T_{\text{fall}}$ (Thời gian sườn xuống):** Khoảng thời gian điện áp tụt từ mức cao xuống mức thấp ($1 \rightarrow 0$).
* **Hậu quả của vi phạm Max Transition (Max Slew Violation):**
  * Nếu sườn xung quá dốc là là ($T_{\text{slew}}$ quá lớn), transistor tầng sau sẽ bị treo ở vùng bão hòa khuếch đại (vùng tuyến tính) quá lâu $\implies$ Sinh ra dòng ngắn mạch từ $V_{DD}$ xuống $V_{SS}$ cực lớn, làm tăng vọt **công suất tiêu tán động (Dynamic Power)** và gây sụt áp nguồn.
  * Sườn xung quá bẹt làm mất độ tin cậy thời gian, dễ bị nhiễu xuyên âm (Crosstalk Noise) kích hoạt lật trạng thái sai lệch.

---

### 3. Cây Phân Phối Xung Nhịp: Clock Latency & Clock Skew

Trong một con chip có hàng triệu Flip-Flop, xung nhịp Clock xuất phát từ bộ tạo dao động (PLL / Crystal Oscillator) phải đi qua một mạng lưới khổng lồ các cổng đệm gọi là **Cây Xung Nhịp (Clock Tree Synthesis - CTS)**:

![Mô hình Cây phân phối xung nhịp Clock Tree Synthesis](file:///D:/Tapeout_chip/buoi_3/docs/cay_xung_nhip_cts_clock_tree.svg)

* **Clock Latency (Độ trễ Clock / Insertion Delay):** Tổng thời gian từ lúc một cạnh xung xuất hiện tại chân nguồn phát (Source) cho đến khi nó bò qua toàn bộ cây đệm để chạm vào chân `CK` của Flip-Flop đích.
  * Nhánh phát (Launch FF1): $T_{\text{clk1}} = 0.60\,\text{ns}$ (đến rất sớm).
  * Nhánh thu (Capture FF2): $T_{\text{clk2}} = 1.10\,\text{ns}$ (đến rất muộn).
* **Clock Skew ($T_{\text{skew}}$):** Độ lệch thời gian giữa hai chân `CK` của hai Flip-Flop khác nhau:
  $$T_{\text{skew}} = T_{\text{clk2}} - T_{\text{clk1}} = 1.10\,\text{ns} - 0.60\,\text{ns} = \mathbf{+0.50\,\text{ns} \ (+500\,\text{ps})}$$
  * **Positive Skew ($T_{\text{skew}} > 0$):** Cạnh clock đến thanh ghi đích trễ hơn thanh ghi phát $\implies$ **Giúp ích cho Setup Time** (thanh ghi đích có thêm thời gian chờ), nhưng **cực kỳ nguy hiểm cho Hold Time** (dữ liệu mới từ FF1 phóng qua đè nát dữ liệu cũ của FF2 trước khi FF2 kịp chốt)!
  * **Negative Skew ($T_{\text{skew}} < 0$):** Cạnh clock đến thanh ghi đích sớm hơn thanh ghi phát $\implies$ Bóp nghẹt Setup Time, nhưng giúp nới rộng biên an toàn cho Hold Time.

---

### 4. Cơ Chế Công Cụ CTS (Clock Tree Synthesis) Cân Bằng Cây Xung Nhịp

Trong giai đoạn Physical Design (PnR), công cụ tự động (như TritonCTS trong OpenROAD) sẽ quét toàn bộ cây xung nhịp và thực hiện tái cấu trúc mạng đệm để triệt tiêu độ lệch pha Clock Skew từ mức nguy hiểm $+500\,\text{ps}$ về mức lý tưởng $\approx 0\,\text{ps}$ (**Zero-Skew Clock Tree**):

![Cơ chế cân bằng cây xung nhịp của công cụ CTS Trước và Sau](file:///D:/Tapeout_chip/buoi_3/docs/cts_can_bang_clock_tree_truoc_va_sau.svg)

#### 3 Vũ Khí Tối Thượng Của Công Cụ CTS Để Cân Bằng Cây:
1. **Chèn đệm trễ bù trừ (Delay Matching Buffers / Delay Padding):**  
   Công cụ phát hiện nhánh `FF1` đến quá sớm ($0.60\,\text{ns}$). Nó chủ động chèn thêm 2 bộ đệm (`clkbuf_4`) vào nhánh `FF1` để **cố tình làm chậm nhánh này**, kéo thời gian đến tăng từ $0.60\,\text{ns}$ lên $1.085\,\text{ns}$.
2. **Điều chỉnh kích cỡ bộ đệm (Cell Sizing / Buffer Upsizing):**  
   Ở nhánh `FF2` tải nặng và xa nguồn, công cụ upsize bộ đệm từ cỡ nhỏ lên cỡ cực đại (`clkbuf_16`) để tăng khả năng phóng dòng nạp tụ, ép độ trễ của nhánh chậm giảm xuống còn $1.100\,\text{ns}$.
3. **Cấu trúc hình học đối xứng (Symmetric H-Tree Routing):**  
   Thay vì đi dây tùy tiện, công cụ luồn dây theo dạng cây đối xứng chữ H (H-Tree Topology), đảm bảo mọi đường dây từ gốc PLL tỏa ra các góc chip đều có cùng chiều dài và cùng điện dung ký sinh $RC$.

👉 **Kết quả đạt được:**  
$$\text{Clock Skew mới} = 1.100\,\text{ns} - 1.085\,\text{ns} = \mathbf{+15\,\text{ps}} \approx \mathbf{0\,\text{ps}}$$
Hai sườn clock tại `FF1` và `FF2` hạ cánh **đồng pha hoàn hảo**, triệt tiêu hoàn toàn hiểm họa vi phạm Hold Time trên toàn chip!

---

## ⏱️ PHẦN III: PHÂN TÍCH CHI TIẾT THỜI GIAN THANH GHI ĐẾN THANH GHI (FF-TO-FF TIMING ANALYSIS)

Mô hình kinh điển nhất trong phân tích STA là chặng truyền thông giữa hai thanh ghi: **Launch Flip-Flop (FF1)** phát dữ liệu, dữ liệu đi qua đám mây logic tổ hợp, và **Latch Flip-Flop (FF2)** thu nhận dữ liệu.

![Mô hình phân tích thời gian Thanh ghi đến Thanh ghi (FF-to-FF)](file:///D:/Tapeout_chip/buoi_3/docs/mo_hinh_thoi_gian_ff_to_ff.svg)

---

### 💡 Đúc Kết Bản Chất: Tại Sao Bắt Buộc Phải Xét Cặp Flip-Flop (FF1 & FF2) Trong Phân Tích Timing?

Trong thiết kế vi mạch số, đường dữ liệu tại chân `D` không thể tự đo lường độc lập. Mọi khế ước thời gian thực chất là **sự tương tác đồng bộ giữa hai trạm gửi và nhận**:

#### 1. Sự Cần Thiết Của Cặp Flip-Flop: Vạch Xuất Phát & Vạch Đích
* **Chân `D` của FF2 chỉ là Vạch Đích:** Nơi tiếp nhận và kiểm định kết quả.
* **Con FF1 là Vạch Xuất Phát:** Để xác định được thời gian di chuyển, bắt buộc phải có một điểm mốc phát lệnh. Con FF1 định nghĩa chính xác thời điểm dữ liệu bắt đầu rời bến ($t = 0$).
* **Hai thông số cốt lõi được hình thành từ sự tương tác này:**
  * **$T_{\text{arrival}}$ (Thời gian đến thực tế):** Là khoảng thời gian từ lúc FF1 bắt đầu gửi dữ liệu, băng qua quãng đường logic tổ hợp, cho đến khi tín hiệu thực sự chạm vào chân `D` của FF2.
  * **$T_{\text{required}}$ (Thời điểm yêu cầu):** Là thời điểm mà xung nhịp `CLK2` gõ tới chân clock của FF2 để ra lệnh chốt dữ liệu (được trừ lùi hoặc cộng thêm các khoảng an toàn vật lý của linh kiện).

#### 2. Hai Thái Cực Tốc Độ Và Hai Lỗi Sinh Tử Của Thế Giới Bán Dẫn

Từ mối quan hệ giữa thời điểm dữ liệu đến ($T_{\text{arrival}}$) và thời điểm xung nhịp gõ cửa ($T_{\text{required}}$), toàn bộ quy chuẩn đóng timing (Timing Closure) quy về việc kiểm soát **hai thái cực tốc độ**:

* **Thái cực 1: Dữ liệu chạy QUÁ CHẬM ($T_{\text{arrival}} > T_{\text{required\_setup}}$) $\implies$ LỖI SETUP (Setup Violation):**
  * *Hiện tượng:* Xung nhịp `CLK2` của chu kỳ kế tiếp đã gõ cửa đòi chốt dữ liệu, nhưng dữ liệu mới từ FF1 vẫn chưa kịp bò tới nơi.
  * *Hậu quả:* FF2 chốt trượt, nuốt phải giá trị cũ hoặc giá trị rác làm sai kết quả tính toán.
  * *Đặc tính cứu sống:* **Cứu được $100\%$** bằng cách hạ tần số xung nhịp (kéo dãn chu kỳ để sườn `CLK2` lùi về sau, cho dữ liệu thêm thời gian chạy tới đích).

* **Thái cực 2: Dữ liệu chạy QUÁ NHANH ($T_{\text{arrival}} < T_{\text{required\_hold}}$) $\implies$ LỖI HOLD (Hold Violation):**
  * *Hiện tượng:* Xung nhịp `CLK2` của chu kỳ hiện tại vừa mới gõ xuống, FF2 đang cần một khoảng thời gian cực ngắn ($T_{\text{hold}}$) để chốt yên vị dữ liệu của chu kỳ này. Tuy nhiên, vì quãng đường giữa 2 FF quá ngắn, **dữ liệu mới của chu kỳ sau từ FF1 đã phóng tới quá nhanh**, tràn vào đè bẹp dữ liệu đang chốt dở dang trước khi FF2 kịp khóa cổng.
  * *Hậu quả:* Dữ liệu bị ghi đè hỗn loạn, mạch mất khả năng lưu trữ.
  * *Đặc tính chết chóc:* **Chết chip vĩnh viễn.** Vì lỗi xảy ra ngay tại cùng thời điểm chuyển mạch, dù có hạ tần số xung nhịp xuống thấp bao nhiêu thì dữ liệu mới vẫn chạy nhanh hơn sườn chốt $\implies$ **Bắt buộc phải sửa từ lúc thiết kế bằng cách chèn thêm các cổng đệm (Buffer Padding) vào đường truyền ngắn nhất để cố tình cản đường, làm chậm dữ liệu mới lại!**

#### 3. Bảng Tổng Kết Quy Tắc Tốc Độ Dữ Liệu

| Tiêu Chí So Sánh | Chạy Quá Chậm: Lỗi Setup | Chạy Quá Nhanh: Lỗi Hold |
| :--- | :--- | :--- |
| **Mối quan hệ thời gian** | $T_{\text{arrival}} > T_{\text{required\_setup}}$ *(Đến sau hạn chót)* | $T_{\text{arrival}} < T_{\text{required\_hold}}$ *(Đến trước khi cửa kịp khóa)* |
| **Nguy cơ vật lý** | Dữ liệu mới chưa kịp hội tụ điện áp. | Dữ liệu mới đè hỏng dữ liệu cũ. |
| **Giải pháp EDA / PnR** | Tối ưu đường dài nhất, tăng drive cell, thêm pipeline. | **Chèn Buffer vào đường ngắn nhất (Shortest Path)** để tăng trễ. |
| **Số phận sau Tapeout** | **Sống sót** (chỉ cần giảm MHz khi chạy thật). | **Chết vĩnh viễn thành "cục gạch"** (không cứu được). |

---

### 1. Các Mốc Thời Gian Cốt Tử
1. **Launch Edge (Cạnh phát):** Cạnh tích cực của Clock tại thời điểm $t = 0$ kích hoạt FF1 đẩy dữ liệu từ ngõ vào ra ngõ `Q`.
2. **Latch Edge (Cạnh chốt):** Cạnh tích cực tiếp theo của Clock (tại thời điểm $t = T_{\text{clk}}$) dùng để chốt dữ liệu vào FF2.
3. **Clock-to-Q Delay ($T_{\text{cq}}$ hoặc $T_{\text{co}}$):** Thời gian trễ nội tại bên trong Flip-Flop, tính từ lúc cạnh Clock đập vào chân `CK` đến khi bit dữ liệu ổn định tại chân `Q`.
4. **Setup Time ($T_{\text{su}}$):** Khoảng thời gian tối thiểu mà dữ liệu tại chân `D` của FF2 phải được giữ **ổn định TUYỆT ĐỐI TRƯỚC KHI** cạnh Latch Edge ập đến.
5. **Hold Time ($T_{\text{h}}$):** Khoảng thời gian tối thiểu mà dữ liệu tại chân `D` của FF2 phải tiếp tục được **giữ nguyên KHÔNG ĐỔI SAU KHI** cạnh Latch Edge đã đi qua.
6. **Clock Uncertainty ($T_{\text{uncertainty}}$):** Khoảng đệm an toàn dự phòng cho hiện tượng rung pha (Jitter) của bộ dao động Clock và độ lệch pha chưa lường hết được trước layout.

---

### 2. Thiết Lập Phương Trình Toán Học Của Khế Ước Thời Gian (Timing Slacks)

#### A. Phân Tích Đường Đến Thật Sự Của Dữ Liệu (Data Arrival Time)
Thời điểm thực tế mà hạt electron mang dữ liệu mới chạm chân `D` của FF2:
$$\text{Data Arrival Time} = \text{Launch Edge} + T_{\text{clk1}} + T_{\text{cq}} + T_{\text{data}}$$

Trong đó:
* $\text{Launch Edge} = 0$ (mốc quy chiếu).
* $T_{\text{clk1}}$: Độ trễ clock từ nguồn đến chân CK của Launch FF.
* $T_{\text{cq}}$: Trễ nội tại Clock-to-Q của Launch FF.
* $T_{\text{data}}$: Tổng trễ qua các cổng logic tổ hợp và dây dẫn ($T_{\text{comb}} + T_{\text{net}}$).

---

#### B. Phân Tích Hạn Chót Cho Phép Của Setup (Data Required Time - Setup)
Dữ liệu buộc phải đến trước cạnh Latch Edge một khoảng ít nhất bằng Setup Time và Uncertainty:
$$\text{Data Required Time (Setup)} = \text{Latch Edge} + T_{\text{clk2}} - T_{\text{su}} - \text{Setup Uncertainty}$$

Trong đó $\text{Latch Edge} = T_{\text{clk}}$ (sau 1 chu kỳ).

$$\implies \mathbf{\text{Setup Slack}} = \text{Data Required Time (Setup)} - \text{Data Arrival Time}$$

> 🟢 **ĐIỀU KIỆN ĐẠT SETUP:**  
> $$\text{Setup Slack} \ge 0$$  
> * Ý nghĩa: Dữ liệu đến **sớm hơn** hạn chót yêu cầu. Slack càng dương thì mạch càng chạy an toàn hoặc có thể ép xung cao hơn!

---

#### C. Phân Tích Giới Hạn Ngăn Chặn Của Hold (Data Required Time - Hold)
Sau khi chốt nhịp Latch Edge, dữ liệu cũ phải được giữ ổn định trong khoảng $T_{\text{h}} + \text{Hold Uncertainty}$. Do đó, dữ liệu mới phóng đi từ nhịp Latch Edge không được phép chạm tới chân D trước mốc:
$$\text{Data Required Time (Hold)} = \text{Latch Edge} + T_{\text{clk2}} + T_{\text{h}} + \text{Hold Uncertainty}$$

Trong đó, xét trong cùng chu kỳ chốt thì $\text{Latch Edge} = 0$ (hoặc xét cùng gốc thời gian).

$$\implies \mathbf{\text{Hold Slack}} = \text{Data Arrival Time (min)} - \text{Data Required Time (Hold)}$$

> 🟢 **ĐIỀU KIỆN ĐẠT HOLD:**  
> $$\text{Hold Slack} \ge 0$$  
> * Ý nghĩa: Dữ liệu mới chạy đến **chậm hơn** mốc bắt buộc phải giữ. Slack dương bảo đảm dữ liệu cũ không bị ghi đè khi chưa chốt xong!

---

## 🧮 PHẦN IV: BÀI TẬP THỰC CHIẾN & NGHỆ THUẬT SỬA LỖI TIMING

### 1. Đề Bài Thực Nghiệm Chuẩn Xưởng Đúc (Trích Slide Bài Giảng)

![Sơ đồ bài tập áp dụng thực chiến trích từ Slide bài giảng Buổi 3](file:///D:/Tapeout_chip/buoi_3/docs/slide_bai_tap_ap_dung_timing.svg)
*Hình IV.1: Trích dẫn nguyên văn slide bài giảng Buổi 3 (Slide 11) - Sơ đồ nguyên lý mạch cổng logic và bộ thông số thời gian chuẩn xưởng đúc.*

Cho một mạch số đồng bộ có các thông số thư viện tế bào chuẩn sau:
* $T_{\text{ccq}} = 30\,\text{ps}$ (Trễ Clock-to-Q nhanh nhất / Contamination delay).
* $T_{\text{pcq}} = 80\,\text{ps}$ (Trễ Clock-to-Q chậm nhất / Propagation delay).
* $T_{\text{su}} = 50\,\text{ps}$ (Setup time yêu cầu của Flip-Flop).
* $T_{\text{h}} = 60\,\text{ps}$ (Hold time yêu cầu của Flip-Flop).
* $T_{\text{pd}} = 40\,\text{ps}$ (Độ trễ cổng logic chậm nhất).
* $T_{\text{cd}} = 25\,\text{ps}$ (Độ trễ cổng logic nhanh nhất).
* Giả định Clock Skew lý tưởng $T_{\text{skew}} = 0$, $T_{\text{uncertainty}} = 0$.

Mạch tổ hợp giữa 2 tầng FF gồm:
* Nhánh dài nhất (Critical Path): Đi qua **3 cổng logic** ($\text{AND} \rightarrow \text{OR} \rightarrow \text{NOR}$).
* Nhánh ngắn nhất (Shortest Path): Chỉ đi qua **1 cổng logic** ($\text{OR}$ hoặc $\text{NOR}$).

---

### 2. Lời Giải Định Lượng 1: Tính Tần Số Tối Đa ($F_{\max}$) & Xử Lý Setup
* **Đường tới hạn (Critical Path):** Nhánh có trễ lớn nhất, quyết định tần số đồng hồ tối đa con chip có thể gánh được.
  $$T_{\text{comb\_max}} = 3 \times T_{\text{pd}} = 3 \times 40\,\text{ps} = 120\,\text{ps}$$
* **Chu kỳ Clock tối thiểu ($T_c$):**
  $$T_c \ge T_{\text{pcq}} + T_{\text{comb\_max}} + T_{\text{su}}$$
  $$T_c \ge 80\,\text{ps} + 120\,\text{ps} + 50\,\text{ps} = \mathbf{250\,\text{ps}}$$
  *(Trong bài giảng xét trường hợp tối ưu trễ cổng $3 \times 40 = 120\,\text{ps}$ cộng gộp cho ra ngưỡng $240\,\text{ps} - 250\,\text{ps}$).*
* **Tần số hoạt động tối đa ($F_{\max}$):**
  $$F_{\max} = \frac{1}{T_c} = \frac{1}{250\,\text{ps}} = \mathbf{4.0\,\text{GHz}}$$

---

### 3. Lời Giải Định Lượng 2: Phát Hiện Vi Phạm Hold & Nghệ Thuật Chèn Buffer
* **Khảo sát đường nhanh nhất (Shortest Path):**
  Tín hiệu phóng ra nhanh nhất từ ngõ Q của Launch FF và chỉ lướt qua đúng 1 cổng logic:
  $$T_{\text{arrival\_min}} = T_{\text{ccq}} + T_{\text{cd}} = 30\,\text{ps} + 25\,\text{ps} = \mathbf{55\,\text{ps}}$$
* **Kiểm tra vi phạm Hold:**
  Ta có yêu cầu thời gian giữ: $T_{\text{h}} = 60\,\text{ps}$.
  $$\text{Hold Slack} = T_{\text{arrival\_min}} - T_{\text{h}} = 55\,\text{ps} - 60\,\text{ps} = \mathbf{-5\,\text{ps}} \quad \implies \text{VI PHẠM (FAIL)!}$$
  > 💥 **HIỆN TƯỢNG:** Dữ liệu mới đến quá sớm (ở mốc $55\,\text{ps}$), trong khi Latch FF yêu cầu dữ liệu cũ phải đứng yên đến mốc $60\,\text{ps}$. Mạch sẽ nuốt mất bit dữ liệu cũ!

#### 🛠️ Phương Pháp Khắc Phục Bằng Kỹ Thuật Chèn Buffer (Buffer Insertion):

![Minh chứng giải pháp chèn buffer khắc phục vi phạm Hold time trích từ Slide bài giảng Buổi 3](file:///D:/Tapeout_chip/buoi_3/docs/slide_giai_phap_chen_buffer_hold.svg)
*Hình IV.2: Minh chứng thực tế từ Slide bài giảng Buổi 3 (Slide 15) - Kỹ thuật chèn Buffer (trễ 25ps) vào các nhánh ngắn n2 (FF C) và n3 (FF D) để kéo dãn thời gian đến, giải quyết triệt để vi phạm Hold time.*

* **Giải pháp:** Chèn thêm các cổng đệm (Buffer) có độ trễ $T_{\text{buf}} = 25\,\text{ps}$ vào đường ngắn nhất.
* **Thời gian đến mới sau khi chèn:**
  $$T_{\text{arrival\_new}} = 30\,\text{ps} + 25\,\text{ps} + 25\,\text{ps}\,(\text{Buffer}) = \mathbf{80\,\text{ps}}$$
* **Đánh giá lại Hold Slack:**
  $$\text{Hold Slack} = 80\,\text{ps} - 60\,\text{ps} = \mathbf{+20\,\text{ps}} \quad \implies \text{AN TOÀN TUYỆT ĐỐI (PASS)!}$$

> ⚠️ **HAI NGUYÊN TẮC VÀNG CỦA KIẾN TRÚC SƯ KHI SỬA TIMING:**  
> 1. **Chỉ được chèn Buffer vào Shortest Path để sửa lỗi Hold.**  
> 2. **TUYỆT ĐỐI KHÔNG CHÈN BUFFER VÀO CRITICAL PATH!** Việc chèn thêm cổng vào đường dài nhất sẽ làm $T_{\text{data}}$ tăng vọt, gây sụp đổ Setup Slack và làm giảm tốc độ toàn bộ con chip.  
> 3. **Tận dụng Clock Skew (Useful Skew):** Có thể điều chỉnh mạng phân phối clock để đưa cạnh Latch trễ hơn hoặc sớm hơn một cách có chủ đích nhằm cân bằng giữa Setup và Hold.

---

## 🏛️ PHẦN V: MÔI TRƯỜNG STA & MA TRẬN PVT CORNERS

### 1. Bốn Nhóm Đường Timing Căn Bản (The 4 Timing Paths)
Trong một thiết kế số bất kỳ, mọi đường truyền tín hiệu đều được OpenSTA/OpenROAD quy về 4 nhóm:

![Bốn nhóm đường timing căn bản trong thiết kế ASIC](file:///D:/Tapeout_chip/buoi_3/docs/bon_nhom_duong_timing_paths.svg)
*Hình V.1: Bốn nhóm đường Timing căn bản (The 4 Timing Paths) trên lõi chip bán dẫn và các khế ước ràng buộc SDC tương ứng.*

---

#### 🔍 Chi Tiết Phân Tích Vật Lý Cấp Độ Chân (Pin-Level) & Khối Mạch (Block-Level):

Để công cụ STA (như OpenSTA hay PrimeTime) tính toán và xuất báo cáo độ trễ (Timing Report), nó không bao giờ nhìn mạch một cách trừu tượng chung chung mà luôn bẻ nhỏ đường truyền thành từng cặp **Startpoint** (Điểm bắt đầu) và **Endpoint** (Điểm kết thúc) gắn liền với từng chân vật lý cụ thể của các cell chuẩn:

---

#### 🔹 1. Path 1: In2Reg (Input Port → Sequential Register)
* **Khối & Chân bắt đầu (Startpoint):**
  * **Khối nguồn:** Cổng tiếp xúc ngoại vi của chip (**Khối Input Pad** trên vành đai IO Pad Ring).
  * **Chân vật lý bắt đầu:** Chân **`PAD_IN`** (ví dụ chân `data_in[7:0]`, `enable`, `rst_n`).
  * **Nguồn nhịp kích hoạt:** Được xem như phóng ra từ sườn xung của một đồng hồ ảo (*Virtual Clock*) hoặc đồng hồ của IC đối tác trên bo mạch PCB bên ngoài chip.
* **Hành trình trung gian:**
  * Dữ liệu đi qua bộ chuyển mức/đệm ngõ vào (Input Buffer như `sky130_fd_sc_hd__buf_*`).
  * Đi vào các chân ngõ vào logic (`A`, `B`, `S`) của chuỗi cổng mạch tổ hợp đầu vào (**Mạch tổ hợp CL1**, ví dụ: cổng giải mã, MUX chọn kênh) và đi ra tại các chân ngõ ra (`Y`, `X`).
* **Khối & Chân kết thúc (Endpoint):**
  * **Khối đích:** Phần tử nhớ tuần tự đầu tiên nhận dữ liệu (**Flip-Flop `Reg 1`**).
  * **Chân vật lý tiếp nhận:** **Chân dữ liệu `D` (Data Input Pin)** của tế bào `Reg 1`.
  * **Chân kiểm định thời gian (Clock Reference Pin):** **Chân xung nhịp `CLK` (hoặc `CK`)** của chính `Reg 1`.
* **Cơ chế ràng buộc STA:** Dữ liệu từ môi trường ngoài chạy qua `CL1` phải có mặt và đứng yên tại chân `D` của `Reg 1` tối thiểu một khoảng thời gian $T_{\text{setup}}$ trước khi sườn xung Clock của chip đánh vào chân `CK` của `Reg 1`.
* **Khế ước SDC bắt buộc:**
  ```tcl
  set_input_delay -clock [get_clocks CLK] -max <T_in_max> [get_ports data_in]
  ```

---

#### 🔸 2. Path 2: Reg2Reg (Register → Register) — [TRỤC XƯƠNG SỐNG CỐT TỬ >90%]
* **Khối & Chân bắt đầu (Startpoint):**
  * **Khối nguồn:** Flip-Flop phát tín hiệu (**Launch Flip-Flop `Reg 1`**).
  * **Chân nhận xung kích hoạt:** **Chân xung nhịp `CLK` (hoặc `CK`)** của `Reg 1`. Sườn xung nhịp gõ vào chân `CK` này là mốc $t = 0$.
  * **Chân phóng dữ liệu ra:** **Chân dữ liệu ngõ ra `Q` (Data Output Pin)** của `Reg 1`. Sau khoảng trễ vật lý $T_{\text{cq}}$ (Clock-to-Q delay), mức logic mới chính thức xuất hiện tại chân `Q` này.
* **Hành trình trung gian:**
  * Tín hiệu từ chân `Q` của `Reg 1` lan truyền trên các lớp kim loại (Metal Interconnect), lần lượt đi vào các chân ngõ vào (như chân `A`, `B`) của chuỗi cổng logic tổ hợp (**Mạch tổ hợp CL2** - chứa ALU, bộ cộng, nhân, shifters), chuyển mức tại các chân ngõ ra (`Y`, `X`) và nạp xả cho điện dung ký sinh.
* **Khối & Chân kết thúc (Endpoint):**
  * **Khối đích:** Flip-Flop chốt tín hiệu (**Latch / Capture Flip-Flop `Reg 2`**).
  * **Chân vật lý tiếp nhận:** **Chân dữ liệu ngõ vào `D` (Data Input Pin)** của tế bào `Reg 2`.
  * **Chân kiểm định thời gian (Clock Reference Pin):** **Chân xung nhịp `CLK` (hoặc `CK`)** của `Reg 2`.
* **Cơ chế ràng buộc STA:** 
  * **Setup Check:** Dữ liệu phóng từ chân `Q` của `Reg 1`, sau khi chạy qua toàn bộ chuỗi cổng `CL2`, phải cập bến chân `D` của `Reg 2` và ổn định hoàn toàn trước khi sườn Clock tiếp theo đánh vào chân `CK` của `Reg 2` một khoảng $T_{\text{setup}}$.
  * **Hold Check:** Dữ liệu mới phóng từ chân `Q` không được chạy quá nhanh tới chân `D` của `Reg 2` làm phá hỏng dữ liệu cũ trước khi sườn Clock tại chân `CK` của `Reg 2` duy trì xong thời gian $T_{\text{hold}}$.
* **Khế ước SDC bắt buộc:**
  ```tcl
  create_clock -name CLK -period <T_cycle> [get_ports clk]
  ```
  *(Đường này chiếm trên $90\%$ tổng số đường trong chip và là nhân tố độc tôn quyết định tần số hoạt động tối đa $F_{\max}$).*

---

#### 🔹 3. Path 3: Reg2Out (Sequential Register → Output Port)
* **Khối & Chân bắt đầu (Startpoint):**
  * **Khối nguồn:** Flip-Flop cuối cùng của chuỗi xử lý số (**Sequential Register `Reg 2`**).
  * **Chân nhận xung kích hoạt:** **Chân xung nhịp `CLK` (`CK`)** của `Reg 2`.
  * **Chân phóng dữ liệu ra:** **Chân dữ liệu ngõ ra `Q` (Data Output Pin)** của `Reg 2` (sau khoảng trễ nội $T_{\text{cq}}$).
* **Hành trình trung gian:**
  * Dữ liệu từ chân `Q` đi vào các chân ngõ vào của mạch logic tổ hợp ngõ ra (**Mạch tổ hợp CL3**, ví dụ: bộ đệm xuất, bộ ghép kênh ra Bus).
  * Đi vào chân ngõ vào của tầng khuếch đại công suất xuất ngoại vi (**Output Pad Driver Cell** như `sky130_ef_io__pad_out`).
* **Khối & Chân kết thúc (Endpoint):**
  * **Khối đích:** Cổng tiếp xúc vật lý xuất tín hiệu ra vỏ chip (**Khối Output Pad** trên vành đai chip).
  * **Chân vật lý kết thúc:** **Chân `PAD_OUT` (hoặc Port OUT của chip, ví dụ `data_out[7:0]`, `valid_out`)**.
* **Cơ chế ràng buộc STA:** Dữ liệu từ chân `Q` chạy ra chân `PAD_OUT` phải kịp xuất hiện và ổn định trên board mạch ngoài trước khi chip đối tác bên ngoài chốt dữ liệu vào kỳ clock tiếp theo.
* **Khế ước SDC bắt buộc:**
  ```tcl
  set_output_delay -clock [get_clocks CLK] -max <T_out_max> [get_ports data_out]
  ```

---

#### 🔸 4. Path 4: In2Out (Input Port → Output Port — Pure Combinational / Feedthrough)
* **Khối & Chân bắt đầu (Startpoint):**
  * **Khối nguồn:** Cổng tiếp xúc ngoại vi đầu vào của chip (**Khối Input Pad**).
  * **Chân vật lý bắt đầu:** **Chân `PAD_IN` (hoặc Port IN của chip)**.
* **Hành trình trung gian:**
  * Tín hiệu từ chân `PAD_IN` đi qua tầng đệm ngõ vào, đi thẳng qua mạng cổng tổ hợp (**Mạch tổ hợp CL4** - ví dụ: đường Multiplexer bypass, đường truyền tín hiệu Reset khẩn cấp, đường truyền bus thử nghiệm quét chuỗi Scan).
  * **Đặc tính độc nhất:** Dữ liệu chạy xuyên suốt qua silicon mà **KHÔNG HỀ ĐI QUA BẤT KỲ CHÂN `D` HAY CHÂN `Q` CỦA BẤT KỲ MỘT FLIP-FLOP NÀO**, cũng không bị chặn lại bởi bất kỳ nhịp đồng hồ `CLK` nào!
* **Khối & Chân kết thúc (Endpoint):**
  * **Khối đích:** Cổng tiếp xúc ngoại vi đầu ra của chip (**Khối Output Pad**).
  * **Chân vật lý kết thúc:** **Chân `PAD_OUT` (hoặc Port OUT của chip)**.
* **Cơ chế ràng buộc STA:** Vì không có sườn clock chốt chặn ở giữa, STA quản lý đường này bằng cách ấn định một giới hạn độ trễ truyền lan tối đa (Max Delay) từ chân `PAD_IN` đến chân `PAD_OUT` để không làm nghẽn bus hệ thống bên ngoài.
* **Khế ước SDC bắt buộc:**
  ```tcl
  set_max_delay <T_max> -from [get_ports in_pin] -to [get_ports out_pin]
  ```

---

#### 📊 Bảng Đánh Giá & Tổng Hợp Bản Chất 4 Nhóm Đường Timing

> 💡 **QUY TẮC VÀNG VỀ NHỊP ĐỒNG HỒ (CLOCKED PATHS):**  
> Bất kỳ đường truyền nào chịu sự kiểm soát của xung nhịp đồng hồ (**Path 1, Path 2, Path 3**) đều **LUÔN LUÔN tồn tại song song cả 2 bài toán sống còn:**  
> 1. Kiểm tra **$T_{\max}$** để chống lỗi **Setup** (Chống chạy quá chậm / Đảm bảo tần số $F_{\max}$).  
> 2. Kiểm tra **$T_{\min}$** để chống lỗi **Hold** (Chống chạy quá nhanh / Đảm bảo không ghi đè dữ liệu cũ).

| Nhóm Đường (Timing Path) | $T_{\max}$ kiểm tra cái gì? (Setup Check) | $T_{\min}$ kiểm tra cái gì? (Hold Check) | Có ảnh hưởng tới chu kỳ Clock $T_{\text{clk}}$? |
| :--- | :--- | :--- | :---: |
| **Path 1: In2Reg**<br>*(Input → Register)* | **Setup** của Flip-Flop nội bộ (`Reg 1`)<br>*(Tín hiệu ngoài vào không được đến quá trễ)* | **Hold** của Flip-Flop nội bộ (`Reg 1`)<br>*(Tín hiệu ngoài vào không được đến quá sớm)* | **Có**<br>*(Chiếm một phần ngân sách chu kỳ)* |
| **Path 2: Reg2Reg**<br>*(Register → Register)* | **Setup** của Flip-Flop nội bộ (`Reg 2`)<br>*(Dữ liệu từ Reg 1 qua logic không được quá trễ)* | **Hold** của Flip-Flop nội bộ (`Reg 2`)<br>*(Dữ liệu từ Reg 1 không được nuốt bit cũ)* | **QUYẾT ĐỊNH CHÍNH ($>90\%$)**<br>*(Định đoạt tần số hoạt động tối đa $F_{\max}$)* |
| **Path 3: Reg2Out**<br>*(Register → Output)* | **Setup** của Chip đối tác bên ngoài bo mạch<br>*(Tín hiệu phóng ra Pad phải kịp trước hạn chót)* | **Hold** của Chip đối tác bên ngoài bo mạch<br>*(Tín hiệu ra Pad không được ghi đè bit cũ của đối tác)* | **Có**<br>*(Chiếm một phần ngân sách chu kỳ)* |
| **Path 4: In2Out**<br>*(Input → Output)* | **Độ trễ lan truyền tối đa** cho phép xuyên chip<br>*(Pure Combinational Max Delay)* | **Độ trễ lan truyền tối thiểu** cho phép xuyên chip<br>*(Pure Combinational Min Delay)* | **KHÔNG**<br>*(Thuần túy tổ hợp, không qua Clock)* |

---

### 2. Bốn Trụ Cột Đầu Vào Bắt Buộc Của Cỗ Máy STA

Để cỗ máy OpenSTA có thể tính toán chính xác tới từng phần nghìn pico-giây, kỹ sư phải cấp đủ 4 file:

1. **Gate Netlist (`.v`):** Bản vẽ sơ đồ mạch mức cổng sau khi Yosys tổng hợp, mô tả rõ cổng nào nối với cổng nào.
2. **Thư viện Liberty (`.lib`):** Chứa toàn bộ bảng tra cứu NLDM mô tả độ trễ, tụ ngõ vào, trễ $T_{\text{cq}}$, $T_{\text{su}}$, $T_{\text{h}}$ của từng cell chuẩn ở các góc điện áp/nhiệt độ.
3. **Khế ước ràng buộc SDC (`.sdc` - Synopsys Design Constraints):** File do kỹ sư tự tay viết, quy định rõ:
   * Xung nhịp bao nhiêu MHz (`create_clock`).
   * Biên rung pha Jitter bao nhiêu (`set_clock_uncertainty`).
   * Độ trễ của tín hiệu ngoại vi bên ngoài đưa vào chip (`set_input_delay`, `set_output_delay`).
   * Ràng buộc vật lý sườn xung và tải tụ (`set_max_transition`, `set_max_capacitance`).
4. **Tệp ký sinh sau đi dây (`.spef` - Standard Parasitic Exchange Format):** Chứa các giá trị điện trở $R$ và tụ điện $C$ của từng đoạn dây đồng/nhôm thật trên từng lớp kim loại sau khi chạy PnR.

---

### 3. Ma Trận Giải Mã 9 Góc PVT Corners (Process - Voltage - Temperature)

Tấm wafer sản xuất ra không bao giờ hoàn hảo tuyệt đối. Tùy thuộc vào nhà máy chế tạo (Process), điện áp nguồn cấp thực tế (Voltage), và môi trường chip hoạt động (Temperature), một tế bào chuẩn có thể chạy rất nhanh hoặc cực kỳ chậm chạp:

| Tên PVT Corner trong OpenLane | Giải Mã Tên Gọi | Ý Nghĩa Vật Lý Bán Dẫn & Tác Động Lên Chip |
| :--- | :--- | :--- |
| **`nom_tt_025C_1v80`** | **Nominal wire, Typical-Typical, $25^\circ\text{C}$, $1.80\,\text{V}$** | Điều kiện danh định chuẩn phòng thí nghiệm: Transistor điển hình, nhiệt độ phòng $25^\circ\text{C}$, nguồn $1.8\,\text{V}$. |
| **`nom_tt_100C_1v60`** | **Nominal wire, Typical-Typical, $100^\circ\text{C}$, $1.60\,\text{V}$** | Điều kiện cực trị nhiệt độ cao, sụt áp nguồn xuống $1.6\,\text{V}$ $\implies$ **Cell chạy rất chậm**. |
| **`nom_tt_n40C_1v95`** | **Nominal wire, Typical-Typical, $-40^\circ\text{C}$, $1.95\,\text{V}$** | Môi trường băng tuyết lạnh $-40^\circ\text{C}$, nguồn tăng vọt $1.95\,\text{V}$ $\implies$ **Cell chạy cực kỳ nhanh**. |
| **`min_tt_025C_1v80`** | **Minimum RC, TT, $25^\circ\text{C}$, $1.80\,\text{V}$** | Dây kim loại to mập, điện trở dây thấp $\implies$ **Dây truyền tín hiệu nhanh hơn danh định**. |
| **`max_tt_025C_1v80`** | **Maximum RC, TT, $25^\circ\text{C}$, $1.80\,\text{V}$** | Dây kim loại bị ăn mòn mỏng, điện trở dây lớn $\implies$ **Dây truyền tín hiệu chậm hơn danh định**. |
| **`min_ff_n40C_1v95`** | **Minimum RC, Fast-Fast, $-40^\circ\text{C}$, $1.95\,\text{V}$** | **GÓC NGUY HIỂM NHẤT CHO LỖI HOLD:** Transistor cực nhanh (FF), dây kim loại siêu tốc (Min RC), nhiệt độ âm lạnh, điện áp cao $\implies$ **Dữ liệu mới phóng đi như tên lửa, đe dọa trực tiếp đến Hold Time!** |
| **`max_ff_n40C_1v95`** | **Maximum RC, FF, $-40^\circ\text{C}$, $1.95\,\text{V}$** | Transistor rất nhanh nhưng dây kim loại bị chậm hơn. |
| **`min_ss_100C_1v60`** | **Minimum RC, Slow-Slow, $100^\circ\text{C}$, $1.60\,\text{V}$** | Transistor cực chậm nhưng dây nhanh. |
| **`max_ss_100C_1v60`** | **Maximum RC, Slow-Slow, $100^\circ\text{C}$, $1.60\,\text{V}$** | **GÓC NGUY HIỂM NHẤT CHO LỖI SETUP:** Transistor chậm chạp (SS), dây dẫn điện trở cao (Max RC), nhiệt độ sôi bỏng $100^\circ\text{C}$, điện áp yếu tụt còn $1.6\,\text{V}$ $\implies$ **Dữ liệu bò rùa bò, đe dọa trực tiếp đến Setup Time!** |

---

#### ⚠️ Hai "Góc Tử Thần" (The 2 Extreme Mortal Corners) Kỹ Sư Tapeout Bắt Buộc Phải Khắc Sâu

Dù OpenLane cung cấp 9 góc tra cứu đầy đủ, trong thực tế Tapeout công nghiệp, mọi chiến lược Timing Closure và phân tích báo cáo đều tập trung tuyệt đối vào **2 góc tử thần đối lập nhau 180 độ**:

```
[ min_ff_n40C_1v95 ] ◄─────────────────────────────────────────────► [ max_ss_100C_1v60 ]
      NHANH NHẤT                                                           CHẬM NHẤT
  (Best-Case Fast)                                                     (Worst-Case Slow)
  KẺ THÙ SỐ 1: HOLD                                                    KẺ THÙ SỐ 1: SETUP
```

##### 🐢 1. Góc Chậm Nhất: `max_ss_100C_1v60` (Worst-Case Slow Corner) — Kẻ Thù Số 1 Của Setup
* **Điều kiện vật lý hội tụ:**
  * **Process (SS):** Cả transistor NMOS và PMOS đều bị biến thiên quang khắc làm dày kênh dẫn $\implies$ khả năng dẫn dòng yếu nhất.
  * **Wire RC (Max RC):** Dây kim loại dẫn điện bị ăn mòn hẹp ngang hoặc mỏng dính $\implies$ điện trở dây $R$ cao nhất, làm hằng số trễ $\tau = R \times C$ tăng vọt.
  * **Temperature ($100^\circ\text{C}$):** Chip vận hành khi nóng sôi sục $\implies$ các nguyên tử silicon dao động nhiệt dữ dội làm tán xạ electron (*Mobility degradation*), cản trở dòng điện tích.
  * **Voltage ($1.60\,\text{V}$):** Điện áp nguồn cấp bị sụt áp sâu nhất (chênh $-11\%$ so với chuẩn $1.80\,\text{V}$) $\implies$ điện trường suy yếu, dòng dẫn $I_{\text{ds}}$ tụt thảm hại.
* **Tác động lên STA:** Toàn bộ tín hiệu di chuyển lờ đờ như rùa bò trên các đường truyền logic dài nhất (**Critical Path**).
* **Mục đích kiểm định:** OpenSTA mở file Liberty của góc này để **săn lùng vi phạm Setup Time**. Nếu mạch của bạn đạt $\text{Setup Slack} \ge 0$ ở góc này, con chip của bạn được bảo đảm $100\%$ sẽ chạy ổn định dù bị mang vào sa mạc hay pin sắp cạn kiệt!

##### 🚀 2. Góc Nhanh Nhất: `min_ff_n40C_1v95` (Best-Case Fast Corner) — Kẻ Thù Số 1 Của Hold
* **Điều kiện vật lý hội tụ:**
  * **Process (FF):** Cả transistor NMOS và PMOS đều có kênh dẫn mỏng, đóng ngắt cực nhạy $\implies$ dòng dẫn $I_{\text{ds}}$ đạt mức cực đại.
  * **Wire RC (Min RC):** Dây kim loại to mập, điện trở thấp $\implies$ tín hiệu lướt vèo vèo qua dây.
  * **Temperature ($-40^\circ\text{C}$):** Môi trường băng tuyết lạnh giá $\implies$ mạng tinh thể silicon tĩnh lặng, electron bay vun vút với độ linh động cực đại (*Maximum carrier mobility*).
  * **Voltage ($1.95\,\text{V}$):** Nguồn cấp bị kích vọt lên cao ($+8\%$ so với danh định $1.80\,\text{V}$) $\implies$ điện trường cực mạnh thúc dòng điện phóng qua các cổng.
* **Tác động lên STA:** Dữ liệu mới phóng đi như tên lửa trên các đường truyền ngắn nhất (**Shortest Path**). Tín hiệu mới lao bổ vào chân `D` của Flip-Flop khi chân này chưa kịp giữ mức bit cũ qua thời gian $T_{\text{hold}}$.
* **Mục đích kiểm định:** OpenSTA mở file Liberty của góc này để **săn lùng vi phạm Hold Time**. 
* **Tầm quan trọng sống còn:** Nếu bị vi phạm Hold ở góc này, bạn không thể giảm xung nhịp để cứu chip được. Do đó, kỹ sư bắt buộc phải nhìn báo cáo góc này để **chèn thêm Buffer vào Shortest Path** nhằm kéo dãn thời gian đến! Nếu đạt $\text{Hold Slack} \ge 0$ ở góc này, con chip của bạn vĩnh viễn không bao giờ bị đột tử thành "cục gạch"!

---

## 🔬 PHẦN VI: TỪ LÝ THUYẾT ĐẾN THỰC CHIẾN LAB 2 (BỘ NHÂN REGISTERED MULTIPLIER)

> 📓 **Sổ tay kinh nghiệm thực hành từng bước:** Chi tiết từng thao tác và bài học rút ra theo thời gian thực được lưu tại [Nhung_Kinh_Nghiem_Rut_Ra_Lab_2.md](file:///D:/Tapeout_chip/buoi_3/docs/Nhung_Kinh_Nghiem_Rut_Ra_Lab_2.md).

---

### 1. "Mớ Lý Thuyết Khô Khan" Ở Trên Giúp Giải Quyết Những Vấn Đề Gì Trong Lab 2?

Nhiều người học thường cảm thấy các công thức $T_{\text{setup}}$, $T_{\text{hold}}$, $T_{\text{arrival}}$, ma trận 9 góc PVT hay 4 Timing Paths là những mớ lý thuyết hàn lâm xa rời thực tế. Nhưng khi bước chân vào **Bài thực hành Lab 2 (Bộ nhân 8-bit Registered Multiplier `mult.v`)** trên nền tảng CTW SEMI / OpenLane, chính hệ thống lý thuyết này sẽ trở thành **chiếc kính hiển vi và chiếc la bàn sinh tử** giúp bạn làm chủ con chip:

![Kiến trúc mạch bộ nhân 8-bit Lab 2](file:///D:/Tapeout_chip/buoi_3/docs/kien_truc_bo_nhan_mult_lab2.svg)
*Hình VI.1: Sơ đồ khối kiến trúc phần cứng của Bộ nhân 8-bit (Registered Multiplier - mult.v), các cổng vào ra và vệt trễ tới hạn Critical Path (Path 1: In2Reg).*

---

#### 💡 Vấn Đề 1: Giúp bạn hiểu tường tận từng dòng trong file SDC (`mult.sdc`) thay vì copy-paste mù quáng
* **Nếu không có lý thuyết:** Bạn chỉ gõ theo hướng dẫn mà không hiểu tại sao phải đặt `set_input_delay 3.0` hay `set_clock_uncertainty 0.25`.
* **Lý thuyết đã giải phóng bạn như thế nào?**
  * Nhờ học về **Path 1 (In2Reg)** ở Phần V, bạn hiểu ngay con số $3.0\,\text{ns}$ của `set_input_delay` chính là lượng thời gian $T_{\text{in}}$ mà tín hiệu bên ngoài bo mạch đã tiêu tốn hết trước khi chạm vào chân `a`, `b` của chip.
  * Nhờ học về **Cây xung nhịp CTS và Clock Skew** ở Phần II, bạn hiểu ngay con số $0.25\,\text{ns}$ của `set_clock_uncertainty` là tấm khiên phòng vệ do kỹ sư tự đặt ra để trừ hao độ rung pha (Jitter) và độ lệch pha (Skew) của cây clock trước khi bước vào công đoạn PnR thực tế.

---

#### 💡 Vấn Đề 2: Giúp bạn "bắt đúng bệnh" trong bảng báo cáo STA 9 góc PVT (`summary.rpt`)
Khi bạn ép chu kỳ xung nhịp từ $15\,\text{ns}$ ($66.7\,\text{MHz}$) xuống **$13.0\,\text{ns}$ ($77\,\text{MHz}$)**, công cụ OpenSTA xuất ra một ma trận bảng số khổng lồ:

| Góc PVT (Corner) | Hold Worst Slack | Setup Worst Slack | Lỗi Setup (Vio) | Trạng Thái Timing | Nhận Định & Ý Nghĩa Vật Lý |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Overall (Toàn Chip)** | **`+2.5096 ns`** | **`-0.1477 ns`** | 3 lỗi | ❌ **FAIL (Setup)** | Tổng thể vi phạm Setup $1.13\%$ tại 3 đường |
| **`nom_tt_025C_1v80`** | `+2.6133 ns` | `+4.9902 ns` | 0 | ✅ **PASS** | Chuẩn danh định phòng Lab ($25^\circ\text{C}, 1.8\text{V}$): Dư dả thời gian |
| **`min_ff_n40C_1v95`**<br>*(Tử Thần Hold)* | **`+2.3896 ns`** | `+6.9657 ns` | 0 | 🛡️ **AN TOÀN** | Nhanh nhất ($-40^\circ\text{C}, 1.95\text{V}$): **Hold Slack dương** $\implies$ Không bao giờ chết chip |
| **`max_ss_100C_1v60`**<br>*(Tử Thần Setup)* | `+2.9143 ns` | **`-0.1477 ns`** | 2 lỗi | 🚨 **VI PHẠM** | Chậm nhất ($100^\circ\text{C}, 1.60\text{V}$): **Thủ phạm duy nhất** gây số âm cho toàn chip |

* **Nếu không có lý thuyết:** Bạn sẽ hoảng loạn khi thấy số âm `Setup WS = -0.1477`, không hiểu tại sao ở góc `nom_tt` và `min_ff` thì Setup Slack lại dương rất cao ($+4.99\,\text{ns}$ và $+6.96\,\text{ns}$), nhưng tổng thể mạch lại bị báo lỗi đỏ (Overall Fail).
* **Lý thuyết đã giải phóng bạn như thế nào?**
  * Nhờ học về **Hai Góc Tử Thần (Mortal Corners)** ở Phần V.3, bạn lập tức lia mắt ngay vào đúng 2 góc:
    1. **Soi góc `max_ss_100C_1v60` (Chậm nhất):** Nhận diện ngay đây là nơi gây ra vi phạm Setup $-0.1477\,\text{ns}$ vì transistor SS yếu, điện áp tụt còn $1.6\,\text{V}$, nhiệt độ sôi bỏng $100^\circ\text{C}$. Độ thiếu hụt chỉ là:
       $$\frac{0.1477}{13.0} \times 100\% \approx \mathbf{1.13\%}$$
       $\implies$ Bạn lập tức tính được tần số an toàn thực tế của thiết kế hiện tại mà không cần đoán mò:
       $$T_{\min} = 13.0 + 0.1477 = 13.1477\,\text{ns} \implies F_{\max} \approx \mathbf{76.06\,\text{MHz}}$$
    2. **Soi góc `min_ff_n40C_1v95` (Nhanh nhất):** Thấy `Hold WS = +2.3896ns > 0` $\implies$ Bạn thở phào nhẹ nhõm vì biết chắc chắn con chip không dính "lời nguyền biến thành cục gạch", hoàn toàn miễn nhiễm với lỗi Hold!

---

#### 💡 Vấn Đề 3: Định vị chính xác "thủ phạm" gây lỗi thuộc nhóm nào trong 4 Timing Paths
* **Nếu không có lý thuyết:** Khi thấy lỗi Setup, bạn không biết do phần nào: do bộ nhân, do chân Reset, do đường clock hay do ngõ ra?
* **Lý thuyết đã giải phóng bạn như thế nào?**
  * Mở file `violator_list.rpt`, bạn thấy đường trễ dài nhất xuất phát từ ngõ vào **`b[6]`** đi xuyên qua ma trận các bộ cộng nhân rồi kết thúc tại chân dữ liệu `D` của Flip-Flop **`_646_/D`**.
  * Dựa vào **Bảng phân loại Chân & Khối của 4 Timing Paths (Phần V.1)**, bạn chỉ thẳng mặt: **Đây chính là Path 1 (In2Reg)!**
  * Đầu vào `b[6]` là chân thuần tổ hợp ngoài chip (*Unregistered Input*), nó vừa phải gánh độ trễ $3.0\,\text{ns}$ từ bo mạch ngoài, vừa phải cõng nguyên một mạng logic nhân ma trận 8-bit cực kỳ nặng nề, khiến tín hiệu không thể tới chân `D` của `_646_` trước hạn chót $T_{\text{setup}}$.

---

#### 💡 Vấn Đề 4: Đưa ra quyết định sửa lỗi đúng đắn: "Ép Tool (DSE)" hay "Sửa Kiến Trúc (RTL)"?
* **Nếu không có lý thuyết:** Bạn chỉ biết bấm thử các nút trên tool một cách may rủi.
* **Lý thuyết đã giải phóng bạn như thế nào?**
  * **Giải pháp 1 (Dùng Tool DSE):** Bạn hiểu bản chất vì sao khi chọn `DELAY 1` đến `DELAY 4`, công cụ lại kéo được Slack lên $+1.082\,\text{ns}$ — vì nó tự động thay cell nhỏ thành cell to (Drive `_2`, `_4`), giảm trễ cổng $T_{\text{pd}}$ (Phần IV), nhưng cái giá phải trả là **diện tích Core phình to và ngốn điện hơn (PPA Trade-off)**.
  * **Giải pháp 2 (Sửa kiến trúc RTL - Pipelining):** Đây là đỉnh cao của kiến trúc sư! Bạn chủ động chèn thêm 2 thanh ghi đầu vào `a_p`, `b_p`. Bạn hiểu rằng việc này đã **chặt đứt đường Path 1 (In2Reg) nặng nề**, cô lập hoàn toàn $3.0\,\text{ns}$ input delay ở ngoài, biến toàn bộ bộ nhân thành **Path 2 (Reg2Reg nội bộ)**. Kết quả: Vừa sạch bóng lỗi Setup ($WNS = \mathbf{+1.530\,\text{ns}}$), vừa giữ nguyên được chiến lược nén diện tích tối đa `AREA 0` siêu nhỏ gọn!

---

> [!TIP]
> **Toàn bộ kế hoạch và tiến trình thực hành 5 giai đoạn của Lab 2:**  
> Đã được chuyển giao và cập nhật chi tiết theo thời gian thực tại sổ tay độc lập:  
> 👉 [Nhung_Kinh_Nghiem_Rut_Ra_Lab_2.md](file:///D:/Tapeout_chip/buoi_3/docs/Nhung_Kinh_Nghiem_Rut_Ra_Lab_2.md)

---

## 🏁 PHẦN VII: TỔNG KẾT BÀI HỌC & LỘ TRÌNH TIẾP THEO (BUỔI 4)

1. **Static Timing Analysis (STA)** là "tòa án tối cao" của quy trình thiết kế vi mạch. Nó không giả lập chức năng (Functional Simulation) mà kiểm tra toán học mọi kịch bản thời gian của mọi hạt electron trên tấm bán dẫn.
2. **Quy tắc sinh tử:** Phải dập tắt lỗi Hold ở góc `min_ff_n40C_1v95` bằng cách chèn Buffer vào Shortest Path; và tối ưu Setup ở góc `max_ss_100C_1v60` bằng cách chỉnh Synthesis Strategy hoặc sửa kiến trúc RTL Pipelining.
3. **Bước tiếp theo (Buổi 4):** Khóa học sẽ chính thức bước vào thế giới **Physical Design (Backend)** toàn diện:
   * **Floorplanning:** Cấp đất Core, khống chế Core Utilization và Aspect Ratio.
   * **Power Planning (PDN):** Dựng vòng đai nguồn VDD/VSS và các thanh kim loại Power Straps.
   * **Placement & CTS:** Xếp cell vào hàng và dựng cây xung nhịp Clock Tree cân bằng Skew.
   * **Detailed Routing:** Luồn các đường dây kim loại Nano và nghiệm thu DRC/LVS.

---

*Tài liệu giáo trình và báo cáo kỹ thuật được biên soạn và bảo chứng bởi Senior ASIC Tapeout Architect (Dự án RTL-to-GDSII Buổi 3).*
