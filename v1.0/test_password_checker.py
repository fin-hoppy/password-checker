
import unittest
import io

from contextlib import redirect_stdout
from unittest.mock import patch

# テスト対象の本体プログラムを読み込む
import password_checker as pc


# --------------------------------------------------
# 1. 入力検証の単体テスト
# --------------------------------------------------

class TestValidation(unittest.TestCase):

    def test_empty_password(self):
        # 空文字列が拒否されることを確認
        result = pc.validate_password("")

        self.assertFalse(result.is_valid)
        self.assertEqual(
            [error.code for error in result.errors],
            ["EMPTY_PASSWORD"]
        )

    def test_whitespace_password(self):
        # 半角スペースのみの入力を拒否する
        result = pc.validate_password("   ")

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].code,
            "WHITESPACE_PASSWORD"
        )

    def test_non_ascii_password(self):
        # 日本語を含む入力では2種類のエラーが発生する
        result = pc.validate_password("abcあ")

        codes = [error.code for error in result.errors]

        self.assertFalse(result.is_valid)
        self.assertIn("NON_ASCII_PASSWORD", codes)
        self.assertIn("INVALID_CHARACTER", codes)

    def test_control_character(self):
        # タブ文字はASCIIだが印字可能文字ではない
        result = pc.validate_password("abc\tdef")

        codes = [error.code for error in result.errors]

        self.assertFalse(result.is_valid)
        self.assertEqual(codes, ["INVALID_CHARACTER"])

    def test_valid_password(self):
        # 半角スペースを含む有効な入力
        result = pc.validate_password("abc def")

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_printable_ascii_boundaries(self):
        # ASCIIコード32（スペース）と126（~）を許可
        result = pc.validate_password("a ~")

        self.assertTrue(result.is_valid)


# --------------------------------------------------
# 2. 文字の種類数・割合・長さの単体テスト
# --------------------------------------------------

class TestBasicScores(unittest.TestCase):

    def test_unique_character_score(self):
        # 12種類以上なら45点
        self.assertEqual(
            pc.calculate_unique_character_score("abcdefghijkl"),
            45
        )

        # 異なる文字が1種類なら3.75点
        self.assertAlmostEqual(
            pc.calculate_unique_character_score("aaaa"),
            3.75
        )

    def test_unique_character_ratio(self):
        # すべて異なる文字なら20点
        self.assertEqual(
            pc.calculate_unique_character_ratio_score("abcd"),
            20
        )

        # 5文字中3種類なら12点
        self.assertEqual(
            pc.calculate_unique_character_ratio_score("abcab"),
            12
        )

        # 空文字列によるゼロ除算を防止できる
        self.assertEqual(
            pc.calculate_unique_character_ratio_score(""),
            0
        )

    def test_length_score(self):
        # 15文字以上なら20点
        self.assertEqual(
            pc.calculate_length_score("abcdefghijklmno"),
            20
        )

        # 4文字なら20 × 4 / 15点
        self.assertAlmostEqual(
            pc.calculate_length_score("abcd"),
            20 * 4 / 15
        )


# --------------------------------------------------
# 3. 同一文字の連続による減点
# --------------------------------------------------

class TestConsecutivePenalty(unittest.TestCase):

    def test_no_consecutive_repeat(self):
        self.assertEqual(
            pc.calculate_consecutive_repeat_penalty("abcdef"),
            0
        )

    def test_repeat_lengths(self):
        # 各連続長に対応する減点表を検証
        cases = [
            ("aa", 3),
            ("aaa", 8),
            ("aaaa", 15),
            ("aaaaa", 24),
            ("aaaaaa", 30),
        ]

        for password, expected in cases:
            with self.subTest(password=password):
                self.assertEqual(
                    pc.calculate_consecutive_repeat_penalty(password),
                    expected
                )

    def test_multiple_repeat_runs(self):
        # 2連続、3連続、4連続を合算する
        self.assertEqual(
            pc.calculate_consecutive_repeat_penalty("aabbbcccc"),
            26
        )

    def test_penalty_cap(self):
        # 合計減点の上限は30点
        self.assertEqual(
            pc.calculate_consecutive_repeat_penalty("aaB" * 11),
            30
        )


# --------------------------------------------------
# 4. 個別の繰り返しパターン採点
# --------------------------------------------------

class TestPatternScore(unittest.TestCase):

    def test_pattern_score_table(self):
        # 確定した採点表を直接検証する
        cases = [
            ("ab", 2, 12),
            ("ab", 3, 9),
            ("ab", 4, 6),

            ("abc", 2, 10),
            ("abc", 3, 6),
            ("abc", 4, 3),

            ("abcd", 2, 10),
            ("abcd", 3, 6),
            ("abcd", 4, 3),

            ("abcde", 2, 8),
            ("abcde", 3, 3),
            ("abcde", 4, 0),
        ]

        for pattern, count, expected in cases:
            with self.subTest(pattern=pattern, count=count):
                self.assertEqual(
                    pc.calculate_pattern_score([pattern, count]),
                    expected
                )

    def test_check_pattern(self):
        patterns = [
            ["abc", 2],
            ["xyz", 3]
        ]

        self.assertTrue(pc.check_pattern(patterns, "abc"))
        self.assertFalse(pc.check_pattern(patterns, "def"))


# --------------------------------------------------
# 5. 繰り返しパターン探索の単体テスト
# --------------------------------------------------

class TestRepeatedPattern(unittest.TestCase):

    def test_repeated_patterns(self):
        cases = [
            ("abcdef", 15),
            ("abab", 12),
            ("ababab", 9),
            ("abcabc", 10),
            ("abcabcabc", 6),
            ("abcdeXYabcde", 8),
            ("aaaaaa", 15),
            ("ababa", 12),
            ("abababXYZ12345XYZ12345", 8),
        ]

        for password, expected in cases:
            with self.subTest(password=password):
                self.assertEqual(
                    pc.calculate_repeated_pattern_score(password),
                    expected
                )

    def test_case_sensitive(self):
        # 大文字と小文字は別のパターンとして扱う
        self.assertEqual(
            pc.calculate_repeated_pattern_score("abAB"),
            15
        )

    def test_identical_characters_excluded(self):
        # aaやaaaaなど同じ文字だけのパターンは除外
        self.assertEqual(
            pc.calculate_repeated_pattern_score("aaaaaaaa"),
            15
        )


# --------------------------------------------------
# 6. 総合点の単体テスト
# --------------------------------------------------

class TestStrength(unittest.TestCase):

    def test_final_scores(self):
        cases = [
            ("aB3!", 5),
            ("aaaa", 0),
            ("aB3!x", 30),
            ("abcabc", 30),
            ("aaBB11!!", 38),
            ("abcdefghij", 60),
            ("abcdefghijklmno", 100),
        ]

        for password, expected in cases:
            with self.subTest(password=password):
                result = pc.check_strength(password)

                self.assertEqual(result, expected)

                # 最終スコアが整数であることを確認
                self.assertIsInstance(result, int)

    def test_score_range(self):
        passwords = [
            "a",
            "aaaa",
            "aB3!x",
            "abcabcabc",
            "abcdefghijklmno",
        ]

        for password in passwords:
            with self.subTest(password=password):
                score = pc.check_strength(password)

                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 100)


# --------------------------------------------------
# 7. CLI統合テスト
# --------------------------------------------------

class TestCUI(unittest.TestCase):

    def test_valid_input_and_exit(self):
        # 入力操作を模擬し、実際のキーボード入力を不要にする
        with patch(
            "builtins.input",
            side_effect=["aB3!", "2"]
        ):
            output = io.StringIO()

            # print()の出力を文字列として取得する
            with redirect_stdout(output):

                # sys.exit()はSystemExitを発生させる
                with self.assertRaises(SystemExit):
                    pc.run_cui()

            text = output.getvalue()

            self.assertIn("Password is valid.", text)
            self.assertIn("Password strength score: 5", text)
            self.assertIn("Exiting the program.", text)

    def test_invalid_input_and_menu_retry(self):
        # 1回目: 有効なパスワード
        # メニュー: 不正な選択肢0
        # メニュー: 1で再入力
        # 2回目: 無効なパスワード
        # メニュー: 2で終了
        inputs = [
            "aB3!",
            "0",
            "1",
            "abcあ",
            "2",
        ]

        output = io.StringIO()

        with patch("builtins.input", side_effect=inputs) as mock_input:
            with redirect_stdout(output):
                with self.assertRaises(SystemExit):
                    pc.run_cui()

        text = output.getvalue()

        # 最初の入力では採点できている
        self.assertIn("Password strength score: 5", text)

        # 不正なメニュー入力が拒否される
        self.assertIn("Invalid option. Please try again.", text)

        # 無効な入力ではエラーを表示する
        self.assertIn("Password is invalid.", text)
        self.assertIn("NON_ASCII_PASSWORD", text)
        self.assertIn("INVALID_CHARACTER", text)

        # 入力関数が想定どおり5回呼ばれたことを確認
        self.assertEqual(mock_input.call_count, 5)

        # 不正な選択肢の後もパスワード入力へ戻らず、
        # メニューだけが再表示されているか確認する
        self.assertIn(
            "Select an option:",
            mock_input.call_args_list[2].args[0]
        )

        # 選択肢1の後はパスワード入力へ戻る
        self.assertIn(
            "Enter a password:",
            mock_input.call_args_list[3].args[0]
        )


# --------------------------------------------------
# 8. テストの実行
# --------------------------------------------------

if __name__ == "__main__":
    unittest.main()
