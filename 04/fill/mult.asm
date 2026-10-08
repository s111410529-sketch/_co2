// mult.asm
// 計算 RAM[2] = RAM[0] * RAM[1]

// 1. 初始化 RAM[2] = 0
@2
M=0

(LOOP)
// 2. 檢查 RAM[0] 是否 <= 0，如果是就結束跳轉至 END
@0
D=M
@END
D;JLE

// 3. 累加：RAM[2] = RAM[2] + RAM[1]
@1
D=M
@2
M=D+M

// 4. 計數器減 1：RAM[0] = RAM[0] - 1
@0
M=M-1

// 5. 跳回 LOOP 繼續執行
@LOOP
0;JMP

(END)
// 6. 無限迴圈鎖定程式
@END
0;JMP
