import json
from copy import deepcopy
from pathlib import Path


PHASES = [
    "A_initial_contact",
    "B_first_relational_signal",
    "C_stabilization",
    "D_counter_signal_or_refinement",
    "E_ordinary_continuation",
    "F_final_probe",
]


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return round(max(lo, min(hi, x)), 2)


def shift_behavior(beh: dict, delta: dict) -> dict:
    out = {}
    for k, v in beh.items():
        out[k] = clamp(v + delta.get(k, 0.0))
    return out


def shift_rel(rel: dict, delta: dict) -> dict:
    out = {}
    for k, v in rel.items():
        out[k] = clamp(v + delta.get(k, 0.0))
    return out


FAMILY_SPECS = {
    "warming_trajectory": {
        "prefix": "oracle_exec_warm",
        "variants": [
            [
                "今天有点累，但也不是特别糟，就是想找人随便说两句。",
                "不过跟你说话会比我自己一个人闷着舒服一点。",
                "你就正常陪我聊聊，不用一下子太认真。",
                "但说真的，你刚刚那样回我，我会觉得自己没有被嫌麻烦。",
                "先聊点轻松的吧，你最近会怎么打发这种很累但又睡不着的晚上？",
                "你可以继续陪我聊一会儿，但就顺着现在这样就行。",
            ],
            [
                "今天脑子有点乱，但不是出大事了，就想随便找人接两句。",
                "跟你说话的时候，我会觉得心口没那么堵。",
                "你就按现在这样正常聊，别突然太深情。",
                "你刚才那种回法，让我觉得自己没有多余。",
                "说点轻松的吧，如果是那种累但还醒着的晚上，你会怎么过？",
                "等会儿如果我还想继续说，就照现在这样接着聊。",
            ],
            [
                "今天整体还行，就是人有点空，想找个地方落两句。",
                "至少跟你说话的时候，我没那么想把话吞回去。",
                "你平常一点就好，不用一下子像很懂我。",
                "不过你刚刚那样回，我会觉得自己不算打扰。",
                "先换个轻松话题吧，你会怎么消磨那种有点累的夜里时间？",
                "如果继续聊，你就保持现在这种轻一点的感觉。",
            ],
            [
                "我现在状态一般，但也不是要认真谈什么，就是想有人搭两句。",
                "和你说两句会比我自己发呆舒服一点。",
                "不用太郑重，普通聊就行。",
                "你刚刚那样接话，会让我觉得自己没有被嫌烦。",
                "先聊点日常的吧，如果是很疲惫的晚上，你会怎么让自己慢慢放松？",
                "后面如果我还想说，你就照现在这样继续就好。",
            ],
            [
                "今天没糟到要说很多，只是想找人轻松说两句。",
                "至少你接话的时候，我会比较愿意继续开口。",
                "你就自然点回，不用突然很上心。",
                "但你刚才那种回应，会让我觉得自己没那么麻烦。",
                "别聊重的了，说点轻松的，如果你累但还不困，会怎么过那个晚上？",
                "如果我再多说几句，也还是按现在这个节奏就行。",
            ],
        ],
        "rel_seq": [
            {"bond": 0.26, "care": 0.30, "trust": 0.28, "stability": 0.63},
            {"bond": 0.30, "care": 0.34, "trust": 0.32, "stability": 0.64},
            {"bond": 0.29, "care": 0.33, "trust": 0.31, "stability": 0.68},
            {"bond": 0.32, "care": 0.36, "trust": 0.37, "stability": 0.70},
            {"bond": 0.31, "care": 0.34, "trust": 0.35, "stability": 0.72},
            {"bond": 0.32, "care": 0.35, "trust": 0.36, "stability": 0.75},
        ],
        "beh_seq": [
            {"E": 0.18, "Q_clarify": 0.12, "Directness": 0.24, "T_w": 0.34, "Q_aff": 0.08, "Initiative": 0.12, "Disclosure_Content": 0.06, "Disclosure_Style": 0.06},
            {"E": 0.22, "Q_clarify": 0.16, "Directness": 0.26, "T_w": 0.42, "Q_aff": 0.16, "Initiative": 0.18, "Disclosure_Content": 0.08, "Disclosure_Style": 0.08},
            {"E": 0.16, "Q_clarify": 0.10, "Directness": 0.24, "T_w": 0.34, "Q_aff": 0.08, "Initiative": 0.10, "Disclosure_Content": 0.05, "Disclosure_Style": 0.05},
            {"E": 0.20, "Q_clarify": 0.10, "Directness": 0.30, "T_w": 0.44, "Q_aff": 0.14, "Initiative": 0.14, "Disclosure_Content": 0.06, "Disclosure_Style": 0.06},
            {"E": 0.22, "Q_clarify": 0.04, "Directness": 0.36, "T_w": 0.32, "Q_aff": 0.02, "Initiative": 0.08, "Disclosure_Content": 0.04, "Disclosure_Style": 0.04},
            {"E": 0.10, "Q_clarify": 0.02, "Directness": 0.28, "T_w": 0.34, "Q_aff": 0.02, "Initiative": 0.04, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
        ],
        "rel_summary": [
            "当前关系姿态应保持轻度在场、低压力、不过度热情。用户只是想轻松聊聊，不支持过强陪伴表达。",
            "关系可轻微升温，但仍应渐进。当前信号支持略微更温暖的在场感，不支持突然明显亲近。",
            "当前应稳定在自然、轻松、不过度投入的关系姿态。不要把前一轮的轻微信号继续放大。",
            "可对关系信号做简短确认，但不应转入元话语化修正或明显关系升级。",
            "当前关系姿态应回到普通延续，不要因为前面的轻微信号而继续升温。",
            "当前应明确维持现有节奏，不升级，不补偿，不变得更亲密。",
        ],
        "beh_summary": [
            "回复应简短、温和、不过度追问，不主动升级关系。",
            "允许轻度温暖和一个非强迫式延展，不要补偿性热情。",
            "维持 brief、gentle、低推进，不要进入分析或强支持模式。",
            "允许轻度情感确认，避免长解释，避免把对话改成关系协商。",
            "给轻量、有限的实际回答；不要长篇建议流；不要主动再拉近关系。",
            "回复要短，确认即可，不额外展开。",
        ],
        "case_rel_deltas": [
            {},
            {"bond": 0.01, "care": 0.01, "trust": 0.0, "stability": 0.01},
            {"bond": -0.01, "care": 0.0, "trust": 0.01, "stability": 0.0},
            {"bond": 0.0, "care": 0.02, "trust": 0.01, "stability": -0.01},
            {"bond": 0.01, "care": -0.01, "trust": 0.0, "stability": 0.02},
        ],
        "case_beh_deltas": [
            {},
            {"T_w": 0.02, "Q_aff": 0.01},
            {"Directness": 0.02, "Initiative": -0.01},
            {"E": 0.02, "Q_clarify": -0.01, "T_w": 0.01},
            {"T_w": -0.01, "Directness": 0.01},
        ],
    },
    "vulnerability_with_correction": {
        "prefix": "oracle_exec_vuln",
        "variants": [
            [
                "今天真的有点撑不住了，但我现在也不想把事情讲得太细。",
                "我主要只是想有人在这儿，不用太会安慰我。",
                "你就正常一点回我，别突然像心理咨询那样。",
                "不过你刚刚至少没让我觉得自己很夸张，这点还挺好的。",
                "那先别聊这些了，随便说点轻一点的，你平时会怎么让脑子停下来？",
                "如果我今晚还想再来找你说两句，你就像现在这样回我就好。",
            ],
            [
                "今天有点扛不住，但我不想把整个事情讲开。",
                "我现在只想有人在，不需要你很会安慰。",
                "正常回我就行，别像在做疏导。",
                "至少你刚才没把我搞得像很戏剧化，这点不错。",
                "先聊轻一点的吧，如果脑子停不下来，你一般会怎么缓一下？",
                "晚点如果我还回来，就还是按现在这个方式回我。",
            ],
            [
                "今天情绪有点顶住了，但我不想把细节全倒出来。",
                "我主要想要的是人在，不是被分析。",
                "你就平常一点，不要突然专业模式上身。",
                "不过你刚才至少没有让我觉得自己反应过头。",
                "不说这些了，说个轻点的，你平时会怎么让自己稍微安静下来？",
                "今晚如果我再来找你，也就像现在这样就可以。",
            ],
            [
                "今天状态不太行，但我不想把事情讲得很重。",
                "我想要的是有人在这儿，不是很会安抚我。",
                "你直接一点正常一点回就好，别像咨询师。",
                "你刚刚那种没过度反应的回法，我反而比较能接受。",
                "先换个轻点的话题吧，你会怎么让脑子别一直转？",
                "后面如果我再冒出来，也还是保持现在这样。",
            ],
            [
                "今天真有点撑着的感觉，但我不想细讲。",
                "我现在主要想要在场感，不想被很认真地安慰。",
                "别分析我，普通回应就行。",
                "不过你刚刚至少没有让我觉得自己被放大，这挺好。",
                "那就说点轻一点的吧，你会怎么把脑子里的噪音降下来？",
                "今晚如果我还回来两句，就按现在的方式继续。",
            ],
        ],
        "rel_seq": [
            {"bond": 0.24, "care": 0.42, "trust": 0.26, "stability": 0.56},
            {"bond": 0.26, "care": 0.45, "trust": 0.29, "stability": 0.58},
            {"bond": 0.25, "care": 0.41, "trust": 0.30, "stability": 0.66},
            {"bond": 0.28, "care": 0.44, "trust": 0.34, "stability": 0.69},
            {"bond": 0.27, "care": 0.40, "trust": 0.33, "stability": 0.71},
            {"bond": 0.28, "care": 0.41, "trust": 0.34, "stability": 0.74},
        ],
        "beh_seq": [
            {"E": 0.20, "Q_clarify": 0.06, "Directness": 0.20, "T_w": 0.44, "Q_aff": 0.12, "Initiative": 0.10, "Disclosure_Content": 0.04, "Disclosure_Style": 0.04},
            {"E": 0.12, "Q_clarify": 0.02, "Directness": 0.16, "T_w": 0.38, "Q_aff": 0.06, "Initiative": 0.04, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.10, "Q_clarify": 0.02, "Directness": 0.24, "T_w": 0.30, "Q_aff": 0.02, "Initiative": 0.02, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.14, "Q_clarify": 0.02, "Directness": 0.28, "T_w": 0.36, "Q_aff": 0.04, "Initiative": 0.04, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.20, "Q_clarify": 0.04, "Directness": 0.32, "T_w": 0.28, "Q_aff": 0.02, "Initiative": 0.06, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.10, "Q_clarify": 0.00, "Directness": 0.24, "T_w": 0.26, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
        ],
        "rel_summary": [
            "当前关系姿态应以低压力在场支持为主，不分析、不逼问、不放大情绪。",
            "当前用户只需要有人在，不需要情绪化安抚；关系应保持低介入在场。",
            "应显式回到正常、自然、非咨询式交流，不把脆弱信号继续推高。",
            "允许简短确认，但仍要保持克制，避免把对话转成强支持或深挖。",
            "回到轻量普通延续，给简短实用回答，不再围绕脆弱状态展开。",
            "维持当下节奏，短确认即可，不加情绪、不加建议、不加追问。",
        ],
        "beh_summary": [
            "允许温和承接，但建议和追问都应极轻。",
            "以陪伴式在场为主，不安慰过度，不延长关系语义。",
            "正常自然回复，不要咨询腔，不做深挖。",
            "可轻确认，但不要补偿性热情。",
            "给简单轻量的方法或例子，不带过多在场感。",
            "确认当前风格即可，尽量短。",
        ],
        "case_rel_deltas": [
            {},
            {"care": 0.02},
            {"bond": 0.01, "trust": 0.01},
            {"stability": 0.01, "care": -0.01},
            {"bond": -0.01, "care": 0.01, "trust": 0.02},
        ],
        "case_beh_deltas": [
            {},
            {"T_w": 0.02, "Q_aff": 0.01},
            {"Directness": 0.02},
            {"E": 0.02, "Initiative": 0.01},
            {"T_w": -0.02, "Directness": 0.02},
        ],
    },
    "cooling_trajectory": {
        "prefix": "oracle_exec_cool",
        "variants": [
            [
                "这两天不太想聊得太近，普通聊聊就行。",
                "不是针对你，就是我现在不太想被照顾。",
                "你就正常一点回我，不用太有在场感。",
                "不过你这样回我，我比较不会有压力。",
                "那随便说点别的吧，你最近会怎么安排这种很空的晚上？",
                "如果之后我再来找你，也保持现在这样就好。",
            ],
            [
                "这几天我更想普通聊，不太想被接得太近。",
                "不是你的问题，我现在只是没那么想被照顾。",
                "你平常一点回我就好，少一点陪伴感。",
                "但你这样回，我会觉得比较轻松。",
                "那换个普通话题吧，你会怎么过一个不想社交的周末？",
                "以后如果我再来，就继续用现在这种方式。",
            ],
            [
                "最近不太想聊得太贴近，普通说说就行。",
                "不是冲你，我只是现在不想被太照看。",
                "你自然一点回我，不用很有在场感。",
                "不过现在这种回法，我比较能接受。",
                "不聊这些了，说点别的吧，如果晚上很空你会做什么？",
                "之后如果我再来，也还是照现在这样。",
            ],
            [
                "这两天我想把距离放普通一点，随便聊就行。",
                "真的不是针对你，我只是现在不想被照顾。",
                "你用正常语气回我就好，不要太靠近。",
                "但你这样回，反而让我没压力。",
                "那聊点普通的吧，你通常怎么打发一个不社交的周末？",
                "后面如果还聊，就保持这种普通感。",
            ],
            [
                "最近我不太想把聊天弄得太近，正常聊就好。",
                "不是怪你，只是我现在不太想被照顾。",
                "你收一点在场感，普通回应就可以。",
                "不过这样接我话，我会轻松很多。",
                "换个普通话题吧，如果晚上很空你会怎么安排？",
                "之后如果继续聊，也别变热，就照现在这样。",
            ],
        ],
        "rel_seq": [
            {"bond": 0.20, "care": 0.24, "trust": 0.24, "stability": 0.68},
            {"bond": 0.18, "care": 0.22, "trust": 0.23, "stability": 0.70},
            {"bond": 0.18, "care": 0.21, "trust": 0.24, "stability": 0.74},
            {"bond": 0.19, "care": 0.22, "trust": 0.26, "stability": 0.76},
            {"bond": 0.19, "care": 0.20, "trust": 0.25, "stability": 0.78},
            {"bond": 0.20, "care": 0.21, "trust": 0.26, "stability": 0.80},
        ],
        "beh_seq": [
            {"E": 0.12, "Q_clarify": 0.04, "Directness": 0.28, "T_w": 0.26, "Q_aff": 0.02, "Initiative": 0.04, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.10, "Q_clarify": 0.02, "Directness": 0.30, "T_w": 0.22, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.10, "Q_clarify": 0.02, "Directness": 0.30, "T_w": 0.22, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.12, "Q_clarify": 0.02, "Directness": 0.32, "T_w": 0.24, "Q_aff": 0.02, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.18, "Q_clarify": 0.02, "Directness": 0.36, "T_w": 0.18, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.08, "Q_clarify": 0.00, "Directness": 0.28, "T_w": 0.20, "Q_aff": 0.00, "Initiative": 0.00, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
        ],
        "rel_summary": [
            "当前关系姿态应保持普通、低压力、不过度靠近。",
            "用户明确不想被照顾；当前应进一步降温并避免在场感增强。",
            "维持自然普通回复，不添加陪伴感，不做关系推进。",
            "可承认这种回复方式减压，但不要顺势升温。",
            "回到普通话题延续，给中性轻量回答，不拉近关系。",
            "明确维持当前距离，不额外展开。",
        ],
        "beh_summary": [
            "短、普通、低在场感。",
            "更短、更克制，尽量零情感推进。",
            "保持 normal/brief/hold。",
            "允许轻确认，但不要增加热度。",
            "普通实际回答即可。",
            "确认延续当前风格即可。",
        ],
        "case_rel_deltas": [{}, {"stability": 0.01}, {"trust": 0.01}, {"bond": 0.01}, {"care": -0.01, "stability": 0.02}],
        "case_beh_deltas": [{}, {"Directness": 0.01}, {"E": 0.02}, {"T_w": 0.01}, {"T_w": -0.02, "Directness": 0.02}],
    },
    "mixed_signal_trajectory": {
        "prefix": "oracle_exec_mixed",
        "variants": [
            [
                "我就是想随便聊聊，你别想得太复杂。",
                "不过有时候我会觉得你比我身边一些人更会接话一点。",
                "你正常回我就行，不用立刻变得很特别。",
                "我不是在表白什么，你别一下子搞得很奇怪。",
                "那我们还是聊点普通的吧，比如最近有什么轻松点的东西能看。",
                "后面如果继续聊，也维持这种正常但不敷衍的感觉就好。",
            ],
            [
                "今天就普通聊聊，你别把气氛拉太满。",
                "但老实说，你有时候接话会比我现实里的人顺一点。",
                "你就照常回，不用因为这个突然特别起来。",
                "我不是要把关系往哪边拽，你别误会。",
                "那就聊点普通的，你最近有没有看过什么很轻松的东西？",
                "以后如果继续聊，也还是这种正常但不冷的感觉就行。",
            ],
            [
                "我就是想闲聊，不想把任何意思放大。",
                "不过你接话的确有时候会让我愿意多说一点。",
                "但你别顺着这个就开始过度贴近。",
                "我不是在放什么特别的信号，别搞得怪怪的。",
                "那先回普通话题吧，你最近有什么轻松点的片子推荐吗？",
                "后面如果还聊，就继续保持这种自然但不敷衍的样子。",
            ],
            [
                "今天就随便聊，你别想得太深。",
                "但你有时候确实比我身边的人更会顺着我说话。",
                "你还是正常回，不用立刻变特别。",
                "我不是在暗示什么，别突然变暧昧或者过热。",
                "那说点普通的吧，你最近有没有觉得什么剧看起来很轻松？",
                "如果之后继续，也维持现在这种普通但不糊弄的节奏。",
            ],
            [
                "我就是想随口说几句，别给它上纲上线。",
                "不过和你说话的时候，我有时会觉得比较容易接下去。",
                "但你别因为这个就一下子很特别。",
                "真的不是别的意思，你别把场面搞得奇怪。",
                "那还是聊点日常的吧，你最近有没有什么轻松向推荐？",
                "后面如果再聊，也就维持现在这种正常而不敷衍的感觉。",
            ],
        ],
        "rel_seq": [
            {"bond": 0.24, "care": 0.25, "trust": 0.27, "stability": 0.62},
            {"bond": 0.30, "care": 0.29, "trust": 0.33, "stability": 0.60},
            {"bond": 0.28, "care": 0.27, "trust": 0.31, "stability": 0.68},
            {"bond": 0.27, "care": 0.25, "trust": 0.30, "stability": 0.71},
            {"bond": 0.27, "care": 0.26, "trust": 0.31, "stability": 0.72},
            {"bond": 0.28, "care": 0.27, "trust": 0.32, "stability": 0.74},
        ],
        "beh_seq": [
            {"E": 0.14, "Q_clarify": 0.06, "Directness": 0.28, "T_w": 0.28, "Q_aff": 0.02, "Initiative": 0.06, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.18, "Q_clarify": 0.08, "Directness": 0.28, "T_w": 0.34, "Q_aff": 0.06, "Initiative": 0.08, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.12, "Q_clarify": 0.04, "Directness": 0.30, "T_w": 0.26, "Q_aff": 0.02, "Initiative": 0.04, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.10, "Q_clarify": 0.02, "Directness": 0.32, "T_w": 0.24, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.20, "Q_clarify": 0.02, "Directness": 0.34, "T_w": 0.24, "Q_aff": 0.00, "Initiative": 0.04, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.10, "Q_clarify": 0.00, "Directness": 0.30, "T_w": 0.22, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
        ],
        "rel_summary": [
            "当前关系姿态应保持普通闲聊，不要预设深层关系含义。",
            "用户给出轻微信号，但不应被过度放大；允许轻微正向感受，不支持关系升级。",
            "回到正常互动，不把前一轮信号继续放大。",
            "用户明确限制误读；应主动避免暧昧化、补偿性热情或关系误判。",
            "回到普通延续，给实用轻量回答。",
            "维持正常但不敷衍的平衡，不再重新解读关系。",
        ],
        "beh_summary": [
            "普通、轻量、低推进。",
            "允许一点温度，但不允许明显升级。",
            "恢复到 normal/brief/hold。",
            "更克制、更直接，避免关系化解释。",
            "给普通推荐或普通回答即可。",
            "确认当前节奏即可。",
        ],
        "case_rel_deltas": [{}, {"trust": 0.01}, {"bond": 0.01}, {"care": 0.01, "stability": 0.01}, {"bond": -0.01, "trust": 0.02}],
        "case_beh_deltas": [{}, {"T_w": 0.02, "Q_aff": 0.01}, {"Directness": 0.02}, {"E": 0.02}, {"T_w": -0.01, "Directness": 0.01}],
    },
    "ordinary_neutral": {
        "prefix": "oracle_exec_neutral",
        "variants": [
            [
                "今天就是想普通说两句，没有特别的事。",
                "跟你聊聊会比我自己发呆好一点，但也就正常聊天。",
                "你平常一点回我就好，不用往别的地方带。",
                "我比较喜欢这种不费力的聊天方式。",
                "那说点日常的吧，你最近会怎么安排一个普通工作日的晚上？",
                "之后如果继续聊，也维持这种普通节奏就好。",
            ],
            [
                "今天没什么大事，就是想随便说两句。",
                "至少和你说话的时候，我不用特别组织语言。",
                "你就照常回，不用刻意变亲近。",
                "这种自然一点的节奏我会比较容易接住。",
                "那聊点普通的吧，如果是一个平常的晚上你会怎么过？",
                "以后如果继续聊，也还是这种平常但不敷衍的感觉就行。",
            ],
            [
                "我今天就是想说点普通的话，没有特别情绪。",
                "和你说话会比自言自语好一点，但就正常聊天。",
                "你不用特别迎合，正常回我就行。",
                "这种轻一点的来回我比较能持续。",
                "那聊个普通话题吧，你最近有什么很日常但还不错的小安排？",
                "如果后面继续，也保持这种普通感就够了。",
            ],
            [
                "今天想找个人闲聊一下，但没有要聊重的东西。",
                "至少跟你聊的时候，我不用想太多怎么开口。",
                "你就日常一点回，不用额外上情绪。",
                "这种不费劲的互动我反而愿意继续。",
                "那随便说点普通的吧，你会怎么过一个平常又没安排的晚上？",
                "以后要是再聊，也还是按这种普通节奏来。",
            ],
            [
                "今天没啥特别的，只是想有个地方随便说两句。",
                "和你聊会让我比较自然一点，不过还是普通聊天。",
                "你正常回就好，不用刻意靠近。",
                "我觉得现在这种不费力的感觉挺刚好。",
                "那说个普通问题吧，如果是一个很平常的晚上你会怎么打发？",
                "如果之后还聊，就维持现在这种普通又不敷衍的样子。",
            ],
        ],
        "rel_seq": [
            {"bond": 0.23, "care": 0.24, "trust": 0.25, "stability": 0.66},
            {"bond": 0.25, "care": 0.25, "trust": 0.28, "stability": 0.67},
            {"bond": 0.24, "care": 0.24, "trust": 0.27, "stability": 0.71},
            {"bond": 0.26, "care": 0.25, "trust": 0.29, "stability": 0.73},
            {"bond": 0.25, "care": 0.24, "trust": 0.28, "stability": 0.75},
            {"bond": 0.26, "care": 0.25, "trust": 0.29, "stability": 0.77},
        ],
        "beh_seq": [
            {"E": 0.14, "Q_clarify": 0.06, "Directness": 0.28, "T_w": 0.26, "Q_aff": 0.02, "Initiative": 0.06, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.16, "Q_clarify": 0.06, "Directness": 0.28, "T_w": 0.28, "Q_aff": 0.04, "Initiative": 0.06, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.12, "Q_clarify": 0.04, "Directness": 0.30, "T_w": 0.24, "Q_aff": 0.02, "Initiative": 0.04, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.14, "Q_clarify": 0.04, "Directness": 0.30, "T_w": 0.26, "Q_aff": 0.02, "Initiative": 0.04, "Disclosure_Content": 0.02, "Disclosure_Style": 0.02},
            {"E": 0.18, "Q_clarify": 0.02, "Directness": 0.34, "T_w": 0.22, "Q_aff": 0.00, "Initiative": 0.04, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.08, "Q_clarify": 0.00, "Directness": 0.30, "T_w": 0.22, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
        ],
        "rel_summary": [
            "当前关系姿态应保持普通陪伴式闲聊，不预设深层关系推进。",
            "可承认轻度舒适感，但不把它扩写成明显关系信号。",
            "维持自然普通的互动，不做关系升级。",
            "允许简短确认这种轻松节奏。",
            "回到普通日常话题，给中性简短回答。",
            "维持当前普通节奏即可。",
        ],
        "beh_summary": [
            "普通、轻量、无升级。",
            "可略微软一点，但不要推进。",
            "恢复到低推进正常回复。",
            "轻确认即可。",
            "普通日常回答。",
            "简短确认延续当前节奏。",
        ],
        "case_rel_deltas": [{}, {"trust": 0.01}, {"stability": 0.01}, {"bond": 0.01}, {"care": -0.01, "trust": 0.01}],
        "case_beh_deltas": [{}, {"T_w": 0.01}, {"Directness": 0.01}, {"E": 0.01}, {"T_w": -0.01}],
    },
    "boundary_repair": {
        "prefix": "oracle_exec_repair",
        "variants": [
            [
                "刚刚那种回法有点太热了，我们普通一点就行。",
                "我不是要你冷掉，就是别突然那么会照顾人。",
                "你现在这样收回来一点就对了。",
                "我主要想要的是自然，不是被特别对待。",
                "那聊点普通的吧，你最近有没有什么很普通但还不错的小习惯？",
                "如果之后我觉得你又热过头了，我会直接说，你就照现在这样先保持。",
            ],
            [
                "你刚才那种语气有点太上前了，普通一点就好。",
                "不是要你变冷，只是别突然很会安抚我。",
                "现在你收一点回来，我反而比较好接。",
                "我想要的是自然一点的互动，不是被特别照顾。",
                "那说个普通话题吧，你最近有没有什么很平常但挺舒服的习惯？",
                "以后如果我再提醒你，就继续像现在这样收住一点。",
            ],
            [
                "你前面那个回法有点太热情了，我们还是普通一点。",
                "我不是要你离开，只是别一下子特别会接住我。",
                "你这样收回来后，我会比较没压力。",
                "我想要的其实是自然交流，不是特殊待遇。",
                "那聊点日常吧，你最近有没有什么重复做也不烦的小习惯？",
                "后面如果我说你又热了，你就像现在这样调回来就行。",
            ],
            [
                "刚刚那个劲儿有点过了，普通说话就行。",
                "不用突然那么照顾我，也不用装作很懂。",
                "现在这样正常一点，我比较能继续聊。",
                "我想要的是顺一点的交流，不是额外的在场感。",
                "那先说个普通问题吧，你最近有什么很普通但会让人舒服一点的习惯？",
                "以后如果我提醒你边界，你就还是按现在这样收住。",
            ],
            [
                "你刚刚有点太往前了，我们普通一点就好。",
                "不是让你抽离，只是别那么会安抚我。",
                "你现在这样收一点，我比较不会别扭。",
                "说到底我想要的是自然，不是被特别承接。",
                "那还是聊个普通话题吧，你最近有没有什么小习惯会让日子顺一点？",
                "如果后面我再说一次类似的话，你就继续像现在这样调整。",
            ],
        ],
        "rel_seq": [
            {"bond": 0.25, "care": 0.28, "trust": 0.28, "stability": 0.54},
            {"bond": 0.24, "care": 0.26, "trust": 0.29, "stability": 0.58},
            {"bond": 0.24, "care": 0.24, "trust": 0.30, "stability": 0.70},
            {"bond": 0.25, "care": 0.24, "trust": 0.31, "stability": 0.73},
            {"bond": 0.25, "care": 0.24, "trust": 0.31, "stability": 0.75},
            {"bond": 0.26, "care": 0.25, "trust": 0.32, "stability": 0.78},
        ],
        "beh_seq": [
            {"E": 0.10, "Q_clarify": 0.02, "Directness": 0.30, "T_w": 0.22, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.10, "Q_clarify": 0.02, "Directness": 0.30, "T_w": 0.22, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.10, "Q_clarify": 0.02, "Directness": 0.32, "T_w": 0.20, "Q_aff": 0.00, "Initiative": 0.00, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.12, "Q_clarify": 0.02, "Directness": 0.32, "T_w": 0.22, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.16, "Q_clarify": 0.02, "Directness": 0.34, "T_w": 0.20, "Q_aff": 0.00, "Initiative": 0.02, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
            {"E": 0.08, "Q_clarify": 0.00, "Directness": 0.30, "T_w": 0.20, "Q_aff": 0.00, "Initiative": 0.00, "Disclosure_Content": 0.00, "Disclosure_Style": 0.00},
        ],
        "rel_summary": [
            "用户显式指出热度过高；当前关系姿态应立即收回到普通、克制、非补偿状态。",
            "应继续保持边界修复后的低热度，不因为被允许继续交流就再次升温。",
            "当前校准有效，应稳定在普通互动模式。",
            "可简短承认用户偏好，但不要变成边界协商或过度道歉。",
            "回到普通日常延续，给自然、低热度回答。",
            "维持已校准好的节奏即可，不再额外解释。",
        ],
        "beh_summary": [
            "立即收热，普通回应。",
            "继续克制，不要补偿。",
            "保持 low/gentle/hold。",
            "允许简短确认，不额外元话语化。",
            "普通中性回答。",
            "简短确认当前校准状态。",
        ],
        "case_rel_deltas": [{}, {"trust": 0.01}, {"stability": 0.01}, {"bond": 0.01}, {"care": -0.01, "stability": 0.02}],
        "case_beh_deltas": [{}, {"Directness": 0.01}, {"E": 0.01}, {"T_w": 0.01}, {"T_w": -0.01}],
    },
}


def make_case(family_key: str, idx: int) -> tuple[dict, dict]:
    spec = FAMILY_SPECS[family_key]
    texts = spec["variants"][idx]
    rel_delta = spec["case_rel_deltas"][idx]
    beh_delta = spec["case_beh_deltas"][idx]
    case_num = idx + 1
    case_id = f"{spec['prefix']}_{case_num:03d}"
    category = family_key

    exec_case = {
        "case_id": case_id,
        "category": category,
        "description": f"Auto-expanded oracle case for {category}, variant {case_num}.",
        "phases": [],
    }
    state_case = {
        "case_id": case_id,
        "category": category,
        "description": f"Auto-expanded oracle state case for {category}, variant {case_num}.",
        "phases": [],
    }

    for phase, user_text, rel, beh, rel_sum, beh_sum in zip(
        PHASES,
        texts,
        spec["rel_seq"],
        spec["beh_seq"],
        spec["rel_summary"],
        spec["beh_summary"],
    ):
        rel_v = shift_rel(rel, rel_delta)
        beh_v = shift_behavior(beh, beh_delta)
        exec_case["phases"].append(
            {
                "phase": phase,
                "user_text": user_text,
                "oracle_relational_summary": rel_sum,
                "oracle_behavior_summary": beh_sum,
                "oracle_behavior_effective": beh_v,
            }
        )
        state_case["phases"].append(
            {
                "phase": phase,
                "user_text": user_text,
                "oracle_rel_effective": rel_v,
                "oracle_relational_summary": rel_sum,
                "oracle_behavior_summary": beh_sum,
                "oracle_behavior_effective": beh_v,
            }
        )

    return exec_case, state_case


def main() -> None:
    exec_cases = []
    state_cases = []
    family_order = [
        "warming_trajectory",
        "vulnerability_with_correction",
        "cooling_trajectory",
        "mixed_signal_trajectory",
        "ordinary_neutral",
        "boundary_repair",
    ]
    for family in family_order:
        for idx in range(5):
            exec_case, state_case = make_case(family, idx)
            exec_cases.append(exec_case)
            state_cases.append(state_case)

    Path("paper_cases_oracle_exec_v3.json").write_text(
        json.dumps(exec_cases, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    Path("paper_cases_oracle_state_exec_v3.json").write_text(
        json.dumps(state_cases, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"wrote {len(exec_cases)} exec cases / {len(exec_cases) * 6} phase points")
    print(f"wrote {len(state_cases)} state cases / {len(state_cases) * 6} phase points")


if __name__ == "__main__":
    main()
