import tempfile
import unittest
from pathlib import Path

from ansys_skill_platform.validators import MechanicalValidator


class MechanicalValidatorTests(unittest.TestCase):
    def test_missing_project_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "missing.wbpj"
            report = MechanicalValidator(project).validate()
            self.assertFalse(report.passed)
            self.assertIn("PROJECT_MISSING", report.to_text())

    def test_minimal_project_warns_but_passes_filesystem(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "demo.wbpj"
            files = root / "demo_files" / "dp0" / "SYS" / "MECH"
            files.mkdir(parents=True)
            project.write_text("demo", encoding="utf-8")
            (files / "ds.dat").write_text(
                "MP,EX,1,210000000000\n"
                "d,all,all\n"
                "f,all,fz,-1\n"
                "solve\n"
                "/com,*************** FINISHED SOLVE FOR LS 1 *************\n",
                encoding="utf-8",
            )

            report = MechanicalValidator(project).validate()
            self.assertTrue(report.passed)
            self.assertIn("DSDAT_FOUND", report.to_text())


if __name__ == "__main__":
    unittest.main()
