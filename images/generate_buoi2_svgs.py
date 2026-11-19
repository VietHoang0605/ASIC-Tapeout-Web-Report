import os, sys
sys.stdout.reconfigure(encoding='utf-8')

img_dir = r"D:\Tapeout_chip\Web_Report\images"
os.makedirs(img_dir, exist_ok=True)

# 1. YOSYS + ABC PIPELINE SVG
svg1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 420" width="100%" height="100%" style="background: #080d1a; border-radius: 16px; font-family: 'Inter', system-ui, -apple-system, sans-serif;">
  <defs>
    <linearGradient id="pBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e172e" />
      <stop offset="100%" stop-color="#070c17" />
    </linearGradient>
    <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <rect x="2" y="2" width="1096" height="416" rx="14" fill="url(#pBg)" stroke="rgba(0, 200, 255, 0.3)" stroke-width="1.5" />

  <!-- Header -->
  <g transform="translate(40, 28)">
    <rect x="0" y="0" width="175" height="24" rx="6" fill="rgba(0, 200, 255, 0.15)" stroke="#00c8ff" stroke-width="1" />
    <text x="87.5" y="16.5" fill="#00c8ff" font-size="11.5" font-weight="700" text-anchor="middle" letter-spacing="0.5">SYNTHESIS FLOW</text>
    <text x="190" y="18" fill="#ffffff" font-size="16" font-weight="800">KIẾN TRÚC PHỐI HỢP YOSYS &amp; ABC ENGINE: TỪ RTL ĐẾN GATE NETLIST</text>
    <text x="190" y="36" fill="#94a3b8" font-size="12">Quy trình biến đổi mã Verilog trừu tượng thành các tế bào chuẩn vật lý trong thư viện Sky130 HD</text>
  </g>

  <!-- Flow Boxes -->
  <!-- Box 1: RTL -->
  <g transform="translate(40, 90)">
    <rect x="0" y="0" width="200" height="240" rx="12" fill="#0f172a" stroke="#38bdf8" stroke-width="1.8" />
    <rect x="0" y="0" width="200" height="36" rx="12" fill="rgba(56, 189, 248, 0.15)" />
    <line x1="0" y1="36" x2="200" y2="36" stroke="rgba(56, 189, 248, 0.3)" stroke-width="1" />
    <text x="100" y="24" fill="#38bdf8" font-size="13" font-weight="800" text-anchor="middle">1. MÃ NGUỒN RTL (.v)</text>

    <text x="16" y="65" fill="#e2e8f0" font-size="12" font-weight="700">• Cấp độ trừu tượng cao</text>
    <text x="16" y="85" fill="#94a3b8" font-size="11">Mô tả luồng dịch chuyển</text>
    <text x="16" y="102" fill="#94a3b8" font-size="11">dữ liệu giữa thanh ghi DFF</text>

    <text x="16" y="132" fill="#e2e8f0" font-size="12" font-weight="700">• Điều kiện lý tưởng:</text>
    <text x="16" y="152" fill="#cbd5e1" font-size="11">Wire Delay = 0</text>
    <text x="16" y="169" fill="#cbd5e1" font-size="11">Gate Delay = 0</text>

    <text x="16" y="200" fill="#10b981" font-size="11.5" font-weight="600">✓ Mục tiêu: Kiểm tra</text>
    <text x="16" y="217" fill="#10b981" font-size="11.5" font-weight="600">tính đúng đắn thuật toán</text>
  </g>

  <!-- Arrow 1 -->
  <g transform="translate(245, 195)">
    <line x1="0" y1="0" x2="40" y2="0" stroke="#38bdf8" stroke-width="2.5" />
    <polygon points="45,0 35,-5 35,5" fill="#38bdf8" />
    <text x="20" y="-10" fill="#38bdf8" font-size="10" font-weight="700" text-anchor="middle">PARSER</text>
  </g>

  <!-- Box 2: Yosys Generic Gates -->
  <g transform="translate(295, 90)">
    <rect x="0" y="0" width="220" height="240" rx="12" fill="#0f172a" stroke="#818cf8" stroke-width="1.8" />
    <rect x="0" y="0" width="220" height="36" rx="12" fill="rgba(129, 140, 248, 0.15)" />
    <line x1="0" y1="36" x2="220" y2="36" stroke="rgba(129, 140, 248, 0.3)" stroke-width="1" />
    <text x="110" y="24" fill="#a5b4fc" font-size="13" font-weight="800" text-anchor="middle">2. YOSYS SYNTHESIS</text>

    <text x="16" y="65" fill="#e2e8f0" font-size="12" font-weight="700">• Dịch sang Generic Gates:</text>
    <g transform="translate(16, 75)">
      <rect x="0" y="0" width="60" height="20" rx="4" fill="rgba(129, 140, 248, 0.2)" />
      <text x="30" y="14" fill="#c7d2fe" font-size="10" font-weight="700" text-anchor="middle">$_AND_</text>

      <rect x="66" y="0" width="56" height="20" rx="4" fill="rgba(129, 140, 248, 0.2)" />
      <text x="94" y="14" fill="#c7d2fe" font-size="10" font-weight="700" text-anchor="middle">$_NOT_</text>

      <rect x="128" y="0" width="56" height="20" rx="4" fill="rgba(129, 140, 248, 0.2)" />
      <text x="156" y="14" fill="#c7d2fe" font-size="10" font-weight="700" text-anchor="middle">$_MUX_</text>
    </g>

    <text x="16" y="125" fill="#e2e8f0" font-size="12" font-weight="700">• Trừu tượng công nghệ:</text>
    <text x="16" y="145" fill="#94a3b8" font-size="11">Chưa gắn với bất kỳ PDK</text>
    <text x="16" y="162" fill="#94a3b8" font-size="11">nhà máy bán dẫn nào.</text>

    <text x="16" y="195" fill="#fbbf24" font-size="11.5" font-weight="600">⚡ Tối ưu sơ bộ:</text>
    <text x="16" y="212" fill="#94a3b8" font-size="11">Triệt tiêu hằng số (Const Prop)</text>
  </g>

  <!-- Arrow 2 -->
  <g transform="translate(520, 195)">
    <line x1="0" y1="0" x2="40" y2="0" stroke="#818cf8" stroke-width="2.5" />
    <polygon points="45,0 35,-5 35,5" fill="#818cf8" />
    <text x="20" y="-10" fill="#818cf8" font-size="10" font-weight="700" text-anchor="middle">AIG NET</text>
  </g>

  <!-- Box 3: ABC Engine & Liberty -->
  <g transform="translate(570, 90)">
    <rect x="0" y="0" width="240" height="240" rx="12" fill="#0f172a" stroke="#f59e0b" stroke-width="1.8" />
    <rect x="0" y="0" width="240" height="36" rx="12" fill="rgba(245, 158, 11, 0.15)" />
    <line x1="0" y1="36" x2="240" y2="36" stroke="rgba(245, 158, 11, 0.3)" stroke-width="1" />
    <text x="120" y="24" fill="#fbbf24" font-size="13" font-weight="800" text-anchor="middle">3. ABC ENGINE (MAPPER)</text>

    <!-- Liberty inject badge -->
    <g transform="translate(16, 48)">
      <rect x="0" y="0" width="208" height="24" rx="4" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" stroke-width="1" />
      <text x="104" y="16" fill="#6ee7b7" font-size="10.5" font-weight="700" text-anchor="middle">📥 Nạp Liberty File (.lib)</text>
    </g>

    <text x="16" y="96" fill="#e2e8f0" font-size="12" font-weight="700">• Đồ thị And-Inverter (AIG):</text>
    <text x="16" y="114" fill="#94a3b8" font-size="11">Cắt nhánh tối ưu Boolean.</text>

    <text x="16" y="138" fill="#e2e8f0" font-size="12" font-weight="700">• Technology Mapping:</text>
    <text x="16" y="156" fill="#94a3b8" font-size="11">Tra cứu 7 thuộc tính vật lý</text>
    <text x="16" y="173" fill="#94a3b8" font-size="11">trong file .lib (Timing, Area, Cap)</text>

    <text x="16" y="202" fill="#f59e0b" font-size="11.5" font-weight="600">🎯 SYNTH_STRATEGY:</text>
    <text x="16" y="219" fill="#94a3b8" font-size="11">Cân bằng AREA 0-3 vs DELAY 0-3</text>
  </g>

  <!-- Arrow 3 -->
  <g transform="translate(815, 195)">
    <line x1="0" y1="0" x2="40" y2="0" stroke="#f59e0b" stroke-width="2.5" />
    <polygon points="45,0 35,-5 35,5" fill="#f59e0b" />
    <text x="20" y="-10" fill="#f59e0b" font-size="10" font-weight="700" text-anchor="middle">MAP CELL</text>
  </g>

  <!-- Box 4: Gate-Level Netlist -->
  <g transform="translate(860, 90)">
    <rect x="0" y="0" width="200" height="240" rx="12" fill="#0f172a" stroke="#10b981" stroke-width="1.8" />
    <rect x="0" y="0" width="200" height="36" rx="12" fill="rgba(16, 185, 129, 0.15)" />
    <line x1="0" y1="36" x2="200" y2="36" stroke="rgba(16, 185, 129, 0.3)" stroke-width="1" />
    <text x="100" y="24" fill="#6ee7b7" font-size="13" font-weight="800" text-anchor="middle">4. GATE NETLIST (.v)</text>

    <text x="16" y="65" fill="#e2e8f0" font-size="12" font-weight="700">• Tế bào thật Sky130:</text>
    <text x="16" y="85" fill="#a7f3d0" font-size="11" font-family="'JetBrains Mono', monospace">sky130_fd_sc_hd__...</text>
    <text x="16" y="103" fill="#94a3b8" font-size="11">nand2_1, dfxtp_2, a21oi_1</text>

    <text x="16" y="133" fill="#e2e8f0" font-size="12" font-weight="700">• Có thông số cụ thể:</text>
    <text x="16" y="153" fill="#cbd5e1" font-size="11">Diện tích (Area μm²)</text>
    <text x="16" y="170" fill="#cbd5e1" font-size="11">Trễ logic (Logic Delay ns)</text>

    <text x="16" y="202" fill="#10b981" font-size="11.5" font-weight="600">✓ Đầu vào cho Floorplan</text>
    <text x="16" y="219" fill="#10b981" font-size="11.5" font-weight="600">&amp; Placement (PnR Flow)</text>
  </g>

  <!-- Bottom Notice -->
  <g transform="translate(40, 350)">
    <rect x="0" y="0" width="1020" height="42" rx="8" fill="#1e1b4b" stroke="#6366f1" stroke-width="1.2" />
    <text x="510" y="26" fill="#e0e7ff" font-size="12" font-weight="600" text-anchor="middle">
      ⚠️ LƯU Ý KIẾN TRÚC SƯ: Nghiệm của ABC ở bước Synthesis chưa biết trễ dây ký sinh sau PnR. OpenROAD sẽ tiếp tục resize cell và chèn buffer trong giai đoạn Placement &amp; CTS!
    </text>
  </g>
</svg>"""

with open(os.path.join(img_dir, "yosys_abc_pipeline.svg"), "w", encoding="utf-8") as f:
    f.write(svg1)

# 2. LIBERTY 7 ATTRIBUTES SVG
svg2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 480" width="100%" height="100%" style="background: #080d1a; border-radius: 16px; font-family: 'Inter', system-ui, -apple-system, sans-serif;">
  <defs>
    <linearGradient id="pBg2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e172e" />
      <stop offset="100%" stop-color="#070c17" />
    </linearGradient>
  </defs>

  <rect x="2" y="2" width="1096" height="476" rx="14" fill="url(#pBg2)" stroke="rgba(245, 158, 11, 0.3)" stroke-width="1.5" />

  <!-- Header -->
  <g transform="translate(40, 28)">
    <rect x="0" y="0" width="160" height="24" rx="6" fill="rgba(245, 158, 11, 0.15)" stroke="#f59e0b" stroke-width="1" />
    <text x="80" y="16.5" fill="#f59e0b" font-size="11.5" font-weight="700" text-anchor="middle" letter-spacing="0.5">LIBERTY (.LIB) DEEP-DIVE</text>
    <text x="175" y="18" fill="#ffffff" font-size="16" font-weight="800">MẮT THẦN CỦA ABC: 7 THUỘC TÍNH CỐT TỬ QUYẾT ĐỊNH VIỆC CHỌN CELL</text>
    <text x="175" y="36" fill="#94a3b8" font-size="12">Các thông số vật lý then chốt giúp cỗ máy Technology Mapping đánh đổi giữa Diện tích (Area) và Thời gian (Delay)</text>
  </g>

  <!-- Left: File Liberty Hub -->
  <g transform="translate(40, 110)">
    <rect x="0" y="0" width="220" height="320" rx="14" fill="#1e1638" stroke="#a855f7" stroke-width="2" />
    <text x="110" y="38" fill="#c084fc" font-size="28" text-anchor="middle">📚</text>
    <text x="110" y="70" fill="#ffffff" font-size="15" font-weight="800" text-anchor="middle">FILE LIBERTY</text>
    <text x="110" y="90" fill="#e9d5ff" font-size="12" font-family="'JetBrains Mono', monospace" text-anchor="middle">sky130_fd_sc_hd.lib</text>

    <text x="20" y="130" fill="#cbd5e1" font-size="11.5" font-weight="600">• Giao ước vật lý:</text>
    <text x="20" y="148" fill="#94a3b8" font-size="11">Do Foundry SkyWater cung cấp.</text>

    <text x="20" y="180" fill="#cbd5e1" font-size="11.5" font-weight="600">• Điều kiện PVT Corner:</text>
    <text x="20" y="198" fill="#94a3b8" font-size="11">Điện áp: 1.80V</text>
    <text x="20" y="214" fill="#94a3b8" font-size="11">Nhiệt độ: 25°C</text>
    <text x="20" y="230" fill="#94a3b8" font-size="11">Tiến trình: TT (Typical)</text>

    <text x="20" y="265" fill="#f43f5e" font-size="11.5" font-weight="600">⚠️ Nếu thiếu file .lib:</text>
    <text x="20" y="282" fill="#94a3b8" font-size="11">Synthesis không thể diễn ra!</text>
  </g>

  <!-- Right: 7 Attributes Cards -->
  <!-- Attr 1: Boolean function -->
  <g transform="translate(300, 90)">
    <rect x="0" y="0" width="360" height="74" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2" />
    <text x="14" y="24" fill="#38bdf8" font-size="12" font-weight="800">1. HÀM BOOLEAN (Boolean Function)</text>
    <text x="14" y="44" fill="#e2e8f0" font-size="11.5">Định nghĩa logic toán học: <tspan fill="#f59e0b" font-family="'JetBrains Mono', monospace">function: "(A &amp; B) | C";</tspan></text>
    <text x="14" y="62" fill="#94a3b8" font-size="10.5">Xác định cell nào có thể đảm đương được cụm logic của thiết kế.</text>
  </g>

  <!-- Attr 2: Area -->
  <g transform="translate(680, 90)">
    <rect x="0" y="0" width="380" height="74" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="1.2" />
    <text x="14" y="24" fill="#10b981" font-size="12" font-weight="800">2. DIỆN TÍCH Ô CHUẨN (Area Cost - μm²)</text>
    <text x="14" y="44" fill="#e2e8f0" font-size="11.5">Kích thước hình học thực tế trên silicon của từng ô chuẩn.</text>
    <text x="14" y="62" fill="#94a3b8" font-size="10.5">Khi đặt <tspan fill="#6ee7b7">SYNTH_STRATEGY = AREA</tspan>, ABC sẽ ép chọn cell diện tích nhỏ nhất.</text>
  </g>

  <!-- Attr 3: Timing arcs (NLDM) -->
  <g transform="translate(300, 175)">
    <rect x="0" y="0" width="360" height="74" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="1.2" />
    <text x="14" y="24" fill="#fbbf24" font-size="12" font-weight="800">3. CUNG TRỄ TÍN HIỆU (Timing Arcs - NLDM)</text>
    <text x="14" y="44" fill="#e2e8f0" font-size="11.5">Mô hình trễ phi tuyến: <tspan fill="#38bdf8" font-family="'JetBrains Mono', monospace">t_pd = f(Input Slew, Output Load)</tspan></text>
    <text x="14" y="62" fill="#94a3b8" font-size="10.5">Độ trễ không cố định mà tra cứu từ bảng 2 chiều theo độ dốc xung &amp; tải.</text>
  </g>

  <!-- Attr 4: Pin Capacitance -->
  <g transform="translate(680, 175)">
    <rect x="0" y="0" width="380" height="74" rx="8" fill="#0f172a" stroke="#c084fc" stroke-width="1.2" />
    <text x="14" y="24" fill="#c084fc" font-size="12" font-weight="800">4. ĐIỆN DUNG CHÂN ĐẦU VÀO (Pin Capacitance)</text>
    <text x="14" y="44" fill="#e2e8f0" font-size="11.5">Tải điện dung ký sinh tại mỗi chân ngõ vào (vài fF đến chục fF).</text>
    <text x="14" y="62" fill="#94a3b8" font-size="10.5">Quyết định tải mà tầng cổng phía trước (Driver) phải gánh.</text>
  </g>

  <!-- Attr 5: Driving Cell -->
  <g transform="translate(300, 260)">
    <rect x="0" y="0" width="360" height="74" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2" />
    <text x="14" y="24" fill="#38bdf8" font-size="12" font-weight="800">5. KHẢ NĂNG LÁI NGUỒN VÀO (Driving Cell)</text>
    <text x="14" y="44" fill="#e2e8f0" font-size="11.5">Mô hình hóa nội trở và sườn dốc tín hiệu từ bên ngoài bơm vào.</text>
    <text x="14" y="62" fill="#94a3b8" font-size="10.5">Giúp tính toán độ méo xung khi đi vào các cổng đầu vào của chip.</text>
  </g>

  <!-- Attr 6: Output Load -->
  <g transform="translate(680, 260)">
    <rect x="0" y="0" width="380" height="74" rx="8" fill="#0f172a" stroke="#ec4899" stroke-width="1.2" />
    <text x="14" y="24" fill="#f472b6" font-size="12" font-weight="800">6. TẢI ĐIỆN DUNG NGÕ RA (Output Load)</text>
    <text x="14" y="44" fill="#e2e8f0" font-size="11.5">Giá trị tụ điện giả định mà các chân ngõ ra phải kéo.</text>
    <text x="14" y="62" fill="#94a3b8" font-size="10.5">Dùng để tính toán sườn dốc và độ trễ của các cell ở tầng cuối cùng.</text>
  </g>

  <!-- Attr 7: Allowed Cell Set (Full Width) -->
  <g transform="translate(300, 345)">
    <rect x="0" y="0" width="760" height="74" rx="8" fill="#0f172a" stroke="#ef4444" stroke-width="1.2" />
    <text x="14" y="24" fill="#f87171" font-size="12" font-weight="800">7. TẬP TẾ BÀO HỢP LỆ &amp; RÀNG BUỘC CẤM DÙNG (Allowed Cell Set / dont_use)</text>
    <text x="14" y="44" fill="#e2e8f0" font-size="11.5">Những cell bị đánh dấu <tspan fill="#fca5a5" font-family="'JetBrains Mono', monospace">dont_use</tspan> (do rủi ro quang khắc hoặc timing) sẽ bị ABC gạch tên khỏi danh sách lựa chọn.</text>
    <text x="14" y="62" fill="#94a3b8" font-size="10.5">Kỹ sư có thể chủ động cấm các cell lái quá yếu hoặc cell quá phức tạp để đảm bảo an toàn vật lý.</text>
  </g>
</svg>"""

with open(os.path.join(img_dir, "liberty_7_attributes.svg"), "w", encoding="utf-8") as f:
    f.write(svg2)

# 3. RIPPLE CARRY ADDER ARCHITECTURE SVG
svg3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 420" width="100%" height="100%" style="background: #080d1a; border-radius: 16px; font-family: 'Inter', system-ui, -apple-system, sans-serif;">
  <defs>
    <linearGradient id="pBg3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e172e" />
      <stop offset="100%" stop-color="#070c17" />
    </linearGradient>
  </defs>

  <rect x="2" y="2" width="1096" height="416" rx="14" fill="url(#pBg3)" stroke="rgba(16, 185, 129, 0.3)" stroke-width="1.5" />

  <!-- Header -->
  <g transform="translate(40, 28)">
    <rect x="0" y="0" width="180" height="24" rx="6" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" stroke-width="1" />
    <text x="90" y="16.5" fill="#10b981" font-size="11.5" font-weight="700" text-anchor="middle" letter-spacing="0.5">CIRCUIT ARCHITECTURE</text>
    <text x="195" y="18" fill="#ffffff" font-size="16" font-weight="800">KIẾN TRÚC MẠCH BỘ CỘNG LAN TRUYỀN 8-BIT (RIPPLE CARRY ADDER - RCA)</text>
    <text x="195" y="36" fill="#94a3b8" font-size="12">Mạch thực nghiệm chính trong Lab 1: Ghép nối tiếp 8 bộ cộng toàn phần 1-bit (Full Adder)</text>
  </g>

  <!-- 8 Full Adders Chain -->
  <!-- Cin input at right (since bit 0 is LSB) -->
  <g transform="translate(980, 150)">
    <rect x="0" y="0" width="70" height="36" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2" />
    <text x="35" y="22" fill="#38bdf8" font-size="12" font-weight="800" text-anchor="middle">Cin = 0</text>
  </g>

  <!-- Adder Stages: FA0 to FA7 from right to left -->
  <!-- Loop drawing in python -->
"""

# Let's generate the 8 full adder blocks in python
fa_blocks = ""
for i in range(8):
    # From right to left: bit 0 at x=860, bit 7 at x=40
    x = 860 - i * 115
    bit = i
    fa_blocks += f"""
    <g transform="translate({x}, 120)">
      <rect x="0" y="0" width="95" height="130" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="1.8" />
      <rect x="0" y="0" width="95" height="26" rx="10" fill="rgba(16, 185, 129, 0.15)" />
      <text x="47.5" y="18" fill="#6ee7b7" font-size="11.5" font-weight="800" text-anchor="middle">FA[{bit}]</text>

      <!-- Inputs A, B -->
      <line x1="28" y1="-25" x2="28" y2="0" stroke="#38bdf8" stroke-width="2" />
      <polygon points="28,0 25,-6 31,-6" fill="#38bdf8" />
      <text x="28" y="-30" fill="#38bdf8" font-size="10" font-weight="700" text-anchor="middle">A{bit}</text>

      <line x1="66" y1="-25" x2="66" y2="0" stroke="#f59e0b" stroke-width="2" />
      <polygon points="66,0 63,-6 69,-6" fill="#f59e0b" />
      <text x="66" y="-30" fill="#f59e0b" font-size="10" font-weight="700" text-anchor="middle">B{bit}</text>

      <!-- Output Sum -->
      <line x1="47.5" y1="130" x2="47.5" y2="160" stroke="#a855f7" stroke-width="2" />
      <polygon points="47.5,165 44.5,155 50.5,155" fill="#a855f7" />
      <text x="47.5" y="180" fill="#c084fc" font-size="11" font-weight="800" text-anchor="middle">S{bit}</text>
    </g>
    """

    # Ripple carry line from FA[i-1] to FA[i]
    if i < 7:
        cx = x - 20
        fa_blocks += f"""
        <g transform="translate({x - 20}, 165)">
          <line x1="20" y1="0" x2="0" y2="0" stroke="#f43f5e" stroke-width="3" />
          <polygon points="0,0 7,-4 7,4" fill="#f43f5e" />
          <text x="10" y="-8" fill="#f43f5e" font-size="9" font-weight="800" text-anchor="middle">C{bit+1}</text>
        </g>
        """

# Cout from FA7
fa_blocks += """
<g transform="translate(10, 165)">
  <line x1="40" y1="0" x2="5" y2="0" stroke="#f43f5e" stroke-width="3" />
  <polygon points="0,0 8,-5 8,5" fill="#f43f5e" />
  <text x="20" y="-8" fill="#f43f5e" font-size="10" font-weight="800" text-anchor="middle">Cout</text>
  <rect x="-5" y="15" width="55" height="24" rx="4" fill="rgba(244, 63, 94, 0.2)" stroke="#f43f5e" stroke-width="1" />
  <text x="22.5" y="31" fill="#fca5a5" font-size="10.5" font-weight="700" text-anchor="middle">sum[8]</text>
</g>

<!-- Connect Cin to FA0 -->
<g transform="translate(955, 165)">
  <line x1="25" y1="0" x2="0" y2="0" stroke="#38bdf8" stroke-width="2" />
  <polygon points="0,0 6,-3 6,3" fill="#38bdf8" />
</g>
"""

svg3 = svg3.replace("<!-- Loop drawing in python -->", fa_blocks)

# Add Bottom explanation banner
svg3 += """
  <!-- Bottom Banner: Critical Path -->
  <g transform="translate(40, 340)">
    <rect x="0" y="0" width="1020" height="46" rx="8" fill="#2d1217" stroke="#f43f5e" stroke-width="1.2" />
    <text x="510" y="22" fill="#fecdd3" font-size="12" font-weight="700" text-anchor="middle">
      ⚡ ĐƯỜNG TRỄ TỚI HẠN (CRITICAL PATH): Tín hiệu nhớ Carry phải "gợn sóng" (Ripple) bò tuần tự từ FA[0] ➔ FA[1] ➔ ... ➔ FA[7] ➔ Cout
    </text>
    <text x="510" y="38" fill="#fda4af" font-size="11" text-anchor="middle">
      Tầng FA[7] chỉ có thể tính xong kết quả khi tầng FA[6] đã chuyển bit nhớ sang. Đây là bài toán đánh đổi kinh điển giữa Diện tích nhỏ và Trễ lớn!
    </text>
  </g>
</svg>
"""

with open(os.path.join(img_dir, "rca_8bit_architecture.svg"), "w", encoding="utf-8") as f:
    f.write(svg3)

print("Successfully generated all 3 new SVGs for Buoi 2 in images folder!")
