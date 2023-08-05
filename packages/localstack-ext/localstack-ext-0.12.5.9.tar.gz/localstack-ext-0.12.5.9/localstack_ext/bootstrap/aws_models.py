from localstack.utils.aws import aws_models
iRXpD=super
iRXpJ=None
iRXpG=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  iRXpD(LambdaLayer,self).__init__(arn)
  self.cwd=iRXpJ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.iRXpG.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,iRXpG,env=iRXpJ):
  iRXpD(RDSDatabase,self).__init__(iRXpG,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,iRXpG,env=iRXpJ):
  iRXpD(RDSCluster,self).__init__(iRXpG,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,iRXpG,env=iRXpJ):
  iRXpD(AppSyncAPI,self).__init__(iRXpG,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,iRXpG,env=iRXpJ):
  iRXpD(AmplifyApp,self).__init__(iRXpG,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,iRXpG,env=iRXpJ):
  iRXpD(ElastiCacheCluster,self).__init__(iRXpG,env=env)
class TransferServer(BaseComponent):
 def __init__(self,iRXpG,env=iRXpJ):
  iRXpD(TransferServer,self).__init__(iRXpG,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,iRXpG,env=iRXpJ):
  iRXpD(CloudFrontDistribution,self).__init__(iRXpG,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,iRXpG,env=iRXpJ):
  iRXpD(CodeCommitRepository,self).__init__(iRXpG,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
