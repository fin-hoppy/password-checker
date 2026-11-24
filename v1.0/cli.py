import sys

from validation import validate_password
from scoring import check_strength

# --------------------------------------------------
# 11. パスワードの入力
# --------------------------------------------------

def enter_the_password():
    """
    ユーザーからパスワードを入力してもらう。
    入力検証や採点はここでは行わない。
    """

    password = input("Enter a password: ")

    return password


# --------------------------------------------------
# 12. 入力検証結果の表示
# --------------------------------------------------

def express_result(result):
    """
    入力が有効か無効かを表示する。
    無効な場合はすべてのエラーを表示する。
    """

    if result.is_valid:
        print("Password is valid.")

    else:
        print("Password is invalid. Errors:")

        for error in result.errors:
            print(
                f"Code: {error.code}, Message: {error.message}"
            )


# --------------------------------------------------
# 13. CLI全体の制御
# --------------------------------------------------

def run_cui():
    """
    パスワード入力、検証、採点、再入力、終了を制御する。
    """

    # 外側のループ: パスワード入力を繰り返す
    while True:

        # パスワード入力
        password = enter_the_password()

        # 入力検証
        validation_result = validate_password(password)

        # 検証結果を表示
        express_result(validation_result)

        # 有効な入力の場合だけ採点を実施する
        if validation_result.is_valid:
            strength_score = check_strength(password)

            print(
                f"Password strength score: {strength_score}"
            )

        # 内側のループ: メニューの入力を繰り返す
        while True:

            option = input(
                "1.Enter another password\n"
                "2.Exit\n\n"
                "Select an option: "
            )

            if option == "1":
                # 内側のループを抜け、外側の先頭に戻る
                break

            elif option == "2":
                # プログラムを終了する
                print("Exiting the program.")
                sys.exit()

            else:
                # 不正な選択肢の場合はメニューだけを再表示
                print("Invalid option. Please try again.")
                continue
