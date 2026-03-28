
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
from pathlib import Path

def generate_animation_v2(name, title, script_func, filename):
    """Generates a simple matplotlib animation and saves as mp4."""
    print(f"🎬 Generating Animation: {name} ({filename})...")
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_title(title, color='#64ffda', fontsize=16)

    line, = ax.plot([], [], lw=3, color='#64ffda')
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 100)
    ax.tick_params(colors='#94a3b8')
    for spine in ax.spines.values():
        spine.set_color('#334155')

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        x, y = script_func(i)
        line.set_data(x, y)
        return line,

    # 100 frames, 50ms interval = 5 seconds
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=50, blit=True)

    try:
        ani.save(filename, writer='ffmpeg', fps=20, extra_args=['-vcodec', 'libx264'])
        print(f"✅ Animation saved to: {filename}")
    except Exception as e:
        print(f"⚠️ FFMPEG Error for {filename}: {e}. Saving as GIF as fallback.")
        ani.save(filename.replace('.mp4', '.gif'), writer='pillow', fps=20)
        print(f"✅ Fallback GIF saved to: {filename.replace('.mp4', '.gif')}")
    plt.close()

# Scripts for animations
def immune_timeline_script(i):
    x = np.linspace(0, 24, 1000)
    # Peak at 24 months (i controls the progress)
    progress = i / 100.0
    # Two peaks: initial (0-2) and late (18-24)
    y1 = 80 * np.exp(-((x - 1)**2) / 2)
    y2 = 60 * np.exp(-((x - 22)**2) / 4)
    y = (y1 + y2) * progress
    return x[:int(progress*1000)], y[:int(progress*1000)]

def aav_transduction_script(i):
    # Sinusoidal transduction across tissues
    x = np.linspace(0, 10, 1000)
    progress = i / 100.0
    y = 50 + 40 * np.sin(x + i*0.1) * progress
    return x[:int(progress*1000)], y[:int(progress*1000)]

def main():
    out_dir = Path("outputs/v2/presentation/videos")
    out_dir.mkdir(parents=True, exist_ok=True)

    generate_animation_v2("Immune Timeline", "Timeline of Delayed Cytokine Perturbation", immune_timeline_script, str(out_dir / "immune_timeline.mp4"))
    generate_animation_v2("AAV Transduction", "Mechanism of AAV Germline Transduction", aav_transduction_script, str(out_dir / "aav_transduction.mp4"))

if __name__ == "__main__":
    main()
