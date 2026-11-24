# --------------------------------------------------
# 1. 入力検証に関するクラス
# --------------------------------------------------

class ValidationErrorInfo:
    # 1件分の入力エラー情報を保持するクラス
    def __init__(self, code, message):
        self.code = code          # エラーの識別コード
        self.message = message    # エラーの説明文


class ValidationResult:
    # 入力検証全体の結果を保持するクラス
    def __init__(self, errors=None):
        # errorsが指定されていない場合は空リストを作る
        self.errors = errors if errors is not None else []

        # エラーが0件であれば入力は有効と判定する
        self.is_valid = len(self.errors) == 0


# --------------------------------------------------
# 2. パスワードの入力検証
# --------------------------------------------------

def validate_password(password):
    """
    パスワードが入力条件を満たしているか検証する。

    引数:
        password (str): 検証対象のパスワード

    戻り値:
        ValidationResult: 検出したエラーと有効性
    """

    errors = []
    space_count = 0

    # 空文字列を禁止する
    if password == "":
        errors.append(
            ValidationErrorInfo(
                "EMPTY_PASSWORD",
                "Password cannot be empty."
            )
        )

    # 半角スペースの数を調べる
    for char in password:
        if char == " ":
            space_count += 1

    # 半角スペースだけで構成された入力を禁止する
    if space_count == len(password) and len(password) != 0:
        errors.append(
            ValidationErrorInfo(
                "WHITESPACE_PASSWORD",
                "Password cannot contain only whitespace."
            )
        )

    # ASCII以外の文字が含まれていないか確認する
    if password.isascii() != True:
        errors.append(
            ValidationErrorInfo(
                "NON_ASCII_PASSWORD",
                "Password must contain only ASCII characters."
            )
        )

    # ASCIIコード32～126以外の文字を禁止する
    # タブ、改行、制御文字などもここで検出する
    for char in password:
        if ord(char) < 32 or ord(char) > 126:
            errors.append(
                ValidationErrorInfo(
                    "INVALID_CHARACTER",
                    f"Password contains invalid character: {char}"
                )
            )
            # 最初の不正文字を検出した時点で探索を終了
            break

    # 複数のエラーをまとめて返す
    return ValidationResult(errors)
