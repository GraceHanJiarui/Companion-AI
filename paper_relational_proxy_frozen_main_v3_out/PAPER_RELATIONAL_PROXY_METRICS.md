# Relational Proxy Metrics

This file reports heuristic automatic proxies for trajectory instability.

These proxies are not treated as ground-truth coherence metrics.
They are intended as structured secondary diagnostics alongside judge-based evaluation.

## Heuristic definitions

- `length_spike`: current reply length is at least 1.8x the previous turn and at least 40 chars longer
- `warmth_jump`: absolute change in warmth-marker count >= 2
- `unexpected_polarity_flip`: polarity score flips sign with magnitude change >= 2
- `unsupported_initiative_jump`: user expresses cooling / boundary cue and assistant initiative score jumps by >= 2
- `abrupt_shift_proxy`: at least two heuristic votes, or any polarity flip / unsupported initiative jump

## Global summary

### baseline_relational_instruction
- num_turns: 180
- avg_reply_len_chars: 94.18
- avg_warmth_score: 0.1
- avg_initiative_score: 0.822
- avg_meta_control_score: 0.95
- length_spike_turns: 41
- warmth_jump_turns: 3
- unexpected_polarity_flip_turns: 4
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 4

### explicit_rel_state_rel_to_interface_i7
- num_turns: 180
- avg_reply_len_chars: 31.18
- avg_warmth_score: 0.089
- avg_initiative_score: 0.006
- avg_meta_control_score: 0.822
- length_spike_turns: 25
- warmth_jump_turns: 0
- unexpected_polarity_flip_turns: 3
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 3

### explicit_rel_state_projected_oracle_i7
- num_turns: 180
- avg_reply_len_chars: 37.45
- avg_warmth_score: 0.144
- avg_initiative_score: 0.022
- avg_meta_control_score: 0.75
- length_spike_turns: 21
- warmth_jump_turns: 2
- unexpected_polarity_flip_turns: 3
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 4
