// NxN registered multiplier with registered inputs (Pipelining Stage 1)
// Fully Registered Design: Inputs and product are registered.
module mult #(
    parameter W = 8
) (
    input  wire           clk,
    input  wire           rst,
    input  wire [W-1:0]   a,
    input  wire [W-1:0]   b,
    output reg  [2*W-1:0] p
);
    // Khai bao 16 D-FF dem dau vao (Input Pipeline Registers)
    reg [W-1:0] a_p, b_p;

    always @(posedge clk) begin
        if (rst) begin
            p   <= {(2*W){1'b0}};
            a_p <= {W{1'b0}};
            b_p <= {W{1'b0}};
        end else begin
            a_p <= a;         // Chang 1: Chot dau vao (Path 1: In2Reg - Tranh input delay)
            b_p <= b;
            p   <= a_p * b_p; // Chang 2: Nhan thuan tuy Reg2Reg noi bo (Path 2: Reg2Reg)
        end
    end
endmodule
