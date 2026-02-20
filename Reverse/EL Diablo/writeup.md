# EL DIABLO

---

## Approach

The challenge provides a UPX-packed, stripped ELF binary containing a heavily guarded custom Virtual Machine (VM). The flag is decrypted by the VM using a user-provided license key. Instead of manually reversing the custom VM's architecture and cryptographic algorithm, we use dynamic instrumentation and an `LD_PRELOAD` hook to bypass the anti-debugging checks, force the VM to execute, and leak the garbled plaintext to reconstruct the flag.

### Step 1: Initial Analysis

- Ran `strings` and `file` on the provided executable, revealing `UPX!` section headers which indicated the binary was compressed.
- Unpacked the executable using `upx -d challenge -o challenge_unpacked`.
- Inspected the unpacked binary: it is a stripped 64-bit ELF executable, meaning symbol names were removed.
- Dynamic tracing with `ltrace` revealed the program expects a license file starting with the prefix `LICENSE-` followed by a 16-character hex string (which it parses into 8 raw bytes).

### Step 2: Core Technique

- **Dynamic analysis / hook injection** — rather than statically patching every anti-debug check in Ghidra, we use `LD_PRELOAD` to hook library calls and bypass execution restrictions.
- The binary employs an aggressive anti-debugging gauntlet before validation: it checks `/proc/version` for WSL, attempts `ptrace(PTRACE_TRACEME)`, reads `/proc/self/status` for a non-zero `TracerPid`, measures execution time to catch manual stepping (`clock_gettime`), and checks its parent process name for debuggers.
- Key observation: If the environment is deemed "clean," the binary intentionally executes an illegal instruction (`SIGILL`). A custom signal handler catches this crash and boots up the custom Virtual Machine ("React" exception-based control flow) to process the license and decrypt the flag.

### Step 3: Implementation

- Created a dummy license file: `echo -n "LICENSE-1234567890ABCDEF" > real.lic`
- Bypassed the anti-debug gauntlet using a custom library (`fake.so`) injected via `LD_PRELOAD`. 
- Leveraged a hidden debug environment variable (`PRINT_FLAG_CHAR=1`) found during static analysis to force the VM to print its output.
- Executed the binary to trigger the VM bypass:

  ```bash
  sudo env PRINT_FLAG_CHAR=1 LD_PRELOAD=./fake.so ./challenge_unpacked.1 real.lic