# 入力検証
from validation import (
    ValidationErrorInfo,
    ValidationResult,
    validate_password,
)

# 採点
from scoring import (
    calculate_unique_character_score,
    calculate_unique_character_ratio_score,
    calculate_length_score,
    calculate_consecutive_repeat_penalty,
    calculate_repeated_pattern_score,
    calculate_pattern_score,
    check_pattern,
    check_strength,
)

# CLI
from cli import (
    enter_the_password,
    express_result,
    run_cui,
)


# スクリプトとして直接起動した場合だけ実行する
if __name__ == "__main__":
    run_cui()