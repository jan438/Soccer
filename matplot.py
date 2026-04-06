import matplotlib.pyplot as plt
import numpy as np

def get_distinct_colors(n):
    """
    Generate up to n visually distinct colors using matplotlib categorical colormaps.
    Falls back to HSV evenly spaced colors if n > available.
    """
    # Combine tab20, tab20b, tab20c (each has 20 colors, but some overlap)
    cmap_names = ['tab20', 'tab20b', 'tab20c']
    colors = []
    for cmap_name in cmap_names:
        cmap = plt.get_cmap(cmap_name)
        colors.extend([cmap(i) for i in range(cmap.N)])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_colors = []
    for c in colors:
        if c not in seen:
            seen.add(c)
            unique_colors.append(c)
    
    # If more colors are needed, generate from HSV evenly spaced
    if n > len(unique_colors):
        extra_needed = n - len(unique_colors)
        hsv_colors = plt.cm.hsv(np.linspace(0, 1, extra_needed, endpoint=False))
        unique_colors.extend(hsv_colors)
    
    return unique_colors[:n]

# Example: Get 48 distinct colors
colors_48 = get_distinct_colors(48)

# Display them
fig, ax = plt.subplots(figsize=(12, 2))
for i, color in enumerate(colors_48):
    ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
ax.set_xlim(0, 48)
ax.set_ylim(0, 1)
ax.axis('off')
plt.show()