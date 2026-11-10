# Author preparation history

`construct_candidate.py` records adaptation of candidate-author helper scripts from the prior EXP-161 preparation. It did not read, copy or pin independent reviewer artifacts. The prepared EXP-104 scripts, data and reports in the parent directory are the authoritative handoff; this one-time adapter is not a regeneration entry point.

The first static run failed only the two settle-pose lash-travel comparisons. `is_equal_approx` was too tight for subtraction of float32 node positions near 400 source pixels: an intended 1.08-pixel travel was measured as 1.07998657226562. Its actual error is approximately 1.343e-5 source pixels. Both the motion check and separate Python geometry check already used 1e-4 absolute tolerance. The static assertion now uses that same bounded absolute tolerance. Both original failed receipts remain here. The frozen runtime, art and candidate controls were not changed.
