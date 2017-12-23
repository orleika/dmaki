#!/bin/bash
docker run -it --rm --net dmaki_link -v $(pwd):/work -w /work gen-wordnet-jp python3 save_stopword.py
