import time
import board
import analogio

pot = analogio.AnalogIn(board.A0)

while True:
    print(pot.value)
    time.sleep(0.1)
