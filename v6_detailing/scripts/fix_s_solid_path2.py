import subprocess

s_solid_d = """M 218 160
C 218 95 180 55 118 55
C 55 55 18 95 18 145
C 18 190 45 220 118 245
C 185 270 218 290 218 320
C 218 355 180 375 118 375
C 55 375 18 340 18 260
L 88 260
C 88 300 100 315 118 315
C 138 315 148 305 148 290
C 148 265 125 245 78 225
C 25 200 88 145 88 145
C 88 120 100 115 118 115
C 138 115 148 130 148 160
Z"""

# Let's refine the inner waist curves:
s_solid_d = """M 218 160
C 218 95 180 55 118 55
C 55 55 18 95 18 145
C 18 195 50 225 105 245
C 175 270 218 295 218 325
C 218 358 178 375 118 375
C 55 375 18 340 18 260
L 88 260
C 88 295 102 315 118 315
C 135 315 148 305 148 290
C 148 265 125 245 75 225
C 35 205 88 145 88 145
C 88 125 100 115 118 115
C 135 115 148 130 148 160
Z"""

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 450" width="300" height="450">
  <rect width="300" height="450" fill="#0F172A"/>
  <path d="{s_solid_d}" fill="#FAD758" stroke="#FFFFFF" stroke-width="2"/>
</svg>'''

with open('scratch/test_s_single_path2.svg', 'w') as f:
    f.write(svg)

subprocess.run(['qlmanage', '-t', '-s', '600', '-o', 'scratch', 'scratch/test_s_single_path2.svg'], check=True)
print('Rendered S test 2!')
