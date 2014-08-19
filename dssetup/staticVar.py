#coding=utf-8
SESSION_EXPIRATION = 1200
#权限组
ADMINISTRATOR = "administrator"  #管理者   拥有所有的权限
APPLICANT = "applicant"  #申请者 最普通的权限
GUEST = ""  #游客  目前 仅仅给 申请表单的权限 
#表单状态
CREATED = "created"  #意味着表单刚刚被创建  还没有进入流程   是不会在已申请表单列表里面出现的
WAITINGFORVERIFY = "unverified" #已经进入申请流程    等待被审核
VERIFIED = "verified"  #有被审核 等待被
OPERATED = "operated"  #已经被操作 等待被检查
CHECKED = "checked"    #已经被检查  等待被确认  
REJECTED = "rejected"  #被拒绝
CLOSED = "closed"      #关闭表单  被关闭的表弟 是不会在表单列表显示出来的
COMPLETED="completed"  #表单已经被确认  整个流程结束
#域名状态״̬
CAN_APPLY = "free"     #意味着域名 可以申请
CANNOT_APPLY = "occupied"  #域名正在被他人申请  所以目前不能申请

 
