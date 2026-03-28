
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
from pathlib import Path

def generate_ltsa_trailer():
    print("🎬 Generating LTSA Video Trailer (v2)...")
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#020617')
    ax.set_facecolor('#020617')

    # Text elements for trailer
    title_text = ax.text(0.5, 0.7, "LTSA SUITE v2.0", ha='center', color='#64ffda', fontsize=24, fontweight='bold', alpha=0)
    subtitle_text = ax.text(0.5, 0.5, "Sovereign Patient Safety", ha='center', color='#94a3b8', fontsize=18, alpha=0)
    tagline_text = ax.text(0.5, 0.3, "Civilization Secured.", ha='center', color='#64ffda', fontsize=16, alpha=0)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    def animate(i):
        # Fade in sequence
        if i < 30: title_text.set_alpha(i/30.0)
        elif i < 60: subtitle_text.set_alpha((i-30)/30.0)
        elif i < 90: tagline_text.set_alpha((i-60)/30.0)
        return title_text, subtitle_text, tagline_text

    ani = animation.FuncAnimation(fig, animate, frames=120, interval=50, blit=True)

    filename = "outputs_v2/ltsa_trailer.mp4"
    try:
        ani.save(filename, writer='ffmpeg', fps=24)
        print(f"✅ Trailer saved to: {filename}")
    except:
        ani.save(filename.replace('.mp4', '.gif'), writer='pillow', fps=24)
        print(f"✅ Fallback Trailer GIF saved to: {filename.replace('.mp4', '.gif')}")
    plt.close()

if __name__ == "__main__":
    generate_ltsa_trailer()
