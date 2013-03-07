import sys
if len(sys.argv) < 2:
    print "Usage: %s file"%sys.argv[0]
f = open(sys.argv[1])
index = 0
gnuplot = """
# Note you need gnuplot 4.4 for the pdfcairo terminal.

set terminal pdfcairo font "Gill Sans, 24" linewidth 6 rounded enhanced dashed

# Line style for axes
set style line 80 lt rgb "#808080"

# Line style for grid
#set style line 81 lt 0  # dashed
#set style line 81 lt rgb "#808080"  # grey

#set grid back linestyle 81
set border 3 back linestyle 80 # Remove border on top and right.  These
# borders are useless and make it harder to see plotted lines near the border.
# Also, put it in grey; no need for so much emphasis on a border.

set xtics nomirror
set ytics nomirror

set ylabel "Count"
set xlabel "Accessed"
set bars small
#set datafile separator ","
set key off
set output "{output}.pdf"
#set yrange [0:1]
set xrange[0:]
set title "{title}"
set boxwidth 0.6
#set arrow from 1.0,graph(0,0) to 1.0,graph(1,1) nohead lc 1 lt -1
set style fill solid 1.0 border lt -1
plot "{input}" index {ind} using 1:2 w boxes title "Access Frequencies" lc rgb "#cccccc"
"""
index = 0
for l in f:
    #print gnuplot.format(input=l.strip(), output=l.strip())
    if "Utilization =" in l:
        util = l.strip().split(' = ')[1]
        print gnuplot.format(input=sys.argv[1], output="%s.%s"%(sys.argv[1], util), title=l[1:].strip(), ind=index)
        index += 1 
