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

### explicit_rel_state_projected_oracle_state_i7_pfitpoly2
- num_turns: 180
- avg_reply_len_chars: 36.91
- avg_warmth_score: 0.133
- avg_initiative_score: 0.011
- avg_meta_control_score: 0.867
- length_spike_turns: 25
- warmth_jump_turns: 5
- unexpected_polarity_flip_turns: 3
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 5

### explicit_rel_state_projected_oracle_behavior_i7
- num_turns: 180
- avg_reply_len_chars: 39.21
- avg_warmth_score: 0.106
- avg_initiative_score: 0.011
- avg_meta_control_score: 0.967
- length_spike_turns: 25
- warmth_jump_turns: 0
- unexpected_polarity_flip_turns: 6
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 6

### explicit_rel_state_projected_oracle_i7
- num_turns: 180
- avg_reply_len_chars: 36.3
- avg_warmth_score: 0.094
- avg_initiative_score: 0.017
- avg_meta_control_score: 0.861
- length_spike_turns: 21
- warmth_jump_turns: 0
- unexpected_polarity_flip_turns: 3
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 3
