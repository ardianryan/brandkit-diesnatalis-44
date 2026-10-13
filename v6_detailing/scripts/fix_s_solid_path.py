import cv2
import numpy as np
import subprocess

# Let's test a single continuous non-self-intersecting path for the S base:
# Outer perimeter:
# (218, 160) -> C (218, 95) (180, 55) (118, 55)
#            -> C (55, 55) (18, 95) (18, 145)
#            -> C (18, 195) (52, 220) (88, 240)
#            -> C (125, 260) (152, 280) (152, 312)
#            -> C (152, 345) (138, 372) (118, 372)
#            -> C (60, 372) (18, 325) (18, 260)   <-- bottom outer terminal corner
# (18, 260)  -> L (88, 260)                        <-- bottom terminal cut!
# Inner perimeter:
# (88, 260)  -> C (88, 285) (98, 305) (118, 305)
#            -> C (135, 305) (148, 292) (148, 275)
#            -> C (148, 250) (125, 230) (88, 210)
#            -> C (50, 190) (25, 170) (25, 145)
#            -> C (25, 115) (55, 100) (88, 100)
#            -> C (118, 100) (148, 120) (148, 160) <-- top inner terminal corner
# (148, 160) -> L (218, 160)                        <-- top terminal cut!
# CLOSE Z!

s_solid_d = """M 218 160
C 218 95 180 55 118 55
C 55 55 18 95 18 145
C 18 195 52 220 88 240
C 125 260 152 280 152 312
C 152 345 138 372 118 372
C 60 372 18 325 18 260
L 88 260
C 88 285 98 305 118 305
C 135 305 148 292 148 275
C 148 250 125 230 88 210
C 50 190 25 170 25 145
C 25 115 55 100 88 100
C 118 100 148 120 148 160
Z"""

# Let's test this in a quick SVG:
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 450" width="300" height="450">
  <rect width="300" height="450" fill="#0F172A"/>
  <path d="{s_solid_d}" fill="#FAD758" stroke="#FFFFFF" stroke-width="2"/>
</svg>'''

with open('scratch/test_s_single_path.svg', 'w') as f:
    f.write(svg)

subprocess.run(['qlmanage', '-t', '-s', '600', '-o', 'scratch', 'scratch/test_s_single_path.svg'], check=True)
print('Rendered single path S!')
