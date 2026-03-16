# Mini-Scope Paper Route: Go/No-Go Plan

## 1. 杩欐潯灏?scope 璺嚎鍦ㄧ爺绌朵粈涔?
杩欐潯璺嚎**涓嶆槸**鍦ㄨ瘉鏄庢暣涓?companion 浜у搧鏈夊濂斤紝涔?*涓嶆槸**鍦ㄩ獙璇佸畬鏁寸殑闀挎湡鍏崇郴绯荤粺璁捐銆?
瀹冨彧鐮旂┒涓€涓洿灏忋€佹洿蹇彲楠岃瘉鐨勯棶棰橈細

**鍦ㄩ暱鏈?companion-style 瀵硅瘽涓紝寮曞叆鏄惧紡鍏崇郴鎬佷腑闂村眰锛屾槸鍚﹁兘鍑忓皯鏄庢樉鐨勫叧绯昏烦鍙橈紝骞舵彁鍗?case-level relational coherence銆?*

杩欓噷鐨勯噸鐐逛笉鏄細

- boundary
- anti-manipulation
- disclosure
- actor 寰皟
- tone evaluator 寰皟
- 瀹屾暣 memory system

鑰屾槸锛?
- 闀挎湡瀵硅瘽涓殑**鍏崇郴璺冲彉**
- 闀挎湡瀵硅瘽涓殑**鍏崇郴杩炶疮鎬?*
- 鏄惧紡鍏崇郴鎬佹槸鍚﹀€煎緱浣滀负涓€涓?*涓棿鎺у埗灞?*

---

## 2. 涓轰粈涔堣繖鏉″皬 scope 璺嚎鍊煎緱鍗曠嫭楠岃瘉

濡傛灉鎶婇鐩〃杩版垚锛?
- 鈥滄樉寮忓叧绯绘€佷腑闂村眰鏄惁鎴愮珛鈥?
瀹冧細鏄惧緱杩囦簬鍐呴儴銆佽繃浜庡伐绋嬪寲銆?
浣嗗鏋滄妸棰樼洰琛ㄨ堪鎴愶細

- **涓轰簡鍑忓皯闀挎湡瀵硅瘽涓殑鍏崇郴璺冲彉銆佹彁鍗囧叧绯昏繛璐€э紝鏄惁闇€瑕佹樉寮忓叧绯绘€佽繖绫讳腑闂存帶鍒跺眰锛?*

瀹冨氨鍙樻垚浜嗕竴涓洿澶栭儴銆佹洿鑳借鐞嗚В鐨勯棶棰樸€?
杩欐潯璺嚎鐨勭洰鏍囦笉鏄洿鎺ュ彂涓€绡囧畬鏁村ぇ璁烘枃锛岃€屾槸鐢?`1-2 鍛╜ 鍥炵瓟锛?
**杩欎釜瀛愰鏈夋病鏈夌户缁繁鎸栫殑浠峰€笺€?*

---

## 3. 鍐荤粨鍚庣殑鐮旂┒鑼冨洿

### 3.1 鐮旂┒闂

**鍦ㄩ暱鏈?companion-style 瀵硅瘽涓紝鏄惧紡鍏崇郴鎬佷腑闂村眰锛岀浉姣?prompt-only 鎺у埗锛屾槸鍚﹁兘锛?*

1. 鍑忓皯鏄庢樉鐨勫叧绯昏烦鍙?2. 鎻愰珮鏁存 case 鐨勫叧绯昏繛璐€?
### 3.2 褰撳墠鍙仛鐨勬瘮杈冪粍

1. `baseline_prompt_only`
2. `baseline_prompt_only_strong`
3. `baseline_relational_instruction`
4. `explicit_rel_state_direct`
5. `explicit_rel_state_projected`

### 3.3 褰撳墠涓嶅仛鐨勫唴瀹?
鍦ㄨ繖鏉?mini-scope 璺嚎閲岋紝**鏆傛椂涓嶅仛**锛?
- `baseline_relational_instruction_retrieval`
- 鏂板鏇村 baseline 鍙樹綋
- tone evaluator 寰皟
- actor LoRA
- controller 钂搁
- 澶氭ā鍨嬫硾鍖?- boundary 浣滀负涓荤粨鏋?
### 3.4 褰撳墠涓荤粨鏋滄寚鏍?
涓荤粨鏋滃彧鐪嬭繖 3 涓細

1. `case-level relational coherence`
2. `abrupt shift rate`
3. `longitudinal consistency`

### 3.5 褰撳墠杈呭姪鍒嗘瀽

杈呭姪鍒嗘瀽鍙繚鐣欒繖 3 涓細

1. `state-to-response alignment`
2. `behavior drift`
3. `realization gap`

---

## 4. 杩欐潯璺嚎鐨勬牳蹇冨亣璁?
### H1

`explicit_rel_state_direct` 鐩告瘮 prompt-only baselines锛屾洿灏戝嚭鐜扮獊鍏€鐨勫叧绯昏烦鍙樸€?
### H2

`explicit_rel_state_direct` 鐩告瘮涓変釜 baseline锛屾洿瀹规槗褰㈡垚 case-level relational coherence銆?
### H3

濡傛灉 `explicit_rel_state_projected` 鐩告瘮 `explicit_rel_state_direct` 杩涗竴姝ユ彁鍗囦簡鍏崇郴杩炶疮鎬э紝鍒欒鏄庡弻灞備腑闂村眰锛堝叧绯绘€?-> 琛屼负鎬侊級鍙兘浼樹簬鍗曞眰涓棿灞傘€?
### H4

濡傛灉 `explicit_rel_state_direct` 鎴?`explicit_rel_state_projected` 鐨勫唴閮ㄧ姸鎬佸眰杈冪ǔ瀹氾紝浣嗘渶缁堣緭鍑轰粛鐒朵笉澶熻繛璐紝鍒欒鏄庡瓨鍦?`realization gap`锛岃€屼笉鏄樉寮忕姸鎬佸眰鏈韩娌℃湁浠峰€笺€?
---

## 5. Go/No-Go 鍒ゆ柇鏍囧噯

杩欐潯灏?scope 璺嚎鐨勭洰鏍囦笉鏄€滃仛瀹岃鏂団€濓紝鑰屾槸灏藉揩鍒ゆ柇鏄惁鍊煎緱缁х画銆?
### 5.1 Go 鏉′欢

婊¤冻涓嬮潰浠绘剰涓ゆ潯锛屽嵆鍙户缁帹杩涳細

1. `explicit_rel_state_direct` 鍦?`case-level relational coherence` 涓婄ǔ瀹氫紭浜庤嚦灏戜袱涓?baseline
2. `explicit_rel_state_direct` 鐨?`abrupt shift rate` 鏄庢樉鏇翠綆
3. `baseline_relational_instruction` 浠嶆棤娉曠ǔ瀹氳拷骞?`explicit_rel_state_direct`
4. `explicit_rel_state_projected` 鐩告瘮 `explicit_rel_state_direct` 鍛堢幇鍑洪澶栨彁鍗囪秼鍔?5. 瀛樺湪涓€鎵规竻妤氱殑 `realization gap` 鏍锋湰锛岃鏄庘€滄樉寮忕姸鎬佸眰鏈韩鍙兘鏈変环鍊硷紝浣嗚緭鍑哄疄鐜版湁闂鈥?
### 5.2 No-Go 鏉′欢

婊¤冻涓嬮潰浠绘剰涓€鏉★紝灏卞簲璁ょ湡鑰冭檻鍋滄杩欐潯璁烘枃瀛愰锛?
1. `explicit_rel_state_direct` 鍜屽己 baseline 娌℃湁绋冲畾宸紓
2. 涓昏宸紓鍙綋鐜板湪鈥滄洿鐭€佹洿淇濆畧鈥濓紝浣嗕笉鑳戒綋鐜版洿杩炶疮
3. judge 寰堥毦绋冲畾鍖哄垎鍏崇郴璺冲彉鍜屽叧绯昏繛璐€?4. `baseline_relational_instruction` 宸插熀鏈拷骞虫垨瓒呰繃 `explicit_rel_state_direct`

### 5.3 涓€涓噸瑕佺殑涓棿缁撹绫诲瀷

杩欐潯 mini-scope 璺嚎闄や簡 `Go` 鍜?`No-Go` 涔嬪锛岃繕鍙兘鍑虹幇涓€绉嶅緢閲嶈鐨勪腑闂寸粨璁猴細

- `direct/projected` 鍦ㄨ瑷€灞備笉浼樹簬寮?baseline
- 浣嗗唴閮ㄧ姸鎬佹參鍙樻槸鎴愮珛鐨?- 涓斿己 baseline 宸茬粡寰堣兘鎵?
濡傛灉鍑虹幇杩欑缁撴灉锛屽畠骞朵笉鍙槸鈥滃け璐モ€濓紝杩樺彲鑳芥敮鎸佷竴涓洿鏈夌爺绌跺懗閬撶殑鍒ゆ柇锛?
- **宸ョ▼鐩磋涓婄湅浼兼洿鍚堢悊鐨勭粨鏋勫寲鎺у埗锛屽苟涓嶄細鑷姩甯︽潵鏇村ソ鐨勮瑷€灞傝〃鐜般€?*
- **寮?prompt baseline 鍙兘宸茬粡鍚冩帀浜嗗緢澶氳〃闈㈡敹鐩娿€?*
- **鐪熸鐨勭摱棰堝彲鑳藉湪 realization锛岃€屼笉鏄?state existence銆?*

杩欑缁撴灉鍙互琚涓猴細

- 绗竴闃舵 seed paper / workshop paper 鐨勪竴绉嶅彲鎺ュ彈缁撹

鑰屼笉鏄繀椤诲綋鍦烘斁寮冩暣鏉＄爺绌舵€濊矾銆?
---

## 6. 1-2 鍛ㄦ渶灏忓疄楠屾柟妗?
## 绗?1 姝ワ細鍐荤粨瀹為獙缁勪笌闂瀹氫箟

### 瑕佸仛浠€涔?
- 涓嶅啀澧炲姞鏂扮殑 baseline
- 涓嶅啀淇敼涓婚棶棰?- 涓嶅啀鎵╁ぇ瀹為獙鑼冨洿

### 瀹屾垚鏍囧噯

- 褰撳墠姣旇緝缁勫喕缁撲负 5 缁?- 涓荤粨鏋滄寚鏍囧喕缁撲负 3 涓?
### 棰勬湡浜у嚭

- 杩欎唤鏂囨。
- 涓庝箣瀵归綈鐨?proposal / execution plan

---

## 绗?2 姝ワ細璺?smoke set

### 瑕佸仛浠€涔?
浣跨敤锛?
- [paper_cases_smoke.json](/d:/My Project/companion-ai/paper_cases_smoke.json)

杩愯 5 缁勶細

1. `baseline_prompt_only`
2. `baseline_prompt_only_strong`
3. `baseline_relational_instruction`
4. `explicit_rel_state_direct`
5. `explicit_rel_state_projected`

### 鍛戒护

```bash
python paper_run_experiment.py --cases-json paper_cases_smoke.json --output paper_results_smoke.jsonl
```

### 鐩殑

涓嶆槸鍑鸿鏂囩粨璁猴紝鑰屾槸纭锛?
1. 鍥涚粍閮借兘绋冲畾璺戦€?2. `baseline_relational_instruction` 鏄惁鏄庢樉姣?`baseline_prompt_only_strong` 鏇村己
3. `explicit_rel_state_direct` 鏄惁鐩稿 baseline 鍑虹幇绯荤粺鎬т紭鍔?4. `explicit_rel_state_projected` 鏄惁鐩稿 `explicit_rel_state_direct` 鍛堢幇棰濆瓒嬪娍

### 棰勬湡杈撳嚭

- [paper_results_smoke.jsonl](/d:/My Project/companion-ai/paper_results_smoke.jsonl)

### 濡傛灉鍑虹幇涓嶅悓缁撴灉

#### 缁撴灉 A锛氬洓缁勯兘鑳借窇锛屼笖 `baseline_relational_instruction` 鏄庢樉姣?strong prompt 鏇村儚鈥滃叕骞冲己 baseline鈥?- 杩涘叆涓嬩竴姝?
#### 缁撴灉 B锛歚baseline_relational_instruction` 闈炲父寮?- 鍏堜慨 baseline 閫昏緫锛屼笉鍋?judge

#### 缁撴灉 C锛歚baseline_relational_instruction` 鐩存帴杩藉钩 `explicit_rel_state_direct`
- 杩欐潯璁烘枃绾块闄╂樉钁椾笂鍗囷紝浣嗕粛鍙厛鍋氬皬瑙勬ā judge 纭

---

## 绗?3 姝ワ細鍋氭渶灏?judge 妯℃澘

### 瑕佸仛浠€涔?
涓嶈绔嬪埢鍋氬鏉傜殑 alignment judge銆?
鍏堝彧鍋氫袱涓洿澶栭儴鐨勯棶棰橈細

1. **鏁存 case 鏄惁鍍忓悓涓€涓叧绯昏繃绋嬪湪杩炵画婕斿寲锛?*
2. **杩欐 case 鏄惁鍑虹幇浜嗘槑鏄剧殑绐佸厐浜茶繎 / 绐佸厐鎶界 / 琛ュ伩鎬х儹鎯咃紵**

### judge 褰㈠紡

浼樺厛浣跨敤锛?
- case-level judge
- pairwise comparison judge

鑰屼笉鏄厛鍋?turn-level 鍐呴儴鐘舵€佸榻愭墦鍒嗐€?
### 姣忎釜 case 鐨?judge 杈撳嚭寤鸿

```json
{
  "case_id": "smoke_warm_001",
  "experiment_mode": "explicit_rel_state_direct",
  "relational_coherence_score": 4,
  "has_abrupt_shift": false,
  "reason": "鏁翠綋鍏崇郴鍙樺寲娓愯繘锛屾病鏈夌獊鐒舵媺杩戞垨绐佺劧鎶界銆?
}
```

### pairwise preference 杈撳嚭寤鸿

```json
{
  "case_id": "smoke_warm_001",
  "comparison": ["explicit_rel_state_direct", "baseline_prompt_only_strong"],
  "winner": "explicit_rel_state_direct",
  "criterion": "relational_coherence",
  "reason": "explicit_rel_state_direct 鍦ㄤ笁杞噷鏇村儚鍚屼竴娈靛叧绯绘紨鍖栬繃绋嬨€?
}
```

### 瀹屾垚鏍囧噯

- 鏈変竴濂楃ǔ瀹氱殑 judge prompt / 妯℃澘
- 鍦ㄥ皯閲?case 涓婅嚜娲斤紝涓嶈嚦浜庢槑鏄句贡鍒?
### 濡傛灉鍑虹幇涓嶅悓缁撴灉

#### 缁撴灉 A锛歫udge 寰堢ǔ瀹?- 杩涘叆涓嬩竴姝?
#### 缁撴灉 B锛歫udge 缁撴灉寰堜贡
- 鍏堟敼 judge 闂锛屼笉鍋氬ぇ瑙勬ā瀹為獙

---

## 绗?4 姝ワ細瀵?smoke set 鍋氫富缁撴灉璇勬祴

### 瑕佸仛浠€涔?
鍏堝彧瀵?smoke set 鍋氾細

1. `case-level relational coherence`
2. `abrupt shift rate`
3. `pairwise preference`

### 鐩殑

灏藉揩鍥炵瓟锛?
- `explicit_rel_state_direct` 鏄惁鐪熺殑鍦ㄢ€滃叧绯昏繛璐€р€濅笂鏈夊噣鏀剁泭
- `explicit_rel_state_projected` 鏄惁姣?`explicit_rel_state_direct` 鏇磋繘涓€姝?- 杩樻槸鍙槸鍦ㄩ暱搴︺€佷繚瀹堢▼搴︿笂鍜?baseline 涓嶄竴鏍?
### 瀹屾垚鏍囧噯

- 瀵?6 涓?case 脳 5 缁?缁欏嚭 case-level judge 缁撴灉
  - 瀵瑰叧閿粍瀵规瘮缁欏嚭 pairwise 缁撴灉锛?  - `explicit_rel_state_direct` vs `baseline_prompt_only`
  - `explicit_rel_state_direct` vs `baseline_prompt_only_strong`
  - `explicit_rel_state_direct` vs `baseline_relational_instruction`
  - `explicit_rel_state_projected` vs `explicit_rel_state_direct`

### 棰勬湡杈撳嚭

- 涓€浠?smoke result summary
- 涓€浠?pairwise summary

### 濡傛灉鍑虹幇涓嶅悓缁撴灉

#### 缁撴灉 A锛歚explicit_rel_state_direct` 绋冲畾鏇村ソ
- 杩涘叆绗?5 姝?
#### 缁撴灉 B锛歚explicit_rel_state_direct` 鍙槸鍦ㄢ€滄洿鐭洿淇濆畧鈥濅笂涓嶅悓锛屼絾 coherence 涓嶅崰浼?- 杩欐潯璺嚎寰堝嵄闄╋紝鍏堜笉瑕佺户缁墿澶?
#### 缁撴灉 C锛歚baseline_relational_instruction` 鎺ヨ繎 `explicit_rel_state_direct`
- 杩欐潯璺嚎瑕佷箞鏀剁缉 claim锛岃涔?go/no-go 鍊惧悜 No-Go

---

## 绗?5 姝ワ細鍙湪 smoke 閫氳繃鍚庡啀璺?20-case 姝ｅ紡瀹為獙

### 鍓嶇疆鏉′欢

鍙湁褰撶 4 姝ュ嚭鐜版瘮杈冩槑纭殑绉瀬瓒嬪娍鏃讹紝鎵嶈繘鍏ヨ繖涓€姝ャ€?
### 瑕佸仛浠€涔?
璺戯細

- [paper_cases_v1.json](/d:/My Project/companion-ai/paper_cases_v1.json)

### 浠嶇劧鍙仛褰撳墠 5 缁?
1. `baseline_prompt_only`
2. `baseline_prompt_only_strong`
3. `baseline_relational_instruction`
4. `explicit_rel_state_direct`
5. `explicit_rel_state_projected`

### 姝ｅ紡涓荤粨鏋滃彧鐪?
1. `case-level relational coherence`
2. `abrupt shift rate`
3. `longitudinal consistency`

杈呭姪鍒嗘瀽鍚庣疆锛?
- `state-to-response alignment`
- `behavior drift`
- `realization gap`

---

## 绗?6 姝ワ細1-2 鍛ㄥ悗鐨勬渶缁堢粨璁?
涓ゅ懆鍐咃紝杩欐潯 mini-scope 璁烘枃璺嚎鍙渶瑕佸洖绛斾竴鍙ヨ瘽锛?
**鏄惧紡鍏崇郴鎬佷腑闂村眰锛屾槸鍚﹀湪鈥滃噺灏戝叧绯昏烦鍙樸€佹彁鍗囧叧绯昏繛璐€р€濊繖涓洿澶栭儴鐨勯棶棰樹笂锛屽睍鐜板嚭鍊煎緱缁х画鐮旂┒鐨勮秼鍔裤€?*

### 濡傛灉绛旀鏄?Yes

璇存槑锛?
- 杩欐潯璁烘枃瀛愰鍊煎緱缁х画
- 鍚庣画鍙啀鑰冭檻锛?  - 杈呭姪鎸囨爣
  - tone evaluator 寰皟
  - 鏇村己 baseline

### 濡傛灉绛旀鏄?No

璇存槑锛?
- 杩欐潯璁烘枃瀛愰涓嶅€煎緱缁х画澶ф姇鍏?- 椤圭洰搴斿洖鍒颁骇鍝?绯荤粺涓荤嚎
- 涓嶅啀璁╄鏂囪矾绾夸富瀵煎綋鍓嶅紑鍙戝喅绛?
### 琛ュ厖锛歂o-Go 涓嶇瓑浜庝骇鍝佺粨鏋勬棤浠峰€?
濡傛灉褰撳墠闃舵鏈€缁堝緱鍒扮殑鍙槸锛?
- `explicit_rel_state_direct/projected` 鍦ㄨ瑷€灞傛病鏈夌ǔ瀹氫紭浜庡己 baseline

杩欐洿鍚堢悊鐨勮В閲婇€氬父鏄細

- 褰撳墠鏄惧紡鐘舵€佽緭鍏?+ 褰撳墠 prompt 瀹炵幇
- 杩樻病鏈夋妸缁撴瀯鍖栫姸鎬佺ǔ瀹氬厬鐜版垚璇█灞備紭鍔?
琛ュ厖锛?
- 灏忚妯?prompt-bridging 璇婃柇宸茬粡琛ㄦ槑锛岀姸鎬佸憟鐜版柟寮忎細褰卞搷杈撳嚭鍒嗗竷锛屽洜姝ゅ師濮?prompt 瀹炵幇骞朵笉鏄腑鎬х殑锛?- 浣?bridge 鍙樹綋骞舵病鏈夌ǔ瀹氳〃鐜板嚭鏄庢樉浼樹簬寮?baseline 鐨勮瑷€灞傛晥鏋滐紱
- 鍥犺€屽綋鍓嶅彲浠ュ厛鍋氫竴涓樁娈垫€у垽鏂細
  - prompt bridge 涓嶆槸瀹屽叏鏃犲叧锛?  - 浣嗗畠涓嶅儚涓昏鐭涚浘锛?  - 鐪熸鐨勪富瑕佺摱棰堟洿鍙兘浣嶄簬琛ㄧず鏀剁泭鏈夐檺锛屾垨鏈井璋?LLM 鐨?realization boundary銆?
瀹冨苟涓嶈嚜鍔ㄦ剰鍛崇潃锛?
- 鏄惧紡鍏崇郴鎬佺粨鏋勫浜у搧娌℃湁浠峰€?
鍥犱负褰撳墠浜у搧缁撴瀯浠嶅彲鑳藉湪涓嬮潰杩欎簺鏂归潰淇濇寔浠峰€硷細

- 鍙В閲婃€?- 鍙皟璇曟€?- 鍙帶鎬?- 鍚庣画璁粌鍜岃捀棣忔帴鍙?
鍥犳锛岃繖鏉?mini-scope 璺嚎鐨?`No-Go` 鍙槸鍚﹀畾锛?
- 鈥滃綋鍓嶈繖鏉?seed paper 鏄惁鍊煎緱缁х画浣滀负璇█灞傛晥鏋滆鏂囨帹杩涒€?
鑰屼笉鏄洿鎺ュ惁瀹氾細

- 鈥滄樉寮忓叧绯绘€佹槸鍚﹀€煎緱缁х画浣滀负浜у搧鍜岃缁冮鏋跺瓨鍦ㄢ€?
### 琛ュ厖锛氫骇鍝佷环鍊间笌璇█灞傜粨鏋滃垎寮€鍒ゆ柇

鍗充娇 `direct/projected` 鍦ㄨ瑷€灞備笉浼樹簬寮?baseline锛屽洓缁村叧绯绘€?/ 鍏淮琛屼负鎬佷粛鍙兘鍦ㄤ骇鍝佸眰闈繚鎸佹槑鏄句环鍊硷紝渚嬪锛?
- 鍙В閲婃€?- 鍙皟璇曟€?- 鍙帶鎬?- 璁粌鍜岃捀棣忔帴鍙?- 闀挎湡绯荤粺鍒嗘瀽

鍥犳锛岃繖鏉?mini-scope 璺嚎涓昏妫€楠岀殑鏄細

- **鏄惧紡鐘舵€佺粨鏋勮兘鍚﹀湪褰撳墠鏈井璋冩潯浠朵笅鑷劧浣撶幇涓烘洿濂界殑璇█灞傚叧绯昏繛璐€?*

鑰屼笉鏄洿鎺ュ垽瀹氾細

- **鏄惧紡鐘舵€佺粨鏋勬湰韬槸鍚﹀€煎緱瀛樺湪浜庝骇鍝佷腑**

### 琛ュ厖锛歄racle State 闃舵鎬у彂鐜?
鍦?prompt-bridging 涔嬪悗锛屽張琛ュ仛浜嗕竴杞渶灏?`oracle state` 瀵圭収瀹為獙锛?
- 鐩存帴涓烘瘡涓?phase 鍐欏畾 `oracle_relational_summary`
- 鍚屾椂涓?projected 鐗堟湰鍐欏畾 `oracle_behavior_summary`
- 姣旇緝锛?  - `explicit_rel_state_direct_oracle`
  - `explicit_rel_state_projected_oracle`

褰撳墠闃舵鎬х粨鏋滄槸锛?
- `projected_oracle` 鏄庢樉姣?`direct_oracle` 鏇寸煭銆佹洿鍏嬪埗銆佹洿鍍忓彲鎵ц鎺у埗閾撅紱
- `direct_oracle` 鍗充娇鎷垮埌 oracle 鍏崇郴鎽樿锛屼緷鐒跺鏄撳啓鎴愰暱瑙ｉ噴銆侀€夐」鍫嗗彔銆佽繃閲嶉櫔浼磋〃杈撅紱
- 鍥犳锛岃繖杞粨鏋滀笉鏀寔鈥滀富瑕佹槸涓婃父 updater 澶櫔鈥濈殑瑙ｉ噴锛?- 鏇存敮鎸侊細
  - 鍗曞眰鍏崇郴鎬佹憳瑕?-> 璇█ 鐨勭害鏉熷姏涓嶅锛?  - 鍙屽眰鍏崇郴鎬?-> 琛屼负鎬?-> 璇█ 鏇村儚鏈夋晥鎺у埗缁撴瀯锛?  - 涓昏鐡堕鏇村儚 `state-to-language realization` 鐨勭粨鏋勮璁°€?
杩欎娇褰撳墠 mini-scope 璺嚎閲屼竴涓洿鍊煎緱缁х画鐪嬬殑瀛愰棶棰樺彉鎴愶細

- **鍗曞眰鍏崇郴鎬佹帶鍒?vs 鍙屽眰鍏崇郴鎬?琛屼负鎬佹帶鍒讹紝鍦ㄩ暱绋嬩簰鍔ㄤ腑鐨勫樊寮傝竟鐣屻€?*

---

## 7. 鍦ㄨ繖鏉?mini-scope 璺嚎瀹屾垚涔嬪墠锛屼笉鑰冭檻浠€涔?
鍦ㄥ畬鎴愪笂杩?go/no-go 鍒ゆ柇涔嬪墠锛屾殏鏃朵笉鑰冭檻锛?
- tone evaluator 寰皟
- actor 寰皟
- controller 钂搁
- 澶氭ā鍨嬪疄楠?- 鏇村鏉?retrieval baseline
- 鎶婃洿澶氫骇鍝佹ā鍧楀啓杩涜鏂?
鍘熷洜寰堢畝鍗曪細

濡傛灉杩欐潯灏忛鏈韩閮戒笉鑳界珯浣忥紝鍚庨潰鍐嶅姞澶嶆潅搴﹀彧浼氭洿涔便€?## 琛ュ厖璁板綍锛歋cheme B 闃舵鎬у彂鐜?
鍦?`oracle state` 缁撴灉琛ㄦ槑 `projected_oracle` 鏄庢樉浼樹簬 `direct_oracle` 涔嬪悗锛屽張缁х画琛ュ仛浜嗕竴涓洿鍏抽敭鐨勫鐓э細

- `baseline_relational_instruction`
- `explicit_rel_state_projected`
- `explicit_rel_state_projected_oracle`

鐩爣寰堢洿鎺ワ細

- 鐪?`projected_oracle` 鏄惁宸茬粡鑳芥槑鏄捐秴杩囧己 baseline锛?- 濡傛灉娌℃湁锛岃鏄庡己 baseline 渚濈劧闈炲父鑳芥墦锛岃€屽弻灞傜粨鏋勭殑璇█灞備紭鍔垮苟涓嶄細鑷姩閲婃斁鍑烘潵銆?
鍙鐜板懡浠わ細

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_v1.json --output paper_results_scheme_b_v1.jsonl --modes baseline_relational_instruction explicit_rel_state_projected explicit_rel_state_projected_oracle
python paper_eval.py --input paper_results_scheme_b_v1.jsonl --out-dir paper_eval_scheme_b_v1_out
```

褰撳墠闃舵鍙互鏀寔鐨勫垽鏂細

- `projected_oracle` 鏄庢樉浼樹簬鐪熷疄 `projected`锛?- 杩欒鏄庡弻灞傛帶鍒堕摼鍦ㄧ悊鎯冲寲鏉′欢涓嬬‘瀹炴湁娼滃姏锛?- 浣?`projected_oracle` 鏄惁宸茬粡绋冲畾浼樹簬 `baseline_relational_instruction`锛屽綋鍓嶄粛涓嶈兘涓嬪己缁撹锛?- 鍥犺€屾洿鍚堢悊鐨勪腑闂寸粨璁烘槸锛?  - 鍙屽眰缁撴瀯鐨勬綔鍔涘瓨鍦紱
  - 鐪熷疄閾捐矾娌℃湁绋冲畾閲婃斁杩欑娼滃姏锛?  - 寮?baseline 宸茬粡鍚冩帀浜嗗緢澶氳瑷€灞傝〃闈㈡敹鐩娿€?
## 琛ュ厖璁板綍锛欳ooling 绫诲鐜?
涓轰簡纭 `scheme B` 鐨勬ā寮忔槸鍚︿細鍦ㄥ叾瀹冮暱绋嬭建杩逛腑閲嶅鍑虹幇锛屽張琛ュ仛浜嗕竴涓?cooling 绫?long case锛?
- [paper_cases_oracle_cooling_v1.json](/d:/My%20Project/companion-ai/paper_cases_oracle_cooling_v1.json)

鍙鐜板懡浠わ細

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_cooling_v1.json --output paper_results_scheme_b_cooling_v1.jsonl --modes baseline_relational_instruction explicit_rel_state_projected explicit_rel_state_projected_oracle
python paper_eval.py --input paper_results_scheme_b_cooling_v1.jsonl --out-dir paper_eval_scheme_b_cooling_v1_out
```

浜哄伐 judge 璁板綍锛?
- [manual_judge_results.md](/d:/My%20Project/companion-ai/paper_eval_scheme_b_cooling_v1_out/manual_judge_results.md)

褰撳墠 cooling case 鐨勪汉宸ュ垽鏂负锛?
- `projected_oracle > projected`
  - 鏀寔
- `projected_oracle > baseline_relational_instruction`
  - 涓嶆敮鎸佸己缁撹锛屾洿绋冲Ε鐨勫垽鏂槸 `tie`

杩欐剰鍛崇潃涔嬪墠鐨勬ā寮忓湪绗笁绉嶈建杩逛笂鍐嶆鍑虹幇锛?
1. oracle 涓ゅ眰鎺у埗閾惧弽澶嶈〃鐜板嚭姣旂湡瀹?`projected` 鏇撮珮鐨勫叧绯昏繛璐€э紱
2. 寮?baseline 鍙嶅琛ㄧ幇鍑虹珵浜夊姏锛?3. 褰撳墠鏈€绋冲Ε鐨?go/no-go 鍒ゆ柇锛屾鍦ㄤ粠鈥滄樉寮忓叧绯绘€佹槸鍚︿紭浜?baseline鈥濊浆鍚戔€滅悊鎯冲寲涓ゅ眰鎺у埗鍦ㄧ粨鏋勪笂鏈夋綔鍔涳紝浣嗙湡瀹為摼璺皻鏈ǔ瀹氬厬鐜拌娼滃姏鈥濄€?

## 绗竴闃舵闃舵鎬х粨璁?
鎴嚦褰撳墠闃舵锛岃繖鏉?mini-scope 璺嚎宸茬粡璺戦€氬苟瀹屾垚浜嗕互涓嬪叧閿楠わ細

- short smoke
- long-range case 鍒濇楠岃瘉
- prompt-bridging 璇婃柇
- oracle state 璇婃柇
- `scheme B` 瀵圭収
- warming / vulnerability / cooling 涓夌被 case 鐨勪汉宸?judge

### 褰撳墠鑳芥垚绔嬬殑缁撹

1. 鍏崇郴鎬佷綔涓?slow variable 鐨勫缓妯″墠鎻愭槸鎴愮珛鐨勩€?2. 鍗曞眰鍏崇郴鎬佹憳瑕?-> 璇█ 鐨勬帶鍒跺姏涓嶈冻锛宍direct` / `direct_oracle` 閮藉鏄撻噸鏂板彉閲嶃€?3. `projected_oracle > projected` 宸插湪澶氱被 case 涓婇噸澶嶅嚭鐜帮紝璇存槑鍙屽眰缁撴瀯鍦ㄧ悊鎯虫潯浠朵笅鏈夋綔鍔涖€?4. 寮?baseline 渚濈劧寰堟湁绔炰簤鍔涳紝`projected_oracle > 寮?baseline` 浠嶆湭褰㈡垚绋冲畾璺?case 寮鸿瘉鎹€?5. prompt bridge 涓嶆槸瀹屽叏鏃犲叧锛屼絾鐩墠涓嶅儚涓昏鐡堕銆?
### 褰撳墠涓嶈兘鎴愮珛鐨勭粨璁?
1. 涓嶈兘璇?`explicit_rel_state_projected` 宸茬粡绋冲畾浼樹簬 `baseline_relational_instruction`銆?2. 涓嶈兘璇存樉寮忓叧绯绘€佸凡缁忚嚜鍔ㄥ甫鏉ヨ瑷€灞備紭鍔裤€?3. 涓嶈兘璇翠笂娓?updater 鏄綋鍓嶄富瑕侀棶棰樻潵婧愩€?
### 褰撳墠鏈€鍚堢悊鐨?paper-seed 瀹氫綅

濡傛灉缁х画鎶婄涓€闃舵鍐欐垚 seed paper / workshop-style paper锛屾洿绋冲Ε鐨勮〃杩板簲璇ユ槸锛?
- 鏄惧紡鍏崇郴鎬佷綔涓?slow variable 鏄悎鐞嗙殑鎺у埗 substrate锛?- 鍗曞眰鎺у埗涓嶈冻浠ョǔ瀹氱害鏉熻瑷€瀹炵幇锛?- 鍙屽眰鎺у埗鍦?oracle 鏉′欢涓嬭〃鐜板嚭娼滃姏锛?- 浣嗙湡瀹為摼璺繕娌℃湁绋冲畾鍏戠幇杩欑娼滃姏锛?- 寮?baseline 鐨勭珵浜夊姏璇存槑涓昏闅剧偣鏇村彲鑳戒綅浜?realization锛岃€屼笉鏄?state existence銆?
### 褰撳墠 go/no-go 鍒ゆ柇

褰撳墠缁撴灉鏇村儚锛?
- **寮?Go / 鏉′欢鎬?Go**

涔熷氨鏄細

- 杩欐潯绾挎病鏈夎鍚︽帀锛?- 浣嗗畠鏇撮€傚悎浣滀负涓€涓€渞ealization gap / control boundary鈥濈殑 paper seed锛?- 鏆傛椂杩樹笉鏀寔鎶婂畠鍐欐垚鈥滄樉寮忓叧绯绘€佹樉钁椾紭浜庡己 baseline鈥濈殑姝ｇ粨璁鸿鏂囥€?

### 鏀跺熬 Todo锛歮ixed-signal long case

浣滀负绗竴闃舵鏀跺熬楠岃瘉锛屼粛寤鸿琛ヤ竴鏉?`mixed_signal` long case銆?
鐩殑涓嶆槸鍐嶆墿涓婚锛岃€屾槸鍥炵瓟涓€涓洿绐勭殑闂锛?
- 褰撳墠鍦?warming / vulnerability / cooling 涓夌被杞ㄨ抗涓婄湅鍒扮殑妯″紡锛屾槸鍚︿細鍦ㄢ€滀俊鍙锋洿娣锋潅銆佹洿涓嶇ǔ瀹氣€濈殑鍏崇郴杞ㄨ抗涓户缁嚭鐜般€?
濡傛灉鍚庣画琛ュ仛 mixed-signal case锛屼紭鍏堢湅锛?
1. `projected_oracle > projected` 鏄惁浠嶉噸澶嶅嚭鐜帮紱
2. `projected_oracle` 涓?`baseline_relational_instruction` 鏄惁缁х画鎺ヨ繎 `tie`锛?3. 寮?baseline 鏄惁鍦?mixed-signal 鏉′欢涓嬪紑濮嬫槑鏄鹃€€鍖栥€?
濡傛灉 mixed-signal 涔熼噸澶嶅綋鍓嶆ā寮忥紝鍒欑涓€闃舵鐨勯樁娈垫€х粨璁轰細鏇寸ǔ銆?

## 琛ュ厖璁板綍锛歱rojected_oracle vs baseline 鐨勫綋鍓嶈瘉鎹竟鐣?
鍒板綋鍓嶉樁娈典负姝紝鍏充簬 `projected_oracle` 涓?`baseline_relational_instruction` 鐨勭洿鎺ヨ瘉鎹紝浠嶄富瑕佹潵鑷凡瀹屾垚浜哄伐 judge 鐨勪笁绫?`scheme B` case锛?
- `warming`锛歚tie`
- `vulnerability`锛歚projected_oracle` 鏇翠紭
- `cooling`锛歚tie`

鍥犳褰撳墠鏈€绋冲Ε鐨勫垽鏂笉鏄細

- `projected_oracle` 宸茬粡绋冲畾浼樹簬寮?baseline

涔熶笉鏄細

- 寮?baseline 宸茬粡鏄庢樉鍘嬭繃 `projected_oracle`

鑰屾槸锛?
- **涓よ€呯洰鍓嶄粛澶勪簬鐪熷疄绔炰簤鐘舵€侊紝浣嗗皻鏈垎鍑虹ǔ瀹氳儨璐熴€?*

鍚屾椂锛宍baseline_relational_instruction_oracle_collapsed` vs `projected_oracle` 杩欒疆鈥滄帶鍒朵俊鎭榻愬疄楠屸€濈洰鍓嶈繕娌℃湁瀹屾垚浜哄伐 / LLM judge锛屽洜姝よ繕涓嶈兘鎶婂畠褰撲綔姝ｅ紡 coherence 璇佹嵁锛屽彧鑳藉厛瑙嗕负锛?
- 涓€涓鏄庘€滃悓鏍锋槸 prompt-based realization锛屽弻灞傛弿杩板拰鍗曞眰鍘嬬缉鎻忚堪骞朵笉绛変环鈥濈殑缁撴瀯鎬т俊鍙枫€?
## 鍚庣画蹇呴』淇濈暀鐨勭粓灞€闂

鏃犺绗竴闃舵 mini-scope 濡備綍鏀跺熬锛屽悗缁兘蹇呴』淇濈暀杩欎釜闂锛?
- **`projected` 涓庡己 baseline 鐨勫姣旓紝鏈€缁堣兘鍚﹁鏄庢姇褰卞眰鏈韩鏈夋剰涔夈€?*

杩欎釜闂涔嬫墍浠ヤ笉鑳戒涪锛屾槸鍥犱负瀹冨悓鏃惰繛鎺ワ細

1. 璁烘枃灞傞潰鐨勭粨鏋勬敹鐩婏紱
2. 闀挎湡鍏崇郴/琛屼负鎬佺殑鏄惧紡寤烘ā浠峰€硷紱
3. 浜у搧灞傞潰瀵硅秴闀跨▼銆乽nexpected 鐢ㄦ埛琛屼负鐨勫彲鎺ф€т笌涓€鑷存€ч渶姹傘€?

## Update: Control-Alignment Judge Completed

??? control-alignment ??? judge:

- `explicit_rel_state_projected_oracle`
- `baseline_relational_instruction_oracle_collapsed`

??:
- `oracle_long_warm_001`:`projected_oracle` ??
- `oracle_long_vuln_001`:`projected_oracle` ??

????:
- ????????? oracle ????,
- ??????? collapsed ??????;
- ??????????????????????????? prompt?

## Stage 2 Direction After Stage 1 Wrap-up

???????,??????????????? baseline,????:

1. ????:
   - ?????????
   - ??????
   - ?????
   - ????? + ?????

2. ????:
   - ??????
   - ???? -> ????

3. realization-aware ??:
   - ???????????? / ???????? LLM ????;
   - ???????????????

4. ?????:
   - ?????unexpected ???????,
   - ????????? baseline ??????????????????

## Stage 2 Clarification: Why move to three-way comparison

绗簩闃舵鏀规垚锛?- single-layer
- two-layer
- strong baseline

涓嶆槸鎶婇棶棰樺仛鏁ｏ紝鑰屾槸涓轰簡鍥炵瓟绗竴闃舵宸茬粡鏆撮湶浣嗚繕娌¤В閲婃竻妤氱殑闂锛?
- strong baseline 涓轰粈涔堣繖涔堝己锛?- two-layer 鍒板簳姣?single-layer 澶氫簡浠€涔堬紱
- 涓轰粈涔?oracle two-layer 鏈夋綔鍔涳紝浣?real projected 杩樻病绋冲畾璧?baseline銆?
### 鏈€鏈夊府鍔╃殑瑙傚療

1. oracle two-layer vs oracle collapsed single-layer
- 鐢ㄦ潵鍒ゆ柇鎺ュ彛鍒嗗眰鏈韩鏄惁鏈変环鍊笺€?
2. single-layer vs strong baseline
- 鐢ㄦ潵鍒ゆ柇 baseline 鐨勫己鏄惁鍥犱负瀹冨凡缁忔帴杩?LLM 鏇村鏄撴墽琛岀殑鍗曞眰鎺у埗褰㈠紡銆?
3. oracle two-layer vs strong baseline
- 鐢ㄦ潵鍒ゆ柇 two-layer 鐨勭悊鎯充笂闄愪笌寮?baseline 鐨勮窛绂汇€?
4. real projected vs oracle projected
- 鐢ㄦ潵鍒ゆ柇鐪熷疄閾捐矾鏄惁绋冲畾閲婃斁缁撴瀯娼滃姏銆?
5. phase-aware / repeated-sampling analysis
- 鐢ㄦ潵鍒ゆ柇宸紓鍒板簳浣撶幇鍦?continuation / probe 绛夐暱鏈熼樁娈碉紝杩樻槸鍙槸鍧囧€煎樊寮傘€?
### 绗簩闃舵鐨勪富闂

绗簩闃舵鏇撮€傚悎姝ｅ紡闂細
- 浠€涔堟牱鐨勬樉寮忓叧绯昏〃绀?/ 鎺у埗鎺ュ彛锛屾洿瀹规槗琚?LLM 绋冲畾瀹炵幇涓洪暱鏈熻繛缁殑鍏崇郴琛屼负銆?
鑰屼笉鏄户缁仠鐣欏湪锛?- 鏄惧紡涓棿灞傚拰 baseline 璋佽耽銆?
