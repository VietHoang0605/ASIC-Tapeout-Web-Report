# -*- coding: utf-8 -*-
import os, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
from build_helpers import convert_markdown_document

base_dir = r"D:\Tapeout_chip"
web_dir = r"D:\Tapeout_chip\Web_Report"
output_js = os.path.join(web_dir, "report_data.js")

# Helper to read file safely
def read_text(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

# =============================================================================
# 1. COMPOSE BUỔI 01
# =============================================================================
print("Processing Buổi 01 data...")

# A. Materials: Giao_Trinh_Ly_Thuyet_Buoi_0.md
b1_mat_raw = read_text(os.path.join(base_dir, r"Buoi_1\docs\Giao_Trinh_Ly_Thuyet_Buoi_0.md"))
b1_mat_html, b1_mat_toc = convert_markdown_document(b1_mat_raw, "b1-mat")

# B. Lab Guide: Tapeout_LAB0.pdf summary + Code + Schematics
counter_v = read_text(os.path.join(base_dir, r"Buoi_1\counter.v"))
counter_tb_v = read_text(os.path.join(base_dir, r"Buoi_1\counter_tb.v"))

b1_lab_raw = r"""# BÀI HƯỚNG DẪN THỰC HÀNH LAB 0: SỬA FLOW FLOORPLANNING & MẠCH COUNTER 8-BIT
*(Tài liệu chuẩn hóa từ Tapeout_LAB0.pdf & Kho mã nguồn Buổi 1)*

---

## 1. MỤC TIÊU VÀ NỘI DUNG TRỌNG TÂM LAB 0
1. **Làm quen môi trường CTW SEMI Web Cockpit:** Điều khiển chuỗi công cụ EDA mã nguồn mở (Yosys, OpenROAD, OpenSTA, Magic, KLayout) đóng gói trong Docker container trên nền Ubuntu WSL2.
2. **Khởi tạo và chạy dự án mẫu SPM (Serial-Parallel Multiplier):** Kiểm tra tính sẵn sàng của hệ sinh thái công cụ (PDK `sky130A`, thư viện tế bào `sky130_fd_sc_hd`).
3. **Mô phỏng Front-End bằng Icarus Verilog & GTKWave:** Xác minh chức năng đếm nhịp của khối `counter.v` bằng giản đồ xung trực quan `dump.vcd`.
4. **Hiện thực hóa quy trình RTL-to-GDSII trên mạch Counter 8-bit:** Phát hiện, định vị nguyên nhân và xử lý triệt để lỗi vi phạm Detailed Placement `DPL-0036` tại trạm dừng `OpenROAD.ResizerTimingPostCTS`.

---

## 2. KHO MÃ NGUỒN THIẾT KẾ & TESTBENCH

### 2.1 Mã nguồn RTL: Bộ đếm đồng bộ 8-bit (`counter.v`)
```verilog
__COUNTER_V__
```

### 2.2 Testbench kiểm thử chức năng & Xuất dạng sóng (`counter_tb.v`)
```verilog
__COUNTER_TB_V__
```

---

## 3. THƯ VIỆN SƠ ĐỒ NGUYÊN LÝ & BẢN VẼ BỐ TRÍ SILICON

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">RTL SCHEMATIC</span>
    <span class="badge-status">SƠ ĐỒ NGUYÊN LÝ MỨC THANH GHI</span>
  </div>
  <img src="images/counter_schematic.svg" alt="RTL Schematic Counter 8-bit" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Kiến trúc 8-bit Synchronous Counter</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">GATE-LEVEL NETLIST SCHEMATIC</span>
    <span class="badge-status">31 TẾ BÀO CHUẨN SKY130 HD</span>
  </div>
  <img src="images/counter_gate_level_schematic.svg" alt="Gate Level Schematic Counter 8-bit" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>8 D-Flip-Flop (dfxtp_2) + 23 Cổng Logic Tổ Hợp</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">FLOORPLAN ARCHITECTURE</span>
    <span class="badge-status">QUY HOẠCH DIE AREA & CORE AREA</span>
  </div>
  <img src="images/floorplan_architecture.svg" alt="Floorplan Architecture" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Ranh giới Die vs Core & Vành đai nguồn PDN</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">3D SILICON RENDER</span>
    <span class="badge-status">MÔ HÌNH CHIP ĐÚC THỰC TẾ GDSII</span>
  </div>
  <img src="images/counter_chip_render.png" alt="3D Silicon Chip Render" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Kết quả Tapeout hoàn chỉnh trên tiến trình SkyWater 130nm</span>
  </div>
</div>

---

## 4. QUY TRÌNH THAO TÁC LAB 0 CHI TIẾT
1. **Thiết lập công cụ (Setup Tab):**
   * Tải PDK `sky130A` tại tab Tools.
   * Chọn Design: `counter`, SCL: `sky130_fd_sc_hd`.
2. **Kiểm tra Front-End (RTL IDE):**
   * Chạy Linting cú pháp Verilog.
   * Chạy Simulation qua Iverilog, mở Waveform xác nhận biến `count[7:0]` nhảy từ `0x00 -> 0x01 -> 0x02`.
3. **Thực thi Pipeline (Full Auto Run):**
   * Nhấn `Run` và theo dõi quá trình chạy tự động từ Synthesis qua Floorplan, Placement, CTS và Routing.
   * Ghi nhận và phân tích hiện tượng lỗi đỏ tại `OpenROAD.ResizerTimingPostCTS`.
""".replace("__COUNTER_V__", counter_v).replace("__COUNTER_TB_V__", counter_tb_v)
b1_lab_html, b1_lab_toc = convert_markdown_document(b1_lab_raw, "b1-lab")

# C. Student Report: Lab0_Ghi_Chep_Kien_Thuc.md + Chuyen_Sau_Hoi_Dap_ASIC.md
b1_rep1_raw = read_text(os.path.join(base_dir, r"Buoi_1\docs\Lab0_Ghi_Chep_Kien_Thuc.md"))
b1_rep2_raw = read_text(os.path.join(base_dir, r"Buoi_1\docs\Chuyen_Sau_Hoi_Dap_ASIC.md"))
b1_rep_full = b1_rep1_raw + "\n\n---\n\n" + b1_rep2_raw
b1_rep_html, b1_rep_toc = convert_markdown_document(b1_rep_full, "b1-rep")

# =============================================================================
# 2. COMPOSE BUỔI 02
# =============================================================================
print("Processing Buổi 02 data...")

# A. Materials: Giao_Trinh_Ly_Thuyet_Buoi_2.md
b2_mat_raw = read_text(os.path.join(base_dir, r"buoi_2\docs\Giao_Trinh_Ly_Thuyet_Buoi_2.md"))
b2_mat_html, b2_mat_toc = convert_markdown_document(b2_mat_raw, "b2-mat")

# B. Lab Guide: Tapeout_LAB1.pdf summary + SVGs + capnhatctwsemi.txt
capnhat_txt = read_text(os.path.join(base_dir, r"buoi_2\docs\capnhatctwsemi.txt"))

b2_lab_raw = r"""# BÀI HƯỚNG DẪN THỰC HÀNH LAB 1: SYNTHESIS & STANDARD CELLS (KHẢO SÁT MẠCH RCA 8-BIT)
*(Tài liệu chuẩn hóa từ Tapeout_LAB1.pdf & Kho tài nguyên sky130Examples)*

---

## 1. MỤC TIÊU VÀ CÂU HỎI TRUNG TÂM BÀI LAB 1
* **Câu hỏi trung tâm:** *ABC chọn cell dựa vào đâu và người thiết kế có thể tự chọn cell hay không?*
* **Mục tiêu thực hành:**
  1. Giải thích được vì sao hai lần tổng hợp trên cùng một đoạn mã nguồn RTL Verilog lại tạo ra các tập hợp Standard Cells hoàn toàn khác nhau.
  2. Phân biệt việc định hướng mapper (`SYNTH_STRATEGY`, `SYNTH_HIERARCHY_MODE`) với việc ép một cell cụ thể (`Manual Instantiation`).
  3. Khảo sát định lượng trên mạch Bộ cộng lan truyền 8-bit (**8-bit Ripple Carry Adder - RCA**) qua 8 cấu hình chiến lược để lập bảng ma trận so sánh Diện tích (Area) và Độ trễ (Delay).

---

## 2. KIẾN TRÚC MẠCH VÀ SƠ ĐỒ TỔNG HỢP LOGIC

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">SYNTHESIS FLOW</span>
    <span class="badge-status">YOSYS FRONTEND &amp; ABC TECHNOLOGY MAPPER</span>
  </div>
  <img src="images/yosys_abc_pipeline.svg" alt="Yosys & ABC Synthesis Flow" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Từ Verilog trừu tượng qua Generic Gates đến Standard Cells Sky130</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">LIBERTY (.LIB)</span>
    <span class="badge-status">7 THUỘC TÍNH CỐT TỬ CỦA TẾ BÀO CHUẨN</span>
  </div>
  <img src="images/liberty_7_attributes.svg" alt="7 Thuộc tính Liberty" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Mắt thần của ABC: Boolean, Area, Timing NLDM, Capacitance</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">RCA ARCHITECTURE</span>
    <span class="badge-status">8-BIT RIPPLE CARRY ADDER &amp; CRITICAL PATH</span>
  </div>
  <img src="images/rca_8bit_architecture.svg" alt="Kiến trúc bộ cộng RCA 8-bit" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Phân tích đường trễ tới hạn bò tuần tự qua 8 tầng Full Adder</span>
  </div>
</div>

---

## 3. THIẾT LẬP MÔI TRƯỜNG & NÂNG CẤP CONTAINER DOCKER

### Script nâng cấp môi trường kích hoạt Schematic Viewer (`capnhatctwsemi.txt`)
```bash
__CAPNHAT_TXT__
```

---

## 4. QUY TRÌNH THỰC HIỆN 2 THÍ NGHIỆM LAB 1
1. **Thí nghiệm 1: Khảo sát 8 Chiến lược Tổng hợp (Synthesis Strategies)**
   * Chạy mạch `rca.v` qua các cấu hình: `AREA 0`, `AREA 1`, `AREA 2`, `AREA 3`, `DELAY 0`, `DELAY 1`, `DELAY 2`, `DELAY 3`.
   * Ghi nhận Diện tích ($S_{\text{cells}}\,\mu m^2$), Độ trễ tới hạn ($t_{pd}\,\text{ns}$), và tổng số lượng cell.
2. **Thí nghiệm 2: Ép Cell Thủ công (Manual Instantiation) vs Tự động hóa**
   * Thay thế phép toán cộng trừu tượng `+` bằng việc instantiate trực tiếp tế bào `sky130_fd_sc_hd__fa_1` trong Verilog.
   * Nhận xét tính phụ thuộc công nghệ và sự suy giảm quyền năng tối ưu hóa của công cụ EDA.
""".replace("__CAPNHAT_TXT__", capnhat_txt)
b2_lab_html, b2_lab_toc = convert_markdown_document(b2_lab_raw, "b2-lab")

# C. Student Report: Lab1_Ghi_Chep_Kien_Thuc.md + Ke_Hoach_Chinh_Phuc_Lab1.md
b2_rep1_raw = read_text(os.path.join(base_dir, r"buoi_2\docs\Lab1_Ghi_Chep_Kien_Thuc.md"))
b2_rep2_raw = read_text(os.path.join(base_dir, r"buoi_2\docs\Ke_Hoach_Chinh_Phuc_Lab1.md"))
b2_rep_full = b2_rep1_raw + "\n\n---\n\n" + b2_rep2_raw
b2_rep_html, b2_rep_toc = convert_markdown_document(b2_rep_full, "b2-rep")

# =============================================================================
# 3. COMPOSE BUỔI 03 (STATIC TIMING ANALYSIS & REGISTERED MULTIPLIER)
# =============================================================================
print("Processing Buổi 03 data...")

# A. Materials: Giao_Trinh_STA_Timing_Closure_Buoi_3.md
b3_mat_raw = read_text(os.path.join(base_dir, r"buoi_3\docs\Giao_Trinh_STA_Timing_Closure_Buoi_3.md"))
b3_mat_html, b3_mat_toc = convert_markdown_document(b3_mat_raw, "b3-mat")

# B. Lab Guide: Tapeout_LAB2.pdf summary + SDC + Verilog + Visual Proofs
mult_v_code = read_text(os.path.join(base_dir, r"buoi_3\docs\mult.v"))
mult_sdc_code = read_text(os.path.join(base_dir, r"buoi_3\docs\mult.sdc"))
mult_post_pnr_sdc_code = read_text(os.path.join(base_dir, r"buoi_3\docs\mult_post_pnr.sdc"))
violator_rpt = read_text(os.path.join(base_dir, r"buoi_3\docs\violator_list_phase_2.rpt"))

b3_lab_raw = r"""# BÀI HƯỚNG DẪN THỰC HÀNH LAB 2: STATIC TIMING ANALYSIS (STA) & TIMING CLOSURE
*(Tài liệu chuẩn hóa chính thức từ Tapeout_LAB2.pdf, Slide Buổi 3 & Báo cáo OpenROAD Post-PnR)*

---

## 1. MỤC TIÊU VÀ TRIẾT LÝ BÀI LAB 2
* **Mục tiêu thực hành cốt tử:**
  1. Sau bài lab, học viên phải **phân tích được thời gian tĩnh sau bước Place and Route (PnR)** trên thiết kế thực tế `mult`.
  2. Phân tích chính xác các vi phạm thời gian (**Timing Violations**) xảy ra tại những đường nào, thuộc nhóm nào (`In2Reg`, `Reg2Reg`, `Reg2Out`).
  3. Tìm ra và làm chủ **2 hướng giải quyết chuẩn công nghiệp** để đạt được tần số hoạt động mong muốn:
     * **Phương pháp 1 (Công cụ):** Tối ưu hóa bằng quét không gian thiết kế **DSE (Design Space Exploration)** với các chiến lược `DELAY 1` đến `DELAY 4`.
     * **Phương pháp 2 (Kiến trúc):** Tái cấu trúc vi kiến trúc bằng kỹ thuật **RTL Pipelining (Fully Registered Multiplier)** để đóng timing closure triệt để với diện tích tối thiểu.
* **Triết lý Signoff từ chuyên gia:**
  > [!IMPORTANT]
  > *"Không phải cứ có vi phạm về timing là con chip không chạy được! Người kỹ sư Signoff phải nhìn thấu vi phạm đó xảy ra ở những góc nào (Corners). Một con chip thương mại cao cấp đòi hỏi pass $100\%$ mọi corners, nhưng chip demo hoặc giáo dục chỉ cần an toàn ở dải nhiệt độ phòng thông thường. Giá trị của con chip và đẳng cấp của kỹ sư nằm ở khả năng kiểm soát ma trận PVT Corners."*

---

## 2. CHUẨN BỊ MÔI TRƯỜNG & KHỞI TẠO DỰ ÁN TRÊN CTW SEMI COCKPIT

### 2.1 Các bước khởi tạo dự án Registered Multiplier
1. Tại giao diện chính của CTW SEMI Web Cockpit, chọn biểu tượng **"..."** ở góc phải trên cùng màn hình, nhấp chọn **Create new project**.
2. Tại bảng danh mục thiết kế mẫu, chọn ví dụ **Registered Multiplier**.
3. Thiết lập thông số môi trường:
   * **Project Name:** `mult`
   * **Target PDK:** `sky130A`
   * **Standard Cell Library (SCL):** `sky130_fd_sc_hd` (High Density)

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">CTW SEMI COCKPIT</span>
    <span class="badge-status">BƯỚC 1: MENU KHỞI TẠO DỰ ÁN MỚI</span>
  </div>
  <img src="images/lab2_create_project_menu.png" alt="Khởi tạo dự án mới trên CTW SEMI" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Thao tác tạo project từ template có sẵn của hệ thống</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">CTW SEMI COCKPIT</span>
    <span class="badge-status">BƯỚC 2: CẤU HÌNH DỰ ÁN REGISTERED MULTIPLIER</span>
  </div>
  <img src="images/lab2_registered_multiplier_settings.png" alt="Cấu hình dự án Registered Multiplier" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Lựa chọn thiết kế mẫu Bộ nhân 8-bit trên tiến trình SkyWater 130nm</span>
  </div>
</div>

---

## 3. MỔ XẺ MÃ NGUỒN RTL GỐC & KHẾ ƯỚC THỜI GIAN MẶC ĐỊNH (15.0ns / 66.67MHz)

### 3.1 Khảo sát kiến trúc vi mạch bộ nhân ban đầu
Mạch nhân ban đầu lấy ngõ vào $A[7:0]$ và $B[7:0]$ từ các chân Pin vật lý bên ngoài đưa thẳng vào khối nhân tổ hợp logic $8 \times 8$. Kết quả phép nhân được đưa qua bộ chọn kênh MUX (để xóa về 0 khi có tín hiệu `rst`), và đầu ra của MUX mới được chốt vào 16 D-Flip-Flop ngõ ra $P[15:0]$.
* **Điểm yếu cốt tử:** Thiết kế **chưa được Fully Registered** — Ngõ ra đã có thanh ghi chốt chặn, nhưng ngõ vào thì **hoàn toàn trần trụi**. Đường trễ dữ liệu từ ngoài chip (`input_delay`) sẽ cộng dồn trực tiếp với toàn bộ độ trễ của 12 tầng cổng logic nhân tổ hợp!

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">CIRCUIT SCHEMATIC</span>
    <span class="badge-status">KIẾN TRÚC VI MẠCH BỘ NHÂN REGISTERED MULTIPLIER LAB 2</span>
  </div>
  <img src="images/kien_truc_bo_nhan_mult_lab2.svg" alt="Kiến trúc bộ nhân 8-bit Lab 2" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Phân tích đường tín hiệu từ Input A/B qua khối nhân tổ hợp đến Flip-Flop ngõ ra P</span>
  </div>
</div>

### 3.2 Khế ước thời gian SDC ban đầu (`mult.sdc`)
Khế ước thời gian định nghĩa chu kỳ xung nhịp $T_{\text{clk}} = 15.0\,\text{ns}$ ($f = 66.67\,\text{MHz}$), dự phòng bất định $0.25\,\text{ns}$, sườn dốc $0.15\,\text{ns}$, trễ ngõ vào ngoài chip $3.0\,\text{ns}$ và trễ tải ngoài bo mạch $3.0\,\text{ns}$:

```tcl
__MULT_SDC__
```

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">CONFIGURATION</span>
    <span class="badge-status">CẤU HÌNH CLOCK PERIOD 15.0ns TRONG CONFIG.JSON</span>
  </div>
  <img src="images/lab2_config_json_clock.png" alt="Cấu hình chu kỳ Clock trong config.json" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Chu kỳ 15ns tương ứng với tần số 66.67 MHz đạt mốc chuẩn an toàn</span>
  </div>
</div>

### 3.3 Nghiệm thu kết quả Mốc Chuẩn Vàng (Baseline 15.0ns)
Khi chạy quy trình với chu kỳ $15.0\,\text{ns}$, công cụ OpenROAD hoàn thành toàn bộ luồng PnR mà không xuất hiện bất kỳ vi phạm nào:
* **Setup Worst Slack (WNS):** $+1.4523\,\text{ns}$ (Dương an toàn tại corner khắc nghiệt nhất `max_ss_100C_1v60`).
* **Hold Worst Slack:** $+2.9096\,\text{ns}$ (Dương an toàn tuyệt đối).
* **Setup/Hold Violations:** $0$ lỗi trên toàn bộ các góc bán dẫn.

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">OPENROAD STA REPORT</span>
    <span class="badge-status">BÁO CÁO SUMMARY.RPT MỐC CHUẨN VÀNG 15.0ns</span>
  </div>
  <img src="images/summary_rpt_phase_1.png" alt="Báo cáo STA giai đoạn 1 mốc 15ns" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Toàn bộ 9 góc PVT corners đều có Slack dương, thiết kế đạt chuẩn xuất xưởng</span>
  </div>
</div>

---

## 4. THỰC NGHIỆM ÉP XUNG XUỐNG 13.0ns (76.92MHz) & BẮT QUẢ TANG LỖI SETUP

### 4.1 Thao tác ép xung trên hệ thống
Theo bài giảng Buổi 3, chu kỳ $15\,\text{ns}$ chạy rất an toàn. Để kiểm tra giới hạn chịu đựng của vi mạch và phát hiện điểm gãy timing, ta tiến hành "ép xung" bằng cách:
1. Mở file `config.json`, chỉnh sửa tham số: `"CLOCK_PERIOD": 13.0`.
2. Bấm nút **Run** để khởi chạy lại toàn bộ flow RTL-to-GDSII.

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">CTW SEMI COCKPIT</span>
    <span class="badge-status">THỰC THI TOÀN BỘ FLOW VỚI CHU KỲ 13.0ns</span>
  </div>
  <img src="images/lab2_run_flow_btn.png" alt="Nút bấm Run flow trên CTW SEMI" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Khởi động quy trình tự động từ Synthesis qua Placement, CTS đến Post-PnR STA</span>
  </div>
</div>

### 4.2 Định vị và mở file báo cáo STA sau PnR (`openroad-stapostpnr`)
Sau khi flow hoàn thành, truy cập vào menu: **Runs** $\to$ **Files** $\to$ tìm thư mục theo tên **`openroad-stapostpnr`** (lưu ý quan trọng từ Lab guide: *phải chọn theo tên bước chứ không chọn theo số thứ tự, vì mỗi flow có tổng số bước chạy khác nhau*).

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">OPENROAD FLOW</span>
    <span class="badge-status">ĐỊNH VỊ THƯ MỤC KẾT QUẢ OPENROAD-STAPOSTPNR</span>
  </div>
  <img src="images/lab2_runs_stapostpnr_menu.png" alt="Vị trí thư mục openroad-stapostpnr" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Thư mục chứa toàn bộ báo cáo phân tích thời gian tĩnh sau PnR</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">UBUNTU TERMINAL</span>
    <span class="badge-status">LỆNH TRA CỨU BÁO CÁO NHANH QUA DÒNG LỆNH</span>
  </div>
  <img src="images/lab2_corners_terminal_view.png" alt="Tra cứu báo cáo terminal trong Ubuntu" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Xem file summary.rpt trực tiếp mà không bị lệch cột trên giao diện web</span>
  </div>
</div>

---

## 5. GIẢI MÃ MA TRẬN 9 GÓC PVT CORNERS & MỔ XẺ ĐƯỜNG TRỄ TỚI HẠN

### 5.1 Ý nghĩa vật lý của 9 góc bán dẫn (Corners)
Trong sản xuất chip thực tế, các thông số về Quy trình chế tạo (**Process**), Điện áp cấp nguồn (**Voltage**) và Nhiệt độ môi trường (**Temperature**) luôn dao động. Nhà máy đúc wafer cung cấp ma trận 9 góc để kiểm thử toàn diện:

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">PVT CORNERS MATRIX</span>
    <span class="badge-status">BẢNG Ý NGHĨA VẬT LÝ &amp; RỦI RO CỦA 9 GÓC BÁN DẪN</span>
  </div>
  <img src="images/lab2_corners_definition_table.png" alt="Bảng giải mã 9 góc PVT corners" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>So sánh điều kiện danh định (Nominal), cực nhanh (Fast) và cực chậm (Slow)</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">INDUSTRIAL EVIDENCE</span>
    <span class="badge-status">MINH CHỨNG THỰC TẾ: DẢI NHIỆT ĐỘ SOM K26 XILINX</span>
  </div>
  <img src="images/lab2_som_k26_temp_range.png" alt="Phạm vi hoạt động nhiệt độ SOM K26 Xilinx" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Càng hoạt động ở môi trường nhiệt độ khắc nghiệt thì chip càng đắt tiền</span>
  </div>
</div>

### 5.2 Phân tích hiện trường vi phạm Setup tại góc `max_ss_100C_1v60`
Khi chu kỳ bị bóp nghẹt từ $15\,\text{ns}$ xuống $13\,\text{ns}$, báo cáo `summary.rpt` gióng lên hồi chuông báo động đỏ:
* **Worst Negative Slack (WNS):** $-0.1477\,\text{ns}$ (Vi phạm Setup âm).
* **Total Negative Slack (TNS):** $-0.1766\,\text{ns}$.
* **Setup Violation Count:** $3$ đường bị vi phạm.
* **Quan sát sống còn:** Lỗi Setup **CHỈ XẢY RA** ở góc `max_ss_100C_1v60` (WNS = $-0.1477\,\text{ns}$) và `nom_ss_100C_1v60` (WNS = $-0.0710\,\text{ns}$). Tại góc nhiệt độ phòng `nom_tt_025C_1v80`, Slack vẫn **DƯƠNG RẤT LỚN ($+4.9902\,\text{ns}$)**!
  * *Nghĩa là: Nếu đem con chip này ra đo đạc trong phòng thí nghiệm máy lạnh $25^\circ\text{C}$, nó vẫn chạy trơn tru ở $77\,\text{MHz}$. Nhưng khi lắp vào xe hơi hay thiết bị ngoài trời nóng $100^\circ\text{C}$ kèm sụt áp $1.60\text{V}$, chip sẽ lập tức gặp lỗi tính toán sai!*

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">OPENROAD STA REPORT</span>
    <span class="badge-status">BÁO CÁO SUMMARY.RPT BẮT QUẢ TANG VI PHẠM SETUP TẠI 13.0ns</span>
  </div>
  <img src="images/summary_rpt_phase_2.png" alt="Báo cáo STA giai đoạn 2 ép xung 13ns" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Lỗi vi phạm tập trung chính xác tại góc max_ss_100C_1v60</span>
  </div>
</div>

### 5.3 Mổ xẻ chi tiết danh sách đường vi phạm (`violator_list.rpt`) và `max.rpt`
Mở file `violator_list.rpt` để truy tìm danh tính thủ phạm:
```text
===========================================================================
Violator List
============================================================================
[setup in-reg] b[6] -> _646_/D : -0.147699
[setup in-reg] b[6] -> _645_/D : -0.028915
```

> [!CAUTION]
> **Phát hiện chấn động từ Kiến trúc sư:** Ký hiệu `[setup in-reg]` chỉ ra rằng đường vi phạm không phải là đường nội bộ giữa 2 Flip-Flop (`Reg2Reg`), mà là đường **Input-to-Register (`In2Reg`)** xuất phát từ chân ngõ vào ngoài chip `b[6]` chạy xuyên suốt qua khối nhân tổ hợp để đến chân $D$ của Flip-Flop `_646_`!

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">CRITICAL PATH TRACING</span>
    <span class="badge-status">MỔ XẺ ĐƯỜNG TRỄ TỚI HẠN CRITICAL PATH TRONG MAX.RPT</span>
  </div>
  <img src="images/lab2_max_rpt_critical_path.png" alt="Đường trễ tới hạn trong max.rpt" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Tín hiệu bò qua 12 tầng logic với tổng thời gian đến là 12.3977ns vượt mức trần 12.25ns</span>
  </div>
</div>

---

## 6. THÍ NGHIỆM 1: SỬA LỖI BẰNG CÔNG CỤ DSE SWEEP (DELAY 1 ĐẾN DELAY 4)

### 6.1 Thiết lập quét không gian thiết kế DSE (Design Space Exploration)
Phương pháp đầu tiên học viên được hướng dẫn là **sử dụng quyền năng của công cụ EDA** để tự động tái cấu trúc netlist và thay đổi kích thước cổng logic (Gate Sizing):
1. Tại Web Cockpit, chọn tính năng **DSE Sweep**.
2. Nhấp **Add axis**, chọn biến `SYNTH_STRATEGY`.
3. Nhập lần lượt 4 giá trị: `DELAY 1`, `DELAY 2`, `DELAY 3`, `DELAY 4` (viết liền không dấu gạch nối).
4. Bấm **Run sweep** và chờ hệ thống chạy song song 4 luồng RTL-to-GDSII độc lập.

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">DSE CONFIGURATION</span>
    <span class="badge-status">CẤU HÌNH QUÉT 4 CHIẾN LƯỢC DELAY TRÊN CTW SEMI</span>
  </div>
  <img src="images/lab2_dse_sweep_config.png" alt="Cấu hình DSE sweep trên CTW SEMI" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Thao tác thêm trục biến SYNTH_STRATEGY để công cụ tự động khám phá</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">DSE RUNS</span>
    <span class="badge-status">DANH SÁCH 4 TIẾN TRÌNH DSE HOÀN THÀNH</span>
  </div>
  <img src="images/lab2_dse_runs_list.png" alt="Danh sách các lần chạy DSE sweep" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>4 thư mục kết quả độc lập tương ứng với DELAY 1, 2, 3, 4</span>
  </div>
</div>

### 6.2 Kết quả đo đạc & Biểu đồ Pareto (Cell Area vs Setup WNS)
Sau khi hoàn thành cả 4 runs, nhấp chọn **View metrics & plots**. Hệ thống tự động vẽ biểu đồ Pareto đa mục tiêu:

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">DSE PARETO METRICS</span>
    <span class="badge-status">BIỂU ĐỒ PARETO ĐỐI CHUẨN DIỆN TÍCH (AREA) VS SETUP WNS</span>
  </div>
  <img src="images/dse_sweep_results_phase_3.png" alt="Biểu đồ Pareto DSE Sweep Phase 3" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Trục hoành là Cell Area (µm²), trục tung là Setup WNS (ns)</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">SYNTHESIS LOG</span>
    <span class="badge-status">BÁO CÁO CÔNG CỤ ABC CỦA LƯỢT CHẠY DELAY 3 (WNS = +1.082ns)</span>
  </div>
  <img src="images/lab2_delay3_synthesis_log.png" alt="Báo cáo tổng hợp ABC DELAY 3" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Cấu hình DELAY 3 đạt biên an toàn lớn nhất nhưng diện tích phình to nhất</span>
  </div>
</div>

### 6.3 Phân tích tư duy đánh đổi PPA (Performance - Power - Area)
* **Kết luận nghiệm thu:** Cả 4 cấu hình `DELAY 1`, `DELAY 2`, `DELAY 3`, `DELAY 4` đều cho Setup TNS = $0$ và Setup WNS $> 0$. Thiết kế đã **Timing Closure thành công ở $13.0\,\text{ns}$**.
* **Nên chọn Strategy nào?**
  * Nếu chọn `DELAY 3`: WNS đạt mức cực đại $+1.082\,\text{ns}$, nhưng diện tích tế bào phình to lên tới $1386.63\,\mu\text{m}^2$ (tăng $17.1\%$ so với mốc gốc).
  * **Lựa chọn tối ưu PPA là `DELAY 1`:** Diện tích chỉ tốn $1254.49\,\mu\text{m}^2$ (chỉ tăng $5.9\%$) mà vẫn dư dả biên an toàn thời gian WNS = $+0.785\,\text{ns}$. Đây là bài học thực tế về việc không lãng phí tài nguyên silicon để lấy những biên an toàn không cần thiết!

---

## 7. THÍ NGHIỆM 2: ĐỈNH CAO KIẾN TRÚC — SỬA MÃ RTL PIPELINING

### 7.1 Tại sao kỹ sư giỏi thích sửa RTL hơn là để Tool gánh?
Việc dùng DSE ép công cụ sửa timing thực chất là ép ABC nhồi nhét các tế bào kích thước lớn (`drive strength 2`, `4`), làm tăng mật độ dòng rò và tiêu tốn nhiều năng lượng. Một kiến trúc sư vi mạch đích thực sẽ **giải quyết triệt để vấn đề ngay từ cấp độ kiến trúc RTL (Architecture-Level Optimization)**.

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">VERILOG RTL ANALYSIS</span>
    <span class="badge-status">MÃ NGUỒN GỐC CHƯA CHỐT THANH GHI ĐẦU VÀO</span>
  </div>
  <img src="images/lab2_rtl_unregistered_code.png" alt="Mã nguồn Verilog ban đầu" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Đầu vào A và B đi thẳng vào mạch nhân làm cho đường In2Reg bị quá tải</span>
  </div>
</div>

### 7.2 Hiện thực hóa kỹ thuật Pipelining (Chốt thanh ghi ngõ vào)
Ta tiến hành sửa đổi mã nguồn Verilog trong file `mult.v`, bổ sung 16 D-Flip-Flop đệm ngõ vào `a_p` và `b_p`:

```verilog
// NxN registered multiplier with registered inputs (Pipelining Stage 1)
// Fully Registered Design: Cả đầu vào và đầu ra đều được chốt thanh ghi
module mult #(
    parameter W = 8
) (
    input  wire           clk,
    input  wire           rst,
    input  wire [W-1:0]   a,
    input  wire [W-1:0]   b,
    output reg  [2*W-1:0] p
);
    // Khai báo 16 D-FF đệm đầu vào (Input Pipeline Registers)
    reg [W-1:0] a_p, b_p;

    always @(posedge clk) begin
        if (rst) begin
            p   <= {(2*W){1'b0}};
            a_p <= {W{1'b0}};
            b_p <= {W{1'b0}};
        end else begin
            a_p <= a;         // Chặng 1: Chốt đầu vào (Path 1: In2Reg - Cực ngắn, triệt tiêu input delay)
            b_p <= b;
            p   <= a_p * b_p; // Chặng 2: Nhân thuần túy Reg2Reg nội bộ (Path 2: Reg2Reg)
        end
    end
endmodule
```

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">VERILOG RTL CODE</span>
    <span class="badge-status">MÃ NGUỒN CẢI TIẾN ÁP DỤNG KỸ THUẬT PIPELINING</span>
  </div>
  <img src="images/lab2_rtl_pipelining_code.png" alt="Mã nguồn RTL sau khi sửa Pipelining" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Thêm 16 thanh ghi đệm ngõ vào tách biệt hoàn toàn đường In2Reg và Reg2Reg</span>
  </div>
</div>

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">PIPELINED ARCHITECTURE</span>
    <span class="badge-status">SƠ ĐỒ VI KIẾN TRÚC MẠCH SAU KHI SỬA RTL PIPELINING</span>
  </div>
  <img src="images/lab2_pipelining_schematic.png" alt="Sơ đồ kiến trúc Pipelining sau khi sửa" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Cấu trúc 2 tầng thanh ghi cách ly hoàn toàn trễ ngoài chip</span>
  </div>
</div>

### 7.3 Nghiệm thu lâm sàng kết quả chạy `mult-run-13ns-fixRTL`
Chạy lại thiết kế đã sửa RTL với cấu hình tối ưu diện tích **`AREA 0`** (vốn là cấu hình bị vi phạm nặng nhất ở thiết kế cũ). Kết quả trả về đẹp hoàn hảo:
* **Lỗi vi phạm Setup:** **HẾT SẠCH $100\%$!**
* **Setup Worst Slack:** Đạt **$+1.5302\,\text{ns}$** (thậm chí theo file log chi tiết đạt tới $+2.709\,\text{ns}$)! Biên an toàn thời gian cao gấp đôi so với phương pháp sửa bằng Tool DSE.
* **Diện tích tối ưu vượt trội:** Do dùng chiến lược `AREA 0`, toàn bộ logic nhân bên trong sử dụng tế bào diện tích nhỏ nhất. Diện tích tổng thể chỉ tăng thêm một lượng rất nhỏ do phát sinh thêm 16 tế bào Flip-Flop ngõ vào.

<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">OPENROAD STA REPORT</span>
    <span class="badge-status">BÁO CÁO SUMMARY.RPT MULT-RUN-13NS-FIXRTL SẠCH BÓNG LỖI</span>
  </div>
  <img src="images/summary_rpt_phase_4.png" alt="Báo cáo STA giai đoạn 4 sửa RTL" class="responsive-diagram-img" />
  <div class="diagram-card-footer">
    <span>Nhấp chuột vào hình để phóng to toàn màn hình</span>
    <span>Setup Slack dương tới +1.5302ns trên mọi corner, diện tích đạt chuẩn tối ưu</span>
  </div>
</div>

---

## 8. BẢNG ĐỐI CHUẨN MASTER PPA TOÀN DIỆN 5 KỊCH BẢN & KÝ DUYỆT TAPE-OUT

| Kịch Bản Thiết Kế | Chu Kỳ Xung Nhịp | Chiến Lược Tổng Hợp | Setup WNS (Corner max_ss) | Setup Vio Count | Diện Tích Cell ($S_{\text{cells}}$) | Đánh Giá Kỹ Thuật Sign-off |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Pha 1: Mốc Chuẩn Vàng (Baseline)** | $15.0\,\text{ns}$ ($66.7\,\text{MHz}$) | `AREA 0` (RTL gốc) | $+1.4523\,\text{ns}$ | $0$ | $1184.21\,\mu\text{m}^2$ | **PASS (ĐẠT CHUẨN):** Chạy an toàn nhưng tần số chưa tối ưu. |
| **Pha 2: Ép Xung Thất Bại** | $13.0\,\text{ns}$ ($76.9\,\text{MHz}$) | `AREA 0` (RTL gốc) | **$-0.1477\,\text{ns}$** | **$3$** | $1184.21\,\mu\text{m}^2$ | **FAIL (BÁO ĐỘNG ĐỎ):** Lỗi Setup trên đường `In2Reg`, cấm tapeout! |
| **Pha 3A: Sửa Bằng DSE DELAY 1** | $13.0\,\text{ns}$ ($76.9\,\text{MHz}$) | `DELAY 1` (Tool sửa) | $+0.7850\,\text{ns}$ | $0$ | $1254.49\,\mu\text{m}^2$ | **PASS:** Tối ưu tốt nhất nhóm DSE (Diện tích chỉ tăng $5.9\%$). |
| **Pha 3B: Sửa Bằng DSE DELAY 3** | $13.0\,\text{ns}$ ($76.9\,\text{MHz}$) | `DELAY 3` (Tool sửa) | $+1.0820\,\text{ns}$ | $0$ | $1386.63\,\mu\text{m}^2$ | **PASS:** WNS cao nhưng diện tích phình to ($+17.1\%$). |
| **Pha 4: Đỉnh Cao RTL Pipelining** | $13.0\,\text{ns}$ ($76.9\,\text{MHz}$) | **`AREA 0` (RTL Fix)** | **$+1.5302\,\text{ns}$** | **$0$** | **$1290.15\,\mu\text{m}^2$** | **QUÁN QUÂN TOÀN NĂNG (BEST PPA):** Biên an toàn cực đại, diện tích tiết kiệm, cấu trúc bền vững! |

> [!TIP]
> **Biên Bản Ký Duyệt Xuất Xưởng (Tape-out Sign-off Certificate):**
> Thiết kế mạch `mult_pipelined` hoàn toàn sạch bóng vi phạm Setup và Hold trên toàn bộ ma trận 9 góc PVT corners. Bản vẽ Layout vật lý sẵn sàng đóng gói GDSII để tích hợp vào khung truyền thông TinyTapeout / Efabless Caravel hướng tới đợt Shuttle Tape-out tiếp theo!
""".replace("__MULT_SDC__", mult_sdc_code)
b3_lab_html, b3_lab_toc = convert_markdown_document(b3_lab_raw, "b3-lab")

# C. Student Report: Nhung_Kinh_Nghiem_Rut_Ra_Lab_2.md
b3_rep_raw = read_text(os.path.join(base_dir, r"buoi_3\docs\Nhung_Kinh_Nghiem_Rut_Ra_Lab_2.md"))
b3_rep_html, b3_rep_toc = convert_markdown_document(b3_rep_raw, "b3-rep")

# =============================================================================
# 4. COMPOSE BUỔI 04 & 05 (LAB 3: PHYSICAL DESIGN, PnR & SIGN-OFF)
# =============================================================================
print("Processing Buổi 04 & 05 (Lab 3) data...")

# A. Materials: Cam_Nang_5_Buoc_Tim_Loi_Va_Dong_Timing_PnR.md
b4_mat_raw = read_text(os.path.join(base_dir, r"buoi_4+5\docs\Cam_Nang_5_Buoc_Tim_Loi_Va_Dong_Timing_PnR.md"))
b4_mat_html, b4_mat_toc = convert_markdown_document(b4_mat_raw, "b4-mat")

# B. Lab Guide: Summary from Tapeout_LAB3_extracted.txt & RTL_to_GDS_training_buoi4_extracted.txt
b4_lab_raw = r"""# BÀI HƯỚNG DẪN THỰC HÀNH LAB 3: PHYSICAL DESIGN, OPENROAD GUI, CVC64 GLS & GTKWAVE

*(Tổng hợp từ `Tapeout_LAB3.pdf` & Slide Buổi 4 `RTL_to_GDS_training_buoi4.pptx`)*

---

## 1. MỤC TIÊU BÀI LAB 3 (BUỔI 4 & BUỔI 5)

1. **Làm chủ kiến trúc lớp kim loại & Standard Cell SkyWater 130nm:** Phân biệt rạch ròi vai trò của `li1` (Local Interconnect), `met1` (ray nguồn `VPWR`/`VGND` và chân cell), `met2`–`met4` (định tuyến tín hiệu TinyTapeout), `met5` (lưới nguồn tổng PDN) cùng hiện tượng sụt áp `IR Drop` ($V_{\text{drop}} = I \cdot R$).
2. **Kiểm tra trạng thái chip qua từng file `.odb` (OpenROAD Database):** Biết cách liệt kê các snapshot `.odb` qua 72 bước của LibreLane/OpenROAD Flow và mở trực tiếp bất kỳ bước nào (`Step 29 Global Placement`, `Step 33 Repair Design`, `Step 38 Resizer Timing`, `Step 40 Detailed Routing`) trên giao diện đồ họa OpenROAD GUI.
3. **Thí nghiệm 1 (`cpu8bit` @ `50 MHz / 20 ns`):** Chẩn đoán nguyên nhân bùng nổ số lượng buffer sửa timing, kiểm tra bản đồ nhiệt mật độ đặt cell (*Placement Density Heatmap*) và rà soát Critical Path bằng Timing Report GUI / lệnh TCL.
4. **Thí nghiệm 2 (`TinyTDC` — Bộ đo thời gian Pico-giây):** Mô phỏng sau Layout (*Post-Layout Gate-Level Simulation*) bằng **CVC64** kèm file trễ ký sinh **SDF** và kiểm chứng từng đường trễ cell ở độ phân giải picosecond bằng **GTKWave**.

---

## 2. CÁC THÔNG SỐ NỀN TẢNG TRONG `config.json` & LỆNH MỞ `.ODB` TRÊN OPENROAD GUI

| Nhóm cấu hình | Biến trong `config.json` | Ý nghĩa kỹ thuật |
| :--- | :--- | :--- |
| **Khuôn chip & Core** | `DIE_AREA`, `FP_DEF_TEMPLATE`, `FP_SIZING`, `TOP_MARGIN_MULT` | Định nghĩa kích thước die vật lý, khung khuôn chuẩn (vd `1x1` TinyTapeout) và lề cách biên giữa Core và Die |
| **Xung nhịp & Timing** | `CLOCK_PERIOD`, `_HOLD_SLACK_MARGIN` | Chu kỳ xung nhịp mục tiêu (ns) và biên dự phòng an toàn sửa Hold Time |
| **Vật lý Placement & Routing** | `PL_TARGET_DENSITY_PCT`, `RT_MAX_LAYER` | Mật độ sắp xếp Standard Cell cho phép và lớp kim loại cao nhất được phép đi dây (`met4`) |
| **Nguồn & Thư viện** | `PDK`, `VDD_PIN`, `GND_PIN`, `VERILOG_FILES` | Chọn PDK `sky130A`, tên lưới nguồn/đất và danh sách mã nguồn RTL đầu vào |

### Lệnh liệt kê & khởi chạy OpenROAD GUI cho một bước `.odb` bất kỳ:

```bash
RUN="$HOME/ctwsemi-data/ips/cpu8bit/runs/cpu8bit-20ns"
find "$RUN" -type f -name '*.odb' -printf '%P\n' | sort -V | nl -w2 -s'. '

STEP="29-openroad-globalplacement"
ODB="$RUN/$STEP/tt_um_dvxf_dj8.odb"
OR_CID="$(docker ps --filter 'ancestor=ghcr.io/librelane/librelane:3.0.14' --format '{{.ID}}' | head -n 1)"
docker exec -d -e DISPLAY="$DISPLAY" "$OR_CID" openroad -gui -db "$ODB"
```
"""
b4_lab_html, b4_lab_toc = convert_markdown_document(b4_lab_raw, "b4-lab")

# C. Student Report: Bao_Cao_Tong_Hop_Physical_Design_Lab_3.md
b4_rep_raw = read_text(os.path.join(base_dir, r"buoi_4+5\docs\Bao_Cao_Tong_Hop_Physical_Design_Lab_3.md"))
b4_rep_html, b4_rep_toc = convert_markdown_document(b4_rep_raw, "b4-rep")

# =============================================================================
# 5. CONSTRUCT SESSIONS_DATA (BUỔI 1 + BUỔI 2 + BUỔI 3 + BUỔI 4&5)
# =============================================================================
sessions_data = [
    {
        "id": "buoi-01",
        "tabTitle": "BUỔI 01: PHYSICAL DESIGN & FLOORPLANNING (LAB 0)",
        "shortTitle": "Buổi 1: Nhập Môn & Lab 0",
        "date": "10/10/2026",
        "badge": "BUỔI 01",
        "icon": "🏗️",
        "summary": "Nhập môn quy trình thiết kế vi mạch số RTL to GDSII, thiết lập Docker CTW SEMI trên WSL2, kiểm thử sóng Iverilog và truy vết hiện trường lỗi Detailed Placement DPL-0036 trên mạch Counter 8-bit.",
        "downloads": [
            { "name": "1. Physical_Design_10_10_2026.mkv", "size": "1.79 GB", "type": "VIDEO", "icon": "🎥", "desc": "Video ghi lại toàn bộ buổi học trực tuyến ngày 10/10/2026" },
            { "name": "RTL_to_GDS_training.pptx", "size": "5.73 MB", "type": "SLIDES", "icon": "📊", "desc": "Slide bài giảng đào tạo Physical Design từ giảng viên" },
            { "name": "Tapeout_LAB0.pdf", "size": "3.20 MB", "type": "LAB GUIDE", "icon": "📕", "desc": "Tài liệu hướng dẫn thực hành Lab 0: Sửa Flow Floorplanning" },
            { "name": "counter.v & counter_tb.v", "size": "1.02 KB", "type": "VERILOG", "icon": "💻", "desc": "Mã nguồn Verilog và Testbench bộ đếm đồng bộ 8-bit" },
            { "name": "CTW_SEMI_Huong_dan_chay.docx", "size": "834 KB", "type": "DOCS", "icon": "📄", "desc": "Hướng dẫn khởi chạy chi tiết bộ công cụ CTW SEMI trên máy tính" }
        ],
        "subsections": [
            {
                "id": "b1-materials",
                "title": "Tài Liệu Buổi Học & Giáo Trình Nền Tảng (Buổi 0)",
                "category": "TÀI LIỆU BUỔI HỌC",
                "icon": "📚",
                "readTime": "12 phút",
                "summary": "Giáo trình lý thuyết toàn diện về 5 cấp độ trừu tượng, Front-End vs Back-End, sự khác biệt bản chất giữa FPGA vs ASIC, và các khái niệm cốt tử trong Physical Design (PDK Sky130, Standard Cells, Floorplan, Placement, CTS, Routing, Signoff).",
                "toc": b1_mat_toc,
                "htmlContent": b1_mat_html
            },
            {
                "id": "b1-lab-guide",
                "title": "Bài Hướng Dẫn Thực Hành Lab 0 & Thư Viện Mạch",
                "category": "BÀI HƯỚNG DẪN LAB 0",
                "icon": "🧪",
                "readTime": "10 phút",
                "summary": "Hướng dẫn từng bước làm chủ Web Cockpit CTW SEMI, nạp PDK, chạy dự án mẫu SPM, mô phỏng Iverilog/GTKWave, cùng thư viện sơ đồ mạch nguyên lý RTL, Gate-Level Netlist và bản vẽ 3D silicon chip.",
                "toc": b1_lab_toc,
                "htmlContent": b1_lab_html
            },
            {
                "id": "b1-student-report",
                "title": "Báo Cáo Thực Chiến Của Học Viên: Giải Mã Lỗi DPL-0036 & Sổ Tay ASIC",
                "category": "BÁO CÁO THỰC CHIẾN HỌC VIÊN",
                "icon": "🏆",
                "readTime": "18 phút",
                "summary": "Hồ sơ chuyên sâu của học viên về hiện trường lỗi DPL-0036 tại ResizerTimingPostCTS, giải mã mâu thuẫn hình học giữa Die Area vs Core Area, phân tích vì sao 7 Endpoints vi phạm Hold lại cần 9 Buffers, và chiến lược tối ưu file config.json.",
                "toc": b1_rep_toc,
                "htmlContent": b1_rep_html
            }
        ]
    },
    {
        "id": "buoi-02",
        "tabTitle": "BUỔI 02: RTL CODING, LOGIC SYNTHESIS & STANDARD CELLS (LAB 1)",
        "shortTitle": "Buổi 2: Synthesis & Lab 1",
        "date": "16/10/2026",
        "badge": "BUỔI 02",
        "icon": "🔬",
        "summary": "Làm chủ cỗ máy Yosys & ABC Technology Mapping, giải mã 7 thuộc tính sống còn trong file Liberty .lib, đánh đổi Area vs Delay và khảo sát bộ cộng RCA 8-bit.",
        "downloads": [
            { "name": "2. Physical_Design_16_10_2026.mkv", "size": "1.65 GB", "type": "VIDEO", "icon": "🎥", "desc": "Video ghi lại toàn bộ buổi học trực tuyến ngày 16/10/2026" },
            { "name": "RTL_to_GDS_training_buoi2.pptx", "size": "4.14 MB", "type": "SLIDES", "icon": "📊", "desc": "Slide bài giảng Buổi 2: RTL to GDS training" },
            { "name": "Tapeout_LAB1.pdf", "size": "2.52 MB", "type": "LAB GUIDE", "icon": "📕", "desc": "Tài liệu hướng dẫn thực hành Lab 1: Synthesis & Standard Cells" },
            { "name": "sky130Examples.zip", "size": "28.8 MB", "type": "PACKAGE", "icon": "📦", "desc": "Kho mã nguồn mẫu gồm 1.809 tệp tin cho Lab 1 và các thí nghiệm nâng cao" },
            { "name": "my_first_constraints.sdc", "size": "5.80 KB", "type": "SDC", "icon": "⏱️", "desc": "Khế ước ràng buộc thời gian thiết kế (Synopsys Design Constraints)" }
        ],
        "subsections": [
            {
                "id": "b2-materials",
                "title": "Tài Liệu Buổi Học & Giáo Trình Lý Thuyết Buổi 2",
                "category": "TÀI LIỆU BUỔI HỌC",
                "icon": "📚",
                "readTime": "15 phút",
                "summary": "Triết lý thực hành từ Kiến trúc sư Trưởng, bộ quy tắc viết code Synthesizable RTL, cỗ máy tổng hợp Yosys + ABC Engine, hiện tượng Glitch và kỹ thuật chặn đầu chặn đuôi bằng Flip-Flop, chiến lược Reset và 3 cạm bẫy Simulation Mismatch.",
                "toc": b2_mat_toc,
                "htmlContent": b2_mat_html
            },
            {
                "id": "b2-lab-guide",
                "title": "Bài Hướng Dẫn Thực Hành Lab 1 & Bộ Sơ Đồ Kiến Trúc",
                "category": "BÀI HƯỚNG DẪN LAB 1",
                "icon": "🧪",
                "readTime": "11 phút",
                "summary": "Đề bài và hướng dẫn thao tác Lab 1, script cập nhật container v1.0.1 kích hoạt Schematic Viewer, sơ đồ luồng tổng hợp logic Yosys+ABC, 7 thuộc tính file Liberty .lib và kiến trúc mạch bộ cộng Ripple Carry Adder 8-bit.",
                "toc": b2_lab_toc,
                "htmlContent": b2_lab_html
            },
            {
                "id": "b2-student-report",
                "title": "Báo Cáo Thực Chiến Của Học Viên: Khảo Sát RCA & Kế Hoạch Master Plan",
                "category": "BÁO CÁO THỰC CHIẾN HỌC VIÊN",
                "icon": "🏆",
                "readTime": "16 phút",
                "summary": "Báo cáo chuyên sâu của học viên về mắt thần ABC, phân tích bảng tra cứu trễ NLDM, 2 giới hạn nhận thức của ABC, bộ ba biến điều khiển SYNTH_STRATEGY, phân tích Critical Path của RCA 8-bit và lộ trình 5 chặng chinh phục Lab 1.",
                "toc": b2_rep_toc,
                "htmlContent": b2_rep_html
            }
        ]
    },
    {
        "id": "buoi-03",
        "tabTitle": "BUỔI 03: STATIC TIMING ANALYSIS (STA) & TIMING CLOSURE (LAB 2)",
        "shortTitle": "Buổi 3: STA Timing & Lab 2",
        "date": "18/10/2026",
        "badge": "BUỔI 03",
        "icon": "⏱️",
        "summary": "Làm chủ kỹ thuật phân tích thời gian tĩnh Static Timing Analysis (STA), bản chất vật lý của Setup time và Hold time, mô hình thanh ghi FF-to-FF, ma trận 9 góc PVT corners, và 2 giải pháp đóng gói Timing Closure (DSE sweep vs RTL Pipelining) trên bộ nhân Registered Multiplier.",
        "downloads": [
            { "name": "3. Physical_Design_18_10_2026.mkv", "size": "1.69 GB", "type": "VIDEO", "icon": "🎥", "desc": "Video ghi lại toàn bộ buổi học trực tuyến ngày 18/10/2026" },
            { "name": "RTL_to_GDS_training_buoi3.pptx", "size": "3.52 MB", "type": "SLIDES", "icon": "📊", "desc": "Slide bài giảng Buổi 3: Static Timing Analysis từ Giảng viên CTW SEMI" },
            { "name": "Tapeout_LAB2.pdf", "size": "4.22 MB", "type": "LAB GUIDE", "icon": "📕", "desc": "Tài liệu hướng dẫn thực hành Lab 2: Static Timing Analysis & Registered Multiplier" },
            { "name": "mult.v & mult.sdc", "size": "1.66 KB", "type": "VERILOG", "icon": "💻", "desc": "Mã nguồn Verilog và Khế ước thời gian SDC cho bộ nhân đồng bộ 8-bit" },
            { "name": "mult_post_pnr.sdc", "size": "6.94 KB", "type": "SDC", "icon": "⏱️", "desc": "Khế ước thời gian sau PnR đã gắn trích xuất trễ ký sinh thực tế" },
            { "name": "summary_reports_phase1_2_4.rpt", "size": "11.7 KB", "type": "REPORTS", "icon": "📑", "desc": "Trọn bộ 3 báo cáo STA OpenROAD: Baseline 15ns, Ép xung 13ns và RTL Fix" }
        ],
        "subsections": [
            {
                "id": "b3-materials",
                "title": "Tài Liệu Buổi Học & Giáo Trình Chuyên Sâu STA (Buổi 3)",
                "category": "TÀI LIỆU BUỔI HỌC",
                "icon": "📚",
                "readTime": "25 phút",
                "summary": "Giáo trình toàn diện về vị thế Kỹ sư STA Signoff, bản chất vật lý của thời gian, mô hình FF-to-FF, công thức tính toán Setup/Hold Slacks, nghệ thuật chèn buffer sửa Hold mà không phá vỡ Critical Path, và ma trận 9 góc PVT corners.",
                "toc": b3_mat_toc,
                "htmlContent": b3_mat_html
            },
            {
                "id": "b3-lab-guide",
                "title": "Bài Hướng Dẫn Thực Hành Lab 2: Phân Tích STA & Thư Viện Minh Chứng",
                "category": "BÀI HƯỚNG DẪN LAB 2",
                "icon": "🧪",
                "readTime": "18 phút",
                "summary": "Đề bài và quy trình chuẩn hóa từ Tapeout_LAB2.pdf & slide bài giảng, phân tích chi tiết từng bước trên CTW SEMI Web Cockpit, mổ xẻ báo cáo stapostpnr, hướng dẫn chạy DSE sweep và kỹ thuật sửa code Verilog RTL Pipelining.",
                "toc": b3_lab_toc,
                "htmlContent": b3_lab_html
            },
            {
                "id": "b3-student-report",
                "title": "Báo Cáo Thực Chiến Học Viên: Sổ Tay 5 Giai Đoạn Vượt Qua Lỗi Timing & Tape-out Signoff",
                "category": "BÁO CÁO THỰC CHIẾN HỌC VIÊN",
                "icon": "🏆",
                "readTime": "22 phút",
                "summary": "Hồ sơ thực nghiệm chuyên sâu của học viên qua 5 giai đoạn: Thiết lập mốc chuẩn vàng 15ns -> Bắt quả tang vi phạm Setup khi ép xung 13ns -> Đánh đổi PPA với DSE sweep DELAY 1-4 -> Đỉnh cao Pipelining RTL -> Tổng hợp đối chứng PPA & Ký duyệt Tape-out.",
            "toc": b3_rep_toc,
            "htmlContent": b3_rep_html
        }
    ]
    },
    {
        "id": "buoi-04",
        "tabTitle": "BUỔI 04 & 05: PHYSICAL DESIGN, 72 BƯỚC PnR, CVC64 GLS & GTKWAVE (LAB 3)",
        "shortTitle": "Buổi 4–5: PnR & Lab 3",
        "date": "24/10 - 19/11/2026",
        "badge": "BUỔI 04 & 05",
        "icon": "",
        "summary": "Làm chủ toàn diện Physical Design: giải phẫu file .odb qua 72 bước LibreLane/OpenROAD, điều khiển OpenROAD GUI & TCL Inspect (Standard Cell 2.72µm, Clock Skew 40 ps, PDN VPWR), ký duyệt mô phỏng Post-Layout SDF với CVC64 (0 lỗi) & GTKWave TinyTDC (Δt = 248.596 ns), hoàn tất đối chứng cpu8bit @ 50 MHz (fmax = 28.57 MHz @ 35 ns) và khởi động GĐ 4 TinyTDC.",
        "downloads": [
            { "name": "4 & 5. Physical_Design_24_30_10_2026.mkv", "size": "Video Lab 3", "type": "VIDEO", "icon": "", "desc": "Video bài giảng Buổi 4 & 5: OpenROAD GUI, CVC64 GLS & GTKWave Signoff" },
            { "name": "RTL_to_GDS_training_buoi4.pptx", "size": "33 Slides", "type": "SLIDES", "icon": "", "desc": "Slide Process Stack Sky130 (li1, met1–met5), IR Drop & cấu hình config.json" },
            { "name": "Tapeout_LAB3.pdf", "size": "40 Trang", "type": "LAB GUIDE", "icon": "", "desc": "Tài liệu hướng dẫn Lab 3: Giải phẫu .odb, thí nghiệm cpu8bit & TinyTDC" },
            { "name": "TinyTDC.zip", "size": "RTL+SDF+TB", "type": "PACKAGE", "icon": "", "desc": "Kho mã nguồn, netlist sau Layout và file trễ SDF cho kiểm chứng CVC64 & GTKWave" },
            { "name": "Bao_Cao_Tong_Hop_Physical_Design_Lab_3.md", "size": "2.036 Dòng", "type": "REPORT", "icon": "", "desc": "Báo cáo tổng hợp Lab 3 cập nhật mới nhất (GĐ 1–3 Done, Khởi động GĐ 4 TinyTDC)" }
        ],
        "subsections": [
            {
                "id": "b4-materials",
                "title": "Cẩm Nang Thực Chiến PnR: 5 Bước Vàng Tìm Lỗi & Đóng Timing",
                "category": "TÀI LIỆU & CẨM NANG PnR",
                "icon": "",
                "readTime": "12 phút",
                "summary": "Lộ trình 5 bước chuẩn công nghiệp chẩn đoán và sửa lỗi Timing Closure trên OpenROAD GUI: khám nghiệm vĩ mô Slack/Corner, truy vết Data Path Details bắt 3 thủ phạm (High Cell Delay, Quá tải Fanout, Logic Depth), soi mặt chip Placement/Congestion, kiểm toán SDC và kê đơn Action Plan.",
                "toc": b4_mat_toc,
                "htmlContent": b4_mat_html
            },
            {
                "id": "b4-lab-guide",
                "title": "Bài Hướng Dẫn Thực Hành Lab 3: Mục Tiêu, Thông Số config.json & Lệnh OpenROAD .odb",
                "category": "BÀI HƯỚNG DẪN LAB 3",
                "icon": "",
                "readTime": "10 phút",
                "summary": "Tóm tắt đề bài thực hành Lab 3 từ Tapeout_LAB3.pdf và Slide Buổi 4: Process Stack Sky130, bảng tra cứu các biến cấu hình config.json (DIE_AREA, PL_TARGET_DENSITY_PCT, RT_MAX_LAYER) và quy trình nạp snapshot .odb vào OpenROAD GUI.",
                "toc": b4_lab_toc,
                "htmlContent": b4_lab_html
            },
            {
                "id": "b4-student-report",
                "title": "Báo Cáo Thực Chiến Học Viên: Giải Phẫu .ODB, OpenROAD GUI, CVC64 GLS & GTKWave Lab 3",
                "category": "BÁO CÁO THỰC CHIẾN HỌC VIÊN",
                "icon": "",
                "readTime": "40 phút",
                "summary": "Hồ sơ kỹ thuật chuyên sâu 2.036 dòng cập nhật ngày 19/11/2026: hoàn thành 100% Giai đoạn 1 (giải phẫu PnR 72 bước & .odb), Giai đoạn 2 (OpenROAD GUI, CVC64 0 lỗi SDF, 5 phép đo picosecond GTKWave trên TinyTDC Δt = 248.596 ns), và Giai đoạn 3 (cpu8bit A/B hold=0.02 thông chốt 0 DRC/LVS, TCL tách Full-Cycle vs Half-Cycle, fmax = 28.57 MHz @ 35 ns + Critical Path GUI); khởi động Giai đoạn 4 (TinyTDC PnR & bảo toàn 512 delay cells).",
                "toc": b4_rep_toc,
                "htmlContent": b4_rep_html
            }
        ]
    }
]

# =============================================================================
# 6. WRITE report_data.js
# =============================================================================
js_content = f"""// ==============================================================================
// KHO DỮ LIỆU BÁO CÁO TOÀN DIỆN KHÓA HỌC: ASIC SILICON TAPEOUT (SKYWATER 130NM)
// Tự động tổng hợp từ D:\\Tapeout_chip\\Buoi_1, buoi_2, buoi_3 & buoi_4+5
// ==============================================================================

const COURSE_METADATA = {{
  title: "BÁO CÁO TOÀN DIỆN KHÓA HỌC: ASIC SILICON TAPEOUT",
  subtitle: "Hành Trình Thực Chiến Từ RTL Đến GDSII Trên Tiến Trình SkyWater 130nm & Nền Tảng CTW SEMI (OpenROAD Flow)",
  student: "Trương Công Việt Hoàng (Lead System Architect & ASIC Trainee)",
  instructor: "Giảng Viên & Chuyên Gia Thiết Kế Vi Mạch CTW SEMI",
  academicYear: "2026",
  targetPDK: "SkyWater 130nm (sky130A / sky130_fd_sc_hd)",
  totalSessions: {len(sessions_data)},
  kpis: [
    {{ label: "Tiến trình chế tạo", value: "SkyWater 130nm", sub: "PDK mã nguồn mở sky130A", color: "#111827" }},
    {{ label: "Chuỗi công cụ EDA", value: "OpenROAD", sub: "Yosys, CVC64, GTKWave ps, KLayout", color: "#0F766E" }},
    {{ label: "Tiến độ khóa học", value: "Buổi 1–5 · Lab 3", sub: "Lab 3: Xong GĐ 1–3 · Mở GĐ 4", color: "#9A3412" }},
    {{ label: "Đo kiểm GLS Signoff", value: "248.596 ns", sub: "TinyTDC SDF 0 lỗi • 556 ps/cell", color: "#1D4ED8" }}
  ]
}};

const SESSIONS_DATA = {json.dumps(sessions_data, ensure_ascii=False, indent=2)};
"""

with open(output_js, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Successfully generated {output_js} with {len(sessions_data)} sessions and full content!")
