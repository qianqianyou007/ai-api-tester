"""一键执行：跑所有自动生成的测试 + 输出报告"""
import subprocess
import sys
import os


def run_all_tests():
    """执行所有生成的测试脚本"""
    test_dir = "generated_tests"
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)

    print("=" * 50)
    print("[START] 开始执行 AI 生成的测试用例")
    print("=" * 50)

    # 运行 pytest（含覆盖率统计）
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            test_dir,
            "-v",
            f"--html={report_dir}/test_report.html",
            "--self-contained-html",
            "--tb=short",
            f"--cov={test_dir}",
            f"--cov-report=html:{report_dir}/coverage",
            "--cov-report=term",
        ],
        capture_output=False,
    )

    print("\n" + "=" * 50)
    if result.returncode == 0:
        print("[DONE] 全部测试通过！")
    else:
        print(f"[WARN] 有测试失败（exit code: {result.returncode}），查看报告了解详情")

    print(f"[REPORT] HTML 报告: {report_dir}/test_report.html")
    print(f"[REPORT] 覆盖率报告: {report_dir}/coverage/index.html")
    return result.returncode


if __name__ == "__main__":
    sys.exit(run_all_tests())