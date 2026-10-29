# 第八週作業報告：IC 設計的 EDA 軟體與應用

## 一、 IC 設計的 EDA 是什麼？

EDA（Electronic Design Automation，電子設計自動化）是指利用電腦軟體與硬體系統，來協助工程師進行積體電路（IC）設計、模擬、驗證、佈局與製造準備的技術。隨著半導體製程不斷微縮、電晶體數量達到數十億甚至數兆規模，純粹依靠人工繪製電路圖已完全不可行，因此 EDA 工具成為現代半導體與晶片設計不可或缺的核心基石。

一個完整的 IC 設計流程通常包含以下幾個關鍵階段，而 EDA 貫穿其中：

1. **行為與架構設計（Behavioral/Architectural Design）：** 使用硬體描述語言（如 Verilog、VHDL、Veryl）來定義晶片的邏輯與功能。
2. **邏輯綜合（Logic Synthesis）：** 將高階的硬體描述語言轉換為由邏輯閘（如 AND、OR、NOT）組成的閘級電路圖。
3. **模擬與驗證（Simulation & Verification）：** 透過模擬器測試電路行為是否符合預期，確保沒有邏輯錯誤或時序違規。
4. **實體設計與佈局繞線（Layout & Routing）：** 將邏輯閘轉換為實際的電晶體幾何圖形，並計算金屬導線的路徑與佈局。

---

## 二、 參考資料與實作工具分析

本次作業參考了 5 個相關教學與開源專案連結，整理其核心功能與學習應用價值如下表：

| 參考專案 / 連結 | 工具性質與核心功能 | 學習應用價值 |
| :--- | :--- | :--- |
| **[Veryl2Chip 網頁版 EDA](https://ccc-eda.github.io/veryl2chip/web/dist/index.html)** | 將現代硬體描述語言 Veryl 轉換為晶片設計的線上 EDA 工具。 | 體驗現代硬體描述語言如何透過網頁端進行邏輯轉換與編譯運作。 |
| **[Hack Computer HDL 模擬器](https://ccc-js.github.io/hack-computer/dist/hdl.html)** | 基於網頁的硬體描述語言（HDL）與計算機架構模擬環境。 | 理解從基本邏輯閘（Nand）逐步建構出 CPU 與記憶體的底層實作原理。 |
| **[Cornell ECE 5745 Handouts](https://www.csl.cornell.edu/courses/ece5745/handouts.html)** | 康乃爾大學高等數位積體電路設計與硬體合成課程講義。 | 提供深入的 VLSI 設計、高階綜合與現代硬體設計方法論參考。 |
| **[Veryl2Chip GitHub 專案](https://github.com/ccc-eda/veryl2chip/)** | Veryl 轉晶片流程的開源專案程式碼與說明。 | 深入研究前端 EDA 工具的開源原始碼與底層編譯流程。 |
| **[Hack Computer GitHub 專案](https://github.com/ccc-js/hack-computer)** | Nand2Tetris 架構下的 Hack 電腦硬體實作與模擬專案。 | 實作硬體組合邏輯與時序邏輯組件的最佳實務範例。 |

---

## 三、 心得與總結

透過本次作業與 5 個參考連結的探索，我們能深刻體會到 IC 設計自動化工具在現代科技中所扮演的關鍵角色。從最早期的基礎邏輯閘與硬體模擬（如 Hack Computer），到現代結合高階硬體描述語言的編譯與轉換工具（如 Veryl2Chip），EDA 不僅大幅降低了晶片設計的門檻，也提升了電路設計的正確性與效率。這對於理解計算機底層硬體架構與晶片製造流程有極大的幫助。