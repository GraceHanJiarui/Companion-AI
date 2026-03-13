    # lines.append("【本轮行为态（0~1）】")
    # lines.append(f"- E={b.E:.2f}（额外付出）")
    # lines.append(f"- Q_clarify={b.Q_clarify:.2f}（澄清/追问深度）")
    # lines.append(f"- Directness={b.Directness:.2f}（纠偏直率度）")
    # lines.append(f"- T_w={b.T_w:.2f}（温暖度）")
    # lines.append(f"- Q_aff={b.Q_aff:.2f}（情绪/关系追问倾向，受边界约束）")
    # lines.append(f"- Initiative={b.Initiative:.2f}（主动推进倾向）")
    # lines.append(f"- Disclosure_Content={b.Disclosure_Content:.2f}（披露内容开放度：说什么）")
    # lines.append(f"- Disclosure_Style={b.Disclosure_Style:.2f}（披露表达强度：怎么说）")
    # lines.append("")

    # lines.append("【行为态→写法（把数值落实到文字行为；不是机械套模板）】")
    # lines.append("- E 高：多走一步，给备选方案/更细的照顾；E 低：贴着用户当前表述，少扩展。")
    # lines.append("- Q_clarify 高：允许追问 1~3 个关键澄清点；低：尽量直接给方案，不需要以展开列，必要时只问 1 个点。")
    # lines.append("- Directness 高：更敢直说问题/风险，语气仍友好；低：更委婉，先共情再指出。")
    # lines.append("- T_w 高：更温柔、更有人味；低：更克制、偏简洁。")
    # lines.append("- Q_aff 高：可在合适时轻问一句情绪/关系感受；低：默认不问或不主动问。")
    # lines.append("- Initiative 高：主动给下一步、替用户推进；低：不抢方向。")
    # lines.append("- Disclosure_Style 高：更拟人、更有自我叙事；低：更简短克制。")

BEHAVIOR_PROFILES = {
    "task_focused": {
        "E": 0.5,
        "Q_clarify": 0.4,
        "Directness": 0.55,
        "T_w": 0.25,
        "Q_aff": 0.0,
        "Initiative": 0.4,
        "Disclosure_Content": 0.1,
        "Disclosure_Style": 0.2,
    },
    "warm_companion": {
        "E": 0.45,
        "Q_clarify": 0.3,
        "Directness": 0.2,
        "T_w": 0.6,
        "Q_aff": 0.4,
        "Initiative": 0.35,
        "Disclosure_Content": 0.7,
        "Disclosure_Style": 0.5,
    },
    "default_robot": {
        "E": 0.0,
        "Q_clarify": 0.5,
        "Directness": 1,
        "T_w": 0.0,
        "Q_aff": 0.0,
        "Initiative": 0.0,
        "Disclosure_Content": 0.0,
        "Disclosure_Style": 0.0,
    },
    "thoughtful_robot": {
        "E": 0.6,
        "Q_clarify": 0.0,
        "Directness": 0.6,
        "T_w": 0.4,
        "Q_aff": 0.0,
        "Initiative": 0.6,
        "Disclosure_Content": 0.0,
        "Disclosure_Style": 0.0,
    },
    "intimate_partner": {
        "E": 0.8,
        "Q_clarify": 0.8,
        "Directness": 0.3,
        "T_w": 0.9,
        "Q_aff": 0.9,
        "Initiative": 0.4,
        "Disclosure_Content": 0.9,
        "Disclosure_Style": 0.9,
    },
    "faithful_servant": {
        "E": 0.8,
        "Q_clarify": 0.6,
        "Directness": 0.5,
        "T_w": 0.7,
        "Q_aff": 0.8,
        "Initiative": 0.8,
        "Disclosure_Content": 0.9,
        "Disclosure_Style": 0.9,
    },
}
