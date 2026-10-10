#!/usr/bin/env python3
"""
Generator Video Logo Reveal Dies Natalis ke-44 SMAN 1 Gedeg (AVERSA)
Tema: Teater Akbar Emas & Beludru Ungu (Cinematic Imperial Velvet)
Durasi: 11 Detik (330 frames @ 30 FPS)
Format:
  1. 16:9 Lanskap (1920x1080) - YouTube, Panggung, Videotron
  2. 9:16 Vertikal (1080x1920) - Instagram Reels, TikTok, Story
  3. 4:5 Portrait (1080x1350) - Instagram Feed Portrait
"""

import math
import os
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS = 30
DURATION_SEC = 11.0
TOTAL_FRAMES = int(DURATION_SEC * FPS) # 330 frames

FONT_CINZEL_BOLD = "assets/fonts/cinzel/ttf/Cinzel-Bold.ttf"
FONT_CINZEL_REG = "assets/fonts/cinzel/ttf/Cinzel-Regular.ttf"
FONT_JAKARTA_BOLD = "assets/fonts/plus-jakarta-sans/ttf/PlusJakartaSans-Bold.ttf"
FONT_JAKARTA_REG = "assets/fonts/plus-jakarta-sans/ttf/PlusJakartaSans-Regular.ttf"
LOGO_SYMBOL_PATH = "assets/png/logo-color-2048.png"

# Color constants (RGB)
C_VELVET_DARK = (14, 2, 18)
C_VELVET_MID = (38, 7, 45)
C_VELVET_PLUM = (54, 9, 56)
C_GOLD_BRIGHT = (255, 234, 160)
C_GOLD_PRIMARY = (245, 197, 56)
C_GOLD_DEEP = (224, 157, 23)
C_WHITE = (255, 255, 255)

def get_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def ease_out_quad(t: float) -> float:
    return t * (2 - t)

def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3

def ease_in_out_quad(t: float) -> float:
    return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

def create_base_gradient(w: int, h: int) -> np.ndarray:
    """Precompute base radial velvet background array in BGR uint8."""
    y, x = np.ogrid[:h, :w]
    cx, cy = w / 2.0, h / 2.0
    # Normalized radial distance
    max_dist = math.sqrt(cx**2 + cy**2)
    dist = np.sqrt((x - cx)**2 + (y - cy)**2) / max_dist
    dist = np.clip(dist, 0.0, 1.0)
    
    # Interp from center (plum) to edge (dark velvet)
    # in BGR
    b1, g1, r1 = C_VELVET_PLUM[2], C_VELVET_PLUM[1], C_VELVET_PLUM[0]
    b0, g0, r0 = C_VELVET_DARK[2], C_VELVET_DARK[1], C_VELVET_DARK[0]
    
    factor = np.power(dist, 1.3)
    b = (b1 * (1 - factor) + b0 * factor).astype(np.uint8)
    g = (g1 * (1 - factor) + g0 * factor).astype(np.uint8)
    r = (r1 * (1 - factor) + r0 * factor).astype(np.uint8)
    
    return np.dstack([b, g, r])

class LogoRevealRenderer:
    def __init__(self, width: int, height: int, name: str):
        self.w = width
        self.h = height
        self.name = name
        self.cx = width // 2
        
        # Adjust layout based on aspect ratio
        if width > height:  # 16:9
            self.cy_logo = int(height * 0.44)
            self.logo_target_size = int(height * 0.55)
            self.font_aversa_size = int(height * 0.082)
            self.font_sub_size = int(height * 0.030)
            self.font_badge_size = int(height * 0.024)
            self.y_aversa = int(height * 0.75)
            self.y_sub = int(height * 0.85)
            self.y_meta = int(height * 0.90)
        elif height / width > 1.6:  # 9:16
            self.cy_logo = int(height * 0.42)
            self.logo_target_size = int(width * 0.72)
            self.font_aversa_size = int(width * 0.125)
            self.font_sub_size = int(width * 0.042)
            self.font_badge_size = int(width * 0.034)
            self.y_aversa = int(height * 0.65)
            self.y_sub = int(height * 0.73)
            self.y_meta = int(height * 0.78)
        else:  # 4:5
            self.cy_logo = int(height * 0.43)
            self.logo_target_size = int(width * 0.62)
            self.font_aversa_size = int(width * 0.105)
            self.font_sub_size = int(width * 0.037)
            self.font_badge_size = int(width * 0.030)
            self.y_aversa = int(height * 0.69)
            self.y_sub = int(height * 0.78)
            self.y_meta = int(height * 0.83)

        self.font_aversa = get_font(FONT_CINZEL_BOLD, self.font_aversa_size)
        self.font_sub = get_font(FONT_JAKARTA_BOLD, self.font_sub_size)
        self.font_meta = get_font(FONT_JAKARTA_REG, self.font_badge_size)

        # Load & pre-scale logo
        raw_logo = Image.open(LOGO_SYMBOL_PATH).convert("RGBA")
        self.logo_pil = raw_logo.resize((self.logo_target_size, self.logo_target_size), Image.Resampling.LANCZOS)
        
        # Precompute base velvet background
        self.bg_bgr = create_base_gradient(self.w, self.h)
        
        # Pre-seed particle clouds
        np.random.seed(44)
        self.num_spiral_particles = 220
        self.spiral_particles = []
        for _ in range(self.num_spiral_particles):
            angle = np.random.uniform(0, 2 * math.pi)
            dist = np.random.uniform(self.w * 0.25, self.w * 0.95)
            speed = np.random.uniform(0.6, 1.4)
            size = np.random.randint(2, 6)
            alpha = np.random.uniform(0.3, 0.9)
            color_choice = np.random.choice([0, 1, 2])
            color = [C_GOLD_BRIGHT, C_GOLD_PRIMARY, C_GOLD_DEEP][color_choice]
            self.spiral_particles.append({
                "angle": angle, "dist": dist, "speed": speed, "size": size,
                "alpha": alpha, "color": color
            })
            
        # Burst particles (for impact at frame 135)
        self.num_burst = 90
        self.burst_particles = []
        for _ in range(self.num_burst):
            angle = np.random.uniform(0, 2 * math.pi)
            speed = np.random.uniform(self.w * 0.12, self.w * 0.45)
            size = np.random.randint(2, 7)
            color_choice = np.random.choice([0, 1, 2])
            color = [C_GOLD_BRIGHT, C_WHITE, C_GOLD_PRIMARY][color_choice]
            self.burst_particles.append({
                "angle": angle, "speed": speed, "size": size, "color": color
            })

    def render_frame(self, frame_idx: int) -> np.ndarray:
        t = frame_idx / float(FPS)
        
        # Start from base background copy
        frame_bgr = self.bg_bgr.copy()
        
        # Create PIL overlay image for alpha drawing
        overlay = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # =========================================================================
        # PHASE 1 & 2: VORTEX PARTICLES & GLOW (0.0s - 4.5s / frame 0 - 135)
        # =========================================================================
        if t < 4.8:
            # Swirling stardust spiral converging toward center
            p_progress = min(1.0, t / 4.4)
            for p in self.spiral_particles:
                # inward movement
                cur_dist = p["dist"] * (1.0 - p_progress * 0.85 * p["speed"])
                cur_angle = p["angle"] + p_progress * 4.5 * p["speed"]
                px = int(self.cx + cur_dist * math.cos(cur_angle))
                py = int(self.cy_logo + cur_dist * math.sin(cur_angle) * 0.7)
                
                if 0 <= px < self.w and 0 <= py < self.h:
                    fade = min(1.0, t / 1.0)
                    if t > 4.2:
                        fade *= max(0.0, (4.8 - t) / 0.6)
                    a = int(255 * p["alpha"] * fade)
                    sz = p["size"]
                    c = p["color"]
                    draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=(c[0], c[1], c[2], a))

        # Central Gathering Energy Glow (0.8s - 4.5s)
        if 0.5 <= t <= 4.6:
            glow_progress = min(1.0, (t - 0.5) / 3.8)
            glow_r = int(self.logo_target_size * 0.35 * (0.6 + 0.4 * glow_progress))
            glow_alpha = int(90 * ease_out_quad(glow_progress))
            if t > 4.2:
                glow_alpha = int(glow_alpha * (4.6 - t) / 0.4)
            # Pulsing radial glow rings
            for r in range(glow_r, 0, -18):
                a_ring = int(glow_alpha * (1.0 - r / glow_r) ** 1.5)
                draw.ellipse(
                    [self.cx - r, self.cy_logo - r, self.cx + r, self.cy_logo + r],
                    fill=(C_GOLD_PRIMARY[0], C_GOLD_PRIMARY[1], C_GOLD_PRIMARY[2], a_ring)
                )

        # Silhouette & Edge Ignition (2.3s - 4.5s)
        if 2.2 <= t <= 4.5:
            sil_progress = min(1.0, (t - 2.2) / 2.0)
            sil_alpha = int(140 * ease_out_quad(sil_progress))
            # Draw logo silhouette in gold tint
            logo_scaled = self.logo_pil.copy()
            # Golden glow tint on logo
            tint_layer = Image.new("RGBA", logo_scaled.size, (C_GOLD_PRIMARY[0], C_GOLD_PRIMARY[1], C_GOLD_PRIMARY[2], sil_alpha))
            # Mask with logo alpha
            r, g, b, a_mask = logo_scaled.split()
            tint_layer.putalpha(Image.fromarray((np.array(a_mask) * (sil_alpha / 255.0)).astype(np.uint8)))
            
            lx = self.cx - self.logo_target_size // 2
            ly = self.cy_logo - self.logo_target_size // 2
            overlay.paste(tint_layer, (lx, ly), mask=tint_layer.split()[3])

        # Anamorphic Light Beam Sweep (3.0s - 4.5s)
        if 3.0 <= t <= 4.5:
            beam_prog = (t - 3.0) / 1.5
            beam_x = int(self.w * (beam_prog * 1.4 - 0.2))
            beam_w = int(self.w * 0.22)
            beam_alpha = int(180 * math.sin(beam_prog * math.pi))
            
            # Horizontal beam line across cy_logo
            h_half = 6
            draw.rectangle([0, self.cy_logo - h_half, self.w, self.cy_logo + h_half], fill=(C_GOLD_BRIGHT[0], C_GOLD_BRIGHT[1], C_GOLD_BRIGHT[2], int(beam_alpha * 0.4)))
            # Flare center hotspot
            draw.ellipse([beam_x - 120, self.cy_logo - 35, beam_x + 120, self.cy_logo + 35], fill=(255, 255, 255, beam_alpha))

        # =========================================================================
        # PHASE 3: IMPACT, SHOCKWAVE & FULL LOGO REVEAL (4.5s - 6.5s / frame 135 - 195)
        # =========================================================================
        if t >= 4.5:
            impact_t = t - 4.5
            
            # 1. Shockwave rings expanding
            if impact_t < 1.8:
                sw_prog = impact_t / 1.8
                sw_r = int(sw_prog * self.w * 0.75)
                sw_alpha = int(220 * (1.0 - sw_prog) ** 1.6)
                sw_width = max(2, int(6 * (1.0 - sw_prog)))
                if sw_alpha > 0 and sw_r > 0:
                    draw.ellipse(
                        [self.cx - sw_r, self.cy_logo - sw_r, self.cx + sw_r, self.cy_logo + sw_r],
                        outline=(C_GOLD_BRIGHT[0], C_GOLD_BRIGHT[1], C_GOLD_BRIGHT[2], sw_alpha),
                        width=sw_width
                    )
                    # Secondary inner echo ring
                    sw_r2 = int(sw_r * 0.7)
                    if sw_r2 > 0:
                        draw.ellipse(
                            [self.cx - sw_r2, self.cy_logo - sw_r2, self.cx + sw_r2, self.cy_logo + sw_r2],
                            outline=(C_GOLD_PRIMARY[0], C_GOLD_PRIMARY[1], C_GOLD_PRIMARY[2], int(sw_alpha * 0.6)),
                            width=max(1, sw_width - 2)
                        )

            # 2. Burst particles shooting outward
            if impact_t < 2.5:
                bp_prog = impact_t / 2.5
                bp_alpha = max(0.0, 1.0 - bp_prog ** 1.3)
                for bp in self.burst_particles:
                    b_dist = bp["speed"] * ease_out_quad(bp_prog)
                    bx = int(self.cx + b_dist * math.cos(bp["angle"]))
                    by = int(self.cy_logo + b_dist * math.sin(bp["angle"]))
                    if 0 <= bx < self.w and 0 <= by < self.h:
                        ba = int(255 * bp_alpha)
                        sz = max(1, int(bp["size"] * (1.0 - bp_prog * 0.5)))
                        bc = bp["color"]
                        draw.ellipse([bx - sz, by - sz, bx + sz, by + sz], fill=(bc[0], bc[1], bc[2], ba))

            # 3. Logo Scaling & Full Alpha Render
            # Spring scale effect: scale from 1.15 decaying to 1.0
            scale_spring = 1.0 + 0.14 * math.exp(-impact_t * 3.5) * math.cos(impact_t * 9.0)
            logo_w = int(self.logo_target_size * scale_spring)
            logo_h = int(self.logo_target_size * scale_spring)
            
            logo_frame = self.logo_pil.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
            
            # Fade in opacity (reaches 100% in 0.3s)
            logo_alpha = min(1.0, impact_t / 0.3)
            if logo_alpha < 1.0:
                l_arr = np.array(logo_frame)
                l_arr[:, :, 3] = (l_arr[:, :, 3] * logo_alpha).astype(np.uint8)
                logo_frame = Image.fromarray(l_arr)
            
            lx = self.cx - logo_w // 2
            ly = self.cy_logo - logo_h // 2
            overlay.paste(logo_frame, (lx, ly), mask=logo_frame.split()[3])

            # 4. Specular Diagonal Light Gleam across Logo (t = 5.2s - 7.0s)
            if 5.2 <= t <= 7.0:
                gleam_prog = (t - 5.2) / 1.8
                gleam_offset = -self.logo_target_size * 0.8 + gleam_prog * (self.logo_target_size * 2.2)
                
                # Draw light band clipped to logo
                gleam_band = Image.new("RGBA", (logo_w, logo_h), (0, 0, 0, 0))
                g_draw = ImageDraw.Draw(gleam_band)
                
                # Diagonal polygon
                bw = 70
                gx1 = int(gleam_offset)
                gx2 = gx1 + bw
                g_draw.polygon(
                    [(gx1, 0), (gx2, 0), (gx2 - logo_h // 2, logo_h), (gx1 - logo_h // 2, logo_h)],
                    fill=(255, 255, 255, 120)
                )
                
                # Mask with logo alpha
                gleam_arr = np.array(gleam_band)
                logo_a_arr = np.array(logo_frame.split()[3])
                gleam_arr[:, :, 3] = np.minimum(gleam_arr[:, :, 3], logo_a_arr)
                masked_gleam = Image.fromarray(gleam_arr)
                overlay.paste(masked_gleam, (lx, ly), mask=masked_gleam.split()[3])

        # =========================================================================
        # PHASE 4: TYPOGRAPHY ELEVATION (6.5s - 9.0s / frame 195 - 270)
        # =========================================================================
        if t >= 6.5:
            typo_t = t - 6.5
            typo_alpha = min(1.0, typo_t / 1.2)
            alpha_byte = int(255 * ease_out_quad(typo_alpha))
            
            # Subtle upward float into place
            y_slide = int(18 * (1.0 - ease_out_cubic(min(1.0, typo_t / 1.5))))
            
            # 1. AVERSA Wordmark
            text_aversa = "AVERSA"
            cur_y_aversa = self.y_aversa + y_slide
            
            # Shadow behind AVERSA
            draw.text((self.cx + 2, cur_y_aversa + 3), text_aversa, font=self.font_aversa, fill=(0, 0, 0, int(alpha_byte * 0.7)), anchor="mm")
            # Golden Text
            draw.text((self.cx, cur_y_aversa), text_aversa, font=self.font_aversa, fill=(C_GOLD_BRIGHT[0], C_GOLD_BRIGHT[1], C_GOLD_BRIGHT[2], alpha_byte), anchor="mm")

            # 2. Golden Filigree Divider Line (fades in 7.0s)
            if typo_t >= 0.5:
                div_prog = min(1.0, (typo_t - 0.5) / 1.0)
                div_len = int(self.w * 0.35 * ease_out_cubic(div_prog))
                div_a = int(190 * div_prog)
                y_div = (self.y_aversa + self.y_sub) // 2 + y_slide
                
                # Left line & Right line with diamond node in center
                draw.line([(self.cx - div_len, y_div), (self.cx - 20, y_div)], fill=(C_GOLD_PRIMARY[0], C_GOLD_PRIMARY[1], C_GOLD_PRIMARY[2], div_a), width=2)
                draw.line([(self.cx + 20, y_div), (self.cx + div_len, y_div)], fill=(C_GOLD_PRIMARY[0], C_GOLD_PRIMARY[1], C_GOLD_PRIMARY[2], div_a), width=2)
                # Diamond center
                draw.polygon(
                    [(self.cx, y_div - 5), (self.cx + 5, y_div), (self.cx, y_div + 5), (self.cx - 5, y_div)],
                    fill=(C_GOLD_BRIGHT[0], C_GOLD_BRIGHT[1], C_GOLD_BRIGHT[2], div_a)
                )

            # 3. Subtitles
            if typo_t >= 0.8:
                sub_prog = min(1.0, (typo_t - 0.8) / 1.0)
                sub_a = int(240 * ease_out_quad(sub_prog))
                
                # DIES NATALIS KE-44 SMAN 1 GEDEG
                draw.text(
                    (self.cx, self.y_sub + y_slide),
                    "DIES NATALIS KE-44 SMAN 1 GEDEG",
                    font=self.font_sub,
                    fill=(C_WHITE[0], C_WHITE[1], C_WHITE[2], sub_a),
                    anchor="mm"
                )
                
                # Kurun Waktu & Nilai: 1982—2026
                draw.text(
                    (self.cx, self.y_meta + y_slide),
                    "1982—2026 • ADHI DHARMA EKAPRAYA",
                    font=self.font_meta,
                    fill=(C_GOLD_DEEP[0], C_GOLD_DEEP[1], C_GOLD_DEEP[2], int(sub_a * 0.9)),
                    anchor="mm"
                )

        # =========================================================================
        # PHASE 5: CELESTIAL TWINKLE & AMBIENT STARDUST (8.5s - 11.0s)
        # =========================================================================
        if t >= 7.5:
            # Twinkle star glints on crown tip & wing tip
            twinkle_time = t - 7.5
            glint_pts = [
                (self.cx + int(self.logo_target_size * 0.16), self.cy_logo - int(self.logo_target_size * 0.28)),
                (self.cx - int(self.logo_target_size * 0.18), self.cy_logo - int(self.logo_target_size * 0.22)),
                (self.cx + int(self.logo_target_size * 0.25), self.cy_logo + int(self.logo_target_size * 0.05)),
            ]
            
            for idx, (gx, gy) in enumerate(glint_pts):
                phase = math.sin(twinkle_time * 5.0 + idx * 2.1)
                if phase > 0.3:
                    glint_sz = int(14 * (phase - 0.3) / 0.7)
                    glint_a = int(220 * (phase - 0.3) / 0.7)
                    # 4-pointed cross star
                    draw.line([(gx - glint_sz, gy), (gx + glint_sz, gy)], fill=(255, 255, 255, glint_a), width=2)
                    draw.line([(gx, gy - glint_sz), (gx, gy + glint_sz)], fill=(255, 255, 255, glint_a), width=2)
                    draw.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=(C_GOLD_BRIGHT[0], C_GOLD_BRIGHT[1], C_GOLD_BRIGHT[2], glint_a))

        # =========================================================================
        # IMPACT FLASH AT t = 4.5s
        # =========================================================================
        if 4.5 <= t <= 4.85:
            flash_prog = (t - 4.5) / 0.35
            flash_a = int(180 * (1.0 - flash_prog) ** 2.0)
            flash_overlay = Image.new("RGBA", (self.w, self.h), (255, 248, 220, flash_a))
            overlay = Image.alpha_composite(overlay, flash_overlay)

        # Composite PIL overlay onto OpenCV frame
        overlay_arr = np.array(overlay)
        alpha_mask = overlay_arr[:, :, 3] / 255.0
        
        # BGR blending
        for c_idx in range(3):
            # overlay_arr is RGBA (0:R, 1:G, 2:B) -> OpenCV is BGR (0:B, 1:G, 2:R)
            ch_overlay = overlay_arr[:, :, 2 - c_idx]
            frame_bgr[:, :, c_idx] = (frame_bgr[:, :, c_idx] * (1.0 - alpha_mask) + ch_overlay * alpha_mask).astype(np.uint8)

        # =========================================================================
        # FINAL CINEMATIC FADE TO BLACK (10.2s - 11.0s / last 24 frames)
        # =========================================================================
        if t >= 10.0:
            fade_prog = min(1.0, (t - 10.0) / 1.0)
            fade_factor = 1.0 - ease_in_out_quad(fade_prog)
            frame_bgr = (frame_bgr * fade_factor).astype(np.uint8)

        return frame_bgr

    def generate_video(self, output_path: str):
        print(f"\n[VIDEO GENERATOR] Memulai render: {self.name} ({self.w}x{self.h}) -> {output_path}")
        t_start = time.time()
        
        # mp4v codec is universally available in OpenCV on macOS
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, FPS, (self.w, self.h))
        
        if not out.isOpened():
            raise RuntimeError(f"Gagal membuka cv2.VideoWriter untuk {output_path}")

        for i in range(TOTAL_FRAMES):
            frame = self.render_frame(i)
            out.write(frame)
            
            if i % 60 == 0 or i == TOTAL_FRAMES - 1:
                pct = int((i + 1) / TOTAL_FRAMES * 100)
                elapsed = time.time() - t_start
                fps_render = (i + 1) / max(0.001, elapsed)
                print(f"  [{self.name}] Frame {i+1}/{TOTAL_FRAMES} ({pct}%) • Speed: {fps_render:.1f} fps")

        out.release()
        t_total = time.time() - t_start
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  Selesai! {output_path} ({file_size_mb:.2f} MB) dalam {t_total:.1f} detik.")

def main():
    print("=" * 70)
    print("PRODUKSI VIDEO LOGO REVEAL RESMI DIES NATALIS KE-44 SMAN 1 GEDEG")
    print("TEMA: AVERSA (TEATER AKBAR EMAS & BELUDRU UNGU)")
    print("=" * 70)
    
    os.makedirs("assets/video", exist_ok=True)
    
    configs = [
        {"name": "16:9 Lanskap", "w": 1920, "h": 1080, "path": "assets/video/logo_reveal_16x9.mp4"},
        {"name": "9:16 Vertikal", "w": 1080, "h": 1920, "path": "assets/video/logo_reveal_9x16.mp4"},
        {"name": "4:5 Portrait", "w": 1080, "h": 1350, "path": "assets/video/logo_reveal_4x5.mp4"},
    ]
    
    for cfg in configs:
        renderer = LogoRevealRenderer(cfg["w"], cfg["h"], cfg["name"])
        renderer.generate_video(cfg["path"])

    print("\n" + "=" * 70)
    print("SEMUA FORMAT VIDEO RESMI TELAH BERHASIL DIRENDER KE assets/video/")
    print("=" * 70)

if __name__ == "__main__":
    main()
