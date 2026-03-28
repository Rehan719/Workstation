
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
from pathlib import Path

def generate_ltsa_trailer_final():
    print("🎬 Generating Final LTSA Video Trailer (v3)...")
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='#010411')
    ax.set_facecolor('#010411')

    # Text elements for final trailer
    title_text = ax.text(0.5, 0.7, "LTSA SUITE v3.0", ha='center', color='#64ffda', fontsize=28, fontweight='bold', alpha=0)
    subtitle_text = ax.text(0.5, 0.5, "The Definitive Sovereign Standard", ha='center', color='#94a3b8', fontsize=20, alpha=0)
    tagline_text = ax.text(0.5, 0.3, "Civilization Secured. 2026.", ha='center', color='#64ffda', fontsize=18, alpha=0)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    def animate(i):
        # Fade in sequence
        if i < 30: title_text.set_alpha(i/30.0)
        elif i < 60: subtitle_text.set_alpha((i-30)/30.0)
        elif i < 90: tagline_text.set_alpha((i-60)/30.0)
        return title_text, subtitle_text, tagline_text

    ani = animation.FuncAnimation(fig, animate, frames=150, interval=40, blit=True)

    filename = "outputs_final/ltsa_trailer.mp4"
    try:
        ani.save(filename, writer='ffmpeg', fps=25)
        print(f"✅ Final Trailer saved to: {filename}")
    except:
        ani.save(filename.replace('.mp4', '.gif'), writer='pillow', fps=25)
        print(f"✅ Fallback Final Trailer GIF saved to: {filename.replace('.mp4', '.gif')}")
    plt.close()

if __name__ == "__main__":
    generate_ltsa_trailer_final()
