#!/usr/bin/env python3
"""
Generator Video 3D Logo Reveal Resmi Dies Natalis ke-44 SMAN 1 Gedeg (AVERSA)
Spesifikasi:
  - 3D Polished Gold Emblem dengan Smooth Bevels & Rim Lighting (Octane Render style)
  - Strict preservation of 100% exact vector geometry & proportions
  - Wordmark AVERSA diambil langsung dari aset resmi (aversa-standalone-color.png)
  - Clean Luxury Studio Backdrop: Deep Imperial Velvet (#1C0521), Center Violet Glow (#42084E)
  - Tanpa elemen garis/node pembatas yang mengganggu di tengah
  - Durasi: 11 Detik (330 frames @ 30 FPS)
  - Multi-Format: 4:5 (Instagram Feed), 16:9 (Lanskap Panggung/YouTube), 9:16 (Vertikal Reels/TikTok)
"""

import math
import os
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FPS = 30
DURATION_SEC = 11.0
TOTAL_FRAMES = int(DURATION_SEC * FPS) # 330 frames

FONT_JAKARTA_BOLD = "assets/fonts/plus-jakarta-sans/ttf/PlusJakartaSans-Bold.ttf"
FONT_JAKARTA_REG = "assets/fonts/plus-jakarta-sans/ttf/PlusJakartaSans-Regular.ttf"
LOGO_SYMBOL_PATH = "assets/png/logo-color-2048.png"
AVERSA_ASSET_PATH = "assets/png/aversa-standalone-color.png"

# Color constants (RGB)
C_VELVET_DARK = (15, 2, 20)
C_VELVET_MID = (38, 7, 45)
C_VELVET_PLUM = (66, 14, 78)
C_GOLD_BRIGHT = (255, 240, 185)
C_GOLD_PRIMARY = (245, 197, 56)
C_GOLD_DEEP = (224, 157, 23)
C_WHITE = (255, 255, 255)

def get_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def ease_out_cubic(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3

def ease_in_out_quad(t: float) -> float:
    return 2.0 * t * t if t < 0.5 else -1.0 + (4.0 - 2.0 * t) * t

def create_base_gradient(w: int, h: int, cy_glow: int) -> np.ndarray:
    """Precompute luxury deep velvet backdrop in BGR uint8 with violet center glow."""
    y, x = np.ogrid[:h, :w]
    cx = w / 2.0
    max_dist = math.sqrt(cx**2 + (h/2.0)**2)
    dist = np.sqrt((x - cx)**2 + (y - cy_glow)**2) / max_dist
    dist = np.clip(dist, 0.0, 1.0)
    
    b0, g0, r0 = C_VELVET_DARK[2], C_VELVET_DARK[1], C_VELVET_DARK[0]
    b1, g1, r1 = C_VELVET_PLUM[2], C_VELVET_PLUM[1], C_VELVET_PLUM[0]
    
    factor = np.power(dist, 1.35)
    b = (b1 * (1.0 - factor) + b0 * factor).astype(np.uint8)
    g = (g1 * (1.0 - factor) + g0 * factor).astype(np.uint8)
    r = (r1 * (1.0 - factor) + r0 * factor).astype(np.uint8)
    return np.dstack([b, g, r])

def compute_normal_map(rgba_img: Image.Image, bevel_px: float = 16.0) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Compute 3D surface normal map (nx, ny, nz) and alpha mask from RGBA image."""
    arr = np.array(rgba_img)
    alpha = arr[:, :, 3]
    
    # Distance transform for smooth bevels
    dist = cv2.distanceTransform((alpha > 64).astype(np.uint8), cv2.DIST_L2, 5)
    bevel = np.clip(dist / float(bevel_px), 0.0, 1.0)
    
    # Facet luminance
    gray = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    height = (bevel * 0.70 + gray * 0.30).astype(np.float32)
    
    dx = cv2.Sobel(height, cv2.CV_32F, 1, 0, ksize=3)
    dy = cv2.Sobel(height, cv2.CV_32F, 0, 1, ksize=3)
    nz_base = 0.28
    norm = np.sqrt(dx**2 + dy**2 + nz_base**2)
    
    nx = (-dx / norm).astype(np.float32)
    ny = (-dy / norm).astype(np.float32)
    nz = (nz_base / norm).astype(np.float32)
    
    return nx, ny, nz, alpha

def render_3d_shaded(base_rgb: np.ndarray, nx: np.ndarray, ny: np.ndarray, nz: np.ndarray, alpha: np.ndarray,
                     light_dir: np.ndarray, spec_power: float = 28.0, rim_intensity: float = 0.75) -> np.ndarray:
    """Render 3D Blinn-Phong shaded RGBA image with moving specular highlights and rim lighting."""
    L = light_dir / np.linalg.norm(light_dir)
    V = np.array([0.0, 0.0, 1.0], dtype=np.float32)
    H = L + V
    H /= np.linalg.norm(H)
    
    N_dot_L = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0.0, 1.0)
    N_dot_H = np.clip(nx * H[0] + ny * H[1] + nz * H[2], 0.0, 1.0)
    specular = np.power(N_dot_H, spec_power)
    rim = np.power(1.0 - np.clip(nz, 0.0, 1.0), 2.2) * (alpha > 32).astype(np.float32)
    
    base_f = base_rgb.astype(np.float32)
    # Ambient + Diffuse (warm gold shading)
    shaded = base_f * (0.35 + 0.65 * N_dot_L[:, :, None])
    # Intense specular gleam (polished glossy gold)
    spec_col = np.array([255.0, 248.0, 210.0], dtype=np.float32)
    shaded += specular[:, :, None] * spec_col * 1.15
    # Edge rim lighting
    rim_col = np.array([255.0, 235.0, 170.0], dtype=np.float32)
    shaded += rim[:, :, None] * rim_col * rim_intensity
    
    shaded_u8 = np.clip(shaded, 0, 255).astype(np.uint8)
    return np.dstack([shaded_u8, alpha])

def get_3d_warp(rgba_img: np.ndarray, yaw_deg: float, pitch_deg: float, f: float = 1500.0) -> np.ndarray:
    """Apply true 3D perspective rotation (yaw, pitch) using perspective projection."""
    h, w = rgba_img.shape[:2]
    rad_y = np.radians(yaw_deg)
    rad_x = np.radians(pitch_deg)
    
    Rx = np.array([[1.0, 0.0, 0.0], [0.0, np.cos(rad_x), -np.sin(rad_x)], [0.0, np.sin(rad_x), np.cos(rad_x)]])
    Ry = np.array([[np.cos(rad_y), 0.0, np.sin(rad_y)], [0.0, 1.0, 0.0], [-np.sin(rad_y), 0.0, np.cos(rad_y)]])
    R = Ry @ Rx
    
    corners = np.array([
        [-w/2.0, -h/2.0, 0.0],
        [ w/2.0, -h/2.0, 0.0],
        [ w/2.0,  h/2.0, 0.0],
        [-w/2.0,  h/2.0, 0.0]
    ])
    
    rot_corners = (R @ corners.T).T
    proj_corners = np.zeros((4, 2), dtype=np.float32)
    for i in range(4):
        z = rot_corners[i, 2] + f
        proj_corners[i, 0] = (rot_corners[i, 0] * f / z) + w/2.0
        proj_corners[i, 1] = (rot_corners[i, 1] * f / z) + h/2.0
        
    src_corners = np.array([[0.0, 0.0], [w, 0.0], [w, h], [0.0, h]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(src_corners, proj_corners)
    return cv2.warpPerspective(rgba_img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))

class LogoReveal3DRenderer:
    def __init__(self, width: int, height: int, name: str):
        self.w = width
        self.h = height
        self.name = name
        self.cx = width // 2
        
        # Framing configuration per ratio
        if width == 1080 and height == 1350:  # 4:5 HERO SHOT
            self.cy_emblem = int(height * 0.40)
            self.emblem_sz = int(width * 0.62)
            self.cy_aversa = int(height * 0.72)
            self.aversa_w = int(width * 0.56)
            self.y_sub = int(height * 0.82)
            self.y_meta = int(height * 0.865)
            self.font_sub_size = 23
            self.font_meta_size = 18
        elif width > height:  # 16:9
            self.cy_emblem = int(height * 0.42)
            self.emblem_sz = int(height * 0.56)
            self.cy_aversa = int(height * 0.76)
            self.aversa_w = int(height * 0.45)
            self.y_sub = int(height * 0.86)
            self.y_meta = int(height * 0.905)
            self.font_sub_size = int(height * 0.028)
            self.font_meta_size = int(height * 0.021)
        else:  # 9:16
            self.cy_emblem = int(height * 0.40)
            self.emblem_sz = int(width * 0.72)
            self.cy_aversa = int(height * 0.66)
            self.aversa_w = int(width * 0.65)
            self.y_sub = int(height * 0.75)
            self.y_meta = int(height * 0.795)
            self.font_sub_size = int(width * 0.040)
            self.font_meta_size = int(width * 0.030)

        self.font_sub = get_font(FONT_JAKARTA_BOLD, self.font_sub_size)
        self.font_meta = get_font(FONT_JAKARTA_REG, self.font_meta_size)

        # Base velvet backdrop
        self.bg_bgr = create_base_gradient(self.w, self.h, self.cy_emblem)

        # 1. Prepare 3D Emblem
        raw_logo = Image.open(LOGO_SYMBOL_PATH).convert("RGBA")
        self.emblem_pil = raw_logo.resize((self.emblem_sz, self.emblem_sz), Image.Resampling.LANCZOS)
        self.emblem_rgb = np.array(self.emblem_pil)[:, :, :3]
        self.e_nx, self.e_ny, self.e_nz, self.e_alpha = compute_normal_map(self.emblem_pil, bevel_px=14.0)

        # 2. Prepare 3D AVERSA Wordmark (Crop exact asset bounding box)
        raw_aversa = Image.open(AVERSA_ASSET_PATH).convert("RGBA")
        bbox = raw_aversa.getbbox()
        cropped_aversa = raw_aversa.crop(bbox) if bbox else raw_aversa
        self.aversa_h = int(self.aversa_w * cropped_aversa.size[1] / cropped_aversa.size[0])
        self.aversa_pil = cropped_aversa.resize((self.aversa_w, self.aversa_h), Image.Resampling.LANCZOS)
        self.aversa_rgb = np.array(self.aversa_pil)[:, :, :3]
        self.a_nx, self.a_ny, self.a_nz, self.a_alpha = compute_normal_map(self.aversa_pil, bevel_px=8.0)

        # Floating Energy Dust Particles (Octane ambient field)
        np.random.seed(44)
        self.num_particles = 140
        self.particles = []
        for _ in range(self.num_particles):
            self.particles.append({
                "x": np.random.uniform(0, self.w),
                "y": np.random.uniform(0, self.h),
                "speed_y": np.random.uniform(-0.4, -1.2),
                "drift_x": np.random.uniform(-0.3, 0.3),
                "size": np.random.randint(2, 5),
                "alpha": np.random.uniform(0.2, 0.75),
                "color": [C_GOLD_BRIGHT, C_GOLD_PRIMARY, C_WHITE][np.random.choice([0, 1, 2])]
            })

    def render_frame(self, frame_idx: int) -> np.ndarray:
        t = frame_idx / float(FPS)
        frame_bgr = self.bg_bgr.copy()
        
        # PIL overlay for text and particles
        overlay = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # =========================================================================
        # 1. FLOATING GOLDEN ENERGY DUST PARTICLES (Continuous subtle movement)
        # =========================================================================
        for p in self.particles:
            cur_x = (p["x"] + p["drift_x"] * frame_idx) % self.w
            cur_y = (p["y"] + p["speed_y"] * frame_idx) % self.h
            sz = p["size"]
            c = p["color"]
            a = int(255 * p["alpha"])
            # Fade out at the very end
            if t >= 10.0:
                a = int(a * max(0.0, 1.0 - (t - 10.0)))
            draw.ellipse([cur_x - sz, cur_y - sz, cur_x + sz, cur_y + sz], fill=(c[0], c[1], c[2], a))

        # =========================================================================
        # 2. 3D EMBLEM PERSPECTIVE & BLINN-PHONG STUDIO LIGHTING
        # =========================================================================
        # Dynamic Light Direction moving across the emblem:
        # Sweeps from left (-0.85) to right (+0.75)
        sweep_x = -0.85 + (t / 11.0) * 1.6
        light_dir = np.array([sweep_x, -0.65, 0.85], dtype=np.float32)

        # 3D Spatial Angles (Yaw & Pitch)
        if t < 2.0:
            # Subtle hovering in void
            yaw = -20.0 + math.sin(t * 1.5) * 1.5
            pitch = 8.0 + math.cos(t * 1.5) * 1.0
            scale_emblem = 0.92
            alpha_emblem = min(1.0, t / 1.5) * 0.35 # Mysterious silhouette glow
            rim_power = 1.2
        elif 2.0 <= t < 4.5:
            # Rising tension, slowly rotating toward camera
            prog = (t - 2.0) / 2.5
            yaw = -20.0 * (1.0 - ease_in_out_quad(prog) * 0.5)
            pitch = 8.0 * (1.0 - ease_in_out_quad(prog) * 0.5)
            scale_emblem = 0.92 + 0.08 * ease_in_out_quad(prog)
            alpha_emblem = 0.35 + 0.65 * ease_out_cubic(prog)
            rim_power = 1.0
        else: # t >= 4.5
            # Reveal moment: emblem swings smoothly to frontal (0 deg) with soft spring settling
            dt_rev = t - 4.5
            decay = math.exp(-dt_rev * 2.8)
            yaw = -10.0 * decay * math.cos(dt_rev * 5.0)
            pitch = 4.0 * decay * math.cos(dt_rev * 5.0)
            scale_emblem = 1.0 + 0.08 * math.exp(-dt_rev * 3.5) * math.cos(dt_rev * 8.0)
            alpha_emblem = 1.0
            rim_power = 0.8

        # Render 3D Shaded Emblem
        shaded_emblem = render_3d_shaded(
            self.emblem_rgb, self.e_nx, self.e_ny, self.e_nz, self.e_alpha,
            light_dir, spec_power=30.0, rim_intensity=rim_power
        )

        # Apply 3D Perspective Warp
        warped_emblem = get_3d_warp(shaded_emblem, yaw_deg=yaw, pitch_deg=pitch, f=1600.0)

        # Apply Scaling & Opacity
        if scale_emblem != 1.0 or alpha_emblem < 1.0:
            new_w = max(10, int(self.emblem_sz * scale_emblem))
            new_h = max(10, int(self.emblem_sz * scale_emblem))
            warped_pil = Image.fromarray(warped_emblem).resize((new_w, new_h), Image.Resampling.LANCZOS)
            if alpha_emblem < 1.0:
                w_arr = np.array(warped_pil)
                w_arr[:, :, 3] = (w_arr[:, :, 3] * alpha_emblem).astype(np.uint8)
                warped_pil = Image.fromarray(w_arr)
        else:
            warped_pil = Image.fromarray(warped_emblem)

        # Paste Emblem centered at (cx, cy_emblem)
        ew, eh = warped_pil.size
        overlay.paste(warped_pil, (self.cx - ew // 2, self.cy_emblem - eh // 2), mask=warped_pil.split()[3])

        # =========================================================================
        # 3. IMPACT SHOCKWAVE PULSE AT t = 4.5s
        # =========================================================================
        if 4.5 <= t <= 6.2:
            sw_prog = min(1.0, max(0.0, (t - 4.5) / 1.7))
            sw_r = int(sw_prog * self.w * 0.65)
            sw_a = int(220 * (max(0.0, 1.0 - sw_prog) ** 1.8))
            sw_w = max(2, int(6 * max(0.0, 1.0 - sw_prog)))
            if sw_a > 0 and sw_r > 0:
                draw.ellipse(
                    [self.cx - sw_r, self.cy_emblem - sw_r, self.cx + sw_r, self.cy_emblem + sw_r],
                    outline=(C_GOLD_BRIGHT[0], C_GOLD_BRIGHT[1], C_GOLD_BRIGHT[2], sw_a),
                    width=sw_w
                )


        # =========================================================================
        # 4. 3D AVERSA WORDMARK (REVEAL FROM ASET RESMI)
        # =========================================================================
        if t >= 6.0:
            av_t = t - 6.0
            av_alpha = min(1.0, av_t / 1.0)
            av_y_slide = int(16 * (1.0 - ease_out_cubic(min(1.0, av_t / 1.2))))
            
            # 3D Shaded AVERSA with subtle moving light sweep
            av_light = np.array([sweep_x * 0.7, -0.6, 0.8], dtype=np.float32)
            shaded_aversa = render_3d_shaded(
                self.aversa_rgb, self.a_nx, self.a_ny, self.a_nz, self.a_alpha,
                av_light, spec_power=24.0, rim_intensity=0.5
            )
            
            aversa_frame_pil = Image.fromarray(shaded_aversa)
            if av_alpha < 1.0:
                av_arr = np.array(aversa_frame_pil)
                av_arr[:, :, 3] = (av_arr[:, :, 3] * av_alpha).astype(np.uint8)
                aversa_frame_pil = Image.fromarray(av_arr)
            
            cur_y_aversa = self.cy_aversa + av_y_slide
            overlay.paste(
                aversa_frame_pil,
                (self.cx - self.aversa_w // 2, cur_y_aversa - self.aversa_h // 2),
                mask=aversa_frame_pil.split()[3]
            )

            # =====================================================================
            # 5. SUBTITLE & IDENTITY TEXT (Clean, Minimalist, No Middle Clutter)
            # =====================================================================
            if av_t >= 0.6:
                sub_p = min(1.0, (av_t - 0.6) / 0.8)
                sub_a = int(245 * ease_out_cubic(sub_p))
                
                # Subtitle: DIES NATALIS KE-44 SMAN 1 GEDEG
                draw.text(
                    (self.cx, self.y_sub + av_y_slide),
                    "DIES NATALIS KE-44 SMAN 1 GEDEG",
                    font=self.font_sub,
                    fill=(C_WHITE[0], C_WHITE[1], C_WHITE[2], sub_a),
                    anchor="mm"
                )
                
                # Meta: 1982—2026
                draw.text(
                    (self.cx, self.y_meta + av_y_slide),
                    "1982—2026",
                    font=self.font_meta,
                    fill=(C_GOLD_PRIMARY[0], C_GOLD_PRIMARY[1], C_GOLD_PRIMARY[2], int(sub_a * 0.9)),
                    anchor="mm"
                )

        # =========================================================================
        # 6. CELESTIAL TWINKLE GLINTS (8.0s - 11.0s)
        # =========================================================================
        if t >= 8.0:
            tw_t = t - 8.0
            # Key sparkle positions on eagle crown & wings
            glints = [
                (self.cx + int(self.emblem_sz * 0.16), self.cy_emblem - int(self.emblem_sz * 0.28)),
                (self.cx - int(self.emblem_sz * 0.18), self.cy_emblem - int(self.emblem_sz * 0.22)),
                (self.cx + int(self.emblem_sz * 0.25), self.cy_emblem + int(self.emblem_sz * 0.05)),
            ]
            for idx, (gx, gy) in enumerate(glints):
                ph = math.sin(tw_t * 5.0 + idx * 2.1)
                if ph > 0.35:
                    sz = int(14 * (ph - 0.35) / 0.65)
                    ga = int(240 * (ph - 0.35) / 0.65)
                    draw.line([(gx - sz, gy), (gx + sz, gy)], fill=(255, 255, 255, ga), width=2)
                    draw.line([(gx, gy - sz), (gx, gy + sz)], fill=(255, 255, 255, ga), width=2)
                    draw.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=(C_GOLD_BRIGHT[0], C_GOLD_BRIGHT[1], C_GOLD_BRIGHT[2], ga))

        # Composite PIL overlay onto OpenCV BGR frame
        overlay_arr = np.array(overlay)
        alpha_mask = overlay_arr[:, :, 3] / 255.0
        
        for c_idx in range(3):
            ch_overlay = overlay_arr[:, :, 2 - c_idx]
            frame_bgr[:, :, c_idx] = (frame_bgr[:, :, c_idx] * (1.0 - alpha_mask) + ch_overlay * alpha_mask).astype(np.uint8)

        # =========================================================================
        # 7. FINAL CINEMATIC FADE TO BLACK (10.2s - 11.0s)
        # =========================================================================
        if t >= 10.2:
            fade_p = min(1.0, (t - 10.2) / 0.8)
            fade_f = 1.0 - ease_in_out_quad(fade_p)
            frame_bgr = (frame_bgr * fade_f).astype(np.uint8)

        return frame_bgr

    def generate_video(self, output_path: str):
        print(f"\n[VIDEO 3D GENERATOR] Merender format: {self.name} ({self.w}x{self.h}) -> {output_path}")
        t_start = time.time()
        
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
    print("=" * 75)
    print("PRODUKSI VIDEO 3D LOGO REVEAL RESMI DIES NATALIS KE-44 SMAN 1 GEDEG")
    print("TEMA: AVERSA (3D POLISHED GOLD EMBLEM & ROYAL PURPLE STUDIO BACKDROP)")
    print("=" * 75)
    
    os.makedirs("assets/video", exist_ok=True)
    
    configs = [
        {"name": "4:5 Portrait (Hero Shot)", "w": 1080, "h": 1350, "path": "assets/video/logo_reveal_4x5.mp4"},
        {"name": "16:9 Lanskap", "w": 1920, "h": 1080, "path": "assets/video/logo_reveal_16x9.mp4"},
        {"name": "9:16 Vertikal", "w": 1080, "h": 1920, "path": "assets/video/logo_reveal_9x16.mp4"},
    ]
    
    for cfg in configs:
        renderer = LogoReveal3DRenderer(cfg["w"], cfg["h"], cfg["name"])
        renderer.generate_video(cfg["path"])

    print("\n" + "=" * 75)
    print("SEMUA FORMAT VIDEO 3D TELAH BERHASIL DIRENDER KE assets/video/")
    print("=" * 75)

if __name__ == "__main__":
    main()
