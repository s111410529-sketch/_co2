// fill.asm
// 依據鍵盤輸入狀態刷白或刷黑螢幕

(CHECK_KBD)
// 1. 讀取鍵盤輸入狀態
@KBD
D=M

// 2. 若有按鍵 (D > 0)，設定繪圖顏色為黑色 (-1)；否則設為白色 (0)
@SET_BLACK
D;JNE

// 沒有按鍵 -> 白色
D=0
@DRAW
0;JMP

(SET_BLACK)
// 有按鍵 -> 黑色 (-1，即 16 進位的 0xFFFF)
D=-1

(DRAW)
// 3. 儲存選擇的顏色到變數 color (RAM[16])
@color
M=D

// 4. 初始化螢幕指標 addr = SCREEN (16384)
@SCREEN
D=A
@addr
M=D

(FILL_LOOP)
// 5. 檢查是否已經刷完整個螢幕 (addr == KBD)
@addr
D=M
@KBD
D=D-A
@CHECK_KBD
D;JEQ // 若已刷滿 8192 個 word，跳回監聽鍵盤

// 6. 填入顏色至目前的螢幕位址 (*addr = color)
@color
D=M
@addr
A=M
M=D

// 7. 指標前進一個 word (addr = addr + 1)
@addr
M=M+1

// 8. 繼續刷下一個 word
@FILL_LOOP
0;JMP
