# BITSCTF: AES 4-Round Key Recovery Write-up

## 🚩 Challenge Overview
The challenge provides a custom Python implementation of AES reduced to **4 rounds**. We are given an `output.txt` file containing:
* An **encrypted flag** (hex string).
* A **key_hint** (13 bytes provided).
* **1000 plaintext-ciphertext samples**.

---

## 🕵️ Step 1: Initial Analysis
The provided `aes.py` script implements a standard AES structure—`SubBytes`, `ShiftRows`, `MixColumns`, and `AddRoundKey`—but strictly limits execution to 4 rounds. 

The `key_hint` provided is `26ab77cadcca0ed41b03c8f2e5`. 
* **Hint Length:** 26 hex characters = **13 bytes**.
* **AES Key Requirement:** 16 bytes.
* **Missing Data:** 3 bytes ($2^{24}$ combinations).

---

## 💡 Step 2: Bypassing the "Square Attack" Red Herring
A 4-round AES implementation paired with exactly 1000 samples is the classic textbook setup for a **Square Attack** (Integral Cryptanalysis). However, this relies on finding specific byte invariants, which can be brittle if the samples aren't perfectly structured.

Since we are only missing 3 bytes, there are only $256^3$ (roughly 16.7 million) possible combinations. A **Known-Plaintext Brute-Force** attack is completely viable, faster to implement, and less prone to parsing errors than complex mathematical cryptanalysis.

| Metric | Value |
| :--- | :--- |
| **Total Combinations** | $256^3 = 16,777,216$ |
| **Complexity** | $\approx 2^{24}$ (Low for modern CPUs) |
| **Strategy** | Multiprocessing Brute-Force |

---

## 🛠️ Step 3: Implementation
Because pure Python bitwise operations are slow, we utilized the `multiprocessing` library to distribute the search space across all available CPU cores. The logic involves iterating through the missing 3 bytes and checking them against a known plaintext-ciphertext pair.

*(See `sol.py` for the full implementation)*

---

## 🔑 Step 4: Key Recovery & Decryption
The script was executed using 20 CPU cores and successfully matched the ciphertext.

* **Search Time:** 1562.8 seconds (~26 minutes).
* **Recovered Full Key:** `26ab77cadcca0ed41b03c8f2e5cdec0c`
* **Decryption Process:** We initialized the custom `AES` class with the recovered 16-byte key to decrypt the `encrypted_flag` hex string.

### 🏆 Final Flag
> `BITSCTF{7h3_qu1ck_br0wn_f0x_jump5_0v3r_7h3_l4zy_d0g}`

---

## 🧰 Tools Used
* **Python (multiprocessing):** To automate the concurrent Known-Plaintext attack.
* **Custom AES Script:** Reusing the challenge creator's exact Python classes to ensure perfect 1:1 encryption/decryption logic.