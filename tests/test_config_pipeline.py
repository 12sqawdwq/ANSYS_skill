import tempfile
import unittest
from pathlib import Path

from ansys_skill_platform.config import load_workflow_config
from ansys_skill_platform.pipeline import PipelineRunner


class ConfigPipelineTests(unittest.TestCase):
    def test_load_yaml_workflow_config(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = root / "workflow.yaml"
            config.write_text(
                """
project:
  solver: mechanical
  path: "demo.wbpj"
  exports: "exports"
benchmark:
  name: cantilever
  fea_tip_displacement_m: -0.00304
  tolerance_percent: 5.0
report:
  output_dir: "reports"
  name: "demo-report"
  formats: ["json", "markdown"]
logging:
  level: DEBUG
""".strip(),
                encoding="utf-8",
            )

            workflow = load_workflow_config(config)
            self.assertEqual(workflow.project.solver, "mechanical")
            self.assertEqual(workflow.project.path, Path("demo.wbpj"))
            self.assertEqual(workflow.benchmark.name, "cantilever")
            self.assertEqual(workflow.report.formats, ["json", "markdown"])
            self.assertEqual(workflow.logging.level, "DEBUG")

    def test_pipeline_writes_reports(self):
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
                "/com,--- Number of solid elements = 10\n"
                "solve\n"
                "/com,*************** FINISHED SOLVE FOR LS 1 *************\n",
                encoding="utf-8",
            )
            config = root / "workflow.yaml"
            config.write_text(
                f"""
project:
  solver: mechanical
  path: "{project}"
benchmark:
  name: cantilever
  fea_tip_displacement_m: -0.00304
  tolerance_percent: 5.0
report:
  output_dir: "{root / 'reports'}"
  name: "demo-report"
  formats: ["json", "markdown"]
""".strip(),
                encoding="utf-8",
            )

            report = PipelineRunner.from_file(config).run()
            self.assertTrue(report.passed)
            self.assertTrue((root / "reports" / "demo-report.json").exists())
            self.assertTrue((root / "reports" / "demo-report.md").exists())
            self.assertIn("benchmark", report.to_markdown().lower())


if __name__ == "__main__":
    unittest.main()
