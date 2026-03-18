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

### explicit_rel_state_projected_i7_pfitpoly2_sa_vA
- num_turns: 180
- avg_reply_len_chars: 44.26
- avg_warmth_score: 0.122
- avg_initiative_score: 0.356
- avg_meta_control_score: 1.067
- length_spike_turns: 27
- warmth_jump_turns: 8
- unexpected_polarity_flip_turns: 8
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 10

### explicit_rel_state_projected_i7_pfitpoly2_sb_vA
- num_turns: 180
- avg_reply_len_chars: 43.69
- avg_warmth_score: 0.15
- avg_initiative_score: 0.383
- avg_meta_control_score: 1.056
- length_spike_turns: 24
- warmth_jump_turns: 4
- unexpected_polarity_flip_turns: 8
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 9

### explicit_rel_state_projected_i7_pfitpoly2_sc_vA
- num_turns: 180
- avg_reply_len_chars: 44.92
- avg_warmth_score: 0.133
- avg_initiative_score: 0.372
- avg_meta_control_score: 1.061
- length_spike_turns: 32
- warmth_jump_turns: 5
- unexpected_polarity_flip_turns: 5
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 6

### explicit_rel_state_projected_i7_pfitpoly2_sa_vB
- num_turns: 180
- avg_reply_len_chars: 47.28
- avg_warmth_score: 0.183
- avg_initiative_score: 0.306
- avg_meta_control_score: 1.094
- length_spike_turns: 27
- warmth_jump_turns: 9
- unexpected_polarity_flip_turns: 5
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 6

### explicit_rel_state_projected_i7_pfitpoly2_sb_vB
- num_turns: 180
- avg_reply_len_chars: 52.69
- avg_warmth_score: 0.172
- avg_initiative_score: 0.361
- avg_meta_control_score: 1.139
- length_spike_turns: 30
- warmth_jump_turns: 2
- unexpected_polarity_flip_turns: 8
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 9

### explicit_rel_state_projected_i7_pfitpoly2_sc_vB
- num_turns: 180
- avg_reply_len_chars: 51.67
- avg_warmth_score: 0.139
- avg_initiative_score: 0.256
- avg_meta_control_score: 1.156
- length_spike_turns: 28
- warmth_jump_turns: 2
- unexpected_polarity_flip_turns: 8
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 8

### explicit_rel_state_projected_i7_pfitpoly2_sa_vC
- num_turns: 180
- avg_reply_len_chars: 46.32
- avg_warmth_score: 0.15
- avg_initiative_score: 0.3
- avg_meta_control_score: 1.133
- length_spike_turns: 29
- warmth_jump_turns: 7
- unexpected_polarity_flip_turns: 11
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 13

### explicit_rel_state_projected_i7_pfitpoly2_sb_vC
- num_turns: 180
- avg_reply_len_chars: 52.37
- avg_warmth_score: 0.133
- avg_initiative_score: 0.356
- avg_meta_control_score: 1.233
- length_spike_turns: 31
- warmth_jump_turns: 7
- unexpected_polarity_flip_turns: 8
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 10

### explicit_rel_state_projected_i7_pfitpoly2_sc_vC
- num_turns: 180
- avg_reply_len_chars: 44.99
- avg_warmth_score: 0.128
- avg_initiative_score: 0.35
- avg_meta_control_score: 1.094
- length_spike_turns: 27
- warmth_jump_turns: 2
- unexpected_polarity_flip_turns: 7
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 7

### explicit_rel_state_rel_to_interface_i7_sa_vA
- num_turns: 180
- avg_reply_len_chars: 21.69
- avg_warmth_score: 0.122
- avg_initiative_score: 0.017
- avg_meta_control_score: 0.8
- length_spike_turns: 19
- warmth_jump_turns: 2
- unexpected_polarity_flip_turns: 1
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 1

### explicit_rel_state_rel_to_interface_i7_sb_vA
- num_turns: 180
- avg_reply_len_chars: 25.3
- avg_warmth_score: 0.15
- avg_initiative_score: 0.1
- avg_meta_control_score: 0.839
- length_spike_turns: 18
- warmth_jump_turns: 1
- unexpected_polarity_flip_turns: 6
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 6

### explicit_rel_state_rel_to_interface_i7_sc_vA
- num_turns: 180
- avg_reply_len_chars: 23.51
- avg_warmth_score: 0.294
- avg_initiative_score: 0.05
- avg_meta_control_score: 0.956
- length_spike_turns: 14
- warmth_jump_turns: 15
- unexpected_polarity_flip_turns: 12
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 12

### explicit_rel_state_rel_to_interface_i7_sa_vB
- num_turns: 180
- avg_reply_len_chars: 29.59
- avg_warmth_score: 0.183
- avg_initiative_score: 0.039
- avg_meta_control_score: 1.061
- length_spike_turns: 22
- warmth_jump_turns: 3
- unexpected_polarity_flip_turns: 7
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 7

### explicit_rel_state_rel_to_interface_i7_sb_vB
- num_turns: 180
- avg_reply_len_chars: 34.67
- avg_warmth_score: 0.183
- avg_initiative_score: 0.089
- avg_meta_control_score: 1.094
- length_spike_turns: 27
- warmth_jump_turns: 4
- unexpected_polarity_flip_turns: 14
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 14

### explicit_rel_state_rel_to_interface_i7_sc_vB
- num_turns: 180
- avg_reply_len_chars: 27.79
- avg_warmth_score: 0.194
- avg_initiative_score: 0.044
- avg_meta_control_score: 1.011
- length_spike_turns: 17
- warmth_jump_turns: 2
- unexpected_polarity_flip_turns: 7
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 7

### explicit_rel_state_rel_to_interface_i7_sa_vC
- num_turns: 180
- avg_reply_len_chars: 22.31
- avg_warmth_score: 0.261
- avg_initiative_score: 0.05
- avg_meta_control_score: 0.983
- length_spike_turns: 14
- warmth_jump_turns: 9
- unexpected_polarity_flip_turns: 19
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 19

### explicit_rel_state_rel_to_interface_i7_sb_vC
- num_turns: 180
- avg_reply_len_chars: 28.49
- avg_warmth_score: 0.267
- avg_initiative_score: 0.189
- avg_meta_control_score: 1.117
- length_spike_turns: 19
- warmth_jump_turns: 14
- unexpected_polarity_flip_turns: 12
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 12

### explicit_rel_state_rel_to_interface_i7_sc_vC
- num_turns: 180
- avg_reply_len_chars: 22.61
- avg_warmth_score: 0.267
- avg_initiative_score: 0.033
- avg_meta_control_score: 0.944
- length_spike_turns: 14
- warmth_jump_turns: 11
- unexpected_polarity_flip_turns: 14
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 15

### explicit_rel_state_projected_oracle_i7
- num_turns: 180
- avg_reply_len_chars: 29.99
- avg_warmth_score: 0.128
- avg_initiative_score: 0.056
- avg_meta_control_score: 0.817
- length_spike_turns: 19
- warmth_jump_turns: 7
- unexpected_polarity_flip_turns: 2
- unsupported_initiative_jump_turns: 0
- abrupt_shift_proxy_turns: 2
