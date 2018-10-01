PNGS = \
  img/norm.freqs.png \
  img/sliced.norm.freqs.png \
  img/signal.png \
  img/sin1.png \
  img/beats.png

all : $(PNGS) tex/article.html

img/signal.png : gen_signal.py
	python gen_signal.py

img/norm.freqs.png img/sliced.norm.freqs.png : gen_slice_no_norm.py waterfall_plot.py
	python gen_slice_no_norm.py

img/sin1.png : example_signals.py
	python example_signals.py

img/beats.png : beat_detector.py
	python beat_detector.py

$(PNGS) : data.py song.wav

song.wav : rogers_dean_no_doubt.opus
	ffmpeg -i $< $@

tex/article.html : tex/article.tex $(PNGS)
	cd tex && htlatex article "html" "" "" "-shell-escape"

.PHONY: all
