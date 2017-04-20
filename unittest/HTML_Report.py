import sys
from Public import HTMLTestRunner
reload(sys)
sys.setdefaultencoding('utf-8')   #这里是为解决生成报告中文编码问题

now = time.strftime("%Y-%m-%d %H-%M-%S")
report_path = "testResult_TianchengUI_" + now + ".html"
fp = file(report_path, 'wb')
report_runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况：')

suite = unittest.TestSuite()
suite.addTest(TestFraudDetail("test_Fraud_001"))
suite.addTest(TestFraudDetail("test_Fraud_006"))
suite.addTest(TestFraudDetail("test_Fraud_007"))
report_runner.run(suite)
