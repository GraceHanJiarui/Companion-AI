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
- num_turns: 60
- avg_reply_len_chars: 114.4
- avg_warmth_score: 0.483
- avg_initiative_score: 1
- avg_meta_control_score: 0.583
- length_spike_turns: 11
- warmth_jump_turns: 4
- unexpected_polarity_flip_turns: 1
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 1

### baseline_relational_instruction_to_interface_i7_sc_vA
- num_turns: 60
- avg_reply_len_chars: 46.98
- avg_warmth_score: 0.317
- avg_initiative_score: 0.25
- avg_meta_control_score: 0.667
- length_spike_turns: 8
- warmth_jump_turns: 4
- unexpected_polarity_flip_turns: 1
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 1

### explicit_rel_state_rel_to_interface_i7_sc_vA
- num_turns: 60
- avg_reply_len_chars: 21.78
- avg_warmth_score: 0.433
- avg_initiative_score: 0.017
- avg_meta_control_score: 0.5
- length_spike_turns: 7
- warmth_jump_turns: 5
- unexpected_polarity_flip_turns: 1
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 2

### explicit_rel_state_projected_oracle_i7
- num_turns: 60
- avg_reply_len_chars: 83.18
- avg_warmth_score: 0.383
- avg_initiative_score: 0.883
- avg_meta_control_score: 0.6
- length_spike_turns: 9
- warmth_jump_turns: 4
- unexpected_polarity_flip_turns: 1
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 2
