module counter (clk,
    en,
    rst,
    count);
 input clk;
 input en;
 input rst;
 output [7:0] count;

 wire _00_;
 wire _01_;
 wire _02_;
 wire _03_;
 wire _04_;
 wire _05_;
 wire _06_;
 wire _07_;
 wire _08_;
 wire _09_;
 wire _10_;
 wire _11_;
 wire _12_;
 wire _13_;
 wire _14_;
 wire _15_;
 wire _16_;
 wire _17_;
 wire _18_;
 wire _19_;
 wire _20_;
 wire _21_;
 wire _22_;
 wire net3;
 wire net4;
 wire net5;
 wire net6;
 wire net7;
 wire net8;
 wire net9;
 wire net10;
 wire net1;
 wire net2;
 wire net11;
 wire net12;
 wire clknet_0_clk;
 wire clknet_1_0__leaf_clk;
 wire clknet_1_1__leaf_clk;
 wire net13;
 wire net14;
 wire net15;
 wire net16;
 wire net17;
 wire net18;
 wire net19;
 wire net20;
 wire net21;

 sky130_fd_sc_hd__decap_3 FILLER_0_29 ();
 sky130_fd_sc_hd__fill_2 FILLER_0_3 ();
 sky130_fd_sc_hd__decap_3 FILLER_0_57 ();
 sky130_fd_sc_hd__decap_3 FILLER_0_60 ();
 sky130_fd_sc_hd__fill_2 FILLER_10_11 ();
 sky130_fd_sc_hd__decap_3 FILLER_10_25 ();
 sky130_fd_sc_hd__decap_3 FILLER_10_29 ();
 sky130_fd_sc_hd__fill_1 FILLER_10_3 ();
 sky130_fd_sc_hd__fill_2 FILLER_10_32 ();
 sky130_fd_sc_hd__decap_3 FILLER_10_49 ();
 sky130_fd_sc_hd__decap_3 FILLER_10_52 ();
 sky130_fd_sc_hd__fill_1 FILLER_10_55 ();
 sky130_fd_sc_hd__decap_3 FILLER_10_57 ();
 sky130_fd_sc_hd__decap_3 FILLER_10_60 ();
 sky130_fd_sc_hd__decap_3 FILLER_1_3 ();
 sky130_fd_sc_hd__fill_1 FILLER_1_30 ();
 sky130_fd_sc_hd__decap_3 FILLER_1_57 ();
 sky130_fd_sc_hd__fill_2 FILLER_1_6 ();
 sky130_fd_sc_hd__decap_3 FILLER_1_60 ();
 sky130_fd_sc_hd__fill_1 FILLER_2_3 ();
 sky130_fd_sc_hd__decap_3 FILLER_2_60 ();
 sky130_fd_sc_hd__decap_3 FILLER_3_28 ();
 sky130_fd_sc_hd__fill_1 FILLER_3_3 ();
 sky130_fd_sc_hd__fill_1 FILLER_3_31 ();
 sky130_fd_sc_hd__decap_3 FILLER_3_57 ();
 sky130_fd_sc_hd__decap_3 FILLER_3_60 ();
 sky130_fd_sc_hd__decap_3 FILLER_4_11 ();
 sky130_fd_sc_hd__fill_1 FILLER_4_22 ();
 sky130_fd_sc_hd__decap_3 FILLER_5_11 ();
 sky130_fd_sc_hd__decap_3 FILLER_5_23 ();
 sky130_fd_sc_hd__fill_1 FILLER_5_46 ();
 sky130_fd_sc_hd__fill_1 FILLER_5_55 ();
 sky130_fd_sc_hd__decap_3 FILLER_5_57 ();
 sky130_fd_sc_hd__decap_3 FILLER_5_60 ();
 sky130_fd_sc_hd__decap_3 FILLER_6_23 ();
 sky130_fd_sc_hd__fill_2 FILLER_6_26 ();
 sky130_fd_sc_hd__fill_1 FILLER_6_29 ();
 sky130_fd_sc_hd__fill_1 FILLER_7_24 ();
 sky130_fd_sc_hd__decap_3 FILLER_7_3 ();
 sky130_fd_sc_hd__decap_3 FILLER_7_52 ();
 sky130_fd_sc_hd__fill_1 FILLER_7_55 ();
 sky130_fd_sc_hd__decap_3 FILLER_7_57 ();
 sky130_fd_sc_hd__fill_1 FILLER_7_6 ();
 sky130_fd_sc_hd__decap_3 FILLER_7_60 ();
 sky130_fd_sc_hd__decap_3 FILLER_8_60 ();
 sky130_fd_sc_hd__fill_1 FILLER_9_3 ();
 sky130_fd_sc_hd__fill_2 FILLER_9_33 ();
 sky130_fd_sc_hd__decap_3 FILLER_9_43 ();
 sky130_fd_sc_hd__fill_2 FILLER_9_46 ();
 sky130_fd_sc_hd__decap_3 FILLER_9_57 ();
 sky130_fd_sc_hd__decap_3 FILLER_9_60 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_0_Left_11 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_0_Right_0 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_10_Left_21 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_10_Right_10 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_1_Left_12 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_1_Right_1 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_2_Left_13 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_2_Right_2 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_3_Left_14 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_3_Right_3 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_4_Left_15 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_4_Right_4 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_5_Left_16 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_5_Right_5 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_6_Left_17 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_6_Right_6 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_7_Left_18 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_7_Right_7 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_8_Left_19 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_8_Right_8 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_9_Left_20 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_9_Right_9 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_22 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_23 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_10_33 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_10_34 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_1_24 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_2_25 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_3_26 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_4_27 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_5_28 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_6_29 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_7_30 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_8_31 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_9_32 ();
 sky130_fd_sc_hd__a21oi_2 _23_ (.A1(net1),
    .A2(net16),
    .B1(net2),
    .Y(_08_));
 sky130_fd_sc_hd__o21a_2 _24_ (.A1(net1),
    .A2(net16),
    .B1(_08_),
    .X(_00_));
 sky130_fd_sc_hd__a21oi_2 _25_ (.A1(net1),
    .A2(net3),
    .B1(net14),
    .Y(_09_));
 sky130_fd_sc_hd__and3_2 _26_ (.A(net1),
    .B(net4),
    .C(net3),
    .X(_10_));
 sky130_fd_sc_hd__nor3_2 _27_ (.A(net2),
    .B(net15),
    .C(_10_),
    .Y(_01_));
 sky130_fd_sc_hd__and4_2 _28_ (.A(net1),
    .B(net5),
    .C(net4),
    .D(net3),
    .X(_11_));
 sky130_fd_sc_hd__nor2_2 _29_ (.A(net2),
    .B(net11),
    .Y(_12_));
 sky130_fd_sc_hd__o21a_2 _30_ (.A1(net13),
    .A2(_10_),
    .B1(_12_),
    .X(_02_));
 sky130_fd_sc_hd__a21oi_2 _31_ (.A1(net12),
    .A2(net11),
    .B1(net2),
    .Y(_13_));
 sky130_fd_sc_hd__o21a_2 _32_ (.A1(net12),
    .A2(net11),
    .B1(_13_),
    .X(_03_));
 sky130_fd_sc_hd__a21oi_2 _33_ (.A1(net12),
    .A2(net11),
    .B1(net17),
    .Y(_14_));
 sky130_fd_sc_hd__a31o_2 _34_ (.A1(net7),
    .A2(net12),
    .A3(net11),
    .B1(net2),
    .X(_15_));
 sky130_fd_sc_hd__nor2_2 _35_ (.A(_14_),
    .B(_15_),
    .Y(_04_));
 sky130_fd_sc_hd__a31o_2 _36_ (.A1(net7),
    .A2(net12),
    .A3(net11),
    .B1(net21),
    .X(_16_));
 sky130_fd_sc_hd__a41o_2 _37_ (.A1(net8),
    .A2(net7),
    .A3(net12),
    .A4(net11),
    .B1(net2),
    .X(_17_));
 sky130_fd_sc_hd__and2b_2 _38_ (.A_N(_17_),
    .B(_16_),
    .X(_05_));
 sky130_fd_sc_hd__a41o_2 _39_ (.A1(net8),
    .A2(net7),
    .A3(net12),
    .A4(net11),
    .B1(net18),
    .X(_18_));
 sky130_fd_sc_hd__and3_2 _40_ (.A(net9),
    .B(net8),
    .C(net7),
    .X(_19_));
 sky130_fd_sc_hd__a31o_2 _41_ (.A1(net12),
    .A2(net11),
    .A3(_19_),
    .B1(net2),
    .X(_20_));
 sky130_fd_sc_hd__and2b_2 _42_ (.A_N(_20_),
    .B(_18_),
    .X(_06_));
 sky130_fd_sc_hd__nand4_2 _43_ (.A(net19),
    .B(net12),
    .C(net11),
    .D(_19_),
    .Y(_21_));
 sky130_fd_sc_hd__a31o_2 _44_ (.A1(net6),
    .A2(_11_),
    .A3(_19_),
    .B1(net10),
    .X(_22_));
 sky130_fd_sc_hd__and3b_2 _45_ (.A_N(net2),
    .B(_21_),
    .C(_22_),
    .X(_07_));
 sky130_fd_sc_hd__dfxtp_2 _46_ (.CLK(clknet_1_0__leaf_clk),
    .D(_00_),
    .Q(net3));
 sky130_fd_sc_hd__dfxtp_2 _47_ (.CLK(clknet_1_1__leaf_clk),
    .D(_01_),
    .Q(net4));
 sky130_fd_sc_hd__dfxtp_2 _48_ (.CLK(clknet_1_1__leaf_clk),
    .D(_02_),
    .Q(net5));
 sky130_fd_sc_hd__dfxtp_2 _49_ (.CLK(clknet_1_0__leaf_clk),
    .D(_03_),
    .Q(net6));
 sky130_fd_sc_hd__dfxtp_2 _50_ (.CLK(clknet_1_0__leaf_clk),
    .D(_04_),
    .Q(net7));
 sky130_fd_sc_hd__dfxtp_2 _51_ (.CLK(clknet_1_0__leaf_clk),
    .D(_05_),
    .Q(net8));
 sky130_fd_sc_hd__dfxtp_2 _52_ (.CLK(clknet_1_1__leaf_clk),
    .D(_06_),
    .Q(net9));
 sky130_fd_sc_hd__dfxtp_2 _53_ (.CLK(clknet_1_1__leaf_clk),
    .D(net20),
    .Q(net10));
 sky130_fd_sc_hd__clkbuf_16 clkbuf_0_clk (.A(clk),
    .X(clknet_0_clk));
 sky130_fd_sc_hd__clkbuf_16 clkbuf_1_0__f_clk (.A(clknet_0_clk),
    .X(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__clkbuf_16 clkbuf_1_1__f_clk (.A(clknet_0_clk),
    .X(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__clkdlybuf4s25_1 fanout11 (.A(_11_),
    .X(net11));
 sky130_fd_sc_hd__clkdlybuf4s25_1 fanout12 (.A(net6),
    .X(net12));
 sky130_fd_sc_hd__dlygate4sd3_1 hold13 (.A(net5),
    .X(net13));
 sky130_fd_sc_hd__dlygate4sd3_1 hold14 (.A(net4),
    .X(net14));
 sky130_fd_sc_hd__dlygate4sd3_1 hold15 (.A(_09_),
    .X(net15));
 sky130_fd_sc_hd__dlygate4sd3_1 hold16 (.A(net3),
    .X(net16));
 sky130_fd_sc_hd__dlygate4sd3_1 hold17 (.A(net7),
    .X(net17));
 sky130_fd_sc_hd__dlygate4sd3_1 hold18 (.A(net9),
    .X(net18));
 sky130_fd_sc_hd__dlygate4sd3_1 hold19 (.A(net10),
    .X(net19));
 sky130_fd_sc_hd__dlygate4sd3_1 hold20 (.A(_07_),
    .X(net20));
 sky130_fd_sc_hd__dlygate4sd3_1 hold21 (.A(net8),
    .X(net21));
 sky130_fd_sc_hd__clkdlybuf4s25_1 input1 (.A(en),
    .X(net1));
 sky130_fd_sc_hd__clkdlybuf4s25_1 input2 (.A(rst),
    .X(net2));
 sky130_fd_sc_hd__clkdlybuf4s25_1 output10 (.A(net10),
    .X(count[7]));
 sky130_fd_sc_hd__clkdlybuf4s25_1 output3 (.A(net3),
    .X(count[0]));
 sky130_fd_sc_hd__clkdlybuf4s25_1 output4 (.A(net4),
    .X(count[1]));
 sky130_fd_sc_hd__clkdlybuf4s25_1 output5 (.A(net5),
    .X(count[2]));
 sky130_fd_sc_hd__clkdlybuf4s25_1 output6 (.A(net12),
    .X(count[3]));
 sky130_fd_sc_hd__clkdlybuf4s25_1 output7 (.A(net7),
    .X(count[4]));
 sky130_fd_sc_hd__clkdlybuf4s25_1 output8 (.A(net8),
    .X(count[5]));
 sky130_fd_sc_hd__clkdlybuf4s25_1 output9 (.A(net9),
    .X(count[6]));
endmodule
