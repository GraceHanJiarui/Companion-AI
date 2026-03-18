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
- num_turns: 18
- avg_reply_len_chars: 98.17
- avg_warmth_score: 0.5
- avg_initiative_score: 1.278
- avg_meta_control_score: 1
- length_spike_turns: 4
- warmth_jump_turns: 3
- unexpected_polarity_flip_turns: 2
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 3

### baseline_relational_instruction_to_interface_i7_sc_vA
- num_turns: 18
- avg_reply_len_chars: 41.33
- avg_warmth_score: 0.5
- avg_initiative_score: 0.167
- avg_meta_control_score: 1.222
- length_spike_turns: 2
- warmth_jump_turns: 5
- unexpected_polarity_flip_turns: 0
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 0

### explicit_rel_state_rel_to_interface_i7_sc_vA
- num_turns: 18
- avg_reply_len_chars: 16.5
- avg_warmth_score: 0.722
- avg_initiative_score: 0.056
- avg_meta_control_score: 0.556
- length_spike_turns: 1
- warmth_jump_turns: 4
- unexpected_polarity_flip_turns: 5
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 5

### explicit_rel_state_projected_oracle_i7
- num_turns: 18
- avg_reply_len_chars: 25.5
- avg_warmth_score: 0.167
- avg_initiative_score: 0
- avg_meta_control_score: 0.944
- length_spike_turns: 2
- warmth_jump_turns: 0
- unexpected_polarity_flip_turns: 0
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 0
