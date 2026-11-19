################################################################################
# Khế ước thời gian SDC cho Bộ nhân 8-bit (mult.sdc)
# Tiến trình: SkyWater 130nm (sky130_fd_sc_hd)
# Nhịp đồng hồ mặc định ban đầu: 15.0ns (66.67 MHz)
################################################################################

create_clock -name clk -period 15.0 [get_ports clk]

set_clock_transition 0.15 [get_clocks clk]
set_clock_uncertainty 0.25 clk

set_input_delay 3.0 -clock clk [get_ports a[*]]
set_input_delay 3.0 -clock clk [get_ports b[*]]
set_input_delay 3.0 -clock clk [get_ports rst]

set_output_delay 3.0 -clock clk [get_ports p[*]]

set_timing_derate -early 0.95
set_timing_derate -late 1.05

set_max_transition 0.75 [current_design]
set_max_capacitance 0.2 [current_design]
set_max_fanout 10 [current_design]
