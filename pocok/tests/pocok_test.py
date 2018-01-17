import git
import os
import yaml
from .abstract_test import AbstractTestSuite
from pocok.pocok import Pocok
from pocok.services.state import StateHolder


class ComposeTestSuite(AbstractTestSuite):

    def test_without_command(self):
        with self.assertRaises(SystemExit) as context:
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=[""])
            pocok.run()
        self.assertIsNotNone(context.exception)

"""
    def test_wrong_parameters(self):
        with self.assertRaises(DocoptExit) as context:
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["notexistcommand"])
            pocok.run()
        self.assertIsNotNone(context.exception)

    def test_config_without_config(self):
        with self.captured_output() as (out, err):
            with self.assertRaises(SystemExit) as context:
                pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "config"])
                pocok.run()
            self.assertIsNotNone(context.exception)
        self.assertIn("catalog config commands works only with config file.", out.getvalue().strip())

    def test_config(self):
        self.init_with_remote_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "config"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue()))
        self.assertIn(yaml.dump(data=AbstractTestSuite.REMOTE_CONFIG, default_flow_style=False, default_style='',
                                indent=4).strip(), out.getvalue().strip())

    def test_add_and_remove_config(self):
        self.init_with_remote_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "config", "add", "teszt", "ssh://teszt.teszt/teszt"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue()))
        data = dict()
        data["teszt"] = dict()
        data["teszt"]["repositoryType"] = "git"
        data["teszt"]["server"] = "ssh://teszt.teszt/teszt"

        self.assertIn(yaml.dump(data, default_flow_style=False, default_style='', indent=4).strip(),
                      out.getvalue().strip())
        self.clean_states()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "config", "remove", "teszt"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue()))
        self.assertNotIn("teszt", out.getvalue().strip())

    def test_list_with_local_config(self):
        self.init_with_local_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "ls"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue().strip()))
        for key in AbstractTestSuite.STACK_LIST_SAMPLE.keys():
            self.assertTrue(key in out.getvalue().strip())

    def test_list_with_remote_config(self):
        self.init_with_remote_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "ls"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue().strip()))
        for key in AbstractTestSuite.STACK_LIST_SAMPLE.keys():
            self.assertTrue(key in out.getvalue().strip())

    def test_branches_with_local_config(self):
        self.init_with_local_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "branches"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue().strip()))
        self.assertIn('Branch is not supported in this repository.', out.getvalue().strip())

    def test_branches_with_remote_config(self):
        self.init_with_remote_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "branches"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue().strip()))
        self.assertIn('Available branches in', out.getvalue().strip())
        self.assertIn('master', out.getvalue().strip())

    def test_switch_branch_with_local_config(self):
        self.init_with_local_catalog()
        with self.assertRaises(SystemExit) as context:
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "branch", "master"])
            pocok.run()
        self.assertEqual(1, context.exception.code)

    def test_switch_branch_with_remote_config(self):
        self.init_with_remote_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "branch", "master"])
            pocok.run()
        self.assertIn("Branch changed", out.getvalue())

    def test_push_with_local_config(self):
        self.init_with_local_catalog()
        StateHolder.skip_docker = True
        pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "push"])
        with self.captured_output() as (out, err):
            pocok.run()
        self.assertEqual(0, len(err.getvalue().strip()))
        self.assertIn("Push completed", out.getvalue())

    def test_add_and_remove(self):
        self.init_with_local_catalog()
        test_dir = os.path.join(self.tmpdir, "test-directory")
        os.makedirs(test_dir)
        git.Repo.clone_from(url=AbstractTestSuite.STACK_LIST_SAMPLE['nginx']['git'], to_path=test_dir)
        StateHolder.skip_docker = True
        pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "add", test_dir])
        with self.captured_output() as (out, err):
            pocok.run()
        self.assertIn("Project added", out.getvalue())
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "ls"])
            pocok.run()
            self.assertEqual(0, len(err.getvalue().strip()))
        for key in AbstractTestSuite.STACK_LIST_SAMPLE.keys():
            self.assertTrue(key in out.getvalue().strip())
        self.assertIn("test-directory", out.getvalue())
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "remove", "test-directory"])
            pocok.run()
        self.assertIn("Project removed", out.getvalue())
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "ls"])
            pocok.run()
            self.assertEqual(0, len(err.getvalue().strip()))
        for key in AbstractTestSuite.STACK_LIST_SAMPLE.keys():
            self.assertTrue(key in out.getvalue().strip())
        self.assertNotIn("test-directory", out.getvalue())

    def test_plan_list(self):
        self.init_with_local_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["plan", "ls", "mysql"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue()))
        self.assertIn("default", out.getvalue())

    def test_branches(self):
        self.init_with_local_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["branches", "mysql"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue()))
        self.assertIn("master", out.getvalue())

    def test_branch_without_change_branch(self):
        self.init_with_local_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["branch", "mysql", "master"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue()))
        self.assertIn("Branch changed", out.getvalue())

    def test_init(self):
        self.init_with_local_catalog()
        test_dir = os.path.join(self.tmpdir, "test-directory")
        os.makedirs(test_dir)
        git.Repo.clone_from(url=AbstractTestSuite.STACK_LIST_SAMPLE['nginx']['git'], to_path=test_dir)
        StateHolder.skip_docker = True
        pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "add", test_dir])
        with self.captured_output() as (out, err):
            pocok.run()
        self.assertIn("Project added", out.getvalue())
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["catalog", "ls"])
            pocok.run()
            self.assertEqual(0, len(err.getvalue().strip()))
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["init", "test-directory"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue()))
        self.assertIn("Project init completed", out.getvalue())
        self.assertTrue(os.path.exists(self.ws_dir))
        self.assertTrue(os.path.exists(os.path.join(self.ws_dir, "test-directory")))
        self.assertTrue(os.path.exists(os.path.join(self.ws_dir, "test-directory/pocok.yml")))
        self.assertTrue(os.path.exists(os.path.join(self.ws_dir, "test-directory/docker-compose.yml")))

    def test_install(self):
        self.init_with_local_catalog()
        with self.captured_output() as (out, err):
            StateHolder.skip_docker = True
            pocok = Pocok(home_dir=self.tmpdir, argv=["install", "mysql"])
            pocok.run()
        self.assertEqual(0, len(err.getvalue()))
        self.assertTrue(os.path.exists(self.ws_dir))
        self.assertTrue(os.path.exists(os.path.join(self.ws_dir, "pocok-example")))
"""