import subprocess
import sys
from pathlib import Path


def execute_pipeline():
    print("=" * 60)
    print("[INFO] Starting Lab 5: Production Data Pipeline")
    print("=" * 60)

    # Project root directory
    project_root = Path(__file__).resolve().parent.parent

    # Pipeline scripts
    scripts = [
        "src/validate_data.py",
        "src/preprocess_pipeline.py",
        "src/validate_outputs.py"
    ]

    # Execute each script sequentially
    for script in scripts:

        script_path = project_root / script

        print(f"\n[INFO] ---> Executing {script}...")

        # Check whether the script exists
        if not script_path.exists():
            print(f"[ERROR] Script not found: {script_path}")
            sys.exit(1)

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(project_root),
                check=False
            )

            # Stop if execution fails
            if result.returncode != 0:
                print(
                    f"\n[ERROR] Pipeline halted."
                    f"\nScript failed: {script}"
                    f"\nExit code: {result.returncode}"
                )
                sys.exit(result.returncode)

            print(f"[SUCCESS] Completed: {script}")

        except Exception as error:
            print(f"[ERROR] Failed to execute {script}")
            print(f"[DETAILS] {error}")
            sys.exit(1)

    print("\n" + "=" * 60)
    print("[SUCCESS] Lab 5 Production Pipeline fully executed!")
    print("=" * 60)


if __name__ == "__main__":
    execute_pipeline()