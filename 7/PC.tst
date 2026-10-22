load PC.hdl,
output-file PC.out,
compare-to PC.cmp,
output-list time%S1.4.1 in%D1.6.1 load%B2.1.2 inc%B2.1.2 reset%B2.1.2 out%D1.6.1;

set in 0, set load 0, set inc 0, set reset 0, tick, tock, output;

set inc 1, tick, tock, output;
tick, tock, output;

set in -32123, tick, tock, output;

set load 1, tick, tock, output;

set load 0, tick, tock, output;
tick, tock, output;

set reset 1, tick, tock, output;

set reset 0, tick, tock, output;
tick, tock, output;

set reset 1, set load 1, set inc 1, tick, tock, output;

set reset 0, tick, tock, output;

set load 0, tick, tock, output;

set reset 1, tick, tock, output;

set in 12345, set load 1, set reset 0, set inc 0, tick, tock, output;

set reset 1, tick, tock, output;

set reset 0, set load 0, set inc 1, tick, tock, output;
tick, tock, output;

set in 0, set load 1, set inc 0, tick, tock, output;

set load 0, set inc 1, tick, tock, output;
tick, tock, output;
