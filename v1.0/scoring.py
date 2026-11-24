# --------------------------------------------------
# 3. 異なる文字数による採点（最大45点）
# --------------------------------------------------

def calculate_unique_character_score(password):
    """
    異なる文字の種類数を評価する。
    12種類以上で45点。
    """

    # set()で重複する文字を除去する
    unique_chars = set(password)

    # 12種類以上の場合は上限を1に制限する
    return 45 * min(len(unique_chars) / 12, 1)


# --------------------------------------------------
# 4. 異なる文字の割合による採点（最大20点）
# --------------------------------------------------

def calculate_unique_character_ratio_score(password):
    """
    全文字数に対する異なる文字数の割合を評価する。
    """

    unique_chars = set(password)

    # 空文字列の場合はゼロ除算を防ぐ
    return (
        20 * len(unique_chars) / len(password)
        if len(password) > 0
        else 0
    )


# --------------------------------------------------
# 5. パスワード長による採点（最大20点）
# --------------------------------------------------

def calculate_length_score(password):
    """
    パスワードの長さを評価する。
    15文字以上で20点。
    """

    length = len(password)

    return 20 * min(length / 15, 1)


# --------------------------------------------------
# 6. 同一文字の連続による減点（最大30点）
# --------------------------------------------------

def calculate_consecutive_repeat_penalty(password):
    """
    同じ文字が連続する区間を検出し、減点額を計算する。

    2連続: 3点
    3連続: 8点
    4連続: 15点
    5連続: 24点
    6連続以上: 30点

    複数の区間の減点を合算し、最大30点とする。
    """

    penalty = 0
    run_lengths = []

    # 現在の連続文字数
    run_length = 1

    # 現在の文字と次の文字を比較する
    for i in range(len(password) - 1):

        if password[i] == password[i + 1]:
            # 同じ文字なら連続文字数を増加させる
            run_length += 1

        else:
            # 連続区間が終わったら長さを記録する
            if run_length > 1:
                run_lengths.append(run_length)

            # 次の区間に向けて初期化する
            run_length = 1

        # パスワード末尾で終わる連続区間も記録する
        if i == len(password) - 2 and run_length > 1:
            run_lengths.append(run_length)

    # 検出した各連続区間に対して減点する
    for p in run_lengths:
        if p == 2:
            penalty += 3
        elif p == 3:
            penalty += 8
        elif p == 4:
            penalty += 15
        elif p == 5:
            penalty += 24
        else:
            penalty += 30

    # 合計減点は最大30点
    if penalty <= 30:
        return penalty
    else:
        return 30


# --------------------------------------------------
# 7. 繰り返しパターンの評価（最大15点）
# --------------------------------------------------

def calculate_repeated_pattern_score(password):
    """
    繰り返し出現する部分文字列を探索する。

    評価条件:
    - 2文字以上
    - 異なる文字を2種類以上含む
    - 大文字と小文字を区別する
    - 重ならない位置に複数回出現する

    複数のパターンが見つかった場合は最低得点を採用する。
    """

    patterns = []

    # パターンの開始位置を選ぶ
    for i in range(len(password)):

        # パターンの終了位置を選ぶ
        for j in range(i + 1, len(password)):

            # password[i:j]はjの直前までを取得する
            pattern = password[i:j]

            if (
                len(set(pattern)) >= 2
                and pattern in password[j:]
                and not check_pattern(patterns, pattern)
            ):
                # 異なる文字を2種類以上含む
                # 現在のパターンの終了位置以降に再出現する
                # まだ登録されていないパターンである

                # str.count()は重複しない出現回数を数える
                patterns.append([
                    pattern,
                    password.count(pattern)
                ])

    # 各パターンの得点を計算し、リストに追加する
    for i in range(len(patterns)):
        patterns[i].append(
            calculate_pattern_score(patterns[i])
        )

    # 繰り返しがない場合は15点
    least_score = 15

    # 最も低い得点を探す
    for i in range(len(patterns)):
        if patterns[i][2] < least_score:
            least_score = patterns[i][2]

    return least_score


# --------------------------------------------------
# 8. 個別パターンの得点計算
# --------------------------------------------------

def calculate_pattern_score(pattern_info):
    """
    パターンの長さと出現回数から得点を計算する。

    pattern_info[0]: パターン文字列
    pattern_info[1]: 出現回数

    戻り値:
        0～15点
    """

    score = 15

    # 2文字のパターン
    if len(pattern_info[0]) == 2:
        match pattern_info[1]:
            case 1:
                score -= 0
            case 2:
                score -= 3
            case 3:
                score -= 6
            case _:
                score -= 9

    # 3～4文字のパターン
    elif len(pattern_info[0]) == 3 or len(pattern_info[0]) == 4:
        match pattern_info[1]:
            case 1:
                score -= 0
            case 2:
                score -= 5
            case 3:
                score -= 9
            case _:
                score -= 12

    # 5文字以上のパターン
    elif len(pattern_info[0]) >= 5:
        match pattern_info[1]:
            case 1:
                score -= 0
            case 2:
                score -= 7
            case 3:
                score -= 12
            case _:
                score -= 15

    return score


# --------------------------------------------------
# 9. パターンの重複登録を防ぐ
# --------------------------------------------------

def check_pattern(patterns, pattern):
    """
    パターンがすでに登録されているか確認する。

    戻り値:
        True: 登録済み
        False: 未登録
    """

    for p in patterns:
        if pattern == p[0]:
            return True

    return False


# --------------------------------------------------
# 10. 総合点の計算
# --------------------------------------------------

def check_strength(password):
    """
    検証済みのパスワードを0～100点で評価する。

    特別ルール:
    - 4文字以下: 長さ以外の加点を0にする
    - 7文字以下: 総合点の上限30点
    - 8～14文字: 総合点の上限60点
    - 15文字以上: 総合点の上限100点

    戻り値:
        int: 0～100の整数
    """

    # 個別の評価関数を呼び出す
    unique_character_score = calculate_unique_character_score(password)
    unique_character_ratio_score = calculate_unique_character_ratio_score(password)
    length_score = calculate_length_score(password)
    consecutive_repeat_penalty = calculate_consecutive_repeat_penalty(password)
    repeated_pattern_score = calculate_repeated_pattern_score(password)

    # 総合点を計算する
    total_score = (
        unique_character_score
        + unique_character_ratio_score
        + length_score
        - consecutive_repeat_penalty
        + repeated_pattern_score
    )


    # 4文字以下は長さによる加点のみ適用
    if len(password) <= 4:
        total_score = length_score - consecutive_repeat_penalty

        if total_score < 0:
            total_score = 0

    # 5～7文字の最大得点は30点
    elif 5 <= len(password) <= 7:

        if total_score < 0:
            total_score = 0
        elif total_score > 30:
            total_score = 30

    # 8～14文字の最大得点は60点
    elif 8 <= len(password) <= 14:

        if total_score < 0:
            total_score = 0
        elif total_score > 60:
            total_score = 60

    # 15文字以上の最大得点は100点
    else:

        if total_score < 0:
            total_score = 0
        elif total_score > 100:
            total_score = 100

    # 小数部分はすべての計算が終わった後に切り捨てる
    return int(total_score)

