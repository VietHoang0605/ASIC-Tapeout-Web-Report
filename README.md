# ASIC Silicon Tapeout Web Report (SkyWater 130nm · RTL to GDSII)

> 🌐 **Xem Web Báo Cáo Trực Tiếp (Vercel):** **https://asic-tapeout-web-report.vercel.app**

Trang web tổng hợp giáo trình, hướng dẫn Lab 0–Lab 3 và báo cáo kỹ thuật thực hành Physical Design trên tiến trình **SkyWater 130nm (`sky130A`)** với chuỗi công cụ **Yosys, OpenROAD, OpenSTA, CVC64, GTKWave, Magic & KLayout**.

## Nội dung chính
- **Buổi 01 (Lab 0):** Nhập môn RTL-to-GDSII, Floorplanning & truy vết lỗi `DPL-0036`.
- **Buổi 02 (Lab 1):** Logic Synthesis (`Yosys + ABC`), Standard Cells & file Liberty `.lib` trên bộ cộng 8-bit RCA.
- **Buổi 03 (Lab 2):** Static Timing Analysis (STA), Setup/Hold, 9 góc PVT, DSE Sweep & RTL Pipelining trên bộ nhân `mult`.
- **Buổi 04 & 05 (Lab 3):** Giải phẫu `.odb` & 72 bước PnR, OpenROAD GUI/TCL, CVC64 Post-Layout GLS (`0` SDF errors), đo xung picosecond trên GTKWave (`TinyTDC`), phân tích `cpu8bit @ 50 MHz` và khởi động GĐ 4 `TinyTDC`.

## Triển khai
- Repository được liên kết trực tiếp với Vercel (`main` branch auto-deploy): https://asic-tapeout-web-report.vercel.app
