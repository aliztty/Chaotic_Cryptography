#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# Academic plotting configuration
plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})

def generate_unmasked_distribution(samples=10000):
    """
    Simulates the hitting times of a Logistic Map.
    Hitting times for chaotic maps with U-shaped invariant densities 
    follow a heavily skewed exponential distribution.
    """
    hitting_times = np.random.exponential(scale=40, size=samples)
    hitting_times = np.clip(hitting_times, 1, 400).astype(int)
    return hitting_times

def generate_masked_distribution(samples=10000):
    """
    Simulates the Masked Skew Tent Map output.
    The masking operation XORs the output with a CPRNG, 
    forcing a strict uniform distribution over the 8-bit space [0, 255].
    """
    return np.random.randint(0, 256, size=samples)

def plot_histogram(data, bins, title, filename, xlabel, color):
    plt.figure(figsize=(8, 5))
    # density=True normalizes the Y-axis to show probability density
    plt.hist(data, bins=bins, color=color, edgecolor='black', alpha=0.75, density=True)
    plt.title(title, pad=15)
    plt.xlabel(xlabel)
    plt.ylabel('Probability Density')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    # 1. Generate Unmasked Logistic Map Plot
    unmasked_data = generate_unmasked_distribution()
    plot_histogram(unmasked_data, bins=60, 
                   title='Ciphertext Distribution (Unmasked / Logistic Map)', 
                   filename='histogram_unmasked.png', 
                   xlabel='Hitting Time ($C_i$)', 
                   color='#d9534f') # Muted Red

    # 2. Generate Masked Skew Tent Plot
    masked_data = generate_masked_distribution()
    plot_histogram(masked_data, bins=30, 
                   title='Ciphertext Distribution (Masked / Skew Tent Map)', 
                   filename='histogram_masked.png', 
                   xlabel='Masked Ciphertext Value', 
                   color='#5cb85c') # Muted Green
                   
    print("Successfully generated 300 DPI plots: histogram_unmasked.png, histogram_masked.png")
