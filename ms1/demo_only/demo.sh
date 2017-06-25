#!/bin/bash
python demo.py --glove "../glove/glove.6B.200d.txt" --train_p "./demo" --slot_l "../Data/slot_l.txt" --intent_l "../Data/intent_l.txt"
python demo_intent.py --glove "../glove/glove.6B.200d.txt" --train_p "./demo" --slot_l "../Data/slot_l.txt" --intent_l "../Data/intent_l.txt"
