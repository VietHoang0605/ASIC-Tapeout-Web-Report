# ASIC Silicon Tapeout — Khóa học Thiết kế Vi mạch RTL to GDSII (SkyWater 130nm)

> 🌐 **Xem Web Báo Cáo Trực Tiếp (Vercel):** **https://asic-tapeout-web-report.vercel.app**

Kho lưu trữ tài liệu học tập, bài Lab thực hành và báo cáo kỹ thuật cho hành trình thiết kế vi mạch số **RTL-to-GDSII** trên tiến trình **SkyWater 130nm (`sky130A` / `sky130_fd_sc_hd`)** bằng chuỗi công cụ EDA mã nguồn mở (**CTW SEMI / LibreLane**).

---

## 🎯 Mục tiêu khóa học

Xâu chuỗi bản chất vật lý bán dẫn và kỹ năng thực chiến qua toàn bộ dây chuyền từ mã nguồn Verilog tới file mặt nạ quang khắc **GDSII** sẵn sàng Tape-out:
* Làm chủ mô phỏng Front-End, tổng hợp logic (Synthesis), ràng buộc thời gian (SDC) và phân tích thời gian tĩnh đa góc PVT (STA).
* Điều khiển, chẩn đoán và sửa lỗi Physical Design (Floorplan, Placement, CTS, Routing, DRC/LVS) qua **OpenROAD GUI/TCL**.
* Kiểm định mạch sau bố trí (Post-Layout Signoff) với trích xuất ký sinh **SPEF/SDF**, mô phỏng **CVC64 Gate-Level Simulation** và đo đạc **GTKWave** ở thang picosecond.

---

## 📚 Lộ trình nội dung (5 Buổi · Lab 0 – Lab 3)

| Buổi | Thư mục | Chủ đề trọng tâm | Mạch thực hành & Công cụ |
| :--- | :--- | :--- | :--- |
| **Buổi 1** | [`Buoi_1/`](./Buoi_1) | Nhập môn RTL-to-GDSII, Testbench & Waveform, Floorplanning và truy vết lỗi Placement (`DPL-0036`). | `counter.v` (8-bit Counter) · `iverilog`, GTKWave, CTW SEMI |
| **Buổi 2** | [`buoi_2/`](./buoi_2) | Logic Synthesis (`Yosys + ABC`), cấu trúc thư viện Standard Cell & Liberty (`.lib`), đánh đổi Area vs Delay. | Bộ cộng 8-bit RCA (`AREA` / `DELAY` strategies) |
| **Buổi 3** | [`buoi_3/`](./buoi_3) | Ràng buộc **SDC**, Static Timing Analysis (Setup/Hold, 9 góc PVT), Timing Closure qua DSE vs RTL Pipelining. | `mult.v` (8-bit Registered Multiplier) · OpenSTA |
| **Buổi 4 & 5** | [`buoi_4+5/`](./buoi_4+5) | Giải phẫu `.odb` & dây chuyền PnR, OpenROAD GUI/TCL, tối ưu Hold/Congestion (`cpu8bit @ 50 MHz`), Post-Layout GLS/SDF & bảo toàn Delay Line (`TinyTDC`). *(Đang hoàn thiện GĐ 4)* | `cpu8bit` (`tt_um_dvxf_dj8`), `TinyTDC` · OpenROAD, CVC64, GTKWave, Magic, KLayout |

---

## 🗂️ Cấu trúc thư mục chính

```text
Tapeout_chip/
├── Buoi_1/                      # Bài giảng, Lab 0, mã nguồn counter & ghi chép Buổi 1
├── buoi_2/                      # Bài giảng, Lab 1 & tài liệu Logic Synthesis / Liberty
├── buoi_3/                      # Bài giảng, Lab 2, giáo trình STA/SDC & kinh nghiệm Timing Closure
├── buoi_4+5/                    # Bài giảng, Lab 3, cẩm nang PnR & báo cáo tổng hợp OpenROAD/GLS
├── CTW_SEMI_Huong_dan_chay.docx # Hướng dẫn cài đặt & vận hành môi trường CTW SEMI
└── my_first_constraints.sdc     # File ràng buộc thời gian SDC mẫu
```

---

## 🛠️ Công nghệ & Chuỗi công cụ EDA

* **PDK & Standard Cell Library:** SkyWater 130nm (`sky130A`), thư viện mật độ cao `sky130_fd_sc_hd`.
* **Nền tảng thực thi:** CTW SEMI Web Cockpit (LibreLane / OpenROAD Flow trong Docker trên WSL2 Ubuntu).
* **Công cụ chuyên biệt:** Icarus Verilog (`iverilog`), Yosys + ABC, OpenROAD, OpenSTA, CVC64 (Post-Layout GLS + SDF), GTKWave, Magic & KLayout (DRC / LVS / GDSII).

---

## 🌐 Xem báo cáo trực quan trên Web (Vercel)

Toàn bộ giáo trình, bài Lab, bảng số liệu và sơ đồ trực quan của khóa học được triển khai trực tuyến tại:

👉 **https://asic-tapeout-web-report.vercel.app**
