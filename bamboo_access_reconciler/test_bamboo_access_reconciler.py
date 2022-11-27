import unittest

from bamboo_access_reconciler import BambooAccessReconciler

class TestBambooAccessReconciler(unittest.TestCase):
    def setUp(self):
        self.bamboo_access_reconciler = BambooAccessReconciler()
        self.bamboo_access_reconciler.read_all_permissions_df_yaml('permissions.yaml')

    def test_get_global_permissions_df(self):
        global_permissions_df = self.bamboo_access_reconciler.get_global_permissions_df()
        self.assertIsNotNone(global_permissions_df)
        self.assertEqual(len(global_permissions_df.index), 2)
        self.assertEqual(len(global_permissions_df.columns), 4)
        self.assertEqual(global_permissions_df.columns[0], 'user')
        self.assertEqual(global_permissions_df.columns[1], 'group')
        self.assertEqual(global_permissions_df.columns[2], 'permission')
        self.assertEqual(global_permissions_df.columns[3], 'value')
        self.assertEqual(global_permissions_df['user'][0], 'admin')
        self.assertEqual(global_permissions_df['group'][0], None)
        self.assertEqual(global_permissions_df['permission'][0], 'ADMINISTER')
        self.assertEqual(global_permissions_df['value'][0], True)
        self.assertEqual(global_permissions_df['user'][1], 'admin')
        self.assertEqual(global_permissions_df['group'][1], None)
        self.assertEqual(global_permissions_df['permission'][1], 'ADMINISTER')
        self.assertEqual(global_permissions_df['value'][1], True)

    def test_get_build_plan_permissions_df(self):
        build_plan_permissions_df = self.bamboo_access_reconciler.get_build_plan_permissions_df()
        self.assertIsNotNone(build_plan_permissions_df)
        self.assertEqual(len(build_plan_permissions_df.index), 2)
        self.assertEqual(len(build_plan_permissions_df.columns), 4)
        self.assertEqual(build_plan_permissions_df.columns[0], 'user')
        self.assertEqual(build_plan_permissions_df.columns[1], 'group')
        self.assertEqual(build_plan_permissions_df.columns[2], 'permission')
        self.assertEqual(build_plan_permissions_df.columns[3], 'value')
        self.assertEqual(build_plan_permissions_df['user'][0], 'admin')
        self.assertEqual(build_plan_permissions_df['group'][0], None)
        self.assertEqual(build_plan_permissions_df['permission'][0], 'BUILD')
        self.assertEqual(build_plan_permissions_df['value'][0], True)
        self.assertEqual(build_plan_permissions_df['user'][1], 'admin')
        self.assertEqual(build_plan_permissions_df['group'][1], None)
        self.assertEqual(build_plan_permissions_df['permission'][1], 'BUILD')
        self.assertEqual(build_plan_permissions_df['value'][1], True)

    def test_get_project_permissions_df(self):
        project_permissions_df = self.bamboo_access_reconciler.get_project_permissions_df()
        self.assertIsNotNone(project_permissions_df)
        self.assertEqual(len(project_permissions_df.index), 2)
        self.assertEqual(len(project_permissions_df.columns), 4)
        self.assertEqual(project_permissions_df.columns[0], 'user')
        self.assertEqual(project_permissions_df.columns[1], 'group')
        self.assertEqual(project_permissions_df.columns[2], 'permission')
        self.assertEqual(project_permissions_df.columns[3], 'value')
        self.assertEqual(project_permissions_df['user'][0], 'admin')
        self.assertEqual(project_permissions_df['group'][0], None)
        self.assertEqual(project_permissions_df['permission'][0], 'ADMINISTER')
        self.assertEqual(project_permissions_df['value'][0], True)
        self.assertEqual(project_permissions_df['user'][1], 'admin')
        self.assertEqual(project_permissions_df['group'][1], None)
        self.assertEqual(project_permissions_df['permission'][1], 'ADMINISTER')
        self.assertEqual(project_permissions_df['value'][1], True)

    def test_get_repository_permissions_df(self):
        repository_permissions_df = self.bamboo_access_reconciler.get_repository_permissions_df()
        self.assertIsNotNone(repository_permissions_df)
        self.assertEqual(len(repository_permissions_df.index), 2)
        self.assertEqual(len(repository_permissions_df.columns), 4)
        self.assertEqual(repository_permissions_df.columns[0], 'user')
        self.assertEqual(repository_permissions_df.columns[1], 'group')
        self.assertEqual(repository_permissions_df.columns[2], 'permission')
        self.assertEqual(repository_permissions_df.columns[3], 'value')
        self.assertEqual(repository_permissions_df['user'][0], 'admin')
        self.assertEqual(repository_permissions_df['group'][0], None)
        self.assertEqual(repository_permissions_df['permission'][0], 'ADMINISTER')
        self.assertEqual(repository_permissions_df['value'][0], True)
        self.assertEqual(repository_permissions_df['user'][1], 'admin')
        self.assertEqual(repository_permissions_df['group'][1], None)
        self.assertEqual(repository_permissions_df['permission'][1], 'ADMINISTER')
        self.assertEqual(repository_permissions_df['value'][1], True)


class TestBambooAccessReconcilerWithGroups(BaseTestBambooAccessReconciler):
  
      def setUp(self):
          self.bamboo_access_reconciler = BambooAccessReconciler(
              bamboo_url='http://localhost:8085',
              bamboo_user='admin',
              bamboo_password='admin',
              group_permissions={
                  'group1': {
                      'bamboo': {
                          'ADMINISTER': True
                      },
                      'build_plan': {
                          'BUILD': True
                      },
                      'project': {
                          'ADMINISTER': True
                      },
                      'repository': {
                          'ADMINISTER': True
                      }
                  }
              }
          )
  
      def test_get_global_permissions_df(self):
          global_permissions_df = self.bamboo_access_reconciler.get_global_permissions_df()
          self.assertIsNotNone(global_permissions_df)
          self.assertEqual(len(global_permissions_df.index), 3)
          self.assertEqual(len(global_permissions_df.columns), 4)
          self.assertEqual(global_permissions_df.columns[0], 'user')
          self.assertEqual(global_permissions_df.columns[1], 'group')
          self.assertEqual(global_permissions_df.columns[2], 'permission')
          self.assertEqual(global_permissions_df.columns[3], 'value')
          self.assertEqual(global_permissions_df['user'][0], 'admin')
          self.assertEqual(global_permissions_df['group'][0], None)
          self.assertEqual(global_permissions_df['permission'][0], 'ADMINISTER')
          self.assertEqual(global_permissions_df['value'][0], True)
          self.assertEqual(global_permissions_df['user'][1], 'admin')
          self.assertEqual(global_permissions_df['group'][1], None)
          self.assertEqual(global_permissions_df['permission'][1], 'ADMINISTER')
          self.assertEqual(global_permissions_df['value'][1], True)
          self.assertEqual(global_permissions_df['user'][2], None)
          self.assertEqual(global_permissions_df['group'][2], 'group1')
          self.assertEqual(global_permissions_df['permission'][2], 'ADMINISTER')
          self.assertEqual(global_permissions_df['value'][2], True)
  
      def test_get_build_plan_permissions_df(self):
          build_plan_permissions_df = self.bamboo_access_reconciler.get_build_plan_permissions_df()
          self.assertIsNotNone(build_plan_permissions_df)
          self.assertEqual(len(build_plan_permissions_df.index), 3)
          self.assertEqual(len(build_plan_permissions_df.columns), 4)
          self.assertEqual(build_plan_permissions_df.columns[0], 'user')
          self.assertEqual(build_plan_permissions_df.columns[1], 'group')
          self.assertEqual(build_plan_permissions_df.columns[2], 'permission')
          self.assertEqual(build_plan_permissions_df.columns[3], 'value')
          self.assertEqual(build_plan_permissions_df['user'][0], 'admin')
          self.assertEqual(build_plan_permissions_df['group'][0], None)
          self.assertEqual(build_plan_permissions_df['permission'][0], 'ADMINISTER')
          self.assertEqual(build_plan_permissions_df['value'][0], True)
          self.assertEqual(build_plan_permissions_df['user'][1], 'admin')
          self.assertEqual(build_plan_permissions_df['group'][1], None)
          self.assertEqual(build_plan_permissions_df['permission'][1], 'ADMINISTER')
          self.assertEqual(build_plan_permissions_df['value'][1], True)
          self.assertEqual(build_plan_permissions_df['user'][2], None)
          self.assertEqual(build_plan_permissions_df['group'][2], 'group1')
          self.assertEqual(build_plan_permissions_df['permission'][2], 'BUILD')
          self.assertEqual(build_plan_permissions_df['value'][2], True)