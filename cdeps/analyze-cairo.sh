python cdeps_to_dot.py "../../cairo/src/*.c"
sfdp -Tpng out.dot > deps.png
eog deps.png