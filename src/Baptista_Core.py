#!/usr/bin/env python3
from typing import List, Tuple

def skew_tent_map(x: float, p: float) -> float:
    """
    Iterates the Skew Tent Map.
    Provides a completely uniform invariant density over [0, 1], 
    unlike the U-shaped distribution of the Logistic Map.
    """
    if 0.0 < x < p:
        return x / p
    elif p <= x < 1.0:
        return (1.0 - x) / (1.0 - p)
    return 0.0

def get_phase_interval(x: float, num_bins: int = 256) -> int:
    """
    Discretizes the continuous phase space [0, 1) into discrete intervals.
    Maps the chaotic state x to an 8-bit integer symbol.
    """
    return int(x * num_bins)

def generate_mask(x: float) -> int:
    """
    Extracts an 8-bit pseudo-random mask from the chaotic state.
    Multiplication shifts the chaotic decimal digits into integer range.
    """
    return int((x * 10**14)) % 256

def encrypt_rectified(plaintext: bytes, x0: float, p: float, eta: int = 50) -> List[Tuple[int, int]]:
    """
    Modified Baptista Encryption.
    Outputs a 2-tuple (Masked_C, Mask) to resolve decryption collision defects 
    while enforcing a uniform ciphertext distribution via XOR masking.
    
    :param plaintext: Raw bytes of the message.
    :param x0: Initial chaotic state (Key).
    :param p: Control parameter for Skew Tent Map.
    :param eta: Minimum iteration threshold to ensure sufficient mixing.
    """
    ciphertext = []
    x = x0
    
    for byte in plaintext:
        c = 0
        while True:
            x = skew_tent_map(x, p)
            c += 1
            # Wait for hitting time (C) exceeding the eta threshold
            if c > eta and get_phase_interval(x) == byte:
                break
        
        # B[C]: Generate mask from the definitive hitting state
        mask = generate_mask(x)
        
        # XOR masking to flatten the exponential decay distribution of C
        masked_c = c ^ mask
        
        ciphertext.append((masked_c, mask))
        
    return ciphertext

def decrypt_rectified(ciphertext: List[Tuple[int, int]], x0: float, p: float) -> bytes:
    """
    Modified Baptista Decryption.
    By isolating the mask in the 2-tuple, the exact iteration count C is 
    recovered deterministically before iterating the map, preventing the 
    Lyapunov exponent from amplifying state-drift errors.
    """
    plaintext = bytearray()
    x = x0
    
    for masked_c, mask in ciphertext:
        # Resolve collision defect: Unmask C accurately before map iteration
        c = masked_c ^ mask
        
        # Advance the dynamical system by exactly C steps
        for _ in range(c):
            x = skew_tent_map(x, p)
            
        plaintext.append(get_phase_interval(x))
        
    return bytes(plaintext)
